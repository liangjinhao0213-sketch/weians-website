# -*- coding: utf-8 -*-
"""Build the case study pages: /cases/ index plus one page per project."""
import io
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
import build_about as A  # noqa: E402
import cases_data as D  # noqa: E402

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
OUT = os.path.join(ROOT, "cases")

ARROW = ('<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
         '<path d="M2 8h11M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.4"/></svg>')


def head(meta, depth):
    pre = "../" * depth
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0B2B5B">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{pre}assets/img/og-image.jpg">
<link rel="icon" href="{pre}assets/img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="{pre}assets/img/apple-touch-icon.png">
<link rel="stylesheet" href="{pre}assets/css/style.css?v={ver}">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
""".format(pre=pre, ver=int(os.path.getmtime(os.path.join(ROOT, "assets", "css", "style.css"))), **meta)


def chrome(depth, active=True):
    """Case pages live at cases/*.html, i.e. depth 1 - same as the products index."""
    parts = dict(A.CHROME)
    if active:
        parts["header"] = parts["header"].replace(
            '<a class="nav__link" href="../cases/index.html">Cases</a>',
            '<a class="nav__link is-active" href="../cases/index.html">Cases</a>')
    return parts


def quote_modal():
    return A.CHROME["toast"]


def close_page(depth):
    parts = chrome(depth)
    pre = "../" * depth
    return (parts["footer"] + parts["floating"] + parts["toast"] +
            '\n<script src="%sassets/js/main.js" defer></script>\n</body>\n</html>\n' % pre)


def build_index():
    parts = chrome(1)
    cards = []
    for c in D.CASES:
        cards.append("""        <a class="case-card reveal" href="%s.html">
          <span class="case-card__media" style="aspect-ratio:%s"><img src="../assets/img/%s" alt="%s — %s" loading="lazy"></span>
          <span class="case-card__body">
            <span class="case-card__loc">%s</span>
            <span class="case-card__title">%s</span>
            <span class="case-card__meta"><em>%s</em><span>%s</span></span>
            <span class="case-card__more">Read the case %s</span>
          </span>
        </a>""" % (c["slug"], c["ratio"], c["image"], c["location"], c["system"],
                   c["location"], c["title"], c["type"], c["system"], ARROW))

    body = """<section class="page-hero page-hero--cases">
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="../index.html">Home</a><i>/</i><span aria-current="page">Cases</span></nav>
    <div class="page-hero__grid">
      <div class="page-hero__main">
        <p class="eyebrow"><span class="eyebrow__no">Cases</span>Selected projects</p>
        <h1 class="page-hero__title">Supplied, shipped.<br><span class="hl">Installed and standing.</span></h1>
        <p class="page-hero__lead">Six projects from four continents — villas, a hotel, offices, a facade. Each one went out as finished units from Foshan and was installed by a local team.</p>
      </div>
      <div class="page-hero__aside">
        <dl class="blog-meta">
          <div><dt>Projects</dt><dd>6 shown</dd></div>
          <div><dt>Markets</dt><dd>US · AU · UK · JP · AE</dd></div>
          <div><dt>Types</dt><dd>Residential · Commercial · Hospitality</dd></div>
        </dl>
      </div>
    </div>
  </div>
</section>

<section class="section--tight">
  <div class="container">
    <div class="case-grid">
%s
    </div>
  </div>
</section>

<section class="section section--offwhite">
  <div class="container">
    <div class="cta-strip reveal">
      <div>
        <p class="eyebrow"><span class="eyebrow__no">Next</span>Your project</p>
        <h2 class="h3">Send the drawings. We will quote it the same way.</h2>
      </div>
      <a class="btn" href="../contact-us/index.html">Talk to the factory %s</a>
    </div>
  </div>
</section>""" % ("\n".join(cards), ARROW)

    meta = dict(title="Cases | Weinas Aluminium Windows &amp; Doors",
                desc=("Six delivered projects: coastal villas, offices in Tokyo, a Dubai facade, a London "
                      "garden extension and a Byron Bay hotel. Aluminium systems from Weinas, Foshan."),
                canonical="https://www.weinas.com/cases/")
    page = head(meta, 1) + parts["header"] + parts["mobile"] + parts["search"]
    page += '<main id="main">\n' + body + '\n</main>\n' + close_page(1)
    os.makedirs(OUT, exist_ok=True)
    io.open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(page)
    return len(page)


def build_case(c):
    parts = chrome(1)
    idx = [x["slug"] for x in D.CASES].index(c["slug"])
    prev_c = D.CASES[idx - 1] if idx else None
    next_c = D.CASES[idx + 1] if idx + 1 < len(D.CASES) else None

    pager = ['<nav class="catpager" aria-label="Case studies">']
    if prev_c:
        pager.append('<a href="%s.html"><small>Previous</small>← %s</a>' % (prev_c["slug"], prev_c["location"]))
    else:
        pager.append('<a href="index.html"><small>Back</small>← All cases</a>')
    if next_c:
        pager.append('<a href="%s.html" style="text-align:right"><small>Next</small>%s →</a>' % (next_c["slug"], next_c["location"]))
    pager.append("</nav>")

    c["title_html"] = c["title"].replace(c["hl"], '<span class="hl">%s</span>' % c["hl"]) if c.get("hl") else c["title"]
    facts = "".join("<div><dt>%s</dt><dd>%s</dd></div>" % (k, v) for k, v in c["facts"])
    blocks = "".join("<h2 class=\"case__h\">%s</h2>\n        <p>%s</p>\n        " % (h, t) for h, t in c["body"])
    others = [x for x in D.CASES if x["slug"] != c["slug"]][:3]
    other_cards = "\n".join("""        <a class="case-card case-card--sm reveal" href="%s.html">
          <span class="case-card__media" style="aspect-ratio:4 / 3"><img src="../assets/img/%s" alt="%s" loading="lazy"></span>
          <span class="case-card__body">
            <span class="case-card__loc">%s</span>
            <span class="case-card__title">%s</span>
            <span class="case-card__meta"><em>%s</em><span>%s</span></span>
          </span>
        </a>""" % (o["slug"], o["image"], o["location"], o["location"], o["title"], o["type"], o["system"]) for o in others)

    body = """<section class="page-hero page-hero--case">
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="../index.html">Home</a><i>/</i><a href="index.html">Cases</a><i>/</i><span aria-current="page">%s</span>
    </nav>
    <div class="page-hero__grid">
      <div class="page-hero__main">
        <p class="eyebrow"><span class="eyebrow__no">%s</span>%s</p>
        <h1 class="page-hero__title">%s</h1>
        <p class="page-hero__lead">%s</p>
      </div>
      <div class="page-hero__aside">
        <ul class="chiprow"><li>%s</li><li>%s</li><li>%s</li></ul>
      </div>
    </div>
  </div>
</section>

<figure class="case-hero">
  <img src="../assets/img/%s" alt="%s" width="1600" height="1000">
</figure>

<section class="section--tight">
  <div class="container">
    <dl class="case-facts">%s</dl>
    <div class="case-grid case-grid--2">
      <div class="case-body">
        %s
      </div>
      <aside class="case-side">
        <p class="case-side__k">System used</p>
        <a class="case-side__link" href="../products/%s/index.html">%s %s</a>
        <p class="case-side__note">Datasheets, CAD and glass build-ups for this system are on the product page.</p>
        <a class="btn btn--line" href="../contact-us/index.html">Ask about a similar project</a>
      </aside>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    %s
  </div>
</section>

<section class="section section--offwhite">
  <div class="container">
    <div class="section-head reveal">
      <div class="section-head__main">
        <p class="eyebrow"><span class="eyebrow__no">More</span>Case studies</p>
        <h2 class="h2">Three more projects.</h2>
      </div>
      <a class="link-arrow" href="index.html">All cases %s</a>
    </div>
    <div class="case-grid case-grid--3">
%s
    </div>
  </div>
</section>""" % (c["location"], c["no"], c["type"], c["title_html"], c["lead"],
                 c["type"], c["system"], c["country"],
                 c["image"], c["location"], facts, blocks,
                 c["system_slug"], c["system"], "", "\n".join(pager), ARROW, other_cards)

    # the pager markup was passed as an empty slot; append it properly
    body = body.replace("</section>%s" % "", "</section>")
    meta = dict(title="%s | Weinas Cases" % c["location"],
                desc=c["lead"][:170],
                canonical="https://www.weinas.com/cases/%s.html" % c["slug"])
    page = head(meta, 1) + parts["header"] + parts["mobile"] + parts["search"]
    page += '<main id="main">\n' + body + "\n</main>\n" + close_page(1)
    io.open(os.path.join(OUT, c["slug"] + ".html"), "w", encoding="utf-8").write(page)
    return len(page)


if __name__ == "__main__":
    total = build_index()
    for c in D.CASES:
        total += build_case(c)
    print("built cases/index.html + %d case pages (%.0f KB)" % (len(D.CASES), total / 1024))
