# -*- coding: utf-8 -*-
"""Build the About Us section: company profile, factory tour, quality control.

The chrome (header / mobile nav / search / footer / floating CTA) is extracted
from index.html and re-based for the sub-folder, so the pages can never drift
from the homepage navigation.
"""
import io
import os
import re

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
OUT = os.path.join(ROOT, "about-us")
os.makedirs(OUT, exist_ok=True)

INDEX = io.open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()


def slice_between(start_marker, end_marker):
    i = INDEX.index(start_marker)
    j = INDEX.index(end_marker, i)
    return INDEX[i:j]


def rebase(markup):
    """Rewrite root-relative asset/anchor links for a page inside /about-us/."""
    markup = markup.replace('href="assets/', 'href="../assets/')
    markup = markup.replace('src="assets/', 'src="../assets/')
    markup = markup.replace('href="about-us/', 'href="../about-us/')
    markup = markup.replace('href="blog/', 'href="../blog/')
    markup = markup.replace('href="contact-us/', 'href="../contact-us/')
    markup = markup.replace('href="products/', 'href="../products/')
    markup = markup.replace('href="cases/', 'href="../cases/')
    markup = markup.replace('href="#', 'href="../index.html#')
    return markup


HEADER = slice_between('<header class="site-header"', "</header>") + "</header>\n"
MOBILE = slice_between('<div class="mobile-nav"', '<div class="search"')
SEARCH = slice_between('<div class="search"', '<main id="main">')
FOOTER = slice_between('<footer class="site-footer"', "</footer>") + "</footer>\n"
FLOATING = '<a class="floating-quote" id="floating-quote" href="#quote">Get A Quote <svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.4"/></svg></a>'
TOAST = '<div class="toast" id="toast" role="status" aria-live="polite" hidden></div>'

# active state: Home is no longer the current section on these pages
HEADER = HEADER.replace('class="nav__link is-active" href="#top"', 'class="nav__link" href="#top"')
# the active item is applied per page, not baked into the shared chrome
ABOUT_LINK_PLAIN = '<a class="nav__link" href="../about-us/company-profile.html" aria-haspopup="true"'
ABOUT_LINK_ACTIVE = '<a class="nav__link is-active" href="../about-us/company-profile.html" aria-haspopup="true"'

CHROME = {
    "header": rebase(HEADER),
    "mobile": rebase(MOBILE),
    "search": rebase(SEARCH),
    "footer": rebase(FOOTER),
    "floating": FLOATING.replace('href="#quote"', 'href="../index.html#quote"'),
    "toast": TOAST,
}

LD = {
    "profile": {
        "title": "Company Profile | Weinas Aluminium Windows &amp; Doors",
        "desc": ("Foshan Weinas Energy Saving Curtain Wall Doors and Windows Technology Co., Ltd. — "
                 "aluminium window and door manufacturer in Foshan, China since 2010. 10,000 m² facility, "
                 "50–100 staff, 60–70% of output exported."),
        "canonical": "https://www.weinas.com/about-us/company-profile.html",
        "crumb": "Company profile",
        "url": "https://www.weinas.com/about-us/company-profile.html",
    },
    "factory": {
        "title": "Factory Tour | Weinas Aluminium Windows &amp; Doors",
        "desc": ("Inside the Weinas factory in Shishan, Foshan: profile cutting, CNC machining, frame assembly, "
                 "glazing, water and air testing, export packing — 10,000 m² and 100 production staff."),
        "canonical": "https://www.weinas.com/about-us/factory-tour.html",
        "crumb": "Factory tour",
        "url": "https://www.weinas.com/about-us/factory-tour.html",
    },
    "quality": {
        "title": "Quality Control | Weinas Aluminium Windows &amp; Doors",
        "desc": ("How Weinas controls quality: incoming material inspection, in-process checks, a 100% "
                 "pre-shipment audit and testing to AS 2047 / EN 14351-1."),
        "canonical": "https://www.weinas.com/about-us/quality-control.html",
        "crumb": "Quality control",
        "url": "https://www.weinas.com/about-us/quality-control.html",
    },
}


