# -*- coding: utf-8 -*-
"""Stamp every page's style.css link with the file mtime so browsers fetch fresh CSS."""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run():
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
            if new != s:
                io.open(p, "w", encoding="utf-8").write(new)
                n += 1
    print("cache-busted %d pages at ?v=%s" % (n, ver))


if __name__ == "__main__":
    run()
