# -*- coding: utf-8 -*-
"""Make the collection cards navigate reliably.

Problem: the rail is drag-scrollable and its cards are one big <a>. A pointer
press that moves a few pixels (or starts a native image drag) cancels the
click, so tapping a card did nothing.

Fix:
  * split the card into <article> + inner link + a real CTA anchor
  * stop native image dragging inside rails / product grids
  * only swallow a click when the rail actually scrolled
"""
import io
import os
import re

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
PAGE = os.path.join(ROOT, "index.html")
ARROW = ('<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
         '<path d="M2 8h11M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.4"/></svg>')


def restructure(s):
    start = s.index('<div class="rail-wrap" id="panel-opening"')
    end = s.index('<div class="rail-wrap" id="panel-application"')
    block = s[start:end]

    pattern = re.compile(
        r'<a class="rail-card rail-card--tech" href="([^"]+)">(.*?)<span class="rail-card__cta">View products (.*?)</span>\s*</a>',
        re.S)

    def repl(m):
        href, inner, svg = m.group(1), m.group(2).strip(), m.group(3)
        return ('<article class="rail-card rail-card--tech">\n'
                '          <a class="rail-card__link" href="%s">%s</a>\n'
                '          <a class="rail-card__cta rail-card__cta--link" href="%s">View products %s</a>\n'
                '        </article>' % (href, inner, href, ARROW))

    block, n = pattern.subn(repl, block)
    print("opening cards restructured:", n)
    return s[:start] + block + s[end:]


def main():
    s = io.open(PAGE, encoding="utf-8").read()
    s = restructure(s)
    io.open(PAGE, "w", encoding="utf-8").write(s)

    # drag hardening + click guard
    js = os.path.join(ROOT, "assets", "js", "main.js")
    j = io.open(js, encoding="utf-8").read()
    j = j.replace("""      var dx = e.clientX - startX;
      if (Math.abs(dx) > 4) moved = true;
      rail.scrollLeft = startLeft - dx;""",
"""      var dx = e.clientX - startX;
      if (Math.abs(dx) > 10) moved = true;
      rail.scrollLeft = startLeft - dx;""")
    j = j.replace("""      if (moved) {
        e.preventDefault();
        e.stopPropagation();
      }""",
"""      if (moved && Math.abs(rail.scrollLeft - startLeft) > 10) {
        e.preventDefault();
        e.stopPropagation();
      }""")
    io.open(js, "w", encoding="utf-8").write(j)
    print("drag guard relaxed")

    css = os.path.join(ROOT, "assets", "css", "style.css")
    c = io.open(css, encoding="utf-8").read()
    if "rail-card__link" not in c.split("/* collection rail")[0] or True:
        if "-webkit-user-drag" not in c:
            c = c.rstrip() + """

/* cards must not start a native image drag, which cancels the click */
.rail img,
.prod img,
.cat img { -webkit-user-drag: none; user-drag: none; }
.rail { user-select: none; }
"""
            io.open(css, "w", encoding="utf-8").write(c)
            print("image drag disabled")


if __name__ == "__main__":
    main()