def head(meta):
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
<meta property="og:type" content="website">
<meta property="og:site_name" content="Weinas Window &amp; Door Co., Ltd.">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="../assets/img/og-image.jpg">
<meta property="og:url" content="{url}">
<link rel="icon" href="../assets/img/favicon.png" type="image/png" sizes="64x64">
<link rel="apple-touch-icon" href="../assets/img/apple-touch-icon.png">
<link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
""".format(**meta)


def breadcrumb(label):
    return """<nav class="breadcrumb" aria-label="Breadcrumb">
  <a href="../index.html">Home</a><i>/</i><a href="company-profile.html">About us</a><i>/</i><span aria-current="page">{}</span>
</nav>""".format(label)


def hero(no, label, title, lead, image, alt, caption_left, caption_right, width="1100", height="820"):
    return """<section class="page-hero">
  <div class="container">
    {crumb}
    <div class="page-hero__grid">
      <div class="page-hero__main">
        <p class="eyebrow"><span class="eyebrow__no">{no}</span>{label}</p>
        <h1 class="page-hero__title">{title}</h1>
        <p class="page-hero__lead">{lead}</p>
      </div>
      <div class="page-hero__aside">
        <figure class="page-hero__figure">
          <img src="../assets/img/{image}" alt="{alt}" width="{width}" height="{height}">
        </figure>
        <p class="page-hero__caption"><span>{caption_left}</span><span>{caption_right}</span></p>
      </div>
    </div>
  </div>
</section>""".format(crumb=breadcrumb(label), no=no, label=label, title=title, lead=lead,
                   image=image, alt=alt, caption_left=caption_left, caption_right=caption_right,
                   width=width, height=height)


def facts(items):
    cells = "".join(
        '<div class="fact-grid__item"><span class="fact-grid__v num">%s</span><span class="fact-grid__k">%s</span></div>'
        % (v, k) for v, k in items
    )
    return '<div class="section--tight"><div class="container"><div class="fact-grid reveal">%s</div></div></div>' % cells


def section_head(no, label, title, lead=None, aside=None):
    aside_html = ""
    if lead:
        aside_html = '<p class="lead">%s</p>' % lead
    if aside:
        aside_html += aside
    return """<div class="section-head reveal">
  <div class="section-head__main">
    <p class="eyebrow"><span class="eyebrow__no">{no}</span>{label}</p>
    <h2 class="h2">{title}</h2>
  </div>
  <div class="section-head__aside">{aside}</div>
</div>""".format(no=no, label=label, title=title, aside=aside_html)


def gallery(items, wide=False):
    figs = "".join(
        '<figure><img src="../assets/img/%s" alt="%s" loading="lazy" width="1100" height="820"><figcaption>%s</figcaption></figure>'
        % (img, alt, cap) for img, cap, alt in items
    )
    return '<div class="gallery%s reveal">%s</div>' % (" gallery--wide" if wide else "", figs)


def certs():
    return """<section class="certs section--tight">
  <div class="container">
    <div class="certs__row reveal">
      <div class="cert"><span class="cert__name">ISO 9001</span><span class="cert__sub">Quality management</span></div>
      <div class="cert"><span class="cert__name">CE</span><span class="cert__sub">EN 14351-1</span></div>
      <div class="cert"><span class="cert__name">SGS</span><span class="cert__sub">Third-party audit</span></div>
      <div class="cert"><span class="cert__name">AS 2047</span><span class="cert__sub">Australian standard</span></div>
      <div class="cert"><span class="cert__name">NFRC</span><span class="cert__sub">US thermal rating</span></div>
      <div class="cert"><span class="cert__name">Uw TEST</span><span class="cert__sub">Thermal report</span></div>
    </div>
    <div class="certs__note">
      <p>Certificates and third-party test reports are available on request for every system.</p>
      <p>Air permeability · water tightness · wind resistance · thermal transmittance</p>
    </div>
  </div>
</section>"""


def page_nav(prev_label, prev_href, next_label, next_href):
    return """<div class="container">
  <div class="page-nav reveal">
    <a class="page-nav__prev" href="{ph}"><small>{pl}</small><strong>← {pt}</strong></a>
    <a class="page-nav__next" href="{nh}"><small>{nl}</small><strong>{nt} →</strong></a>
  </div>
