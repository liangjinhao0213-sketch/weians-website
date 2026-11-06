# -*- coding: utf-8 -*-
"""Journal images, photo-render edition: scene panel + product render + numbered
detail legend. Rendered at 1600x900 by headless Edge."""
import io
import os

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
OUT = os.path.join(ROOT, "_source", "posters2")
os.makedirs(OUT, exist_ok=True)

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
  @font-face {
    font-family: "Inter";
    src: url("../../assets/fonts/inter-latin-UcCo3FwrK3.woff2") format("woff2");
    font-weight: 300 700; font-display: block;
  }
  * { margin: 0; box-sizing: border-box; }
  html, body { width: 1600px; height: 900px; }
  body { font-family: "Inter", sans-serif; background: #F5F5F6; color: #0B2B5B; overflow: hidden; }

  .wrap { position: relative; width: 1600px; height: 900px; display: grid; grid-template-columns: 660px 1fr; }

  /* left: scene */
  .scene { position: relative; overflow: hidden; background: #0B2B5B; }
  .scene img { width: 100%; height: 640px; object-fit: cover; display: block; }
  .scene .veil { position: absolute; left: 0; top: 0; width: 100%; height: 640px;
                 background: linear-gradient(180deg, rgba(11,43,91,.82) 0%, rgba(11,43,91,.34) 42%, rgba(11,43,91,.72) 100%); }
  .head { position: absolute; left: 140px; top: 46px; right: 40px; color: #fff; }
  .brand { font-size: 10px; letter-spacing: .24em; text-transform: uppercase; color: rgba(255,255,255,.7); }
  .brand b { color: #fff; letter-spacing: .1em; font-size: 11px; }
  .kicker { margin-top: 26px; font-size: 9.5px; letter-spacing: .2em; text-transform: uppercase; color: #C8A87E; }
  h1 { margin-top: 10px; font-size: 27px; line-height: 1.16; letter-spacing: -.02em; font-weight: 500; max-width: 500px; }
  .scene-cap { position: absolute; left: 140px; bottom: 300px; font-size: 9px; letter-spacing: .16em;
               text-transform: uppercase; color: rgba(255,255,255,.75); }

  .legend { position: absolute; left: 0; bottom: 0; width: 100%; height: 260px; background: #fff;
            padding: 26px 40px 26px 140px; display: grid; gap: 14px; align-content: start; }
  .legend h2 { font-size: 9px; letter-spacing: .2em; text-transform: uppercase; color: #8A9198; }
  .row { display: grid; grid-template-columns: 22px 1fr; gap: 12px; align-items: start; }
  .num { width: 20px; height: 20px; border: 1px solid #0B2B5B; border-radius: 50%;
         display: grid; place-items: center; font-size: 9px; color: #0B2B5B; }
  .row h3 { font-size: 10px; letter-spacing: .14em; text-transform: uppercase; font-weight: 600; }
  .row p { margin-top: 3px; font-size: 10.5px; line-height: 1.45; color: #5C636A; }

  /* right: product */
  .stage { position: relative; background: var(--stage, #F2F2F4); overflow: hidden; }
  .stage::after { content: ""; position: absolute; inset: 0; pointer-events: none;
                  background: radial-gradient(120% 95% at 50% 46%, rgba(255,255,255,0) 42%, rgba(11,43,91,.10) 100%); }
  .stage img { position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%);
               height: 90%; width: auto; max-width: 92%; object-fit: contain; }
  .dot { position: absolute; width: 26px; height: 26px; border-radius: 50%; background: #0B2B5B; color: #fff;
         display: grid; place-items: center; font-size: 11px; font-weight: 600;
         box-shadow: 0 0 0 4px rgba(255,255,255,.9); }
  .dot::after { content: ""; position: absolute; inset: -9px; border-radius: 50%;
                border: 1px solid rgba(11,43,91,.35); }

  .foot { position: absolute; right: 40px; bottom: 26px; text-align: right; color: #0B2B5B; }
  .foot b { font-size: 46px; font-weight: 300; letter-spacing: -.04em; }
  .foot small { display: block; margin-top: 2px; font-size: 8.5px; letter-spacing: .18em;
                text-transform: uppercase; color: #8A9198; }
</style>
</head>
<body>
  <div class="wrap">
    <div class="scene">
      <img src="../../assets/img/__SCENE__" alt="">
      <div class="veil"></div>
      <div class="head">
        <div class="brand"><b>WEINAS</b> · JOURNAL</div>
        <p class="kicker">__KICKER__</p>
        <h1>__TITLE__</h1>
      </div>
      <div class="scene-cap">__SCENE_CAP__</div>
      <div class="legend">
        <h2>Details</h2>
__ROWS__
      </div>
    </div>
    <div class="stage" style="--stage: __STAGE__">
      <img src="../../assets/img/renders/__RENDER__" alt="">
__DOTS__
    </div>
    <div class="foot"><b>__METRIC__</b><small>__METRIC_LABEL__</small></div>
  </div>
</body>
</html>
"""

# dot positions are percentages inside the product stage
POSTS = [
    dict(slug="rainwater-protection-coastal-residences", scene="project-palm-beach.jpg",
         scene_cap="Palm Beach · Florida", render="sliding-door.jpg", stage="#F2F2F4",
         kicker="HIDDEN SPLIT DRAINAGE", title="Rainwater protection for coastal residences",
         metric="5.0", metric_label="mm wall at load points",
         rows=[("Hidden split drainage", "Water leaves through the rail cavity, not the face of the profile."),
               ("Pressure-equalised track", "A split cavity buffers the differential before the seal."),
               ("5 + 15A + 5 glazing", "15 mm airspace keeps the inner pane above the dew point.")],
         dots=[(35, 17), (74, 46), (46, 86)]),

    dict(slug="wind-pressure-high-rise-balconies", scene="collection-facade.jpg",
         scene_cap="High-rise · balcony", render="sliding-door.jpg", stage="#F2F2F4",
         kicker="RIGIDITY WITHOUT WEIGHT", title="Wind pressure on high-rise balconies",
         metric="3.0", metric_label="mm profile wall",
         rows=[("3.0–5.0 mm wall", "Stiffer section under typhoon pressure — less deflection."),
               ("Tandem rollers", "400 kg leaves stay on track, one-finger operation."),
               ("Embedded sash", "Leaf and frame meet on a face, not a gap — no whistle.")],
         dots=[(36, 20), (75, 50), (47, 87)]),

    dict(slug="water-leakage-coastal-high-rises", scene="project-dubai.jpg",
         scene_cap="Al Quoz · Dubai", render="casement-window.jpg", stage="#F0F1F3",
         kicker="GRAVITY DRAINAGE", title="Water leakage in coastal high-rises",
         metric="20", metric_label="mm air cavity",
         rows=[("Floor-drain path", "Vertical gravity drainage instead of tortuous side slots."),
               ("Equal-pressure cavities", "Independent cavities balance pressure before the gasket."),
               ("5 + 20A + 5", "20 mm gap: better acoustics, less condensation.")],
         dots=[(30, 22), (70, 52), (44, 84)]),

    dict(slug="chinese-new-year-orders", scene="factory-sign.jpg",
         scene_cap="Loading bay · Foshan", render="folding-door.jpg", stage="#F2F2F4",
         kicker="BEFORE THE SPRING FESTIVAL", title="Orders finished and packed before the holiday",
         metric="100", metric_label="% pre-shipment check",
         rows=[("Foam-cradled crating", "Corners protected, frames braced, plan checked."),
               ("Corner crimped", "Joints squared and crimped before glazing."),
               ("Glazed & sealed", "Gaskets seated, drainage checked, hardware fitted.")],
         dots=[(34, 24), (70, 54), (45, 86)]),

    dict(slug="heavy-duty-aluminium-sliding-door", scene="top-pick-frames.jpg",
         scene_cap="Palm Beach · interior", render="sliding-door.jpg", stage="#F2F2F4",
         kicker="STRUCTURE & HARDWARE", title="Heavy-duty aluminium sliding doors",
         metric="400", metric_label="kg per leaf",
         rows=[("Stainless tandem rollers", "Load spread across the track — no rattle at speed."),
               ("Polyamide thermal break", "A non-conductive bridge inside the frame."),
               ("Wall of glass", "Slim sightline, larger panes, fewer mullions.")],
         dots=[(36, 18), (74, 48), (46, 88)]),

    dict(slug="macaroon-colour-casement-doors", scene="project-cottesloe.jpg",
         scene_cap="Cottesloe · Western Australia", render="casement-window.jpg", stage="#F0F1F3",
         kicker="COLOUR & GLASS", title="Macaroon colour casement doors",
         metric="RAL", metric_label="powder-coated to any colour",
         rows=[("Macaroon palette", "Mint, coral, sky — soft tones for family spaces."),
               ("Slim casement frame", "Narrow stiles, more glass, cleaner swing."),
               ("Silk-screen printed", "Patterns fired into the glass; colour stays vivid.")],
         dots=[(31, 21), (69, 51), (43, 85)]),
]


def build(p):
    rows = "\n".join(
        """        <div class="row"><span class="num">%d</span>
          <div><h3>%s</h3><p>%s</p></div>
        </div>""" % (i + 1, t, d) for i, (t, d) in enumerate(p["rows"]))
    dots = "\n".join(
        '      <span class="dot" style="left:%s%%;top:%s%%">%d</span>' % (x, y, i + 1)
        for i, (x, y) in enumerate(p["dots"]))

    html = (TEMPLATE
            .replace("__SCENE__", p["scene"]).replace("__SCENE_CAP__", p["scene_cap"])
            .replace("__RENDER__", p["render"]).replace("__STAGE__", p["stage"]).replace("__KICKER__", p["kicker"])
            .replace("__TITLE__", p["title"]).replace("__METRIC__", p["metric"])
            .replace("__METRIC_LABEL__", p["metric_label"])
            .replace("__ROWS__", rows).replace("__DOTS__", dots))
    path = os.path.join(OUT, p["slug"] + ".html")
    io.open(path, "w", encoding="utf-8").write(html)
    return path


if __name__ == "__main__":
    for spec in POSTS:
        print("wrote", build(spec))
