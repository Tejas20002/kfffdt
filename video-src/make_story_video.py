#!/usr/bin/env python3
"""Builds the ~75 s story video "Kutch Jal Mandir Abhiyan – From dry beds to full tanks"
from the Trust's own field photos.

Steps:  cards  -> HTML text cards rendered to PNG by headless Chrome (transparent overlays,
                  count-up frames for the impact figures, end card)
        shots  -> one clip per photo: slow Ken Burns move + caption sliding in (ffmpeg)
        final  -> all clips joined with crossfades, then a Full HD master and a web copy

Run:  python3 video-src/make_story_video.py            (all steps)
      python3 video-src/make_story_video.py cards      (just one step: cards | shots | final)
Needs: ffmpeg, Google Chrome. Output: new/video/jal-mandir-story.mp4 + poster (site), video-src/jal-mandir-story-1080p.mp4 (master).
"""
import os, subprocess, sys, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UP = os.path.join(ROOT, "original", "wp-content", "uploads", "2025", "01")
LOGO = os.path.join(ROOT, "new", "img", "logo.png")
WORK = os.path.join(ROOT, "video-src", "build")
OUT = os.path.join(ROOT, "new", "video")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W, H, FPS = 1920, 1080, 30

# ---- the story: (photo, seconds, ken-burns move, caption kicker, caption text) ----
SHOTS = [
    ("Jal-Mandir-Abhiyan-img-26-scaled.jpg", 6.5, "in",    None, "TITLE"),
    ("Jal-Mandir-Abhiyan-img-6.jpg",         5.2, "right", "The problem", "Kutch gets just 312 mm of rain a year – on about 13 days."),
    ("Jal-Mandir-Abhiyan-img-57.jpg",        5.2, "out",   "The problem", "And about 70% of it runs off to the sea."),
    ("Jal-Mandir-Abhiyan-img-53.jpg",        5.2, "in",    "The village decides", "People's participation is a must."),
    ("Jal-Mandir-Abhiyan-img-56.jpg",        5.0, "left",  "The village decides", "Every site starts with a Gram Panchayat resolution."),
    ("Jal-Mandir-Abhiyan-img-52.jpg",        4.0, "out",   None, None),
    ("Jal-Mandir-Abhiyan-img-5.jpg",         5.4, "right", "The work", "The project funds the excavator. Villagers bring their own tractors."),
    ("Jal-Mandir-Abhiyan-img-51.jpg",        5.0, "in",    "The work", "The silt goes back to strengthen bunds and fields."),
    ("Jal-Mandir-Abhiyan-img-29-scaled.jpg", 4.0, "left",  None, None),
    ("Jal-Mandir-Abhiyan-img-44-scaled.jpg", 4.6, "in",    "The rain comes", "Then the monsoon arrives…"),
    ("Jal-Mandir-Abhiyan-img-30-scaled.jpg", 5.2, "right", "The rain comes", "…and this time, the water stays."),
    ("Jal-Mandir-Abhiyan-img-35-scaled.jpg", 4.2, "out",   None, None),
    ("Jal-Mandir-Abhiyan-img-59.jpg",        5.0, "in",    "The rain comes", "Water for people, cattle and wildlife."),
    ("Jal-Mandir-Abhiyan-img-62.jpg",        4.2, "left",  None, None),
]
# impact figures (from the Jal Mandir project profile 2012–2024 on kfffdt.org.in)
STATS = [  # (value, decimals, prefix, suffix, label, seconds)
    (332, 0, "", "", "village tanks revived", 4.0),
    (8835, 0, "+", "", "lac litres of new water storage", 4.0),
    (43, 0, "", "%", "of the cost was contributed by the villagers themselves", 4.6),
]
END_SECONDS = 8.5
XF = 0.9                                   # crossfade length
CHAPTER_BREAKS = {3, 9, 14}                # fade through black before these clip indexes

FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap">'
BASE_CSS = """*{margin:0;box-sizing:border-box}html,body{width:1920px;height:1080px;background:transparent;overflow:hidden}
body{font-family:Inter,system-ui,sans-serif;color:#fff;-webkit-font-smoothing:antialiased}
.kick{font:700 26px Inter,sans-serif;letter-spacing:.22em;text-transform:uppercase;color:#f0c46f}
h1,h2{font-family:Fraunces,Georgia,serif;font-weight:700;line-height:1.08}"""
DROP = '<svg viewBox="0 0 40 52" width="{w}"><path fill="{c}" d="M20 2C20 2 4 22 4 33a16 16 0 0 0 32 0C36 22 20 2 20 2z"/></svg>'


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit("FAILED: %s\n%s" % (" ".join(cmd[:6]), r.stderr[-2000:]))


