# -*- coding: utf-8 -*-
"""Journal images, part 2: macro-detail, scene-led and colour-board layouts.

Type A (product + scene split) lives in build_posters2.py.
This file covers:
  B  macro detail  -> full-bleed close-up + two zoom insets + spec column
  C  scene-led     -> full-bleed site photo + white fact card + product chip
  F  colour board  -> product + four finish chips + RAL metric
"""
import io
import os

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
OUT = os.path.join(ROOT, "_source", "posters3")
os.makedirs(OUT, exist_ok=True)

BASE_CSS = """
  @font-face {
    font-family: "Inter";
    src: url("../../assets/fonts/inter-latin-UcCo3FwrK3.woff2") format("woff2");
    font-weight: 300 700; font-display: block;
  }
  * { margin: 0; box-sizing: border-box; }
  html, body { width: 1600px; height: 900px; }
  body { font-family: "Inter", sans-serif; background: #F2F2F4; color: #0B2B5B; overflow: hidden; position: relative; }
  .brand { font-size: 10px; letter-spacing: .24em; text-transform: uppercase; color: #8A9198; }
  .brand b { color: #0B2B5B; letter-spacing: .1em; font-size: 11px; }
  .kicker { font-size: 9.5px; letter-spacing: .2em; text-transform: uppercase; color: #9C7B52; }
  h1 { font-size: 26px; line-height: 1.16; letter-spacing: -.02em; font-weight: 500; }
  .rows { display: grid; gap: 14px; }
  .row { display: grid; grid-template-columns: 22px 1fr; gap: 12px; }
  .num { width: 20px; height: 20px; border: 1px solid #0B2B5B; border-radius: 50%;
         display: grid; place-items: center; font-size: 9px; color: #0B2B5B; }
  .row h3 { font-size: 10px; letter-spacing: .14em; text-transform: uppercase; font-weight: 600; }
  .row p { margin-top: 3px; font-size: 10.5px; line-height: 1.45; color: #5C636A; }
  .metric b { font-size: 46px; font-weight: 300; letter-spacing: -.04em; }
  .metric small { display: block; margin-top: 2px; font-size: 8.5px; letter-spacing: .18em;
                  text-transform: uppercase; color: #8A9198; }
"""


def page(css, body):
    return """<!doctype html><html lang="en"><head><meta charset="utf-8">
<style>%s%s</style></head><body>%s</body></html>""" % (BASE_CSS, css, body)


# ---------------------------------------------------------------- type B: macro
B_CSS = """
  .shot { position: absolute; left: 520px; top: 0; width: 1080px; height: 900px; overflow: hidden; background: #EDEEF0; }
  .shot img { width: 100%; height: 100%; object-fit: cover; }
  .shot::after { content: ""; position: absolute; inset: 0;
                 background: linear-gradient(90deg, #F2F2F4 0%, rgba(242,242,244,0) 18%); }
  .panel { position: absolute; left: 0; top: 0; width: 600px; height: 900px; padding: 46px 60px 40px 140px;
           background: #F2F2F4; display: grid; grid-template-rows: auto auto 1fr auto; gap: 22px; }
  .head { display: grid; gap: 12px; }
  .insets { position: absolute; left: 430px; top: 150px; display: grid; gap: 18px; }
  .inset { width: 180px; height: 150px; border: 1px solid rgba(11,43,91,.16); overflow: hidden;
           background: #fff; }
  .inset img { width: 100%; height: 100%; object-fit: cover; }
  .inset span { position: absolute; }
  .inset-wrap { position: relative; }
  .inset-cap { margin-top: 6px; font-size: 8.5px; letter-spacing: .16em; text-transform: uppercase; color: #8A9198; }
  .metric { text-align: right; }
"""


