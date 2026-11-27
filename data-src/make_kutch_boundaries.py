"""Build the real boundaries used by new/explore.html: the Kutch district outline, its 10 talukas and its villages.

Usage:  python3 -I data-src/make_kutch_boundaries.py <cache-dir> new/data

Sources (downloaded once into <cache-dir>):
  - District and taluka boundaries: OpenStreetMap (ODbL) via the Overpass API – relation 8269590 "Kutch"
    and the admin_level 6 (taluka) relations inside it
  - Village boundaries: Census of India 2001 village maps, published by DataMeet (ODbL)
    https://github.com/datameet/indian_village_boundaries (gj/gj.geojson)

Writes boundaries.json, in the same scene coordinates as kutch.json (1 unit = 1 km, x east, z south),
stored as integers in units of 1/Q km to keep the file small:
  {"q": Q, "district": [ring, ...], "talukas": [{"n": name, "r": [ring, ...]}],
   "villages": [{"n": name, "t": taluka index, "r": [ring, ...]}]}
each ring being a flat list [x0, z0, x1, z1, ...].
"""
import json, math, os, sys, urllib.parse, urllib.request

CACHE, OUT = sys.argv[1], sys.argv[2]
os.makedirs(CACHE, exist_ok=True)
UA = {"User-Agent": "site-build-script/1.0"}
META = json.load(open(os.path.join(OUT, "kutch.json")))
Q = 50                                            # 1 unit = 20 m
TOL = {"district": .03, "taluka": .06, "village": .06}   # simplification tolerance, km


def get(url, name, data=None):
    path = os.path.join(CACHE, name)
    if not os.path.exists(path):
        req = urllib.request.Request(url, data=data, headers=UA)
        open(path, "wb").write(urllib.request.urlopen(req, timeout=300).read())
    return open(path, "rb").read()


def xz(lon, lat):
    return (lon - META["lonc"]) * META["kmx"], (META["latc"] - lat) * META["kmy"]


def simplify(pts, tol):
    """Douglas–Peucker on a closed ring of (x, z) points."""
    if len(pts) < 5:
        return pts
    keep = [False] * len(pts); keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        (ax, az), (bx, bz) = pts[a], pts[b]
        dx, dz = bx - ax, bz - az; L = math.hypot(dx, dz) or 1e-9
        best, bi = 0, -1
        for i in range(a + 1, b):
            px, pz = pts[i]
            d = abs(dx * (az - pz) - dz * (ax - px)) / L if (dx or dz) else math.hypot(px - ax, pz - az)
            if d > best: best, bi = d, i
        if best > tol:
            keep[bi] = True; stack += [(a, bi), (bi, b)]
    out = [p for p, k in zip(pts, keep) if k]
    return out if len(out) >= 4 else pts


def pack(ring_lonlat, tol):
    pts = [xz(lon, lat) for lon, lat in ring_lonlat]
    if pts[0] != pts[-1]: pts.append(pts[0])
    pts = simplify(pts, tol)
    flat = []
    for x, z in pts[:-1]:
        flat += [round(x * Q), round(z * Q)]
    return flat


def area(ring):
    return abs(sum(ring[i][0] * ring[i + 1][1] - ring[i + 1][0] * ring[i][1] for i in range(len(ring) - 1))) / 2


def join_ways(ways):
    """Assemble OSM member ways (lists of (lon, lat)) into closed rings."""
    ways = [w[:] for w in ways if len(w) > 1]
    rings = []
    while ways:
        ring = ways.pop(0)
        while ring[0] != ring[-1]:
            for i, w in enumerate(ways):
                if w[0] == ring[-1]: ring += w[1:]
                elif w[-1] == ring[-1]: ring += w[::-1][1:]
                elif w[-1] == ring[0]: ring = w + ring[1:]
                elif w[0] == ring[0]: ring = w[::-1] + ring[1:]
                else: continue
                ways.pop(i); break
            else:
                break                                  # open ring: OSM data incomplete here, drop it
        if ring[0] == ring[-1] and len(ring) > 3:
            rings.append(ring)
    return rings


# ---------- OpenStreetMap: district + talukas ----------
query = ('[out:json][timeout:240];rel(8269590);map_to_area->.k;'
         '(rel(area.k)["boundary"="administrative"]["admin_level"="6"];rel(8269590););out geom;')
osm = json.loads(get("https://overpass-api.de/api/interpreter", "osm-kutch-admin.json", urllib.parse.urlencode({"data": query}).encode()))
district, talukas = None, []
for rel in osm["elements"]:
    outer = [[(p["lon"], p["lat"]) for p in m["geometry"]] for m in rel.get("members", []) if m["type"] == "way" and m.get("role") in ("outer", "") and "geometry" in m]
    rings = sorted(join_ways(outer), key=area, reverse=True)
    if rel["id"] == 8269590:
        district = [pack(r, TOL["district"]) for r in rings if area(r) > 1e-5]
    else:
        talukas.append({"n": rel["tags"].get("name:en", rel["tags"]["name"]).replace(" Taluka", ""), "r": [pack(r, TOL["taluka"]) for r in rings if area(r) > 1e-5]})
talukas.sort(key=lambda t: t["n"])
tix = {t["n"].lower(): i for i, t in enumerate(talukas)}
print(len(talukas), "talukas:", ", ".join(t["n"] for t in talukas))

# ---------- DataMeet / Census 2001: villages ----------
gj = json.loads(get("https://raw.githubusercontent.com/datameet/indian_village_boundaries/master/gj/gj.geojson", "datameet-gj.geojson"))
villages = []
for f in gj["features"]:
    p = f["properties"]
    if not str(p.get("DISTRICT", "")).lower().startswith(("kachchh", "kutch")):
        continue
    polys = [f["geometry"]["coordinates"]] if f["geometry"]["type"] == "Polygon" else f["geometry"]["coordinates"]
    rings = [pack(poly[0], TOL["village"]) for poly in polys]
    villages.append({"n": " ".join(str(p["NAME"]).split()), "t": tix.get(str(p["SUB_DISTRICT"]).lower(), -1), "r": rings})
villages.sort(key=lambda v: (v["t"], v["n"]))
print(len(villages), "villages;", sum(v["t"] < 0 for v in villages), "with an unmatched taluka")

out = {"q": Q, "credits": "District and talukas © OpenStreetMap contributors (ODbL); villages: Census of India 2001 maps via DataMeet (ODbL)",
       "district": district, "talukas": talukas, "villages": villages}
path = os.path.join(OUT, "boundaries.json")
json.dump(out, open(path, "w"), separators=(",", ":"), ensure_ascii=False)
print("wrote", path, os.path.getsize(path) // 1024, "KB;", sum(len(r) // 2 for v in villages for r in v["r"]), "village points")
