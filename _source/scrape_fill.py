# -*- coding: utf-8 -*-
"""Top up categories that came back short because the source host timed out.

Runs scrape_category for each target, up to a few passes, and stops early when
a pass adds nothing new.
"""
import io
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scrape_category as S  # noqa: E402

# category id, slug, outfile, expected count
TARGETS = [
    ("4782836", "aluminium-casement-doors", "source_casement-doors.json", 101),
    ("4782838", "aluminium-tilt-and-turn-windows", "source_tilt-and-turn-windows.json", 13),
    ("4782840", "aluminium-front-doors", "source_front-doors.json", 13),
    ("4782837", "aluminium-bathroom-doors", "source_bathroom-doors.json", 12),
]

ROOT = os.path.dirname(HERE)


def count(f):
    p = os.path.join(ROOT, "_source", f)
    if not os.path.exists(p):
        return 0
    return len(json.load(io.open(p, encoding="utf-8")))


def with_images(f):
    p = os.path.join(ROOT, "_source", f)
    data = json.load(io.open(p, encoding="utf-8")) if os.path.exists(p) else []
    return len([d for d in data if d.get("local_image")])


def main(passes=4):
    for n in range(passes):
        short = []
        for cid, slug, out, expected in TARGETS:
            have, imgs = count(out), with_images(out)
            if have < expected or imgs < have:
                short.append((cid, slug, out, expected, have, imgs))
        if not short:
            print("all categories complete")
            return
        print("\n--- pass %d: %d categories to top up" % (n + 1, len(short)))
        for cid, slug, out, expected, have, imgs in short:
            print("  %s: %d/%d products, %d images" % (slug, have, expected, imgs))
            try:
                S.main(cid, slug, out)
            except Exception as exc:  # noqa: BLE001
                print("    failed:", exc)
            time.sleep(2)
    print("\nfinal counts:")
    for cid, slug, out, expected in TARGETS:
        print("  %-32s %3d/%3d  images %3d" % (slug, count(out), expected, with_images(out)))


if __name__ == "__main__":
    main()