def shoot(html, png, transparent=True, scale=1):
    path = png.replace(".png", ".html")
    open(path, "w", encoding="utf8").write(html)
    cmd = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=%d,%d" % (W, H),
           "--force-device-scale-factor=%d" % scale, "--virtual-time-budget=4000", "--screenshot=" + png, "file://" + path]
    if transparent:
        cmd.insert(3, "--default-background-color=00000000")
    run(cmd)


def page(body, css):
    return "<!doctype html><html><head><meta charset='utf-8'>%s<style>%s%s</style></head><body>%s</body></html>" % (FONTS, BASE_CSS, css, body)


def cards():
    os.makedirs(WORK, exist_ok=True)
    # title card (over the cracked tank bed)
    shoot(page(
        '<div class="v"></div><div class="t">%s<div class="kick">Kutch Jal Mandir Abhiyan</div><h1>From dry beds<br>to full tanks</h1>'
        '<p>How Kutch&#8217;s villages are bringing their old tanks back to life</p></div>' % DROP.format(w=64, c="#9fd3ee"),
        ".v{position:absolute;inset:0;background:radial-gradient(ellipse at center,rgba(8,20,12,.35),rgba(8,20,12,.78))}"
        ".t{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:22px}"
        "h1{font-size:132px;text-shadow:0 6px 40px rgba(0,0,0,.45)}p{font-size:38px;opacity:.92;max-width:1200px}"), os.path.join(WORK, "cap_00.png"))
    # lower-third captions
    for i, (_, _, _, kick, text) in enumerate(SHOTS):
        if not text or text == "TITLE":
            continue
        shoot(page('<div class="g"></div><div class="c"><div class="kick">%s</div><h2>%s</h2></div>' % (kick, text),
                   ".g{position:absolute;inset:0;background:linear-gradient(0deg,rgba(6,16,10,.82) 0%,rgba(6,16,10,.45) 30%,rgba(6,16,10,0) 58%)}"
                   ".c{position:absolute;left:130px;bottom:120px;max-width:1300px}.kick{margin-bottom:18px;display:flex;align-items:center;gap:16px}"
                   ".kick:before{content:'';width:56px;height:4px;border-radius:4px;background:#f0c46f}"
                   "h2{font-size:76px;text-shadow:0 4px 30px rgba(0,0,0,.5)}"), os.path.join(WORK, "cap_%02d.png" % i))
    # impact figures: count-up frames
    stat_css = (".bg{position:absolute;inset:0;background:radial-gradient(circle at 70% 30%,#3f7a4f 0%,#2e5b3b 45%,#1d3d27 100%)}"
                ".r{position:absolute;right:-180px;top:-180px;width:760px;height:760px;border-radius:50%;border:3px solid rgba(240,196,111,.18);box-shadow:0 0 0 90px rgba(240,196,111,.05),0 0 0 200px rgba(240,196,111,.03)}"
                ".s{position:absolute;left:150px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center}"
                ".n{font:700 300px/1 Fraunces,serif;color:#f0c46f;letter-spacing:-.02em}.l{font:600 58px/1.2 Inter,sans-serif;max-width:1250px;margin-top:20px}"
                ".f{position:absolute;left:150px;bottom:80px;font:600 26px Inter,sans-serif;letter-spacing:.16em;text-transform:uppercase;opacity:.7;display:flex;gap:14px;align-items:center}")
    steps = 18
    for si, (val, dec, pre, suf, label, _) in enumerate(STATS):
        for k in range(steps + 1):
            p = k / steps
            v = val * (1 - (1 - p) ** 3)
            num = pre + ("{:,.%df}" % dec).format(v) + suf
            shoot(page('<div class="bg"></div><div class="r"></div><div class="s"><div class="kick">Impact · 2012 – 2024</div><div class="n">%s</div><div class="l">%s</div></div>'
                       '<div class="f">%sKutch Jal Mandir Abhiyan</div>' % (num, label, DROP.format(w=22, c="#9fd3ee")), stat_css),
                  os.path.join(WORK, "stat%d_%02d.png" % (si, k)), transparent=False)
    # end card (rendered at 2x so the slow zoom stays sharp)
    shoot(page('<div class="e"><img src="file://%s"><h2>Every drop counts.<br>Every village matters.</h2>'
               '<p class="k">Kutch Fodder Fruit &amp; Forest Development Trust · Bhuj, Kutch · since 1989</p>'
               '<p class="c">Partner with us &nbsp;·&nbsp; 98258 58919 &nbsp;·&nbsp; kfffdt@gmail.com &nbsp;·&nbsp; kfffdt.org.in</p></div>' % LOGO,
               "body{background:#f7f1e3;color:#1d2a1f}.e{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:30px}"
               "img{height:150px}h2{font-size:96px;color:#1d2a1f}.k{font:600 30px Inter,sans-serif;color:#5d6a5e}"
               ".c{font:700 32px Inter,sans-serif;color:#fff;background:#2e5b3b;padding:20px 40px;border-radius:99px;margin-top:10px}"),
          os.path.join(WORK, "end.png"), transparent=False, scale=2)
    print("cards done")


