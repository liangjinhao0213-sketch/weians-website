# -*- coding: utf-8 -*-
"""Wire the new Contact page into the shared chrome: nav links, footer social row."""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import icons  # noqa: E402

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
PAGE = os.path.join(ROOT, "index.html")

s = io.open(PAGE, encoding="utf-8").read()

# ---------------------------------------------------------- Contact Us -> page
REPL = [
    ('<li><a class="nav__link" href="#quote" data-spy>Contact Us</a></li>',
     '<li><a class="nav__link" href="contact-us/index.html">Contact Us</a></li>'),
    ('<li><a href="#quote">Contact Us</a></li>',
     '<li><a href="contact-us/index.html">Contact Us</a></li>'),
]
for old, new in REPL:
    if old in s:
        s = s.replace(old, new)
        print("link replaced:", old[:52])

# ------------------------------------------------------- footer social = 5 icons
social_links = []
for key, label, path, href, note in icons.SOCIALS:
    extra = ' data-coming-soon data-toast="%s — profile link to be added."' % note if note else ""
    social_links.append(
        '          <a class="footer__social-link footer__social-link--%s" href="%s" target="_blank" '
        'rel="noopener" aria-label="%s"%s><svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true">%s</svg></a>'
        % (key, href, label, extra, path))

start = s.index('<div class="footer__social">')
end = s.index("</div>", start) + len("</div>")
s = s[:start] + '<div class="footer__social">\n' + "\n".join(social_links) + "\n        </div>" + s[end:]

io.open(PAGE, "w", encoding="utf-8").write(s)
print("footer social replaced with", len(social_links), "links")
