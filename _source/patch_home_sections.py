# -*- coding: utf-8 -*-
"""Homepage refresh:
1. 'By opening' collection cards get an explicit CTA.
2. 'By application' cards get a contact button.
3. The catalogue grid now renders eight real products from products_data.py,
   each linking to its detail page.
"""
import io
import os
import re
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
import products_data as D  # noqa: E402
from build_products import slugify  # noqa: E402

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
PAGE = os.path.join(ROOT, "index.html")
ARROW = ('<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
         '<path d="M2 8h11M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.4"/></svg>')

# catalogue picks: (category slug, product code, sightline, uw, svg)
PICKS = [
    ("aluminium-sliding-doors", "WS-90", "22 mm", "1.3 W/m²K", "aluminium-sliding-doors.svg"),
    ("aluminium-casement-windows", "WC-75", "55 mm", "1.4 W/m²K", "aluminium-casement-windows.svg"),
    ("aluminium-sliding-windows", "WSW-70", "45 mm", "1.6 W/m²K", "aluminium-sliding-windows.svg"),
    ("interior-sliding-partition-doors", "IP-60", "40 mm", "—", "interior-sliding-partition-doors.svg"),
    ("aluminium-tilt-and-turn-windows", "WT-75", "52 mm", "1.1 W/m²K", "aluminium-tilt-and-turn-windows.svg"),
    ("thermal-insulation-windows", "WTH-90", "60 mm", "0.9 W/m²K", "thermal-insulation-windows.svg"),
    ("aluminium-folding-doors", "WF-85", "68 mm", "1.3 W/m²K", "aluminium-folding-doors.svg"),
    ("aluminium-pivot-doors", "WP-100", "70 mm", "1.5 W/m²K", "aluminium-pivot-doors.svg"),
]

CATS = {c["slug"]: c for c in D.CATEGORIES}


def find_product(cat_slug, code):
    cat = CATS[cat_slug]
    for (pcode, name, blurb, extra, sizes) in cat["products"]:
        if pcode == code:
            return cat, dict(code=pcode, name=name, blurb=blurb, extra=extra, sizes=sizes,
                             slug=slugify(pcode + " " + name))
    raise KeyError((cat_slug, code))


def prod_card(pick):
    cat_slug, code, sight, uw, svg = pick
    cat, p = find_product(cat_slug, code)
    href = "products/%s/%s.html" % (cat_slug, p["slug"])
    title = "%s %s" % (p["code"], p["name"])
    return """        <article class="prod reveal">
          <a class="prod__media" href="%s" aria-label="%s">\
<img src="assets/img/products/%s" alt="%s technical elevation" loading="lazy" width="400" height="500"></a>
          <div class="prod__info">
            <h3 class="prod__name"><a href="%s">%s</a></h3>
            <p class="prod__spec">%s</p>
          </div>
          <div class="prod__hover">
            <dl>
              <div><dt>Sightline</dt><dd><b>%s</b></dd></div>
              <div><dt>Uw value</dt><dd><b>%s</b></dd></div>
              <div><dt>Max size</dt><dd><b>%s</b></dd></div>
            </dl>
            <div class="prod__actions">
              <a class="btn btn--sm" href="%s">View product</a>
              <a class="btn btn--sm btn--ghost" href="#quote">Request A Quote</a>
            </div>
          </div>
        </article>""" % (href, title, svg, title, href, title, uw, sight, uw, p["sizes"], href)


def main():
    s = io.open(PAGE, encoding="utf-8").read()

    # ---------------------------------------------- 1. opening cards: CTA pill
    cta = '<span class="rail-card__cta">View products %s</span>' % ARROW
    start = s.index('<div class="rail-wrap" id="panel-opening"')
    end = s.index('<div class="rail-wrap" id="panel-application"')
    block = s[start:end]
    block, n = re.subn(r'(</span></span>)(\s*</a>)', r'\1\n          ' + cta + r'\2', block)
    s = s[:start] + block + s[end:]
    print("opening cards with CTA:", n)

    # ------------------------------------ 2. application cards: contact button
    start = s.index('<div class="rail-wrap" id="panel-application"')
    end = s.index("</section>", start)
    block = s[start:end]
    cards = re.findall(r'<a class="rail-card" href="([^"]*)">(.*?)</a>', block, re.S)
    print("application cards:", len(cards))

    rebuilt = []
    for href, inner in cards:
        rebuilt.append(
            '<article class="rail-card rail-card--app">\n'
            '          <a class="rail-card__link" href="%s">%s</a>\n'
            '          <a class="rail-card__cta rail-card__cta--link" href="contact-us/index.html">'
            'Contact us %s</a>\n'
            '        </article>' % (href, inner.strip(), ARROW))

    # replace every <a class="rail-card" ...>…</a> with its rebuilt version, in order
    out, idx = [], 0
    for m in re.finditer(r'<a class="rail-card" href="[^"]*">.*?</a>', block, re.S):
        out.append(block[idx:m.start()])
        out.append(rebuilt.pop(0))
        idx = m.end()
    out.append(block[idx:])
    block = "".join(out)
    s = s[:start] + block + s[end:]

    # ------------------------------------------ 3. catalogue: real products
    gstart = s.index('<div class="prod-grid">')
    gend = s.index("</section>", gstart)
    cards_html = "\n".join(prod_card(p) for p in PICKS)
    s = s[:gstart] + '<div class="prod-grid">\n' + cards_html + "\n      " + s[gend:]
    print("catalogue cards rebuilt:", len(PICKS))

    io.open(PAGE, "w", encoding="utf-8").write(s)


if __name__ == "__main__":
    main()