def kenburns(move, n):
    z = {"in": "1+0.13*on/%d" % n, "out": "1.13-0.13*on/%d" % n}.get(move, "1.12")
    cx, cy = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    if move == "right":
        cx = "(iw-iw/zoom)*on/%d" % n
    if move == "left":
        cx = "(iw-iw/zoom)*(1-on/%d)" % n
    return "zoompan=z='%s':x='%s':y='%s':d=%d:s=%dx%d:fps=%d" % (z, cx, cy, n, W, H, FPS)


def enc(out):
    return ["-c:v", "libx264", "-preset", "medium", "-crf", "14", "-pix_fmt", "yuv420p", "-r", str(FPS), out]


def shots():
    clips = []
    for i, (photo, d, move, _, text) in enumerate(SHOTS):
        n = int(round(d * FPS))
        out = os.path.join(WORK, "clip_%02d.mp4" % i)
        bg = "[0:v]scale=5760:3240:force_original_aspect_ratio=increase,crop=5760:3240,setsar=1," + kenburns(move, n) + "[bg]"
        if text:
            cap = os.path.join(WORK, "cap_%02d.png" % i)
            t0, t1 = (0.9, 0.8) if text == "TITLE" else (0.6, 0.7)
            fo = d - 1.1
            slide = "if(lt(t,%.2f),40,if(lt(t,%.2f),40*pow(1-(t-%.2f)/%.2f,3),0))" % (t0, t0 + t1, t0, t1)
            fc = (bg + ";[1:v]format=rgba,fade=t=in:st=%.2f:d=%.2f:alpha=1,fade=t=out:st=%.2f:d=0.6:alpha=1[c];"
                  "[bg][c]overlay=x=0:y='%s':eval=frame:shortest=1,format=yuv420p[v]") % (t0, t1, fo, slide)
            cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(UP, photo), "-loop", "1", "-framerate", str(FPS), "-t", "%.2f" % d, "-i", cap,
                   "-filter_complex", fc, "-map", "[v]", "-frames:v", str(n)] + enc(out)
        else:
            cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(UP, photo), "-filter_complex", bg.replace("[bg]", "[v]"),
                   "-map", "[v]", "-frames:v", str(n)] + enc(out)
        run(cmd)
        clips.append(out)
        print("shot", i, "done")
    for si, (*_, d) in enumerate(STATS):
        out = os.path.join(WORK, "stat_%d.mp4" % si)
        run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "15", "-i", os.path.join(WORK, "stat%d_%%02d.png" % si),
             "-vf", "fps=%d,tpad=stop_mode=clone:stop_duration=%.2f,format=yuv420p" % (FPS, d - 19 / 15), "-frames:v", str(int(d * FPS))] + enc(out))
    end_clip()
    print("stat + end clips done")


def end_clip():
    n = int(END_SECONDS * FPS)
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(WORK, "end.png"), "-vf",
         "zoompan=z='1+0.035*on/%d':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=%d:s=%dx%d:fps=%d,format=yuv420p" % (n, n, W, H, FPS),
         "-frames:v", str(n)] + enc(os.path.join(WORK, "end.mp4")))