</div>""".format(ph=prev_href, pl=prev_label, pt=prev_label, nh=next_href, nl=next_label, nt=next_label)


def cta():
    return """<section class="cta-band">
  <div class="container cta-band__grid">
    <div>
      <h2>Tell us about your opening schedule.</h2>
      <p>Drawings, sizes or a specification — we return a factory-direct quotation, lead time and shipping plan, usually within one business day.</p>
    </div>
    <div class="cta-band__actions">
      <a class="btn" href="../index.html#quote">Get A Quote</a>
      <a class="btn btn--ghost" href="../index.html#catalogue">Browse systems</a>
    </div>
  </div>
</section>"""


# --------------------------------------------------------------- page bodies
PROFILE_BODY = hero(
    "01", "Company profile",
    "Aluminium openings, engineered in <span class='hl'>Foshan</span> since 2010.",
    "Foshan Weinas Energy Saving Curtain Wall Doors and Windows Technology Co., Ltd. — WEINAS — is an aluminium "
    "window and door manufacturer in Shishan, Foshan. We design, extrude, finish and assemble in one 10,000 m² "
    "facility, and export 60–70% of what we make.",
    "factory-facility.jpg",
    "Aerial view of the Weinas aluminium window and door factory in Foshan",
    "Shishan · Foshan, Guangdong",
    "Established 2010",
) + facts([
    ("2010", "Year established"),
    ("10,000 m²", "Manufacturing facility"),
    ("50–100", "Employees"),
    ("60–70%", "Of output exported"),
]) + """
<section class="section">
  <div class="container">
    <div class="split">
      <div class="split__head reveal">
        <p class="eyebrow"><span class="eyebrow__no">02</span>Who we are</p>
        <h2 class="h2">One factory for <span class='hl'>profile, finish and glazing</span>.</h2>
        <p class="lead">Most window suppliers buy extrusions, sub-contract the coating and assemble elsewhere. We keep all four stages under one roof — which is why a specification survives from drawing to container.</p>
      </div>
      <div class="prose reveal" style="--delay:100ms">
        <p class="is-lead">Weinas started in 2010 as an aluminium fabrication workshop in Shishan — the centre of Foshan's aluminium processing industry. Fifteen years on, the same site holds 10,000 m² of extrusion support, CNC machining, powder coating, insulated glazing and final assembly, run by a team of 50–100 people.</p>
        <p>Our development team of ten engineers turns a measured opening into something a factory can actually build: profile selection, thermal-break detailing, glass build-up, hardware schedule and a drawing set for approval before the first bar is cut.</p>
        <p>Every profile, panel and gasket that leaves the plant is ours — so tolerance, finish and water-tightness do not depend on a supplier we cannot see. That is the practical difference for the architects, builders and distributors who specify Weinas.</p>
        <p>60–70% of our output is exported, mostly to residential and commercial projects: villas, apartments, hotels and facades. The rest is domestic work at the same specification.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--offwhite">
  <div class="container">
    """ + section_head("03", "What we do", "Four stages, <span class='hl'>one quality gate</span>.",
                        "From a measured opening to a water-tested assembly, packed for sea freight.") + """
    <div class="cards-4 reveal">
      <div class="cap"><span class="cap__no">01</span><h3 class="cap__title">Engineering &amp; drawings</h3><p class="cap__text">Measured drawings, thermal and glass specification, hardware schedule and a submittal package for consultant approval.</p></div>
      <div class="cap"><span class="cap__no">02</span><h3 class="cap__title">Extrusion &amp; fabrication</h3><p class="cap__text">6063-T6 profiles cut and machined on CNC centres to ±0.2 mm — drainage, handle recesses and glazing rebates included.</p></div>
      <div class="cap"><span class="cap__no">03</span><h3 class="cap__title">Coating &amp; glazing</h3><p class="cap__text">Nine-stage pre-treatment and automated powder coating, plus low-E argon-filled IGUs assembled and sealed in-house.</p></div>
      <div class="cap"><span class="cap__no">04</span><h3 class="cap__title">Export &amp; logistics</h3><p class="cap__text">Water-tested assemblies, foam-cradled crating and container loading checked against the packing list.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    """ + section_head("04", "Inside Weinas", "The plant, in <span class='hl'>six frames</span>.",
                        "A working factory rather than a show suite: fabrication, coating, glazing, testing, packing.") + gallery([
        ("factory-facility.jpg", "Facility · 10,000 m²", "Aerial view of the Weinas factory"),
        ("factory-workshop.jpg", "Engineering", "Engineers preparing drawings in the office"),
        ("factory-welding.jpg", "Fabrication", "Precision welding and assembly"),
        ("factory-sign.jpg", "Loading bay · export packing", "Packed window and door sets on the loading bay"),
        ("collection-office.jpg", "Showroom", "Showroom for full-size mock-ups"),
        ("project-palm-beach.jpg", "Installed project", "Villa project with Weinas sliding doors"),
    ]) + """
  </div>
