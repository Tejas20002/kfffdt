#!/usr/bin/env python3
"""Generates the redesigned KFFFDT static site into ./new  (run: python3 build_new.py)."""
import os, html

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "new")
E = html.escape
PHONE1, PHONE2, MAIL = "98258 58919", "91065 82919", "kfffdt@gmail.com"
ADDR = "102, Kaushik Apartment, Bhanushali Nagar, Bhuj – Kutch, Gujarat 370001"

NAV = [("index.html", "Home"), ("about.html", "About"), ("projects.html", "Programs"),
       ("activities.html", "Impact"), ("gallery.html", "Gallery"), ("explore.html", "3D Explore"), ("updates.html", "Updates"), ("legal.html", "Legal"), ("contact.html", "Contact")]

PROGRAMS = {
 "water-conservation": dict(title="Water Conservation", img="g04", tag="Rain is rare in Kutch. We make every drop count.",
   intro="Kutch receives little rain, and most of it runs off. We build storage tanks, percolation tanks and check dams so that water stays in the village, and recharge groundwater.",
   bullets=["Roof Top Rain Water Harvesting", "Artificial Ground Water Recharging", "Kutch Jal Mandir Abhiyan – revival of traditional drinking water sources", "Farm Bunding, Farm Pond", "Land ploughing for moisture conservation", "Guidance for micro-irrigation systems for better use of natural resources"],
   table=(["", "Description", "Numbers", "Rs. in Lacs"], [["a","Construction of Storage Tank","141","509.47"],["b","Construction of Percolation Tank","48","131.90"],["c","Construction of Check Dams","16","195.58"],["d","Construction of Sub Surface Check Dams","8","12.19"],["e","Roof Top Rain Water Harvesting","9","14.63"],["f","Artificial Ground Water Recharging Tube Wells","19","19.20"]])),
 "kutch-jal-mandir-abhiyan": dict(title="Kutch Jal Mandir Abhiyan", img="g11", tag="Reviving traditional drinking water sources with the community.",
   intro="Kutch averages 312 mm of rain over just 13 rainy days, and about 70% of it flows to the sea. Jal Mandir Abhiyan revives old village storage tanks (talavs) for drinking water, for recharging water sources and for all flora and fauna.",
   bullets=["Village selection: need based", "People's participation: must", "Panchayat resolution: must", "Project funds an excavator for 100–150 hours depending on site conditions", "Village community provides tractors to carry the excavated material (people's contribution)", "Excavated material strengthens existing bunds and is used in agriculture", "Daily work is logged in a work book; payment is by bank transfer only", "A name plate with project details and the donor's name is fixed at each site"],
   table=(["No.", "Project profile 2012–2024", "Qty", "Unit"], [["1","Existing storage tanks (Jal Mandir) revived","332","Number"],["2","Water storage capacity increase","8835.93","Lac litre"],["3","Total project expenditure","525.32","Rs. in Lac"],["4","Project support","297.49","Rs. in Lac"],["5","People's contribution in form of tractors","227.83","Rs. in Lac"],["6","Cost per litre of rain water","0.059","Rs. in Lac"]]),
   table2=(["No.", "Implementing agency", "Role"], [["1","Kutch Fodder Fruit & Forest Development Trust","Overall implementation and monitoring"],["2","Kutch Nav Nirman Abhiyan","Support agency"],["3","Setu Abhiyan","Village level support"],["4","Gram Panchayat","Village level support"],["5","Village Committee","Implementing & monitoring"]]),
   table3=(["No.", "Funding group", "Foundation"], [["1","Aarti Industries, Mumbai","Aarti Foundation"],["2","Leshark Global LLP, Tirupur (Tamil Nadu)","Concern India Foundation, Mumbai"],["3","Agrocel Industries Private Limited, Bhuj","Agrocel, Bhuj"],["4","Kutchhi Jain Foundation, Mumbai","Foundation"],["5","Shri Gunvantbhai Shah, Mumbai","Individual"],["6","Mitsu Chem Plast Ltd, Mumbai","Mitsu Foundation"],["7","Kachchhi Oswal Jain living in North America","KOJAINA"],["8","Many individual donors from Kachchhi Jain Mahajan","KVO Jain Mahajan"]])),
 "agriculture-development": dict(title="Agriculture Development", img="g16", tag="Seeds, soil and fodder for rainfed farmers.",
   intro="Support for rainfed farmers through traditional seeds, chemical-free farming, soil and water testing, fodder security and grazing land development.",
   sections=[
     ("Anmol Beej Bank – largest traditional seed bank of Gujarat", ["Conservation and promotion of traditional seeds", "Distribution of fodder seeds to rainfed farmers for dry fodder security", "Support traditional seed grower farmers", "Encourage rainfed farmers to use traditional instead of hybrid seeds"]),
     ("Farm Bunding & Farm Pond", ["Farm bunding for in-situ moisture conservation and to prevent soil erosion", "Farm ponds to store rainwater for critical irrigation if rain is delayed"]),
     ("Bio Resource Centre – first of its kind in Gujarat", ["Promotion of chemical-free farming", "Better soil health through bacterial solutions and on-field support", "Integrated Pest Management for biological control of pests and insects"]),
     ("Soil & Water Testing", ["Lab at Krishi Sewa Kendra testing EC, TDS, pH of irrigation water and EC, pH, organic carbon of soil", "Macro and micro nutrient testing via GSFC and IFFCO laboratories", "Area-specific micro-nutrient consortia for better production"]),
     ("Bio Gas Plants & Composting of Agriculture Waste", ["Linkage with Government and CSR projects", "Demonstration of composting agricultural waste using various bacteria"]),
     ("Green Fodder Security", ["Distribution of Napier Hybrid Bajra cuttings to irrigated farmers for green fodder security at farm level"]),
     ("Grazing Land Development & Tree Plantation", ["Support for Gauchar (grazing) land development", "Tree plantation with the community and with the Indian Army, Bhuj", "Seed ball broadcasting"])]),
 "animal-health-care": dict(title="Animal Health Care", img="g13", tag="Healthy livestock, healthy families.",
   intro="Pashupalak Mitra animal health care centres serve pastoral communities, with a focus on preventing Brucella disease.",
   bullets=["Vaccination of female calves – cattle & buffaloes", "Milk and blood sample collection and testing – animal Brucella", "Human blood collection and testing – human Brucella", "Community-level awareness about Brucella", "Deworming, drenching and primary health care of small ruminants", "Primary health care and awareness during the Lumpy virus attack"],
   note="Partners: National Dairy Development Board, Government Animal Health Dept., Indian Immunological Laboratory (Hyderabad), Shri Krishna Medical College, Karamsad."),
 "natural-disaster-management": dict(title="Natural Disaster Management", img="g21", tag="Relief and rebuilding when disaster strikes.",
   intro="From the 2001 Kutch earthquake to COVID-19, the Trust has coordinated with disaster authorities to deliver relief and rebuild.",
   sections=[
     ("Kutch Earthquake – 2001", ["Distribution of tarpaulin sheets and relief materials", "Primary survey of damaged houses", "Coordination with Disaster Management Authority", "Temporary shelters for affected families", "134 permanent houses built and 24 repaired/retrofitted; primary school, community centre, drinking water scheme, 100% sanitation and solar street lights, with support of Castrol Oil India Limited"]),
     ("COVID-19", ["Awareness among village communities; posters at village level", "Primary health kits", "Oxygen concentrators at cluster level", "Ration kits for poor families"])]),
 "decentralized-drinking-water-supply-scheme-project": dict(title="Decentralized Drinking Water Supply", img="g22", tag="Community-managed drinking water and sanitation.",
   intro="Community Managed Drinking & Sanitation Programme under the WASMO project.",
   bullets=["Roof top rain water harvesting at school level", "Awareness on village-level cleanliness and total sanitation for Nirmal Gram – Swachh Bharat Mission"]),
 "primary-education-for-unreached-community": dict(title="Primary Education for the Unreached", img="g20", tag="Van Shala – schools where none existed.",
   intro="Education: reaching the unreached. Van Shala (forest school) at Kalara Wandh, Lakhpat – Kutch."),
}
ORDER = ["water-conservation", "kutch-jal-mandir-abhiyan", "agriculture-development", "animal-health-care", "decentralized-drinking-water-supply-scheme-project", "natural-disaster-management", "primary-education-for-unreached-community"]

ACT = [
 ("Water conservation", "705", "1,421.67", [("Storage tanks / check dams","141 nos","509.47"),("Percolation tanks","48 nos","131.90"),("Underground check dams","8 nos","12.19"),("Kutch Jal Mandir Abhiyan","332 nos","525.32"),("Raising capacity of minor irrigation scheme","1 no","8.45"),("Renovation of storage tanks","6 nos","19.56"),("Cement concrete check dams","16 nos","195.58"),("Recharge tube wells","19 nos","19.20"),("Farm ponds","134 nos","33.50")]),
 ("Soil & moisture conservation", "", "92.44", [("Contour & staggered trenches","603,739 RMt","29.25"),("Loose boulder check dams","20,788 CMt","21.81"),("Farm bunding","204,150 RMt","41.38")]),
 ("WASMO – village water supply schemes", "", "620.82", [("Villages","37","601.25"),("Drinking water wells","7 nos","4.94"),("Roof top rain water harvesting","9 nos","14.63")]),
 ("Reconstruction of earthquake-affected villages", "", "189.65", [("Temporary shelters","174 nos","13.05"),("Permanent shelters & other infrastructure","1 village","164.35"),("Model housing project","3 nos","12.25")]),
 ("Agriculture & fodder development", "", "320.43", [("Promotion of horticulture","21,725 plants","4.30"),("Fodder security project","1,090 farmers","21.80"),("Fodder bank","1 no","1.63"),("Gauchar land development","170 acres","37.80"),("Agriculture extension project","1,400 farmers","65.85"),("Promotion of NB21 as green fodder","1,421,800 cuttings","21.33"),("Anmol Deshi Beej Bank","2 projects","65.00"),("Tree plantation","8 projects","26.25"),("Bio Resource Centre","1,870 farmers","34.50"),("Samriddhi Krishi Seva Kendra","1 centre","24.50"),("Fodder storage shed","278 farmers","17.47")]),
]
FUNDERS = ["Ministry of Rural Development, GoI", "Ministry of Wasteland Development, GoI", "Ministry of Water Resources, GoG", "Castrol India", "UNDP – ABHIYAN", "WASMO", "Aarti Foundation", "Concern India Foundation", "Adani Foundation", "TATA Power CSR", "NDDB", "Agrocel"]
GALLERY = ["g%02d" % i for i in range(1, 20)]

