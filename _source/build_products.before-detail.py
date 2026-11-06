# -*- coding: utf-8 -*-
"""Build the products section: index, 12 category pages, product detail pages.

Layout notes
- cards use .ph placeholder blocks (dashed inner frame + label) until real images land
- every quote button opens one shared modal, populated from data-* attributes
- headings reuse the two-tone .hl accent
"""
import io
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
import build_about as A  # noqa: E402
import products_data as D  # noqa: E402
import apply_source_products as SRCP  # noqa: E402

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
OUT = os.path.join(ROOT, "products")

ARROW = ('<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
         '<path d="M2 8h11M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.4"/></svg>')

CATS = {c["slug"]: c for c in D.CATEGORIES}
GROUP_NAME = {g[0]: g[1] for g in D.GROUPS}


def chrome(depth):
    """Header/footer markup rebased to the page depth (1 = /products/, 2 = /products/x/)."""
    parts = dict(A.CHROME)
    # Products is the current section here -- mark it before the depth rebase
    parts["header"] = parts["header"].replace(
        '<a class="nav__link" href="../products/index.html" aria-haspopup="true"',
        '<a class="nav__link is-active" href="../products/index.html" aria-haspopup="true"')
    if depth > 1:
        for k in ("header", "mobile", "search", "footer", "floating"):
            parts[k] = parts[k].replace('"../', '"../../')
    return parts


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
<link rel="stylesheet" href="{pre}assets/css/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
""".format(pre=pre, **meta)


def breadcrumb(items):
    out = ['<nav class="breadcrumb" aria-label="Breadcrumb">']
    for i, (label, href) in enumerate(items):
        if i:
            out.append("<i>/</i>")
        if href:
            out.append('<a href="%s">%s</a>' % (href, label))
        else:
            out.append('<span aria-current="page">%s</span>' % label)
    out.append("</nav>")
    return "".join(out)


def ph(label, sub, ratio="4 / 3", cls=""):
    return ('<span class="ph %s" style="aspect-ratio:%s"><span class="ph__label">'
            '<b>%s</b>%s</span></span>' % (cls, ratio, label, sub))


def quote_btn(product, cls="btn pcard__quote"):
    import json
    import html as H
    name, code = product["full_name"], product["code"]
    specs = product["modal_specs"]
    data = H.escape(json.dumps(specs, ensure_ascii=False), quote=True)
    return ('<button class="%s" type="button" data-quote data-name="%s" data-code="%s" data-specs="%s">'
            'Get a quote %s</button>' % (cls, H.escape(name), code, data, ARROW))


MODAL = """<div class="qmodal" id="qmodal" hidden>
  <div class="qmodal__backdrop" data-close></div>
  <div class="qmodal__panel" role="dialog" aria-modal="true" aria-labelledby="qm-title">
    <button class="qmodal__close" type="button" data-close aria-label="Close quotation form">
      <svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 3l10 10M13 3L3 13" stroke="currentColor" stroke-width="1.5"/></svg>
    </button>
    <div class="qmodal__side">
      <p class="qmodal__kicker">Key configuration</p>
      <h2 class="qmodal__title" id="qm-title" data-qm-title>Product</h2>
      <p class="qmodal__code" data-qm-code>—</p>
      <dl class="qmodal__specs" data-qm-specs></dl>
      <p class="qmodal__note">Glass build-ups, hardware schedule, CAD and the full datasheet travel with the quotation.</p>
    </div>
    <div class="qmodal__body">
      <p class="qmodal__kicker">Request a quotation</p>
      <h3 class="qmodal__h">Tell us the quantity and the destination.</h3>
      <form class="qform" id="qm-form" novalidate>
        <div class="qform__row">
          <label class="qfield"><span>Name *</span><input name="name" type="text" required autocomplete="name" placeholder="Your name"></label>
          <label class="qfield"><span>Company</span><input name="company" type="text" autocomplete="organization" placeholder="Company / studio"></label>
        </div>
        <div class="qform__row">
          <label class="qfield"><span>Email *</span><input name="email" type="email" required autocomplete="email" placeholder="name@company.com"></label>
          <label class="qfield"><span>WhatsApp</span><input name="whatsapp" type="tel" autocomplete="tel" placeholder="+1 555 000 0000"></label>
        </div>
        <label class="qfield"><span>Message</span><textarea name="message" id="qm-message" rows="3"></textarea></label>
        <p class="qform__status" id="qm-status" role="status" hidden></p>
        <div class="qform__foot">
          <p class="qform__note">Reply within one business day. No third-party marketing.</p>
          <button class="btn" type="submit">Send enquiry %s</button>
        </div>
      </form>
    </div>
  </div>