</section>

""" + certs() + """
<section class="section">
  """ + page_nav("Back to homepage", "../index.html", "Factory tour", "factory-tour.html") + """
</section>

""" + cta()

FACTORY_BODY = hero(
    "02", "Factory tour",
    "Where the opening is <span class='hl'>made</span>.",
    "10,000 m² in Shishan, Foshan: profile cutting, CNC machining, frame assembly, glazing, testing and packing — "
    "with around 100 people on the production floor.",
    "factory-warehouse.jpg",
    "Packing and warehouse aisle inside the Weinas factory",
    "Production floor · Foshan",
    "100 staff",
) + facts([
    ("10,000 m²", "Under one roof"),
    ("100", "Production staff"),
    ("6", "Production stages"),
    ("±0.2 mm", "Machining tolerance"),
]) + """
<section class="section">
  <div class="container">
    <div class="split split--reverse">
      <div class="split__media reveal">
        <img src="../assets/img/factory-welding.jpg" alt="Fabrication and welding of aluminium frames" loading="lazy" width="1100" height="820">
        <div class="gallery gallery--wide" style="grid-template-columns:1fr 1fr">
          <figure><img src="../assets/img/factory-workshop.jpg" alt="Engineering office" loading="lazy"><figcaption>Engineering</figcaption></figure>
          <figure><img src="../assets/img/factory-facility.jpg" alt="Factory aerial" loading="lazy"><figcaption>Facility</figcaption></figure>
        </div>
      </div>
      <div class="split__head reveal" style="--delay:100ms">
        <p class="eyebrow"><span class="eyebrow__no">03</span>The line</p>
        <h2 class="h2">Six stages, <span class='hl'>start to container</span>.</h2>
        <p class="lead">Each stage has an owner and a check. Nothing moves forward on the assumption that the previous step was right.</p>
        <div class="numbered">
""" + "".join("""          <div class="numbered__row">
            <span class="numbered__no">%02d</span>
            <div><h3 class="numbered__title">%s</h3><p class="numbered__text">%s</p></div>
          </div>
""" % (i, t, d) for i, (t, d) in enumerate([
        ("Profile cutting", "Double-head saws cut 6063-T6 profiles to length; off-cuts are sorted and returned to the extrusion stream."),
        ("CNC machining", "Five-axis centres mill drainage slots, handle recesses and glazing rebates, checked against the first-off sample."),
        ("Frame assembly", "Corner crimping and screw-fixed joints, squared on the bench before any glass goes in."),
        ("Glazing &amp; sealing", "IGUs set on EPDM gaskets, sealed and drained; hardware mounted, adjusted and cycle-tested."),
        ("Water &amp; air test", "Sample units sprayed and pressurised to AS 2047 / EN 14351 before the batch is released."),
        ("Packing &amp; loading", "Foam cradles, corner protection and a container plan; loading checked against the packing list."),
    ], 1)) + """        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--offwhite">
  <div class="container">
    """ + section_head("04", "Capability", "What the plant <span class='hl'>can hold</span>.",
                        "Tolerances, finishes and glass build-ups we hold in-house, without sub-contracting.") + """
    <table class="data-table reveal">
      <caption>Manufacturing capability</caption>
      <tbody>
        <tr><th scope="row">Profile</th><td>6063-T6 aluminium, 1.4–2.0 mm wall thickness, thermally broken with polyamide</td></tr>
        <tr><th scope="row">Machining</th><td>CNC machining centres, ±0.2 mm on critical interfaces</td></tr>
        <tr><th scope="row">Finish</th><td>Nine-stage pre-treatment, automated powder coating, 60–80 µm</td></tr>
        <tr><th scope="row">Glazing</th><td>Double and triple IGUs, low-E, argon-filled, warm-edge spacer</td></tr>
        <tr><th scope="row">Testing</th><td>Air permeability, water tightness and wind resistance per AS 2047 / EN 14351-1</td></tr>
        <tr><th scope="row">Capacity</th><td>10,000 m² facility · 50–100 employees · 60–70% export share</td></tr>
      </tbody>
    </table>
  </div>