CSS = """
:root{--ink:#1d2a1f;--muted:#5d6a5e;--green:#2e5b3b;--green2:#3f7a4f;--ochre:#c98a2b;--clay:#a4492b;--sand:#f7f1e3;--sand2:#efe5cf;--card:#fffdf8;--line:#e3d9c0;--r:18px}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font:17px/1.65 Inter,system-ui,sans-serif;color:var(--ink);background:var(--sand)}
h1,h2,h3{font-family:Fraunces,Georgia,serif;line-height:1.15;margin:0 0 .5em;font-weight:700}
h1{font-size:clamp(2.2rem,5.5vw,4rem)}h2{font-size:clamp(1.7rem,3.4vw,2.5rem)}h3{font-size:1.25rem}
a{color:var(--green);text-decoration:none}img{max-width:100%;display:block}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}
header{position:sticky;top:0;z-index:50;background:rgba(247,241,227,.92);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.bar{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:10px 20px;max-width:1180px;margin:0 auto}
.bar img{height:46px;width:auto}
nav{display:flex;gap:4px;flex-wrap:wrap}nav a{padding:8px 13px;border-radius:99px;color:var(--ink);font-weight:500;font-size:.95rem}
nav a:hover,nav a.on{background:var(--green);color:#fff}
.burger{display:none;background:none;border:1px solid var(--line);border-radius:10px;padding:8px 12px;font-size:1.1rem}
.btn{display:inline-block;background:var(--ochre);color:#231a05;font-weight:600;padding:13px 26px;border-radius:99px;transition:.2s}
.btn:hover{transform:translateY(-2px);background:#dc9a37}.btn.alt{background:transparent;border:2px solid #fff;color:#fff}
.hero{position:relative;min-height:84vh;display:flex;align-items:flex-end;color:#fff;background:#243;overflow:hidden}
.hero img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.hero:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,25,14,.15),rgba(10,25,14,.82))}
.hero .wrap{position:relative;z-index:2;padding-bottom:70px}.hero p{max-width:640px;font-size:1.2rem;opacity:.95}
.kick{text-transform:uppercase;letter-spacing:.16em;font-size:.78rem;font-weight:600;color:var(--ochre)}
.hero .kick{color:#f0c46f}
section{padding:80px 0}.alt-bg{background:var(--sand2)}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:-50px;position:relative;z-index:5}
.stat{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:26px;box-shadow:0 14px 30px -18px rgba(0,0,0,.35)}
.stat b{display:block;font:700 2.3rem Fraunces,serif;color:var(--green)}.stat span{color:var(--muted);font-size:.95rem}
.grid{display:grid;gap:22px}.g3{grid-template-columns:repeat(3,1fr)}.g2{grid-template-columns:1fr 1fr}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;transition:.25s;display:flex;flex-direction:column}
.card:hover{transform:translateY(-5px);box-shadow:0 18px 34px -20px rgba(0,0,0,.4)}
.card img{aspect-ratio:16/10;object-fit:cover;width:100%}.card div{padding:20px 22px 24px}.card p{color:var(--muted);margin:.2em 0 .8em}
.more{font-weight:600}
.split{display:grid;grid-template-columns:1fr 1fr;gap:50px;align-items:center}.split img{border-radius:var(--r)}
.mv{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:24px}
.mv div{background:var(--green);color:#fff;border-radius:var(--r);padding:26px}.mv div:last-child{background:var(--clay)}.mv h3{color:#f6dca0}
.page-hero{background:var(--green);color:#fff;padding:70px 0 60px;position:relative;overflow:hidden}
.page-hero.img{padding:110px 0 70px}.page-hero.img img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.35}
.page-hero .wrap{position:relative}.page-hero p{max-width:680px;font-size:1.15rem;opacity:.92}
.list{list-style:none;padding:0;margin:0;display:grid;gap:10px}
.list li{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:13px 16px 13px 46px;position:relative}
.list li:before{content:"";position:absolute;left:16px;top:20px;width:14px;height:14px;border-radius:50%;background:var(--ochre)}
.tw{overflow-x:auto;border:1px solid var(--line);border-radius:var(--r);background:var(--card);margin:22px 0}
table{border-collapse:collapse;width:100%;font-size:.95rem}th,td{padding:12px 16px;text-align:left;border-bottom:1px solid var(--line)}
th{background:var(--sand2);font-weight:600;white-space:nowrap}tr:last-child td{border-bottom:0}td.n,th.n{text-align:right;white-space:nowrap}
tr.sub td{background:#f3ead3;font-weight:700}
.gal{columns:3;column-gap:14px}.gal a{display:block;margin-bottom:14px;border-radius:14px;overflow:hidden}.gal img{width:100%;transition:.4s}.gal a:hover img{transform:scale(1.05)}
.lb{position:fixed;inset:0;background:rgba(0,0,0,.92);display:none;align-items:center;justify-content:center;z-index:99;cursor:zoom-out}.lb.on{display:flex}.lb img{max-width:94vw;max-height:92vh;border-radius:8px}
.chips{display:flex;flex-wrap:wrap;gap:10px}.chips span{background:var(--card);border:1px solid var(--line);padding:9px 16px;border-radius:99px;font-size:.92rem}
.cta{background:var(--green);color:#fff;border-radius:28px;padding:56px;text-align:center}.cta p{max-width:560px;margin:0 auto 24px}
form{display:grid;gap:14px}input,textarea{font:inherit;padding:14px 16px;border:1px solid var(--line);border-radius:12px;background:#fff;width:100%}
.info{display:grid;gap:14px}.info div{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 20px}.info b{display:block;color:var(--green)}
.ft{position:relative;background:#16241a;color:#c9d4c9;padding:30px 0 0;margin-top:70px;font-size:.96rem}
.ft>.wave{top:-69px;bottom:auto}
.ft a{color:#e9d9a8}.ft h4{color:#fff;margin:0 0 14px;font:700 1.15rem Fraunces,serif}
.ft-cta{position:relative;overflow:hidden;display:flex;align-items:center;justify-content:space-between;gap:28px;flex-wrap:wrap;padding:44px 48px;border-radius:28px;background:linear-gradient(120deg,#2e5b3b,#3f7a4f 60%,#4f8a5c);box-shadow:0 30px 60px -30px rgba(0,0,0,.7);margin-bottom:60px}
.ft-cta>*{position:relative;z-index:1}.ft-cta h3{color:#fff;font:700 clamp(1.5rem,3vw,2.2rem)/1.2 Fraunces,serif;margin:.25em 0 .3em;max-width:620px}.ft-cta p{margin:0;color:rgba(255,255,255,.82)}
.ft-cta .kick{color:#f0c46f}.ft-cta-b{display:flex;gap:12px;flex-wrap:wrap}.ft-cta-b .btn{display:inline-flex;align-items:center;gap:8px}.ft-cta-b svg{width:17px;height:17px}
.ft-rip{position:absolute;right:-60px;top:50%;width:0;height:0;z-index:0}.ft-rip i{position:absolute;left:-160px;top:-160px;width:320px;height:320px;border-radius:50%;border:2px solid rgba(240,196,111,.35);opacity:0;animation:rp2 6s ease-out infinite}
.ft-rip i:nth-child(2){animation-delay:2s}.ft-rip i:nth-child(3){animation-delay:4s}
.ft-grid{display:grid;grid-template-columns:1.5fr 1.1fr .9fr 1.4fr;gap:44px}
.ft-logo{display:inline-block;background:#fff;padding:10px 14px;border-radius:14px;margin-bottom:16px}.ft-logo img{height:50px;display:block}
.ft-brand p{margin:0 0 18px;max-width:330px}
.ft-badges{display:flex;flex-wrap:wrap;gap:8px}.ft-badges a{font-size:.78rem;font-weight:700;letter-spacing:.06em;padding:6px 12px;border-radius:99px;border:1px solid rgba(240,196,111,.4);color:#f0c46f;transition:.2s}.ft-badges a:hover{background:#f0c46f;color:#16241a}
.ft-links{list-style:none;margin:0;padding:0;display:grid;gap:9px}
.ft-links a{color:#c9d4c9;background:linear-gradient(#f0c46f,#f0c46f) 0 100%/0 1px no-repeat;padding-bottom:2px;transition:color .2s,background-size .3s}.ft-links a:hover{color:#fff;background-size:100% 1px}
.ft-contact{list-style:none;margin:0;padding:0;display:grid;gap:14px}.ft-contact li{display:flex;gap:12px;align-items:flex-start}
.ft-contact svg{width:18px;height:18px;flex:none;margin-top:3px;color:#f0c46f}
.ft-bottom{margin-top:52px;padding:20px 0 24px;border-top:1px solid #2c3d30;display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap;font-size:.86rem}
.ft-bl{display:flex;gap:18px;align-items:center;flex-wrap:wrap}
.totop{display:inline-flex;align-items:center;gap:8px;font:600 .86rem Inter,sans-serif;color:#16241a;background:#f0c46f;border:0;border-radius:99px;padding:8px 16px;cursor:pointer;transition:.2s}
.totop svg{width:12px;height:15px;transition:transform .3s}.totop:hover{background:#fff}.totop:hover svg{transform:translateY(-4px)}
@media(max-width:900px){.ft-grid{grid-template-columns:1fr 1fr;gap:34px}.ft-brand{grid-column:1/-1}.ft-cta{padding:32px 24px}}
@media(max-width:560px){.ft-grid{grid-template-columns:1fr}.ft-bottom{flex-direction:column;align-items:flex-start}}
.reveal{opacity:0;transform:translateY(22px);transition:.7s}.reveal.in{opacity:1;transform:none}
/* --- motion: water / rain / growth concepts --- */
@keyframes kb{from{transform:scale(1)}to{transform:scale(1.13) translate(-1.5%,-1%)}}
.hero img{animation:kb 26s ease-in-out infinite alternate}
canvas.rain{position:absolute;inset:0;width:100%;height:100%;z-index:2;pointer-events:none}
.hero h1 span{display:inline-block;opacity:0;transform:translateY(30px)}.slide.on h1 span{animation:up .9s cubic-bezier(.2,.8,.2,1) forwards}
@keyframes up{to{opacity:1;transform:none}}
.hero .kick,.hero p,.hero .btn{opacity:0}.slide.on .kick,.slide.on p,.slide.on .btn{animation:up 1s .9s forwards}
.wave{position:absolute;left:0;right:0;bottom:-1px;height:70px;z-index:3;overflow:hidden;line-height:0}
.wave svg{width:200%;height:100%;animation:wv 14s linear infinite}.wave svg+svg{position:absolute;left:0;top:0;opacity:.45;animation-duration:22s;animation-direction:reverse}
@keyframes wv{to{transform:translateX(-50%)}}
.page-hero .wave{height:44px}
.sub-h{max-width:640px;margin:0 auto 34px;text-align:center}.sub-h p{color:var(--muted)}
.rain-box{display:grid;grid-template-columns:1.1fr .9fr;gap:50px;align-items:center}
.dots{display:grid;grid-template-columns:repeat(10,1fr);gap:9px;max-width:400px;margin:0 auto}
.dots i{aspect-ratio:1;border-radius:50% 50% 50% 0;transform:rotate(-45deg);background:#5fa8d3;display:block}
.dots.play i.sea{animation:drain 1.5s ease-in var(--d) forwards}
.dots.play i.keep{animation:keepit 1s 2.5s forwards}
.legend{display:flex;gap:22px;flex-wrap:wrap;margin-top:22px;font-size:.95rem}.legend b{display:inline-block;width:12px;height:12px;border-radius:50%;margin-right:7px}
.tank{width:100%;max-width:240px;margin:0 auto;display:block}
.tank .water{transform:translateY(140px);transition:transform 3.4s cubic-bezier(.25,.8,.3,1) .4s}.in .tank .water{transform:translateY(0)}
.tank .wv{animation:wv2 5s linear infinite}@keyframes wv2{to{transform:translateX(-80px)}}
.tl{position:relative;max-width:860px;margin:0 auto;padding:10px 0}
.tl:before,.tl .fill{content:"";position:absolute;left:50%;top:0;width:4px;margin-left:-2px;border-radius:4px;background:var(--line)}.tl:before{bottom:0}
.tl .fill{background:linear-gradient(var(--green2),var(--ochre));height:calc(var(--p,0)*100%);z-index:1}
.ev{position:relative;width:50%;padding:0 44px 46px 0;text-align:right}.ev:nth-child(even){margin-left:50%;padding:0 0 46px 44px;text-align:left}
.ev:after{content:"";position:absolute;right:-9px;top:6px;width:18px;height:18px;border-radius:50%;background:var(--card);border:4px solid var(--ochre);z-index:2;transition:.5s}
.ev:nth-child(even):after{right:auto;left:-9px}.ev.in:after{background:var(--green);border-color:var(--green);box-shadow:0 0 0 8px rgba(63,122,79,.18)}
.ev b{font:700 1.7rem Fraunces,serif;color:var(--clay);display:block}.ev p{margin:.2em 0 0;color:var(--muted)}
.sprout{width:46px;height:46px;vertical-align:middle;margin-right:8px}.sprout path{stroke-dasharray:60;stroke-dashoffset:60}.in .sprout path,.in.sprout path{animation:dr 1.8s .3s forwards}@keyframes dr{to{stroke-dashoffset:0}}
.leaf-f{position:absolute;top:-30px;width:22px;height:22px;opacity:.0;background:var(--green2);border-radius:0 100% 0 100%;animation:fall linear infinite}
@keyframes fall{0%{transform:translate(0,0) rotate(0);opacity:0}10%{opacity:.5}100%{transform:translate(80px,520px) rotate(300deg);opacity:0}}
.cta{position:relative;overflow:hidden}.cta>*{position:relative;z-index:1}
.map{border:1px solid var(--line);border-radius:var(--r);overflow:hidden;background:var(--card)}.map iframe{width:100%;height:420px;border:0;display:block}
.map .tabs{display:flex;gap:8px;padding:12px;flex-wrap:wrap;border-bottom:1px solid var(--line)}
.map .tabs button{font:inherit;font-size:.92rem;padding:8px 16px;border-radius:99px;border:1px solid var(--line);background:var(--sand);cursor:pointer}.map .tabs button.on{background:var(--green);color:#fff;border-color:var(--green)}
.req{color:var(--clay)}.fr{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:900px){.rain-box,.fr{grid-template-columns:1fr}.tl:before,.tl .fill{left:14px}.ev,.ev:nth-child(even){width:100%;margin-left:0;padding:0 0 38px 44px;text-align:left}.ev:after,.ev:nth-child(even):after{left:5px;right:auto}.hero{min-height:78vh}}
/* --- hero slider: 5 slides, each with its own effect --- */
.hero.slider:after{display:none}
.slide{position:absolute;inset:0;display:flex;align-items:flex-end;opacity:0;visibility:hidden;transition:opacity 1.1s,visibility 0s 1.1s}
.slide.on{opacity:1;visibility:visible;transition:opacity 1.1s}
.slide:before{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,rgba(10,25,14,.15),rgba(10,25,14,.82))}
.slide .wrap{z-index:3;width:100%}
.fx{position:absolute;pointer-events:none;z-index:2}
/* 2 · tank water rising */
.fx-rise{left:0;right:0;bottom:0;height:46%;transform:translateY(100%);background:linear-gradient(180deg,rgba(95,168,211,.5),rgba(26,86,135,.78));transition:transform 6s cubic-bezier(.2,.7,.2,1) .5s}
.slide.on .fx-rise{transform:none}
.fx-rise svg{position:absolute;left:0;top:-39px;width:200%;height:40px;animation:wv 9s linear infinite}.fx-rise svg+svg{top:-30px;opacity:.5;animation-duration:14s;animation-direction:reverse}
/* 3 · seeds and leaves falling */
.fx-leaves{inset:0;overflow:hidden}
.lf{position:absolute;top:-40px;left:var(--x);width:var(--s);height:var(--s);background:var(--c);border-radius:0 100% 0 100%;opacity:0;animation:lfall var(--t) linear infinite;animation-delay:var(--d);animation-play-state:paused}
.slide.on .lf{animation-play-state:running}
@keyframes lfall{0%{transform:translate(0,0) rotate(0);opacity:0}8%{opacity:.85}30%{transform:translate(50px,30vh) rotate(140deg)}60%{transform:translate(-30px,60vh) rotate(300deg)}100%{transform:translate(70px,105vh) rotate(520deg);opacity:.2}}
/* 4 · grass swaying */
.grass{left:0;right:0;bottom:0;height:190px;overflow:hidden}
.grass i{position:absolute;bottom:0;left:var(--x);width:9px;height:var(--h);background:linear-gradient(0deg,#2e5b3b,var(--g));clip-path:polygon(50% 0,100% 100%,0 100%);transform-origin:50% 100%;animation:sway var(--t) ease-in-out infinite alternate;animation-delay:var(--d);animation-play-state:paused}
.slide.on .grass i{animation-play-state:running}
@keyframes sway{from{transform:rotate(-7deg)}to{transform:rotate(8deg)}}
/* 5 · sun rays + glow */
.fx-sun{right:-28vw;top:-48vw;width:92vw;height:92vw;border-radius:50%;background:repeating-conic-gradient(rgba(255,214,128,.32) 0 5deg,transparent 5deg 15deg);-webkit-mask-image:radial-gradient(circle,#000 8%,transparent 68%);mask-image:radial-gradient(circle,#000 8%,transparent 68%);animation:spin 80s linear infinite}
.fx-glow{right:-12vw;top:-12vw;width:44vw;height:44vw;border-radius:50%;background:radial-gradient(circle,rgba(255,224,150,.6),transparent 66%);animation:pulse 5s ease-in-out infinite alternate}
@keyframes spin{to{transform:rotate(360deg)}}@keyframes pulse{from{transform:scale(.88);opacity:.65}to{transform:scale(1.15);opacity:1}}
/* controls */
.hctl{position:absolute;z-index:6;right:max(20px,calc((100% - 1180px)/2 + 20px));bottom:98px;display:flex;align-items:center;gap:12px}
.hctl button{border:1px solid rgba(255,255,255,.45);background:rgba(255,255,255,.16);color:#fff;backdrop-filter:blur(6px);width:44px;height:44px;border-radius:50%;font-size:1.4rem;line-height:1;cursor:pointer;transition:.2s}.hctl button:hover{background:#fff;color:var(--green)}
.hctl .dts{display:flex;gap:7px}.hctl .dts button{width:11px;height:11px;padding:0;background:rgba(255,255,255,.4);border-color:transparent;transition:width .35s,background .35s;border-radius:99px}.hctl .dts button.on{width:34px;background:var(--ochre)}
@media(max-width:900px){.hctl{right:16px;bottom:86px}.hctl button:not(.dts button){width:38px;height:38px}.grass{height:140px}}
/* --- rain section: options, end states, 365-day strip --- */
@keyframes drain{50%{transform:translateY(22%) rotate(-45deg) scale(.8)}100%{transform:rotate(-45deg);opacity:.15}}
@keyframes keepit{to{background:var(--green2);transform:scale(1.18) rotate(-45deg)}}
.opt{display:flex;justify-content:center;gap:8px;margin-bottom:34px;flex-wrap:wrap}
.opt button{font:inherit;font-weight:600;padding:10px 24px;border-radius:99px;border:1px solid var(--line);background:var(--card);cursor:pointer;transition:.2s}.opt button:hover{border-color:var(--green)}.opt button.on{background:var(--green);color:#fff;border-color:var(--green)}
.views{display:grid}.view{grid-area:1/1;align-self:center;visibility:hidden;opacity:0;transform:translateY(10px);transition:opacity .45s,transform .45s,visibility 0s .45s}.view.on{visibility:visible;opacity:1;transform:none;transition:opacity .45s,transform .45s}
.bigs{display:flex;gap:34px;justify-content:center;margin-top:22px}.bigs b{display:block;font:700 2.8rem/1 Fraunces,serif;color:#2f86c0}.bigs .g b{color:var(--green)}.bigs span{font-size:.92rem;color:var(--muted)}
.legend{align-items:center;justify-content:center}.replay{margin-left:auto;font:inherit;font-size:.9rem;font-weight:600;background:none;border:1px solid var(--line);border-radius:99px;padding:6px 14px;cursor:pointer;color:var(--green)}.replay:hover{background:var(--green);color:#fff}
.yr{display:grid;grid-template-columns:auto 1fr;gap:5px 12px;align-items:center;max-width:540px;margin:0 auto}.yr .m{font-size:.78rem;font-weight:600;color:var(--muted);width:2.4em}.yr .mo{display:grid;grid-template-columns:repeat(31,1fr);gap:3px}.yr i{aspect-ratio:1;border-radius:3px;background:#dcd0b3;display:block}
.yr.play i.r{animation:lite .9s var(--d) both}@keyframes lite{0%{transform:scale(1)}50%{transform:scale(2.4);background:#9fd3ee;box-shadow:0 0 0 4px rgba(95,168,211,.3)}100%{transform:scale(1.3);background:#2f86c0}}
.tankcol{text-align:center}.tankcol .tank{max-width:300px}.tbig{font:700 2.6rem/1.1 Fraunces,serif;color:var(--green);margin-top:10px}.tbig small{font:600 1rem Inter,sans-serif;color:var(--muted)}
.btn.ghost{background:transparent;border:2px solid var(--green);color:var(--green)}.btn.ghost:hover{background:var(--green);color:#fff}
@media(prefers-reduced-motion:reduce){.dots i.sea{opacity:.15}.dots i.keep{background:var(--green2)}.yr i.r{background:#2f86c0}}
@media(max-width:900px){.bigs{gap:22px}.bigs b{font-size:2.2rem}}
/* --- home: fodder, fruit & forest --- */
.fff .opt button{display:inline-flex;align-items:center;gap:8px}.fff .opt svg{width:18px;height:18px}
.fff .view{display:grid;grid-template-columns:1.05fr .95fr;gap:48px;align-items:center}
.scene{border-radius:28px;overflow:hidden;border:1px solid var(--line);background:#fbf7ec;box-shadow:0 34px 60px -40px rgba(30,50,30,.55)}
.sc{display:block;width:100%;height:auto}
.sc .bl{transform-box:fill-box;transform-origin:50% 100%;animation:fsway 2.8s ease-in-out var(--s) infinite alternate}
.sc .gr,.sc .gw,.sc .pp,.sc .cn{transform-box:fill-box;transform-origin:50% 100%}.sc .fp,.sc .sun{transform-box:fill-box;transform-origin:50% 50%}
.sc .sun{animation:fglow 4s ease-in-out infinite alternate}.sc .cl{animation:fdrift 18s ease-in-out infinite alternate}
.sc .bd path{fill:none;stroke:#2e5b3b;stroke-width:2;stroke-linecap:round}
.armed .sc .gr{transform:scaleY(0)}.armed .sc .gw,.armed .sc .pp,.armed .sc .fp{transform:scale(0)}.armed .sc .cn{transform:scale(.25)}.armed .sc .sd,.armed .sc .fd,.armed .sc .bd{opacity:0}
.fff .play .gr{animation:fgrow .9s cubic-bezier(.2,.8,.2,1.2) var(--d) both}
.fff .play .gw,.fff .play .pp,.fff .play .fp{animation:fpop .7s cubic-bezier(.2,.8,.2,1.3) var(--d) both}
.fff .play .cn{animation:fcan 1.2s cubic-bezier(.2,.8,.2,1.1) .2s both}
.fff .play .sd{animation:fseed 1s ease-in var(--d) both}.fff .play .fd{animation:ffall .9s cubic-bezier(.5,0,.9,.5) 3.3s both}
.fff .play .bd{opacity:1;animation:ffly 15s linear 2.6s infinite both}
.sc .gnd{transition:fill 2.6s .5s}.fff:not(.armed) .gnd,.fff .play .gnd{fill:var(--g)}
@keyframes fgrow{0%{transform:scaleY(0)}70%{transform:scaleY(1.1)}100%{transform:scaleY(1)}}
@keyframes fpop{0%{transform:scale(0)}70%{transform:scale(1.15)}100%{transform:scale(1)}}
@keyframes fcan{from{transform:scale(.25)}to{transform:scale(1)}}
@keyframes fsway{from{transform:rotate(-5deg)}to{transform:rotate(5deg)}}
@keyframes fglow{to{transform:scale(1.12)}}@keyframes fdrift{to{transform:translateX(46px)}}
@keyframes fseed{0%{transform:translateY(-170px);opacity:0}12%{opacity:1}80%{transform:none;opacity:1}100%{transform:none;opacity:0}}
@keyframes ffall{0%{transform:none;opacity:0}8%{opacity:1}100%{transform:translate(68px,74px);opacity:1}}
@keyframes ffly{from{transform:translateX(-60px)}to{transform:translateX(470px)}}
.finfo .ftag{font-weight:700;font-size:.8rem;letter-spacing:.14em;text-transform:uppercase;color:var(--ochre)}
.finfo h3{font:700 2.1rem/1.15 Fraunces,serif;margin:.25em 0 .45em;color:var(--ink)}.finfo p{color:var(--muted);margin:0}
.fbig{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin:20px 0 4px}.fbig b{font:700 3.3rem/1 Fraunces,serif;color:var(--green)}.fbig span{font-weight:600;color:var(--muted)}
.fmini{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:16px 0 24px}
.fmini div{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:14px 14px 12px;transition:transform .3s,border-color .3s}.fmini div:hover{transform:translateY(-4px);border-color:var(--ochre)}
.fmini b{display:block;font:700 1.55rem/1.1 Fraunces,serif;color:var(--ochre)}.fmini b.t{font-size:1.2rem;line-height:1.3}.fmini span{display:block;font-size:.84rem;line-height:1.35;color:var(--muted);margin-top:4px}
.fact{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
@media(max-width:900px){.fff .view{grid-template-columns:1fr;gap:26px}.finfo h3{font-size:1.7rem}.fbig b{font-size:2.6rem}}
@media(max-width:520px){.fmini{grid-template-columns:1fr 1fr}.fmini div:last-child{grid-column:1/-1}}
/* --- 3D explore: nav item + home teaser --- */
nav a[href="explore.html"]{box-shadow:inset 0 0 0 1.5px var(--ochre)}
@media(min-width:901px) and (max-width:1120px){nav a{padding:8px 9px;font-size:.9rem}.bar img{height:40px}}
.xteaser{background:radial-gradient(120% 140% at 85% 15%,#3f7a4f 0%,#1f3d29 55%,#16241a 100%);color:#e9efe6;overflow:hidden}
.xteaser .kick{color:#f0c46f}.xteaser h2{color:#fff}.xteaser p{color:#c9d4c9}.xteaser .split{align-items:center}
.xt-img{display:block;border-radius:28px;overflow:hidden;border:1px solid rgba(255,255,255,.25);box-shadow:0 40px 80px -40px rgba(0,0,0,.75);transform:perspective(1200px) rotateY(-9deg) rotateX(3deg);transition:transform .7s cubic-bezier(.2,.8,.2,1)}
.xt-img:hover{transform:perspective(1200px) rotateY(0) rotateX(0) translateY(-4px)}.xt-img img{display:block;width:100%;aspect-ratio:16/10;object-fit:cover}
.xt-tags{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 26px}.xt-tags span{padding:7px 13px;border-radius:99px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.18);font-size:.85rem}
@media(prefers-reduced-motion:reduce){.xt-img{transform:none}}
/* --- contact page: photo + floating form --- */
.cx{position:relative;min-height:calc(100vh - 67px);display:flex;flex-direction:column;align-items:center;justify-content:center;padding:64px 20px 110px;overflow:hidden;color:#fff}
.cx>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;animation:kb 30s ease-in-out infinite alternate}
.cx:before{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,rgba(10,25,14,.5),rgba(10,25,14,.82))}
.cx>*:not(img){position:relative;z-index:2}.cx>.wave{position:absolute;z-index:3}
.cx-intro{text-align:center;margin-bottom:26px;max-width:620px;animation:cardin .9s cubic-bezier(.2,.8,.2,1) both}.cx-intro h1{margin:.1em 0 .2em}.cx-intro p{opacity:.9;margin:0;font-size:1.1rem}
.cx-card{width:100%;max-width:600px;background:rgba(255,253,248,.97);color:var(--ink);border-radius:28px;padding:34px 34px 28px;box-shadow:0 40px 80px -30px rgba(0,0,0,.75);position:relative;overflow:hidden;animation:cardin 1s cubic-bezier(.2,.8,.2,1) .2s both}
@keyframes cardin{from{opacity:0;transform:translateY(50px) scale(.96)}}
.cx-card h2{font-size:1.6rem;margin:0 0 18px}
.cx-stack{display:grid}.cx-stack>*{grid-area:1/1}
.cx-form{display:block;transition:opacity .4s,filter .4s,visibility .4s}
.fl{position:relative;margin-bottom:4px}
.fl input,.fl textarea{width:100%;font:inherit;padding:24px 46px 8px 16px;border:1.5px solid var(--line);border-radius:14px;background:#fff;transition:border-color .2s,box-shadow .2s;resize:vertical}
.fl label{position:absolute;left:17px;top:16px;color:var(--muted);pointer-events:none;transition:transform .2s,color .2s;transform-origin:left top}
.fl input:focus,.fl textarea:focus{outline:none;border-color:var(--green);box-shadow:0 0 0 4px rgba(46,91,59,.12)}
.fl input:focus+label,.fl input:not(:placeholder-shown)+label,.fl textarea:focus+label,.fl textarea:not(:placeholder-shown)+label{transform:translateY(-10px) scale(.76);color:var(--green);font-weight:600}
.fl .okmark{position:absolute;right:14px;top:18px;width:20px;height:20px;border-radius:50%;background:var(--green2);opacity:0;transform:scale(.3);transition:.25s cubic-bezier(.2,.8,.2,1.4)}
.fl .okmark:after{content:"";position:absolute;left:7px;top:3.5px;width:5px;height:9px;border:solid #fff;border-width:0 2px 2px 0;transform:rotate(45deg)}
.fl.ok .okmark{opacity:1;transform:scale(1)}
.fl.bad input,.fl.bad textarea{border-color:var(--clay);box-shadow:0 0 0 4px rgba(164,73,43,.1)}.fl.bad label{color:var(--clay)!important}
.fl .err{display:block;min-height:1.25em;padding:3px 4px 0;font-size:.8rem;color:var(--clay)}
.cx-card .fr{gap:12px}.send{border:0;cursor:pointer;width:100%;margin-top:6px;font-size:1.02rem;padding:15px}
@keyframes shake{20%,60%{transform:translateX(-9px)}40%,80%{transform:translateX(9px)}}.cx-card.shake{animation:shake .45s}
.splash{position:absolute;inset:0;z-index:3;display:flex;align-items:center;justify-content:center;pointer-events:none;opacity:0;transition:opacity .3s}
.sending .splash{opacity:1}.sent .splash{opacity:0}
.splash svg{width:46px;opacity:0}.sending .splash svg{animation:dropfall .65s cubic-bezier(.55,0,1,.45) forwards}
@keyframes dropfall{0%{opacity:1;transform:translateY(-190px)}88%{opacity:1}100%{opacity:0;transform:translateY(0) scaleY(.6)}}
.splash i{position:absolute;width:170px;height:60px;border:2px solid #5fa8d3;border-radius:50%;opacity:0}
.sending .splash i{animation:rp3 1.2s ease-out .6s forwards}.sending .splash i:nth-of-type(2){animation-delay:.8s}.sending .splash i:nth-of-type(3){animation-delay:1s}
@keyframes rp3{from{transform:scale(.1);opacity:1}to{transform:scale(1.7);opacity:0}}
.sending .cx-form{opacity:.1;filter:blur(3px)}.sent .cx-form{opacity:0;visibility:hidden}
.cx-done{align-self:center;text-align:center;opacity:0;visibility:hidden;transition:opacity .5s .1s,visibility .5s}.sent .cx-done{opacity:1;visibility:visible}
.cx-done svg{width:88px;height:88px;display:block;margin:0 auto 14px}
.cx-done circle,.cx-done path{fill:none;stroke:var(--green2);stroke-width:5;stroke-linecap:round;stroke-linejoin:round}
.cx-done circle{stroke-dasharray:252;stroke-dashoffset:252}.cx-done path{stroke-dasharray:60;stroke-dashoffset:60}
.sent .cx-done circle{animation:dr2 .8s .25s forwards}.sent .cx-done path{animation:dr2 .5s 1s forwards}@keyframes dr2{to{stroke-dashoffset:0}}
.cx-done p{color:var(--muted);margin:.4em 0}.cx-done .small{font-size:.9rem}.cx-done .again{margin-top:14px;cursor:pointer;font:inherit;font-weight:600}
.cx-chips{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-top:26px;max-width:760px;animation:cardin 1s cubic-bezier(.2,.8,.2,1) .45s both}
.cx-chips a,.cx-chips span{display:inline-flex;align-items:center;gap:8px;padding:10px 16px;border-radius:99px;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.3);color:#fff;font-size:.92rem;backdrop-filter:blur(6px);transition:.2s}
.cx-chips a:hover{background:#fff;color:var(--green)}.cx-chips svg{width:16px;height:16px;flex:none}
.offices{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}
.off{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:22px 20px;display:flex;flex-direction:column;gap:6px}
.off:hover{border-color:var(--ochre);box-shadow:0 18px 30px -20px rgba(0,0,0,.35)}
.off .tag{font-size:.72rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--ochre)}.off h3{margin:0;font-size:1.08rem}.off p{margin:0;color:var(--muted);font-size:.93rem}
.off .acts{margin-top:auto;padding-top:12px;display:flex;gap:16px;flex-wrap:wrap;font-size:.9rem;font-weight:600}
.off .acts button{background:none;border:0;padding:0;font:inherit;color:var(--green);cursor:pointer}.off .acts button:hover,.off .acts a:hover{text-decoration:underline}
.off.hq{background:var(--green);border-color:var(--green);color:#fff}.off.hq p{color:rgba(255,255,255,.82)}.off.hq .tag{color:#f0c46f}.off.hq .acts button,.off.hq .acts a{color:#fff}
@media(max-width:1100px){.offices{grid-template-columns:repeat(3,1fr)}}
@media(max-width:700px){.offices{grid-template-columns:1fr}.cx-card{padding:26px 20px 22px;border-radius:22px}.cx{padding:44px 16px 96px}}
@media(prefers-reduced-motion:reduce){.cx-intro,.cx-card,.cx-chips{animation:none}}
/* --- gallery page: event video, project chips, project groups, lightbox --- */
.vsec{background:#16241a;color:#e8efe6;padding:64px 0 72px}.vsec h2{color:#fff;margin:0}.vsec .kick,.vsec .more{color:#f0c46f}.vsec p{margin:.4em 0 0;opacity:.8}
.vhead{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;flex-wrap:wrap;margin-bottom:26px}
.vwrap{position:relative;border-radius:24px;overflow:hidden;aspect-ratio:16/9;background:#000;box-shadow:0 30px 60px -30px rgba(0,0,0,.8)}
.vwrap video{width:100%;height:100%;display:block}.vwrap .snd{position:absolute;top:18px;right:18px;z-index:2;font:600 .95rem Inter,sans-serif;color:#231a05;background:var(--ochre);border:0;border-radius:99px;padding:11px 20px;cursor:pointer;box-shadow:0 8px 24px -8px rgba(0,0,0,.6);animation:ring 2.2s infinite;transition:opacity .3s,visibility .3s}.vwrap .snd:hover{background:#dc9a37}.vwrap .snd.gone{opacity:0;visibility:hidden}
.gsec{padding-top:40px}
.fchips{position:sticky;top:66px;z-index:20;display:flex;gap:8px;overflow-x:auto;padding:12px 2px;margin:0 0 30px;background:var(--sand);scrollbar-width:none}.fchips::-webkit-scrollbar{display:none}
.fchips button{flex:none;font:inherit;font-size:.92rem;font-weight:600;padding:9px 16px;border-radius:99px;border:1px solid var(--line);background:var(--card);cursor:pointer;transition:.2s;white-space:nowrap}
.fchips button small{opacity:.6;margin-left:3px}.fchips button:hover{border-color:var(--green)}.fchips button.on{background:var(--green);color:#fff;border-color:var(--green)}
.pgrp{margin-bottom:64px;scroll-margin-top:140px}.pgrp.hide{display:none}
.pgh{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;flex-wrap:wrap;margin-bottom:20px;border-bottom:1px solid var(--line);padding-bottom:14px}
.pgh h2{margin:0;font-size:clamp(1.4rem,2.6vw,2rem)}.pgh p{margin:.3em 0 0;color:var(--muted)}
.pgh h2:after{content:"";display:block;width:0;height:3px;margin-top:8px;border-radius:3px;background:var(--ochre);transition:width .8s .15s}.pgrp.in .pgh h2:after{width:56px}
.pgl{text-align:right;font-size:.92rem}.pgl span{display:block;color:var(--muted)}.pgl a{font-weight:600}
.pgrid{columns:3 260px;column-gap:14px}
.ph{display:block;position:relative;break-inside:avoid;margin:0 0 14px;border-radius:16px;overflow:hidden;background:var(--sand2)}
.ph img{width:100%;height:auto;display:block;transition:transform .7s cubic-bezier(.2,.8,.2,1),filter .4s}.ph:hover img{transform:scale(1.07);filter:brightness(1.06)}
.ph .cap2{position:absolute;left:0;right:0;bottom:0;padding:34px 14px 12px;color:#fff;font-size:.88rem;font-weight:600;background:linear-gradient(transparent,rgba(8,20,12,.82));transform:translateY(100%);transition:transform .35s}
.ph:hover .cap2,.ph:focus-visible .cap2{transform:none}
.gsec[data-f="all"] .ph.extra{display:none}
.gsec.js .ph{opacity:0;transform:translateY(34px) scale(.96)}.gsec.js .pgrp.in .ph{animation:pop .7s cubic-bezier(.2,.8,.2,1) forwards;animation-delay:calc(var(--k)*65ms)}
@keyframes pop{to{opacity:1;transform:none}}
.seeall{display:block;margin:6px auto 0;font:inherit;font-weight:600;padding:12px 26px;border-radius:99px;border:2px solid var(--green);color:var(--green);background:transparent;cursor:pointer;transition:.2s}.seeall:hover{background:var(--green);color:#fff}
.gsec:not([data-f="all"]) .seeall{display:none}
.lbx{position:fixed;inset:0;z-index:200;background:rgba(8,14,10,.95);display:flex;align-items:center;justify-content:center;opacity:0;visibility:hidden;transition:opacity .3s,visibility .3s}.lbx.on{opacity:1;visibility:visible}
.lstage{margin:0;display:flex;flex-direction:column;align-items:center;max-width:92vw}
.lstage img{max-width:86vw;max-height:76vh;border-radius:10px;opacity:0;transform:scale(.97);transition:opacity .35s,transform .35s}.lstage img.in{opacity:1;transform:none}
.lstage figcaption{color:#e8efe6;text-align:center;margin-top:16px;display:flex;gap:14px;align-items:baseline;flex-wrap:wrap;justify-content:center}
.lcap{font:700 1.15rem Fraunces,serif;color:#fff}.lcnt{font-size:.85rem;opacity:.7}.ltag{font-size:.78rem;color:#f0c46f;text-transform:uppercase;letter-spacing:.1em}
.lbx button{position:absolute;border:1px solid rgba(255,255,255,.3);background:rgba(255,255,255,.08);color:#fff;width:52px;height:52px;border-radius:50%;font-size:1.8rem;line-height:1;cursor:pointer;transition:.2s}.lbx button:hover{background:#fff;color:var(--green)}
.lp{left:24px;top:50%;margin-top:-26px}.ln{right:24px;top:50%;margin-top:-26px}.lx{right:24px;top:20px}
@media(max-width:900px){.lp,.ln{top:auto;bottom:22px;margin:0}.lp{left:calc(50% - 64px)}.ln{right:calc(50% - 64px)}.pgl{text-align:left}}
@media(prefers-reduced-motion:reduce){.gsec.js .ph{opacity:1;transform:none}}
/* --- gallery mosaic + banner --- */
.dark{background:#16241a;color:#e8efe6}.dark h2{color:#fff}.dark .kick,.dark .more{color:#f0c46f}
.mosaic{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:250px;grid-auto-flow:dense;gap:14px}
.mosaic a{position:relative;overflow:hidden;border-radius:22px;display:block;opacity:0;transform:translateY(46px) scale(.95);transition:opacity .9s calc(var(--i)*.11s),transform .9s cubic-bezier(.2,.8,.2,1) calc(var(--i)*.11s),box-shadow .3s}
.mosaic.in a{opacity:1;transform:none}.mosaic.in a:hover{transform:translateY(-7px);box-shadow:0 26px 44px -20px rgba(0,0,0,.8)}
.mosaic .t1{grid-column:span 2;grid-row:span 2}.mosaic .t2{grid-row:span 2}.mosaic .t3{grid-column:span 2}
.mosaic img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;animation:kb2 16s ease-in-out infinite alternate;animation-delay:calc(var(--i)*-2.3s);transition:filter .4s}
@keyframes kb2{from{transform:scale(1)}to{transform:scale(1.1) translate(-1.5%,-1%)}}
.mosaic a:hover img{filter:brightness(1.12) saturate(1.1)}
.mosaic .cap{position:absolute;left:0;right:0;bottom:0;padding:44px 18px 16px;color:#fff;background:linear-gradient(transparent,rgba(8,20,12,.85));font-size:.88rem;transform:translateY(55%);opacity:.9;transition:.4s}
.mosaic .cap b{display:block;font:700 1.05rem Fraunces,serif;margin-bottom:2px}.mosaic a:hover .cap{transform:none;opacity:1}
.mosaic .t1 .cap{transform:none;padding-top:70px}.mosaic .t1 .cap b{font-size:1.4rem}
.mosaic .more:before{content:"";position:absolute;inset:0;z-index:1;background:rgba(201,138,43,.82);transition:.4s}.mosaic .more:hover:before{background:rgba(46,91,59,.85)}
.mosaic .more .cap{z-index:2;inset:0;transform:none;background:none;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;font-size:.95rem}.mosaic .more .cap b{font-size:1.5rem}
.banner{position:relative;overflow:hidden;color:#fff;text-align:center;padding:150px 0 140px;background:linear-gradient(rgba(10,28,18,.62),rgba(10,28,18,.78)),url(img/g06.jpg) center/cover fixed}
.banner h2{font-size:clamp(2rem,5vw,3.6rem);margin:.2em 0 .3em}.banner p{max-width:560px;margin:0 auto 28px;font-size:1.15rem;opacity:.92}.banner .wrap{position:relative;z-index:4}
.banner .wave.top{top:-1px;bottom:auto;transform:rotate(180deg)}
.tick{position:absolute;left:0;right:0;top:50%;transform:translateY(-50%);z-index:1;overflow:hidden;white-space:nowrap;pointer-events:none;opacity:.16}
.tick div{display:inline-block;animation:tk 40s linear infinite}.tick span{display:inline-block;font:700 clamp(5rem,14vw,11rem)/1 Fraunces,serif;color:transparent;-webkit-text-stroke:2px #fff;margin-right:.5em;text-transform:uppercase}
@keyframes tk{to{transform:translateX(-50%)}}
.dropi{position:relative;width:46px;height:60px;margin:0 auto 14px}.dropi svg{position:relative;width:46px;animation:bob 3s ease-in-out infinite}
@keyframes bob{50%{transform:translateY(-7px)}}
.dropi i{position:absolute;left:50%;bottom:-4px;width:70px;height:24px;margin-left:-35px;border:2px solid rgba(159,211,238,.8);border-radius:50%;opacity:0;animation:rp2 3s ease-out infinite}.dropi i:nth-child(2){animation-delay:1s}.dropi i:nth-child(3){animation-delay:2s}
@keyframes rp2{from{transform:scale(.3);opacity:.9}to{transform:scale(2.6);opacity:0}}
@media(max-width:900px){.mosaic{grid-template-columns:1fr 1fr;grid-auto-rows:170px}.mosaic .cap{transform:none}.banner{padding:110px 0 100px;background-attachment:scroll}}
/* --- latest updates --- */
.ugrid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.ucard{background:var(--card);border:1px solid var(--line);border-radius:22px;overflow:hidden;display:flex;flex-direction:column;color:inherit;transition:transform .3s,box-shadow .3s,border-color .3s,opacity .7s}
.ucard:hover{transform:translateY(-6px);border-color:var(--ochre);box-shadow:0 22px 36px -22px rgba(0,0,0,.4)}
.ucard.hide{display:none}.ucard.pop{animation:pop .6s cubic-bezier(.2,.8,.2,1) both;animation-delay:calc(var(--k)*70ms);opacity:0;transform:translateY(24px)}
.uimg{position:relative;aspect-ratio:16/10;overflow:hidden;background:var(--sand2)}.uimg img{width:100%;height:100%;object-fit:cover;transition:transform .7s cubic-bezier(.2,.8,.2,1)}
.uimg.clip img{object-position:top;filter:sepia(.15)}.ucard:hover .uimg img{transform:scale(1.07)}
.udate{position:absolute;left:14px;top:14px;background:rgba(22,36,26,.86);color:#fff;font-size:.78rem;font-weight:600;padding:6px 12px;border-radius:99px}
.ub{padding:20px 22px 22px;display:flex;flex-direction:column;gap:8px;flex:1}.ub h3{margin:0;font-size:1.18rem;line-height:1.3}.ub p{margin:0;color:var(--muted);font-size:.94rem}.ub .more{margin-top:auto;padding-top:8px}
.utag{font-size:.72rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--ochre)}.t-media{color:var(--clay)}.t-event{color:var(--green2)}.t-story{color:#2f86c0}
.ufeat{display:grid;grid-template-columns:1.25fr 1fr;background:var(--card);border:1px solid var(--line);border-radius:28px;overflow:hidden;color:inherit;margin-bottom:34px;transition:box-shadow .3s,transform .3s}
.ufeat:hover{transform:translateY(-4px);box-shadow:0 26px 44px -26px rgba(0,0,0,.45)}.ufeat.hide{display:none}
.ufi{position:relative;min-height:320px;overflow:hidden}.ufi img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .8s}.ufeat:hover .ufi img{transform:scale(1.05)}
.unew{position:absolute;left:18px;top:18px;background:var(--ochre);color:#231a05;font-weight:700;font-size:.8rem;padding:7px 14px;border-radius:99px;display:flex;align-items:center;gap:8px}
.unew:before{content:"";width:8px;height:8px;border-radius:50%;background:#231a05;animation:blink 1.4s ease-in-out infinite}@keyframes blink{50%{opacity:.2}}
.uft{padding:38px 40px;display:flex;flex-direction:column;justify-content:center;gap:10px}.uft time{color:var(--muted);font-size:.9rem}.uft h2{margin:0;font-size:clamp(1.6rem,2.8vw,2.3rem)}.uft p{margin:0 0 10px;color:var(--muted)}.uft .btn{align-self:flex-start}
.unote{text-align:center;color:var(--muted);margin-top:36px}
.umeta{display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin-bottom:22px;padding-bottom:16px;border-bottom:1px solid var(--line);font-size:.92rem;color:var(--muted)}
.ubody p{font-size:1.1rem;line-height:1.75;margin:0 0 1em}
.uclip{margin:30px 0 0;background:var(--card);border:1px solid var(--line);border-radius:20px;padding:18px}.uclip img{width:100%;border-radius:10px;transition:transform .4s}.uclip a:hover img{transform:scale(1.01)}
.uclip figcaption{font-size:.86rem;color:var(--muted);margin-top:10px;text-align:center}
.unav{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:20px}.unav a{display:block;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px 18px;color:var(--ink);font-weight:600;font-size:.95rem;transition:.25s}
.unav a:hover{border-color:var(--green);transform:translateY(-3px)}.unav small{display:block;color:var(--ochre);font-weight:700;margin-bottom:4px}.unav .r{text-align:right}
@media(max-width:900px){.ugrid,.ufeat,.unav{grid-template-columns:1fr}.ufi{min-height:220px}.uft{padding:26px 22px}}
/* --- home: partners --- */
.partners{position:relative;overflow:hidden}
.pstats{display:flex;gap:30px}.pstats div{text-align:left}.pstats b{display:block;font:700 2.4rem/1 Fraunces,serif;color:var(--green)}.pstats span{font-size:.85rem;color:var(--muted)}
.plabel{display:flex;align-items:baseline;gap:14px;margin:34px 0 14px;font-weight:700;font-size:.82rem;letter-spacing:.14em;text-transform:uppercase;color:var(--ochre)}
.plabel:after{content:"";flex:1;height:1px;background:var(--line)}.plabel small{order:3;font-weight:500;letter-spacing:0;text-transform:none;color:var(--muted)}
.marquee{overflow:hidden;padding:10px 0 16px;-webkit-mask-image:linear-gradient(90deg,transparent,#000 7%,#000 93%,transparent);mask-image:linear-gradient(90deg,transparent,#000 7%,#000 93%,transparent)}
.mq-track{display:flex;width:max-content;animation:mq 48s linear infinite}.marquee:hover .mq-track{animation-play-state:paused}
@keyframes mq{to{transform:translateX(-50%)}}
.pl{flex:none;width:210px;height:116px;margin-right:16px;background:#fff;border:1px solid var(--line);border-radius:20px;display:flex;align-items:center;justify-content:center;padding:18px 22px;transition:transform .3s,box-shadow .3s,border-color .3s}
.pl img{max-width:100%;max-height:72px;object-fit:contain;transition:transform .45s cubic-bezier(.2,.8,.2,1.3)}
.pl:hover{transform:translateY(-6px);border-color:var(--ochre);box-shadow:0 18px 30px -18px rgba(0,0,0,.35)}.pl:hover img{transform:scale(1.08)}
.pimpl{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.pi{background:#fff;border:1px solid var(--line);border-radius:22px;padding:22px 20px 18px;text-align:center;transition:transform .3s,box-shadow .3s,border-color .3s}
.pi:hover{transform:translateY(-6px) rotate(-.6deg);border-color:var(--green2);box-shadow:0 22px 34px -20px rgba(0,0,0,.35)}
.pi-logo{height:96px;display:flex;align-items:center;justify-content:center;margin-bottom:12px}.pi-logo img{max-height:96px;max-width:100%;object-fit:contain;transition:transform .5s cubic-bezier(.2,.8,.2,1.3)}
.pi:hover .pi-logo img{transform:scale(1.08)}.pi b{font-size:.95rem}
.allsup{margin-top:30px;background:var(--card);border:1px solid var(--line);border-radius:20px;overflow:hidden}
.allsup summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;padding:18px 24px;font-weight:600;color:var(--green)}.allsup summary::-webkit-details-marker{display:none}
.allsup summary i{width:30px;height:30px;border-radius:50%;background:var(--green);position:relative;flex:none;transition:transform .35s}
.allsup summary i:before,.allsup summary i:after{content:"";position:absolute;left:50%;top:50%;width:12px;height:2px;margin:-1px 0 0 -6px;background:#fff;border-radius:2px}.allsup summary i:after{transform:rotate(90deg);transition:transform .35s}
.allsup[open] summary i{transform:rotate(180deg)}.allsup[open] summary i:after{transform:rotate(0)}
.supchips{display:flex;flex-wrap:wrap;gap:10px;padding:0 24px 24px}
.supchips span{background:var(--sand);border:1px solid var(--line);padding:9px 16px;border-radius:99px;font-size:.92rem}
.allsup[open] .supchips span{animation:chip .5s cubic-bezier(.2,.8,.2,1.2) both;animation-delay:calc(var(--i)*35ms)}
@keyframes chip{from{opacity:0;transform:translateY(14px) scale(.9)}}
@media(max-width:900px){.pimpl{grid-template-columns:1fr 1fr}.pstats{gap:20px}.pl{width:170px;height:100px}}
@media(prefers-reduced-motion:reduce){.mq-track{animation:none;flex-wrap:wrap;width:auto;row-gap:16px}.mq-track [aria-hidden]{display:none}.marquee{-webkit-mask-image:none;mask-image:none}}
/* --- clickable gateway cards on home --- */
a.stat{display:block;color:inherit;transition:.25s}a.stat:hover{transform:translateY(-5px);border-color:var(--ochre);box-shadow:0 18px 30px -18px rgba(0,0,0,.4)}
.stat .go{display:block;margin-top:10px;font-style:normal;font-size:.85rem;font-weight:600;color:var(--green)}
.sh{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;flex-wrap:wrap;margin-bottom:28px}.sh .more{white-space:nowrap}
.strip{display:grid;grid-template-columns:repeat(6,1fr);gap:10px}.strip a{aspect-ratio:1;overflow:hidden;border-radius:14px;display:block}.strip img{width:100%;height:100%;object-fit:cover;transition:.45s}.strip a:hover img{transform:scale(1.1)}
@media(max-width:900px){.strip{grid-template-columns:repeat(3,1fr)}#bd{grid-template-columns:1fr 1fr!important}}
/* --- water-drop cursor (fine pointers only; enabled by JS via html.has-cur) --- */
html.has-cur,html.has-cur a,html.has-cur button,html.has-cur label,html.has-cur .lb{cursor:none}
html.has-cur input,html.has-cur textarea{cursor:text}
.cur-dot,.cur-ring,.cur-trail,.cur-ripple{position:fixed;left:0;top:0;pointer-events:none;border-radius:50%}
.cur-dot{width:9px;height:9px;background:var(--ochre);z-index:10001;transform:translate(-50%,-50%);transition:opacity .2s,width .2s,height .2s}
.cur-ring{width:40px;height:40px;border:2px solid #fff;mix-blend-mode:difference;z-index:10000;transform:translate(-50%,-50%);transition:width .28s,height .28s,background .28s,opacity .2s}
.cur-ring.link{width:68px;height:68px;background:rgba(255,255,255,.9)}
.cur-ring.down{width:26px;height:26px}.cur-dot.link{width:0;height:0}
.cur-ring.hide,.cur-dot.hide{opacity:0}
.cur-trail{width:12px;height:12px;background:rgba(95,168,211,.55);z-index:9990;animation:tr .8s ease-out forwards}
@keyframes tr{from{transform:translate(-50%,-50%) scale(1)}to{transform:translate(-50%,calc(-50% + 22px)) scale(0);opacity:0}}
.cur-ripple{width:110px;height:110px;border:2px solid #5fa8d3;z-index:9995;animation:rp .85s ease-out forwards}
@keyframes rp{from{transform:translate(-50%,-50%) scale(.1);opacity:1}to{transform:translate(-50%,-50%) scale(1);opacity:0}}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}.reveal,.hero h1 span,.hero .kick,.hero p,.hero .btn{opacity:1!important;transform:none!important}.in .dots i.sea{transform:rotate(-45deg);opacity:.25}.tank .water{transform:none}.sprout path{stroke-dashoffset:0}}
@media(max-width:900px){.g3,.g2,.split,.mv,.fg{grid-template-columns:1fr}.stats{grid-template-columns:1fr 1fr}.gal{columns:2}
 .burger{display:block}nav{display:none;position:absolute;top:100%;left:0;right:0;background:var(--sand);padding:12px 20px;border-bottom:1px solid var(--line);flex-direction:column}nav.open{display:flex}section{padding:56px 0}.cta{padding:36px 22px}}
"""

