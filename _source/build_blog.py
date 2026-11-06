# -*- coding: utf-8 -*-
"""Build the Journal: blog index + one page per article.

Chrome (header / footer / search / floating CTA) and shared blocks come from
build_about.py, which extracts them from index.html.
"""
import io


def _accent(title, phrase):
    """Wrap an accent phrase inside a title with the navy highlight span."""
    if phrase and phrase in title:
        return title.replace(phrase, "<span class='hl'>%s</span>" % phrase, 1)
    return title
import json
import os

import build_about as A

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
OUT = os.path.join(ROOT, "blog")
os.makedirs(OUT, exist_ok=True)

POSTS = json.load(io.open(os.path.join(ROOT, "_source", "posts.json"), encoding="utf-8"))
ARROW = ('<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
         '<path d="M2 8h11M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.4"/></svg>')

HEADER = A.CHROME["header"]
HEADER = HEADER.replace('class="nav__link" href="../blog/index.html"',
                        'class="nav__link is-active" href="../blog/index.html"')


def head(title, desc, canonical, og_type="website", published=None):
    extra = ""
    if published:
        extra = '\n<meta property="article:published_time" content="%s">' % published
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0B2B5B">
<!-- TODO(上线前): 域名确定后，替换 canonical / og:url / JSON-LD / robots.txt / sitemap.xml 里的 www.weinas.com -->
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Weinas Window &amp; Door Co., Ltd.">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="../assets/img/og-image.jpg">
<meta property="og:url" content="{canonical}">{extra}
<link rel="icon" href="../assets/img/favicon.png" type="image/png" sizes="64x64">
<link rel="apple-touch-icon" href="../assets/img/apple-touch-icon.png">
<link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
""".format(title=title, desc=desc, canonical=canonical, og_type=og_type, extra=extra)


def breadcrumb(items):
    parts = []
    for i, (label, href) in enumerate(items):
        if href:
            parts.append('<a href="%s">%s</a>' % (href, label))
        else:
            parts.append('<span aria-current="page">%s</span>' % label)
    return '<nav class="breadcrumb" aria-label="Breadcrumb">%s</nav>' % "<i>/</i>".join(parts)


def shell(head_html, body, ld):
    return (head_html + HEADER + A.CHROME["mobile"] + A.CHROME["search"]
            + '<main id="main">\n' + body + '\n</main>\n'
            + A.CHROME["footer"] + A.CHROME["floating"] + "\n" + A.CHROME["toast"] + "\n"
            + '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=2)
            + '\n</script>\n<script src="../assets/js/main.js" defer></script>\n</body>\n</html>\n')


def post_card(post, delay=0, heading="h3"):
    return """      <a class="post reveal" href="{slug}.html" style="--delay:{delay}ms">
        <span class="post__media"><img src="../assets/img/{image}" alt="{alt}" loading="lazy" width="900" height="600"></span>
        <span class="post__meta"><span>{date}</span><span>{category}</span></span>
        <{h} class="post__title">{title}</{h}>
        <p class="post__excerpt">{excerpt}</p>
        <span class="post__more">Read article {arrow}</span>
      </a>""".format(slug=post["slug"], delay=delay, image=post["image"],
                     alt=post["title"].replace('"', "&quot;"), date=post["date"],
                     category=post["category"], h=heading, title=post["title"],
                     excerpt=post["excerpt"], arrow=ARROW)


# ------------------------------------------------------------------- index
def build_index():
    posts = POSTS
    featured = posts[0]
    rest = posts[1:]

    body = """<section class="page-hero page-hero--blog">
  <div class="container">
    {crumb}
    <div class="page-hero__grid">
      <div class="page-hero__main">
        <p class="eyebrow"><span class="eyebrow__no">Blog</span>Journal</p>
        <h1 class="page-hero__title">Notes from <span class='hl'>the factory</span>.</h1>
        <p class="page-hero__lead">What we learn building aluminium openings: drainage under typhoon rain, wall thickness at height, gaskets that keep a door quiet. Written on the floor, not in a brochure.</p>
      </div>
      <div class="page-hero__aside">
        <dl class="blog-meta">
          <div><dt>Articles</dt><dd>{count:02d}</dd></div>
          <div><dt>Latest</dt><dd>{latest}</dd></div>
          <div><dt>Topics</dt><dd>Water · Structure · Systems · Finishes</dd></div>
        </dl>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <a class="featured reveal" href="{f_slug}.html">
      <span class="featured__media"><img src="../assets/img/{f_image}" alt="{f_alt}" width="1400" height="875"></span>
      <span class="featured__body">
        <span class="featured__meta"><em>Latest</em><span>{f_date}</span><span>{f_category}</span></span>
        <h2 class="featured__title">{f_title}</h2>
        <p class="featured__excerpt">{f_excerpt}</p>
        <span class="post__more">Read article {arrow}</span>
      </span>
    </a>
  </div>
</section>

