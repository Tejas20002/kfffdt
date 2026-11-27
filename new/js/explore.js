// Explore Kutch in 3D – the real shape of Kutch with the Trust's programs as spatial pins.
// Pick a program and only its projects, events and centres appear; pick a month and the land changes with the season.
// Ground: data/kutch.bin + data/kutch.json, built by data-src/make_kutch_terrain.py from NASA SRTM heights
// (AWS Terrain Tiles), ESA WorldCover 2021 land cover and the OpenStreetMap district boundary.
// 1 scene unit = 1 km; heights are exaggerated so the low hills read. Programs, items and months come from #x3d-data
// (X3D, X3D_ITEMS and X3D_MONTHS in build_new.py).
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const stage = document.getElementById('x3d');
const DATA = JSON.parse(document.getElementById('x3d-data').textContent);
const PROG = DATA.programs, ITEMS = DATA.items, TYPES = DATA.types, MONTHS = DATA.months;
const REDUCE = matchMedia('(prefers-reduced-motion: reduce)').matches;
const q = s => stage.querySelector(s);

init().catch(e => { console.error(e); stage.classList.add('nogl'); });

async function init() {
  if (!document.createElement('canvas').getContext('webgl2')) throw new Error('WebGL2 not available');
  const [meta, buf, BND] = await Promise.all([
    fetch('data/kutch.json').then(r => { if (!r.ok) throw new Error('terrain meta ' + r.status); return r.json(); }),
    fetch('data/kutch.bin').then(r => { if (!r.ok) throw new Error('terrain data ' + r.status); return r.arrayBuffer(); }),
    fetch('data/boundaries.json').then(r => { if (!r.ok) throw new Error('boundaries ' + r.status); return r.json(); }),
  ]);

  // ---------------- helpers ----------------
  const rng = seed => () => { seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  const R = rng(1989);
  const hash = (x, y) => { const s = Math.sin(x * 127.1 + y * 311.7) * 43758.5453; return s - Math.floor(s); };
  const sstep = (a, b, x) => { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); };
  const ease = k => k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
  const col = h => new THREE.Color(h);

  // ---------------- real terrain grid ----------------
  const NX = meta.nx, NY = meta.ny, N = NX * NY, CELL = meta.cell;
  const HM = new Int16Array(buf, 0, N), CL = new Uint8Array(buf, N * 2, N), IN = new Uint8Array(buf, N * 3, N);
  const X0 = -(NX - 1) * CELL / 2, Z0 = -(NY - 1) * CELL / 2;
  const ZS = .032;                                                      // scene units per metre (~32x exaggeration)
  const SEA_Y = -.9;   // water level: dry land never sits below .12, so Kutch stands about a unit proud of its flat surroundings
  const SEA0 = new Uint8Array(N), SEA = new Uint8Array(N);
  for (let k = 0; k < N; k++) SEA0[k] = (CL[k] === 80 || CL[k] === 0) && HM[k] <= -1 ? 1 : 0;
  for (let k = 0; k < N; k++) {   // drop isolated one- or two-cell "sea" pits inland: they are Rann depressions, not sea
    if (!SEA0[k]) continue;
    const i = k % NX, j = Math.floor(k / NX); let n = 0;
    for (let b = -1; b <= 1; b++) for (let a = -1; a <= 1; a++) { const ii = i + a, jj = j + b; if (a || b) n += ii >= 0 && jj >= 0 && ii < NX && jj < NY ? SEA0[jj * NX + ii] : 1; }
    SEA[k] = n >= 3 ? 1 : 0;
  }
  const isSea = k => SEA[k] === 1;
  const HY = new Float32Array(N);
  for (let k = 0; k < N; k++) HY[k] = isSea(k) ? Math.max(-3.4, Math.min(-1.3, -1.3 + Math.min(HM[k], 0) * ZS * .5)) : Math.max(.12, HM[k] * ZS);

  // real boundaries (boundaries.json): district + talukas from OpenStreetMap, villages from the Census 2001 maps (DataMeet)
  const BQ = BND.q, ringPts = r => { const o = []; for (let i = 0; i < r.length; i += 2) o.push([r[i] / BQ, r[i + 1] / BQ]); return o; };
  const bboxOf = rings => { let x0 = 1e9, x1 = -1e9, z0 = 1e9, z1 = -1e9; for (const r of rings) for (const [x, z] of r) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (z < z0) z0 = z; if (z > z1) z1 = z; } return { x0, x1, z0, z1 }; };
  const DIST = BND.district.map(ringPts);
  const TAL = BND.talukas.map(t => ({ n: t.n, rings: t.r.map(ringPts) }));
  const VIL = BND.villages.map(v => { const rings = v.r.map(ringPts); return { n: v.n, t: v.t, rings, b: bboxOf(rings) }; });
  const ll = (lat, lon) => ({ x: (lon - meta.lonc) * meta.kmx, z: (meta.latc - lat) * meta.kmy });
  const near = (x, z) => { const i = Math.round((x - X0) / CELL), j = Math.round((z - Z0) / CELL); return Math.min(Math.max(j, 0), NY - 1) * NX + Math.min(Math.max(i, 0), NX - 1); };
  function height(x, z) {
    const fi = Math.min(Math.max((x - X0) / CELL, 0), NX - 1.001), fj = Math.min(Math.max((z - Z0) / CELL, 0), NY - 1.001);
    const i = Math.floor(fi), j = Math.floor(fj), u = fi - i, v = fj - j, k = j * NX + i;
    return HY[k] * (1 - u) * (1 - v) + HY[k + 1] * u * (1 - v) + HY[k + NX] * (1 - u) * v + HY[k + NX + 1] * u * v;
  }
  const landAt = (x, z) => { const k = near(x, z); return IN[k] === 1 && !isSea(k) && CL[k] !== 80; };
  const S = Object.fromEntries(PROG.map(d => { const p = ll(d.lat, d.lon); return [d.id, { d, x: p.x, z: p.z }]; }));

  // district centre for the home view
  let bx0 = 1e9, bx1 = -1e9, bz0 = 1e9, bz1 = -1e9;
  for (const ring of DIST) for (const [x, z] of ring) { bx0 = Math.min(bx0, x); bx1 = Math.max(bx1, x); bz0 = Math.min(bz0, z); bz1 = Math.max(bz1, z); }
  const HOME_TGT = new THREE.Vector3((bx0 + bx1) / 2 - 8, 0, (bz0 + bz1) / 2 + 24);
  const HOME_POS = HOME_TGT.clone().add(new THREE.Vector3(0, 250, 235));

  // ---------------- renderer, scene, camera ----------------
  const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 1.75));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  renderer.setClearColor('#cfe0e6');
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.domElement.setAttribute('aria-label', '3D view of Kutch built from real terrain and land-cover data. Use the program buttons below and the month list on the side to explore.');
  renderer.domElement.setAttribute('role', 'img');
  stage.prepend(renderer.domElement);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(40, 1, 1, 3200);
  camera.position.copy(REDUCE ? HOME_POS : HOME_TGT.clone().add(new THREE.Vector3(-90, 540, 660)));

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.target.copy(HOME_TGT);
  Object.assign(controls, { enableDamping: true, dampingFactor: .07, minDistance: 22, maxDistance: 560, minPolarAngle: .2, maxPolarAngle: 1.22, screenSpacePanning: false, autoRotateSpeed: .3, rotateSpeed: .6 });
  const LIM = { x: (NX - 1) * CELL / 2 - 20, z: (NY - 1) * CELL / 2 - 15 };
  controls.addEventListener('change', () => {
    controls.target.x = THREE.MathUtils.clamp(controls.target.x, -LIM.x, LIM.x);
    controls.target.z = THREE.MathUtils.clamp(controls.target.z, -LIM.z, LIM.z);
    controls.target.y = THREE.MathUtils.clamp(controls.target.y, 0, 14);
  });

  // sky dome + fog
  const SKY = { dryTop: col('#86bfe3'), dryBot: col('#f3e4c6'), wetTop: col('#7f95a8'), wetBot: col('#e1e6e1') };
  const skyU = { top: { value: SKY.dryTop.clone() }, bot: { value: SKY.dryBot.clone() } };
  const sky = new THREE.Mesh(new THREE.SphereGeometry(1500, 32, 16), new THREE.ShaderMaterial({
    side: THREE.BackSide, depthWrite: false, fog: false, uniforms: skyU,
    vertexShader: 'varying vec3 vp; void main(){ vp = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
    fragmentShader: 'uniform vec3 top; uniform vec3 bot; varying vec3 vp; void main(){ float h = clamp(vp.y * 1.5 + .06, 0., 1.); gl_FragColor = vec4(mix(bot, top, pow(h, .75)), 1.);\n#include <colorspace_fragment>\n}',
  }));
  scene.add(sky);
  scene.fog = new THREE.Fog(SKY.dryBot.clone(), 420, 1300);

  const hemi = new THREE.HemisphereLight('#fff4dc', '#8a7552', 1.15);
  const sun = new THREE.DirectionalLight('#ffe6bd', 2.7);
  sun.position.copy(HOME_TGT).add(new THREE.Vector3(170, 260, 120)); sun.target.position.copy(HOME_TGT);
  sun.castShadow = true;
  Object.assign(sun.shadow.camera, { left: -240, right: 240, top: 200, bottom: -200, near: 20, far: 700 });
  sun.shadow.mapSize.set(2048, 2048);
  sun.shadow.bias = -.0004; sun.shadow.normalBias = .04;
  scene.add(hemi, sun, sun.target);

  // tanks sit on a levelled pad (lowest nearby ground) so they never float on a slope
  const TANKS = [[S.jal, 0, 0, 2.6], [S.jal, 7, 5, 1.6], [S.jal, -6, 6, 1.4], [S.jal, 4, -7, 1.5], [S.water, 0, 0, 2.3, true], [S.water, -6, 4, 1.4], [S.fodder, 8, -6, 1.5], [S.drink, -7, -5, 1.6], [S.animal, -6, -6, 1.4], [S.school, -6, 5, 1.4]]
    .map(([s, dx, dz, r, dam]) => ({ x: s.x + dx, z: s.z + dz, r, dam })).filter(t => landAt(t.x, t.z));
  for (const t of TANKS) {
    const rr = t.r + CELL * 1.1, ks = [];
    const i0 = Math.max(0, Math.floor((t.x - rr - X0) / CELL)), i1 = Math.min(NX - 1, Math.ceil((t.x + rr - X0) / CELL));
    const j0 = Math.max(0, Math.floor((t.z - rr - Z0) / CELL)), j1 = Math.min(NY - 1, Math.ceil((t.z + rr - Z0) / CELL));
    for (let j = j0; j <= j1; j++) for (let i = i0; i <= i1; i++) if (Math.hypot(X0 + i * CELL - t.x, Z0 + j * CELL - t.z) <= rr) ks.push(j * NX + i);
    const base = Math.min(...ks.map(k => HY[k]));
    for (const k of ks) HY[k] = base;
    t.y = base + .12;
  }

  // ---------------- terrain mesh: real heights, colours from real land cover ----------------
  let geo = new THREE.PlaneGeometry((NX - 1) * CELL, (NY - 1) * CELL, NX - 1, NY - 1);
  geo.rotateX(-Math.PI / 2);
  const pa = geo.attributes.position;
  for (let k = 0; k < N; k++) pa.setY(k, HY[k]);
  geo = geo.toNonIndexed();
  geo.computeVertexNormals();
  const PAL = {   // [summer, monsoon, winter]
    sea: ['#b7a57c', '#b7a57c', '#b7a57c'], rann: ['#efece4', '#d3e5e2', '#f8f7f3'], rannW: ['#e0dacb', '#8fc2d6', '#eef0ec'], bare: ['#c9ac80', '#b8a67c', '#c3ab84'],
    crop: ['#cfae74', '#86b55e', '#b9b766'], shrub: ['#a99a5e', '#5f9047', '#8a9656'], grass: ['#d2bf80', '#95c262', '#c8bf7a'], tree: ['#5a7d42', '#356f38', '#4c7a40'],
    built: ['#cbbfae', '#c2b8a8', '#cfc5b6'], wet: ['#aaae8b', '#6fae94', '#94b49c'], mangr: ['#3d6a4c', '#2b6b47', '#346a4a'],
  };
  for (const k in PAL) PAL[k] = PAL[k].map(col);
  const CLASS = { 10: 'tree', 20: 'shrub', 30: 'grass', 40: 'crop', 50: 'built', 90: 'wet', 95: 'mangr' };
  const kind = k => { const c = CL[k], h = HM[k]; if (isSea(k)) return 'sea'; if (c === 80 || c === 0) return 'rannW'; if (c === 60) return h < 25 ? 'rann' : 'bare'; return CLASS[c] || 'bare'; };
  const P = geo.attributes.position.array, nv = geo.attributes.position.count;
  const tC = new THREE.Color();
  const perPoint = [0, 1, 2].map(() => new Float32Array(N * 3));   // one colour per grid point and season, blended across each triangle
  for (let k = 0; k < N; k++) {
    const kd = kind(k), f = kd === 'crop' ? .88 + hash(k * .37, 1.3) * .2 : .96 + hash(k * .21, 7.1) * .07;   // farm patchwork
    for (let si = 0; si < 3; si++) {
      tC.copy(PAL[kd][si]);
      perPoint[si].set([tC.r * f, tC.g * f, tC.b * f], k * 3);
    }
  }
  const perVert = [0, 1, 2].map(() => new Float32Array(nv * 3));
  for (let v = 0; v < nv; v++) { const k = near(P[v * 3], P[v * 3 + 2]); for (let si = 0; si < 3; si++) perVert[si].set(perPoint[si].subarray(k * 3, k * 3 + 3), v * 3); }
  geo.setAttribute('color', new THREE.BufferAttribute(perVert[0], 3));
  geo.setAttribute('color2', new THREE.BufferAttribute(perVert[1], 3));
  geo.setAttribute('color3', new THREE.BufferAttribute(perVert[2], 3));
  const seasonU = { value: new THREE.Vector3(1, 0, 0) };   // weights: summer, monsoon, winter
  // the land is cut exactly along the OpenStreetMap district outline: a mask of the outline is tested for every pixel
  const CB = bboxOf(DIST); CB.x0 -= 2; CB.z0 -= 2; CB.x1 += 2; CB.z1 += 2;
  const CW = 2560, CH = Math.round(CW * (CB.z1 - CB.z0) / (CB.x1 - CB.x0)), cS = CW / (CB.x1 - CB.x0);
  const cutTex = (() => {
    const cv = document.createElement('canvas'); cv.width = CW; cv.height = CH;
    const g = cv.getContext('2d'); g.fillStyle = '#fff'; g.beginPath();
    for (const r of DIST) { r.forEach(([x, z], i) => g[i ? 'lineTo' : 'moveTo']((x - CB.x0) * cS, (z - CB.z0) * cS)); g.closePath(); }
    g.fill();
    const d = g.getImageData(0, 0, CW, CH).data, a = new Uint8Array(CW * CH);
    for (let i = 0; i < a.length; i++) a[i] = d[i * 4];
    const t = new THREE.DataTexture(a, CW, CH, THREE.RedFormat, THREE.UnsignedByteType);
    t.unpackAlignment = 1; t.magFilter = t.minFilter = THREE.LinearFilter; t.needsUpdate = true; return t;
  })();
  // project villages are painted onto the ground from a small canvas (see drawHi)
  const HIN = 1536, hiCanvas = document.createElement('canvas'); hiCanvas.width = hiCanvas.height = HIN;
  const hiTex = new THREE.CanvasTexture(hiCanvas); hiTex.colorSpace = THREE.SRGBColorSpace; hiTex.flipY = false; hiTex.anisotropy = 4;
  const terrU = { uSeasonW: seasonU, uCut: { value: cutTex }, uCutBox: { value: new THREE.Vector4(CB.x0, CB.z0, 1 / (CB.x1 - CB.x0), 1 / (CB.z1 - CB.z0)) }, uHi: { value: hiTex }, uHiBox: { value: new THREE.Vector4(0, 0, 0, 0) } };
  const terrainMat = new THREE.MeshStandardMaterial({ vertexColors: true, flatShading: true, roughness: 1, metalness: 0 });
  terrainMat.onBeforeCompile = sh => {   // blend the three season palettes on the GPU, cut to the district, paint highlights
    Object.assign(sh.uniforms, terrU);
    sh.vertexShader = 'attribute vec3 color2;\nattribute vec3 color3;\nuniform vec3 uSeasonW;\nvarying vec2 vXZ;\n' + sh.vertexShader
      .replace('#include <color_vertex>', '#include <color_vertex>\n  vColor.rgb = color.rgb * uSeasonW.x + color2 * uSeasonW.y + color3 * uSeasonW.z;')
      .replace('#include <begin_vertex>', '#include <begin_vertex>\n  vXZ = position.xz;');
    sh.fragmentShader = 'uniform sampler2D uCut;\nuniform vec4 uCutBox;\nuniform sampler2D uHi;\nuniform vec4 uHiBox;\nvarying vec2 vXZ;\n' + sh.fragmentShader
      .replace('#include <clipping_planes_fragment>', '#include <clipping_planes_fragment>\n  if (texture2D(uCut, (vXZ - uCutBox.xy) * uCutBox.zw).r < .5) discard;')
      .replace('#include <color_fragment>', '#include <color_fragment>\n  vec2 hu = (vXZ - uHiBox.xy) * uHiBox.zw;\n  if (hu.x > 0. && hu.x < 1. && hu.y > 0. && hu.y < 1.) { vec4 hc = texture2D(uHi, hu); diffuseColor.rgb = mix(diffuseColor.rgb, hc.rgb, hc.a); }');
  };
  const terrain = new THREE.Mesh(geo, terrainMat);
  terrain.receiveShadow = true;
  scene.add(terrain);

  // exact height of the terrain surface (the same two triangles per grid cell as the mesh), so lines lie right on it
  function surf(x, z) {
    const fi = Math.min(Math.max((x - X0) / CELL, 0), NX - 1.0001), fj = Math.min(Math.max((z - Z0) / CELL, 0), NY - 1.0001);
    const i = Math.floor(fi), j = Math.floor(fj), u = fi - i, v = fj - j, k = j * NX + i;
    return u + v <= 1 ? HY[k] + (HY[k + 1] - HY[k]) * u + (HY[k + NX] - HY[k]) * v
      : HY[k + NX + 1] + (HY[k + NX] - HY[k + NX + 1]) * (1 - u) + (HY[k + 1] - HY[k + NX + 1]) * (1 - v);
  }
  // drape a ring on the terrain: split every edge where it crosses a grid line or a cell diagonal -> flat [x, y, z, ...] polyline
  function drapeRing(pts, off) {
    const out = [], n = pts.length, ts = [];
    const cross = (p, q) => { if (p === q) return; const lo = Math.min(p, q), hi = Math.max(p, q); for (let g = Math.floor(lo) + 1; g < hi; g++) ts.push((g - p) / (q - p)); };
    for (let s = 0; s < n; s++) {
      const [x1, z1] = pts[s], [x2, z2] = pts[(s + 1) % n];
      const a1 = (x1 - X0) / CELL, b1 = (z1 - Z0) / CELL, a2 = (x2 - X0) / CELL, b2 = (z2 - Z0) / CELL;
      ts.length = 0; ts.push(0); cross(a1, a2); cross(b1, b2); cross(a1 + b1, a2 + b2); ts.sort((p, q) => p - q);
      for (const t of ts) { const x = x1 + (x2 - x1) * t, z = z1 + (z2 - z1) * t; out.push(x, surf(x, z) + off, z); }
    }
    const [x, z] = pts[0]; out.push(x, surf(x, z) + off, z);
    return out;
  }
  const toSegments = (polys) => { let n = 0; for (const p of polys) n += p.length - 3; const a = new Float32Array(n * 2); let o = 0; for (const p of polys) for (let i = 0; i + 5 < p.length; i += 3) { a.set(p.subarray ? p.subarray(i, i + 6) : p.slice(i, i + 6), o); o += 6; } return a; };
  const lineMesh = (polys, mat, order) => { const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(toSegments(polys), 3)); const l = new THREE.LineSegments(g, mat); l.renderOrder = order; l.frustumCulled = false; scene.add(l); return l; };

  // ---------------- around Kutch: open ocean out to the horizon ----------------
  const seaMat = new THREE.MeshStandardMaterial({ color: '#3d8db7', roughness: .3, metalness: .05, flatShading: true });
  const seaGeo = new THREE.PlaneGeometry(NX * CELL + 160, NY * CELL + 160, 110, 80); seaGeo.rotateX(-Math.PI / 2); seaGeo.translate(0, SEA_Y, 0);
  const seaMesh = new THREE.Mesh(seaGeo, seaMat); scene.add(seaMesh);   // gentle low-poly waves near Kutch
  const seaPos = seaGeo.attributes.position;
  const farSea = new THREE.Mesh(new THREE.PlaneGeometry(7000, 7000).rotateX(-Math.PI / 2), seaMat);   // calm water beyond, fading into the haze
  farSea.position.y = SEA_Y - .15; scene.add(farSea);

  // the cut edge: an earth wall along the district outline, down below the water line
  const wallP = [], wallC = [], wTop = col('#a07a52'), wBot = col('#5d4530');
  for (const ring of DIST) {
    const p = drapeRing(ring, 0), yb = SEA_Y - 1;
    for (let i = 0; i + 5 < p.length; i += 3) {
      const [ax, ay, az, bx, by, bz] = p.slice(i, i + 6);
      wallP.push(ax, ay, az, ax, yb, az, bx, by, bz, bx, by, bz, ax, yb, az, bx, yb, bz);
      wallC.push(...[wTop, wBot, wTop, wTop, wBot, wBot].flatMap(c => [c.r, c.g, c.b]));
    }
  }
  const wallG = new THREE.BufferGeometry(); wallG.setAttribute('position', new THREE.Float32BufferAttribute(wallP, 3)); wallG.setAttribute('color', new THREE.Float32BufferAttribute(wallC, 3)); wallG.computeVertexNormals();
  const wall = new THREE.Mesh(wallG, new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, roughness: 1, flatShading: true }));
  wall.castShadow = wall.receiveShadow = true; scene.add(wall);

  // district outline (dashed), taluka boundaries, and village boundaries that appear as you zoom in
  const bMat = new THREE.LineDashedMaterial({ color: '#d4932f', dashSize: 2.2, gapSize: 1.3 });
  for (const ring of DIST) { const p = drapeRing(ring, .2), g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(p, 3)); const l = new THREE.Line(g, bMat); l.computeLineDistances(); l.renderOrder = 4; scene.add(l); }
  const talMat = new THREE.LineBasicMaterial({ color: '#5b4a33', transparent: true, opacity: .55, depthWrite: false });
  lineMesh(TAL.flatMap(t => t.rings.map(r => drapeRing(r, .16))), talMat, 3);
  const vilMat = new THREE.LineBasicMaterial({ color: '#2f2c24', transparent: true, opacity: 0, depthWrite: false });
  const vilLines = lineMesh(VIL.flatMap(v => v.rings.map(r => drapeRing(r, .12))), vilMat, 3); vilLines.visible = false;
  const hoverMat = new THREE.LineBasicMaterial({ color: '#ffffff', transparent: true, opacity: .95, depthWrite: false, depthTest: false });

  // ---------------- props ----------------
  const M = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, flatShading: true, roughness: .9, ...o });
  const mats = { trunk: M('#7a5634'), crown: M('#7f9150'), shrub: M('#9a9256'), mangr: M('#2f5e43'), hut: M('#f3ede2'), thatch: M('#a7773f'), wall: M('#efe6d6'), city: M('#e6ddce'), tile: M('#b9563a'),
    concrete: M('#c9c1b0'), steel: M('#9aa7ad'), tankTop: M('#dfe8ec'), crop: M('#cdb77a'), bale: M('#e2b55a'), fruit: M('#e98b2a', { roughness: .6 }), cowW: M('#f1ece4'), cowB: M('#8a5a3c'), dark: M('#3a3a36'),
    flag: M('#e98b2a', { side: THREE.DoubleSide }), bed: M('#8a6a48'), bund: M('#a88a5c') };
  const dummy = new THREE.Object3D();
  function instanced(geom, mat, list, cast = true) {
    const m = new THREE.InstancedMesh(geom, mat, Math.max(1, list.length)); m.count = list.length;
    list.forEach((p, i) => { dummy.position.set(p.x, p.y, p.z); dummy.rotation.set(0, p.ry || 0, 0); dummy.scale.setScalar(p.s || 1); if (p.sy) dummy.scale.y = (p.s || 1) * p.sy; dummy.updateMatrix(); m.setMatrixAt(i, dummy.matrix); });
    m.castShadow = cast; m.receiveShadow = true; scene.add(m); return m;
  }
  const cellXZ = k => ({ x: X0 + (k % NX) * CELL, z: Z0 + Math.floor(k / NX) * CELL });

  // vegetation and towns straight from the land-cover grid (inside Kutch)
  const trees = [], bushes = [], mangroves = [], blds = [];
  for (let k = 0; k < N; k++) {
    if (!IN[k]) continue;
    const c = CL[k], { x: gx, z: gz } = cellXZ(k);
    const put = (arr, n, s0, s1, extra = {}) => { for (let m = 0; m < n; m++) { const x = gx + (R() - .5) * 1.5, z = gz + (R() - .5) * 1.5; arr.push({ x, z, y: height(x, z) - .05, s: s0 + R() * (s1 - s0), ry: R() * 6, ...extra }); } };
    if (c === 10) put(trees, 2, .7, 1);
    else if (c === 95) put(mangroves, 2, .45, .65, { sy: .55 });
    else if (c === 20 && R() < .16) put(bushes, 1, .4, .6, { sy: .75 });
    else if ((c === 40 || c === 30) && R() < .025) put(trees, 1, .6, .85);
    else if (c === 50) for (let m = 0; m < 5; m++) { const x = gx + (R() - .5) * 1.5, z = gz + (R() - .5) * 1.5; blds.push({ x, z, y: height(x, z) - .05, s: .42 + R() * .3, sy: .7 + R() * 1.6, ry: R() * .5 }); }
  }
  // the planted forest near Bhuj
  for (let i = 0; i < 70; i++) {
    const a = R() * Math.PI * 2, r = 2.5 + Math.sqrt(R()) * 8, x = S.forest.x + Math.cos(a) * r, z = S.forest.z + Math.sin(a) * r;
    if (landAt(x, z)) trees.push({ x, z, y: height(x, z) - .05, s: .7 + R() * .4, ry: R() * 6 });
  }
  const trunkG = new THREE.CylinderGeometry(.18, .3, 1.7, 5); trunkG.translate(0, .85, 0);
  const crownG = new THREE.IcosahedronGeometry(1.3, 0); crownG.translate(0, 2.4, 0);
  const bushG = new THREE.IcosahedronGeometry(1.3, 0); bushG.translate(0, 1, 0);
  instanced(trunkG, mats.trunk, trees); instanced(crownG, mats.crown, trees);
  instanced(bushG, mats.shrub, bushes); instanced(bushG, mats.mangr, mangroves);
  const bldG = new THREE.BoxGeometry(1, 1, 1); bldG.translate(0, .5, 0);
  instanced(bldG, mats.city, blds);

  // tanks (Jal Mandir and check-dam ponds): dry bed + earth bund + water that rises with the monsoon
  const waterMat = new THREE.MeshStandardMaterial({ color: '#3b97cf', roughness: .15, metalness: .05, transparent: true, opacity: .93 });
  const waters = TANKS.map(t => {
    const bed = new THREE.Mesh(new THREE.CircleGeometry(t.r, 28), mats.bed); bed.rotation.x = -Math.PI / 2; bed.position.set(t.x, t.y, t.z); bed.receiveShadow = true;
    const bund = new THREE.Mesh(new THREE.TorusGeometry(t.r + .15, .32, 6, 32), mats.bund); bund.rotation.x = -Math.PI / 2; bund.scale.z = .7; bund.position.set(t.x, t.y + .05, t.z); bund.castShadow = bund.receiveShadow = true;
    const w = new THREE.Mesh(new THREE.CircleGeometry(t.r * .96, 28), waterMat); w.rotation.x = -Math.PI / 2; w.position.set(t.x, t.y - .1, t.z);
    scene.add(bed, bund, w);
    if (t.dam) { const dam = new THREE.Mesh(new THREE.BoxGeometry(t.r * 2.2, .9, .6), mats.concrete); dam.position.set(t.x, t.y + .3, t.z + t.r + .2); dam.castShadow = true; scene.add(dam); }
    return { m: w, t };
  });

  // bhunga huts (round Kutchi houses): villages near the programs and in Banni
  const huts = [];
  const dh = ll(23.833, 69.644), bn = ll(23.7, 69.52);
  const villages = [[S.jal.x + 6, S.jal.z - 5, 8], [S.fodder.x - 6, S.fodder.z + 5, 7], [S.animal.x + 5, S.animal.z - 4, 7], [S.school.x + 5, S.school.z + 4, 5], [S.drink.x + 5, S.drink.z + 5, 8], [S.water.x + 6, S.water.z - 5, 6], [dh.x, dh.z, 9], [bn.x, bn.z, 7]];
  for (const [vx, vz, n] of villages) for (let i = 0; i < n; i++) {
    const a = i / n * Math.PI * 2 + R() * .5, r = 1.4 + R() * 2.2, x = vx + Math.cos(a) * r, z = vz + Math.sin(a) * r;
    if (landAt(x, z)) huts.push({ x, z, y: height(x, z) - .1, s: .55 + R() * .2, ry: R() * 6 });
  }
  const hutG = new THREE.CylinderGeometry(.9, .95, 1.3, 9); hutG.translate(0, .65, 0);
  const roofG = new THREE.ConeGeometry(1.25, 1.2, 9); roofG.translate(0, 1.9, 0);
  instanced(hutG, mats.hut, huts); instanced(roofG, mats.thatch, huts);

  // village rebuilt after 2001: rows of permanent houses
  const houses = [];
  for (let r = 0; r < 4; r++) for (let c = 0; c < 6; c++) {
    if ((r === 1 || r === 2) && (c === 2 || c === 3)) continue;
    const x = S.rebuild.x - 6 + c * 2.4, z = S.rebuild.z - 3.6 + r * 2.5;
    houses.push({ x, z, y: height(x, z) - .08, s: .72 });
  }
  const houseG = new THREE.BoxGeometry(2, 1.2, 1.6); houseG.translate(0, .6, 0);
  const tileG = new THREE.CylinderGeometry(.85, .85, 2.2, 3); tileG.rotateZ(Math.PI / 2); tileG.translate(0, 1.55, 0);
  instanced(houseG, mats.wall, houses); instanced(tileG, mats.tile, houses);

  // Van Shala (forest school) with a flag
  const school = new THREE.Group();
  const sch = new THREE.Mesh(new THREE.BoxGeometry(6, 2, 3.2), mats.wall); sch.position.y = 1;
  const schRoof = new THREE.Mesh(new THREE.CylinderGeometry(1.9, 1.9, 6.6, 3), M('#2e5b3b')); schRoof.rotation.z = Math.PI / 2; schRoof.position.y = 2.75;
  const pole = new THREE.Mesh(new THREE.CylinderGeometry(.06, .06, 5, 5), mats.dark); pole.position.set(4.2, 2.5, 0);
  const flag = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 1), mats.flag); flag.geometry.translate(.8, 0, 0); flag.position.set(4.2, 4.5, 0);
  school.add(sch, schRoof, pole, flag); school.traverse(o => { o.castShadow = o.receiveShadow = true; });
  school.scale.setScalar(.7); school.position.set(S.school.x + 3, height(S.school.x + 3, S.school.z - 2.5) - .08, S.school.z - 2.5); school.rotation.y = .3; scene.add(school);

  // drinking-water tower (WASMO)
  const tower = new THREE.Group();
  for (const [lx, lz] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) { const leg = new THREE.Mesh(new THREE.BoxGeometry(.25, 6, .25), mats.steel); leg.position.set(lx * 1.1, 3, lz * 1.1); tower.add(leg); }
  const tank = new THREE.Mesh(new THREE.CylinderGeometry(2, 2, 2.4, 12), mats.tankTop); tank.position.y = 7.2;
  const cap = new THREE.Mesh(new THREE.ConeGeometry(2.1, .8, 12), mats.steel); cap.position.y = 8.8;
  tower.add(tank, cap); tower.traverse(o => { o.castShadow = true; });
  tower.scale.setScalar(.65); tower.position.set(S.drink.x - 3.5, height(S.drink.x - 3.5, S.drink.z + 1.5) - .1, S.drink.z + 1.5); scene.add(tower);

  // cattle near the animal-health centre
  const cows = [];
  const cowG = { body: new THREE.BoxGeometry(1.7, .8, .75), head: new THREE.BoxGeometry(.55, .5, .5), leg: new THREE.BoxGeometry(.18, .65, .18) };
  for (let i = 0; i < 9; i++) {
    const a = R() * Math.PI * 2, r = 3 + R() * 3.5, x = S.animal.x + Math.cos(a) * r, z = S.animal.z + Math.sin(a) * r;
    if (!landAt(x, z)) continue;
    const g = new THREE.Group(), m = R() < .6 ? mats.cowW : mats.cowB;
    const body = new THREE.Mesh(cowG.body, m); body.position.y = 1.05;
    const head = new THREE.Mesh(cowG.head, m); head.position.set(1, .95, 0);
    g.add(body, head);
    for (const [lx, lz] of [[-.6, -.25], [.6, -.25], [-.6, .25], [.6, .25]]) { const l = new THREE.Mesh(cowG.leg, m); l.position.set(lx, .33, lz); g.add(l); }
    g.traverse(o => { o.castShadow = true; });
    g.scale.setScalar(.6); g.position.set(x, height(x, z) - .05, z); g.rotation.y = R() * 6; g.userData = { head, ph: R() * 6 };
    scene.add(g); cows.push(g);
  }

  // fodder plots: crop rows that grow with the monsoon, plus hay bales
  const PLOTS = [[-4.5, -3.5, 6, 4], [4.5, -3.5, 6, 4], [0, 4, 9, 3.6]].map(([dx, dz, w, d]) => ({ x: S.fodder.x + dx, z: S.fodder.z + dz, w, d }));
  const crops = [], soil = [];
  for (const p of PLOTS) {
    soil.push({ x: p.x, z: p.z, y: height(p.x, p.z) + .02, w: p.w, d: p.d });
    for (let x = -p.w / 2 + .4; x < p.w / 2; x += .65) for (let z = -p.d / 2 + .35; z < p.d / 2; z += .8) { const wx = p.x + x, wz = p.z + z; crops.push({ x: wx, z: wz, y: height(wx, wz) + .02, ry: R() * 3, s: .75 }); }
  }
  for (const s of soil) { const m = new THREE.Mesh(new THREE.BoxGeometry(s.w, .12, s.d), M('#8f6f4a')); m.position.set(s.x, s.y, s.z); m.receiveShadow = true; scene.add(m); }
  const cropG = new THREE.ConeGeometry(.32, 1.3, 4); cropG.translate(0, .65, 0);
  const cropMesh = instanced(cropG, mats.crop, crops, false);
  const baleG = new THREE.CylinderGeometry(.6, .6, 1.1, 10); baleG.rotateZ(Math.PI / 2); baleG.translate(0, .6, 0);
  instanced(baleG, mats.bale, [[-6.5, 2.5], [-6.5, 3.6], [-5.4, 3]].map(([dx, dz]) => ({ x: S.fodder.x + dx, z: S.fodder.z + dz, y: height(S.fodder.x + dx, S.fodder.z + dz), ry: .4, s: .8 })));

  // orchard near the fruit hotspot; fruit appears after the rains
  const orch = [], fruits = [];
  for (let r = 0; r < 4; r++) for (let c = 0; c < 5; c++) {
    const x = S.fruit.x - 3 + c * 2.4, z = S.fruit.z - 2 - r * 2.3;   // north of the hub, away from the coast
    if (!landAt(x, z)) continue;
    const y = height(x, z) - .05; orch.push({ x, z, y, s: .6 });
    for (let k = 0; k < 5; k++) { const a = k / 5 * Math.PI * 2 + r; fruits.push({ x: x + Math.cos(a) * .55, z: z + Math.sin(a) * .55, y: y + 1.1 + R() * .55 }); }
  }
  const oCrown = new THREE.SphereGeometry(1.25, 7, 5); oCrown.translate(0, 2.2, 0);
  instanced(trunkG, mats.trunk, orch); instanced(oCrown, M('#4f8d4f'), orch);
  const fruitMesh = instanced(new THREE.IcosahedronGeometry(.16, 0), mats.fruit, fruits.map(f => ({ ...f, s: .001 })), false);

  // clouds
  const cloudMat = new THREE.MeshStandardMaterial({ color: '#ffffff', emissive: '#ffffff', emissiveIntensity: .14, flatShading: true, roughness: 1, transparent: true, opacity: .82, depthWrite: false });
  const clouds = [], puffG = new THREE.IcosahedronGeometry(1, 1);
  for (let i = 0; i < 7; i++) {
    const g = new THREE.Group(), n = 5 + Math.floor(R() * 3);
    for (let k = 0; k < n; k++) { const r = 3.6 + R() * 3.6 - Math.abs(k - n / 2) * .5; const s = new THREE.Mesh(puffG, cloudMat); s.scale.set(r, r * .6, r); s.position.set(k * 4 - n * 2, R() * 1.6, (R() - .5) * 5); s.castShadow = true; g.add(s); }
    g.position.set(HOME_TGT.x - 300 + i * 95 + R() * 30, 105 + R() * 25, HOME_TGT.z - 120 - R() * 110); g.scale.setScalar(1.1);   // over the Rann, away from the camera g.userData.v = 2.5 + R() * 3;
    scene.add(g); clouds.push(g);
  }

  // winter: Rann Utsav tent city by Dhordo, migratory birds over Banni's wetlands
  const tents = [];
  for (let r = 0; r < 4; r++) for (let c = 0; c < 7; c++) { const x = dh.x + 3 + c * 1.15, z = dh.z - 2.5 + r * 1.2; tents.push({ x, z, y: height(x, z) - .02, ry: Math.PI / 4 }); }
  const tentG = new THREE.ConeGeometry(.55, .9, 4); tentG.translate(0, .45, 0);
  const tentMesh = instanced(tentG, M('#fbf8f0'), tents.map(t => ({ ...t, s: .001 })));
  const birdMat = new THREE.LineBasicMaterial({ color: '#25352c', transparent: true, opacity: 0, depthWrite: false });
  const flocks = [0, 1, 2].map(f => {
    const pts = [];
    for (let b = 0; b < 7; b++) { const bx = 9 + f * 4 + (b % 2 ? 1 : -1) * Math.ceil(b / 2) * .9, bz = Math.ceil(b / 2) * .9, by = (R() - .5) * .6; pts.push(bx - .7, by + .3, bz, bx, by, bz, bx, by, bz, bx + .7, by + .3, bz); }
    const g = new THREE.Group(), l = new THREE.LineSegments(new THREE.BufferGeometry().setAttribute('position', new THREE.BufferAttribute(new Float32Array(pts), 3)), birdMat);
    g.add(l); g.position.set(bn.x + (f - 1) * 6, 15 + f * 2.5, bn.z + (f - 1) * 4); g.rotation.y = f * 2.1; g.visible = false; g.userData.v = .22 + f * .07; scene.add(g); return g;
  });

  // rain showers in the rainy months
  const DROPS = 2600, rainPos = new Float32Array(DROPS * 6);
  for (let i = 0; i < DROPS; i++) { const x = HOME_TGT.x + (R() - .5) * 460, y = R() * 140, z = HOME_TGT.z + (R() - .5) * 330; rainPos.set([x, y, z, x + .3, y + 2.4, z], i * 6); }
  const rainGeo = new THREE.BufferGeometry(); rainGeo.setAttribute('position', new THREE.BufferAttribute(rainPos, 3));
  const rainMat = new THREE.LineBasicMaterial({ color: '#e3f1fb', transparent: true, opacity: 0, depthWrite: false });
  const rain = new THREE.LineSegments(rainGeo, rainMat); rain.visible = false; rain.frustumCulled = false; scene.add(rain);

  // ---------------- markers ----------------
  // program hubs: ground ring + light beam + floating gem (shown while no program is open)
  const ringG = new THREE.RingGeometry(2.4, 3, 48); ringG.rotateX(-Math.PI / 2);
  const beamG = new THREE.CylinderGeometry(.07, .07, 8, 6); beamG.translate(0, 4, 0);
  const gemG = new THREE.OctahedronGeometry(.95, 0);
  const hubs = PROG.map(d => {
    const s = S[d.id], y = Math.max(height(s.x, s.z), .3);
    const ring = new THREE.Mesh(ringG, new THREE.MeshBasicMaterial({ color: '#ffffff', transparent: true, opacity: .85, depthWrite: false, side: THREE.DoubleSide }));
    ring.position.set(s.x, y + .3, s.z);
    const beam = new THREE.Mesh(beamG, new THREE.MeshBasicMaterial({ color: '#fff6df', transparent: true, opacity: .45, depthWrite: false }));
    beam.position.set(s.x, y, s.z);
    const gem = new THREE.Mesh(gemG, new THREE.MeshStandardMaterial({ color: d.color, emissive: d.color, emissiveIntensity: .45, flatShading: true, roughness: .4 }));
    gem.position.set(s.x, y + 9, s.z); gem.castShadow = true;
    scene.add(ring, beam, gem);
    return { d, x: s.x, z: s.z, y, ring, beam, gem, anchor: new THREE.Vector3(s.x, y + 11.2, s.z) };
  });
  // projects, events and centres: a small ring and beam each, shown only for the open program
  const iRingG = new THREE.RingGeometry(1.1, 1.5, 36); iRingG.rotateX(-Math.PI / 2);
  const iDotG = new THREE.CircleGeometry(.6, 20); iDotG.rotateX(-Math.PI / 2);
  const iBeamG = new THREE.CylinderGeometry(.05, .05, 5, 5); iBeamG.translate(0, 2.5, 0);
  const iBeamM = new THREE.MeshBasicMaterial({ color: '#fff6df', transparent: true, opacity: .6, depthWrite: false });
  const marks = ITEMS.map(it => {
    const p = ll(it.lat, it.lon), y = Math.max(height(p.x, p.z), .3);
    const ring = new THREE.Mesh(iRingG, new THREE.MeshBasicMaterial({ color: '#ffffff', transparent: true, opacity: .9, depthWrite: false, side: THREE.DoubleSide }));
    const dot = new THREE.Mesh(iDotG, new THREE.MeshBasicMaterial({ color: '#ffffff', depthWrite: false, side: THREE.DoubleSide }));
    ring.position.y = .3; dot.position.y = .26;
    const g = new THREE.Group(); g.add(ring, dot, new THREE.Mesh(iBeamG, iBeamM)); g.position.set(p.x, y, p.z); g.visible = false; scene.add(g);
    return { it, x: p.x, z: p.z, y, g, ring, dot, anchor: new THREE.Vector3(p.x, y + 5.6, p.z) };
  });

  // ---------------- spatial UI ----------------
  const pinLayer = q('.xpins'), labLayer = q('.xlabels'), panel = q('.xpanel'), toast = q('.xtoast'), body = q('.xp-body');
  const dockBtns = [...stage.querySelectorAll('.xd-places button')];
  const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');
  function mkPin(cls, color, svg, label, badge, aria, onClick) {
    const b = document.createElement('button');
    b.type = 'button'; b.className = cls; b.tabIndex = -1; b.style.setProperty('--c', color);
    b.innerHTML = `<i>${svg}</i><span>${esc(label)}</span>` + (badge != null ? `<em>${badge}</em>` : '');
    b.setAttribute('aria-label', aria);
    b.addEventListener('click', onClick);
    pinLayer.appendChild(b); return b;
  }
  const hubPins = PROG.map((d, i) => { const el = mkPin('xpin', d.color, d.svg, d.short, d.n, `${d.kick} – ${d.n} on the map`, () => { tour(false); openProg(i); }); el._a = hubs[i].anchor; return el; });
  const itemPins = ITEMS.map((it, j) => { const el = mkPin('xpin xi', '#2e5b3b', TYPES[it.type].svg, it.short, null, it.title, () => { tour(false); openItem(j); }); el._a = marks[j].anchor; el._item = true; el.hidden = true; return el; });
  let active = hubPins.slice();
  const labels = meta.places.concat([{ name: 'Dhordo', kind: 'town', ...ll(23.833, 69.644) }]).map(p => {
    const el = document.createElement('div'); el.className = 'xlab ' + p.kind; el.textContent = p.name; labLayer.appendChild(el);
    const y = p.kind === 'water' || p.kind === 'region' ? 1 : Math.max(height(p.x, p.z), .2) + (p.kind === 'peak' ? 1.4 : .5);
    return { el, kind: p.kind, v: new THREE.Vector3(p.x, y, p.z) };
  });
  dockBtns.forEach((b, i) => b.addEventListener('click', () => { tour(false); openProg(i); }));

  let cp = -1, ci = -1, list = [], fly = null, lastAct = performance.now(), introDone = REDUCE;
  const inProg = (it, pid) => it.program.includes(pid);
  const placeTxt = it => it.place + (it.taluka && !it.place.includes(it.taluka) ? `, ${it.taluka} taluka` : '');
  const mini = () => q('.xtitle').classList.add('mini');
  setTimeout(mini, 9000);

  function flyTo(p, t, dur = 1700) {
    fly = { p0: camera.position.clone(), p1: p.clone(), t0: controls.target.clone(), t1: t.clone(), dur: REDUCE ? 1 : dur, start: performance.now() };
    controls.enabled = false;
  }
  // keep the scene's centre in the free area beside (desktop) or above (phone) the panel by offsetting the projection
  const VO = { x: 0, y: 0, tx: 0, ty: 0, fw: .95 };
  const applyVO = () => { if (VO.x || VO.y) camera.setViewOffset(W.w, W.h, VO.x, VO.y, W.w, W.h); else camera.clearViewOffset(); };
  function aimVO() {
    const narrow = W.w < 760, open = cp >= 0;
    const left = 152, right = W.w - 22 - Math.min(380, W.w - 44) - 12;   // between the month rail and the panel
    VO.tx = open && !narrow ? Math.max(0, Math.round(W.w / 2 - (left + right) / 2)) : 0; VO.ty = open && narrow ? Math.round(W.h * .26) : 0;
    VO.fw = open && !narrow ? Math.max(.3, (right - left) / W.w) : .95;
    if (REDUCE) { VO.x = VO.tx; VO.y = VO.ty; applyVO(); }
  }
  const horizDir = t => { const v = new THREE.Vector3(camera.position.x - t.x, 0, camera.position.z - t.z); if (v.lengthSq() < 1) v.set(0, 0, 1); return v.normalize(); };
  function flyToSpot(s, far = 1) {
    const t = new THREE.Vector3(s.x, s.y + 2, s.z), dir = horizDir(t), narrow = W.w < 760;
    flyTo(t.clone().add(dir.multiplyScalar((narrow ? 48 : 38) * far)).add(new THREE.Vector3(0, (narrow ? 34 : 27) * far, 0)), t);
  }
  // frame a group of places inside the free area
  function flyToGroup(pts) {
    if (pts.length === 1) return flyToSpot(pts[0], 2.3);
    let x0 = 1e9, x1 = -1e9, z0 = 1e9, z1 = -1e9;
    for (const s of pts) { x0 = Math.min(x0, s.x); x1 = Math.max(x1, s.x); z0 = Math.min(z0, s.z); z1 = Math.max(z1, s.z); }
    const tanH = Math.tan(THREE.MathUtils.degToRad(camera.fov / 2)), ext = Math.max(x1 - x0, (z1 - z0) * 1.3) + 12;
    const fw = Math.max(.25, VO.fw - 170 / W.w), fh = W.w < 760 ? .44 - 50 / W.h : .74 - 60 / W.h;   // leave room for the pin labels
    const d = THREE.MathUtils.clamp(Math.max(ext / (2 * tanH * camera.aspect * fw), ext / (2 * tanH * fh * 1.35)), 75, 540);
    const tgt = new THREE.Vector3((x0 + x1) / 2, 0, (z0 + z1) / 2), dir = horizDir(tgt);
    flyTo(tgt.clone().addScaledVector(dir, d * .685).add(new THREE.Vector3(0, d * .729, 0)), tgt);
  }

  // ---------------- real village boundaries: highlights, hover names ----------------
  const rgba = (hex, a) => { const c = col(hex); return `rgba(${Math.round(c.r * 255)},${Math.round(c.g * 255)},${Math.round(c.b * 255)},${a})`; };
  const areaRings = a => a ? (a.v != null ? VIL[a.v].rings : TAL[a.t].rings) : null;
  // paint the outlines of the open program's villages (or talukas) onto the ground; focus = the selected item's area
  function drawHi(areas, color, focus) {
    const g = hiCanvas.getContext('2d'); g.clearRect(0, 0, HIN, HIN);
    const list = areas.filter(Boolean);
    if (!list.length) { terrU.uHiBox.value.set(0, 0, 0, 0); hiTex.needsUpdate = true; return; }
    const fb = bboxOf((focus ? [focus] : list).flatMap(areaRings)), pad = focus ? 14 : 5;
    const size = Math.max(fb.x1 - fb.x0, fb.z1 - fb.z0, 8) + pad * 2, x0 = (fb.x0 + fb.x1) / 2 - size / 2, z0 = (fb.z0 + fb.z1) / 2 - size / 2, sc = HIN / size;
    const path = rings => { g.beginPath(); for (const r of rings) { r.forEach(([x, z], i) => g[i ? 'lineTo' : 'moveTo']((x - x0) * sc, (z - z0) * sc)); g.closePath(); } };
    g.lineJoin = 'round';
    for (const a of list) {
      const on = focus && a.v === focus.v && a.t === focus.t, tal = a.t != null;
      path(areaRings(a));
      g.fillStyle = rgba(color, tal ? .13 : on ? .5 : .3); g.fill();
      const w = Math.min(14, Math.max(1.6, (tal ? .3 : on ? .22 : .14) * sc));
      if (on) { g.strokeStyle = 'rgba(255,255,255,.95)'; g.lineWidth = w * 2.2; g.stroke(); }
      g.strokeStyle = rgba(color, .95); g.lineWidth = w; g.stroke();
    }
    terrU.uHiBox.value.set(x0, z0, 1 / size, 1 / size); hiTex.needsUpdate = true;
  }
  // which village is at (x, z)? a coarse grid of buckets keeps this fast
  const VB = 10, vBuckets = new Map();
  VIL.forEach((v, i) => { for (let a = Math.floor(v.b.x0 / VB); a <= Math.floor(v.b.x1 / VB); a++) for (let b = Math.floor(v.b.z0 / VB); b <= Math.floor(v.b.z1 / VB); b++) { const k = a + ',' + b; if (!vBuckets.has(k)) vBuckets.set(k, []); vBuckets.get(k).push(i); } });
  const inRing = (x, z, r) => { let c = false; for (let i = 0, k = r.length - 1; i < r.length; k = i++) { const [xi, zi] = r[i], [xk, zk] = r[k]; if ((zi > z) !== (zk > z) && x < xi + (z - zi) * (xk - xi) / (zk - zi)) c = !c; } return c; };
  function villageAt(x, z) {
    for (const i of vBuckets.get(Math.floor(x / VB) + ',' + Math.floor(z / VB)) || []) { const v = VIL[i]; if (x >= v.b.x0 && x <= v.b.x1 && z >= v.b.z0 && z <= v.b.z1 && v.rings.some(r => inRing(x, z, r))) return i; }
    return -1;
  }
  // where does a screen point meet the ground? march along the camera ray over the height field
  const ray = new THREE.Raycaster(), ndc = new THREE.Vector2();
  function groundAt(cx, cy) {
    const rc = renderer.domElement.getBoundingClientRect();
    ndc.set((cx - rc.left) / rc.width * 2 - 1, -((cy - rc.top) / rc.height) * 2 + 1); ray.setFromCamera(ndc, camera);
    const o = ray.ray.origin, d = ray.ray.direction; if (d.y > -.02) return null;
    const hAt = t => Math.max(surf(o.x + d.x * t, o.z + d.z * t), SEA_Y);
    let t = Math.max(0, (o.y - 16) / -d.y), prev = t;
    for (let n = 0; n < 3000; n++) {
      if (o.y + d.y * t <= hAt(t)) { let a = prev, b = t; for (let m = 0; m < 10; m++) { const c = (a + b) / 2; if (o.y + d.y * c <= hAt(c)) b = c; else a = c; } return { x: o.x + d.x * b, z: o.z + d.z * b }; }
      prev = t; t += .35; if (o.y + d.y * t < SEA_Y - 1) return null;
    }
    return null;
  }
  const tip = q('.xtip'); let hoverV = -1, hoverLine = null, hoverEv = null, dragging = false, tipT = null;
  function setHover(i, cx, cy) {
    if (i !== hoverV) {
      if (hoverLine) { scene.remove(hoverLine); hoverLine.geometry.dispose(); hoverLine = null; }
      hoverV = i;
      if (i >= 0) { hoverLine = lineMesh(VIL[i].rings.map(r => drapeRing(r, .25)), hoverMat, 6); tip.innerHTML = `<b>${esc(VIL[i].n)}</b><small>${esc(TAL[VIL[i].t].n)} taluka</small>`; }
    }
    tip.classList.toggle('show', i >= 0);
    if (i >= 0) { const rc = stage.getBoundingClientRect(); tip.style.transform = `translate3d(${Math.round(cx - rc.left + 14)}px,${Math.round(cy - rc.top + 16)}px,0)`; }
  }
  const cv = renderer.domElement; let downAt = null;
  cv.addEventListener('pointermove', e => { if (e.pointerType === 'mouse') hoverEv = e; });
  cv.addEventListener('pointerleave', () => { hoverEv = null; setHover(-1); });
  cv.addEventListener('pointerdown', e => { downAt = { x: e.clientX, y: e.clientY, t: performance.now() }; });
  cv.addEventListener('pointerup', e => {   // a tap (no drag) on a phone shows the village name for a few seconds
    if (e.pointerType === 'mouse' || !downAt || Math.hypot(e.clientX - downAt.x, e.clientY - downAt.y) > 8 || performance.now() - downAt.t > 500) return;
    const g = groundAt(e.clientX, e.clientY); setHover(g ? villageAt(g.x, g.z) : -1, e.clientX, e.clientY);
    clearTimeout(tipT); tipT = setTimeout(() => setHover(-1), 3500);
  });
  controls.addEventListener('start', () => { dragging = true; setHover(-1); });
  controls.addEventListener('end', () => { dragging = false; });

  function setActive(pins) {
    for (const el of active) if (!pins.includes(el)) { el.hidden = true; el.classList.remove('on', 'pop', 'off'); }
    pins.forEach((el, k) => {
      if (!el.hidden) return;
      el.hidden = false; el._w = 0; el._L = null;
      if (!REDUCE) { el.classList.remove('pop'); void el.offsetWidth; el.style.setProperty('--d', Math.min(k * .045, .6).toFixed(3) + 's'); el.classList.add('pop'); }
    });
    active = pins;
  }
  function showMarks(pid, color) {
    for (const h of hubs) h.ring.visible = h.beam.visible = h.gem.visible = pid == null;
    for (const m of marks) { const on = pid != null && inProg(m.it, pid); m.g.visible = on; if (on) { m.ring.material.color.set(color); m.dot.material.color.set(color); } }
  }
  function showPanel(color, isItem) {
    panel.style.setProperty('--c', color);
    panel.classList.toggle('item', isItem);
    panel.classList.add('open'); panel.classList.remove('swap'); void panel.offsetWidth; panel.classList.add('swap');
    panel.setAttribute('aria-hidden', 'false'); panel.inert = false; stage.classList.add('pan'); aimVO();
    q('.xp-in').scrollTop = 0;
  }
  function markDock() {
    dockBtns.forEach((b, k) => { b.classList.toggle('on', k === cp); b.setAttribute('aria-current', k === cp ? 'true' : 'false'); });
    const box = q('.xd-places'), db = dockBtns[cp];   // scroll only the dock row, never the page
    if (db) box.scrollTo({ left: db.offsetLeft - box.offsetLeft - (box.clientWidth - db.offsetWidth) / 2, behavior: REDUCE ? 'auto' : 'smooth' });
  }

  // level 1: a program, with only its own projects and events on the map
  function openProg(i, flyMode = 'fly') {
    cp = (i + PROG.length) % PROG.length; ci = -1; mini();
    const d = PROG[cp];
    list = ITEMS.map((it, j) => j).filter(j => inProg(ITEMS[j], d.id));
    q('.xp-kick').textContent = d.kick;
    q('.xp-count').textContent = `${cp + 1} / ${PROG.length}`;
    const rows = list.map(j => {
      const it = ITEMS[j], T = TYPES[it.type];
      return `<li><button type="button" data-j="${j}"><i>${T.svg}</i><span><b>${esc(it.title)}</b><small>${esc(T.label)} · ${esc(placeTxt(it))}${it.when ? ' · ' + esc(it.when) : ''}</small></span></button></li>`;
    }).join('');
    body.innerHTML = `<h2 class="xp-title">${esc(d.title)}</h2><p class="xp-where"><span>${esc(d.where)}</span></p>`
      + `<div class="xp-stat"><b>${esc(d.stat[0])}</b><span>${esc(d.stat[1])}</span></div><p class="xp-text">${esc(d.text)}</p>`
      + `<div class="xp-facts">${d.facts.map(f => `<div><b>${esc(f[0])}</b><span>${esc(f[1])}</span></div>`).join('')}</div>`
      + `<div class="xp-list"><h3>Projects &amp; events <b>${list.length}</b></h3>`
      + (list.length ? `<ul>${rows}</ul>` : '<p class="none">Projects and events for this program will appear here.</p>') + '</div>';
    body.querySelectorAll('[data-j]').forEach(b => b.addEventListener('click', () => { tour(false); openItem(+b.dataset.j); }));
    const a = q('.xp-go'); a.href = d.link; a.textContent = d.link_label;
    q('.xp-prev').setAttribute('aria-label', 'Previous program'); q('.xp-next').setAttribute('aria-label', 'Next program');
    showPanel(d.color, false); markDock();
    for (const j of list) itemPins[j].style.setProperty('--c', d.color);
    itemPins.forEach(p => p.classList.remove('on'));
    setActive(list.map(j => itemPins[j])); showMarks(d.id, d.color); drawHi(list.map(j => ITEMS[j].area), d.color, null);
    if (flyMode === 'fly') flyToGroup(list.length ? list.map(j => marks[j]) : [hubs[cp]]);
    history.replaceState(null, '', '#' + d.id);
    lastAct = performance.now();
  }
  // level 2: one project, event or centre
  const CAL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><rect x="4" y="5" width="16" height="15" rx="2"/><path d="M8 3v4M16 3v4M4 10h16"/></svg>';
  function openItem(j) {
    const it = ITEMS[j];
    if (cp < 0 || !inProg(it, PROG[cp].id)) openProg(PROG.findIndex(d => inProg(it, d.id)), 'none');
    ci = j; mini();
    const d = PROG[cp], T = TYPES[it.type], M = it.month ? MONTHS[it.month - 1] : null;
    q('.xp-back span').textContent = d.short; q('.xp-back').setAttribute('aria-label', 'Back to ' + d.kick);
    q('.xp-count').textContent = `${list.indexOf(j) + 1} / ${list.length}`;
    body.innerHTML = `<div class="xp-type"><i>${T.svg}</i>${esc(T.label)}${it.when ? `<span>· ${esc(it.when)}</span>` : ''}</div>`
      + `<h2 class="xp-title">${esc(it.title)}</h2>`
      + `<p class="xp-where"><span>${esc(placeTxt(it))}${it.approx ? ' <em>approximate location</em>' : ''}</span></p>`
      + (it.area ? `<p class="xp-bnd"><i></i>Outlined: ${esc(it.area.v != null ? VIL[it.area.v].n + ' village boundary' : TAL[it.area.t].n + ' taluka')}</p>` : '')
      + (it.img ? `<figure class="xp-img"><img src="${esc(it.img)}" alt="${esc(it.img_alt || it.title)}"></figure>` : '')
      + `<p class="xp-text">${esc(it.text)}</p>`
      + (M ? `<button class="xp-month" type="button" style="--k:${M.color}">${CAL}<span>See Kutch in ${esc(M.name)}</span></button>` : '');
    const mb = body.querySelector('.xp-month'); if (mb) mb.addEventListener('click', () => { stopPlay(); setMonth(it.month - 1); });
    const a = q('.xp-go'); a.href = it.link || d.link; a.textContent = it.link ? it.link_label : d.link_label;
    q('.xp-prev').setAttribute('aria-label', 'Previous place'); q('.xp-next').setAttribute('aria-label', 'Next place');
    showPanel(d.color, true);
    itemPins.forEach((p, k) => p.classList.toggle('on', k === j));
    drawHi(list.map(k => ITEMS[k].area), d.color, it.area);
    flyToSpot(marks[j]);
    history.replaceState(null, '', `#${d.id}/${it.id}`);
    lastAct = performance.now();
  }
  function close(reset = true) {
    cp = -1; ci = -1; list = [];
    panel.classList.remove('open', 'item'); panel.setAttribute('aria-hidden', 'true'); panel.inert = true; stage.classList.remove('pan');
    markDock(); itemPins.forEach(p => p.classList.remove('on'));
    setActive(hubPins); showMarks(null); aimVO(); drawHi([], '#000', null);
    history.replaceState(null, '', location.pathname + location.search);
    if (reset) flyTo(HOME_POS, HOME_TGT, 1500);
  }
  const step = k => { if (ci >= 0 && list.length) openItem(list[(list.indexOf(ci) + k + list.length) % list.length]); else if (cp >= 0) openProg(cp + k); };
  const back = () => { if (ci >= 0) openProg(cp); else if (cp >= 0) close(); };
  panel.inert = true;
  q('.xp-x').addEventListener('click', () => { tour(false); close(); });
  q('.xp-back').addEventListener('click', () => { tour(false); openProg(cp); });
  q('.xp-next').addEventListener('click', () => { tour(false); step(1); });
  q('.xp-prev').addEventListener('click', () => { tour(false); step(-1); });
  q('.xd-reset').addEventListener('click', () => { tour(false); close(); });

  // gentle 3D tilt of the glass panel under the pointer
  const pin = q('.xp-in');
  if (!REDUCE) {
    panel.addEventListener('pointermove', e => { const r = panel.getBoundingClientRect(); pin.style.setProperty('--ry', ((e.clientX - r.left) / r.width - .5) * 9 + 'deg'); pin.style.setProperty('--rx', -((e.clientY - r.top) / r.height - .5) * 7 + 'deg'); });
    panel.addEventListener('pointerleave', () => { pin.style.setProperty('--ry', '0deg'); pin.style.setProperty('--rx', '0deg'); });
  }

  // guided tour through the programs
  const tourBtn = q('.xd-tour'); let tourT = null;
  function tour(on) {
    clearInterval(tourT); tourT = null;
    tourBtn.setAttribute('aria-pressed', on ? 'true' : 'false');
    tourBtn.querySelector('span').textContent = on ? 'Pause' : 'Tour';
    if (on) { openProg(cp < 0 ? 0 : cp + 1); tourT = setInterval(() => openProg(cp + 1), 7500); }
  }
  tourBtn.addEventListener('click', () => tour(!tourT));
  controls.addEventListener('start', () => { mini(); lastAct = performance.now(); if (tourT) tour(false); fly = null; controls.enabled = true; });

  let toastT;
  function showToast(html, k) { toast.innerHTML = html; toast.style.setProperty('--k', k || '#2e5b3b'); toast.classList.add('show'); clearTimeout(toastT); toastT = setTimeout(() => toast.classList.remove('show'), 5200); }

  // ---------------- months ----------------
  // Each month is a mix of three palettes (dry summer, green monsoon, clear winter) plus its own tank level,
  // crop height, mango crop, Rann Utsav tents, winter birds and rain showers.
  const MP = [
    { w: [0, 0, 1], water: .7, crop: .55, fruit: 0, tents: 1, birds: 1, rain: 0 },             // Jan
    { w: [.25, 0, .75], water: .58, crop: .5, fruit: 0, tents: 1, birds: 1, rain: 0 },         // Feb
    { w: [.7, 0, .3], water: .45, crop: .22, fruit: .2, tents: .2, birds: .5, rain: 0 },       // Mar
    { w: [1, 0, 0], water: .3, crop: .12, fruit: .5, tents: 0, birds: 0, rain: 0 },            // Apr
    { w: [1, 0, 0], water: .12, crop: .1, fruit: .9, tents: 0, birds: 0, rain: 0 },            // May
    { w: [.82, .18, 0], water: .08, crop: .2, fruit: 1, tents: 0, birds: 0, rain: .25 },       // Jun
    { w: [.12, .88, 0], water: .6, crop: .65, fruit: .15, tents: 0, birds: 0, rain: 1 },       // Jul
    { w: [0, 1, 0], water: .92, crop: .95, fruit: 0, tents: 0, birds: 0, rain: .9 },           // Aug
    { w: [0, 1, 0], water: 1, crop: 1, fruit: 0, tents: 0, birds: .15, rain: .4 },             // Sep
    { w: [.2, .6, .2], water: .96, crop: .7, fruit: 0, tents: 0, birds: .6, rain: 0 },         // Oct
    { w: [.05, .2, .75], water: .88, crop: .35, fruit: 0, tents: .85, birds: 1, rain: 0 },     // Nov
    { w: [0, 0, 1], water: .8, crop: .45, fruit: 0, tents: 1, birds: 1, rain: 0 },             // Dec
  ];
  const KEYS = ['water', 'crop', 'fruit', 'tents', 'birds'];
  const cloneSt = s => { const o = { w: s.w.slice() }; for (const k of KEYS) o[k] = s[k]; return o; };
  const lerpSt = (a, b, e) => { const o = { w: a.w.map((v, k) => v + (b.w[k] - v) * e) }; for (const k of KEYS) o[k] = a[k] + (b[k] - a[k]) * e; return o; };

  const C3 = a => a.map(col), V3 = a => a.map(p => new THREE.Vector3(...p));
  const SET = {   // [summer, monsoon, winter]
    crown: C3(['#7f9150', '#4f8f4c', '#5f8a48']), shrub: C3(['#9a9256', '#5d8d45', '#7c8d50']), crop: C3(['#cdb77a', '#5f9e4f', '#b9b45c']),
    cloud: C3(['#ffffff', '#b9c2cb', '#ffffff']), cloudA: [.5, .9, .38], cloudE: [.14, 0, .16],
    sun: C3(['#ffdcaa', '#f1f2ee', '#fff3dc']), sunI: [3, 1.7, 2.5], sunP: V3([[150, 320, 110], [170, 260, 120], [235, 150, 165]]),
    hemi: C3(['#fff1d6', '#e9eef0', '#f4f7fb']), sea: C3(['#3d8db7', '#4b8aa3', '#2c7fb4']),
    skyT: C3(['#9cc6df', '#7f95a8', '#5fa9e6']), skyB: C3(['#d7e5e6', '#c8d5da', '#d9e8f0']), fogN: [360, 400, 560], fogF: [1100, 1150, 1600],
  };
  const tmpV = new THREE.Vector3();
  function applySeason(s) {
    const w = s.w, n = a => a[0] * w[0] + a[1] * w[1] + a[2] * w[2];
    const c = (out, a) => out.setRGB(n([a[0].r, a[1].r, a[2].r]), n([a[0].g, a[1].g, a[2].g]), n([a[0].b, a[1].b, a[2].b]));
    seasonU.value.set(w[0], w[1], w[2]);
    c(mats.crown.color, SET.crown); c(mats.shrub.color, SET.shrub); c(mats.crop.color, SET.crop);
    c(cloudMat.color, SET.cloud); cloudMat.opacity = n(SET.cloudA); cloudMat.emissiveIntensity = n(SET.cloudE);
    c(sun.color, SET.sun); sun.intensity = n(SET.sunI);
    tmpV.set(0, 0, 0); SET.sunP.forEach((p, k) => tmpV.addScaledVector(p, w[k])); sun.position.copy(HOME_TGT).add(tmpV);
    c(hemi.color, SET.hemi); c(seaMat.color, SET.sea);
    c(skyU.top.value, SET.skyT); c(skyU.bot.value, SET.skyB); scene.fog.color.copy(skyU.bot.value); scene.fog.near = n(SET.fogN); scene.fog.far = n(SET.fogF);
    const lvl = s.water;
    waters.forEach(({ m, t }) => { m.position.y = lvl < .05 ? t.y - .1 : t.y + .02 + .14 * lvl; m.scale.setScalar(.6 + .4 * lvl); });
    crops.forEach((cr, i) => { dummy.position.set(cr.x, cr.y, cr.z); dummy.rotation.set(0, cr.ry, 0); dummy.scale.set(cr.s, cr.s * s.crop, cr.s); dummy.updateMatrix(); cropMesh.setMatrixAt(i, dummy.matrix); });
    cropMesh.instanceMatrix.needsUpdate = true;
    const fs = Math.max(.001, sstep(.3, 1, s.fruit));
    fruits.forEach((f, i) => { dummy.position.set(f.x, f.y, f.z); dummy.rotation.set(0, 0, 0); dummy.scale.setScalar(fs); dummy.updateMatrix(); fruitMesh.setMatrixAt(i, dummy.matrix); });
    fruitMesh.instanceMatrix.needsUpdate = true;
    const ts = Math.max(.001, sstep(.35, 1, s.tents));
    tents.forEach((t, i) => { dummy.position.set(t.x, t.y, t.z); dummy.rotation.set(0, t.ry, 0); dummy.scale.setScalar(ts); dummy.updateMatrix(); tentMesh.setMatrixAt(i, dummy.matrix); });
    tentMesh.instanceMatrix.needsUpdate = true;
    birdMat.opacity = sstep(.4, 1, s.birds); flocks.forEach(g => { g.visible = birdMat.opacity > .02; });
  }

  const rail = q('.xmonths'), mBox = q('.xm-list'), mBtns = [...mBox.querySelectorAll('button')], mSeason = q('.xm-season'), playBtn = q('.xm-play');
  const PLAY = playBtn.innerHTML, PAUSE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 5h3.5v14H7zM13.5 5H17v14h-3.5z" fill="currentColor"/></svg>';
  let mIdx = new Date().getMonth(), st = cloneSt(MP[mIdx]), stFrom = cloneSt(st), mK = 1, rainT0 = 0, rainAmt = 0, playT = null;
  function setMonth(i, mode) {
    mIdx = (i + 12) % 12; stFrom = cloneSt(st); mK = 0; rainT0 = performance.now();
    const M = MONTHS[mIdx];
    mBox.style.setProperty('--i', mIdx);
    mBtns.forEach((b, k) => { b.setAttribute('aria-checked', k === mIdx ? 'true' : 'false'); b.tabIndex = k === mIdx ? 0 : -1; });
    mSeason.innerHTML = `<span class="xm-cur">${esc(M.abbr)}</span><span class="xm-dot"> · </span><span class="xm-s">${esc(M.season)}</span>`; rail.style.setProperty('--k', M.color);
    if (mode !== 'quiet') showToast(`<b>${esc(M.name)} · ${esc(M.season)}</b> – ${esc(M.text)}`, M.color);
    if (REDUCE || mode === 'quiet') { mK = 1; st = cloneSt(MP[mIdx]); applySeason(st); }
  }
  function stopPlay() {
    if (!playT) return;
    clearInterval(playT); playT = null;
    playBtn.setAttribute('aria-pressed', 'false'); playBtn.innerHTML = PLAY; playBtn.setAttribute('aria-label', 'Play the year, month by month');
  }
  playBtn.addEventListener('click', () => {
    if (playT) return stopPlay();
    playBtn.setAttribute('aria-pressed', 'true'); playBtn.innerHTML = PAUSE; playBtn.setAttribute('aria-label', 'Pause the year');
    setMonth(mIdx + 1); playT = setInterval(() => setMonth(mIdx + 1), 3600);
  });
  mBtns.forEach((b, i) => b.addEventListener('click', () => { stopPlay(); setMonth(i); }));
  mBox.addEventListener('keydown', e => {
    const k = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key];
    const nx = k ? mIdx + k : e.key === 'Home' ? 0 : e.key === 'End' ? 11 : null;
    if (nx === null) return;
    e.preventDefault(); e.stopPropagation(); stopPlay(); setMonth(nx); mBtns[mIdx].focus();
  });
  // the month list folds away: open by default on wide screens, closed on phones, and remembered per visitor
  const mToggle = q('.xm-toggle');
  function setRail(open, save) {
    rail.classList.toggle('closed', !open); mToggle.setAttribute('aria-expanded', open ? 'true' : 'false'); mBox.inert = !open;
    if (save) try { localStorage.setItem('x3d-months-open', open ? '1' : '0'); } catch (e) { /* storage blocked: just don't remember */ }
  }
  let railPref = null; try { railPref = localStorage.getItem('x3d-months-open'); } catch (e) { railPref = null; }
  setRail(railPref ? railPref === '1' : innerWidth > 760, false);
  mToggle.addEventListener('click', () => setRail(rail.classList.contains('closed'), true));
  setMonth(mIdx, 'quiet');   // start on this month

  // ---------------- size, loop ----------------
  const W = { w: 1, h: 1 };
  const setHH = () => stage.style.setProperty('--hh', (document.querySelector('header')?.offsetHeight || 67) + 'px');
  setHH(); addEventListener('resize', setHH);
  function resize() {
    W.w = stage.clientWidth; W.h = stage.clientHeight; renderer.setSize(W.w, W.h, false); camera.aspect = W.w / W.h;
    aimVO(); VO.x = VO.tx; VO.y = VO.ty; applyVO(); camera.updateProjectionMatrix();
    for (const el of hubPins.concat(itemPins)) el._w = 0;   // pin sizes change at the phone breakpoint
  }
  new ResizeObserver(resize).observe(stage); resize();

  const v3 = new THREE.Vector3(); let last = performance.now(), running = true;
  document.addEventListener('visibilitychange', () => { running = !document.hidden; if (running) { last = performance.now(); requestAnimationFrame(loop); } });

  function project(v) { v3.copy(v).project(camera); return { x: (v3.x * .5 + .5) * W.w, y: (-v3.y * .5 + .5) * W.h, behind: v3.z > 1 }; }
  const crowdW = el => { if (!el._wc) { el.classList.add('crowd'); el._wc = el.offsetWidth; el.classList.remove('crowd'); } return el._wc; };
  // pins never cover each other: a crowded pin climbs on a longer stem, then drops its label
  function placeUI(dt) {
    const boxes = [], P = [];
    for (const el of active) {
      const p = project(el._a), off = p.behind || p.x < -60 || p.x > W.w + 60 || p.y < -20 || p.y > W.h + 80;
      el.classList.toggle('off', off);
      if (off) continue;
      if (!el._w) { el._w = el.offsetWidth; el._h = el.offsetHeight; el._wc = 0; }
      P.push({ el, p, d: camera.position.distanceTo(el._a), on: el.classList.contains('on') });
    }
    P.sort((a, b) => b.on - a.on);   // the selected pin first, then in list order
    const hit = r => boxes.some(b => r.x0 < b.x1 && r.x1 > b.x0 && r.y0 < b.y1 && r.y1 > b.y0);
    for (const o of P) {
      const { el, p } = o, sc = THREE.MathUtils.clamp((el._item ? 112 : 130) / o.d, .7, 1.12), h = el._h * sc;
      let best = null;
      for (let pass = 0; pass < 2 && !best; pass++) {
        if (pass && o.on) break;
        const w = (pass ? crowdW(el) : el._w) * sc + 6;
        for (let k = 0; k < 5 && !best; k++) {
          const L = k * (h + 4), r = { x0: p.x - w / 2, x1: p.x + w / 2, y0: p.y - L - h - 2, y1: p.y - L + 2 };
          if (!hit(r)) best = { r, L, crowd: pass === 1 };
        }
      }
      if (!best) { const w = (o.on ? el._w : crowdW(el)) * sc; best = { r: { x0: p.x - w / 2, x1: p.x + w / 2, y0: p.y - h, y1: p.y }, L: 0, crowd: !o.on }; }
      boxes.push(best.r);
      el._L = el._L == null ? best.L : el._L + (best.L - el._L) * Math.min(1, dt * 14);
      el.classList.toggle('crowd', best.crowd);
      el.style.setProperty('--lift', (el._L / sc).toFixed(1) + 'px');
      el.style.transform = `translate3d(${p.x.toFixed(1)}px,${(p.y - el._L).toFixed(1)}px,0) translate(-50%,-100%) scale(${sc.toFixed(3)})`;
      el.style.zIndex = String(3000 - Math.round(o.d) + (o.on ? 800 : 0));
    }
    const camD = camera.position.distanceTo(controls.target);
    vilMat.opacity = .42 * (1 - sstep(130, 300, camD)); vilLines.visible = vilMat.opacity > .01;
    if (hoverEv && !dragging && !fly) { const e = hoverEv, g = groundAt(e.clientX, e.clientY); hoverEv = null; setHover(g ? villageAt(g.x, g.z) : -1, e.clientX, e.clientY); }
    for (const l of labels) {
      const p = project(l.v);
      let show = !p.behind && p.x > -80 && p.x < W.w + 80 && p.y > -20 && p.y < W.h + 20 && (l.kind === 'town' || l.kind === 'peak' ? camD < 420 : camD > 140);
      if (show && (l.kind === 'town' || l.kind === 'peak')) {
        if (!l.w) { l.w = l.el.offsetWidth || 60; l.h = l.el.offsetHeight || 22; }
        const a = { x0: p.x - l.w / 2, x1: p.x + l.w / 2, y0: p.y - 4, y1: p.y - 4 + l.h };
        if (hit(a)) show = false;
        else boxes.push(a);   // later labels give way to earlier ones (e.g. Dhordo to Khavda until you zoom in)
      }
      l.el.classList.toggle('off', !show);
      if (show) l.el.style.transform = `translate3d(${p.x.toFixed(1)}px,${p.y.toFixed(1)}px,0)`;
    }
  }

  function loop(now) {
    if (!running) return;
    const dt = Math.min(.05, (now - last) / 1000), t = now / 1000; last = now;

    if (fly) {
      const k = Math.min(1, (now - fly.start) / fly.dur), e = ease(k);
      camera.position.lerpVectors(fly.p0, fly.p1, e); controls.target.lerpVectors(fly.t0, fly.t1, e);
      if (k >= 1) { fly = null; controls.enabled = true; }
    }
    controls.autoRotate = !REDUCE && introDone && cp < 0 && !fly && now - lastAct > 7000;
    controls.update();
    if (VO.x !== VO.tx || VO.y !== VO.ty) {
      const k = Math.min(1, dt * 4.5); VO.x += (VO.tx - VO.x) * k; VO.y += (VO.ty - VO.y) * k;
      if (Math.abs(VO.tx - VO.x) < .5 && Math.abs(VO.ty - VO.y) < .5) { VO.x = VO.tx; VO.y = VO.ty; }
      applyVO();
    }

    if (mK < 1) { mK = Math.min(1, mK + dt / 2.2); st = lerpSt(stFrom, MP[mIdx], ease(mK)); applySeason(st); }
    const rr = MP[mIdx].rain, rainTo = !REDUCE && rr > 0 && (now - rainT0) % 15000 < 3500 + 5500 * rr ? .4 + .6 * rr : 0;   // passing showers, not all-day rain
    rainAmt += (rainTo - rainAmt) * Math.min(1, dt * 2.5);
    rain.visible = rainAmt > .01; rainMat.opacity = rainAmt * .6;
    if (rain.visible) {
      const a = rainGeo.attributes.position.array, x0 = HOME_TGT.x - 230, x1 = HOME_TGT.x + 230;
      for (let i = 0; i < DROPS; i++) { const o = i * 6; let y = a[o + 1] - 90 * dt; if (y < 0) y += 140; a[o + 1] = y; a[o + 4] = y + 2.4; a[o] += 8 * dt; if (a[o] > x1) a[o] = x0; a[o + 3] = a[o] + .3; }
      rainGeo.attributes.position.needsUpdate = true;
    }

    if (!REDUCE) {
      for (let i = 0; i < seaPos.count; i++) { const x = seaPos.getX(i), z = seaPos.getZ(i); seaPos.setY(i, SEA_Y + Math.sin(x * .09 + t * 1.1) * .05 + Math.cos(z * .07 + t * .8) * .04); }
      seaPos.needsUpdate = true; seaGeo.computeVertexNormals();
      for (const c of clouds) { c.position.x += c.userData.v * dt; if (c.position.x > HOME_TGT.x + 320) c.position.x = HOME_TGT.x - 320; }
      for (const g of cows) g.userData.head.position.y = .95 - (Math.sin(t * 1.3 + g.userData.ph) > .6 ? .35 : 0);
      flag.rotation.y = Math.sin(t * 2.4) * .25;
      for (const g of flocks) if (g.visible) g.rotation.y += g.userData.v * dt;
      if (cp < 0) hubs.forEach((s, i) => {
        s.gem.position.y = s.y + 9 + Math.sin(t * 1.6 + i) * .5; s.gem.rotation.y = t * .9 + i;
        const p = (t * .6 + i * .13) % 1; s.ring.scale.setScalar(1 + p * .5); s.ring.material.opacity = .8 * (1 - p);
      });
      else marks.forEach((m, i) => {
        if (!m.g.visible) return;
        const on = ci >= 0 && ITEMS[ci] === m.it, p = (t * .7 + i * .17) % 1;
        m.ring.scale.setScalar((on ? 1.6 : 1) + p * .7); m.ring.material.opacity = (on ? 1 : .85) * (1 - p);
      });
    }
    sky.position.copy(camera.position);
    renderer.render(scene, camera);
    placeUI(dt);
    requestAnimationFrame(loop);
  }

  // first frame, then the intro flight and this month's story
  stage.classList.add('ready'); stage.classList.remove('nogl');
  requestAnimationFrame(loop);
  const [hp, hi] = location.hash.slice(1).split('/');
  const tp = PROG.findIndex(d => d.id === hp), ti = hi ? ITEMS.findIndex(it => it.id === hi) : -1;
  const openHash = () => {
    if (tp < 0) return;
    if (ti >= 0 && inProg(ITEMS[ti], PROG[tp].id)) { openProg(tp, 'none'); openItem(ti); } else openProg(tp);
  };
  const monthNote = () => { const M = MONTHS[mIdx]; showToast(`<b>${esc(M.name)} · ${esc(M.season)}</b> – ${esc(M.text)}`, M.color); };
  if (REDUCE) openHash();
  else {
    flyTo(HOME_POS, HOME_TGT, 3600);
    setTimeout(monthNote, 2200);
    setTimeout(() => { introDone = true; openHash(); }, 3800);
  }

  addEventListener('keydown', e => {
    if (e.target.closest && e.target.closest('input,textarea')) return;
    if (e.key === 'Escape' && cp >= 0) { tour(false); back(); }
    else if (e.key === 'ArrowRight' && cp >= 0) { tour(false); step(1); }
    else if (e.key === 'ArrowLeft' && cp >= 0) { tour(false); step(-1); }
  });
}
