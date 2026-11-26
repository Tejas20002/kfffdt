# KFFFDT site preview (kfffdt.org.in)

Live preview (GitHub Pages): https://tejas20002.github.io/kfffdt/

- `index.html`  – chooser: "Same as live" vs "New design"
- `original/`   – offline mirror of the 14 real pages (WordPress/Elementor output, static)
- `new/`        – redesigned static site (plain HTML/CSS, no CMS)
- `build_new.py` – generates `new/*.html`; edit content/styles there, then `python3 build_new.py`
- `new/js/explore.js` – the "Explore in 3D" page (three.js scene + glass UI); program pins and text live in `X3D` in `build_new.py`
- `new/vendor/three/` – three.js r187 (MIT), served from the site itself, no CDN
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