</section>

<section class="section">
  <div class="container">
    """ + section_head("05", "Walk the plant", "From the saw <span class='hl'>to the container</span>.",
                        "The same floor that machines the profile packs the crate.") + gallery([
        ("factory-facility.jpg", "Facility", "Factory exterior and loading yard"),
        ("factory-workshop.jpg", "Engineering", "Drawing review before production"),
        ("factory-welding.jpg", "Fabrication", "Frame welding and assembly"),
        ("factory-sign.jpg", "Loading bay", "Packed sets waiting for the container"),
        ("project-tokyo.jpg", "Installed", "Interior partition project"),
        ("project-cottesloe.jpg", "Installed", "Residential casement project"),
    ]) + """
  </div>
</section>

<section class="section">
  """ + page_nav("Company profile", "company-profile.html", "Quality control", "quality-control.html") + """
</section>

""" + cta()

QUALITY_BODY = hero(
    "03", "Quality control",
    "Tested, not <span class='hl'>assumed</span>.",
    "Four gates stand between raw material and the container: incoming inspection, in-process checks, a 100% "
    "pre-shipment audit and testing to international standards.",
    "factory-welding.jpg",
    "Close-up of precision fabrication at the Weinas factory",
    "Quality gate · Foshan",
    "100% pre-shipment",
) + """
<section class="section">
  <div class="container">
    """ + section_head("01", "The promise",
                        "Our quality assurance <span class='hl'>promise</span>.",
                        "The process is uncompromising and documented — every batch can be traced back to its material lot, machine and inspector.") + """
    <div class="cards-4 reveal">
      <div class="cap"><span class="cap__no">01</span><h3 class="cap__title">Incoming inspection</h3><p class="cap__text">Every delivery of profile, glass, gasket and hardware is verified against the purchase specification before it enters stock.</p></div>
      <div class="cap"><span class="cap__no">02</span><h3 class="cap__title">In-process checks</h3><p class="cap__text">Dimensions, square and finish are measured at critical stages — after machining, after assembly and after glazing.</p></div>
      <div class="cap"><span class="cap__no">03</span><h3 class="cap__title">Pre-shipment audit</h3><p class="cap__text">A final, comprehensive 100% inspection against your approved drawings: size, hardware, glass, seals and labelling.</p></div>
      <div class="cap"><span class="cap__no">04</span><h3 class="cap__title">Certified standards</h3><p class="cap__text">Processes and products are tested to leading international standards, with reports available for the project file.</p></div>
    </div>
  </div>
</section>

<section class="section section--offwhite">
  <div class="container">
    <div class="split">
      <div class="split__head reveal">
        <p class="eyebrow"><span class="eyebrow__no">02</span>Inspection flow</p>
        <h2 class="h2">Where the <span class='hl'>checks</span> happen.</h2>
        <p class="lead">Six points, in the order a unit actually moves through the plant. Each one can stop the batch.</p>
      </div>
      <div class="numbered reveal" style="--delay:100ms">
""" + "".join("""        <div class="numbered__row">
          <span class="numbered__no">%02d</span>
          <div><h3 class="numbered__title">%s</h3><p class="numbered__text">%s</p></div>
        </div>