</div>""" % ARROW


def close_page(depth, extra_scripts=""):
    parts = chrome(depth)
    pre = "../" * depth
    return (parts["footer"] + parts["floating"] + parts["toast"] + MODAL +
            '\n<script src="%sassets/js/main.js" defer></script>%s\n</body>\n</html>\n' % (pre, extra_scripts))


# ---------------------------------------------------------------- index page
# curated category photos (the same ones the homepage category grid uses);
# categories without one fall back to their first product photo
CAT_PHOTO = {
    "aluminium-sliding-doors": "products-photo/sliding-doors.jpg",
    "aluminium-casement-windows": "products-photo/casement-windows.jpg",
    "aluminium-sliding-windows": "products-photo/sliding-windows.jpg",
    "interior-sliding-partition-doors": "products-photo/interior-partition.jpg",
    "aluminium-casement-doors": "products-photo/casement-doors.jpg",
    "aluminium-tilt-and-turn-windows": "products-photo/tilt-turn-windows.jpg",
    "thermal-insulation-windows": "products-photo/thermal-windows.jpg",
    "aluminium-folding-doors": "products-photo/folding-doors.jpg",
    "aluminium-swing-doors": "products-photo/swing-doors.jpg",
    "aluminium-bathroom-doors": "products-photo/bathroom-doors.jpg",
    "aluminium-front-doors": "products-photo/front-doors.jpg",
    "aluminium-pivot-doors": "products-photo/pivot-doors.jpg",
}


def cat_media(c):
    """Category cover: curated photo, else the first product photo, else a placeholder."""
    src = CAT_PHOTO.get(c["slug"])
    if not src:
        for p in c.get("products_full", []):
            if p.get("image") and os.path.exists(os.path.join(ROOT, "assets", "img", p["image"].replace("/", os.sep))):
                src = p["image"]
                break
    if src:
        return '<img src="../assets/img/%s" alt="%s" loading="lazy">' % (src, c["name"])
    return ph(c["short"] + " image", "1600 × 1200")
def build_index():
    parts = chrome(1)
    groups_html = []
    for gi, (gkey, gname, gline) in enumerate(D.GROUPS):
        cats = [c for c in D.CATEGORIES if c["group"] == gkey]
        cards = []
        for c in cats:
            cards.append("""        <a class="ccard reveal" href="%s/index.html">
          <span class="ccard__media">%s</span>
          <span class="ccard__body">
            <span class="ccard__no">%s</span>
            <h3 class="ccard__name">%s</h3>
            <p class="ccard__line">%s</p>
            <span class="ccard__meta">%d systems · %s</span>
            <span class="ccard__more">View more %s</span>
          </span>
        </a>""" % (c["slug"], cat_media(c), c["no"], c["name"],
                   c["tagline"], len(c["products"]), c["chips"][0], ARROW))
        groups_html.append("""<section class="section" id="g-%s">
  <div class="container">
    <div class="section-head reveal">
      <div class="section-head__main">
        <p class="eyebrow"><span class="eyebrow__no">0%d</span>%s</p>
        <h2 class="h2">%s</h2>
      </div>
      <p class="section-head__note">%s</p>
    </div>
    <div class="catgrid">
%s
    </div>
  </div>
</section>""" % (gkey, gi + 1, gname, gname + ".<br><span class='hl'>%d systems.</span>" % len(cats),
                 gline, "\n".join(cards)))

    body = """<section class="page-hero page-hero--products">
  <div class="container">
    %s
    <div class="page-hero__grid">
      <div class="page-hero__main">
        <p class="eyebrow"><span class="eyebrow__no">Products</span>12 categories</p>
        <h1 class="page-hero__title">Every opening.<br><span class="hl">One engineering standard.</span></h1>
        <p class="page-hero__lead">Doors, windows and partitions built from our own extrusion in Foshan — grouped by how they open, so you can compare like with like.</p>
      </div>
      <div class="page-hero__aside">
        <dl class="blog-meta">
          <div><dt>Categories</dt><dd>12</dd></div>
          <div><dt>Configurations</dt><dd>72</dd></div>
          <div><dt>Lead time</dt><dd>25–40 days</dd></div>
        </dl>
      </div>
    </div>
    <nav class="groupbar" aria-label="Product groups">
