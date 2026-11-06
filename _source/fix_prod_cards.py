# -*- coding: utf-8 -*-
"""Catalogue cards: drop the whole-card link, tighten the button row, and make
the action panel always visible on touch devices (where hover never fires)."""
import io
import os
import re

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
PAGE = os.path.join(ROOT, "index.html")


def main():
    s = io.open(PAGE, encoding="utf-8").read()
    start = s.index('<div class="prod-grid">')
    end = s.index("</section>", start)
    grid = s[start:end]

    # 1. media wrapper is no longer a link
    grid, n1 = re.subn(
        r'<a class="prod__media" href="([^"]+)" aria-label="[^"]*">(<img [^>]*>)</a>',
        r'<div class="prod__media">\2</div>', grid)

    # 2. the name is plain text again
    grid, n2 = re.subn(
        r'<h3 class="prod__name"><a href="[^"]+">([^<]+)</a></h3>',
        r'<h3 class="prod__name">\1</h3>', grid)

    # 3. shorter button labels so both fit side by side
    grid = grid.replace(">View product</a>", ">View details</a>")

    s = s[:start] + grid + s[end:]
    io.open(PAGE, "w", encoding="utf-8").write(s)
    print("media links removed:", n1, "| name links removed:", n2)

    css = os.path.join(ROOT, "assets", "css", "style.css")
    c = io.open(css, encoding="utf-8").read()

    # tighten the action row and keep it inside the card
    c = c.replace(""".prod__actions { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.prod__actions .btn { justify-content: center; padding: 9px 10px; font-size: 0.625rem; letter-spacing: 0.06em; }""",
""".prod__actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
}
.prod__actions .btn {
  justify-content: center;
  padding: 8px 6px;
  font-size: 0.5625rem;
  letter-spacing: 0.04em;
  white-space: nowrap;
}""")

    if "/* touch: no hover, so show the actions inline */" not in c:
        c = c.rstrip() + """

/* touch: no hover, so show the actions inline instead of behind a hover panel */
@media (hover: none), (max-width: 760px) {
  .prod__hover {
    position: static;
    transform: none;
    border-top: 1px solid var(--line);
    padding: 12px clamp(14px, 1.4vw, 20px) 14px;
  }
  .prod { padding-bottom: 2px; }
  .prod__actions .btn { padding: 10px 6px; font-size: 0.625rem; }
}
"""
    io.open(css, "w", encoding="utf-8").write(c)
    print("css updated")


if __name__ == "__main__":
    main()
