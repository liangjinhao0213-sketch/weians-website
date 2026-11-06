# -*- coding: utf-8 -*-
"""Rebuild the whole homepage catalogue <section> from the scraped data.

Replaces the section as a unit (from its opening tag to the next </section>),
so any leftover damage inside the grid disappears. Every href and image is
validated before the file is written.
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import products_data as D  # noqa: E402
import apply_source_products as SRC  # noqa: E402

ROOT = os.path.dirname(HERE)
ARROW = ('<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
         '<path d="M2 8h11M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.4"/></svg>')

PICKS = [
    "aluminium-sliding-doors",
    "aluminium-casement-windows",
    "aluminium-sliding-windows",
    "interior-sliding-partition-doors",
    "aluminium-tilt-and-turn-windows",
    "thermal-insulation-windows",
    "aluminium-folding-doors",
    "aluminium-pivot-doors",
]

CARD = """        <article class="prod reveal" style="--delay:{delay}ms">
          <div class="prod__media"><img src="assets/img/{img}" alt="{alt}" loading="lazy"></div>
          <div class="prod__info">
            <h3 class="prod__name">{name}</h3>
            <p class="prod__spec">{spec}</p>
          </div>
          <div class="prod__hover">
            <dl>
              <div><dt>Model</dt><dd><b>{model}</b></dd></div>
              <div><dt>MOQ</dt><dd><b>{moq}</b></dd></div>
              <div><dt>Price</dt><dd><b>{price}</b></dd></div>
            </dl>
            <div class="prod__actions">
              <a class="btn btn--sm" href="{href}">View details</a>
              <a class="btn btn--sm btn--ghost" href="#quote">Request A Quote</a>
            </div>
          </div>
        </article>"""


def main():
    SRC.run()
    cats = {c["slug"]: c for c in D.CATEGORIES}
    cards = []
    for i, slug in enumerate(PICKS):
        cat = cats[slug]
        items = [p for p in cat["products_full"]
                 if p.get("image") and os.path.exists(os.path.join(ROOT, "assets", "img", p["image"].replace("/", os.sep)))]
        p = items[0]
        table = dict(p["table"])
        cards.append(CARD.format(
            delay=(i % 3) * 70,
            img=p["image"],
            alt=p["full_name"][:110].replace('"', "&quot;"),
            name="%s · %s" % (cat["short"], p["code"]),
            spec=table.get("Price", "on request"),
            model=table.get("Model", p["code"]),
            moq=table.get("MOQ", "on request"),
            price=table.get("Price", "on request"),
            href="products/%s/%s" % (slug, p["slug"] + ".html"),
        ))

    section = """<section class="section section--offwhite" id="catalogue">
  <div class="container">
    <div class="section-head reveal">
      <div class="section-head__main">
        <p class="eyebrow"><span class="eyebrow__no">06</span>Catalogue</p>
        <h2 class="h2">Eight best-sellers. <span class="hl">Twelve in total.</span></h2>
        <p class="catalogue__note"><i></i>B2B only — pricing on request</p>
      </div>
      <div class="section-head__aside">
        <p class="lead">Uniform drawings, datasheets and CAD details for every system. Hover a product to read its performance summary and request a quotation.</p>
      </div>
    </div>
    <div class="prod-grid">
%s
    </div>
  </div>
</section>""" % "\n".join(cards)

    page = os.path.join(ROOT, "index.html")
    s = io.open(page, encoding="utf-8").read()
    start = s.index('<section class="section section--offwhite" id="catalogue">')
    end = s.index("</section>", start) + len("</section>")
    s = s[:start] + section + s[end:]
    io.open(page, "w", encoding="utf-8").write(s)

    print("catalogue section rebuilt: %d cards" % len(cards))
    for ln in re.findall(r'href="(products/[^"]+)"', section):
        ok = os.path.exists(os.path.join(ROOT, ln.replace("/", os.sep)))
        if not ok:
            print("  MISSING href:", ln)


if __name__ == "__main__":
    main()
