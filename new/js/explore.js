// Explore Kutch in 3D – the real shape of Kutch with the Trust's programs as spatial pins.
// Ground: data/kutch.bin + data/kutch.json, built by data-src/make_kutch_terrain.py from NASA SRTM heights
// (AWS Terrain Tiles), ESA WorldCover 2021 land cover and the OpenStreetMap district boundary.
// 1 scene unit = 1 km; heights are exaggerated so the low hills read. Program data comes from #x3d-data.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const stage = document.getElementById('x3d');
const DATA = JSON.parse(document.getElementById('x3d-data').textContent);
const REDUCE = matchMedia('(prefers-reduced-motion: reduce)').matches;
const q = s => stage.querySelector(s);

init().catch(e => { console.error(e); stage.classList.add('nogl'); });

async function init() {
  if (!document.createElement('canvas').getContext('webgl2')) throw new Error('WebGL2 not available');
  const [meta, buf] = await Promise.all([
    fetch('data/kutch.json').then(r => { if (!r.ok) throw new Error('terrain meta ' + r.status); return r.json(); }),
    fetch('data/kutch.bin').then(r => { if (!r.ok) throw new Error('terrain data ' + r.status); return r.arrayBuffer(); }),
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
  const EDGE = new Float32Array(N);   // 0 = open sea at the map edge, 1 = untouched (only outside Kutch)
  for (let k = 0; k < N; k++) {
    if (IN[k]) { EDGE[k] = 1; continue; }
    const i = k % NX, j = Math.floor(k / NX), x = X0 + i * CELL, z = Z0 + j * CELL;
    const d = Math.min(i, NX - 1 - i, j, NY - 1 - j) * CELL, f = 26 + 9 * Math.sin(x * .045 + .5) + 7 * Math.sin(z * .06 + 2) + 5 * Math.sin((x + z) * .11);
    EDGE[k] = sstep(f, f + 16, d);
  }
  const SEA0 = new Uint8Array(N), SEA = new Uint8Array(N);
  for (let k = 0; k < N; k++) SEA0[k] = ((CL[k] === 80 || CL[k] === 0) && HM[k] <= -1) || EDGE[k] < .02 ? 1 : 0;
  for (let k = 0; k < N; k++) {   // drop isolated one- or two-cell "sea" pits inland: they are Rann depressions, not sea
    if (!SEA0[k] || EDGE[k] < .02) { SEA[k] = SEA0[k]; continue; }
    const i = k % NX, j = Math.floor(k / NX); let n = 0;
    for (let b = -1; b <= 1; b++) for (let a = -1; a <= 1; a++) { const ii = i + a, jj = j + b; if ((a || b) && ii >= 0 && jj >= 0 && ii < NX && jj < NY) n += SEA0[jj * NX + ii]; }
    SEA[k] = n >= 3 ? 1 : 0;
  }
  const isSea = k => SEA[k] === 1;
  const HY = new Float32Array(N);
  for (let k = 0; k < N; k++) HY[k] = isSea(k) ? Math.max(-2.6, Math.min(-.45, -.45 + Math.min(HM[k], 0) * ZS * .5)) : Math.max(.12, HM[k] * ZS * EDGE[k]);
  const ll = (lat, lon) => ({ x: (lon - meta.lonc) * meta.kmx, z: (meta.latc - lat) * meta.kmy });
  const near = (x, z) => { const i = Math.round((x - X0) / CELL), j = Math.round((z - Z0) / CELL); return Math.min(Math.max(j, 0), NY - 1) * NX + Math.min(Math.max(i, 0), NX - 1); };
  function height(x, z) {
    const fi = Math.min(Math.max((x - X0) / CELL, 0), NX - 1.001), fj = Math.min(Math.max((z - Z0) / CELL, 0), NY - 1.001);
    const i = Math.floor(fi), j = Math.floor(fj), u = fi - i, v = fj - j, k = j * NX + i;
    return HY[k] * (1 - u) * (1 - v) + HY[k + 1] * u * (1 - v) + HY[k + NX] * (1 - u) * v + HY[k + NX + 1] * u * v;
  }
  const landAt = (x, z) => { const k = near(x, z); return IN[k] === 1 && !isSea(k) && CL[k] !== 80; };
  const S = Object.fromEntries(DATA.map(d => { const p = ll(d.lat, d.lon); return [d.id, { d, x: p.x, z: p.z }]; }));

  // district centre for the home view
  let bx0 = 1e9, bx1 = -1e9, bz0 = 1e9, bz1 = -1e9;
  for (const ring of meta.boundary) for (const [x, z] of ring) { bx0 = Math.min(bx0, x); bx1 = Math.max(bx1, x); bz0 = Math.min(bz0, z); bz1 = Math.max(bz1, z); }
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
  renderer.domElement.setAttribute('aria-label', '3D view of Kutch built from real terrain and land-cover data. Use the buttons below to visit each program.');
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
  const PAL = {   // [dry season, monsoon]
    sea: ['#b7a57c', '#b7a57c'], rann: ['#efece4', '#d3e5e2'], rannW: ['#e0dacb', '#8fc2d6'], bare: ['#c9ac80', '#b8a67c'],
    crop: ['#cfae74', '#86b55e'], shrub: ['#a99a5e', '#5f9047'], grass: ['#d2bf80', '#95c262'], tree: ['#5a7d42', '#356f38'],
    built: ['#cbbfae', '#c2b8a8'], wet: ['#aaae8b', '#6fae94'], mangr: ['#3d6a4c', '#2b6b47'],
  };
  for (const k in PAL) PAL[k] = PAL[k].map(col);
  const OUTC = col('#ebe4d4');
  const CLASS = { 10: 'tree', 20: 'shrub', 30: 'grass', 40: 'crop', 50: 'built', 90: 'wet', 95: 'mangr' };
  const kind = k => { const c = CL[k], h = HM[k]; if (isSea(k)) return 'sea'; if (c === 80 || c === 0) return 'rannW'; if (c === 60) return h < 25 ? 'rann' : 'bare'; return CLASS[c] || 'bare'; };
  const P = geo.attributes.position.array, nv = geo.attributes.position.count;
  const cDry = new Float32Array(nv * 3), cWet = new Float32Array(nv * 3);
  const tA = new THREE.Color(), tB = new THREE.Color();
  const vDry = new Float32Array(N * 3), vWet = new Float32Array(N * 3);   // one colour per grid point, blended across each triangle
  for (let k = 0; k < N; k++) {
    const kd = kind(k);
    tA.copy(PAL[kd][0]); tB.copy(PAL[kd][1]);
    if (!IN[k] && kd !== 'sea') { tA.lerp(OUTC, .62); tB.lerp(OUTC, .62); }
    const f = kd === 'crop' ? .88 + hash(k * .37, 1.3) * .2 : .96 + hash(k * .21, 7.1) * .07;   // farm patchwork
    vDry.set([tA.r * f, tA.g * f, tA.b * f], k * 3); vWet.set([tB.r * f, tB.g * f, tB.b * f], k * 3);
  }
  for (let v = 0; v < nv; v++) {
    const k = near(P[v * 3], P[v * 3 + 2]);
    cDry.set(vDry.subarray(k * 3, k * 3 + 3), v * 3); cWet.set(vWet.subarray(k * 3, k * 3 + 3), v * 3);
  }
  geo.setAttribute('color', new THREE.BufferAttribute(cDry, 3));
  geo.setAttribute('color2', new THREE.BufferAttribute(cWet, 3));
  const seasonU = { value: 0 };
  const terrainMat = new THREE.MeshStandardMaterial({ vertexColors: true, flatShading: true, roughness: 1, metalness: 0 });
  terrainMat.onBeforeCompile = sh => {   // blend dry -> monsoon colours on the GPU
    sh.uniforms.uSeason = seasonU;
    sh.vertexShader = 'attribute vec3 color2;\nuniform float uSeason;\n' + sh.vertexShader.replace('#include <color_vertex>', '#include <color_vertex>\n  vColor.rgb = mix(color.rgb, color2, uSeason);');
  };
  const terrain = new THREE.Mesh(geo, terrainMat);
  terrain.receiveShadow = true;
  scene.add(terrain);

  // sea with gentle low-poly waves
  const seaGeo = new THREE.PlaneGeometry(2400, 2400, 80, 80); seaGeo.rotateX(-Math.PI / 2); seaGeo.translate(HOME_TGT.x, -.06, HOME_TGT.z);
  const seaMat = new THREE.MeshStandardMaterial({ color: '#3d8db7', roughness: .3, metalness: .05, flatShading: true, transparent: true, opacity: .95 });
  const seaMesh = new THREE.Mesh(seaGeo, seaMat); scene.add(seaMesh);
  const seaPos = seaGeo.attributes.position;

  // district boundary (OpenStreetMap) as a dashed line hugging the ground
  const bMat = new THREE.LineDashedMaterial({ color: '#d4932f', dashSize: 2.2, gapSize: 1.3 });
  for (const ring of meta.boundary) {
    const pts = [];
    for (let i = 0; i < ring.length - 1; i++) {
      const [x1, z1] = ring[i], [x2, z2] = ring[i + 1], n = Math.max(1, Math.ceil(Math.hypot(x2 - x1, z2 - z1) / 1.2));
      for (let s = 0; s < n; s++) { const x = x1 + (x2 - x1) * s / n, z = z1 + (z2 - z1) * s / n; pts.push(new THREE.Vector3(x, Math.max(height(x, z), 0) + .4, z)); }
    }
    pts.push(pts[0].clone());
    const line = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), bMat); line.computeLineDistances(); scene.add(line);
  }

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
    const x = S.fruit.x - 3 + c * 2.4, z = S.fruit.z + 2 + r * 2.3;
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

  // rain (only while the monsoon arrives)
  const DROPS = 2600, rainPos = new Float32Array(DROPS * 6);
  for (let i = 0; i < DROPS; i++) { const x = HOME_TGT.x + (R() - .5) * 460, y = R() * 140, z = HOME_TGT.z + (R() - .5) * 330; rainPos.set([x, y, z, x + .3, y + 2.4, z], i * 6); }
  const rainGeo = new THREE.BufferGeometry(); rainGeo.setAttribute('position', new THREE.BufferAttribute(rainPos, 3));
  const rainMat = new THREE.LineBasicMaterial({ color: '#e3f1fb', transparent: true, opacity: 0, depthWrite: false });
  const rain = new THREE.LineSegments(rainGeo, rainMat); rain.visible = false; rain.frustumCulled = false; scene.add(rain);

  // hotspot anchors: ground ring + light beam + floating gem
  const ringG = new THREE.RingGeometry(2.4, 3, 48); ringG.rotateX(-Math.PI / 2);
  const beamG = new THREE.CylinderGeometry(.07, .07, 8, 6); beamG.translate(0, 4, 0);
  const gemG = new THREE.OctahedronGeometry(.95, 0);
  const spots = DATA.map(d => {
    const s = S[d.id], y = Math.max(height(s.x, s.z), .3);
    const ring = new THREE.Mesh(ringG, new THREE.MeshBasicMaterial({ color: '#ffffff', transparent: true, opacity: .85, depthWrite: false, side: THREE.DoubleSide }));
    ring.position.set(s.x, y + .3, s.z);
    const beam = new THREE.Mesh(beamG, new THREE.MeshBasicMaterial({ color: '#fff6df', transparent: true, opacity: .45, depthWrite: false }));
    beam.position.set(s.x, y, s.z);
    const gem = new THREE.Mesh(gemG, new THREE.MeshStandardMaterial({ color: d.color, emissive: d.color, emissiveIntensity: .45, flatShading: true, roughness: .4 }));
    gem.position.set(s.x, y + 9, s.z); gem.castShadow = true;
    scene.add(ring, beam, gem);
    return { d, x: s.x, z: s.z, ring, gem, y, anchor: new THREE.Vector3(s.x, y + 11.2, s.z) };
  });

  // ---------------- spatial UI ----------------
  const pinLayer = q('.xpins'), labLayer = q('.xlabels'), panel = q('.xpanel'), toast = q('.xtoast');
  const dockBtns = [...stage.querySelectorAll('.xd-places button')];
  const pins = DATA.map((d, i) => {
    const b = document.createElement('button');
    b.type = 'button'; b.className = 'xpin'; b.tabIndex = -1; b.style.setProperty('--c', d.color);
    b.innerHTML = `<i>${d.svg}</i><span>${d.short}</span>`;
    b.setAttribute('aria-label', d.title);
    b.addEventListener('click', () => { tour(false); open(i); });
    pinLayer.appendChild(b); return b;
  });
  const labels = meta.places.map(p => {
    const el = document.createElement('div'); el.className = 'xlab ' + p.kind; el.textContent = p.name; labLayer.appendChild(el);
    const y = p.kind === 'water' || p.kind === 'region' ? 1 : Math.max(height(p.x, p.z), .2) + (p.kind === 'peak' ? 1.4 : .5);
    return { el, kind: p.kind, v: new THREE.Vector3(p.x, y, p.z) };
  });
  dockBtns.forEach((b, i) => b.addEventListener('click', () => { tour(false); open(i); }));

  let cur = -1, fly = null, lastAct = performance.now(), introDone = REDUCE;
  const mini = () => q('.xtitle').classList.add('mini');
  setTimeout(mini, 9000);
  function flyTo(p, t, dur = 1700) {
    fly = { p0: camera.position.clone(), p1: p.clone(), t0: controls.target.clone(), t1: t.clone(), dur: REDUCE ? 1 : dur, start: performance.now() };
    controls.enabled = false;
  }
  function flyToSpot(s) {
    const t = new THREE.Vector3(s.x, s.y + 2, s.z);
    const dir = new THREE.Vector3(camera.position.x - t.x, 0, camera.position.z - t.z);
    if (dir.lengthSq() < 1) dir.set(0, 0, 1);
    dir.normalize();
    const narrow = stage.clientWidth < 760;
    flyTo(t.clone().add(dir.multiplyScalar(narrow ? 48 : 38)).add(new THREE.Vector3(0, narrow ? 34 : 27, 0)), t.clone().add(new THREE.Vector3(0, narrow ? -4 : 0, 0)));
  }
  const fmt = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
  function open(i) {
    cur = (i + DATA.length) % DATA.length; mini();
    const d = DATA[cur];
    q('.xp-kick').textContent = d.kick;
    q('.xp-count').textContent = `${cur + 1} / ${DATA.length}`;
    q('.xp-title').textContent = d.title;
    q('.xp-where').textContent = d.where;
    q('.xp-stat b').textContent = d.stat[0];
    q('.xp-stat span').textContent = d.stat[1];
    q('.xp-text').textContent = d.text;
    q('.xp-facts').innerHTML = d.facts.map(f => `<div><b>${fmt(f[0])}</b><span>${fmt(f[1])}</span></div>`).join('');
    const a = q('.xp-go'); a.href = d.link; a.textContent = d.link_label;
    panel.style.setProperty('--c', d.color);
    panel.classList.add('open'); panel.classList.remove('swap'); void panel.offsetWidth; panel.classList.add('swap');
    panel.setAttribute('aria-hidden', 'false');
    pins.forEach((p, k) => p.classList.toggle('on', k === cur));
    dockBtns.forEach((b, k) => { b.classList.toggle('on', k === cur); b.setAttribute('aria-current', k === cur ? 'true' : 'false'); });
    const box = q('.xd-places'), db = dockBtns[cur];   // scroll only the dock row, never the page
    box.scrollTo({ left: db.offsetLeft - box.offsetLeft - (box.clientWidth - db.offsetWidth) / 2, behavior: REDUCE ? 'auto' : 'smooth' });
    flyToSpot(spots[cur]);
    history.replaceState(null, '', '#' + d.id);
    lastAct = performance.now();
  }
  function close(reset = true) {
    cur = -1; panel.classList.remove('open'); panel.setAttribute('aria-hidden', 'true');
    pins.forEach(p => p.classList.remove('on')); dockBtns.forEach(b => { b.classList.remove('on'); b.setAttribute('aria-current', 'false'); });
    history.replaceState(null, '', location.pathname + location.search);
    if (reset) flyTo(HOME_POS, HOME_TGT, 1500);
  }
  q('.xp-x').addEventListener('click', () => { tour(false); close(); });
  q('.xp-next').addEventListener('click', () => { tour(false); open(cur + 1); });
  q('.xp-prev').addEventListener('click', () => { tour(false); open(cur - 1); });
  q('.xd-reset').addEventListener('click', () => { tour(false); close(); });

  // gentle 3D tilt of the glass panel under the pointer
  const pin = q('.xp-in');
  if (!REDUCE) {
    panel.addEventListener('pointermove', e => { const r = panel.getBoundingClientRect(); pin.style.setProperty('--ry', ((e.clientX - r.left) / r.width - .5) * 9 + 'deg'); pin.style.setProperty('--rx', -((e.clientY - r.top) / r.height - .5) * 7 + 'deg'); });
    panel.addEventListener('pointerleave', () => { pin.style.setProperty('--ry', '0deg'); pin.style.setProperty('--rx', '0deg'); });
  }

  // guided tour
  const tourBtn = q('.xd-tour'); let tourT = null;
  function tour(on) {
    clearInterval(tourT); tourT = null;
    tourBtn.setAttribute('aria-pressed', on ? 'true' : 'false');
    tourBtn.querySelector('span').textContent = on ? 'Pause' : 'Tour';
    if (on) { open(cur < 0 ? 0 : cur + 1); tourT = setInterval(() => open(cur + 1), 7000); }
  }
  tourBtn.addEventListener('click', () => tour(!tourT));
  controls.addEventListener('start', () => { mini(); lastAct = performance.now(); if (tourT) tour(false); fly = null; controls.enabled = true; });

  // seasons
  let season = 0, seasonTo = 0, rainUntil = 0, rainAmt = 0, toastT;
  const seasonBtn = q('.xd-season');
  function showToast(t) { toast.textContent = t; toast.classList.add('show'); clearTimeout(toastT); toastT = setTimeout(() => toast.classList.remove('show'), 3600); }
  function setSeason(v, quiet) {
    seasonTo = v; if (REDUCE) season = v;
    seasonBtn.setAttribute('aria-pressed', v ? 'true' : 'false');
    seasonBtn.querySelector('.lbl').textContent = v ? 'Monsoon' : 'Dry season';
    if (v && !REDUCE) rainUntil = performance.now() + 4200;
    if (!quiet) showToast(v ? 'The monsoon arrives – the Rann floods, tanks fill and the land turns green' : 'Dry season – the Rann turns to salt, tanks run low');
    if (REDUCE) applySeason(v);
  }
  seasonBtn.addEventListener('click', () => setSeason(seasonTo ? 0 : 1));

  const CROWN = [col('#7f9150'), col('#4f8f4c')], SHRUB = [col('#9a9256'), col('#5d8d45')], CROP = [col('#cdb77a'), col('#5f9e4f')], CLOUD = [col('#ffffff'), col('#b9c2cb')];
  const SUNC = [col('#ffe6bd'), col('#f1f2ee')], HEMI = [col('#fff4dc'), col('#e9eef0')], SEAC = [col('#3d8db7'), col('#4b8aa3')];
  function applySeason(s) {
    seasonU.value = s;
    mats.crown.color.lerpColors(CROWN[0], CROWN[1], s); mats.shrub.color.lerpColors(SHRUB[0], SHRUB[1], s); mats.crop.color.lerpColors(CROP[0], CROP[1], s);
    cloudMat.color.lerpColors(CLOUD[0], CLOUD[1], s); cloudMat.emissiveIntensity = .14 * (1 - s);
    sun.color.lerpColors(SUNC[0], SUNC[1], s); sun.intensity = 2.7 - 1.0 * s;
    hemi.color.lerpColors(HEMI[0], HEMI[1], s);
    seaMat.color.lerpColors(SEAC[0], SEAC[1], s);
    skyU.top.value.lerpColors(SKY.dryTop, SKY.wetTop, s); skyU.bot.value.lerpColors(SKY.dryBot, SKY.wetBot, s); scene.fog.color.copy(skyU.bot.value);
    waters.forEach(({ m, t }) => { m.position.y = s < .02 ? t.y - .1 : t.y + .02 + .14 * s; m.scale.setScalar(.6 + .4 * s); });
    crops.forEach((c, i) => { dummy.position.set(c.x, c.y, c.z); dummy.rotation.set(0, c.ry, 0); dummy.scale.set(c.s, c.s * (.18 + .82 * s), c.s); dummy.updateMatrix(); cropMesh.setMatrixAt(i, dummy.matrix); });
    cropMesh.instanceMatrix.needsUpdate = true;
    const fs = Math.max(.001, sstep(.55, 1, s));
    fruits.forEach((f, i) => { dummy.position.set(f.x, f.y, f.z); dummy.rotation.set(0, 0, 0); dummy.scale.setScalar(fs); dummy.updateMatrix(); fruitMesh.setMatrixAt(i, dummy.matrix); });
    fruitMesh.instanceMatrix.needsUpdate = true;
  }
  applySeason(0);

  // ---------------- size, loop ----------------
  const W = { w: 1, h: 1 };
  const setHH = () => stage.style.setProperty('--hh', (document.querySelector('header')?.offsetHeight || 67) + 'px');
  setHH(); addEventListener('resize', setHH);
  function resize() { W.w = stage.clientWidth; W.h = stage.clientHeight; renderer.setSize(W.w, W.h, false); camera.aspect = W.w / W.h; camera.updateProjectionMatrix(); }
  new ResizeObserver(resize).observe(stage); resize();

  const v3 = new THREE.Vector3(); let last = performance.now(), running = true;
  document.addEventListener('visibilitychange', () => { running = !document.hidden; if (running) { last = performance.now(); requestAnimationFrame(loop); } });

  function project(v) { v3.copy(v).project(camera); return { x: (v3.x * .5 + .5) * W.w, y: (-v3.y * .5 + .5) * W.h, behind: v3.z > 1 }; }
  function placeUI() {
    for (let i = 0; i < spots.length; i++) {
      const s = spots[i], el = pins[i], p = project(s.anchor);
      const off = p.behind || p.x < -60 || p.x > W.w + 60 || p.y < -20 || p.y > W.h + 80;
      el.classList.toggle('off', off);
      if (off) { el._r = null; continue; }
      const d = camera.position.distanceTo(s.anchor), sc = THREE.MathUtils.clamp(130 / d, .7, 1.12);
      el.style.transform = `translate3d(${p.x.toFixed(1)}px,${p.y.toFixed(1)}px,0) translate(-50%,-100%) scale(${sc.toFixed(3)})`;
      if (el._w) el._r = { x0: p.x - el._w * sc / 2, x1: p.x + el._w * sc / 2, y0: p.y - el._h * sc - 12, y1: p.y };
      el.style.zIndex = String(3000 - Math.round(d) + (i === cur ? 800 : 0));
    }
    const camD = camera.position.distanceTo(controls.target), boxes = [];
    for (let i = 0; i < pins.length; i++) {
      const el = pins[i]; if (el.classList.contains('off')) continue;
      if (!el._w) { el._w = el.offsetWidth; el._h = el.offsetHeight; }
      const r = el._r; if (r) boxes.push(r);
    }
    for (const l of labels) {
      const p = project(l.v);
      let show = !p.behind && p.x > -80 && p.x < W.w + 80 && p.y > -20 && p.y < W.h + 20 && (l.kind === 'town' || l.kind === 'peak' ? camD < 420 : camD > 140);
      if (show && (l.kind === 'town' || l.kind === 'peak')) {
        if (!l.w) { l.w = l.el.offsetWidth || 60; l.h = l.el.offsetHeight || 22; }
        const a = { x0: p.x - l.w / 2, x1: p.x + l.w / 2, y0: p.y - 4, y1: p.y - 4 + l.h };
        if (boxes.some(b => a.x0 < b.x1 && a.x1 > b.x0 && a.y0 < b.y1 && a.y1 > b.y0)) show = false;
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
    controls.autoRotate = !REDUCE && introDone && cur < 0 && !fly && now - lastAct > 7000;
    controls.update();

    if (season !== seasonTo) {
      season = seasonTo > season ? Math.min(seasonTo, season + dt / 2.8) : Math.max(seasonTo, season - dt / 2.2);
      applySeason(ease(season));
    }
    const rainTo = seasonTo === 1 && now < rainUntil ? 1 : 0;
    rainAmt += (rainTo - rainAmt) * Math.min(1, dt * 2.5);
    rain.visible = rainAmt > .01; rainMat.opacity = rainAmt * .6;
    if (rain.visible) {
      const a = rainGeo.attributes.position.array, x0 = HOME_TGT.x - 230, x1 = HOME_TGT.x + 230;
      for (let i = 0; i < DROPS; i++) { const o = i * 6; let y = a[o + 1] - 90 * dt; if (y < 0) y += 140; a[o + 1] = y; a[o + 4] = y + 2.4; a[o] += 8 * dt; if (a[o] > x1) a[o] = x0; a[o + 3] = a[o] + .3; }
      rainGeo.attributes.position.needsUpdate = true;
    }

    if (!REDUCE) {
      for (let i = 0; i < seaPos.count; i++) { const x = seaPos.getX(i), z = seaPos.getZ(i); seaPos.setY(i, -.06 + Math.sin(x * .09 + t * 1.1) * .05 + Math.cos(z * .07 + t * .8) * .04); }
      seaPos.needsUpdate = true; seaGeo.computeVertexNormals();
      for (const c of clouds) { c.position.x += c.userData.v * dt; if (c.position.x > HOME_TGT.x + 320) c.position.x = HOME_TGT.x - 320; }
      for (const g of cows) g.userData.head.position.y = .95 - (Math.sin(t * 1.3 + g.userData.ph) > .6 ? .35 : 0);
      flag.rotation.y = Math.sin(t * 2.4) * .25;
      for (let i = 0; i < spots.length; i++) {
        const s = spots[i], on = i === cur;
        s.gem.position.y = s.y + 9 + Math.sin(t * 1.6 + i) * .5; s.gem.rotation.y = t * .9 + i;
        const p = (t * .6 + i * .13) % 1; s.ring.scale.setScalar((on ? 1.25 : 1) + p * .5); s.ring.material.opacity = (on ? 1 : .8) * (1 - p);
      }
    }
    sky.position.copy(camera.position);
    renderer.render(scene, camera);
    placeUI();
    requestAnimationFrame(loop);
  }

  // first frame, then intro: fly in, the monsoon arrives
  stage.classList.add('ready'); stage.classList.remove('nogl');
  requestAnimationFrame(loop);
  const target = DATA.findIndex(d => '#' + d.id === location.hash);
  if (REDUCE) { setSeason(1, true); if (target >= 0) open(target); }
  else {
    flyTo(HOME_POS, HOME_TGT, 3600);
    setTimeout(() => setSeason(1), 2000);
    setTimeout(() => { introDone = true; if (target >= 0) open(target); }, 3800);
  }

  addEventListener('keydown', e => {
    if (e.target.closest && e.target.closest('input,textarea')) return;
    if (e.key === 'Escape' && cur >= 0) { tour(false); close(); }
    else if (e.key === 'ArrowRight' && cur >= 0) { tour(false); open(cur + 1); }
    else if (e.key === 'ArrowLeft' && cur >= 0) { tour(false); open(cur - 1); }
  });
}
