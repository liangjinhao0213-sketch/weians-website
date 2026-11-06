# -*- coding: utf-8 -*-
"""Rebuild every product page from whatever has been scraped so far.

  python rebuild_all.py            # build + finalise every category that has data
  python rebuild_all.py --fast     # skip the per-category sitemap/stale pass

Safe to run while a crawl is still going: it only reads the JSON files that
exist right now.
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build_products as BP  # noqa: E402
import products_data as D  # noqa: E402
import apply_source_products as SRC  # noqa: E402
import finalize_category as FIN  # noqa: E402
import sync_home_cards as CARDS  # noqa: E402

ROOT = os.path.dirname(HERE)


def cache_bust():
    ver = str(int(os.path.getmtime(os.path.join(ROOT, "assets", "css", "style.css"))))
    n = 0
    for base, dirs, files in os.walk(ROOT):
        if "_source" in base or "assets" in base:
            continue
        for f in files:
            if not f.endswith(".html"):
                continue
            p = os.path.join(base, f)
            s = io.open(p, encoding="utf-8").read()
            new = re.sub(r'(href="[^"]*assets/css/style\.css)(\?v=\d+)?(")', r'\1?v=%s\3' % ver, s)
            new = re.sub(r'(src="[^"]*assets/js/main\.js)(\?v=\d+)?(")', r'\1?v=%s\3' % ver, new)
            if new != s:
                io.open(p, "w", encoding="utf-8").write(new)
                n += 1
    return n


def main(argv):
    fast = "--fast" in argv

    BP.enrich()
    total = BP.build_index()
    for cat in D.CATEGORIES:
        total += BP.build_category(cat)
        for p in cat["products_full"]:
            total += BP.build_product(cat, p)
    print("built products/index.html + %d categories + %d product pages (%.0f KB)"
          % (len(D.CATEGORIES), sum(len(c["products_full"]) for c in D.CATEGORIES), total / 1024))

    if not fast:
        sourced = [s for s, jf in SRC.SOURCES.items() if SRC.load(jf)]
        FIN.main(sourced)
        CARDS.sync()
        print("cache-busted pages:", cache_bust())

    # report
    print()
    print("%-38s %6s %6s" % ("category", "items", "pages"))
    for c in D.CATEGORIES:
        n = len(c["products_full"])
        print("%-38s %6d %6d" % (c["slug"], n, -(-n // 6)))


if __name__ == "__main__":
    main(sys.argv[1:])