def type_b(post):
    rows = "\n".join(
        '<div class="row"><span class="num">%d</span><div><h3>%s</h3><p>%s</p></div></div>' % (i + 1, t, d)
        for i, (t, d) in enumerate(post["rows"]))
    insets = "\n".join(
        """      <div><div class="inset"><img src="../../assets/img/renders/%s" alt=""></div>
        <p class="inset-cap">%s</p></div>""" % (img, cap) for img, cap in post["insets"])
    body = """
  <div class="shot"><img src="../../assets/img/renders/%s" alt=""></div>
  <div class="panel">
    <div class="brand"><b>WEINAS</b> · JOURNAL</div>
    <div class="head">
      <p class="kicker">%s</p>
      <h1>%s</h1>
    </div>
    <div class="rows">%s</div>
    <div class="metric"><b>%s</b><small>%s</small></div>
  </div>
  <div class="insets">%s</div>
""" % (post["macro"], post["kicker"], post["title"], rows, post["metric"], post["metric_label"], insets)
    return page(B_CSS, body)


# ---------------------------------------------------------------- type C: scene
C_CSS = """
  .scene { position: absolute; inset: 0; }
  .scene img { width: 100%; height: 100%; object-fit: cover; }
  .veil { position: absolute; inset: 0;
          background: linear-gradient(180deg, rgba(11,43,91,.62) 0%, rgba(11,43,91,.28) 40%, rgba(11,43,91,.88) 100%); }
  .top { position: absolute; left: 140px; top: 44px; display: grid; gap: 10px; color: #fff; }
  .top .brand { color: rgba(255,255,255,.72); }
  .top .brand b { color: #fff; }
  .top .kicker { color: #C8A87E; }
  .card { position: absolute; left: 140px; bottom: 60px; width: 640px; background: #fff; padding: 30px 34px; }
  .card h1 { font-size: 25px; max-width: 18ch; }
  .card .rows { margin-top: 20px; gap: 11px; }
  .chip { position: absolute; right: 140px; bottom: 60px; width: 300px; background: #fff; padding: 18px; }
  .chip img { width: 100%; height: 190px; object-fit: contain; }
  .chip p { margin-top: 12px; font-size: 9px; letter-spacing: .16em; text-transform: uppercase; color: #8A9198; text-align: center; }
  .metric { position: absolute; right: 140px; top: 60px; text-align: right; color: #fff; }
  .metric b { color: #fff; }
  .metric small { color: rgba(255,255,255,.7); }
"""


def type_c(post):
    rows = "\n".join(
        '<div class="row"><span class="num">%d</span><div><h3>%s</h3><p>%s</p></div></div>' % (i + 1, t, d)
        for i, (t, d) in enumerate(post["rows"]))
    body = """
  <div class="scene"><img src="../../assets/img/%s" alt=""></div>
  <div class="veil"></div>
  <div class="top">
    <div class="brand"><b>WEINAS</b> · JOURNAL</div>
    <p class="kicker">%s</p>
    <p style="font-size:9.5px;letter-spacing:.16em;text-transform:uppercase;color:rgba(255,255,255,.72)">%s</p>
  </div>
  <div class="metric"><b>%s</b><small>%s</small></div>
  <div class="card">
    <h1>%s</h1>
    <div class="rows">%s</div>
  </div>
  <div class="chip"><img src="../../assets/img/renders/%s" alt=""><p>%s</p></div>
""" % (post["scene"], post["kicker"], post["scene_cap"], post["metric"], post["metric_label"],
       post["title"], rows, post["render"], post["chip_cap"])
    return page(C_CSS, body)


# -------------------------------------------------------------- type F: colour
F_CSS = """
  .stage { position: absolute; left: 0; top: 0; width: 1000px; height: 900px; background: #F5F5F7; overflow: hidden; }
  .stage img { position: absolute; left: 46%; top: 52%; transform: translate(-50%, -50%);
               height: 88%; width: auto; object-fit: contain; }
  .board { position: absolute; right: 0; top: 0; width: 600px; height: 900px; background: #0B2B5B; color: #fff;
           padding: 54px 140px 54px 54px; display: grid; grid-template-rows: auto auto 1fr auto; gap: 26px; }
  .board .brand { color: rgba(255,255,255,.62); }
  .board .brand b { color: #fff; }
  .board .kicker { color: #C8A87E; }
  .board h1 { font-size: 25px; color: #fff; }
  .swatches { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; align-content: start; }
  .sw { aspect-ratio: 1 / 1.5; border: 1px solid rgba(255,255,255,.28); display: grid; align-items: end;
        padding: 8px; font-size: 8px; letter-spacing: .1em; text-transform: uppercase; color: rgba(11,43,91,.75); }
  .board .metric b { color: #fff; font-size: 64px; }
  .board .metric small { color: rgba(255,255,255,.6); }
"""