def final():
    clips = [os.path.join(WORK, "clip_%02d.mp4" % i) for i in range(len(SHOTS))]
    clips += [os.path.join(WORK, "stat_%d.mp4" % i) for i in range(len(STATS))] + [os.path.join(WORK, "end.mp4")]
    durs = [s[1] for s in SHOTS] + [s[-1] for s in STATS] + [END_SECONDS]
    inputs, fc, L, prev = [], [], durs[0], "[0:v]"
    for c in clips:
        inputs += ["-i", c]
    for k in range(1, len(clips)):
        tr = "fadeblack" if k in CHAPTER_BREAKS else ("smoothleft" if k in (15, 16) else "fade")
        fc.append("%s[%d:v]xfade=transition=%s:duration=%.2f:offset=%.3f[x%d]" % (prev, k, tr, XF, L - XF, k))
        L += durs[k] - XF
        prev = "[x%d]" % k
    fc.append("%sfade=t=in:st=0:d=0.8,fade=t=out:st=%.2f:d=1.0,format=yuv420p[v]" % (prev, L - 1.0))
    os.makedirs(OUT, exist_ok=True)
    master = os.path.join(ROOT, "video-src", "jal-mandir-story-1080p.mp4")   # Full HD master for YouTube / social (not part of the site)
    run(["ffmpeg", "-y", "-loglevel", "error"] + inputs + ["-filter_complex", ";".join(fc), "-map", "[v]",
         "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart", master])
    web = os.path.join(OUT, "jal-mandir-story.mp4")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", master, "-vf", "scale=1280:720", "-c:v", "libx264", "-preset", "slow",
         "-crf", "25", "-pix_fmt", "yuv420p", "-movflags", "+faststart", web])
    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "3.5", "-i", master, "-frames:v", "1", "-vf", "scale=1280:720", "-q:v", "3",
         os.path.join(OUT, "jal-mandir-story-poster.jpg")])
    print("final: %.1f s ->" % L, master, web)


# ---- voice-over (macOS built-in voices) ----
# (clip index the line is anchored to, seconds after that clip starts, text)
NARRATION = {
    "en": [
        (0, 0.8, "In Kutch, every drop of water matters."),
        (0, 3.9, "Just three hundred and twelve millimetres of rain falls here in a year, on about thirteen days. And nearly seventy percent of it runs off to the sea."),
        (3, 0.5, "So the villages decided to act. Every Jal Mandir begins with the people, and a resolution of the Gram Panchayat."),
        (6, 0.5, "The project pays for the excavator. The villagers bring their own tractors. And the silt goes back to strengthen bunds and fields."),
        (9, 0.5, "Then the monsoon comes... and this time, the water stays."),
        (12, 0.3, "Water for families, for cattle, and for wildlife. The old village tanks are alive again."),
        (13, 3.0, "Since twenty twelve, three hundred and thirty-two tanks revived. Over eight thousand eight hundred lakh litres of storage. And forty-three percent of the cost, paid by the villagers themselves."),
        (17, 0.6, "Kutch Fodder Fruit and Forest Development Trust. Every drop counts. Every village matters."),
    ],
    "hi": [
        (0, 0.8, "कच्छ में पानी की हर बूंद कीमती है।"),
        (0, 3.9, "यहाँ साल भर में सिर्फ़ तीन सौ बारह मिलीमीटर बारिश होती है, वो भी लगभग तेरह दिनों में। और उसका करीब सत्तर प्रतिशत पानी बहकर समुद्र में चला जाता है।"),
        (3, 0.5, "इसलिए गाँवों ने खुद आगे आने का फ़ैसला किया। हर जल मंदिर की शुरुआत लोगों की भागीदारी और ग्राम पंचायत के प्रस्ताव से होती है।"),
        (6, 0.5, "मशीन का खर्च परियोजना उठाती है, और ट्रैक्टर गाँव वाले खुद लाते हैं। निकली हुई मिट्टी खेतों और मेड़ों को मज़बूत करती है।"),
        (9, 0.5, "फिर मानसून आता है... और इस बार, पानी रुक जाता है।"),
        (12, 0.3, "परिवारों के लिए, पशुओं के लिए, और वन्य जीवों के लिए पानी। गाँव के पुराने तालाब फिर से जीवित हैं।"),
        (13, 3.0, "दो हज़ार बारह से अब तक, तीन सौ बत्तीस तालाब फिर से जीवित। आठ हज़ार आठ सौ लाख लीटर से ज़्यादा भंडारण। और तैंतालीस प्रतिशत खर्च, खुद गाँव वालों का।"),
        (17, 0.6, "कच्छ फ़ॉडर फ्रूट एंड फ़ॉरेस्ट डेवलपमेंट ट्रस्ट। हर बूंद मायने रखती है। हर गाँव मायने रखता है।"),
    ],
}
VOICES = {"aman": ("Aman", "en", 168), "tara": ("Tara", "en", 168), "lekha": ("Lekha", "hi", 172)}
VOUT = os.path.join(ROOT, "video-src", "voiced")


