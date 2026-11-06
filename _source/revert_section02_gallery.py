# -*- coding: utf-8 -*-
"""Undo the 3D showroom in section 02 and restore the original markup.

Removes:
  * the showroom section from index.html (restored from _source/_section02-original.html)
  * the .wg* styles from assets/css/style.css
  * the lazy loader from assets/js/main.js
  * the copied three.js modules in assets/js/wg

The window-gallery source project is left untouched.

Run: python revert_section02_gallery.py
"""
import io
import os
import re
import shutil

SITE = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
INDEX = os.path.join(SITE, "index.html")
BACKUP = os.path.join(SITE, "_source", "_section02-original.html")
CSS = os.path.join(SITE, "assets", "css", "style.css")
JS = os.path.join(SITE, "assets", "js", "main.js")
WG_DIR = os.path.join(SITE, "assets", "js", "wg")


def read(p):
    return io.open(p, encoding="utf-8").read()


def write(p, s):
    io.open(p, "w", encoding="utf-8").write(s)


def main():
    # 1) markup
    if 'data-window-gallery' in read(INDEX):
        if not os.path.exists(BACKUP):
            raise SystemExit("backup of section 02 not found: " + BACKUP)
        original = read(BACKUP)
        s = read(INDEX)
        i = s.find('id="top-picks"')
        start = s.rfind("<section", 0, i)
        end = s.find("</section>", i) + len("</section>")
        s = s[:start] + original + s[end:]
        write(INDEX, s)
        print("markup: section 02 restored (%d chars)" % len(original))
    else:
        print("markup: already original")

    # 2) css
    s = read(CSS)
    if ".wg-section" in s:
        start = s.find("/* ------------------------------------------------------------------ 3D showroom (section 02) */")
        if start < 0:
            start = s.find(".wg-section {")
            start = s.rfind("/*", 0, start)
        s = s[:start].rstrip() + "\n"
        write(CSS, s)
        print("css: showroom block removed")
    else:
        print("css: already clean")

    # 3) js loader
    s = read(JS)
    if "data-window-gallery" in s:
        start = s.find("/* ------------------------------------------------ 3D window showroom (lazy) */")
        s = s[:start].rstrip() + "\n"
        write(JS, s)
        print("js: loader removed")
    else:
        print("js: already clean")

    # 4) copied three.js modules
    if os.path.isdir(WG_DIR):
        shutil.rmtree(WG_DIR)
        print("assets/js/wg removed")

    # 5) bump asset versions on the homepage
    js_v = int(os.path.getmtime(JS))
    css_v = int(os.path.getmtime(CSS))
    s = read(INDEX)
    s = re.sub(r'assets/js/main\.js\?v=\d+', 'assets/js/main.js?v=%d' % js_v, s)
    s = re.sub(r'assets/css/style\.css\?v=\d+', 'assets/css/style.css?v=%d' % css_v, s)
    write(INDEX, s)
    print("versions bumped:", js_v, css_v)


if __name__ == "__main__":
    main()
