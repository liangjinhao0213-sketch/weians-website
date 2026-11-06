# -*- coding: utf-8 -*-
"""Keep the homepage catalogue cards pointing at existing product pages.

Whenever a category switches from placeholder products to the scraped ones the
old slugs disappear. This walks the eight catalogue cards and, if a card points
at a missing page, repoints it at the first product of that category (and swaps
in the real photo + price).
"""
import io
import os
import re

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"


def products_of(slug):
    folder = os.path.join(ROOT, "products", slug)
    if not os.path.isdir(folder):
        return []
    out = []
    for f in sorted(os.listdir(folder)):
        if not f.endswith(".html") or f == "index.html":
            continue
        h = io.open(os.path.join(folder, f), encoding="utf-8").read()
        m = re.search(r'products-src/([^"]+)"', h)
        price = re.search(r"<dt>Price</dt>\s*<dd>([^<]+)</dd>", h)
        name = re.search(r'<h1 class="page-hero__title">(.*?)</h1>', h, re.S)
        title = re.sub(r"<[^>]+>", " ", name.group(1)) if name else f
        out.append(dict(file=f, img=m.group(1) if m else None,
                        price=(price.group(1).strip() if price else ""),
                        title=" ".join(title.split())))
    return out


def sync():
    page = os.path.join(ROOT, "index.html")
    s = io.open(page, encoding="utf-8").read()
    changed = 0

    for m in reversed(list(re.finditer(r'<article class="prod reveal">.*?</article>', s, re.S))):
        card = m.group(0)
        hrefs = re.findall(r'href="(products/[a-z0-9-]+/[^"]+\.html)"', card)
        if not hrefs:
            continue
        target = hrefs[0]
        if os.path.exists(os.path.join(ROOT, target.replace("/", os.sep))):
            continue
        slug = target.split("/")[1]
        items = [p for p in products_of(slug) if p["img"]]
        if not items:
            continue
        pick = items[0]
        new_href = "products/%s/%s" % (slug, pick["file"])
        new_card = card.replace(target, new_href)

        # photo
        new_card = re.sub(r'<img src="[^"]*"[^>]*>',
                          '<img src="assets/img/products-src/%s" alt="%s" loading="lazy">'
                          % (pick["img"], pick["title"][:90]), new_card, count=1)
        # spec line -> real price
        if pick["price"]:
            new_card = re.sub(r'<p class="prod__spec">[^<]*</p>',
                              '<p class="prod__spec">%s</p>' % pick["price"], new_card, count=1)
        s = s[:m.start()] + new_card + s[m.end():]
        changed += 1
        print("  card %-40s -> %s" % (slug, new_href))

    if changed:
        io.open(page, "w", encoding="utf-8").write(s)
    print("homepage cards repointed:", changed)
    return changed


if __name__ == "__main__":
    sync()