JS = """
document.querySelector('.burger').onclick=()=>document.querySelector('nav').classList.toggle('open');
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
const countUp=el=>{const t=+el.dataset.count,s=el.dataset.suffix||'',d=+(el.dataset.dec||0),id=(el._c=(el._c||0)+1);let st=null;
 const f=ts=>{if(el._c!==id)return;st=st||ts;const p=Math.min((ts-st)/1400,1);el.textContent=(t*p).toLocaleString('en-IN',{maximumFractionDigits:d,minimumFractionDigits:d})+s;if(p<1)requestAnimationFrame(f)};requestAnimationFrame(f)};
document.querySelectorAll('[data-count]').forEach(el=>{if(el.closest('.views'))return;const o=new IntersectionObserver(([e])=>{if(!e.isIntersecting)return;o.disconnect();countUp(el)});o.observe(el)});
/* rain + ripples over hero */
(()=>{const cv=document.querySelector('canvas.rain');if(!cv||matchMedia('(prefers-reduced-motion:reduce)').matches)return;
const c=cv.getContext('2d');let W,H,rip=[],dr=[],on=true;const rs=()=>{W=cv.width=cv.offsetWidth;H=cv.height=cv.offsetHeight};rs();addEventListener('resize',rs);
new IntersectionObserver(([e])=>on=e.isIntersecting).observe(cv);
const loop=()=>{requestAnimationFrame(loop);if(!on||!cv.closest('.slide.on'))return;c.clearRect(0,0,W,H);
 if(Math.random()<.35)dr.push({x:Math.random()*W,y:-20,v:9+Math.random()*6,y1:H*(.45+Math.random()*.4)});
 c.strokeStyle='rgba(255,255,255,.35)';c.lineWidth=1.2;
 dr=dr.filter(d=>{d.y+=d.v;c.beginPath();c.moveTo(d.x,d.y-16);c.lineTo(d.x,d.y);c.stroke();if(d.y>=d.y1){rip.push({x:d.x,y:d.y1,r:1});return false}return true});
 rip=rip.filter(r=>{r.r+=.7;const a=1-r.r/60;if(a<=0)return false;c.strokeStyle='rgba(255,255,255,'+(a*.55)+')';c.beginPath();c.ellipse(r.x,r.y,r.r,r.r*.32,0,0,7);c.stroke();return true})};loop()})();
/* timeline progress line */
(()=>{const t=document.querySelector('.tl');if(!t)return;const f=()=>{const r=t.getBoundingClientRect(),p=Math.min(1,Math.max(0,(innerHeight*.6-r.top)/r.height));t.style.setProperty('--p',p)};addEventListener('scroll',f,{passive:true});f()})();
/* hero slider */
(()=>{const h=document.querySelector('.hero.slider');if(!h)return;const S=[...h.querySelectorAll('.slide')],D=[...h.querySelectorAll('.dts button')];
let i=0,t=null;const rm=matchMedia('(prefers-reduced-motion:reduce)').matches;
const go=n=>{i=(n+S.length)%S.length;S.forEach((s,k)=>s.classList.toggle('on',k===i));D.forEach((d,k)=>d.classList.toggle('on',k===i))};
const stop=()=>{clearInterval(t);t=null};const play=()=>{stop();if(!rm)t=setInterval(()=>go(i+1),7500)};
h.querySelector('.pv').onclick=()=>{go(i-1);play()};h.querySelector('.nx').onclick=()=>{go(i+1);play()};
D.forEach((d,k)=>d.onclick=()=>{go(k);play()});
h.addEventListener('mouseenter',stop);h.addEventListener('mouseleave',play);
document.addEventListener('visibilitychange',()=>document.hidden?stop():play());
addEventListener('keydown',e=>{if(e.key==='ArrowLeft'){go(i-1);play()}if(e.key==='ArrowRight'){go(i+1);play()}});
let sx=null;h.addEventListener('touchstart',e=>sx=e.touches[0].clientX,{passive:true});h.addEventListener('touchend',e=>{if(sx===null)return;const d=e.changedTouches[0].clientX-sx;if(Math.abs(d)>50){go(d<0?i+1:i-1);play()}sx=null});
const m=location.hash.match(/^#s([1-5])$/);go(m?+m[1]-1:0);play()})();
/* rain section: tabs, replay */
(()=>{const rb=document.getElementById('rb');if(!rb)return;const d=rb.querySelector('.dots'),y=rb.querySelector('.yr');
const rp=el=>{el.classList.remove('play');void el.offsetWidth;el.classList.add('play')};
const cur=()=>rb.querySelector('.view.on');const run=()=>{rp(cur().id==='v1'?d:y);cur().querySelectorAll('[data-count]').forEach(countUp)};
const ob=rb.closest('section').querySelectorAll('.opt button');ob.forEach(b=>b.onclick=()=>{ob.forEach(x=>x.classList.toggle('on',x===b));rb.querySelectorAll('.view').forEach(v=>v.classList.toggle('on',v.id===b.dataset.v));run()});
rb.querySelectorAll('.replay').forEach(b=>b.onclick=run);
const o=new IntersectionObserver(([e])=>{if(e.isIntersecting){o.disconnect();run()}},{threshold:.3});o.observe(rb)})();
/* fodder, fruit & forest: tabs, replay, play when in view */
(()=>{const s=document.getElementById('fff');if(!s)return;if(!matchMedia('(prefers-reduced-motion:reduce)').matches)s.classList.add('armed');
const bt=s.querySelectorAll('.opt button'),vs=s.querySelectorAll('.view'),cur=()=>s.querySelector('.view.on');
const run=()=>{const v=cur();v.classList.remove('play');void v.offsetWidth;v.classList.add('play');v.querySelectorAll('[data-count]').forEach(countUp)};
bt.forEach(b=>b.onclick=()=>{bt.forEach(x=>{x.classList.toggle('on',x===b);x.setAttribute('aria-selected',x===b)});vs.forEach(v=>v.classList.toggle('on',v.id===b.dataset.v));run()});
s.querySelectorAll('.replay').forEach(b=>b.onclick=run);
const o=new IntersectionObserver(([e])=>{if(e.isIntersecting){o.disconnect();run()}},{threshold:.3});o.observe(s.querySelector('.views'))})();
/* water-drop cursor: dot + trailing ring, droplet trail, ripple on click */
(()=>{if(!matchMedia('(hover:hover) and (pointer:fine)').matches||matchMedia('(prefers-reduced-motion:reduce)').matches)return;
const mk=c=>{const d=document.createElement('div');d.className=c;document.body.appendChild(d);return d};
const dot=mk('cur-dot hide'),ring=mk('cur-ring hide');let x=0,y=0,rx=0,ry=0,lt=0,ready=false;
document.documentElement.classList.add('has-cur');
addEventListener('mousemove',e=>{x=e.clientX;y=e.clientY;if(!ready){ready=true;rx=x;ry=y;dot.classList.remove('hide');ring.classList.remove('hide')}
 const l=!!e.target.closest('a,button,label,.card,.gal a,.lb');dot.classList.toggle('link',l);ring.classList.toggle('link',l);
 const n=performance.now();if(n-lt>45&&!l){lt=n;const t=mk('cur-trail');t.style.left=x+'px';t.style.top=y+'px';t.onanimationend=()=>t.remove()}});
addEventListener('mousedown',()=>ring.classList.add('down'));addEventListener('mouseup',()=>ring.classList.remove('down'));
addEventListener('click',e=>{const r=mk('cur-ripple');r.style.left=e.clientX+'px';r.style.top=e.clientY+'px';r.onanimationend=()=>r.remove()});
document.addEventListener('mouseleave',()=>{dot.classList.add('hide');ring.classList.add('hide')});document.addEventListener('mouseenter',()=>{if(ready){dot.classList.remove('hide');ring.classList.remove('hide')}});
(function f(){rx+=(x-rx)*.16;ry+=(y-ry)*.16;dot.style.left=x+'px';dot.style.top=y+'px';ring.style.left=rx+'px';ring.style.top=ry+'px';requestAnimationFrame(f)})()})();
/* back to top */
document.querySelectorAll('.totop').forEach(b=>b.onclick=()=>scrollTo({top:0,behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth'}));
/* map tabs */
document.querySelectorAll('.map .tabs button').forEach(b=>b.onclick=()=>{document.querySelectorAll('.map .tabs button').forEach(x=>x.classList.remove('on'));b.classList.add('on');document.querySelector('.map iframe').src=b.dataset.src});
const lb=document.querySelector('.lb');if(lb){document.querySelectorAll('.gal a').forEach(a=>a.onclick=e=>{e.preventDefault();lb.querySelector('img').src=a.href;lb.classList.add('on')});lb.onclick=()=>lb.classList.remove('on')}
"""

def footer_html():
    p1, p2 = PHONE1.replace(" ", ""), PHONE2.replace(" ", "")
    leaves = "".join('<span class="leaf-f" style="left:%d%%;animation-duration:%ds;animation-delay:%ds"></span>' % (x, d, dl) for x, d, dl in [(8, 10, 0), (30, 13, 3), (58, 11, 1), (84, 14, 5)])
    progs = "".join('<li><a href="p-%s.html">%s</a></li>' % (k, E(PROGRAMS[k]["title"])) for k in ORDER)
    explore = "".join('<li><a href="%s">%s</a></li>' % (h, l) for h, l in [("index.html", "Home"), ("about.html", "About the Trust"), ("activities.html", "Our impact"), ("gallery.html", "Gallery"), ("explore.html", "Explore in 3D"), ("updates.html", "Latest updates"), ("legal.html", "Legal details"), ("contact.html", "Contact")])
    badges = "".join('<a href="legal.html">%s</a>' % b for b in ["80G", "12A", "CSR-1", "NGO Darpan"])
    return (f'<footer class="ft">{WAVE("#16241a")}<div class="wrap">'
            f'<div class="ft-cta reveal">{leaves}<div class="ft-rip" aria-hidden="true"><i></i><i></i><i></i></div>'
            '<div class="ft-cta-t"><div class="kick">Every drop counts</div><h3>Help bring water back to Kutch&#8217;s villages.</h3>'
            '<p>CSR partners, foundations and individuals – 80G and 12A registered, CSR-1 registered.</p></div>'
            f'<div class="ft-cta-b"><a class="btn" href="contact.html">Partner with us</a><a class="btn alt" href="tel:{p1}">{ICON["phone"]}{PHONE1}</a></div></div>'
            '<div class="ft-grid">'
            f'<div class="ft-brand"><a class="ft-logo" href="index.html"><img src="img/logo.png" alt="Kutch Fodder Fruit &amp; Forest Development Trust"></a>'
            '<p>Well-being of people through environmental up-gradation and well management of natural resources.</p>'
            f'<div class="ft-badges">{badges}</div></div>'
            f'<div><h4>Programs</h4><ul class="ft-links">{progs}</ul></div>'
            f'<div><h4>Explore</h4><ul class="ft-links">{explore}</ul></div>'
            f'<div><h4>Reach us</h4><ul class="ft-contact"><li>{ICON["pin"]}<span>{E(ADDR)}</span></li>'
            f'<li>{ICON["phone"]}<span><a href="tel:{p1}">{PHONE1}</a> · <a href="tel:{p2}">{PHONE2}</a></span></li>'
            f'<li>{ICON["mail"]}<span><a href="mailto:{MAIL}">{MAIL}</a></span></li>'
            f'<li>{ICON["clock"]}<span>Mon–Sat 9:00–18:00 · Sunday closed</span></li></ul></div></div>'
            '<div class="ft-bottom"><span>© 2026 Kutch Fodder Fruit &amp; Forest Development Trust · Reg. No. E-940 Kutch, 28.03.1989</span>'
            '<span class="ft-bl"><a href="../original/index.html">View original site ↗</a><button class="totop" type="button" aria-label="Back to top">'
            '<svg viewBox="0 0 40 52"><path fill="currentColor" d="M20 2C20 2 4 22 4 33a16 16 0 0 0 32 0C36 22 20 2 20 2z"/></svg>Back to top</button></span></div>'
            '</div></footer>')


# Preview builds (GitHub Pages) stay out of search results so they never compete with kfffdt.org.in.
# Set to False when this design goes live on the real domain.
NOINDEX = True


def page(fname, title, body, desc="", bare=False):
    nav = "".join('<a href="%s"%s>%s</a>' % (h, ' class="on"' if h == fname or (fname.startswith("p-") and h == "projects.html") or (fname.startswith("u-") and h == "updates.html") else "", l) for h, l in NAV)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">{'<meta name="robots" content="noindex, nofollow">' if NOINDEX else ''}