%s
    </nav>
  </div>
</section>

%s

<section class="section section--offwhite">
  <div class="container">
    <div class="cta-strip reveal">
      <div>
        <p class="eyebrow"><span class="eyebrow__no">?</span>Not sure which system</p>
        <h2 class="h3">Send the drawing. We will tell you what fits.</h2>
      </div>
      <a class="btn" href="../contact-us/index.html">Talk to the factory %s</a>
    </div>
  </div>
</section>""" % (breadcrumb([("Home", "../index.html"), ("Products", None)]),
                 "\n".join('    <a href="#g-%s">%s <span>%d</span></a>' % (g[0], g[1], len([c for c in D.CATEGORIES if c["group"] == g[0]]))
                           for g in D.GROUPS),
                 "\n\n".join(groups_html), ARROW)

    meta = dict(title="Products | Weinas Aluminium Windows &amp; Doors",
                desc=("Twelve aluminium systems from Weinas: sliding doors and windows, casement, "
                      "tilt and turn, thermal, swing, entrance, pivot and folding doors. "
                      "Factory-direct from Foshan."),
                canonical="https://www.weinas.com/products/")
    page = head(meta, 1) + parts["header"] + parts["mobile"] + parts["search"]
    page += '<main id="main">\n' + body + '\n</main>\n' + close_page(1)
    os.makedirs(OUT, exist_ok=True)
    io.open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(page)
    return len(page)


# ------------------------------------------------------------- category page
def build_category(cat):
    parts = chrome(2)
    cards = []
    for i, p in enumerate(cat["products_full"]):
        cards.append("""      <article class="pcard reveal">
        <a class="pcard__media" href="%s.html">%s</a>
        <div class="pcard__body">
          <p class="pcard__code">%s</p>
          <h3 class="pcard__name"><a href="%s.html">%s</a></h3>
          <p class="pcard__line">%s</p>
          <dl class="pcard__specs">
            <div><dt>%s</dt><dd>%s</dd></div>
            <div><dt>%s</dt><dd>%s</dd></div>
          </dl>
          <div class="pcard__actions">
            <a class="btn btn--line" href="%s.html">View details</a>
            %s
          </div>
        </div>
      </article>""" % (p["slug"], (('<img src="../../assets/img/%s" alt="%s" loading="lazy">' % (p["image"], p["full_name"])) if p.get("image") else ph(p["code"] + " image", "1400 × 1050", "4 / 3")),
                       p["code"], p["slug"], p["name"], p["blurb"],
                       p["extra"][0][0], p["extra"][0][1],
                       p["extra"][1][0], p["extra"][1][1],
                       p["slug"], quote_btn(p)))

    idx = [c["slug"] for c in D.CATEGORIES].index(cat["slug"])
    prev_cat = D.CATEGORIES[idx - 1] if idx else None
    nxt = D.CATEGORIES[idx + 1] if idx + 1 < len(D.CATEGORIES) else None
    pager = ['<nav class="catpager" aria-label="Categories">']
    if prev_cat:
        pager.append('<a href="../%s/index.html"><small>Previous</small>← %s</a>' % (prev_cat["slug"], prev_cat["name"]))
    else:
        pager.append('<a href="../index.html"><small>Back</small>← All products</a>')
    if nxt:
        pager.append('<a href="../%s/index.html" style="text-align:right"><small>Next</small>%s →</a>' % (nxt["slug"], nxt["name"]))
    pager.append("</nav>")

    body = """<section class="page-hero page-hero--cat">
  <div class="container">
    %s
    <div class="page-hero__grid">
      <div class="page-hero__main">
        <p class="eyebrow"><span class="eyebrow__no">%s</span>%s</p>
        <h1 class="page-hero__title">%s</h1>
        <p class="page-hero__lead">%s</p>
      </div>
      <div class="page-hero__aside">
        <ul class="chiprow">%s</ul>
      </div>
    </div>
  </div>
