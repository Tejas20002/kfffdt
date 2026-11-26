// Explore Kutch in 3D – a stylised Kutch landscape with the Trust's programs as spatial pins.
// Not a map: places sit roughly where the work happens (Lakhpat west, Mundra on the coast,
// Bhachau east, the salt Rann to the north). Program data comes from the page (#x3d-data).
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const stage = document.getElementById('x3d');
const DATA = JSON.parse(document.getElementById('x3d-data').textContent);
const REDUCE = matchMedia('(prefers-reduced-motion: reduce)').matches;
const q = s => stage.querySelector(s);

try { init(); } catch (e) { console.error(e); stage.classList.add('nogl'); }

function init() {
  if (!document.createElement('canvas').getContext('webgl2')) throw new Error('WebGL2 not available');

  // ---------------- helpers ----------------
  const rng = seed => () => { seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  const R = rng(1989);
  const hash = (x, y) => { const s = Math.sin(x * 127.1 + y * 311.7) * 43758.5453; return s - Math.floor(s); };
  const vnoise = (x, y) => {
    const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi;
    const u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf);
    const a = hash(xi, yi), b = hash(xi + 1, yi), c = hash(xi, yi + 1), d = hash(xi + 1, yi + 1);
    return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v;
  };
  const fbm = (x, y) => { let s = 0, a = .5, f = 1; for (let i = 0; i < 4; i++) { s += a * vnoise(x * f, y * f); f *= 2.03; a *= .5; } return s; };
  const sstep = (a, b, x) => { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); };
  const ease = k => k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
  const col = h => new THREE.Color(h);
  const H = Object.fromEntries(DATA.map(d => [d.id, d]));

  // ---------------- landscape ----------------
  const coastS = x => 62 + 8 * Math.sin(x * .045) + 4 * Math.sin(x * .13 + 1);   // sea south of this z (Gulf of Kutch)
  const coastW = z => -96 + 6 * Math.sin(z * .06);                              // sea west of this x
  const rannN = x => -54 + 6 * Math.sin(x * .05 + 1) + 3 * Math.sin(x * .17);   // salt Rann north of this z
  const rannE = z => 98 + 5 * Math.sin(z * .07);                                // salt Rann east of this x
  const edgeF = (x, z) => { const r = Math.pow(Math.abs(x) ** 4 + (Math.abs(z) * 1.15) ** 4, .25); return sstep(112, 150, r + (fbm(x * .03 + 40, z * .03) - .45) * 30); };
  const seaF = (x, z) => Math.max(sstep(coastS(x) - 6, coastS(x) + 6, z), 1 - sstep(coastW(z) - 6, coastW(z) + 6, x), edgeF(x, z));
  const rannF = (x, z) => Math.max(1 - sstep(rannN(x) - 8, rannN(x) + 4, z), sstep(rannE(z) - 4, rannE(z) + 8, x));

  const TANKS = [
    { x: H.jal.x, z: H.jal.z, r: 7.5 }, { x: H.water.x, z: H.water.z, r: 6, dam: true },
    { x: 28, z: 14, r: 4.5 }, { x: -22, z: 26, r: 4.5 }, { x: 55, z: -26, r: 4 }, { x: -62, z: -6, r: 4.5 },
    { x: 2, z: 46, r: 4 }, { x: -30, z: -30, r: 4 }, { x: 60, z: 12, r: 3.8 },
  ];
  const PLOTS = [[-6, -6, 9, 6], [6, -6, 9, 6], [0, 6, 13, 5.5]].map(([dx, dz, w, d]) => ({ x: H.fodder.x + dx, z: H.fodder.z + dz, w, d }));
  const inPlot = (x, z) => PLOTS.some(p => Math.abs(x - p.x) < p.w / 2 && Math.abs(z - p.z) < p.d / 2);

  function baseHeight(x, z) {
    let h = 1 + fbm(x * .025 + 3, z * .025 - 7) * 7;
    const ridgeZ = -18 + 10 * Math.sin(x * .035);
    h += 5.5 * Math.exp(-((z - ridgeZ) ** 2) / 140) * (.5 + fbm(x * .05, z * .05));   // central hill range
    h += 9 * Math.exp(-(((x - 8) ** 2) + ((z + 36) ** 2)) / 160);                   // a tall hill near the Rann
    for (const p of PLOTS) h -= 1.2 * Math.exp(-(((x - p.x) ** 2) + ((z - p.z) ** 2)) / 80) * (h > 3 ? 1 : 0); // flatter farmland
    const rann = rannF(x, z), sea = seaF(x, z);
    h = h * (1 - rann) + .35 * rann;
    return h * (1 - sea) - 3 * sea;
  }
  TANKS.forEach(t => { t.base = baseHeight(t.x, t.z); t.bed = t.base - 1.6; });
  function height(x, z) {
    let h = baseHeight(x, z);
    for (const t of TANKS) {
      const d = Math.hypot(x - t.x, z - t.z);
      if (d < t.r) { const w = Math.min(1, (1 - d * d / (t.r * t.r)) * 2.5); h = h * (1 - w) + t.bed * w; }
      else if (d < t.r * 1.45) h += .5 * Math.sin(Math.PI * (d - t.r) / (.45 * t.r));            // earth bund around the tank
    }
    return h;
  }
  const nearTank = (x, z, k = 1.5) => TANKS.some(t => Math.hypot(x - t.x, z - t.z) < t.r * k);
  const nearSpot = (x, z, k = 9) => DATA.some(d => d.id !== 'forest' && Math.hypot(x - d.x, z - d.z) < k);
  const onLand = (x, z) => seaF(x, z) < .02 && rannF(x, z) < .02;

  // ---------------- renderer, scene, camera ----------------
  const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 1.75));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  renderer.setClearColor('#cfe0e6');
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.domElement.setAttribute('aria-label', '3D view of a stylised Kutch landscape. Use the buttons below to visit each program.');
  renderer.domElement.setAttribute('role', 'img');
  stage.prepend(renderer.domElement);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(40, 1, .5, 1800);
  const HOME_POS = new THREE.Vector3(0, 105, 140), HOME_TGT = new THREE.Vector3(0, 0, 8);
  camera.position.copy(REDUCE ? HOME_POS : new THREE.Vector3(-40, 250, 330));

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.target.copy(HOME_TGT);
  Object.assign(controls, { enableDamping: true, dampingFactor: .07, minDistance: 28, maxDistance: 250, minPolarAngle: .25, maxPolarAngle: 1.2, screenSpacePanning: false, autoRotateSpeed: .35, rotateSpeed: .6 });
  controls.addEventListener('change', () => {
    controls.target.x = THREE.MathUtils.clamp(controls.target.x, -95, 95);
    controls.target.z = THREE.MathUtils.clamp(controls.target.z, -80, 80);
    controls.target.y = THREE.MathUtils.clamp(controls.target.y, 0, 14);
  });

  // sky dome + fog
  const SKY = { dryTop: col('#86bfe3'), dryBot: col('#f5e4c3'), wetTop: col('#7f95a8'), wetBot: col('#e1e6e1') };
  const skyU = { top: { value: SKY.dryTop.clone() }, bot: { value: SKY.dryBot.clone() } };
  const sky = new THREE.Mesh(new THREE.SphereGeometry(900, 32, 16), new THREE.ShaderMaterial({
    side: THREE.BackSide, depthWrite: false, fog: false, uniforms: skyU,
    vertexShader: 'varying vec3 vp; void main(){ vp = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
    fragmentShader: 'uniform vec3 top; uniform vec3 bot; varying vec3 vp; void main(){ float h = clamp(vp.y * 1.5 + .06, 0., 1.); gl_FragColor = vec4(mix(bot, top, pow(h, .75)), 1.); #include <colorspace_fragment> }',
  }));
  scene.add(sky);
  scene.fog = new THREE.Fog(SKY.dryBot.clone(), 190, 560);

  const hemi = new THREE.HemisphereLight('#fff4dc', '#8a7552', 1.15);
  const sun = new THREE.DirectionalLight('#ffe6bd', 2.7);
  sun.position.set(90, 130, 70);
  sun.castShadow = true;
  Object.assign(sun.shadow.camera, { left: -130, right: 130, top: 130, bottom: -130, near: 10, far: 420 });
  sun.shadow.mapSize.set(2048, 2048);
  sun.shadow.bias = -.0004; sun.shadow.normalBias = .03;
  scene.add(hemi, sun, sun.target);

  // terrain: non-indexed so every triangle gets one flat colour (low-poly look); two palettes, dry and monsoon
  const SIZE = 330, SEG = 190;
  let geo = new THREE.PlaneGeometry(SIZE, SIZE, SEG, SEG);
  geo.rotateX(-Math.PI / 2);
  const pos = geo.attributes.position;
  for (let i = 0; i < pos.count; i++) pos.setY(i, height(pos.getX(i), pos.getZ(i)));
  geo = geo.toNonIndexed();
  geo.computeVertexNormals();
  const P = geo.attributes.position.array, nv = geo.attributes.position.count;
  const dryCols = new Float32Array(nv * 3), wetCols = new Float32Array(nv * 3), curCols = new Float32Array(nv * 3);
  const PAL = {
    sand: col('#dcc395'), ochre: col('#cfa86e'), dgrass: col('#bfb07c'), rock: col('#a48a68'), salt: col('#f2efe7'), beach: col('#e8d9b6'),
    bed: col('#8a6a48'), bund: col('#b99b6b'), soil: col('#a68357'), seabed: col('#cbb78d'),
    g1: col('#a9cb7c'), g2: col('#88b968'), g3: col('#70a258'), rockW: col('#8f8c6c'), saltW: col('#d3e6e3'), bedW: col('#6b5a44'), bundW: col('#95ab64'), soilW: col('#7d6a45'),
  };
  const tmpA = new THREE.Color(), tmpB = new THREE.Color(), mA = new THREE.Color(), mB = new THREE.Color();
  const mix3 = (a, b, c, n, out) => { const k = THREE.MathUtils.clamp((n - .3) / .42, 0, 1); return k < .5 ? out.copy(a).lerp(b, k * 2) : out.copy(b).lerp(c, (k - .5) * 2); };
  for (let t = 0; t < nv; t += 3) {
    const cx = (P[t * 3] + P[t * 3 + 3] + P[t * 3 + 6]) / 3, cy = (P[t * 3 + 1] + P[t * 3 + 4] + P[t * 3 + 7]) / 3, cz = (P[t * 3 + 2] + P[t * 3 + 5] + P[t * 3 + 8]) / 3;
    const sea = seaF(cx, cz), rann = rannF(cx, cz), n = fbm(cx * .09 + 11, cz * .09 - 4);
    let d, w;
    if (sea > .55) { d = w = PAL.seabed; }
    else {
      mix3(PAL.sand, PAL.ochre, PAL.dgrass, n, mA); mix3(PAL.g1, PAL.g2, PAL.g3, n, mB);
      const rk = sstep(12.5, 15.5, cy); if (rk > 0) { mA.lerp(PAL.rock, rk); mB.lerp(PAL.rockW, rk); }
      d = mA; w = mB;
      if (sea > .06) { d = w = PAL.beach; }
      const tk = TANKS.find(k => Math.hypot(cx - k.x, cz - k.z) < k.r * 1.3);
      if (tk) { const inside = Math.hypot(cx - tk.x, cz - tk.z) < tk.r * .92; d = inside ? PAL.bed : PAL.bund; w = inside ? PAL.bedW : PAL.bundW; }
      if (inPlot(cx, cz)) { d = PAL.soil; w = PAL.soilW; }
    }
    tmpA.copy(d); tmpB.copy(w);
    if (rann > .15) { tmpA.lerp(PAL.salt, Math.min(1, rann * 1.3)); tmpB.lerp(PAL.saltW, Math.min(1, rann * 1.3)); }
    const j = .94 + hash(cx * .7, cz * .7) * .1;
    for (let v = 0; v < 3; v++) {
      const o = (t + v) * 3;
      dryCols[o] = tmpA.r * j; dryCols[o + 1] = tmpA.g * j; dryCols[o + 2] = tmpA.b * j;
      wetCols[o] = tmpB.r * j; wetCols[o + 1] = tmpB.g * j; wetCols[o + 2] = tmpB.b * j;
    }
  }
  curCols.set(dryCols);
  geo.setAttribute('color', new THREE.BufferAttribute(curCols, 3));
  const terrain = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ vertexColors: true, flatShading: true, roughness: 1, metalness: 0 }));
  terrain.receiveShadow = true;
  scene.add(terrain);

  // sea with low-poly waves
  const seaGeo = new THREE.PlaneGeometry(1000, 1000, 70, 70); seaGeo.rotateX(-Math.PI / 2);
  const seaMat = new THREE.MeshStandardMaterial({ color: '#3d8db7', roughness: .3, metalness: .05, flatShading: true, transparent: true, opacity: .94 });
  const seaMesh = new THREE.Mesh(seaGeo, seaMat); seaMesh.receiveShadow = true; scene.add(seaMesh);
  const seaPos = seaGeo.attributes.position;

  // shared parts
  const M = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, flatShading: true, roughness: .9, ...o });
  const mats = { trunk: M('#7a5634'), crown: M('#8f9a5a'), hut: M('#f3ede2'), thatch: M('#a7773f'), wall: M('#efe6d6'), tile: M('#b9563a'), concrete: M('#c9c1b0'), steel: M('#9aa7ad'), tankTop: M('#dfe8ec'), crop: M('#cdb77a'), bale: M('#e2b55a'), fruit: M('#e98b2a', { roughness: .6 }), cowW: M('#f1ece4'), cowB: M('#8a5a3c'), dark: M('#3a3a36'), flag: M('#e98b2a', { side: THREE.DoubleSide }) };
  const dummy = new THREE.Object3D();
  function instanced(geom, mat, list, cast = true) {
    const m = new THREE.InstancedMesh(geom, mat, list.length);
    list.forEach((p, i) => { dummy.position.set(p.x, p.y, p.z); dummy.rotation.set(0, p.ry || 0, 0); dummy.scale.setScalar(p.s || 1); if (p.sy) dummy.scale.y = p.sy; dummy.updateMatrix(); m.setMatrixAt(i, dummy.matrix); });
    m.castShadow = cast; m.receiveShadow = true; scene.add(m); return m;
  }

  // trees: a planted forest near Bhuj plus scattered trees
  const trees = [];
  for (let i = 0; i < 90; i++) {
    const a = R() * Math.PI * 2, r = Math.sqrt(R()) * 17, x = H.forest.x + Math.cos(a) * r, z = H.forest.z + Math.sin(a) * r;
    if (Math.hypot(x - H.forest.x, z - H.forest.z) < 3.5 || nearTank(x, z) || !onLand(x, z)) continue;
    trees.push({ x, z, y: height(x, z) - .1, s: .8 + R() * .55, ry: R() * 6 });
  }
  for (let i = 0; i < 900 && trees.length < 260; i++) {
    const x = (R() - .5) * 200, z = (R() - .5) * 130, y = height(x, z);
    if (!onLand(x, z) || y > 12 || y < 1 || nearTank(x, z) || nearSpot(x, z) || inPlot(x, z)) continue;
    if (fbm(x * .04, z * .04) < .45) continue;  // clumps, not an even carpet
    trees.push({ x, z, y: y - .1, s: .6 + R() * .6, ry: R() * 6 });
  }
  const trunkG = new THREE.CylinderGeometry(.18, .3, 1.7, 5); trunkG.translate(0, .85, 0);
  const crownG = new THREE.IcosahedronGeometry(1.3, 0); crownG.translate(0, 2.4, 0);
  instanced(trunkG, mats.trunk, trees); instanced(crownG, mats.crown, trees);

  // bhunga huts (round Kutchi houses) in a few villages
  const huts = [];
  const villages = [[H.jal.x + 12, H.jal.z - 9, 8], [H.fodder.x - 12, H.fodder.z + 9, 7], [H.animal.x + 10, H.animal.z - 8, 7], [H.school.x + 9, H.school.z + 7, 4], [H.drink.x + 8, H.drink.z + 9, 8], [H.water.x + 10, H.water.z - 10, 6], [-24, 8, 6], [40, 36, 5]];
  for (const [vx, vz, n] of villages) for (let i = 0; i < n; i++) {
    const a = i / n * Math.PI * 2 + R() * .5, r = 2.4 + R() * 3.2, x = vx + Math.cos(a) * r, z = vz + Math.sin(a) * r;
    if (onLand(x, z) && !nearTank(x, z, 1.2)) huts.push({ x, z, y: height(x, z) - .15, s: .85 + R() * .3, ry: R() * 6 });
  }
  const hutG = new THREE.CylinderGeometry(.9, .95, 1.3, 9); hutG.translate(0, .65, 0);
  const roofG = new THREE.ConeGeometry(1.25, 1.2, 9); roofG.translate(0, 1.9, 0);
  instanced(hutG, mats.hut, huts); instanced(roofG, mats.thatch, huts);

  // rebuilt village after 2001: rows of permanent houses
  const houses = [];
  for (let r = 0; r < 4; r++) for (let c = 0; c < 6; c++) {
    if ((r === 1 || r === 2) && (c === 2 || c === 3)) continue;  // open square in the middle
    const x = H.rebuild.x - 8 + c * 3.2, z = H.rebuild.z - 5 + r * 3.4;
    houses.push({ x, z, y: height(x, z) - .1, ry: 0 });
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
  school.position.set(H.school.x + 4, height(H.school.x + 4, H.school.z - 3) - .1, H.school.z - 3); school.rotation.y = .3; scene.add(school);

  // drinking-water tower (WASMO)
  const tower = new THREE.Group();
  for (const [lx, lz] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) { const leg = new THREE.Mesh(new THREE.BoxGeometry(.25, 6, .25), mats.steel); leg.position.set(lx * 1.1, 3, lz * 1.1); tower.add(leg); }
  const tank = new THREE.Mesh(new THREE.CylinderGeometry(2, 2, 2.4, 12), mats.tankTop); tank.position.y = 7.2;
  const cap = new THREE.Mesh(new THREE.ConeGeometry(2.1, .8, 12), mats.steel); cap.position.y = 8.8;
  tower.add(tank, cap); tower.traverse(o => { o.castShadow = true; });
  tower.position.set(H.drink.x - 5, height(H.drink.x - 5, H.drink.z + 2) - .2, H.drink.z + 2); scene.add(tower);

  // cattle near the animal-health centre
  const cows = [];
  const cowG = { body: new THREE.BoxGeometry(1.7, .8, .75), head: new THREE.BoxGeometry(.55, .5, .5), leg: new THREE.BoxGeometry(.18, .65, .18) };
  for (let i = 0; i < 9; i++) {
    const a = R() * Math.PI * 2, r = 5 + R() * 5, x = H.animal.x + Math.cos(a) * r, z = H.animal.z + Math.sin(a) * r;
    if (!onLand(x, z)) continue;
    const g = new THREE.Group(), m = R() < .6 ? mats.cowW : mats.cowB;
    const body = new THREE.Mesh(cowG.body, m); body.position.y = 1.05;
    const head = new THREE.Mesh(cowG.head, m); head.position.set(1, .95, 0);
    g.add(body, head);
    for (const [lx, lz] of [[-.6, -.25], [.6, -.25], [-.6, .25], [.6, .25]]) { const l = new THREE.Mesh(cowG.leg, m); l.position.set(lx, .33, lz); g.add(l); }
    g.traverse(o => { o.castShadow = true; });
    g.position.set(x, height(x, z) - .05, z); g.rotation.y = R() * 6; g.userData = { head, ph: R() * 6 };
    scene.add(g); cows.push(g);
  }

  // fodder plots: crop rows that grow with the monsoon, plus hay bales
  const crops = [];
  for (const p of PLOTS) for (let x = -p.w / 2 + .6; x < p.w / 2; x += .9) for (let z = -p.d / 2 + .5; z < p.d / 2; z += 1.1) {
    const wx = p.x + x, wz = p.z + z; crops.push({ x: wx, z: wz, y: height(wx, wz) - .05, ry: R() * 3 });
  }
  const cropG = new THREE.ConeGeometry(.32, 1.3, 4); cropG.translate(0, .65, 0);
  const cropMesh = instanced(cropG, mats.crop, crops, false);
  const baleG = new THREE.CylinderGeometry(.6, .6, 1.1, 10); baleG.rotateZ(Math.PI / 2); baleG.translate(0, .6, 0);
  instanced(baleG, mats.bale, [[-9, 4], [-9, 5.4], [-7.6, 4.7]].map(([dx, dz]) => ({ x: H.fodder.x + dx, z: H.fodder.z + dz, y: height(H.fodder.x + dx, H.fodder.z + dz), ry: .4 })));

  // orchard near the fruit hotspot; fruit appears after the rains
  const orch = [], fruits = [];
  for (let r = 0; r < 4; r++) for (let c = 0; c < 5; c++) {
    const x = H.fruit.x - 4 + c * 3.4, z = H.fruit.z + 2 + r * 3.3;
    if (!onLand(x, z)) continue;
    const y = height(x, z) - .1; orch.push({ x, z, y, s: .75 });
    for (let k = 0; k < 5; k++) { const a = k / 5 * Math.PI * 2 + r, yy = y + 1.7 + R() * .9; fruits.push({ x: x + Math.cos(a) * .85, z: z + Math.sin(a) * .85, y: yy }); }
  }
  const oCrown = new THREE.SphereGeometry(1.25, 7, 5); oCrown.translate(0, 2.2, 0);
  instanced(trunkG, mats.trunk, orch); instanced(oCrown, M('#4f8d4f'), orch);
  const fruitG = new THREE.IcosahedronGeometry(.2, 0);
  const fruitMesh = instanced(fruitG, mats.fruit, fruits.map(f => ({ ...f, s: .001 })), false);

  // tanks: water discs rise with the monsoon; one check dam on the water-conservation tank
  const waterMat = new THREE.MeshStandardMaterial({ color: '#3b97cf', roughness: .15, metalness: .05, transparent: true, opacity: .93 });
  const waters = TANKS.map(t => { const m = new THREE.Mesh(new THREE.CircleGeometry(t.r * 1.02, 32), waterMat); m.rotation.x = -Math.PI / 2; m.position.set(t.x, t.bed - .3, t.z); m.receiveShadow = true; scene.add(m); return { m, t }; });
  for (const t of TANKS.filter(k => k.dam)) {
    const dam = new THREE.Mesh(new THREE.BoxGeometry(t.r * 2.3, 2, 1), mats.concrete);
    dam.position.set(t.x, t.base - .2, t.z + t.r * 1.02); dam.castShadow = dam.receiveShadow = true; scene.add(dam);
  }

  // clouds
  const cloudMat = new THREE.MeshStandardMaterial({ color: '#ffffff', emissive: '#ffffff', emissiveIntensity: .14, flatShading: true, roughness: 1, transparent: true, opacity: .82, depthWrite: false });
  const clouds = [];
  const puffG = new THREE.IcosahedronGeometry(1, 1);
  for (let i = 0; i < 7; i++) {
    const g = new THREE.Group(), n = 5 + Math.floor(R() * 3);
    for (let k = 0; k < n; k++) { const r = 2.4 + R() * 2.6 - Math.abs(k - n / 2) * .35; const s = new THREE.Mesh(puffG, cloudMat); s.scale.set(r, r * .62, r); s.position.set(k * 2.7 - n * 1.35, R() * 1.2, (R() - .5) * 3.5); s.castShadow = true; g.add(s); }
    g.position.set(-210 + i * 64 + R() * 24, 54 + R() * 12, -100 + R() * 180); g.userData.v = 2 + R() * 2.5;
    scene.add(g); clouds.push(g);
  }

  // rain (only while the monsoon arrives)
  const DROPS = 1600, rainPos = new Float32Array(DROPS * 6);
  for (let i = 0; i < DROPS; i++) { const x = (R() - .5) * 260, y = R() * 100, z = (R() - .5) * 240; rainPos.set([x, y, z, x + .25, y + 1.8, z], i * 6); }
  const rainGeo = new THREE.BufferGeometry(); rainGeo.setAttribute('position', new THREE.BufferAttribute(rainPos, 3));
  const rainMat = new THREE.LineBasicMaterial({ color: '#e3f1fb', transparent: true, opacity: 0, depthWrite: false });
  const rain = new THREE.LineSegments(rainGeo, rainMat); rain.visible = false; rain.frustumCulled = false; scene.add(rain);

  // hotspot anchors: ground ring + light beam + floating gem
  const ringG = new THREE.RingGeometry(2.4, 3, 48); ringG.rotateX(-Math.PI / 2);
  const beamG = new THREE.CylinderGeometry(.07, .07, 8, 6); beamG.translate(0, 4, 0);
  const gemG = new THREE.OctahedronGeometry(.95, 0);
  const spots = DATA.map(d => {
    const y = Math.max(height(d.x, d.z), .4);
    const ring = new THREE.Mesh(ringG, new THREE.MeshBasicMaterial({ color: '#ffffff', transparent: true, opacity: .85, depthWrite: false, side: THREE.DoubleSide }));
    ring.position.set(d.x, y + .25, d.z);
    const beam = new THREE.Mesh(beamG, new THREE.MeshBasicMaterial({ color: '#fff6df', transparent: true, opacity: .45, depthWrite: false }));
    beam.position.set(d.x, y, d.z);
    const gem = new THREE.Mesh(gemG, new THREE.MeshStandardMaterial({ color: d.color, emissive: d.color, emissiveIntensity: .45, flatShading: true, roughness: .4 }));
    gem.position.set(d.x, y + 9, d.z); gem.castShadow = true;
    scene.add(ring, beam, gem);
    return { d, ring, gem, y, anchor: new THREE.Vector3(d.x, y + 11.2, d.z) };
  });

  // ---------------- spatial UI ----------------
  const pinLayer = q('.xpins'), panel = q('.xpanel'), toast = q('.xtoast');
  const dockBtns = [...stage.querySelectorAll('.xd-places button')];
  const pins = DATA.map((d, i) => {
    const b = document.createElement('button');
    b.type = 'button'; b.className = 'xpin'; b.tabIndex = -1; b.style.setProperty('--c', d.color);
    b.innerHTML = `<i>${d.svg}</i><span>${d.short}</span>`;
    b.setAttribute('aria-label', d.title);
    b.addEventListener('click', () => open(i));
    pinLayer.appendChild(b); return b;
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
    const t = new THREE.Vector3(s.d.x, s.y + 2, s.d.z);
    const dir = new THREE.Vector3(camera.position.x - t.x, 0, camera.position.z - t.z);
    if (dir.lengthSq() < 1) dir.set(0, 0, 1);
    dir.normalize();
    const narrow = stage.clientWidth < 760;
    flyTo(t.clone().add(dir.multiplyScalar(narrow ? 44 : 34)).add(new THREE.Vector3(0, narrow ? 30 : 23, 0)), t.clone().add(new THREE.Vector3(0, narrow ? -4 : 0, 0)));
  }
  const fmt = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
  function open(i) {
    cur = (i + DATA.length) % DATA.length; mini();
    const d = DATA[cur];
    q('.xp-kick').textContent = d.kick;
    q('.xp-count').textContent = `${cur + 1} / ${DATA.length}`;
    q('.xp-title').textContent = d.title;
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
    if (!quiet) showToast(v ? 'The monsoon arrives – tanks fill and the land turns green' : 'Dry season – tanks run low, fodder is scarce');
    if (REDUCE) applySeason(v);
  }
  seasonBtn.addEventListener('click', () => setSeason(seasonTo ? 0 : 1));

  const cc = new THREE.Color();
  const CROWN = [col('#8f9a5a'), col('#4f8f4c')], CROP = [col('#cdb77a'), col('#5f9e4f')], CLOUD = [col('#ffffff'), col('#b9c2cb')];
  const SUNC = [col('#ffe6bd'), col('#f1f2ee')], HEMI = [col('#fff4dc'), col('#e9eef0')], SEAC = [col('#3d8db7'), col('#4b8aa3')];
  function applySeason(s) {
    for (let i = 0; i < curCols.length; i++) curCols[i] = dryCols[i] + (wetCols[i] - dryCols[i]) * s;
    geo.attributes.color.needsUpdate = true;
    mats.crown.color.lerpColors(CROWN[0], CROWN[1], s);
    mats.crop.color.lerpColors(CROP[0], CROP[1], s);
    cloudMat.color.lerpColors(CLOUD[0], CLOUD[1], s); cloudMat.emissiveIntensity = .14 * (1 - s);
    sun.color.lerpColors(SUNC[0], SUNC[1], s); sun.intensity = 2.7 - 1.0 * s;
    hemi.color.lerpColors(HEMI[0], HEMI[1], s);
    seaMat.color.lerpColors(SEAC[0], SEAC[1], s);
    skyU.top.value.lerpColors(SKY.dryTop, SKY.wetTop, s); skyU.bot.value.lerpColors(SKY.dryBot, SKY.wetBot, s); scene.fog.color.copy(skyU.bot.value);
    waters.forEach(({ m, t }) => { m.position.y = s < .02 ? t.bed - .3 : t.bed + .05 + 1.25 * s; });
    crops.forEach((c, i) => { dummy.position.set(c.x, c.y, c.z); dummy.rotation.set(0, c.ry, 0); dummy.scale.set(1, .18 + .82 * s, 1); dummy.updateMatrix(); cropMesh.setMatrixAt(i, dummy.matrix); });
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

  function placePins() {
    for (let i = 0; i < spots.length; i++) {
      const s = spots[i], el = pins[i];
      v3.copy(s.anchor).project(camera);
      const x = (v3.x * .5 + .5) * W.w, y = (-v3.y * .5 + .5) * W.h;
      const off = v3.z > 1 || x < -60 || x > W.w + 60 || y < -20 || y > W.h + 80;
      el.classList.toggle('off', off);
      if (off) continue;
      const d = camera.position.distanceTo(s.anchor), sc = THREE.MathUtils.clamp(95 / d, .7, 1.12);
      el.style.transform = `translate3d(${x.toFixed(1)}px,${y.toFixed(1)}px,0) translate(-50%,-100%) scale(${sc.toFixed(3)})`;
      el.style.zIndex = String(2000 - Math.round(d) + (i === cur ? 500 : 0));
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
      const a = rainGeo.attributes.position.array;
      for (let i = 0; i < DROPS; i++) { const o = i * 6; let y = a[o + 1] - 70 * dt; if (y < 0) y += 100; a[o + 1] = y; a[o + 4] = y + 1.8; a[o] += 6 * dt; if (a[o] > 130) a[o] -= 260; a[o + 3] = a[o] + .25; }
      rainGeo.attributes.position.needsUpdate = true;
    }

    if (!REDUCE) {
      for (let i = 0; i < seaPos.count; i++) { const x = seaPos.getX(i), z = seaPos.getZ(i); seaPos.setY(i, Math.sin(x * .09 + t * 1.1) * .22 + Math.cos(z * .07 + t * .8) * .2); }
      seaPos.needsUpdate = true; seaGeo.computeVertexNormals();
      for (const c of clouds) { c.position.x += c.userData.v * dt; if (c.position.x > 220) c.position.x = -220; }
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
    placePins();
    requestAnimationFrame(loop);
  }

  // first frame, then intro: fly in, the monsoon arrives
  stage.classList.add('ready'); stage.classList.remove('nogl');
  requestAnimationFrame(loop);
  const target = DATA.findIndex(d => '#' + d.id === location.hash);
  if (REDUCE) { setSeason(1, true); if (target >= 0) open(target); }
  else {
    flyTo(HOME_POS, HOME_TGT, 3400);
    setTimeout(() => setSeason(1), 1900);
    setTimeout(() => { introDone = true; if (target >= 0) open(target); }, 3600);
  }

  addEventListener('keydown', e => {
    if (e.target.closest && e.target.closest('input,textarea')) return;
    if (e.key === 'Escape' && cur >= 0) { tour(false); close(); }
    else if (e.key === 'ArrowRight' && cur >= 0) { tour(false); open(cur + 1); }
    else if (e.key === 'ArrowLeft' && cur >= 0) { tour(false); open(cur - 1); }
  });
}