<title>{E(title)} · KFFFDT</title><meta name="description" content="{E(desc or 'Kutch Fodder Fruit and Forest Development Trust – community-centric sustainable development in Kutch since 1989.')}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600&display=swap">
<style>{CSS}</style></head><body>
<header><div class="bar"><a href="index.html"><img src="img/logo.png" alt="KFFFDT"></a><button class="burger" aria-label="Menu">☰</button><nav>{nav}</nav></div></header>
{body}
{"" if bare else footer_html()}
<div class="lb"><img alt=""></div><script>{JS}</script></body></html>"""

WAVE = lambda fill: '<div class="wave"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path fill="%s" d="M0 35c120 28 240 28 360 0s240-28 360 0 240 28 360 0 240-28 360 0v35H0z"/></svg><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path fill="%s" d="M0 30c120-26 240-26 360 0s240 26 360 0 240-26 360 0 240 26 360 0v40H0z"/></svg></div>' % (fill, fill)

def words(t, d0=.15):
    out = []
    for i, w in enumerate(t.split(" ")):
        out.append('<span style="animation-delay:%.2fs">%s</span>' % (d0 + i * .09, w) if w != "<br>" else "<br>")
    return " ".join(out)

DOTS = "".join('<i class="%s" style="--d:%.2fs"></i>' % ("keep" if (i * 53) % 100 < 30 else "sea", .5 + (i % 10) * .07 + (i // 10) * .05) for i in range(100))
TANK = '<svg class="tank" viewBox="0 0 200 240" aria-label="Village tank filling with water"><defs><clipPath id="tk"><path d="M30 40h140l-12 170a14 14 0 0 1-14 13H56a14 14 0 0 1-14-13z"/></clipPath></defs><g clip-path="url(#tk)"><rect width="200" height="240" fill="#e8f3f8"/><g class="water"><g class="wv"><path d="M-80 90q20-14 40 0t40 0 40 0 40 0 40 0 40 0 40 0 40 0V260H-80z" fill="#5fa8d3"/></g></g></g><path d="M30 40h140l-12 170a14 14 0 0 1-14 13H56a14 14 0 0 1-14-13z" fill="none" stroke="#2e5b3b" stroke-width="6" stroke-linejoin="round"/><path d="M22 40h156" stroke="#2e5b3b" stroke-width="8" stroke-linecap="round"/></svg>'
SPROUT = '<svg class="sprout" viewBox="0 0 48 48" fill="none" stroke="#3f7a4f" stroke-width="3" stroke-linecap="round"><path d="M24 44V22"/><path d="M24 26C24 16 16 12 8 12c0 9 6 14 16 14z"/><path d="M24 22c0-8 6-12 16-12 0 8-6 13-16 12z"/></svg>'
EVENTS = [("1988–89", "Founders negotiate with the government for cultivable wasteland; the Trust is registered on 28 March 1989 at Kothara, Abdasa."), ("1998 →", "Watershed, drought-proofing and storage-tank works begin across Kutch villages."), ("2001", "Kutch earthquake: temporary shelters, then 134 permanent houses, a school and a drinking-water scheme."), ("2012", "Kutch Jal Mandir Abhiyan starts reviving traditional village water tanks with community tractors."), ("2021", "80G, 12A and CSR-1 registrations – transparent partnerships with CSR funders."), ("2024", "332 Jal Mandir tanks revived and 8,835 lac litres of storage added. The journey continues.")]
TL = "".join('<div class="ev reveal"><b>%s</b><p>%s</p></div>' % (y, E(t)) for y, t in EVENTS)

def slide(img, kick, head, text, btns, fx="", on=False, first=False):
    b = " &nbsp; ".join('<a class="btn%s" href="%s">%s</a>' % (" alt" if k else "", h, t) for k, (h, t) in enumerate(btns))
    return f'<div class="slide{" on" if on else ""}"><img src="img/{img}.jpg" alt=""{"" if first else " loading=\"lazy\""}>{fx}<div class="wrap"><div class="kick">{kick}</div><h1>{words(head)}</h1><p>{text}</p><p style="margin-top:26px">{b}</p></div></div>'

_wave2 = lambda c: '<svg viewBox="0 0 1440 40" preserveAspectRatio="none"><path fill="%s" d="M0 20c120 18 240 18 360 0s240-18 360 0 240 18 360 0 240-18 360 0v20H0z"/></svg>' % c
FX_RISE = '<div class="fx fx-rise">%s%s</div>' % (_wave2("rgba(95,168,211,.5)"), _wave2("rgba(140,200,230,.5)"))
FX_LEAVES = '<div class="fx fx-leaves">' + "".join('<span class="lf" style="--x:%d%%;--s:%dpx;--t:%.1fs;--d:%.1fs;--c:%s"></span>' % ((i * 37 + 8) % 96, 12 + (i * 7) % 16, 8 + (i * 5) % 7, -((i * 3) % 11), ["#6fa95f", "#c98a2b", "#8fbf5a", "#e0b04f"][i % 4]) for i in range(18)) + "</div>"
FX_GRASS = '<div class="fx grass">' + "".join('<i style="--x:%.1f%%;--h:%dpx;--t:%.1fs;--d:%.1fs;--g:%s"></i>' % (i * 1.35, 60 + (i * 53) % 110, 2.4 + (i % 5) * .5, -(i % 7) * .4, ["#7fb04e", "#9fcb5f", "#5f9a45"][i % 3]) for i in range(75)) + "</div>"
FX_SUN = '<div class="fx fx-sun"></div><div class="fx fx-glow"></div>'
SLIDES = "".join([
    slide("hero", "Bhuj · Kutch · Gujarat · Since 1989", "Bringing water, green <br> and livelihood back to Kutch.", "Kutch Fodder Fruit &amp; Forest Development Trust helps village communities manage their own natural resources – in 200+ villages.", [("projects.html", "Our programs"), ("contact.html", "Contact us")], '<canvas class="rain"></canvas>', on=True, first=True),
    slide("g11", "Kutch Jal Mandir Abhiyan", "332 village tanks, <br> brought back to life.", "Traditional drinking-water tanks revived with the villagers' own tractors – adding 8,835 lac litres of storage.", [("p-kutch-jal-mandir-abhiyan.html", "See the project"), ("activities.html", "Our impact")], FX_RISE),
    slide("g17", "Agriculture Development", "Seeds of a <br> greener tomorrow.", "Anmol Beej Bank, chemical-free farming and fodder security for rainfed farmers.", [("p-agriculture-development.html", "Explore agriculture"), ("projects.html", "All programs")], FX_LEAVES),
    slide("g13", "Animal Health Care · Grazing Land", "Healthy herds, <br> richer grazing lands.", "Pashupalak Mitra care centres and Gauchar land development keep Kutch's pastoral families thriving.", [("p-animal-health-care.html", "Animal health care"), ("p-agriculture-development.html", "Grazing land")], FX_GRASS),
    slide("g09", "Community · Since 1989", "Built by villages, <br> together.", "In 200+ villages, people lead – from the 2001 earthquake rebuild to today's water, farm and school projects.", [("about.html", "Our story"), ("contact.html", "Join us")], FX_SUN),
])
SLIDER = '<div class="hero slider" aria-roledescription="carousel" aria-label="Featured programs">%s<div class="hctl"><button class="pv" aria-label="Previous slide">&#8249;</button><span class="dts">%s</span><button class="nx" aria-label="Next slide">&#8250;</button></div>%s</div>' % (SLIDES, "".join('<button aria-label="Slide %d"%s></button>' % (k + 1, ' class="on"' if k == 0 else "") for k in range(5)), WAVE("#f7f1e3"))

TILES = [("t1", "g03", "Revived village pond", "Kutch Jal Mandir Abhiyan"), ("t2", "g16", "Krishi Seva Kendra", "Farmers' meeting"), ("", "g09", "Inauguration", "With the community"), ("", "g17", "Tree plantation", "Greener Kutch"), ("t3", "g13", "Livestock at the village pond", "Animal health care"), ("", "g11", "Traditional step-well tank", "Heritage revived"), ("more", "g07", "View all photos", "Open the full gallery")]
TILE_HASH = {"g03": "#aerial", "g16": "#ksk", "g09": "#gauchar", "g17": "#gauchar", "g13": "#animal", "g11": "#jal"}
MOSAIC = '<div class="mosaic reveal">' + "".join('<a class="%s" href="gallery.html%s" style="--i:%d"><img src="img/%s.jpg" alt="%s" loading="lazy"><span class="cap"><b>%s</b>%s</span></a>' % (c, TILE_HASH.get(g, ""), i, g, t, t, sub) for i, (c, g, t, sub) in enumerate(TILES)) + "</div>"
TICK = "".join("<span>Water</span><span>Green</span><span>Livelihood</span><span>Fodder</span><span>Fruit</span><span>Forest</span>" for _ in range(2))
BANNER = ('<div class="banner">' + WAVE("#f7f1e3").replace('class="wave"', 'class="wave top"') + '<div class="tick"><div>' + TICK + '</div></div>'
          '<div class="wrap reveal"><div class="dropi"><i></i><i></i><i></i><svg viewBox="0 0 40 52"><path fill="#9fd3ee" d="M20 2C20 2 4 22 4 33a16 16 0 0 0 32 0C36 22 20 2 20 2z"/></svg></div>'
          '<h2>Every drop counts.<br>Every village matters.</h2><p>Join us in bringing water, green and livelihood back to Kutch.</p>'
          '<a class="btn" href="contact.html">Partner with us</a> &nbsp; <a class="btn alt" href="projects.html">See our programs</a></div>' + WAVE("#efe5cf") + '</div>')

MONTHS = [("Jan", 31), ("Feb", 28), ("Mar", 31), ("Apr", 30), ("May", 31), ("Jun", 30), ("Jul", 31), ("Aug", 31), ("Sep", 30), ("Oct", 31), ("Nov", 30), ("Dec", 31)]
RAIN = {"Jun": [24, 28], "Jul": [3, 8, 14, 19, 27], "Aug": [2, 9, 16, 23], "Sep": [6, 15]}  # 13 days, illustrative monsoon spread
_rk = iter(range(13))
YR = "".join('<span class="m">%s</span><div class="mo">%s</div>' % (m, "".join('<i class="r" style="--d:%.2fs"></i>' % (.18 * next(_rk)) if day in RAIN.get(m, []) else "<i></i>" for day in range(1, n + 1))) for m, n in MONTHS)

# ---- Gallery page: photos grouped by project / event ----
GROUPS = [
    ("jal", "Kutch Jal Mandir Abhiyan", "p-kutch-jal-mandir-abhiyan.html", "Reviving traditional village tanks with the community, 2012–2024."),
    ("aerial", "Aerial views · 2024", "p-water-conservation.html", "Drone photos of village tanks, Aug–Sep 2024."),
    ("watershed", "Watershed & check dams", "p-water-conservation.html", "Check dams and watershed works holding monsoon water."),
    ("wasmo", "WASMO – drinking water", "p-decentralized-drinking-water-supply-scheme-project.html", "Community-managed drinking water schemes."),
    ("ksk", "Krishi Seva Kendra & Bio Resource Centre", "p-agriculture-development.html", "Farmer meetings, soil testing and chemical-free farming."),
    ("seed", "Anmol Beej Bank & green fodder", "p-agriculture-development.html", "Traditional seeds and Napier fodder for rainfed farmers."),
    ("gauchar", "Gauchar land & tree plantation", "p-agriculture-development.html", "Grazing land pilot at Nani Khakhar and plantation drives."),
    ("animal", "Livestock & animal health", "p-animal-health-care.html", "Vaccination camps, vet care and water for herds."),
    ("edu", "Education – Van Shala", "p-primary-education-for-unreached-community.html", "Van Shala at Kalara Wandh, Lakhpat, and village schools."),
    ("community", "Community & awards", "about.html", "Women's meetings, village gatherings and recognition."),
]
PHOTOS = [
    ('jal', 'jal-01.jpg', 'Cracked, dry tank bed', 720, 332),
    ('jal', 'jal-02.jpg', 'Villagers gather on the dry bed', 720, 498),
    ('jal', 'jal-03.jpg', 'Puja before work begins', 720, 540),
    ('jal', 'jal-04.jpg', 'Blessings at the excavation site', 720, 540),
    ('jal', 'jal-05.jpg', "Excavator and the village's tractors", 720, 298),
    ('jal', 'jal-06.jpg', 'Desilting the tank', 720, 540),
    ('jal', 'jal-07.jpg', 'Students visit a work site', 720, 416),
    ('jal', 'jal-08.jpg', 'Water drums for families', 720, 400),
    ('jal', 'jal-09.jpg', 'Traditional step-well tank', 720, 504),
    ('jal', 'jal-10.jpg', 'Overflowing after rain', 720, 338),
    ('jal', 'jal-11.jpg', 'Full tank at the weir', 720, 348),
    ('jal', 'jal-12.jpg', 'Evening at a revived tank', 720, 332),
    ('jal', 'jal-13.jpg', 'Revived tank below the hills', 720, 340),
    ('jal', 'jal-14.jpg', 'Tank full after monsoon', 720, 330),
    ('jal', 'jal-15.jpg', 'Women at the filled tank', 720, 406),
    ('jal', 'jal-16.jpg', 'Cattle drinking at the tank', 720, 332),
    ('aerial', 'aerial-01.jpg', 'Revived tank from the air', 720, 406),
    ('aerial', 'aerial-02.jpg', 'Tank and embankment, aerial view', 720, 406),
    ('aerial', 'aerial-03.jpg', 'Village tanks after monsoon', 720, 406),
    ('aerial', 'aerial-04.jpg', 'Full tank in green surroundings', 720, 406),
    ('aerial', 'aerial-05.jpg', 'Chain of ponds, aerial view', 720, 406),
    ('aerial', 'aerial-06.jpg', 'Tank beside farmland', 720, 406),
    ('aerial', 'aerial-07.jpg', 'Wetland after the rains', 720, 406),
    ('aerial', 'aerial-08.jpg', 'Pond by the highway', 720, 406),
    ('watershed', 'watershed-01.jpg', 'Check dam holding water', 720, 404),
    ('watershed', 'watershed-02.jpg', 'Piyoni, post-monsoon', 720, 540),
    ('watershed', 'watershed-03.jpg', 'Watershed project, Lathedi – Abdasa', 720, 540),
    ('watershed', 'watershed-04.jpg', 'Check dam overflowing, Lathedi', 720, 540),
    ('wasmo', 'wasmo-01.jpg', 'Village water tower', 464, 498),
    ('wasmo', 'wasmo-02.jpg', 'Household water point', 621, 400),
    ('wasmo', 'wasmo-03.jpg', 'Women at the village water point', 652, 322),
    ('wasmo', 'wasmo-04.jpg', 'Drinking-water intake', 720, 476),
    ('ksk', 'ksk-01.jpg', 'Meeting at Krishi Seva Kendra', 720, 324),
    ('ksk', 'ksk-02.jpg', 'Field visit with farmers', 720, 404),
    ('ksk', 'ksk-03.jpg', 'Soil health check', 720, 540),
    ('ksk', 'ksk-04.jpg', 'Soil testing support', 720, 322),
    ('ksk', 'ksk-05.jpg', 'Bio-inputs at the resource centre', 720, 540),
    ('ksk', 'ksk-06.jpg', 'Farmer with his harvest', 720, 480),
    ('seed', 'seed-01.jpg', 'Traditional millet seed', 433, 560),
    ('seed', 'seed-02.jpg', 'Seed stock', 668, 402),
    ('seed', 'seed-03.jpg', 'Anmol Beej Rath seed van', 720, 408),
    ('seed', 'seed-04.jpg', 'Napier green-fodder cuttings', 720, 480),
    ('seed', 'seed-05.jpg', 'Farmers with fodder cuttings', 720, 636),
    ('seed', 'seed-06.jpg', 'Tall fodder crop', 720, 550),
    ('gauchar', 'gauchar-01.jpg', 'Preparing Gauchar land', 694, 376),
    ('gauchar', 'gauchar-02.jpg', 'Seed drill on grazing land', 662, 334),
    ('gauchar', 'gauchar-03.jpg', 'Plantation on Gauchar land', 617, 410),
    ('gauchar', 'gauchar-04.jpg', 'Pilot project inauguration', 705, 366),
    ('gauchar', 'gauchar-05.jpg', 'Tree plantation drive', 720, 474),
    ('animal', 'animal-01.jpg', 'Livestock health camp', 720, 646),
    ('animal', 'animal-02.jpg', 'Checking sheep', 720, 404),
    ('animal', 'animal-03.jpg', 'Ear tag and vaccine', 475, 338),
    ('animal', 'animal-04.jpg', 'Treating a buffalo', 450, 338),
    ('animal', 'animal-05.jpg', 'Vet care for goats', 569, 338),
    ('animal', 'animal-06.jpg', 'Advising a herder family', 717, 432),
    ('animal', 'animal-07.jpg', 'Mobile animal-health van', 557, 538),
    ('animal', 'animal-08.jpg', 'Herd at a village pond', 720, 324),
    ('animal', 'animal-09.jpg', 'Cattle at the water trough', 720, 324),
    ('edu', 'edu-01.jpg', 'Building the Van Shala shelter', 403, 238),
    ('edu', 'edu-02.jpg', 'Van Shala classroom', 346, 238),
    ('edu', 'edu-03.jpg', 'Mid-day meal at Van Shala', 372, 230),
    ('edu', 'edu-04.jpg', 'Open-air class', 415, 242),
    ('edu', 'edu-05.jpg', 'Learning under the sky', 419, 242),
    ('edu', 'edu-06.jpg', 'School sanitation block', 437, 256),
    ('community', 'community-01.jpg', "Women's meeting", 720, 526),
    ('community', 'community-02.jpg', 'Village gathering', 477, 222),
    ('community', 'community-03.jpg', "Women's group meeting", 720, 338),
    ('community', 'community-04.jpg', 'Awards received by the Trust', 720, 558),
]

GAL_JS = r"""
(()=>{const sec=document.querySelector('.gsec');if(!sec)return;sec.classList.add('js');sec.dataset.f='all';
const G=[...sec.querySelectorAll('.pgrp')],chips=[...sec.querySelectorAll('.fchips button')],rm=matchMedia('(prefers-reduced-motion:reduce)').matches;
G.forEach(g=>g.querySelectorAll('.ph').forEach((p,k)=>p.style.setProperty('--k',k%12)));
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){io.unobserve(e.target);e.target.classList.add('in')}}),{threshold:.05});G.forEach(g=>io.observe(g));
const setF=(f,scroll)=>{sec.dataset.f=f;chips.forEach(c=>c.classList.toggle('on',c.dataset.f===f));
 G.forEach(g=>{const s=f==='all'||g.dataset.g===f;g.classList.toggle('hide',!s);g.classList.remove('in');if(s)io.observe(g)});
 const on=chips.find(c=>c.dataset.f===f);if(on)on.scrollIntoView({block:'nearest',inline:'center',behavior:rm?'auto':'smooth'});
 if(scroll){const t=sec.querySelector('.fchips');scrollTo({top:t.getBoundingClientRect().top+scrollY-70,behavior:rm?'auto':'smooth'})}
 try{history.replaceState(null,'',f==='all'?location.pathname:'#'+f)}catch(e){}};
chips.forEach(c=>c.onclick=()=>setF(c.dataset.f,true));
sec.querySelectorAll('.seeall').forEach(b=>b.onclick=()=>setF(b.dataset.f,true));
const h=location.hash.slice(1);if(h&&G.some(g=>g.dataset.g===h))setF(h,true);
const lb=document.querySelector('.lbx'),im=lb.querySelector('img'),cap=lb.querySelector('.lcap'),cnt=lb.querySelector('.lcnt'),tag=lb.querySelector('.ltag');let L=[],at=0;
im.onload=()=>im.classList.add('in');
const show=i=>{at=(i+L.length)%L.length;const p=L[at];im.classList.remove('in');im.src=p.getAttribute('href');if(im.complete)im.classList.add('in');im.alt=p.dataset.cap;
 cap.textContent=p.dataset.cap;tag.textContent=p.dataset.g;cnt.textContent=(at+1)+' / '+L.length;[1,-1].forEach(d=>{(new Image).src=L[(at+d+L.length)%L.length].getAttribute('href')})};