def clip_starts():
    durs = [s[1] for s in SHOTS] + [s[-1] for s in STATS] + [END_SECONDS]
    starts, L = [0.0], durs[0]
    for d in durs[1:]:
        starts.append(L - XF)
        L += d - XF
    return starts, L


def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                                capture_output=True, text=True).stdout.strip())


def voice(name):
    vname, lang, rate = VOICES[name]
    starts, total = clip_starts()
    lines = [(starts[c] + off, text) for c, off, text in NARRATION[lang]]
    tmp = os.path.join(WORK, "vo_" + name)
    os.makedirs(tmp, exist_ok=True)
    os.makedirs(VOUT, exist_ok=True)
    inputs, fc, report = [], [], []
    for i, (t, text) in enumerate(lines):
        f = os.path.join(tmp, "l%02d.aiff" % i)
        run(["say", "-v", vname, "-r", str(rate), "-o", f, text])
        d = dur(f)
        end_limit = (lines[i + 1][0] if i + 1 < len(lines) else total - 0.4) - 0.2
        slot = end_limit - t
        tempo = min(max(d / slot, 1.0), 1.15)
        left = slot - d / tempo
        report.append("  %5.1fs  %4.1fs speech / %4.1fs slot%s%s" % (t, d, slot, "  (sped x%.2f)" % tempo if tempo > 1 else "",
                                                                       "  ** OVERFLOWS %.1fs **" % -left if left < 0 else ""))
        inputs += ["-i", f]
        ms = int(t * 1000)
        fc.append("[%d:a]aresample=48000,%satrim=0:%.3f,adelay=%d:all=1[a%d]" % (i, "atempo=%.3f," % tempo if tempo > 1 else "", slot, ms, i))
    fc.append("%samix=inputs=%d:normalize=0,highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=150,"
              "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,apad,atrim=0:%.3f[vo]" % ("".join("[a%d]" % i for i in range(len(lines))), len(lines), total))
    wav = os.path.join(tmp, "voice.wav")
    run(["ffmpeg", "-y", "-loglevel", "error"] + inputs + ["-filter_complex", ";".join(fc), "-map", "[vo]", wav])
    master = os.path.join(ROOT, "video-src", "jal-mandir-story-1080p.mp4")      # silent master from the 'final' step
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", master, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
         "-movflags", "+faststart", os.path.join(VOUT, "jal-mandir-story-1080p-%s.mp4" % name)])
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", master, "-i", wav, "-map", "0:v", "-map", "1:a", "-vf", "scale=1280:720", "-c:v", "libx264",
         "-preset", "slow", "-crf", "25", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
         os.path.join(VOUT, "jal-mandir-story-%s.mp4" % name)])
    print("voice %s (%s):\n%s" % (name, vname, "\n".join(report)))


def publish(name):
    """Copy the chosen voiced web version into the website (new/video/jal-mandir-story.mp4)."""
    shutil.copyfile(os.path.join(VOUT, "jal-mandir-story-%s.mp4" % name), os.path.join(OUT, "jal-mandir-story.mp4"))
    print("published voice:", name)


if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else "all"
    if step in ("cards", "all"):
        cards()
    if step in ("shots", "all"):
        shots()
    if step == "end":                         # re-render only the end card clip
        end_clip()
    if step in ("final", "all"):
        final()
    if step == "voice":                       # python3 make_story_video.py voice aman|tara|lekha
        voice(sys.argv[2])
    if step == "publish":                     # python3 make_story_video.py publish aman
        publish(sys.argv[2])
