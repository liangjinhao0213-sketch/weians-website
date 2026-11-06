# -*- coding: utf-8 -*-
"""Replace homepage section 02 (Top picks) with the 3D window showroom.

Idempotent: running twice keeps one showroom section. The old section is kept in
_source/_section02-original.html the first time, so it can be restored.

Run: python build_section02_gallery.py
"""
import io
import os

SITE = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
INDEX = os.path.join(SITE, "index.html")
BACKUP = os.path.join(SITE, "_source", "_section02-original.html")

NEW = """<section class="wg-section" id="top-picks">
  <div class="container">
    <div class="section-head reveal">
      <div class="section-head__main">
        <p class="eyebrow eyebrow--light"><span class="eyebrow__no">02</span>Material &amp; finish</p>
        <h2 class="h2 wg-section__title">Seven finishes.<br><span class="hl">One profile.</span></h2>
      </div>
      <div class="section-head__aside">
        <p class="lead wg-section__lead">The WS-90 three-track slider, rendered from the profile drawing. Drag it, then choose the powder coat — the same seven colours we keep in stock for sampling.</p>
      </div>
    </div>

    <div class="wg reveal" data-window-gallery>
      <div class="wg__stage" data-wg-stage tabindex="0" role="img"
           aria-label="Interactive 3D view of the WS-90 aluminium sliding window">
        <img class="wg__poster" src="assets/img/top-pick-frames.jpg" alt="" aria-hidden="true" loading="lazy">
        <span class="wg__badge">WebGL</span>
        <span class="wg__hint" data-wg-hint>Drag to rotate</span>
      </div>

      <div class="wg__panel">
        <p class="wg__kicker">Selected finish</p>
        <p class="wg__name" data-wg-name>Porcelain Grey</p>
        <p class="wg__note" data-wg-note>Cool matte, fine as porcelain</p>
        <p class="wg__code"><span data-wg-code>01</span> / 07</p>

        <dl class="wg__specs">
          <div><dt>Sightline</dt><dd>22 mm</dd></div>
          <div><dt>Max panel</dt><dd>3.2 &times; 3.4 m</dd></div>
          <div><dt>Uw value</dt><dd>1.3 W/m&sup2;K</dd></div>
          <div><dt>Finish</dt><dd>Powder coat, RAL matched</dd></div>
        </dl>

        <div class="wg__actions">
          <a class="btn" href="#quote" data-quote-open>Request this system</a>
          <a class="btn btn--ghost" href="products/aluminium-sliding-doors/index.html">All sliding doors</a>
        </div>
      </div>
    </div>
  </div>
</section>"""


def main():
    s = io.open(INDEX, encoding="utf-8").read()

    if 'data-window-gallery' in s:
        print("showroom section already in place")
        return

    i = s.find('id="top-picks"')
    if i < 0:
        raise SystemExit("section 02 not found")
    start = s.rfind("<section", 0, i)
    end = s.find("</section>", i) + len("</section>")

    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    io.open(BACKUP, "w", encoding="utf-8").write(s[start:end])

    s = s[:start] + NEW + s[end:]
    io.open(INDEX, "w", encoding="utf-8").write(s)
    print("section 02 replaced (%d -> %d chars)" % (end - start, len(NEW)))
    print("original saved to", BACKUP)


if __name__ == "__main__":
    main()