const open=p=>{L=[...p.closest('.pgrp').querySelectorAll('.ph')];lb.classList.add('on');lb.setAttribute('aria-hidden','false');document.body.style.overflow='hidden';show(L.indexOf(p))};
const close=()=>{lb.classList.remove('on');lb.setAttribute('aria-hidden','true');document.body.style.overflow=''};
sec.querySelectorAll('.ph').forEach(p=>p.onclick=e=>{e.preventDefault();open(p)});
lb.querySelector('.lp').onclick=()=>show(at-1);lb.querySelector('.ln').onclick=()=>show(at+1);lb.querySelector('.lx').onclick=close;
lb.onclick=e=>{if(e.target===lb||e.target.classList.contains('lstage'))close()};
addEventListener('keydown',e=>{if(!lb.classList.contains('on'))return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(at-1);if(e.key==='ArrowRight')show(at+1)});
let sx=null;lb.addEventListener('touchstart',e=>sx=e.touches[0].clientX,{passive:true});lb.addEventListener('touchend',e=>{if(sx===null)return;const d=e.changedTouches[0].clientX-sx;if(Math.abs(d)>50)show(d<0?at+1:at-1);sx=null});
const v=document.querySelector('.vwrap video'),snd=document.querySelector('.vwrap .snd');if(v&&!rm)new IntersectionObserver(([e])=>{if(e.isIntersecting)v.play().catch(()=>{});else v.pause()},{threshold:.4}).observe(v);if(v&&snd){snd.onclick=()=>{v.muted=false;v.currentTime=0;v.play().catch(()=>{})};v.addEventListener('volumechange',()=>snd.classList.toggle('gone',!v.muted))}
})();
"""

def gallery_body():
    count = lambda k: sum(1 for p in PHOTOS if p[0] == k)
    chips = '<button class="on" data-f="all">All projects <small>%d</small></button>' % len(PHOTOS) + "".join(
        '<button data-f="%s">%s <small>%d</small></button>' % (k, E(t), count(k)) for k, t, _, _ in GROUPS)
    secs = ""
    for k, t, link, intro in GROUPS:
        ps = [p for p in PHOTOS if p[0] == k]
        tiles = "".join('<a class="ph%s" href="img/gal/%s" data-cap="%s" data-g="%s"><img src="img/gal/t/%s" alt="%s" width="%d" height="%d" loading="lazy"><span class="cap2">%s</span></a>'
                        % (" extra" if i >= 6 else "", n, E(c), E(t), n, E(c), w, h, E(c)) for i, (_, n, c, w, h) in enumerate(ps))
        more = '<button class="seeall" type="button" data-f="%s">See all %d photos →</button>' % (k, len(ps)) if len(ps) > 6 else ""
        secs += (f'<div class="pgrp" id="g-{k}" data-g="{k}"><div class="pgh"><div><h2>{E(t)}</h2><p>{E(intro)}</p></div>'
                 f'<div class="pgl"><span>{len(ps)} photos</span><a href="{link}">About this project →</a></div></div><div class="pgrid">{tiles}</div>{more}</div>')
    video = ('<section class="vsec"><div class="wrap"><div class="vhead"><div><div class="kick">Story video · Kutch Jal Mandir Abhiyan</div><h2>From dry beds to full tanks</h2>'
             '<p>How Kutch&#8217;s villages bring their old tanks back to life – a 75-second story with voice-over, made from our own field photos.</p></div>'
             '<a class="more" href="p-kutch-jal-mandir-abhiyan.html">About Jal Mandir Abhiyan →</a></div>'
             '<div class="vwrap"><video controls muted playsinline loop preload="none" poster="video/jal-mandir-story-poster.jpg">'
             '<source src="video/jal-mandir-story.mp4" type="video/mp4"></video><button class="snd" type="button">&#128266; Sound on</button></div></div></section>')
    lbx = ('<div class="lbx" aria-hidden="true"><button class="lx" type="button" aria-label="Close">&times;</button><button class="lp" type="button" aria-label="Previous photo">&#8249;</button>'
           '<figure class="lstage"><img alt=""><figcaption><span class="lcnt"></span><b class="lcap"></b><span class="ltag"></span></figcaption></figure>'
           '<button class="ln" type="button" aria-label="Next photo">&#8250;</button></div>')
    return (hero_page("Gallery", "Photos and video from our projects across Kutch, grouped by project.", "g03") + video +
            f'<section class="gsec"><div class="wrap"><div class="fchips">{chips}</div>{secs}</div></section>{lbx}<script>{GAL_JS}</script>')

# ---- Contact page: photo + floating form, 5 offices ----
OFFICES = [
    ("Head office", "Administrative office, Bhuj", "102, Kaushik Apartment, Bhanushali Nagar, Bhuj – Kutch, Gujarat 370001", "Kaushik Apartment Bhanushali Nagar Bhuj Kutch 370001", "Bhuj (HQ)", 15),
    ("Registered office", "Kothara", "At Kothara, Taluka Abdasa – Kutch", "Kothara Abdasa Kutch Gujarat", "Kothara", 13),
    ("Field centre", "Samriddhi Krishi Seva Kendra", "At Nani Khakhar, Taluka Mandvi – Kutch", "Nani Khakhar Mandvi Kutch Gujarat", "Nani Khakhar", 13),
    ("Field centre", "Wel Netrutva Krishi Seva Kendra", "At Nani Nagalpar, Taluka Anjar – Kutch", "Nani Nagalpar Anjar Kutch Gujarat", "Nani Nagalpar", 13),
    ("Field centre", "Khadir Vistar Vikas Kendra", "At Ratanpar (Khadir), Taluka Bhachau – Kutch", "Ratanpar Khadir Bhachau Kutch Gujarat", "Ratanpar", 12),
]
ICON = {
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/><path d="m22 6-10 7L2 6"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
}
CONTACT_JS = r"""
(()=>{const f=document.getElementById('cf');if(!f)return;const card=document.querySelector('.cx-card');
const rules={'your-name':v=>v.trim().length>=2||'Please enter your name',
 'your-email':v=>/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim())||'Please enter a valid email address',
 'your-phone':v=>{const d=v.replace(/\D/g,'');return d.length===10||(d.length===12&&d.startsWith('91'))||'Please enter a 10-digit phone number'},
 'your-message':v=>true};
const fields=[...f.querySelectorAll('input,textarea')];
const check=(el,show)=>{const r=rules[el.name](el.value),ok=r===true,b=el.closest('.fl');b.classList.toggle('ok',ok&&el.value.trim()!=='');if(show||ok)b.classList.toggle('bad',!ok);b.querySelector('.err').textContent=b.classList.contains('bad')?r:'';return ok};
fields.forEach(el=>{el.addEventListener('input',()=>check(el,false));el.addEventListener('blur',()=>{if(el.value.trim())check(el,true)})});
f.onsubmit=e=>{e.preventDefault();let first=null;fields.forEach(el=>{if(!check(el,true)&&!first)first=el});
 if(first){first.focus();card.classList.remove('shake');void card.offsetWidth;card.classList.add('shake');return}
 const v=n=>f[n].value.trim();card.querySelector('.nm').textContent=v('your-name').split(' ')[0];card.classList.add('sending');
 setTimeout(()=>{location.href='mailto:kfffdt@gmail.com?subject='+encodeURIComponent('Website enquiry from '+v('your-name'))+'&body='+encodeURIComponent(v('your-message')+'\n\nName: '+v('your-name')+'\nEmail: '+v('your-email')+'\nPhone: '+v('your-phone'));card.classList.add('sent')},1500)};
card.querySelector('.again').onclick=()=>{f.reset();f.querySelectorAll('.fl').forEach(b=>{b.classList.remove('ok','bad');b.querySelector('.err').textContent=''});card.classList.remove('sending','sent');f.querySelector('input').focus()};
document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>{document.querySelectorAll('.map .tabs button')[+b.dataset.tab].click();document.querySelector('.map').scrollIntoView({behavior:'smooth',block:'center'})});
})();
"""

def contact_body():
    from urllib.parse import quote_plus
    def fl(name, label, typ="text", area=False):
        el = (f'<textarea id="{name}" name="{name}" rows="5" maxlength="2000" placeholder=" "></textarea>' if area else
              f'<input id="{name}" name="{name}" type="{typ}" placeholder=" " autocomplete="{ {"your-name": "name", "your-email": "email", "your-phone": "tel"}.get(name, "off") }">')
        return f'<div class="fl">{el}<label for="{name}">{label}</label><i class="okmark"></i><span class="err" aria-live="polite"></span></div>'
    p1, p2 = PHONE1.replace(" ", ""), PHONE2.replace(" ", "")
    hero = (f'<section class="cx"><img src="img/gal/jal-12.jpg" alt="">'
            '<div class="cx-intro"><div class="kick" style="color:#f0c46f">Contact us</div><h1>Let\'s talk.</h1><p>Questions, partnerships, CSR or a field visit – write to us and the team will get back to you.</p></div>'
            '<div class="cx-card"><div class="cx-stack">'
            '<form id="cf" class="cx-form" novalidate><h2>Send us a message</h2>'
            f'<div class="fr">{fl("your-name", "Name *")}{fl("your-email", "Email *", "email")}</div>{fl("your-phone", "Phone No. *", "tel")}{fl("your-message", "Message", area=True)}'
            '<button class="btn send" type="submit">Send Message</button></form>'
            '<div class="cx-done" aria-live="polite"><svg viewBox="0 0 90 90"><circle cx="45" cy="45" r="40"/><path d="M27 46l12 12 24-26"/></svg>'
            f'<h2>Thank you, <span class="nm"></span>!</h2><p>Your email app has opened with your message filled in – press <b>Send</b> there to reach us.</p>'
            f'<p class="small">No email app? Write to <a href="mailto:{MAIL}">{MAIL}</a> or call <a href="tel:{p1}">{PHONE1}</a>.</p>'
            '<button class="btn ghost again" type="button">Send another message</button></div></div>'
            '<div class="splash" aria-hidden="true"><svg viewBox="0 0 40 52"><path fill="#5fa8d3" d="M20 2C20 2 4 22 4 33a16 16 0 0 0 32 0C36 22 20 2 20 2z"/></svg><i></i><i></i><i></i></div></div>'
            f'<div class="cx-chips"><a href="tel:{p1}">{ICON["phone"]}{PHONE1}</a><a href="tel:{p2}">{ICON["phone"]}{PHONE2}</a><a href="mailto:{MAIL}">{ICON["mail"]}{MAIL}</a>'
            f'<a href="#offices">{ICON["pin"]}Bhuj – Kutch</a><span>{ICON["clock"]}Mon–Sat 9:00–18:00 · Sunday closed</span></div>{WAVE("#f7f1e3")}</section>')
    maps = ["https://maps.google.com/maps?q=%s&z=%d&output=embed" % (quote_plus(q), z) for _, _, _, q, _, z in OFFICES]
    cards = "".join(
        f'<div class="off reveal{" hq" if i == 0 else ""}" style="transition-delay:{i * 0.08:.2f}s"><span class="tag">{E(t)}</span><h3>{E(n)}</h3><p>{E(a)}</p>'
        f'<div class="acts"><button type="button" data-tab="{i}">Show on map</button><a href="https://www.google.com/maps/dir/?api=1&amp;destination={quote_plus(q)}" target="_blank" rel="noopener">Directions ↗</a></div></div>'
        for i, (t, n, a, q, _, _) in enumerate(OFFICES))
    tabs = "".join('<button class="%s" type="button" data-src="%s">%s</button>' % ("on" if i == 0 else "", u, E(o[4])) for i, (o, u) in enumerate(zip(OFFICES, maps)))
    offices = (f'<section id="offices"><div class="wrap"><div class="sh reveal"><div><div class="kick">Visit us</div><h2 style="margin:0">Our offices across Kutch</h2>'
               f'<p style="margin:.5em 0 0;color:var(--muted)">Head office in Bhuj, registered office at Kothara and three field centres serving farmers and herders.</p></div></div>'
               f'<div class="offices">{cards}</div>'
               f'<div class="map reveal" style="margin-top:28px"><div class="tabs">{tabs}</div><iframe src="{maps[0]}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Office map"></iframe></div>'
               '<p style="color:var(--muted);font-size:.88rem;margin-top:10px">Field-centre pins point to the village; call ahead before visiting.</p></div></section>')
    return hero + offices + "<script>" + CONTACT_JS + "</script>"

# ---- Home: partners section (logos from the original site, list from the Legal page) ----
FUNDING_LOGOS = [("aarti-foundation-eng", "Aarti Foundation"), ("kutch-nav-nirman-abhiyan-logo", "Kutch Nav Nirman Abhiyan"),
    ("wasmo-logo", "WASMO – Water and Sanitation Management Organisation"), ("ministry-of-rural-development-logo", "Ministry of Rural Development, Government of India"),
    ("mitsu-logo", "Mitsu"), ("le-shark-logo", "Le Shark"), ("reliance-foundation-logo", "Reliance Foundation"), ("powerica-logo", "Powerica"),
    ("galaxy-supplier-logo", "Galaxy Surfactants"), ("welspun-foundation-for-health-knowledge", "Welspun Foundation for Health & Knowledge"),
    ("hmel-logo", "HMEL – HPCL-Mittal Energy"), ("adani-foundation-logo", "Adani Foundation"), ("cgpl-logo", "CGPL – Coastal Gujarat Power Limited"),
    ("tpcdt-logo", "TPCDT – Tata Power Community Development Trust"), ("concern-india-logo", "Concern India Foundation")]
IMPL_LOGOS = [("setu-logo", "Setu Abhiyan"), ("gss-logo", "Shri Gram Swaraj Sangh"), ("logo-bt", "Shri Bhojay Sarvodaya Trust"), ("satvik-web-logo", "Satvik")]
ALL_SUPPORTERS = ["Ministry of Rural Development, GoI", "Ministry of Wasteland Development, GoI", "Ministry of Water Resources, GoG", "Castrol Oil India",
    "Water & Sanitation Management Organisation", "Kutch Nav Nirman Abhiyan", "National Dairy Development Board – NDDB", "Indian Immunological Laboratory – IIL",
    "Tata Power", "Coastal Gujarat Power Limited", "Aarti Foundation, Mumbai", "Concern India Foundation, Mumbai", "Adani Foundation", "HPCL Mittal Foundation",
    "Welspun Foundation", "Galaxy Surfactants Pvt Ltd", "Indian Military – Bhuj Station", "Mitsu Foundation", "Bhojay Sarvodaya Trust", "SPM Foundation"]

def partners_html():
    card = lambda f, n, hidden=False: '<div class="pl"%s title="%s"><img src="img/partners/%s.png" alt="%s" loading="lazy"></div>' % (' aria-hidden="true"' if hidden else "", E(n), f, "" if hidden else E(n))
    track = "".join(card(f, n) for f, n in FUNDING_LOGOS) + "".join(card(f, n, True) for f, n in FUNDING_LOGOS)
    impl = "".join('<div class="pi reveal" style="transition-delay:%.2fs"><div class="pi-logo"><img src="img/partners/%s.png" alt="" loading="lazy"></div><b>%s</b></div>' % (i * .1, f, E(n)) for i, (f, n) in enumerate(IMPL_LOGOS))
    chips = "".join('<span style="--i:%d">%s</span>' % (i, E(n)) for i, n in enumerate(ALL_SUPPORTERS))
    return ('<section class="alt-bg partners"><div class="wrap">'
            '<div class="sh reveal"><div><div class="kick">Supporters</div><h2 style="margin:0">Funding &amp; implementing partners</h2>'
            '<p style="margin:.5em 0 0;color:var(--muted);max-width:560px">Government bodies, foundations and CSR partners who have worked with the Trust across Kutch.</p></div>'
            '<div class="pstats"><div><b data-count="20">0</b><span>supporting agencies</span></div><div><b data-count="15">0</b><span>funding partners</span></div><div><b data-count="4">0</b><span>implementing partners</span></div></div></div>'
            '<div class="plabel reveal"><span>Funding partners</span><small>Hover to pause</small></div>'
            f'<div class="marquee reveal"><div class="mq-track">{track}</div></div>'
            '<div class="plabel reveal"><span>Implementing partners</span></div>'
            f'<div class="pimpl">{impl}</div>'
            f'<details class="allsup reveal"><summary><span>View all 20 supporting agencies</span><i></i></summary><div class="supchips">{chips}</div></details>'
            '</div></section>')

# ---- Latest updates (news, events, milestones, media) ----
# To add an update: put a new dict at the TOP of this list and run  python3 build_new.py
#   date: "YYYY-MM-DD" for sorting (None if unknown)   when: what visitors see
#   type: story | milestone | event | media             img: card image under new/img (no .jpg)
#   clip: newspaper clipping under new/img/updates (media posts)   link/link_label: optional button
UPDATES = [
    dict(slug="story-video-dry-beds-to-full-tanks", date="2026-11-21", when="Nov 2026", type="story", source="KFFFDT",
         title="New story video: From dry beds to full tanks", img="updates/story-video",
         summary="A 75-second film, with voice-over, on how Kutch's villages bring their old tanks back to life – made from our own field photos.",
         body=["Kutch gets just 312 mm of rain a year, on about 13 days, and roughly 70% of it runs off to the sea. Our new short film follows one Kutch Jal Mandir Abhiyan story from a cracked, dry tank bed to a full village tank.",
               "It shows how each village decides together, how the project funds the excavator while villagers bring their own tractors, and what changes when the monsoon arrives."],
         link="gallery.html", link_label="Watch the video"),
    dict(slug="jal-mandir-332-tanks", date="2024-12-31", when="2024", type="milestone", source="Project profile 2012–2024",
         title="Kutch Jal Mandir Abhiyan: 332 village tanks revived", img="gal/jal-14",
         summary="Between 2012 and 2024, 332 traditional village tanks were revived, adding 8,835.93 lakh litres of water storage.",
         body=["Since 2012 the Kutch Jal Mandir Abhiyan has revived 332 existing storage tanks (Jal Mandirs) with community participation, increasing water storage capacity by 8,835.93 lakh litres.",
               "The total project expenditure was ₹525.32 lakh: ₹297.49 lakh came as project support and ₹227.83 lakh as the villagers' own contribution in the form of tractors – about 43% of the cost.",
               "Every site needs a Gram Panchayat resolution and people's participation. Excavated silt is used to strengthen existing bunds and for agriculture."],
         link="p-kutch-jal-mandir-abhiyan.html", link_label="See the project profile"),
    dict(slug="monsoon-2024-aerial-views", date="2024-09-02", when="Aug – Sep 2024", type="event", source="Drone survey",
         title="Monsoon 2024: village tanks seen from the air", img="gal/aerial-01",
         summary="Drone photos taken in August and September 2024 show village tanks across our working area holding monsoon water.",
         body=["In August and September 2024 we photographed village tanks from the air after the monsoon rains.",
               "The aerial views show tanks, embankments and the surrounding farmland – a record of how much water the revived structures hold after the rains."],
         link="gallery.html#aerial", link_label="View the aerial photos"),
    dict(slug="mann-ki-baat-jal-mandir", date="2022-03-31", when="31 Mar 2022", type="media", source="Kutchmitra",
         title="Jal Mandir mentioned in the Prime Minister's 'Mann Ki Baat'", img="updates/kutchmitra-2022-mann-ki-baat", clip="kutchmitra-2022-mann-ki-baat",
         summary="Kutchmitra reported that Prime Minister Narendra Modi spoke about rainwater harvesting in 'Mann Ki Baat' and mentioned Jal Mandirs for village ponds.",
         body=["Kutchmitra (Main Edition, 31 March 2022, page 10) reported that in 'Mann Ki Baat' the Prime Minister gave special emphasis to rainwater harvesting and mentioned Jal Mandirs for village ponds.",
               "The report notes that folk singer Lal Rambhiya's 'Jal Mandir Dayra' programmes had raised awareness in hundreds of Kutch villages, and that in Kantisen Shroff's centenary year Kutch Nav Nirman Abhiyan resolved to revive 100 Jal Mandirs with about 45% people's participation.",
               "At the time, work on 66 Jal Mandirs in 10 talukas of Kutch was complete, with campaign head Jayesh Lalka guiding the effort."]),
    dict(slug="world-water-day-2022-article", date="2022-03-22", when="World Water Day 2022", type="media", source="Article by Jayesh Lalka",
         title="World Water Day 2022: Jal Mandir Abhiyan – protecting Kutch's water culture", img="updates/world-water-day-2022-article", clip="world-water-day-2022-article",
         summary="On World Water Day 2022, our Managing Trustee Jayesh Lalka wrote about how villages, donors and panchayats are reviving Kutch's traditional tanks.",
         body=["For World Water Day 2022, Jayesh Lalka – Managing Trustee & Director of the Trust – wrote a newspaper article titled 'Jal Mandir Abhiyan: a commendable effort to protect our water culture'.",
               "The article describes how the campaign grew with the support of villagers, donors and gram panchayats across Kutch, and calls on village leaders to join it. The full article (in Gujarati) is shown below."]),
    dict(slug="anmol-beej-rath-launch", date=None, when="", type="media", source="Sandesh",
         title="Anmol Beej Rath sets out from Nani Khakhar", img="updates/sandesh-anmol-beej-rath", clip="sandesh-anmol-beej-rath",
         summary="Sandesh reported the launch of the Anmol Beej Rath to promote native (desi) seeds in 26 villages of Mandvi and Mundra talukas.",
         body=["Sandesh reported that Samriddhi Krishi Seva Kendra at Nani Khakhar (Mandvi taluka) – through the Bio Resource Centre, Anmol Beej Bank and Pashupalak Mitra – started promoting native seeds in 26 villages of Mandvi and Mundra talukas with the Anmol Beej Rath.",
               "Native-seed distribution centres were started at Nani Khakhar, Kathda, Bag, Gundiyali and Faradi (Mandvi taluka), Lodai (Bhuj), Dador (Nakhatrana), Siyot (Lakhpat) and Ratanpar (Khadir)."],
         link="p-agriculture-development.html", link_label="Agriculture programme"),
    dict(slug="brucellosis-vaccination-mundra", date=None, when="", type="media", source="Divya Bhaskar",
         title="Brucellosis vaccination for livestock in 11 villages of Mundra", img="updates/bhaskar-brucellosis-vaccination", clip="bhaskar-brucellosis-vaccination",
         summary="Divya Bhaskar reported a vaccination drive to protect dairy animals from brucellosis in 11 villages, with the support of Adani Foundation and other organisations.",
         body=["Divya Bhaskar reported that, under Adani Foundation's CSR programme in Mundra, dairy animals in 11 villages were being vaccinated against brucellosis – a bacterial disease that can cause abortion in cattle and buffaloes and can also spread to people.",
               "The work is carried out by Kutch Fodder Fruit & Forest Development Trust with the National Dairy Development Board, Kutch Nav Nirman Abhiyan and other organisations. According to the report, the programme has run since 2012 and more than 45,000 female animals have been vaccinated."],
         link="p-animal-health-care.html", link_label="Animal health care"),
    dict(slug="pabasari-jal-mandir-kumbhardi", date=None, when="", type="event", source="Newspaper report",
         title="Pabasari Jal Mandir revival begins at Kumbhardi, Bhachau", img="updates/pabasari-kumbhardi-jal-mandir", clip="pabasari-kumbhardi-jal-mandir",
         summary="Work to deepen and clean the Pabasari tank at Kumbhardi village began with support from Aarti Foundation, Setu Abhiyan and the Gram Panchayat.",
         body=["Revival of the Pabasari Jal Mandir (village tank) at Kumbhardi in Bhachau taluka began as part of the Kutch Jal Mandir Abhiyan, with support from Aarti Foundation.",
               "The idea to deepen the tank and clear the surrounding waste and babool came from the village sarpanch, Devshibhai Rabari. Setu Abhiyan and the Gram Panchayat supported the work, and villagers contributed tractors. Jayesh Lalka praised the community's participation."],
         link="p-kutch-jal-mandir-abhiyan.html", link_label="Kutch Jal Mandir Abhiyan"),
]
UTYPE = {"story": "Story", "milestone": "Milestone", "event": "Event", "media": "In the media"}
UPDATES.sort(key=lambda u: u["date"] or "0000", reverse=True)

def ucard(u, cls="ucard reveal", delay=0.0):
    tag = UTYPE[u["type"]] + (" · " + E(u["source"]) if u["type"] == "media" else "")
    date = '<span class="udate">%s</span>' % E(u["when"]) if u["when"] else ""
    return (f'<a class="{cls}" data-t="{u["type"]}" href="u-{u["slug"]}.html" style="transition-delay:{delay:.2f}s">'
            f'<div class="uimg{" clip" if u.get("clip") else ""}"><img src="img/{u["img"]}.jpg" alt="" loading="lazy">{date}</div>'
            f'<div class="ub"><span class="utag t-{u["type"]}">{tag}</span><h3>{E(u["title"])}</h3><p>{E(u["summary"])}</p><span class="more">Read more →</span></div></a>')

def updates_home():
    cards = "".join(ucard(u, delay=i * .1) for i, u in enumerate(UPDATES[:3]))
    return ('<section><div class="wrap"><div class="sh reveal"><div><div class="kick">What&#8217;s new</div><h2 style="margin:0">Latest updates</h2>'
            '<p style="margin:.5em 0 0;color:var(--muted)">News, events, milestones and media coverage from our work across Kutch.</p></div>'
            f'<a class="more" href="updates.html">All updates →</a></div><div class="ugrid">{cards}</div></div></section>')

UPD_JS = r"""
(()=>{const sec=document.querySelector('.upd');if(!sec)return;const chips=[...sec.querySelectorAll('.fchips button')],cards=[...sec.querySelectorAll('.ugrid .ucard')],feat=sec.querySelector('.ufeat');
const set=f=>{chips.forEach(c=>c.classList.toggle('on',c.dataset.f===f));sec.dataset.f=f;let k=0;
 cards.forEach(c=>{const show=(f==='all'&&!c.classList.contains('dup'))||(f!=='all'&&c.dataset.t===f);c.classList.toggle('hide',!show);if(show){c.style.setProperty('--k',k++);c.classList.remove('pop');void c.offsetWidth;c.classList.add('pop')}});
 if(feat)feat.classList.toggle('hide',f!=='all')};
chips.forEach(c=>c.onclick=()=>set(c.dataset.f));})();
"""

def updates_page():
    f = UPDATES[0]
    feat = (f'<a class="ufeat reveal" href="u-{f["slug"]}.html"><div class="ufi"><img src="img/{f["img"]}.jpg" alt=""><span class="unew">Latest</span></div>'
            f'<div class="uft"><span class="utag t-{f["type"]}">{UTYPE[f["type"]]}</span><time>{E(f["when"])}</time><h2>{E(f["title"])}</h2><p>{E(f["summary"])}</p><span class="btn">Read more</span></div></a>')
    counts = {t: sum(1 for u in UPDATES if u["type"] == t) for t in UTYPE}
    chips = '<button class="on" data-f="all">All <small>%d</small></button>' % len(UPDATES) + "".join(
        '<button data-f="%s">%s <small>%d</small></button>' % (t, n, counts[t]) for t, n in UTYPE.items() if counts[t])
    cards = ucard(f, "ucard dup hide") + "".join(ucard(u, delay=(i % 3) * .1) for i, u in enumerate(UPDATES[1:]))
    return (hero_page("Latest updates", "News, events, milestones and media coverage from our work across Kutch.", "gal/jal-12") +
            f'<section class="upd" data-f="all"><div class="wrap">{feat}<div class="fchips">{chips}</div><div class="ugrid">{cards}</div>'
            '<p class="unote">Have news or a press clipping about our work? <a href="contact.html">Send it to us</a>.</p></div></section><script>' + UPD_JS + '</script>')

def update_page(i):
    u = UPDATES[i]
    newer, older = (UPDATES[i - 1] if i > 0 else None), (UPDATES[i + 1] if i + 1 < len(UPDATES) else None)
    meta = f'<div class="umeta"><span class="utag t-{u["type"]}">{UTYPE[u["type"]]}</span>' + (f'<time>{E(u["when"])}</time>' if u["when"] else "") + f'<span>{E(u["source"])}</span></div>'
    body = "".join("<p>%s</p>" % E(x) for x in u["body"])
    clip = (f'<figure class="uclip"><a href="img/updates/{u["clip"]}.jpg" target="_blank" rel="noopener"><img src="img/updates/{u["clip"]}.jpg" alt="Newspaper clipping: {E(u["title"])}" loading="lazy"></a>'
            f'<figcaption>Original clipping{" – " + E(u["source"]) if u["source"] else ""} (Gujarati). Click to open full size.</figcaption></figure>') if u.get("clip") else ""
    btn = f'<p style="margin-top:26px"><a class="btn" href="{u["link"]}">{E(u["link_label"])}</a></p>' if u.get("link") else ""
    nav = '<div class="unav">' + (f'<a href="u-{newer["slug"]}.html"><small>← Newer</small>{E(newer["title"])}</a>' if newer else "<span></span>") + \
          (f'<a class="r" href="u-{older["slug"]}.html"><small>Older →</small>{E(older["title"])}</a>' if older else "<span></span>") + '</div>'
    hero_img = None if u.get("clip") else u["img"]
    return hero_page(u["title"], u["summary"], hero_img) + (f'<section><div class="wrap" style="max-width:820px">{meta}<div class="ubody">{body}</div>{clip}{btn}'
            f'<p style="margin-top:34px"><a class="more" href="updates.html">← All updates</a></p>{nav}</div></section>')

# ---- Rain section: lives on the Water Conservation page (was on home) ----
RAIN_SECTION = f"""<section class="alt-bg"><div class="wrap"><div class="sub-h reveal"><div class="kick">The problem we solve</div><h2>Where does Kutch's rain go?</h2><p>Just 312 mm falls in about 13 rainy days a year – and about 70% of it runs off to the sea.</p></div>
<div class="opt reveal"><button class="on" data-v="v1">Where the rain goes</button><button data-v="v2">When it rains</button></div>
<div class="rain-box reveal" id="rb"><div class="views">
<div class="view on" id="v1"><div class="dots">{DOTS}</div>
<div class="bigs"><div><b data-count="70" data-suffix="%">0</b><span>runs off to the sea</span></div><div class="g"><b data-count="30" data-suffix="%">0</b><span>stays on the land – what tanks &amp; check dams hold</span></div></div>
<div class="legend"><span><b style="background:#5fa8d3"></b>every drop = 1% of the rain</span><button class="replay" type="button">↻ Replay</button></div></div>
<div class="view" id="v2"><div class="yr">{YR}</div>
<div class="bigs"><div class="g"><b data-count="13">0</b><span>rainy days in a typical year</span></div><div><b data-count="352">0</b><span>days with no rain at all</span></div></div>
<div class="legend"><span><b style="background:#2f86c0"></b>rainy day (monsoon; dates illustrative)</span><span><b style="background:#d9cdb0"></b>dry day · one row per month</span><button class="replay" type="button">↻ Replay</button></div></div>
</div>
<div class="tankcol">{TANK}<div class="tbig">+<b data-count="8835">0</b> <small>lac litres</small></div><p style="margin:.2em 0 .6em"><b style="color:var(--green)"><span data-count="332">0</span> village tanks</b> revived since 2012</p>
<p style="color:var(--muted);font-size:.95rem">Every Jal Mandir gets a name plate with the donor's name.</p>
<a class="btn" href="contact.html">Fund a Jal Mandir tank</a> &nbsp; <a class="btn ghost" href="p-kutch-jal-mandir-abhiyan.html">See the project</a></div></div></div></section>"""


# ---- Home: Fodder, Fruit & Forest – what the Trust's name stands for ----
# Figures come from the Agriculture & fodder rows of ACT and the agriculture program page.
def _sky(gid, cloud_x):
    return (f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4ecd6"/><stop offset="1" stop-color="#fbf7ec"/></linearGradient></defs>'
            f'<rect width="400" height="300" fill="url(#{gid})"/><circle class="sun" cx="334" cy="58" r="24" fill="#f2c46b"/>'
            f'<g transform="translate({cloud_x} 52)" opacity=".9"><g class="cl"><ellipse rx="28" ry="9" fill="#fff"/><ellipse cx="12" cy="-7" rx="15" ry="10" fill="#fff"/></g></g>')


def _fodder():
    import random
    R = random.Random(7)
    rows = [(170, .5, 15, "#a3c78b"), (194, .65, 13, "#86b571"), (220, .8, 12, "#66a05e"), (248, .95, 10, "#4f8f55"), (282, 1.12, 9, "#3f7a4f")]
    g = []
    for r, (y, sc, n, col) in enumerate(rows):
        step = 400 / n
        for c in range(n):
            x = step * (c + .5) + R.uniform(-step * .25, step * .25)
            g.append('<g transform="translate(%.0f %.0f) scale(%s)"><g class="gr" style="--d:%.2fs"><path class="bl" style="--s:%.2fs;fill:%s" d="M-2 0Q-6-12-13-22Q-5-15 1 0ZM-2.4 0Q-2-20 0-36Q2-20 2.4 0ZM-1 0Q5-13 13-20Q4-10 2.5 0ZM-3 0Q-9-8-15-11Q-7-6-1 0Z"/></g></g>'
                     % (x, y + R.uniform(-3, 3), sc, .25 + r * .22 + c * .045, R.uniform(0, 2), col))
    bales = "".join('<g transform="translate(%d %d)"><g class="pp" style="--d:%.1fs"><rect x="-27" y="-24" width="54" height="26" rx="9" fill="#e4b65c" stroke="#b8862f" stroke-width="2"/><path d="M-14-24v26M0-24v26M14-24v26" stroke="#c4913a" stroke-width="1.6"/></g></g>' % b
                    for b in [(320, 288, 2.5), (368, 292, 2.7), (344, 268, 2.9)])
    return ('<svg class="sc" viewBox="0 0 400 300" role="img" aria-label="Grass growing row by row across a field, with fodder bales">' + _sky("skF", 80)
            + '<path class="gnd" d="M0 162Q90 142 200 154T400 150V300H0Z" fill="#e2cf9f" style="--g:#bcd597"/>' + "".join(g) + bales + "</svg>")


FRUITS = [(-60, -110), (-35, -142), (-10, -104), (15, -150), (40, -120), (62, -98), (-48, -172), (5, -182), (38, -176), (-20, -128), (25, -94), (-72, -88), (72, -132), (-4, -160), (52, -150), (-38, -96)]


def _fruit():
    orchard = "".join('<g transform="translate(%d %d) scale(%s)"><g class="gw" style="--d:%.2fs"><rect x="-2.5" y="-16" width="5" height="17" rx="2" fill="#8a6440"/><circle cy="-25" r="13" fill="#7fab69"/><circle cx="7" cy="-21" r="9" fill="#70a05e"/></g></g>' % t
                      for t in [(30, 160, .8, .2), (78, 154, .7, .3), (118, 158, .6, .45), (276, 156, .6, .4), (322, 152, .75, .35), (366, 158, .85, .25)])
    fruits = "".join('<g transform="translate(%d %d)"><g class="fp" style="--d:%.2fs"><circle r="8" fill="#e98b2a"/><circle cx="-2.6" cy="-2.6" r="2.4" fill="#f8c37f"/><path d="M0-8q4-5 9-4q-3 5-9 4" fill="#6fae5a"/></g></g>' % (x, y, .9 + k * .12)
                     for k, (x, y) in enumerate(FRUITS))
    tree = ('<g transform="translate(170 272)"><path d="M-12 0Q-7-46-5-92L5-92Q8-46 14 0Z" fill="#7a5634"/><path d="M-3-60Q-26-80-40-96M3-70Q24-88 40-100" stroke="#7a5634" stroke-width="7" stroke-linecap="round" fill="none"/>'
            '<g class="cn"><circle cy="-130" r="62" fill="#3f7a4f"/><circle cx="-54" cy="-104" r="42" fill="#4a8756"/><circle cx="54" cy="-106" r="44" fill="#4a8756"/><circle cx="-28" cy="-166" r="38" fill="#4f8d5b"/><circle cx="30" cy="-164" r="40" fill="#4f8d5b"/></g>'
            + fruits + "</g>")
    basket = ('<g transform="translate(300 274)">' + "".join('<g transform="translate(%d %d)"><g class="fp" style="--d:%.1fs"><circle r="8" fill="#e98b2a"/><circle cx="-2.6" cy="-2.6" r="2.4" fill="#f8c37f"/></g></g>' % f for f in [(-12, -24, 4.1), (12, -24, 4.3), (0, -28, 4.5)])
              + '<path d="M-30-22H30L22 4H-22Z" fill="#c4904f" stroke="#9c6b33" stroke-width="2" stroke-linejoin="round"/><path d="M-27-12H27M-25-2H25" stroke="#9c6b33" stroke-width="1.5"/></g>')
    drop = '<g transform="translate(232 174)"><g class="fd"><circle r="8" fill="#e98b2a"/><circle cx="-2.6" cy="-2.6" r="2.4" fill="#f8c37f"/></g></g>'
    return ('<svg class="sc" viewBox="0 0 400 300" role="img" aria-label="Fruit appearing on a tree, one dropping into a basket">' + _sky("skR", 250)
            + '<path class="gnd" d="M0 168Q120 148 220 162T400 158V300H0Z" fill="#e2cf9f" style="--g:#bcd597"/>' + orchard + tree + drop + basket + "</svg>")


def _tree(x, y, sc, d, tall, back):
    c1, c2 = ("#8ab474", "#7aa865") if back else ("#3f7a4f", "#4f8d5b")
    if tall:
        shape = f'<rect x="-3.5" y="-46" width="7" height="48" rx="3" fill="#7a5634"/><ellipse cy="-78" rx="20" ry="40" fill="{c1}"/><ellipse cx="-6" cy="-68" rx="11" ry="25" fill="{c2}"/>'
    else:
        shape = f'<rect x="-4" y="-38" width="8" height="40" rx="3" fill="#7a5634"/><circle cy="-60" r="30" fill="{c1}"/><circle cx="-22" cy="-45" r="20" fill="{c2}"/><circle cx="22" cy="-47" r="21" fill="{c2}"/>'
    return f'<g transform="translate({x} {y}) scale({sc})"><g class="gw" style="--d:{d:.2f}s">{shape}</g></g>'


def _forest():
    back = [(40, 168, .55, 0), (118, 160, .62, 1), (205, 166, .5, 0), (292, 158, .6, 1), (372, 166, .55, 0)]
    front = [(78, 264, 1, 0), (170, 274, 1.15, 1), (262, 266, .95, 0), (348, 272, 1.05, 1)]
    trees = "".join(_tree(x, y, sc, .3 + k * .14, tall, True) for k, (x, y, sc, tall) in enumerate(back))
    seeds = trees_f = ""
    for k, (x, y, sc, tall) in enumerate(front):
        d = .9 + k * .28
        seeds += f'<circle class="sd" cx="{x}" cy="{y - 4}" r="4.5" fill="#8a6a45" style="--d:{d - .8:.2f}s"/>'
        trees_f += _tree(x, y, sc, d, tall, False)
    birds = '<g transform="translate(0 92)"><g class="bd"><path d="M0 0q6-7 12 0q6-7 12 0"/><path d="M30-12q5-6 10 0q5-6 10 0"/></g></g>'
    return ('<svg class="sc" viewBox="0 0 400 300" role="img" aria-label="Seed balls falling and trees growing across dry land">' + _sky("skT", 120)
            + '<path class="gnd" d="M0 172Q100 148 210 164T400 156V300H0Z" fill="#e6d6ab" style="--g:#c6dba3"/>' + trees
            + '<path class="gnd" d="M0 236Q120 214 240 232T400 226V300H0Z" fill="#dcc794" style="--g:#a9c987"/>' + seeds + trees_f + birds + "</svg>")


FFF_ICON = {
    "fodder": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M12 21V9M12 21c-1-5-4-8-8-9M12 21c1-5 4-8 8-9M12 13c-1-3-3-5-5-6M12 13c1-3 3-5 5-6"/></svg>',
    "fruit": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="14" r="7"/><path d="M12 7c0-2 1-4 3-4M12 7c-2-2-5-2-6 0"/></svg>',
    "forest": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22v-6M6 16h12l-6-7zM8 11h8l-4-7z"/></svg>',
}
FFF_TABS = [
    dict(key="fodder", label="Fodder", scene=_fodder, tag="Fodder security", h="Green fodder for the dry months",
         p="Livestock needs fodder all year, even when the rain fails. We give fodder seeds to rainfed farmers and Napier (NB21) green-fodder cuttings to irrigated farmers, develop village grazing land (gauchar) and help families build fodder storage sheds.",
         big=("1421800", 0, "green-fodder cuttings given to farmers"),
         mini=[("1090", "farmers in the fodder security project"), ("170", "acres of grazing land developed"), ("278", "farmers with fodder storage sheds")],
         links=[("p-agriculture-development.html", "See agriculture &amp; fodder")]),
    dict(key="fruit", label="Fruit", scene=_fruit, tag="Horticulture", h="Fruit trees on dry farms",
         p="Fruit plants give rainfed farms a crop that lasts for years. Alongside saplings, farmers get soil and water testing at our Krishi Seva Kendra and chemical-free farming support from the Bio Resource Centre.",
         big=("21725", 0, "fruit plants promoted with farmers"),
         mini=[("1870", "farmers supported by the Bio Resource Centre"), ("1400", "farmers in agriculture extension"), ("1", "Krishi Seva Kendra with a soil &amp; water lab")],
         links=[("p-agriculture-development.html", "See agriculture")]),
    dict(key="forest", label="Forest", scene=_forest, tag="Tree plantation", h="Bringing the trees back",
         p="The Trust began in 1989 because trees were disappearing from Kutch, and rainfall and harvests suffered with them. Today we plant trees with villages and with the Indian Army in Bhuj, and broadcast seed balls on open land.",
         big=("8", 0, "tree-plantation projects"),
         mini=[("26.25", "Rs. lacs invested in plantation", 2), ("=1989", "the year we began, to bring the green back"), ("=Seed balls", "broadcast on open grazing land")],
         links=[("about.html", "Why we began"), ("p-agriculture-development.html", "See tree plantation")]),
]


def fff_section():
    btns = views = ""
    for i, t in enumerate(FFF_TABS):
        on = i == 0
        btns += '<button type="button" role="tab" id="ft-%s" aria-controls="f-%s" aria-selected="%s" data-v="f-%s"%s>%s%s</button>' % (
            t["key"], t["key"], "true" if on else "false", t["key"], ' class="on"' if on else "", FFF_ICON[t["key"]], t["label"])
        minis = ""
        for m in t["mini"]:
            val, label = m[0], m[1]
            if val.startswith("="):
                minis += '<div><b class="%s">%s</b><span>%s</span></div>' % ("t" if not val[1:].isdigit() else "", val[1:], label)
            else:
                minis += '<div><b data-count="%s"%s>0</b><span>%s</span></div>' % (val, ' data-dec="%d"' % m[2] if len(m) > 2 else "", label)
        links = "".join('<a class="btn%s" href="%s">%s</a>' % ("" if k == 0 else " ghost", h, l) for k, (h, l) in enumerate(t["links"]))
        n, dec, blabel = t["big"]
        views += ('<div class="view%s" id="f-%s" role="tabpanel" aria-labelledby="ft-%s"><div class="scene">%s</div>'
                  '<div class="finfo"><div class="ftag">%s</div><h3>%s</h3><p>%s</p>'
                  '<div class="fbig"><b data-count="%s"%s>0</b><span>%s</span></div><div class="fmini">%s</div>'
                  '<div class="fact">%s<button class="replay" type="button">↻ Replay</button></div></div></div>') % (
            " on" if on else "", t["key"], t["key"], t["scene"](), t["tag"], t["h"], t["p"], n, ' data-dec="%d"' % dec if dec else "", blabel, minis, links)
    return ('<section class="alt-bg fff" id="fff"><div class="wrap"><div class="sub-h reveal"><div class="kick">What our name stands for</div><h2>Fodder, Fruit &amp; Forest</h2>'
            "<p>Three words in our name, three kinds of work that keep Kutch's villages, livestock and land green.</p></div>"
            '<div class="opt reveal" role="tablist" aria-label="Fodder, fruit and forest">' + btns + "</div>"
            '<div class="views reveal">' + views + "</div></div></section>")


FFF = fff_section()


# ---- Explore Kutch in 3D (three.js scene in new/js/explore.js, vendored three.js r187 in new/vendor/three) ----
# lat/lon place each program on the real map (taluka level where the site or news names a place; "shown near" otherwise).
X3D_ICON = {
    "jal": '<path d="M12 3c3 4 6 7.5 6 11a6 6 0 0 1-12 0c0-3.5 3-7 6-11z"/>',
    "water": '<path d="M3 9c2-2 4-2 6 0s4 2 6 0 4-2 6 0M3 15c2-2 4-2 6 0s4 2 6 0 4-2 6 0"/>',
    "drink": '<path d="M4 9h9a3 3 0 0 1 3 3v2M8 9V5h5M16 18v2M4 6v6"/>',
    "fodder": '<path d="M12 21V9M12 21c-1-5-4-8-8-9M12 21c1-5 4-8 8-9M12 13c-1-3-3-5-5-6M12 13c1-3 3-5 5-6"/>',
    "fruit": '<circle cx="12" cy="14" r="7"/><path d="M12 7c0-2 1-4 3-4M12 7c-2-2-5-2-6 0"/>',
    "forest": '<path d="M12 22v-6M6 16h12l-6-7zM8 11h8l-4-7z"/>',
    "animal": '<path d="M7 8h10l1 5a6 6 0 0 1-12 0zM4 6l3 2M20 6l-3 2M10 15h4"/>',
    "rebuild": '<path d="M4 11l8-6 8 6v9H4zM10 20v-5h4v5"/>',
    "school": '<path d="M4 5h6a2 2 0 0 1 2 2v12a2 2 0 0 0-2-2H4zM20 5h-6a2 2 0 0 0-2 2v12a2 2 0 0 1 2-2h6z"/>',
    "centres": '<path d="M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>',
    # item types
    "t-project": '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3"/>',
    "t-event": '<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M8 3v4M16 3v4M4 10h16"/>',
    "t-centre": '<path d="M4 21V8l8-4 8 4v13M9 21v-5h6v5M3 21h18"/>',
}
X3D_SVG = lambda k: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % X3D_ICON[k]

# Programs: one pin each on the 3D map. lat/lon is where the program's pin (and its 3D props) sit.
X3D = [
    dict(id="jal", short="Jal Mandir", kick="Kutch Jal Mandir Abhiyan", title="Village tanks, revived together", lat=23.343, lon=70.263, where="332 village tanks across Kutch, 2012–2024", color="#3b97cf",
         stat=["332", "village tanks revived since 2012"],
         text="Old village tanks are desilted with the community: the project pays for an excavator, villagers bring their tractors, and the silt goes back to strengthen bunds and fields.",
         facts=[["8,835 lac L", "water storage added"], ["43%", "of the cost carried by villagers"]], link="p-kutch-jal-mandir-abhiyan.html", link_label="Open Jal Mandir"),
    dict(id="water", short="Check dams", kick="Water conservation", title="Holding the rain where it falls", lat=22.993, lon=69.026, where="Watershed works in Abdasa and across Kutch", color="#2f86c0",
         stat=["705", "water structures built"],
         text="Storage and percolation tanks, check dams, farm ponds and recharge wells keep rainwater in the village and push it back into the ground.",
         facts=[["141", "storage tanks"], ["134", "farm ponds"]], link="p-water-conservation.html", link_label="Open water conservation"),
    dict(id="drink", short="Drinking water", kick="Drinking water · WASMO", title="Water schemes run by the village", lat=23.350, lon=69.265, where="Abdasa, Nakhatrana and Lakhpat talukas", color="#4aa7bf",
         stat=["37", "villages with community-run water schemes"],
         text="Under WASMO, village committees build and manage their own drinking-water schemes, with roof-top rainwater harvesting at schools.",
         facts=[["₹620.82 lac", "invested in village schemes"], ["9", "roof-top harvesting systems"]], link="p-decentralized-drinking-water-supply-scheme-project.html", link_label="Open drinking water"),
    dict(id="fodder", short="Fodder", kick="Fodder security", title="Green fodder for village cattle", lat=22.879, lon=69.516, where="Farmers across Kutch; grazing-land pilot at Nani Khakhar", color="#5f9e4f",
         stat=["14,21,800", "Napier (NB21) green-fodder cuttings"],
         text="Fodder seeds for rainfed farmers, Napier cuttings for irrigated farms, grazing land for the village herd and sheds to store dry fodder.",
         facts=[["1,090", "farmers in the fodder project"], ["170 acres", "grazing land developed"]], link="p-agriculture-development.html", link_label="Open agriculture"),
    dict(id="fruit", short="Fruit & seeds", kick="Agriculture development", title="Orchards, seeds and healthy soil", lat=22.843, lon=69.275, where="Krishi Seva Kendras and native-seed centres across Kutch", color="#e08326",
         stat=["21,725", "fruit plants promoted"],
         text="Anmol Beej Bank – Gujarat's largest traditional seed bank – keeps local seeds alive, and the Bio Resource Centre helps farmers move to chemical-free farming.",
         facts=[["1,870", "farmers at the Bio Resource Centre"], ["26", "villages on the Beej Rath route"]], link="p-agriculture-development.html", link_label="Open agriculture"),
    dict(id="forest", short="Forest", kick="Tree plantation", title="Bringing the trees back", lat=23.30, lon=69.73, where="With villages, and with the Indian Army in Bhuj", color="#3f7a4f",
         stat=["8", "tree-plantation projects"],
         text="The Trust began in 1989 because trees were disappearing from Kutch. We plant with villages and with the Indian Army in Bhuj, and broadcast seed balls on open land.",
         facts=[["₹26.25 lac", "invested in plantation"], ["1989", "the year we began"]], link="about.html", link_label="Why we began"),
    dict(id="animal", short="Animal health", kick="Animal health care", title="Healthy herds, healthy families", lat=22.839, lon=69.725, where="Pashupalak Mitra and livestock centres; 11 villages in Mundra", color="#a4492b",
         stat=["45,000+", "animals vaccinated against brucellosis in Mundra since 2012"],
         text="Pashupalak Mitra centres vaccinate female calves, test milk and blood for Brucella and run awareness camps with pastoral families.",
         facts=[["3", "livestock service centres"], ["NDDB", "among our animal-health partners"]], link="p-animal-health-care.html", link_label="Open animal health"),
    dict(id="rebuild", short="Rebuilding", kick="Disaster management", title="After the 2001 earthquake", lat=23.17, lon=70.12, where="Earthquake relief and a village rebuilt", color="#c98a2b",
         stat=["134", "permanent houses built"],
         text="After the 2001 earthquake the Trust put up temporary shelters, then rebuilt a village with a school, community centre, drinking water, sanitation and solar street lights.",
         facts=[["174", "temporary shelters"], ["24", "houses repaired and retrofitted"]], link="p-natural-disaster-management.html", link_label="Open disaster relief"),
    dict(id="school", short="Schools", kick="Primary education", title="A school where there was none", lat=23.66, lon=68.86, where="Lakhpat taluka and the edge of the Rann", color="#7d63b0",
         stat=["2", "schools for children the system missed"],
         text="Reaching the unreached: a Van Shala (forest school) at Kalara Wandh in Lakhpat, and a school for the children of salt-pan workers at Kadol, on the edge of the Rann.",
         facts=[["Van Shala", "forest school, Lakhpat"], ["Agariya Shala", "for salt-pan workers' children"]], link="p-primary-education-for-unreached-community.html", link_label="Open education"),
    dict(id="centres", short="Our centres", kick="Offices & field centres", title="Where the Trust works from", lat=23.130, lon=68.940, where="Registered at Kothara, run from Bhuj, field centres in three talukas", color="#2e5b3b",
         stat=["200+", "villages in seven talukas of Kutch"],
         text="Field centres bring farm advice, native seeds and animal care close to the villages: Samriddhi Krishi Seva Kendra at Nani Khakhar, Wel Netrutva Krishi Seva Kendra at Nani Nagalpar and Khadir Vistar Vikas Kendra at Ratanpar.",
         facts=[["1989", "registered at Kothara, Abdasa"], ["5", "offices and field centres"]], link="contact.html", link_label="Addresses & contact"),
]
for _d in X3D:
    _d["icon"] = _d["id"]

# Projects, events and centres. They appear on the map only after you pick their program.
# To add one, copy an entry and change it:
#   id        unique, lower-case, used in links: explore.html#<program>/<id>
#   program   list of program ids above (an item can belong to more than one)
#   type      "project", "event" or "centre"
#   short     label on the map pin (keep it under ~22 characters)
#   place, taluka, lat, lon   village and position (approx=True shows "approximate location")
#   when      date text, e.g. "28 March 1989" ("" if undated); month 1–12 offers "See Kutch in <month>"
#   text      one or two sentences;  img/img_alt, link/link_label are optional
# Coordinates: OpenStreetMap (Nominatim). Kalara Wandh is not on OSM, so it is approximate.
X3D_ITEMS = [
    dict(id="pabasari-kumbhardi", program=["jal"], type="event", short="Pabasari tank", title="Pabasari Jal Mandir revival", place="Kumbhardi", taluka="Bhachau", lat=23.343, lon=70.263,
         text="Work to deepen and clean the Pabasari tank began with support from Aarti Foundation, Setu Abhiyan and the Gram Panchayat. The idea came from the sarpanch, Devshibhai Rabari, and villagers brought their own tractors.",
         img="img/updates/pabasari-kumbhardi-jal-mandir.jpg", img_alt="Newspaper report on the Pabasari Jal Mandir revival", link="u-pabasari-jal-mandir-kumbhardi.html", link_label="Read the news report"),
    dict(id="lathedi-watershed", program=["water"], type="project", short="Lathedi watershed", title="Watershed project, Lathedi", place="Lathedi", taluka="Abdasa", lat=22.993, lon=69.026,
         text="Watershed works and check dams keep monsoon water in the village; after good rains the check dam at Lathedi overflows.",
         img="img/gal/watershed-04.jpg", img_alt="Check dam overflowing at Lathedi", link="gallery.html#watershed", link_label="Watershed photos"),
    dict(id="piyoni", program=["water"], type="project", short="Piyoni", title="Water held at Piyoni", place="Piyoni", taluka="Abdasa", lat=23.278, lon=69.182,
         text="Part of the Trust's watershed and check-dam work: water still standing at Piyoni after the monsoon.",
         img="img/gal/watershed-02.jpg", img_alt="Piyoni after the monsoon", link="gallery.html#watershed", link_label="Watershed photos"),
    dict(id="wasmo-abdasa", program=["drink"], type="project", short="Abdasa villages", title="Village water schemes, Abdasa", place="Villages of Abdasa taluka", taluka="Abdasa", lat=23.261, lon=68.827, approx=True,
         text="Under WASMO, each village water committee (pani samiti) plans, builds and runs its own drinking-water scheme, with water-quality training at committee level."),
    dict(id="wasmo-nakhatrana", program=["drink"], type="project", short="Nakhatrana villages", title="Village water schemes, Nakhatrana", place="Villages of Nakhatrana taluka", taluka="Nakhatrana", lat=23.350, lon=69.265, approx=True,
         text="Community-managed drinking water and sanitation under WASMO, including awareness for total sanitation (Nirmal Gram)."),
    dict(id="wasmo-lakhpat", program=["drink"], type="project", short="Lakhpat villages", title="Village water schemes, Lakhpat", place="Villages of Lakhpat taluka", taluka="Lakhpat", lat=23.635, lon=68.901, approx=True,
         text="Decentralised drinking-water schemes in Lakhpat taluka, run by the village water committees, with roof-top rainwater harvesting at schools."),
    dict(id="gauchar-nani-khakhar", program=["fodder", "forest"], type="project", short="Gauchar pilot", title="Grazing-land (gauchar) pilot", place="Nani Khakhar", taluka="Mandvi", lat=22.879, lon=69.516,
         text="The village's common grazing land was prepared, sown with fodder seed by seed drill and planted with trees – a pilot for gauchar development in Kutch.",
         img="img/gal/gauchar-02.jpg", img_alt="Seed drill on grazing land", link="gallery.html#gauchar", link_label="Gauchar photos"),
    dict(id="ksk-nani-khakhar", program=["fruit", "animal", "centres"], type="centre", short="Samriddhi KSK", title="Samriddhi Krishi Seva Kendra", place="Nani Khakhar", taluka="Mandvi", lat=22.879, lon=69.516,
         text="Field centre for farmers and herders: the Bio Resource Centre for chemical-free farming, the Anmol Beej Bank of traditional seeds, and Pashupalak Mitra animal care with a livestock service centre.",
         link="p-agriculture-development.html", link_label="Agriculture programme"),
    dict(id="beej-rath", program=["fruit"], type="event", short="Beej Rath sets out", title="Anmol Beej Rath sets out", place="Nani Khakhar", taluka="Mandvi", lat=22.879, lon=69.516,
         text="The Anmol Beej Rath set out to promote native (desi) seeds in 26 villages of Mandvi and Mundra talukas, opening native-seed centres along the way.",
         img="img/updates/sandesh-anmol-beej-rath.jpg", img_alt="Sandesh report on the Anmol Beej Rath", link="u-anmol-beej-rath-launch.html", link_label="Read the news report"),
    dict(id="seed-kathda", program=["fruit"], type="centre", short="Seed centre · Kathda", title="Native-seed centre, Kathda", place="Kathda", taluka="Mandvi", lat=22.843, lon=69.275,
         text="One of the native-seed distribution centres opened with the Anmol Beej Rath, bringing traditional seeds back to rainfed farms."),
    dict(id="seed-bag", program=["fruit"], type="centre", short="Seed centre · Bag", title="Native-seed centre, Bag", place="Bag", taluka="Mandvi", lat=22.850, lon=69.401,
         text="One of the native-seed distribution centres opened with the Anmol Beej Rath, bringing traditional seeds back to rainfed farms."),
    dict(id="seed-gundiyali", program=["fruit"], type="centre", short="Seed centre · Gundiyali", title="Native-seed centre, Gundiyali", place="Gundiyali", taluka="Mandvi", lat=22.836, lon=69.419,
         text="One of the native-seed distribution centres opened with the Anmol Beej Rath, bringing traditional seeds back to rainfed farms."),
    dict(id="seed-faradi", program=["fruit"], type="centre", short="Seed centre · Faradi", title="Native-seed centre, Faradi", place="Faradi", taluka="Mandvi", lat=22.941, lon=69.515,
         text="One of the native-seed distribution centres opened with the Anmol Beej Rath, bringing traditional seeds back to rainfed farms."),
    dict(id="seed-lodai", program=["fruit"], type="centre", short="Seed centre · Lodai", title="Native-seed centre, Lodai", place="Lodai", taluka="Bhuj", lat=23.395, lon=69.890,
         text="A native-seed distribution centre in Bhuj taluka, part of the Anmol Beej Bank network."),
    dict(id="seed-dador", program=["fruit"], type="centre", short="Seed centre · Dador", title="Native-seed centre, Dador", place="Dador", taluka="Nakhatrana", lat=23.492, lon=69.383,
         text="A native-seed distribution centre in Nakhatrana taluka, part of the Anmol Beej Bank network."),
    dict(id="seed-siyot", program=["fruit"], type="centre", short="Seed centre · Siyot", title="Native-seed centre, Siyot", place="Siyot", taluka="Lakhpat", lat=23.733, lon=68.903,
         text="A native-seed distribution centre in Lakhpat taluka, in the far west of Kutch."),
    dict(id="seed-ratanpar", program=["fruit"], type="centre", short="Seed centre · Ratanpar", title="Native-seed centre, Ratanpar (Khadir)", place="Ratanpar (Khadir)", taluka="Bhachau", lat=23.860, lon=70.364,
         text="A native-seed distribution centre on Khadir island, in the middle of the Great Rann."),
    dict(id="ksk-nani-nagalpar", program=["fruit", "animal", "centres"], type="centre", short="Wel Netrutva KSK", title="Wel Netrutva Krishi Seva Kendra", place="Nani Nagalpar", taluka="Anjar", lat=23.107, lon=69.997,
         text="Field centre for farmers in Anjar taluka, with a Pashupalak Mitra animal-health centre.", link="p-agriculture-development.html", link_label="Agriculture programme"),
    dict(id="army-plantation", program=["forest"], type="project", short="With the Indian Army", title="Tree plantation with the Indian Army", place="Bhuj", taluka="Bhuj", lat=23.247, lon=69.668, approx=True,
         text="Plantation drives with the Indian Army in Bhuj, alongside community plantation and seed-ball broadcasting on open land.", link="p-agriculture-development.html", link_label="Agriculture programme"),
    dict(id="brucellosis-mundra", program=["animal"], type="project", short="Brucellosis · Mundra", title="Brucellosis vaccination in 11 villages", place="Villages of Mundra taluka", taluka="Mundra", lat=22.839, lon=69.725, approx=True, when="Since 2012",
         text="With Adani Foundation's CSR programme and the National Dairy Development Board, dairy animals in 11 villages are vaccinated against brucellosis – more than 45,000 female animals so far.",
         img="img/updates/bhaskar-brucellosis-vaccination.jpg", img_alt="Divya Bhaskar report on the brucellosis vaccination", link="u-brucellosis-vaccination-mundra.html", link_label="Read the news report"),
    dict(id="lsc-kothara", program=["animal"], type="centre", short="Livestock centre", title="Livestock service centre, Kothara", place="Kothara", taluka="Abdasa", lat=23.130, lon=68.940,
         text="One of the Trust's three livestock service centres, with Nani Khakhar and Ratanpar (Khadir)."),
    dict(id="khadir-kendra", program=["animal", "centres"], type="centre", short="Khadir Vistar Vikas Kendra", title="Khadir Vistar Vikas Kendra", place="Ratanpar (Khadir)", taluka="Bhachau", lat=23.860, lon=70.364,
         text="Field centre for the Khadir area in the Great Rann, with one of the Trust's three livestock service centres."),
    dict(id="earthquake-2001", program=["rebuild"], type="event", short="Rebuilt village", title="Rebuilding after the earthquake", place="A village in Kutch (location to be confirmed)", taluka="", lat=23.17, lon=70.12, approx=True, when="From 26 January 2001", month=1,
         text="Relief materials, a survey of damaged houses and temporary shelters came first; then, with Castrol India, 134 permanent houses, a primary school, community centre, drinking-water scheme, full sanitation and solar street lights.",
         link="p-natural-disaster-management.html", link_label="Disaster management"),
    dict(id="van-shala", program=["school"], type="project", short="Van Shala", title="Van Shala, Kalara Wandh", place="Kalara Wandh", taluka="Lakhpat", lat=23.66, lon=68.86, approx=True,
         text="A forest school (Van Shala) that brings primary education to children at Kalara Wandh; the Trust works as its support agency.",
         img="img/gal/edu-02.jpg", img_alt="Van Shala classroom", link="p-primary-education-for-unreached-community.html", link_label="Education programme"),
    dict(id="agariya-shala", program=["school"], type="project", short="Agariya Shala", title="Agariya Shala, Kadol", place="Kadol", taluka="Bhachau", lat=23.473, lon=70.292,
         text="A non-registered school for the children of Agariyas – the salt-pan workers of the Rann – at Kadol village.", link="p-primary-education-for-unreached-community.html", link_label="Education programme"),
    dict(id="head-office", program=["centres"], type="centre", short="Head office", title="Administrative office, Bhuj", place="Bhanushali Nagar, Bhuj", taluka="Bhuj", lat=23.247, lon=69.668,
         text="102, Kaushik Apartment, Bhanushali Nagar, Bhuj – Kutch, Gujarat 370001.", link="contact.html", link_label="Contact"),
    dict(id="kothara-1989", program=["centres"], type="event", short="Where we began", title="Where the Trust began", place="Kothara", taluka="Abdasa", lat=23.130, lon=68.940, when="28 March 1989", month=3,
         text="The Trust was registered on 28 March 1989 at village Kothara in Abdasa taluka, where its registered office still is.", link="about.html", link_label="About the Trust"),
]
X3D_TYPES = {"project": "Project", "event": "Event", "centre": "Centre"}


def _check_x3d():
    import os, re
    ids, progs = set(), {d["id"] for d in X3D}
    for it in X3D_ITEMS:
        where = "X3D_ITEMS[%s]" % it.get("id")
        assert re.fullmatch(r"[a-z0-9-]+", it["id"]) and it["id"] not in ids, where + ": id must be unique, lower-case letters, digits and -"
        ids.add(it["id"])
        assert it["program"] and all(p in progs for p in it["program"]), where + ": unknown program"
        assert it["type"] in X3D_TYPES, where + ": type must be project, event or centre"
        assert 22.6 < it["lat"] < 24.8 and 68.0 < it["lon"] < 71.3, where + ": lat/lon is outside Kutch"
        assert 1 <= it.get("month", 1) <= 12, where + ": month must be 1–12"
        if it.get("img"):
            assert os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "new", it["img"])), where + ": image not found " + it["img"]

X3D_SEASON = {"Winter": "#5b7fd1", "Summer": "#e09a2f", "Monsoon": "#3b97cf", "Post-monsoon": "#6a9f4f"}
X3D_MONTHS = [
    ("January", "Jan", "Winter", "Cool, clear days. The Rann is white salt, Rann Utsav tents stand at Dhordo and migratory birds winter in Banni."),
    ("February", "Feb", "Winter", "Rabi crops ripen on irrigated farms and the village tanks slowly drop."),
    ("March", "Mar", "Summer", "The heat builds, the rabi harvest comes in and the last winter visitors leave."),
    ("April", "Apr", "Summer", "Hot, dry winds. Tanks run low and mango fruit sets in the orchards."),
    ("May", "May", "Summer", "The hottest month. Many tanks are dry – the time to desilt them before the rains."),
    ("June", "Jun", "Summer", "Kesar mangoes are picked, the first showers arrive and farmers get ready to sow."),
    ("July", "Jul", "Monsoon", "The monsoon reaches Kutch: kharif sowing begins and the tanks start to fill."),
    ("August", "Aug", "Monsoon", "The heart of the monsoon. The Rann floods and the land turns green."),
    ("September", "Sep", "Monsoon", "The rains taper off; tanks and check dams are full."),
    ("October", "Oct", "Post-monsoon", "Kharif harvest. The Rann still holds water and migratory birds begin to arrive."),
    ("November", "Nov", "Winter", "The Rann dries to white salt, Rann Utsav begins at Dhordo and rabi crops are sown."),
    ("December", "Dec", "Winter", "Cool and bright: the white Rann at its best, with cranes and flamingos in Banni and the Rann."),
]

X3D_CSS = """
.x3d{--hh:67px;position:relative;height:calc(100svh - var(--hh));min-height:520px;overflow:hidden;background:linear-gradient(#b9d6ea,#f3e4c4 70%);isolation:isolate}
.x3d>canvas{position:absolute;inset:0;width:100%!important;height:100%!important;display:block;touch-action:none;outline:none}
.xg{background:rgba(255,252,244,.6);-webkit-backdrop-filter:blur(20px) saturate(1.6);backdrop-filter:blur(20px) saturate(1.6);border:1px solid rgba(255,255,255,.72);box-shadow:inset 0 1px 0 rgba(255,255,255,.85),0 22px 50px -22px rgba(25,45,30,.5)}
.xtitle{position:absolute;left:22px;top:22px;z-index:6;max-width:330px;padding:16px 20px;border-radius:24px}
.xtitle{transition:padding .4s}.xtitle.mini{padding:12px 18px}.xtitle.mini h1{font-size:1.35rem;margin:.1em 0 0}.xtitle.mini p{display:none}
.xtitle .kick{margin:0}.xtitle h1{font:700 1.75rem/1.1 Fraunces,serif;margin:.15em 0 .35em;color:var(--ink)}.xtitle p{margin:0;font-size:.86rem;line-height:1.45;color:#4c584d}
.xpins{position:absolute;inset:0;z-index:4;pointer-events:none;overflow:hidden}
.xlabels{position:absolute;inset:0;z-index:3;pointer-events:none;overflow:hidden}
.xlab{position:absolute;left:0;top:0;white-space:nowrap;transition:opacity .4s;will-change:transform}.xlab.off{opacity:0}
.xlab.town,.xlab.peak{font:600 .74rem/1.1 Inter,sans-serif;color:#1d2a1f;text-shadow:0 0 3px #fff,0 0 7px rgba(255,255,255,.95);translate:-50% -4px}
.xlab.town:before{content:"";display:block;width:7px;height:7px;margin:0 auto 3px;border-radius:50%;background:#1d2a1f;box-shadow:0 0 0 2px #fff}
.xlab.peak{color:#5a3d22}.xlab.peak:before{content:"▲";display:block;text-align:center;font-size:.7rem;margin-bottom:1px}
.xlab.region{font:600 .78rem/1 Inter,sans-serif;letter-spacing:.22em;text-transform:uppercase;color:rgba(70,62,44,.72);translate:-50% -50%;text-shadow:0 0 8px rgba(255,255,255,.7)}
.xlab.water{font:italic 500 .92rem/1 Inter,sans-serif;letter-spacing:.06em;color:rgba(255,255,255,.88);translate:-50% -50%;text-shadow:0 1px 4px rgba(10,50,80,.45)}
.xlegend{display:flex;flex-wrap:wrap;gap:6px 12px;margin-top:10px;font-size:.73rem;color:#4c584d}.xlegend span{display:inline-flex;align-items:center;gap:5px}
.xlegend i{width:11px;height:11px;border-radius:3px;background:var(--s);border:1px solid rgba(0,0,0,.14)}.xlegend .bd i{width:16px;height:0;border:0;border-top:2px dashed #d4932f;border-radius:0}
.xcred{margin-top:9px;font-size:.64rem;line-height:1.4;color:#6b766c}.xtitle.mini .xlegend{display:none}.xtitle.mini .xcred{margin-top:4px}
.xpin{position:absolute;left:0;top:0;pointer-events:auto;display:flex;align-items:center;gap:7px;padding:5px 12px 5px 5px;border-radius:99px;border:1px solid rgba(255,255,255,.75);background:rgba(255,252,244,.74);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);font:600 .8rem/1 Inter,sans-serif;color:var(--ink);white-space:nowrap;cursor:pointer;transform-origin:50% 100%;box-shadow:0 10px 24px -12px rgba(0,0,0,.45);transition:opacity .3s,background .3s,box-shadow .3s;will-change:transform}
.xpin[hidden]{display:none}
.xpin i{width:26px;height:26px;border-radius:50%;display:grid;place-items:center;background:var(--c);color:#fff;flex:none}.xpin svg{width:15px;height:15px}
.xpin em{font-style:normal;min-width:20px;height:20px;padding:0 6px;margin:0 -5px 0 1px;border-radius:99px;background:color-mix(in srgb,var(--c) 16%,#fff);color:color-mix(in srgb,var(--c) 75%,#1d2a1f);font:700 .7rem/20px Inter,sans-serif;text-align:center}
.xpin:after{content:"";position:absolute;left:50%;top:100%;width:2px;height:calc(10px + var(--lift,0px));margin-left:-1px;background:linear-gradient(rgba(255,255,255,.95),rgba(255,255,255,.25))}
.xpin:hover,.xpin.on{background:#fff;box-shadow:0 0 0 4px color-mix(in srgb,var(--c) 35%,transparent),0 14px 30px -12px rgba(0,0,0,.5)}
.xpin.xi{gap:6px;padding:4px 10px 4px 4px;font-size:.74rem}.xpin.xi i{width:22px;height:22px}.xpin.xi svg{width:12px;height:12px}
.xpin.crowd{gap:0;padding:4px}.xpin.crowd span,.xpin.crowd em{display:none}
.xpin.pop{animation:xpop .6s cubic-bezier(.2,.8,.2,1.35) var(--d,0s) both}@keyframes xpop{from{opacity:0;scale:.3}}
.xpin.off{opacity:0;pointer-events:none}
.xpanel{position:absolute;right:22px;top:22px;z-index:7;width:min(380px,calc(100% - 44px));perspective:1100px;opacity:0;transform:translateX(26px) scale(.97);pointer-events:none;transition:opacity .45s,transform .6s cubic-bezier(.2,.8,.2,1)}
.xpanel.open{opacity:1;transform:none;pointer-events:auto}
.xp-in{position:relative;overflow:hidden auto;max-height:calc(100svh - var(--hh) - 158px);border-radius:30px;padding:20px 24px;transform:rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg));transition:transform .25s ease-out;scrollbar-width:thin}
.xp-in:before{content:"";position:absolute;right:-60px;top:-60px;width:200px;height:200px;border-radius:50%;background:radial-gradient(color-mix(in srgb,var(--c) 40%,transparent),transparent 70%);pointer-events:none}
.xpanel.swap .xp-body>*{animation:xswap .55s cubic-bezier(.2,.8,.2,1) both}.xpanel.swap .xp-body>:nth-child(2){animation-delay:.05s}.xpanel.swap .xp-body>:nth-child(3){animation-delay:.1s}.xpanel.swap .xp-body>:nth-child(4){animation-delay:.15s}.xpanel.swap .xp-body>:nth-child(5){animation-delay:.2s}.xpanel.swap .xp-body>:nth-child(n+6){animation-delay:.25s}
@keyframes xswap{from{opacity:0;transform:translateY(10px)}}
.xp-top{position:relative;display:flex;align-items:center;gap:10px;min-height:32px}
.xp-kick{font-weight:700;font-size:.74rem;letter-spacing:.13em;text-transform:uppercase;color:color-mix(in srgb,var(--c) 70%,#1d2a1f)}
.xp-back{display:none;align-items:center;gap:6px;max-width:62%;border:0;background:rgba(255,255,255,.65);border-radius:99px;padding:7px 13px 7px 9px;font:600 .8rem Inter,sans-serif;color:color-mix(in srgb,var(--c) 70%,#1d2a1f);cursor:pointer}
.xp-back span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.xp-back svg{width:15px;height:15px;flex:none}.xp-back:hover{background:#fff}
.xpanel.item .xp-back{display:inline-flex}.xpanel.item .xp-kick{display:none}
.xp-count{margin-left:auto;font-size:.78rem;color:var(--muted);font-variant-numeric:tabular-nums}
.xp-x{flex:none;width:32px;height:32px;border-radius:50%;border:0;background:rgba(0,0,0,.07);font-size:1.3rem;line-height:1;cursor:pointer;color:var(--ink)}.xp-x:hover{background:rgba(0,0,0,.13)}
.xp-title{position:relative;font:700 1.6rem/1.15 Fraunces,serif;margin:10px 0 12px;color:var(--ink)}
.xp-where{position:relative;display:flex;gap:8px;align-items:flex-start;margin:-4px 0 12px;font-size:.84rem;line-height:1.4;color:#4c584d}
.xp-where:before{content:"";flex:none;width:9px;height:9px;margin-top:4px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);background:var(--c)}
.xp-where em{font-style:normal;font-size:.72rem;padding:1px 8px;border-radius:99px;background:rgba(0,0,0,.06);white-space:nowrap}
.xp-stat{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;padding:12px 14px;border-radius:18px;background:rgba(255,255,255,.55);border:1px solid rgba(255,255,255,.85)}
.xp-stat b{font:700 2rem/1 Fraunces,serif;color:color-mix(in srgb,var(--c) 75%,#1d2a1f)}.xp-stat span{flex:1;min-width:140px;font-size:.86rem;color:#4c584d}
.xp-text{font-size:.92rem;line-height:1.55;color:#3d4a3f;margin:14px 0}
.xp-facts{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:16px}.xp-facts div{padding:10px 12px;border-radius:14px;background:rgba(255,255,255,.45);border:1px solid rgba(255,255,255,.75)}
.xp-facts b{display:block;font:700 1.1rem/1.2 Fraunces,serif;color:var(--ink)}.xp-facts span{display:block;font-size:.78rem;line-height:1.35;color:#5d6a5e}
.xp-list{margin:0 0 14px}
.xp-list h3{display:flex;align-items:center;gap:8px;margin:0 0 8px;font:700 .72rem/1 Inter,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:#4c584d}
.xp-list h3 b{min-width:20px;height:20px;padding:0 6px;border-radius:99px;background:var(--c);color:#fff;font-size:.7rem;line-height:20px;text-align:center;letter-spacing:0}
.xp-list ul{list-style:none;margin:0;padding:0;display:grid;gap:5px}
.xp-list button{display:flex;align-items:center;gap:10px;width:100%;padding:8px 10px;border:1px solid rgba(255,255,255,.8);border-radius:14px;background:rgba(255,255,255,.45);font:inherit;text-align:left;color:var(--ink);cursor:pointer;transition:background .2s,transform .2s}
.xp-list button:hover{background:#fff;transform:translateX(2px)}
.xp-list i,.xp-type i{flex:none;width:28px;height:28px;border-radius:9px;display:grid;place-items:center;background:var(--c);color:#fff}.xp-list svg,.xp-type svg{width:14px;height:14px}
.xp-list b{display:block;font-size:.86rem;line-height:1.25}.xp-list small{display:block;margin-top:2px;font-size:.75rem;line-height:1.3;color:#5d6a5e}
.xp-list .none{padding:10px 12px;border-radius:14px;background:rgba(255,255,255,.4);font-size:.84rem;color:#5d6a5e}
.xp-type{display:flex;align-items:center;gap:9px;margin-top:8px;font:700 .72rem/1.2 Inter,sans-serif;letter-spacing:.1em;text-transform:uppercase;color:color-mix(in srgb,var(--c) 70%,#1d2a1f)}
.xp-type span{font-weight:600;letter-spacing:.02em;text-transform:none;color:#5d6a5e;font-size:.8rem}
.xp-img{margin:0 0 4px;border-radius:18px;overflow:hidden;aspect-ratio:16/9;background:rgba(255,255,255,.45);border:1px solid rgba(255,255,255,.8)}.xp-img img{display:block;width:100%;height:100%;object-fit:cover}
.xp-month{display:inline-flex;align-items:center;gap:8px;margin:-4px 0 14px;padding:7px 13px;border:1px solid rgba(0,0,0,.1);border-radius:99px;background:rgba(255,255,255,.6);font:600 .8rem Inter,sans-serif;color:var(--ink);cursor:pointer}.xp-month:hover{background:#fff}.xp-month svg{width:15px;height:15px;color:var(--k)}
.xp-act{display:flex;gap:8px;align-items:center}
.xp-go{flex:1;text-align:center;background:var(--green);color:#fff;font-weight:600;padding:11px 16px;border-radius:99px;font-size:.9rem}.xp-go:hover{background:#244a30}
.xp-prev,.xp-next{border:1px solid rgba(0,0,0,.1);background:rgba(255,255,255,.6);border-radius:99px;padding:10px 14px;font:600 .88rem Inter,sans-serif;cursor:pointer;color:var(--ink)}.xp-prev:hover,.xp-next:hover{background:#fff}
.xdock{position:absolute;left:50%;bottom:18px;transform:translateX(-50%);z-index:7;width:max-content;display:flex;align-items:center;gap:4px;padding:7px;border-radius:26px;max-width:calc(100% - 24px)}
.xd-places{display:flex;gap:2px;min-width:0;overflow-x:auto;scrollbar-width:none}.xd-places::-webkit-scrollbar{display:none}
.xd-places button{position:relative;flex:none;display:flex;flex-direction:column;align-items:center;gap:5px;width:76px;padding:8px 4px 7px;border:0;border-radius:18px;background:transparent;font:600 .7rem/1.15 Inter,sans-serif;color:var(--ink);cursor:pointer;transition:background .25s}
.xd-places button i{width:34px;height:34px;border-radius:12px;display:grid;place-items:center;background:var(--c);color:#fff;box-shadow:0 6px 14px -6px var(--c);transition:transform .3s cubic-bezier(.2,.8,.2,1.4)}.xd-places svg{width:18px;height:18px}
.xd-places em{position:absolute;top:4px;left:calc(50% + 9px);min-width:17px;height:17px;padding:0 4px;border-radius:99px;background:#fff;color:var(--ink);font:700 .62rem/17px Inter,sans-serif;font-style:normal;text-align:center;box-shadow:0 0 0 1.5px var(--c)}
.xd-places button:hover{background:rgba(255,255,255,.55)}.xd-places button:hover i{transform:translateY(-3px) scale(1.06)}.xd-places button.on{background:#fff;box-shadow:0 6px 16px -10px rgba(0,0,0,.4)}
.xd-sep{flex:none;width:1px;align-self:stretch;margin:8px 4px;background:rgba(29,42,31,.15)}
.xd-tour,.xd-reset{flex:none;display:flex;align-items:center;gap:8px;height:48px;padding:0 14px;border:0;border-radius:18px;background:rgba(255,255,255,.5);font:600 .82rem Inter,sans-serif;color:var(--ink);cursor:pointer;transition:background .25s}
.xd-tour:hover,.xd-reset:hover{background:#fff}.xd-tour svg,.xd-reset svg{width:16px;height:16px}
.xd-tour[aria-pressed=true]{background:var(--green);color:#fff}
.xmonths{position:absolute;left:22px;bottom:104px;z-index:6;width:102px;padding:8px;border-radius:22px;transition:opacity .35s}
.xm-head{display:grid;grid-template-columns:1fr auto;align-items:center;column-gap:4px;padding:2px 2px 8px 8px}
.xm-lab{font:700 .6rem/1 Inter,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#6b766c}
.xm-season{grid-column:1/-1;margin-top:3px;font:700 .82rem/1.15 Inter,sans-serif;color:color-mix(in srgb,var(--k) 72%,#1d2a1f);transition:color .4s}
.xm-play{flex:none;width:30px;height:30px;border-radius:50%;border:0;background:rgba(255,255,255,.7);display:grid;place-items:center;color:var(--ink);cursor:pointer}.xm-play:hover{background:#fff}.xm-play svg{width:13px;height:13px}
.xm-play[aria-pressed=true]{background:var(--green);color:#fff}
.xm-list{position:relative;display:flex;flex-direction:column}
.xm-glide{position:absolute;left:0;right:0;top:0;height:calc(100% / 12);border-radius:12px;background:#fff;box-shadow:0 4px 12px -6px rgba(0,0,0,.35);transform:translateY(calc(var(--i) * 100%));transition:transform .45s cubic-bezier(.2,.8,.2,1.15)}
.xm-list button{position:relative;display:flex;align-items:center;gap:9px;height:29px;padding:0 10px;border:0;border-radius:12px;background:none;font:600 .8rem Inter,sans-serif;color:#4c584d;cursor:pointer;transition:color .25s}
.xm-list button:before{content:"";flex:none;width:4px;height:13px;border-radius:2px;background:var(--k);opacity:.5;transition:height .3s,opacity .3s}
.xm-list button:hover{color:var(--ink)}.xm-list button[aria-checked=true]{color:var(--ink)}.xm-list button[aria-checked=true]:before{opacity:1;height:17px}
.xm-list button:focus-visible{outline:2px solid var(--green);outline-offset:-2px}
.xtoast{position:absolute;left:50%;top:22px;z-index:8;transform:translate(-50%,-14px);opacity:0;padding:10px 18px;border-radius:22px;font-weight:600;font-size:.88rem;line-height:1.4;color:var(--ink);pointer-events:none;transition:opacity .4s,transform .5s cubic-bezier(.2,.8,.2,1);max-width:min(560px,calc(100% - 40px));text-align:center}
.xtoast.show{opacity:1;transform:translate(-50%,0)}.xtoast b{color:color-mix(in srgb,var(--k,#2e5b3b) 75%,#1d2a1f)}
.xload{position:absolute;inset:0;z-index:9;display:grid;place-content:center;justify-items:center;gap:14px;background:linear-gradient(#b9d6ea,#f3e4c4 70%);color:var(--green);font-weight:600;transition:opacity .9s,visibility 0s .9s}
.x3d.ready .xload{opacity:0;visibility:hidden}.xl-ring{width:44px;height:44px;border-radius:50%;border:3px solid rgba(46,91,59,.2);border-top-color:var(--green);animation:spin 1s linear infinite}
.xfall{display:none}
.x3d.nogl{height:auto;min-height:0;background:var(--sand2)}.x3d.nogl>:not(.xfall){display:none!important}
.x3d.nogl .xfall{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:16px;max-width:1180px;margin:0 auto;padding:44px 20px 64px}
.xf-head{grid-column:1/-1}.xf-head h1{font:700 2.2rem/1.1 Fraunces,serif;margin:.2em 0}.xf-head p{color:var(--muted)}
.xf-card{display:block;background:var(--card);border:1px solid var(--line);border-top:5px solid var(--c);border-radius:18px;padding:18px 20px;color:var(--ink)}
.xf-card h3{font:700 1.2rem/1.2 Fraunces,serif;margin:.3em 0}.xf-card p{font-size:.92rem;color:var(--muted);margin:.4em 0}.xf-card b{color:var(--green)}
.xf-where{font-size:.82rem!important;color:var(--ochre)!important}
.xf-items{margin:.6em 0 .8em;padding-left:1.1em;font-size:.86rem;color:var(--muted)}.xf-items li{margin:.25em 0}.xf-items b{color:var(--ink)}
@media(max-height:800px) and (min-width:761px){.xmonths{bottom:96px}.xm-list button{height:25px;font-size:.76rem}.xtitle:not(.mini) .xlegend{display:none}}
@media(max-width:760px){
.xtitle{left:12px;top:12px;right:12px;max-width:none;padding:12px 16px;border-radius:20px}.xlegend{display:none}.xcred{font-size:.6rem}.xlab.region,.xlab.water{font-size:.66rem}.xtitle h1{font-size:1.3rem;margin:.1em 0 0}.xtitle p{display:none}
.xpanel{left:12px;right:12px;top:auto;bottom:100px;width:auto;transform:translateY(24px)}.xpanel.open{transform:none}
.xp-in{padding:16px 18px;border-radius:24px;max-height:calc((100svh - var(--hh)) * .48)}.xpanel:not(.item) :is(.xp-stat,.xp-text,.xp-facts){display:none}.xp-img{aspect-ratio:2/1}.xtitle{transition:opacity .35s}.x3d.pan .xtitle{opacity:0;pointer-events:none}
.xp-title{font-size:1.3rem;margin:6px 0 8px}.xp-stat b{font-size:1.5rem}.xp-text{font-size:.86rem;margin:10px 0}.xp-facts{margin-bottom:12px}
.xpin span,.xpin em{display:none}.xpin,.xpin.xi{gap:0;padding:4px}.xpin.on span{display:inline}.xpin.on{gap:6px;padding-right:10px}
.xdock{left:10px;right:10px;bottom:10px;transform:none;max-width:none;width:auto}.xd-places{flex:1}
.xd-places button{width:62px;font-size:.64rem}.xd-places em{left:calc(50% + 7px)}.xd-tour span{display:none}.xd-tour,.xd-reset{padding:0 10px}
.xmonths{left:auto;right:8px;bottom:auto;top:50%;transform:translateY(-42%);width:auto;padding:5px;border-radius:18px}
.xm-head{display:flex;justify-content:center;padding:1px 0 5px}.xm-lab,.xm-season{display:none}.xm-play{width:28px;height:28px}
.xm-list button{height:25px;gap:5px;padding:0 8px 0 6px;font-size:.68rem}.xm-list button:before{width:3px;height:10px}.xm-list button[aria-checked=true]:before{height:13px}
.x3d.pan .xmonths{opacity:0;pointer-events:none}
.xtoast{top:auto;bottom:100px}
}
@media(prefers-reduced-motion:reduce){.xpanel,.xp-in,.xtoast,.xm-glide{transition:none}.xl-ring{animation:none}.xpin.pop{animation:none}}
"""


def explore_body():
    import json
    _check_x3d()
    n = {d["id"]: sum(d["id"] in it["program"] for it in X3D_ITEMS) for d in X3D}
    places = "".join('<button type="button" style="--c:%s" aria-current="false" aria-label="%s – %d on the map"><i>%s</i><span>%s</span><em aria-hidden="true">%d</em></button>'
                     % (d["color"], E(d["kick"]), n[d["id"]], X3D_SVG(d["icon"]), E(d["short"]), n[d["id"]]) for d in X3D)
    data = dict(programs=[dict(d, svg=X3D_SVG(d["icon"]), n=n[d["id"]]) for d in X3D],
                items=[dict(dict(approx=False, when="", month=0, taluka="", img="", img_alt="", link="", link_label=""), **it) for it in X3D_ITEMS],
                types={k: dict(label=v, svg=X3D_SVG("t-" + k)) for k, v in X3D_TYPES.items()},
                months=[dict(name=m, abbr=a, season=s, color=X3D_SEASON[s], text=t) for m, a, s, t in X3D_MONTHS])
    data = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    def fitems(pid):
        its = [it for it in X3D_ITEMS if pid in it["program"]]
        return '<ul class="xf-items">%s</ul>' % "".join('<li><b>%s</b> – %s%s</li>' % (E(it["title"]), E(it["place"]), (", " + E(it["taluka"]) + " taluka") if it.get("taluka") and it["taluka"] not in it["place"] else "") for it in its) if its else ""
    fall = "".join('<div class="xf-card" style="--c:%s"><div class="kick">%s</div><h3>%s</h3><p class="xf-where">%s</p><p><b>%s</b> %s</p><p>%s</p>%s<a class="more" href="%s">%s →</a></div>'
                   % (d["color"], E(d["kick"]), E(d["title"]), E(d["where"]), E(d["stat"][0]), E(d["stat"][1]), E(d["text"]), fitems(d["id"]), d["link"], E(d["link_label"])) for d in X3D)
    months = "".join('<button type="button" role="radio" aria-checked="false" tabindex="-1" style="--k:%s" aria-label="%s, %s"><span aria-hidden="true">%s</span></button>'
                     % (X3D_SEASON[s], m, s.lower(), a) for m, a, s, t in X3D_MONTHS)
    reset = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12a8 8 0 1 0 2.5-5.8M4 4v5h5"/></svg>'
    play = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z" fill="currentColor"/></svg>'
    back = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg>'
    return ('<div class="x3d" id="x3d">'
            '<div class="xlabels" aria-hidden="true"></div><div class="xpins" aria-hidden="true"></div>'
            '<div class="xtitle xg"><div class="kick">Explore in 3D</div><h1>Kutch, up close</h1><p>The real shape of Kutch, from satellite data. Drag to look around and scroll or pinch to zoom. Pick a program to see its projects and events on the map, and a month to see the season.</p>'
            '<div class="xlegend"><span style="--s:#efece4"><i></i>Salt Rann</span><span style="--s:#cfae74"><i></i>Farmland</span><span style="--s:#a99a5e"><i></i>Scrub</span><span style="--s:#8fc2d6"><i></i>Wetland</span><span style="--s:#cbbfae"><i></i>Towns</span><span class="bd"><i></i>District boundary</span></div>'
            '<div class="xcred">Terrain: NASA SRTM (AWS Terrain Tiles) · Land cover: ESA WorldCover 2021, CC BY 4.0 · Boundary and village positions © OpenStreetMap contributors · Heights ×32</div></div>'
            '<div class="xtoast xg" role="status"></div>'
            '<aside class="xpanel" aria-hidden="true" aria-label="Details"><div class="xp-in xg">'
            '<div class="xp-top"><button class="xp-back" type="button">' + back + '<span></span></button><span class="xp-kick"></span><span class="xp-count"></span><button class="xp-x" type="button" aria-label="Close">×</button></div>'
            '<div class="xp-body"></div>'
            '<div class="xp-act"><a class="xp-go" href="#"></a><button class="xp-prev" type="button" aria-label="Previous">←</button><button class="xp-next" type="button">Next →</button></div>'
            '</div></aside>'
            '<div class="xmonths xg"><div class="xm-head"><span class="xm-lab">Month</span>'
            '<button class="xm-play" type="button" aria-pressed="false" aria-label="Play the year, month by month" title="Play the year">' + play + '</button><b class="xm-season"></b></div>'
            '<div class="xm-list" role="radiogroup" aria-label="Month shown on the map" style="--i:0"><span class="xm-glide"></span>' + months + '</div></div>'
            '<div class="xdock xg" role="toolbar" aria-label="Programs and view controls"><div class="xd-places">' + places + '</div><span class="xd-sep"></span>'
            '<button class="xd-tour" type="button" aria-pressed="false">' + play + '<span>Tour</span></button>'
            '<button class="xd-reset" type="button" aria-label="Show all programs" title="Show all programs">' + reset + '</button></div>'
            '<div class="xload"><div class="xl-ring"></div><span>Building Kutch…</span></div>'
            '<div class="xfall"><div class="xf-head"><div class="kick">Explore</div><h1>Kutch, up close</h1><p>The 3D view needs WebGL 2, which this browser does not offer, so here are the same programs, projects and events as cards.</p></div>' + fall + '</div>'
            '</div>'
            '<script type="application/json" id="x3d-data">' + data + '</script>'
            '<script type="importmap">{"imports":{"three":"./vendor/three/three.module.js","three/addons/":"./vendor/three/addons/"}}</script>'
            '<script type="module" src="js/explore.js"></script>'
            "<script>setTimeout(function(){var s=document.getElementById('x3d');if(!s.classList.contains('ready'))s.classList.add('nogl')},15000)</script>"
            '<noscript><style>.x3d>:not(.xfall){display:none!important}.x3d{height:auto}.xfall{display:grid!important;gap:16px;padding:40px 20px}</style></noscript>'
            '<style>' + X3D_CSS + '</style>')


X3D_TEASER = ('<section class="xteaser"><div class="wrap split"><div class="reveal"><div class="kick">New · Explore in 3D</div><h2>Step into Kutch</h2>'
              '<p>Fly over the real shape of Kutch – built from satellite terrain and land-cover data – from the white salt Rann and Banni grassland to the Gulf coast. '
              'Pick a program to see its projects, events and centres where the work happens, and step through the year month by month: the Rann floods, then dries to white salt, and the tanks fill and run low.</p>'
              '<div class="xt-tags"><span>Real terrain &amp; land cover</span><span>%d programs · %d places</span><span>Month by month</span></div>'
              '<a class="btn" href="explore.html">Explore in 3D →</a></div>'
              '<div class="reveal"><a class="xt-img" href="explore.html"><img src="img/explore-poster.jpg" alt="3D view of Kutch built from real terrain data, with program pins" loading="lazy"></a></div></div></section>') % (len(X3D), len(X3D_ITEMS))


def hero_page(title, sub, img=None):
    im = f'<img src="img/{img}.jpg" alt="">' if img else ""
    return f'<div class="page-hero{" img" if img else ""}">{im}<div class="wrap"><div class="kick" style="color:#f0c46f">KFFFDT</div><h1>{E(title)}</h1><p>{E(sub)}</p></div>{WAVE("#f7f1e3")}</div>'

def table(head, rows, num_from=2):
    th = "".join('<th class="%s">%s</th>' % ("n" if i >= num_from else "", E(h)) for i, h in enumerate(head))
    tr = "".join("<tr>" + "".join('<td class="%s">%s</td>' % ("n" if i >= num_from else "", E(c)) for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<div class="tw"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'

def prog_cards(keys):
    return "".join(f'<a class="card reveal" href="p-{k}.html"><img src="img/{PROGRAMS[k]["img"]}.jpg" alt="" loading="lazy"><div><h3>{E(PROGRAMS[k]["title"])}</h3><p>{E(PROGRAMS[k]["tag"])}</p><span class="more">Learn more →</span></div></a>' for k in keys)

def build():
    os.makedirs(OUT, exist_ok=True)
    W = lambda n, c: open(os.path.join(OUT, n), "w", encoding="utf8").write(c)

    # HOME
    home = f"""{SLIDER}
<div class="wrap"><div class="stats">
<a class="stat" href="about.html"><b data-count="200" data-suffix="+">0</b><span>villages reached</span><i class="go">Where we work →</i></a>
<a class="stat" href="p-kutch-jal-mandir-abhiyan.html"><b data-count="332">0</b><span>Jal Mandir tanks revived</span><i class="go">See the project →</i></a>
<a class="stat" href="activities.html"><b data-count="2041" data-suffix=" lacs">0</b><span>rupees invested in field works</span><i class="go">Our impact →</i></a>
<a class="stat" href="about.html"><b data-count="37">0</b><span>years of service (est. 1989)</span><i class="go">Our story →</i></a></div></div>
<section><div class="wrap split"><div class="reveal"><div class="kick">About the Trust</div><h2>Rooted in Kutch, led by the community</h2>
<p>Founded on 28 March 1989 at Kothara, Abdasa, the Trust began with a simple observation: as trees disappeared, rainfall fell and famine became common. We work to restore that balance – with villagers, not for them.</p>
<div class="mv"><div><h3>Our mission</h3>Self-reliant rural communities able to undertake the overall management of natural resources.</div><div><h3>Our vision</h3>Community-centric sustainable development, easily managed by the community for their well-being.</div></div>
<p style="margin-top:22px"><a class="btn" href="about.html">Read our story</a></p></div><a href="about.html" class="reveal"><img src="img/g16.jpg" alt="Community meeting at Krishi Seva Kendra"></a></div></section>
{BANNER}
{FFF}
<section><div class="wrap"><div class="sh reveal"><div><div class="kick">What we do</div><h2 style="margin:0">Our programs</h2></div><a class="more" href="projects.html">All programs →</a></div><div class="grid g3">{prog_cards(ORDER)}</div></div></section>
{X3D_TEASER}
<section class="alt-bg"><div class="wrap"><div class="sh reveal"><div><div class="kick">Results</div><h2 style="margin:0">Our impact, 1998 – 2024</h2></div><a class="more" href="activities.html">Full activity report →</a></div>
<div class="grid g3"><a class="stat reveal" href="activities.html"><b data-count="1421.67" data-dec="2">0</b><span>Rs. lacs · water conservation · 705 structures</span><i class="go">View details →</i></a>
<a class="stat reveal" href="activities.html"><b data-count="620.82" data-dec="2">0</b><span>Rs. lacs · WASMO village water schemes · 37 villages</span><i class="go">View details →</i></a>
<a class="stat reveal" href="activities.html"><b data-count="320.43" data-dec="2">0</b><span>Rs. lacs · agriculture &amp; fodder · 1,400+ farmers</span><i class="go">View details →</i></a></div></div></section>
{updates_home()}
<section class="dark"><div class="wrap"><div class="sh reveal"><div><div class="kick">Gallery</div><h2 style="margin:0">Faces and places from the field</h2><p style="margin:.6em 0 0;opacity:.8;max-width:520px">Villagers, tanks, farms and herds – the people and places behind the numbers.</p></div><a class="more" href="gallery.html">Open gallery →</a></div>
{MOSAIC}</div></section>
<section class="alt-bg"><div class="wrap"><div class="sh reveal"><div><div class="kick">Trust &amp; transparency</div><h2 style="margin:0">Registered and accountable</h2></div><a class="more" href="legal.html">Legal details, trustees &amp; bank →</a></div>
<div class="grid" style="grid-template-columns:repeat(4,1fr)" id="bd">
<a class="stat reveal" href="legal.html"><b style="font-size:1.6rem">80G</b><span>AAATK 7287 RF 2021401</span></a><a class="stat reveal" href="legal.html"><b style="font-size:1.6rem">12A</b><span>AAATK 7287 RE 2021401</span></a>
<a class="stat reveal" href="legal.html"><b style="font-size:1.6rem">CSR-1</b><span>CSR00000198</span></a><a class="stat reveal" href="legal.html"><b style="font-size:1.6rem">NGO Darpan</b><span>GJ/2021/0288976</span></a></div></div></section>
<section><div class="wrap"><div class="sub-h reveal"><div class="kick">{SPROUT}Our journey</div><h2>35+ years of growing things</h2></div><div class="tl"><div class="fill"></div>{TL}</div></div></section>
{partners_html()}"""
    W("index.html", page("index.html", "Home", home))

    # ABOUT
    objs = ["Support the community in water conservation, groundwater recharge and wasteland / grazing land development.", "Establish laboratories, resource & training centres, workshops and demonstrations; publish related literature.", "Protect animals useful to humans; cattle breeding, animal husbandry and relief during calamities.", "Create employment opportunities through the Trust's activities.", "Carry out agricultural and allied activities.", "Maintain ecology and environment by protecting trees linked to water, land and ecology.", "Help communities use government / panchayat wasteland and cultivable land for trees and grasses under various schemes.", "Cultivate, store and distribute fodder grasses.", "Plant and maintain fruit-bearing, fuel-wood and fodder trees; promote agriculture, horticulture and processing."]
    brief = [("Name", "Kutch Fodder Fruit & Forest Development Trust – KFFFDT"), ("Type", "Registered under Charitable Trust Act, 1950"), ("Registration No.", "E-940 Kutch, 28.03.1989"), ("Registered office", "Kothara, Taluka Abdasa – Kutch"), ("Administrative office", "102, Kaushik Apartment, Bhanushali Nagar, Bhuj – Kutch"), ("Field offices", "Samriddhi Krishi Seva Kendra, Nani Khakhar (Mandvi) · Wel Netrutva Krishi Seva Kendra, Nani Nagalpar (Anjar) · Khadir Vistar Vikas Kendra, Ratanpar (Bhachau)"), ("Contact", f"{PHONE1} / 97277 68919 · {MAIL}")]
    about = hero_page("About the Trust", "કચ્છ ઘાસચારા ફળઝાડ અને જંગલ વિકાસ ટ્રસ્ટ", "g19") + f"""<section><div class="wrap split"><div><h2>Why we began</h2>
<p>In 1988 the founders entered a dialogue with the government to allot cultivable wasteland for conservation, regeneration and afforestation. This led to a public charitable trust, registered on 28 March 1989 at Kothara, Abdasa Block, Kutch.</p>
<p>Trees were disappearing fast. Rainfall became insufficient, famines frequent, and the nature-based village economy fell out of balance – leaving people more vulnerable. The founders concluded that early action was needed to check this degradation.</p></div><img src="img/g23.jpg" alt=""></div></section>
<section class="alt-bg"><div class="wrap"><div class="grid g2"><div class="stat"><div class="kick">Our goal</div><h3>Well-being of people through environmental up-gradation and well management of natural resources.</h3></div>
<div class="stat"><div class="kick">Where we work</div><h3>200+ villages</h3>Abdasa, Lakhpat, Mandvi, Mundra, Anjar, Bhachau &amp; Rapar blocks of Kutch.</div></div>
<h2 style="margin-top:50px">Objectives</h2><ul class="list">{"".join("<li>%s</li>" % E(o) for o in objs)}</ul></div></section>
<section><div class="wrap"><h2>Brief about the Trust</h2>{table(["", "Details"], brief, 9)}</div></section>"""
    W("about.html", page("about.html", "About", about))

    # PROJECTS
    W("projects.html", page("projects.html", "Programs", hero_page("Programs", "Seven thematic areas, one aim: community-managed natural resources.") + f'<section><div class="wrap"><div class="grid g3">{prog_cards(ORDER)}</div></div></section>'))

    # PROGRAM PAGES
    for k in ORDER:
        p = PROGRAMS[k]; b = ""
        if p.get("bullets"): b += '<ul class="list">' + "".join("<li>%s</li>" % E(x) for x in p["bullets"]) + "</ul>"
        for h, items in p.get("sections", []): b += f'<h3 style="margin-top:34px">{E(h)}</h3><ul class="list">' + "".join("<li>%s</li>" % E(x) for x in items) + "</ul>"
        if p.get("note"): b += f'<p style="margin-top:20px;color:var(--muted)">{E(p["note"])}</p>'
        for t in ("table", "table2", "table3"):
            if p.get(t): b += table(*p[t], num_from=9 if t != "table" else 2)
        body = hero_page(p["title"], p["intro"], p["img"]) + (RAIN_SECTION if k == "water-conservation" else "") + f'<section><div class="wrap" style="max-width:860px">{b or "<p>More details coming soon.</p>"}<p style="margin-top:30px"><a class="btn" href="projects.html">← All programs</a></p></div></section>'
        W(f"p-{k}.html", page(f"p-{k}.html", p["title"], body, p["intro"]))

    # ACTIVITIES
    rows = ""
    for name, qty, amt, items in ACT:
        rows += f'<tr class="sub"><td colspan="2">{E(name)}</td><td class="n">{E(qty)}</td><td class="n">{E(amt)}</td></tr>'
        rows += "".join(f'<tr><td>{E(a)}</td><td></td><td class="n">{E(b)}</td><td class="n">{E(c)}</td></tr>' for a, b, c in items)
    rows += '<tr class="sub"><td colspan="3">TOTAL (Rs. in lacs)</td><td class="n">2,041.45</td></tr>'
    act = hero_page("Our impact, 1998 – 2024", "Activities implemented with the support of government agencies, CSR partners and foundations.") + f"""<section><div class="wrap"><div class="stats" style="margin-top:0"><div class="stat"><b data-count="1421.67" data-dec="2">0</b><span>Rs. lacs · water conservation</span></div><div class="stat"><b data-count="620.82" data-dec="2">0</b><span>Rs. lacs · WASMO schemes</span></div><div class="stat"><b data-count="320.43" data-dec="2">0</b><span>Rs. lacs · agriculture &amp; fodder</span></div><div class="stat"><b data-count="2041.45" data-dec="2">0</b><span>Rs. lacs · total</span></div></div>
<div class="tw"><table><thead><tr><th>Activity</th><th></th><th class="n">Quantity</th><th class="n">Amount (Rs. lacs)</th></tr></thead><tbody>{rows}</tbody></table></div>
<p style="color:var(--muted)">Supporting projects &amp; agencies include Watershed Project, WASMO, Drought Proofing Project, UNDP–ABHIYAN, Sujalam Suflam Yojna, Kutch Jal Mandir Abhiyan and CSR projects.</p></div></section>"""
    W("activities.html", page("activities.html", "Impact", act))

    # GALLERY
    gal = gallery_body()
    W("gallery.html", page("gallery.html", "Gallery", gal))

    # UPDATES
    W("updates.html", page("updates.html", "Latest updates", updates_page()))
    W("explore.html", page("explore.html", "Explore Kutch in 3D", explore_body(), "Fly over a 3D Kutch, pick one of the Trust's programs to see its projects and events on the map, and step through the seasons month by month.", bare=True))
    for i, u in enumerate(UPDATES):
        W(f"u-{u['slug']}.html", page(f"u-{u['slug']}.html", u["title"], update_page(i), u["summary"]))

    # LEGAL
    leg = [("Trust Registration No.", "E-940 Kutch, 28.03.1989"), ("80G Certificate No.", "AAATK 7287 RF 2021401, 28.05.2021"), ("12AA Certificate No.", "AAATK 7287 RE 2021401, 28.05.2021"), ("PAN", "AAATK 7287 R"), ("CSR-1 Registration No.", "CSR00000198 / 02.04.2021"), ("NGO Darpan ID", "GJ/2021/0288976")]
    bank = [("Account name", "Kutch Fodder Fruit & Forest Development Trust"), ("Bank of Baroda", "Vijay Nagar Branch, Bhuj 370001 · A/c 78160100013737 · IFSC BARB0VJBHUJ"), ("AU Small Finance Bank", "Jubilee Circle, Bhuj 370001 · A/c 1981212024998751 · IFSC AUBL0002120")]
    tr = [("1","Dhirubhai Dabhi","74","Trustee & Chairman","Bachelor of Rural Studies"),("2","Jayeshkumar Lalka","54","Managing Trustee & Director","M.Sc Geology, PG Diploma Ecology & Environment"),("3","Rajubhai Chavda","42","Trustee & Project Manager","Bachelor of Rural Studies"),("4","Rajubhai Chauhan","61","Trustee & Financial Controller","B.Com"),("5","Anand Thacker","60","Trustee","B.Com"),("6","Dalesh Meisheri","60","Trustee","B.E. Instrumentation"),("7","Vikram Lalka","52","Trustee","B.Sc Botany")]
    st = [("1","Jayeshkumar Lalka","Project Director","M.Sc","30 yrs"),("2","Rajubhai Chavda","Project Manager","B.R.S","19 yrs"),("3","Dhruti Panchani","Agri Expert","B.Sc Agri","2 yrs"),("4","Nimisha Pindoriya","Accountant","B.Com","2 yrs"),("5","Shivji Matang","Para Professional – Agriculture","10th","12 yrs"),("6","Nanandlal Bambhaniya","Para Professional – Animal Health","10th","3 yrs"),("7","Hirabhai Sosa","Office Assistant","8th","15 yrs")]
    legal = hero_page("Legal details", "Registrations, bank details, trustees and staff – transparency for donors and CSR partners.") + f"""<section><div class="wrap"><h2>Registrations</h2>{table(["", "Details"], leg, 9)}<h2 style="margin-top:44px">Bank accounts</h2>{table(["", "Details"], bank, 9)}
<h2 style="margin-top:44px">Trustees</h2>{table(["No.", "Name", "Age", "Designation", "Qualification"], tr, 9)}<h2 style="margin-top:44px">Staff</h2>{table(["No.", "Name", "Designation", "Qualification", "Experience"], st, 9)}</div></section>"""
    W("legal.html", page("legal.html", "Legal", legal))

    # CONTACT
    ct = contact_body()
    W("contact.html", page("contact.html", "Contact", ct))
    print("built", len(os.listdir(OUT)), "files in", OUT)

if __name__ == "__main__":
    build()
