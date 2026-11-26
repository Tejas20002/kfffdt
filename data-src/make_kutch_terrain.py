"""Build the real-Kutch terrain used by new/explore.html.

Usage:  python3 -I data-src/make_kutch_terrain.py <cache-dir> new/data

Sources (downloaded once into <cache-dir>):
  - Elevation: AWS Terrain Tiles (terrarium PNG, zoom 9; mostly NASA SRTM)
  - Land cover: ESA WorldCover 2021 v200 (10 m, CC BY 4.0) – the ~290 m overview level of the cloud-optimised GeoTIFFs
  - District boundary: OpenStreetMap relation 8269590 "Kutch" via Nominatim (ODbL)

Writes:
  kutch.bin  – per grid vertex: Int16 height (m), then Uint8 land-cover class, then Uint8 inside-Kutch flag
  kutch.json – grid geometry, boundary rings in scene km, place labels, credits
Scene coordinates: 1 unit = 1 km, x east, z south, origin at the grid centre.
"""
import json, math, os, struct, subprocess, sys, urllib.request, zlib
from collections import Counter

CACHE, OUT = sys.argv[1], sys.argv[2]
os.makedirs(CACHE, exist_ok=True); os.makedirs(OUT, exist_ok=True)
UA = {"User-Agent": "site-build-script/1.0"}

LON0, LON1, LAT_N, LAT_S = 68.0, 71.95, 24.85, 22.45          # grid extent (degrees)
LATC = (LAT_N + LAT_S) / 2
KX, KY = 111.32 * math.cos(math.radians(LATC)), 110.95          # km per degree
CELL = 1.6                                                       # km between grid vertices
DLON, DLAT = CELL / KX, CELL / KY
NX, NY = int(math.ceil((LON1 - LON0) / DLON)) + 1, int(math.ceil((LAT_N - LAT_S) / DLAT)) + 1
LONC = LON0 + (NX - 1) * DLON / 2
LATM = LAT_N - (NY - 1) * DLAT / 2


def get(url, name, headers=None):
    path = os.path.join(CACHE, name)
    if not os.path.exists(path):
        req = urllib.request.Request(url, headers={**UA, **(headers or {})})
        data = urllib.request.urlopen(req, timeout=120).read()
        open(path, "wb").write(data)
    return open(path, "rb").read()


def xz(lat, lon):
    return round((lon - LONC) * KX, 2), round((LATM - lat) * KY, 2)


# ---------- elevation (terrarium tiles, Web Mercator z9) ----------
Z = 9
def merc(lat, lon):
    n = 2 ** Z * 256
    s = math.sin(math.radians(lat))
    return (lon + 180) / 360 * n, (0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)) * n