""" % (i, t, d) for i, (t, d) in enumerate([
        ("Material in", "Profile alloy and wall thickness gauged; glass build-up, spacer and desiccant checked against the order."),
        ("First-off approval", "The first frame of every run is measured in full and signed off before the batch continues."),
        ("Machining &amp; assembly", "Drainage, rebates and square are checked in process; hardware is fitted and operated."),
        ("Glazing &amp; sealing", "Gasket compression, sealant beads and drainage paths inspected on every unit."),
        ("Water &amp; air test", "Sample units are sprayed and pressurised to the project standard; failures stop the batch."),
        ("Pre-shipment audit", "100% inspection against the drawing set, photographed and recorded before crating."),
    ], 1)) + """      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    """ + section_head("03", "Standards", "What we are <span class='hl'>measured</span> against.",
                        "Project requirements drive the test plan — these are the standards we are routinely asked to meet.") + """
    <table class="data-table reveal">
      <caption>Test and certification scope</caption>
      <tbody>
        <tr><th scope="row">Quality system</th><td>ISO 9001 — documented process control and traceability</td></tr>
        <tr><th scope="row">Product standard</th><td>CE marking to EN 14351-1 / AS 2047 for windows and doors</td></tr>
        <tr><th scope="row">Air &amp; water</th><td>Air permeability and water tightness tested per project class</td></tr>
        <tr><th scope="row">Wind load</th><td>Structural and serviceability performance to the specified design pressure</td></tr>
        <tr><th scope="row">Thermal</th><td>Uw values verified by calculation and third-party test reports</td></tr>
        <tr><th scope="row">Acoustic</th><td>Rw rating available for acoustic glazing build-ups</td></tr>
      </tbody>
    </table>
    <div class="certs__note">
      <p>Third-party reports are issued per system and supplied with the quotation pack on request.</p>
      <p>Please state the target standard (AS 2047, EN 14351-1, NFRC) when you send drawings.</p>
    </div>
  </div>
</section>

""" + certs() + """
<section class="section">
  <div class="container">
    """ + section_head("04", "On the floor", "Inspection, in <span class='hl'>practice</span>.",
                        "Measuring, testing and recording — the parts of quality that do not show on a brochure.") + gallery([
        ("factory-facility.jpg", "Facility", "Factory and testing area"),
        ("factory-workshop.jpg", "Record keeping", "Drawing and inspection records"),
        ("factory-welding.jpg", "Fabrication", "Joint and finish check"),
        ("factory-warehouse.jpg", "Packing audit", "Crate and label verification"),
        ("top-pick-frames.jpg", "Installed quality", "Completed sliding system in situ"),
        ("project-byron.jpg", "Installed quality", "Bathroom door installation"),
    ]) + """
  </div>
</section>

<section class="section">
  """ + page_nav("Factory tour", "factory-tour.html", "Company profile", "company-profile.html") + """
</section>

""" + cta()


# ------------------------------------------------------------------ assemble
def render(meta_key, body):
    meta = LD[meta_key]
    page = head(meta) + CHROME["header"].replace(ABOUT_LINK_PLAIN, ABOUT_LINK_ACTIVE) \
        + CHROME["mobile"] + CHROME["search"]
    page += '<main id="main">\n' + body + '\n</main>\n'
    page += CHROME["footer"] + CHROME["floating"] + "\n" + CHROME["toast"] + "\n"
    page += """<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "{title}",
  "url": "{url}",
  "isPartOf": {{ "@type": "WebSite", "name": "Weinas", "url": "https://www.weinas.com/" }},
  "breadcrumb": {{
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.weinas.com/" }},
      {{ "@type": "ListItem", "position": 2, "name": "About us", "item": "https://www.weinas.com/about-us/company-profile.html" }},
      {{ "@type": "ListItem", "position": 3, "name": "{crumb}", "item": "{url}" }}
    ]
  }}
}}
</script>
<script src="../assets/js/main.js" defer></script>
</body>
</html>
""".format(title=meta["title"].replace('"', ""), url=meta["url"], crumb=meta["crumb"])
    return page


PAGES = {
    "company-profile.html": ("profile", PROFILE_BODY),
    "factory-tour.html": ("factory", FACTORY_BODY),
    "quality-control.html": ("quality", QUALITY_BODY),
}

if __name__ == "__main__":
    for filename, (key, body) in PAGES.items():
        html = render(key, body)
        io.open(os.path.join(OUT, filename), "w", encoding="utf-8").write(html)
        print("wrote about-us/%s (%d bytes)" % (filename, len(html)))