def type_f(post):
    sw = "\n".join('<div class="sw" style="background:%s">%s</div>' % (c, n) for c, n in post["swatches"])
    body = """
  <div class="stage"><img src="../../assets/img/renders/%s" alt=""></div>
  <div class="board">
    <div class="brand"><b>WEINAS</b> · JOURNAL</div>
    <div>
      <p class="kicker">%s</p>
      <h1 style="margin-top:10px">%s</h1>
    </div>
    <div class="swatches">%s</div>
    <div class="metric"><b>%s</b><small>%s</small></div>
  </div>
""" % (post["render"], post["kicker"], post["title"], sw, post["metric"], post["metric_label"])
    return page(F_CSS, body)


POSTS = [
    dict(file="wind-pressure-high-rise-balconies", type="B",
         macro="macro-track.jpg", kicker="RIGIDITY WITHOUT WEIGHT",
         title="Wind pressure on high-rise balconies",
         metric="3.0", metric_label="mm profile wall",
         rows=[("3.0–5.0 mm wall", "A stiffer section under typhoon pressure — less deflection."),
               ("Tandem rollers", "400 kg leaves stay on track, one-finger operation."),
               ("Embedded sash", "Leaf and frame meet on a face, not a gap.")],
         insets=[("macro-corner.jpg", "Corner joint"), ("macro-handle.jpg", "Handle & stile")]),

    dict(file="chinese-new-year-orders", type="C",
         scene="factory-sign.jpg", scene_cap="Loading bay · Foshan",
         kicker="BEFORE THE SPRING FESTIVAL",
         title="Orders finished and packed before the holiday",
         metric="100", metric_label="% pre-shipment check",
         render="folding-door.jpg", chip_cap="WF-85 folding · packed complete",
         rows=[("Foam-cradled crating", "Corners protected, frames braced, plan checked."),
               ("Corner crimped", "Joints squared and crimped before glazing."),
               ("Glazed & sealed", "Gaskets seated, drainage checked, hardware fitted.")]),

    dict(file="heavy-duty-aluminium-sliding-door", type="B",
         macro="macro-handle.jpg", kicker="STRUCTURE & HARDWARE",
         title="Heavy-duty aluminium sliding doors",
         metric="400", metric_label="kg per leaf",
         rows=[("Stainless tandem rollers", "Load spread across the track — no rattle."),
               ("Polyamide thermal break", "A non-conductive bridge inside the frame."),
               ("Wall of glass", "Slim sightline, larger panes, fewer mullions.")],
         insets=[("macro-track.jpg", "Track & rollers"), ("macro-corner.jpg", "Frame corner")]),

    dict(file="macaroon-colour-casement-doors", type="F",
         render="casement-window.jpg", kicker="COLOUR & GLASS",
         title="Macaroon colour casement doors",
         metric="RAL", metric_label="powder-coated to any colour",
         swatches=[("#CFE3DC", "Mint"), ("#F2D6D0", "Coral"), ("#D8DEE8", "Sky"), ("#E7DCC8", "Sand")]),
]

BUILDERS = {"B": type_b, "C": type_c, "F": type_f}

if __name__ == "__main__":
    for post in POSTS:
        html = BUILDERS[post["type"]](post)
        path = os.path.join(OUT, post["file"] + ".html")
        io.open(path, "w", encoding="utf-8").write(html)
        print("wrote", post["file"], "(type %s)" % post["type"])