</section>

<section class="section--tight">
  <div class="container">
    <div class="pgrid" data-per-page="6">
%s
    </div>
    <nav class="ppager" data-pager aria-label="Product pages"></nav>
  </div>
</section>

<section class="section">
  <div class="container">
    %s
  </div>
</section>""" % (breadcrumb([("Home", "../../index.html"), ("Products", "../index.html"), (cat["name"], None)]),
                 cat["no"], GROUP_NAME[cat["group"]],
                 cat["name"] + "<br><span class='hl'>%d systems.</span>" % len(cat["products"]),
                 cat["lead"],
                 "".join("<li>%s</li>" % c for c in cat["chips"]),
                 "\n".join(cards), "\n".join(pager))

    meta = dict(title="%s | Weinas" % cat["name"],
                desc=cat["lead"][:170],
                canonical="https://www.weinas.com/products/%s/" % cat["slug"])
    page = head(meta, 2) + parts["header"] + parts["mobile"] + parts["search"]
    page += '<main id="main">\n' + body + '\n</main>\n' + close_page(2)
    d = os.path.join(OUT, cat["slug"])
    os.makedirs(d, exist_ok=True)
    io.open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page)
    return len(page)


# -------------------------------------------------------------- product page
def build_product(cat, p):
    parts = chrome(2)
    rows = "".join("<div><dt>%s</dt><dd>%s</dd></div>" % (k, v) for k, v in p["table"])
    options = "".join(
        '<div class="opt"><h4>%s</h4><p>%s</p></div>' % (k, v) for k, v in p["options"])

    desc_block = ""
    if p.get("intro"):
        paras = [p["intro"]] + [b for b in p.get("body", []) if b and b != p["intro"]]
        desc_block = """<section class="section">
  <div class="container">
    <div class="product__desc">
      <h2 class="case__h">Product description</h2>
      %s
    </div>
  </div>
</section>""" % "".join("<p>%s</p>" % t for t in paras[:4])

    related = [x for x in cat["products_full"] if x["slug"] != p["slug"]][:3]
    rel_html = "\n".join("""        <a class="ccard ccard--sm reveal" href="%s.html">
          <span class="ccard__media">%s</span>
          <span class="ccard__body">
            <span class="ccard__no">%s</span>
            <h3 class="ccard__name">%s</h3>
            <span class="ccard__more">View details %s</span>
          </span>
        </a>""" % (r["slug"], (('<img src="../../assets/img/%s" alt="%s" loading="lazy">' % (r["image"], r["full_name"])) if r.get("image") else ph(r["code"] + " image", "800 × 600")), r["code"], r["name"], ARROW)
        for r in related)

    body = """<section class="page-hero page-hero--product">
  <div class="container">
    %s
    <div class="page-hero__grid">
      <div class="page-hero__main">
        <p class="eyebrow"><span class="eyebrow__no">%s</span>%s</p>
        <h1 class="page-hero__title">%s<br><span class="hl">%s</span></h1>
        <p class="page-hero__lead">%s</p>
      </div>
      <div class="page-hero__aside">
        <ul class="chiprow">%s</ul>
      </div>
    </div>
  </div>
</section>

<section class="section--tight">
  <div class="container">
    <div class="product">
      <div class="product__media">
        %s
        <div class="product__thumbs">%s</div>
      </div>
      <div class="product__info">
        <h2 class="product__h">Specification &amp; terms</h2>
        <dl class="spec-table">%s</dl>
        <div class="product__actions">
          %s
          <a class="btn btn--line" href="../../contact-us/index.html">Ask a question</a>
        </div>
        <p class="product__note">Datasheet, CAD block and glass build-up are sent with the quotation.</p>
      </div>
    </div>
  </div>
</section>

<!--DESC-->
<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <div class="section-head__main">
        <p class="eyebrow"><span class="eyebrow__no">Options</span>Configuration</p>
        <h2 class="h2">What you can change.<br><span class="hl">What stays the same.</span></h2>
      </div>
    </div>
    <div class="options">%s</div>
  </div>
</section>

<section class="section section--offwhite">
  <div class="container">
    <div class="section-head reveal">
      <div class="section-head__main">
        <p class="eyebrow"><span class="eyebrow__no">%s</span>Same category</p>
        <h2 class="h2">Other %s.</h2>
      </div>
    </div>
    <div class="catgrid catgrid--3">