<section class="section section--offwhite">
  <div class="container">
    <div class="section-head reveal">
      <div class="section-head__main">
        <p class="eyebrow"><span class="eyebrow__no">02</span>Archive</p>
        <h2 class="h2">More from the <span class='hl'>journal</span>.</h2>
      </div>
      <div class="section-head__aside">
        <p class="lead">Technical notes and factory news, newest first.</p>
      </div>
    </div>
    <div class="blog-grid">
{cards}
    </div>
  </div>
</section>

{cta}""".format(
        crumb=breadcrumb([("Home", "../index.html"), ("Blog", None)]),
        count=len(posts), latest=posts[0]["date"],
        f_slug=featured["slug"], f_image=featured["image"],
        f_alt=featured["title"].replace('"', "&quot;"), f_date=featured["date"],
        f_category=featured["category"], f_title=featured["title"], f_excerpt=featured["excerpt"],
        arrow=ARROW,
        cards="\n".join(post_card(p, i * 70) for i, p in enumerate(rest)),
        cta=A.cta(),
    )

    ld = {
        "@context": "https://schema.org",
        "@type": "Blog",
        "name": "Weinas Journal",
        "url": "https://www.weinas.com/blog/",
        "blogPost": [
            {"@type": "BlogPosting", "headline": p["title"],
             "datePublished": p["date_iso"],
             "url": "https://www.weinas.com/blog/%s.html" % p["slug"]} for p in posts
        ],
    }
    html = shell(head("Blog | Weinas Journal — aluminium windows &amp; doors",
                      "Technical notes and factory news from Weinas: drainage systems, wind pressure, "
                      "wall thickness, sealing and finishes for aluminium windows and doors.",
                      "https://www.weinas.com/blog/"), body, ld)
    io.open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)
    print("wrote blog/index.html")


# ----------------------------------------------------------------- articles
def build_article(post, prev_post, next_post):
    first = post["blocks"][0]["text"] if post["blocks"] else ""
    standfirst = first
    for stop in (". ", "? ", "! "):
        idx = first.find(stop)
        if 40 < idx < 220:
            standfirst = first[: idx + 1]
            break
    if len(standfirst) > 220:
        standfirst = standfirst[: standfirst.rfind(" ", 0, 217)] + "…"

    blocks = []
    for i, b in enumerate(post["blocks"]):
        if b["kind"] == "h2":
            blocks.append("<h2>%s</h2>" % b["text"])
        else:
            cls = ' class="is-lead"' if i == 0 else ""
            blocks.append("<p%s>%s</p>" % (cls, b["text"]))

    prev_html = ""
    next_html = ""
    if prev_post:
        prev_html = ('<a href="%s.html"><small>Previous</small>← %s</a>'
                     % (prev_post["slug"], prev_post["title"][:60]))
    if next_post:
        next_html = ('<a href="%s.html" style="text-align:right"><small>Next</small>%s →</a>'
                     % (next_post["slug"], next_post["title"][:60]))

    body = """<section class="page-hero page-hero--article">
  <div class="container">
    {crumb}
    <div class="page-hero__main">
      <p class="eyebrow"><span class="eyebrow__no">{category}</span>{date}</p>
      <h1 class="page-hero__title">{title_html}</h1>
      <p class="page-hero__lead">{excerpt}</p>
    </div>
  </div>
</section>

<figure class="article-hero">
  <img src="../assets/img/{image}" alt="{alt}" width="1400" height="933">
</figure>

<section class="section">
  <div class="container">
    <div class="article-body reveal">
{blocks}
      <div class="article-foot">
        <a href="index.html"><small>Journal</small>← All articles</a>
        {next}
      </div>
    </div>
  </div>
</section>

{cta}""".format(
        crumb=breadcrumb([("Home", "../index.html"), ("Blog", "index.html"),
                          (post["title"][:42] + ("…" if len(post["title"]) > 42 else ""), None)]),
        category=post["category"], date=post["date"], title_html=_accent(post["title"], post.get("accent", "")),
        excerpt=standfirst, image=post["image"],
        alt=post["title"].replace('"', "&quot;"),
        blocks="\n".join("      " + b for b in blocks),
        next=next_html,
        cta=A.cta(),
    )

    ld = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post["title"],
        "datePublished": post["date_iso"],
        "image": "https://www.weinas.com/assets/img/" + post["image"],
        "author": {"@type": "Organization", "name": "Weinas Window & Door Co., Ltd."},
        "publisher": {"@type": "Organization", "name": "Weinas Window & Door Co., Ltd."},
        "mainEntityOfPage": "https://www.weinas.com/blog/%s.html" % post["slug"],
    }
    html = shell(head("%s | Weinas Journal" % post["title"].replace("&", "&amp;"),
                      post["excerpt"].replace('"', "&quot;"),
                      "https://www.weinas.com/blog/%s.html" % post["slug"],
                      og_type="article", published=post["date_iso"]),
                 body, ld)
    io.open(os.path.join(OUT, "%s.html" % post["slug"]), "w", encoding="utf-8").write(html)
    print("wrote blog/%s.html" % post["slug"])


if __name__ == "__main__":
    build_index()
    for i, post in enumerate(POSTS):
        newer = POSTS[i - 1] if i > 0 else None
        older = POSTS[i + 1] if i + 1 < len(POSTS) else None
        build_article(post, newer, older)
