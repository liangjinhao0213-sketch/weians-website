# -*- coding: utf-8 -*-
"""After a rebuild: drop stale product pages and refresh that category's sitemap block.

  python finalize_category.py aluminium-sliding-windows aluminium-sliding-doors
"""
import io
import os
import re
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
import products_data as D  # noqa: E402
import apply_source_products as SRC  # noqa: E402

ROOT = os.path.dirname(HERE)
BASE = "https://www.weinas.com/products"


def clean(slug, cat):
    folder = os.path.join(ROOT, "products", slug)
    keep = {p["slug"] + ".html" for p in cat.get("products_full", [])} | {"index.html"}
    removed = 0
    for f in os.listdir(folder):
        if f.endswith(".html") and f not in keep:
            os.remove(os.path.join(folder, f))
            removed += 1
    return removed, len(keep) - 1


def sitemap(slug, cat):
    path = os.path.join(ROOT, "sitemap.xml")
    x = io.open(path, encoding="utf-8").read()
    x = re.sub(r"  <url>\n    <loc>%s/%s/[^<]*</loc>\n    <priority>[^<]*</priority>\n  </url>\n?"
               % (BASE, re.escape(slug)), "", x)
    block = ['  <url>\n    <loc>%s/%s/</loc>\n    <priority>0.8</priority>\n  </url>' % (BASE, slug)]
    for p in cat.get("products_full", []):
        block.append('  <url>\n    <loc>%s/%s/%s.html</loc>\n    <priority>0.6</priority>\n  </url>'
                     % (BASE, slug, p["slug"]))
    x = x.replace("</urlset>", "\n".join(block) + "\n</urlset>")
    io.open(path, "w", encoding="utf-8").write(x)
    return x.count("<url>")


def main(slugs):
    SRC.run()
    for slug in slugs:
        cat = next((c for c in D.CATEGORIES if c["slug"] == slug), None)
        if not cat or not cat.get("products_full"):
            print("skip", slug)
            continue
        removed, kept = clean(slug, cat)
        total = sitemap(slug, cat)
        print("%-32s kept %3d products, removed %d stale, sitemap %d urls"
              % (slug, kept, removed, total))


if __name__ == "__main__":
    main(sys.argv[1:] or ["aluminium-sliding-doors", "aluminium-sliding-windows"])
