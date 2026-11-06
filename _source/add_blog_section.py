# -*- coding: utf-8 -*-
"""Homepage: rename News -> Blog, add the Journal section with the 3 newest posts."""
import io
import json
import os

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
PAGE = os.path.join(ROOT, "index.html")
POSTS = json.load(io.open(os.path.join(ROOT, "_source", "posts.json"), encoding="utf-8"))

ARROW = ('<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
         '<path d="M2 8h11M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.4"/></svg>')

s = io.open(PAGE, encoding="utf-8").read()

# ---------------------------------------------------------------- 1. News -> Blog
OLD_NAV = '<li><a class="nav__link" href="/news/" data-coming-soon>News</a></li>'
NEW_NAV = '<li><a class="nav__link" href="blog/index.html">Blog</a></li>'
if OLD_NAV in s:
    s = s.replace(OLD_NAV, NEW_NAV)
    print("desktop nav renamed")
elif NEW_NAV not in s:
    raise SystemExit("desktop News link not found")

OLD_PLAIN = '<li><a href="/news/" data-coming-soon>News</a></li>'
NEW_PLAIN = '<li><a href="blog/index.html">Blog</a></li>'
if OLD_PLAIN in s:
    s = s.replace(OLD_PLAIN, NEW_PLAIN)
    print("mobile + footer links renamed")

# --------------------------------------------------------- 2. Journal section
if 'id="journal"' not in s:
    cards = []
    for i, post in enumerate(POSTS[:3]):
        cards.append("""      <a class="post reveal" href="blog/{slug}.html" style="--delay:{delay}ms">
        <span class="post__media"><img src="assets/img/{image}" alt="{alt}" loading="lazy" width="900" height="600"></span>
        <span class="post__meta"><span>{date}</span><span>{category}</span></span>
        <h3 class="post__title">{title}</h3>
        <p class="post__excerpt">{excerpt}</p>
        <span class="post__more">Read article {arrow}</span>
      </a>""".format(slug=post["slug"], delay=i * 80, image=post["image"],
                     alt=post["title"].replace('"', "&quot;"), date=post["date"],
                     category=post["category"], title=post["title"],
                     excerpt=post["excerpt"], arrow=ARROW))

    section = """<section class="section" id="journal">
  <div class="container">
    <div class="section-head reveal">
      <div class="section-head__main">
        <p class="eyebrow"><span class="eyebrow__no">08</span>Journal</p>
        <h2 class="h2">Notes from the factory.</h2>
      </div>
      <div class="section-head__aside">
        <p class="lead">Drainage, wall thickness, gaskets — the details that decide whether an opening still closes properly in year five.</p>
        <a class="link-arrow" href="blog/index.html">All articles """ + ARROW + """</a>
      </div>
    </div>
    <div class="post-grid">
""" + "\n".join(cards) + """
    </div>
  </div>
</section>

"""

    anchor = '<section class="section section--offwhite" id="quote">'
    if anchor not in s:
        raise SystemExit("quote section anchor not found")
    s = s.replace(anchor, section + anchor, 1)
    print("journal section inserted")

    # quote becomes 09
    s = s.replace('<p class="eyebrow"><span class="eyebrow__no">08</span>Start a project</p>',
                  '<p class="eyebrow"><span class="eyebrow__no">09</span>Start a project</p>')
    print("quote renumbered to 09")

io.open(PAGE, "w", encoding="utf-8").write(s)
print("index.html updated")
