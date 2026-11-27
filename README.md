# KFFFDT site preview (kfffdt.org.in)

Live preview (GitHub Pages): https://tejas20002.github.io/kfffdt/

- `index.html`  – chooser: "Same as live" vs "New design"
- `original/`   – offline mirror of the 14 real pages (WordPress/Elementor output, static)
- `new/`        – redesigned static site (plain HTML/CSS, no CMS)
- `build_new.py` – generates `new/*.html`; edit content/styles there, then `python3 build_new.py`
- `new/js/explore.js` – the "Explore in 3D" page (three.js scene + glass UI). Its content lives in `build_new.py`:
  `X3D` = the programs (one pin each), `X3D_ITEMS` = projects, events and centres (shown only after a program is picked),
  `X3D_MONTHS` = the month-by-month season notes. To add a project or event, copy an entry in `X3D_ITEMS`
  (the comment above it lists the fields) and run `python3 build_new.py` – the build stops with a message if an id,
  program, position or image is wrong. Deep links: `explore.html#fruit` or `explore.html#fruit/beej-rath`.
- `new/vendor/three/` – three.js r187 (MIT), served from the site itself, no CDN
- `new/data/kutch.bin` + `kutch.json` – the real Kutch ground for the 3D page (1.6 km grid: height, land cover, inside-district flag).
  Rebuild with `python3 -I data-src/make_kutch_terrain.py <cache-dir> new/data`.
  Sources: NASA SRTM via AWS Terrain Tiles, ESA WorldCover 2021 (CC BY 4.0), OpenStreetMap district boundary (ODbL) – credited on the page.
- `new/data/boundaries.json` – real boundaries for the 3D page: the district outline (the land is cut along it) and the 10 talukas
  from OpenStreetMap, and all 958 Kutch village boundaries from the Census 2001 maps published by DataMeet (both ODbL).
  Rebuild with `python3 -I data-src/make_kutch_boundaries.py <cache-dir> new/data`, then run `build_new.py` again
  (it matches every project to its village outline and warns if a name does not match).
- `video-src/make_story_video.py` – builds the story video (working files and masters are not in git)
- `serve.sh`    – run `./serve.sh` then open http://localhost:8080

## Updating the live preview

```sh
python3 build_new.py          # regenerate the new design
git add -A && git commit -m "Update site"
git push                      # GitHub Pages republishes in about a minute
```

Every page carries `noindex` so this preview never competes with kfffdt.org.in in search results.
When the new design moves to the real domain, set `NOINDEX = False` in `build_new.py`.
`.nojekyll` must stay: the mirror has an `_ext/` folder that Jekyll would otherwise drop.

Not mirrored: the 48 unused Echofy demo pages, wp-admin/PHP/database (needs a Hostinger backup).
