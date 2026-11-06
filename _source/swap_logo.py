# -*- coding: utf-8 -*-
"""Swap in the client's existing logo: header, footer plate, favicons, OG data."""
import io
import os

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"

REPLACEMENTS = [
    # header logo
    ('<img src="assets/img/logo.png" alt="Weinas — Doors And Windows Manufacturer" width="131" height="57">',
     '<img src="assets/img/logo.png" alt="Weinas — Doors And Windows Manufacturer" width="153" height="42">'),
    # footer logo -> white plaque so the navy strokes stay readable on navy
    ('<img src="assets/img/logo-light.png" alt="Weinas — Doors And Windows Manufacturer" width="148" height="65" loading="lazy">',
     '<span class="footer__logo"><img src="assets/img/logo.png" alt="Weinas — Doors And Windows Manufacturer" width="176" height="48" loading="lazy"></span>'),
    # favicons
    ('<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">',
     '<link rel="icon" href="assets/img/favicon.png" type="image/png" sizes="64x64">'),
    ('<link rel="apple-touch-icon" href="assets/img/logo.png">',
     '<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">'),
]

for rel in ("index.html", r"_source\build_site.py"):
    p = os.path.join(ROOT, rel)
    s = io.open(p, encoding="utf-8").read()
    missing = [old[:60] for old, _ in REPLACEMENTS if old not in s]
    for old, new in REPLACEMENTS:
        s = s.replace(old, new)
    io.open(p, "w", encoding="utf-8").write(s)
    print(rel, "updated" if not missing else "MISSING: " + str(missing))

# --- CSS: header logo size + footer plaque
css_path = os.path.join(ROOT, "assets", "css", "style.css")
c = io.open(css_path, encoding="utf-8").read()

c = c.replace("""  width: auto;
  height: 52px;
  transition: height var(--f-base);""",
"""  width: auto;
  height: 42px;
  transition: height var(--f-base);""")
c = c.replace(".site-header.is-scrolled .brand img { height: 44px; }",
              ".site-header.is-scrolled .brand img { height: 36px; }")
c = c.replace(".footer__brand img { width: 148px; height: auto; }",
""".footer__logo {
  display: inline-block;
  background: #fff;
  padding: 15px 18px;
}
.footer__logo img { display: block; width: 176px; height: auto; }""")

io.open(css_path, "w", encoding="utf-8").write(c)
print("css updated")

# --- drop files that are no longer referenced
for name in ("logo-light.png", "favicon.svg", "_footer-logo-compare.png"):
    p = os.path.join(ROOT, "assets", "img", name)
    if os.path.exists(p):
        os.remove(p)
        print("removed", name)
