# -*- coding: utf-8 -*-
"""Scrape the remaining Weinas categories without any manual input.

Category ids come from the source site's own navigation:
  /supplier-<id>-<slug>
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scrape_category as S  # noqa: E402

# id, our category slug
CATEGORIES = [
    ("4782832", "aluminium-casement-windows"),
    ("4782835", "interior-sliding-partition-doors"),
    ("4782836", "aluminium-casement-doors"),
    ("4782838", "aluminium-tilt-and-turn-windows"),
    ("4782839", "thermal-insulation-windows"),
    ("4782843", "aluminium-swing-doors"),
    ("4782837", "aluminium-bathroom-doors"),
    ("4782840", "aluminium-front-doors"),
    ("4782841", "aluminium-pivot-doors"),
    ("4782842", "aluminium-folding-doors"),
]


def main():
    for cid, slug in CATEGORIES:
        out = "source_%s.json" % slug.replace("aluminium-", "").replace("interior-", "")
        # resume: scrape_category.main() skips products already stored
        print("\n=== %s (%s) -> %s" % (slug, cid, out))
        try:
            S.main(cid, slug, out)
        except Exception as exc:  # noqa: BLE001
            print("  !! failed:", exc)


if __name__ == "__main__":
    main()