%s
    </div>
  </div>
</section>""" % (
        breadcrumb([("Home", "../../index.html"), ("Products", "../index.html"),
                    (cat["name"], "../index.html"), (p["code"], None)]),
        p["code"], cat["name"], p["head"][0], p["head"][1], p["blurb"],
        "".join("<li>%s</li>" % c for c in p["chips"]),
        (('<img src="../../assets/img/%s" alt="%s" loading="lazy">' % (p["image"], p["full_name"])) if p.get("image")
         else ph(p["code"] + " — main image", "1600 × 1400", "4 / 5")),
        "".join(ph("Detail %d" % (i + 1), "600 × 600", "1 / 1", "ph--sm") for i in range(3)) if not p.get("image") else "",
        rows,
        quote_btn(p, cls="btn product__quote"),
        options,
        cat["no"], cat["short"].lower(), rel_html)

    body = body.replace("<!--DESC-->", desc_block)

    meta = dict(title="%s %s | Weinas" % (p["code"], p["name"]),
                desc=p["blurb"],
                canonical="https://www.weinas.com/products/%s/%s.html" % (cat["slug"], p["slug"]))
    page = head(meta, 2) + parts["header"] + parts["mobile"] + parts["search"]
    page += '<main id="main">\n' + body + '\n</main>\n' + close_page(2)
    io.open(os.path.join(OUT, cat["slug"], p["slug"] + ".html"), "w", encoding="utf-8").write(page)
    return len(page)


# ------------------------------------------------------------------ prepare
def slugify(text):
    out = []
    for ch in text.lower():
        if ch.isalnum():
            out.append(ch)
        elif ch in " -/&":
            out.append("-")
    s = "".join(out)
    while "--" in s:
        s = s.replace("--", "-")
    return s.strip("-")


def enrich():
    for cat in D.CATEGORIES:
        for (code, name, blurb, extra, sizes) in cat["products"]:
            p = dict(code=code, name=name, blurb=blurb, extra=extra, sizes=sizes)
            p["slug"] = slugify(code + " " + name)
            p["full_name"] = "%s %s" % (code, name)
            words = name.split()
            cut = len(words) - (2 if len(words) >= 3 else 1)
            p["head"] = (" ".join(words[:cut]), " ".join(words[cut:]))
            p["chips"] = [extra[0][1] if "kg" not in extra[0][1] else extra[0][1],
                          cat["chips"][1], sizes]
            p["table"] = [
                ("Model", code),
                ("System", name),
                ("Profile alloy", cat["base"][0][1]),
                ("Thermal break", cat["base"][1][1]),
                ("Glazing", cat["base"][2][1]),
                ("Hardware", cat["base"][3][1]),
                ("Max size", sizes),
            ] + list(extra)
            p["options"] = [
                ("Opening", "%s · %s" % (name.split()[0], extra[-1][1])),
                ("Glazing", cat["base"][2][1] + " — low-E, laminated or silk-screen on request"),
                ("Finish", "Powder coat in any RAL, anodised, or wood-grain transfer"),
                ("Hardware", cat["base"][3][1] + " — German brands, RC2 upgrade available"),
                ("Size", "Made to the opening: %s" % sizes),
                ("Delivery", "25–40 days ex-works, FOB Foshan or CIF to your port"),
            ]
            p["modal_specs"] = [
                ["Model", code],
                ["Profile", cat["base"][0][1]],
                ["Glazing", cat["base"][2][1]],
                ["Max size", sizes],
                extra[0],
                extra[1],
            ]
            cat.setdefault("products_full", []).append(p)
        cat["products_full"] = cat["products_full"]
    SRCP.run()


if __name__ == "__main__":
    enrich()
    total = build_index()
    for c in D.CATEGORIES:
        total += build_category(c)
        for p in c["products_full"]:
            try:
                total += build_product(c, p)
            except Exception as exc:  # noqa: BLE001
                print("FAILED", c["slug"], p["slug"], exc)
                raise
    n_products = sum(len(c["products_full"]) for c in D.CATEGORIES)
    print("built products/index.html + %d category pages + %d product pages (%.0f KB)"
          % (len(D.CATEGORIES), n_products, total / 1024))