px0, py0 = merc(LAT_N + .05, LON0 - .05); px1, py1 = merc(LAT_S - .05, LON1 + .05)
TX0, TY0, TX1, TY1 = int(px0 // 256), int(py0 // 256), int(px1 // 256), int(py1 // 256)
MW, MH = (TX1 - TX0 + 1) * 256, (TY1 - TY0 + 1) * 256
dem = [0.0] * (MW * MH)
for ty in range(TY0, TY1 + 1):
    for tx in range(TX0, TX1 + 1):
        png = os.path.join(CACHE, f"t{Z}_{tx}_{ty}.png")
        get(f"https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{Z}/{tx}/{ty}.png", f"t{Z}_{tx}_{ty}.png")
        raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", png, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
        ox, oy = (tx - TX0) * 256, (ty - TY0) * 256
        for y in range(256):
            row = (oy + y) * MW + ox
            for x in range(256):
                r, g, b = raw[(y * 256 + x) * 3: (y * 256 + x) * 3 + 3]
                dem[row + x] = r * 256 + g + b / 256 - 32768
print("elevation mosaic", MW, "x", MH)


def dem_at(lat, lon):
    x, y = merc(lat, lon); x -= TX0 * 256 + .5; y -= TY0 * 256 + .5
    x0, y0 = int(x), int(y); fx, fy = x - x0, y - y0
    x0 = min(max(x0, 0), MW - 2); y0 = min(max(y0, 0), MH - 2)
    a, b, c, d = dem[y0 * MW + x0], dem[y0 * MW + x0 + 1], dem[(y0 + 1) * MW + x0], dem[(y0 + 1) * MW + x0 + 1]
    return a * (1 - fx) * (1 - fy) + b * fx * (1 - fy) + c * (1 - fx) * fy + d * fx * fy


# ---------- land cover (ESA WorldCover overview level, 1125 px per 3 degrees) ----------
WC = {}
def read_cog_overview(url, name, want=1125):
    head = get(url, name + ".head", {"Range": "bytes=0-65535"})
    def rng(a, n):
        if a + n <= len(head): return head[a:a + n]
        return urllib.request.urlopen(urllib.request.Request(url, headers={**UA, "Range": f"bytes={a}-{a + n - 1}"}), timeout=120).read()
    TS = {1: 1, 3: 2, 4: 4, 16: 8}
    off = struct.unpack("<I", head[4:8])[0]
    while off:
        n = struct.unpack("<H", rng(off, 2))[0]
        ent = rng(off + 2, n * 12); tags = {}
        for i in range(n):
            tag, typ, cnt = struct.unpack("<HHI", ent[i * 12:i * 12 + 8]); val = ent[i * 12 + 8:i * 12 + 12]
            fmt = {1: "B", 3: "H", 4: "I", 16: "Q"}.get(typ)
            if fmt is None: continue
            raw = val[:TS[typ] * cnt] if TS[typ] * cnt <= 4 else rng(struct.unpack("<I", val)[0], TS[typ] * cnt)
            tags[tag] = struct.unpack("<" + fmt * cnt, raw)
        if tags[256][0] == want:
            W, T = tags[256][0], tags[322][0]
            assert tags[259][0] == 8 and tags.get(317, (1,))[0] == 1, "expected deflate, no predictor"
            per = math.ceil(W / T); img = bytearray(W * W)
            blob_path = os.path.join(CACHE, name + f".ov{W}")
            if os.path.exists(blob_path): return bytes(open(blob_path, "rb").read()), W
            for k, (o, c) in enumerate(zip(tags[324], tags[325])):
                if not c: continue
                tile = zlib.decompress(rng(o, c)); r0, c0 = (k // per) * T, (k % per) * T
                for y in range(T):
                    if r0 + y >= W: break
                    w = min(T, W - c0); img[(r0 + y) * W + c0:(r0 + y) * W + c0 + w] = tile[y * T:y * T + w]
            open(blob_path, "wb").write(img); return bytes(img), W
        off = struct.unpack("<I", rng(off + 2 + n * 12, 4))[0]
    raise SystemExit("overview not found in " + name)

for lat_s in (21, 24):
    for lon_w in (66, 69):
        t = f"N{lat_s:02d}E{lon_w:03d}"
        url = f"https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_{t}_Map.tif"
        WC[(lat_s, lon_w)] = read_cog_overview(url, "wc_" + t)
        print("land cover", t, "ok")


def wc_at(lat, lon):
    key = (21 if lat < 24 else 24, 66 if lon < 69 else 69)
    img, W = WC[key]
    r = int((key[0] + 3 - lat) / 3 * W); c = int((lon - key[1]) / 3 * W)
    return img[min(max(r, 0), W - 1) * W + min(max(c, 0), W - 1)]


# ---------- district boundary (OpenStreetMap) ----------
osm = json.loads(get("https://nominatim.openstreetmap.org/lookup?osm_ids=R8269590&format=json&polygon_geojson=1&polygon_threshold=0.002", "kutch_boundary.json"))
g = osm[0]["geojson"]
rings = [r for poly in (g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]) for r in poly]
print("boundary rings", len(rings), "points", sum(len(r) for r in rings))
boxes = [(min(p[0] for p in r), max(p[0] for p in r), min(p[1] for p in r), max(p[1] for p in r)) for r in rings]


def inside(lat, lon):
    hit = False
    for r, (a, b, c, d) in zip(rings, boxes):
        if not (a <= lon <= b and c <= lat <= d): continue
        j = len(r) - 1
        for i in range(len(r)):
            xi, yi = r[i]; xj, yj = r[j]
            if (yi > lat) != (yj > lat) and lon < (xj - xi) * (lat - yi) / (yj - yi) + xi: hit = not hit
            j = i
    return hit


# ---------- sample the grid ----------
H = []; C = []; IN = []
offs = [(-.32, -.32), (0, -.32), (.32, -.32), (-.32, 0), (0, 0), (.32, 0), (-.32, .32), (0, .32), (.32, .32)]
for j in range(NY):
    lat = LAT_N - j * DLAT
    for i in range(NX):
        lon = LON0 + i * DLON
        hs, cs = [], Counter()
        for fx, fy in offs:
            la, lo = lat + fy * DLAT, lon + fx * DLON
            hs.append(dem_at(la, lo)); cs[wc_at(la, lo)] += 1
        H.append(int(round(sum(hs) / len(hs)))); C.append(cs.most_common(1)[0][0]); IN.append(1 if inside(lat, lon) else 0)
    if j % 40 == 0: print("row", j, "/", NY)

with open(os.path.join(OUT, "kutch.bin"), "wb") as f:
    f.write(struct.pack("<%dh" % len(H), *[max(-32768, min(32767, h)) for h in H]))
    f.write(bytes(C)); f.write(bytes(IN))

# highest point of the Kala Dungar hills (northern Kutch) for its label
best = max(((dem_at(23.7 + a * .01, 69.6 + b * .01), 23.7 + a * .01, 69.6 + b * .01) for a in range(35) for b in range(45)))
PLACES = [  # name, lat, lon, kind
    ("Bhuj", 23.242, 69.667, "town"), ("Gandhidham", 23.075, 70.134, "town"), ("Anjar", 23.114, 70.028, "town"), ("Mandvi", 22.834, 69.353, "town"),
    ("Mundra", 22.839, 69.721, "town"), ("Bhachau", 23.296, 70.343, "town"), ("Rapar", 23.572, 70.643, "town"), ("Nakhatrana", 23.350, 69.264, "town"),
    ("Naliya", 23.260, 68.827, "town"), ("Lakhpat", 23.826, 68.777, "town"), ("Dholavira", 23.887, 70.213, "town"), ("Khavda", 23.850, 69.720, "town"),
    ("Kala Dungar", best[1], best[2], "peak"),
    ("Great Rann of Kutch", 24.18, 69.95, "region"), ("Little Rann", 23.42, 71.18, "region"), ("Banni grassland", 23.66, 69.45, "region"),
    ("Gulf of Kutch", 22.66, 69.95, "water"), ("Arabian Sea", 22.95, 68.32, "water"),
]
meta = dict(
    nx=NX, ny=NY, cell=CELL, lon0=LON0, latN=LAT_N, dlon=DLON, dlat=DLAT, kmx=KX, kmy=KY, lonc=LONC, latc=LATM,
    boundary=[[xz(p[1], p[0]) for p in r] for r in rings],
    places=[dict(name=n, kind=k, x=xz(la, lo)[0], z=xz(la, lo)[1]) for n, la, lo, k in PLACES],
    peak_m=round(best[0]),
    classes={"10": "tree cover", "20": "shrubland", "30": "grassland", "40": "cropland", "50": "built-up", "60": "bare / sparse", "80": "water", "90": "herbaceous wetland", "95": "mangroves"},
    credits="Terrain: AWS Terrain Tiles (NASA SRTM and others) · Land cover: ESA WorldCover 2021, CC BY 4.0 · District boundary: © OpenStreetMap contributors, ODbL",
)
json.dump(meta, open(os.path.join(OUT, "kutch.json"), "w"), separators=(",", ":"))
cnt = Counter(c for c, f in zip(C, IN) if f)
print("grid", NX, "x", NY, "| inside Kutch:", sum(IN), "vertices | classes inside:", dict(cnt.most_common()))
print("height range m:", min(H), max(H), "| Kala Dungar peak ~", round(best[0]), "m at", round(best[1], 3), round(best[2], 3))
