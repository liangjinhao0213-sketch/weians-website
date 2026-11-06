# -*- coding: utf-8 -*-
"""Assemble index.html for the Weinas homepage."""
import os

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"

PRODUCTS = [
    ("Aluminium Sliding Doors", "aluminium-sliding-doors", "Sightline 22 mm · Uw 1.3 W/m²K"),
    ("Aluminium Casement Windows", "aluminium-casement-windows", "Sightline 55 mm · Uw 1.4 W/m²K"),
    ("Aluminium Sliding Windows", "aluminium-sliding-windows", "2–3 track · Up to 4.2 m span"),
    ("Interior Sliding Partition Doors", "interior-sliding-partition-doors", "Soft-close track · 40 dB acoustic"),
    ("Aluminium Casement Doors", "aluminium-casement-doors", "Uw 1.4 · 120 kg leaf"),
    ("Aluminium Tilt And Turn Windows", "aluminium-tilt-and-turn-windows", "Dual action · Uw 1.1 W/m²K"),
    ("Thermal Insulation Windows", "thermal-insulation-windows", "Polyamide break · Uw 0.9 W/m²K"),
    ("Aluminium Swing Doors", "aluminium-swing-doors", "Concealed hinge · RC2 option"),
    ("Aluminium Bathroom Doors", "aluminium-bathroom-doors", "Frosted lite · fully waterproof"),
    ("Aluminium Front Doors", "aluminium-front-doors", "Security core · 68 mm leaf"),
    ("Aluminium Pivot Doors", "aluminium-pivot-doors", "Offset axis · 200 kg leaf"),
    ("Aluminium Folding Doors", "aluminium-folding-doors", "Up to 12 panels · 6.0 m clear"),
]

CATALOGUE = [
    ("WS-90 Sliding Door", "aluminium-sliding-doors", "Uw 1.3 W/m²K",
     [("Sightline", "22 mm"), ("Uw value", "1.3 W/m²K"), ("Max panel", "3.2 × 3.4 m")]),
    ("WC-75 Casement Window", "aluminium-casement-windows", "Uw 1.4 W/m²K",
     [("Sightline", "55 mm"), ("Uw value", "1.4 W/m²K"), ("Water", "Class 9A")]),
    ("WS-70 Sliding Window", "aluminium-sliding-windows", "Uw 1.6 W/m²K",
     [("Tracks", "2 / 3"), ("Uw value", "1.6 W/m²K"), ("Max span", "4.2 m")]),
    ("WP-60 Interior Partition", "interior-sliding-partition-doors", "40 dB acoustic",
     [("Acoustic", "40 dB (−1)"), ("Track", "Soft close"), ("Height", "2.7 m")]),
    ("WT-75 Tilt & Turn Window", "aluminium-tilt-and-turn-windows", "Uw 1.1 W/m²K",
     [("Uw value", "1.1 W/m²K"), ("Glazing", "Triple"), ("Operation", "Tilt + turn")]),
    ("WT-85 Thermal Window", "thermal-insulation-windows", "Uw 0.9 W/m²K",
     [("Uw value", "0.9 W/m²K"), ("IGU", "48 mm"), ("Standard", "Passive-ready")]),
    ("WF-85 Folding Door", "aluminium-folding-doors", "6.0 m clear span",
     [("Panels", "Up to 12"), ("Clear span", "6.0 m"), ("Acoustic", "38 dB")]),
    ("WV-100 Pivot Door", "aluminium-pivot-doors", "200 kg leaf",
     [("Leaf weight", "200 kg"), ("Axis", "Offset"), ("Rating", "RC2 option")]),
]

CASES = [
    ("project-palm-beach.jpg", "Palm Beach · Florida", "Residential", "WS-90 sliding", "4 / 5"),
    ("project-tokyo.jpg", "Shibuya · Tokyo", "Commercial", "Interior partition", "4 / 3"),
    ("project-cottesloe.jpg", "Cottesloe · Western Australia", "Residential", "WC-75 casement", "1 / 1"),
    ("project-byron.jpg", "Byron Bay · New South Wales", "Hospitality", "Bathroom doors", "4 / 5"),
    ("project-dubai.jpg", "Al Quoz · Dubai", "Commercial", "Curtain wall", "16 / 10"),
    ("project-australia.jpg", "Kensington · London", "Residential", "WF-85 folding", "16 / 10"),
]

COLLECTIONS = {
    "opening": [
        ("Sliding systems", "aluminium-sliding-doors", "24 models"),
        ("Casement systems", "aluminium-casement-windows", "31 models"),
        ("Folding systems", "aluminium-folding-doors", "12 models"),
        ("Pivot systems", "aluminium-pivot-doors", "8 models"),
        ("Tilt & turn systems", "aluminium-tilt-and-turn-windows", "18 models"),
    ],
    "application": [
        ("Villas", "collection-villa.jpg", "26 projects"),
        ("Apartments", "collection-casement.jpg", "22 projects"),
        ("Hotels", "collection-office.jpg", "14 projects"),
        ("Offices", "collection-facade.jpg", "18 projects"),
        ("Balconies", "collection-balcony.jpg", "11 projects"),
    ],
}

# ------------------------------------------------------------------ icons
I = {
    "arrow": '<svg class="btn__arrow" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.4"/></svg>',
    "arrow-sm": '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.4"/></svg>',
    "chevron": '<svg class="nav__chevron" viewBox="0 0 12 8" fill="none" aria-hidden="true"><path d="M1 1.5l5 5 5-5" stroke="currentColor" stroke-width="1.4"/></svg>',
    "search": '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><circle cx="8.5" cy="8.5" r="6" stroke="currentColor" stroke-width="1.4"/><path d="M13 13l4 4" stroke="currentColor" stroke-width="1.4"/></svg>',
    "close": '<svg viewBox="0 0 18 18" fill="none" aria-hidden="true"><path d="M4 4l10 10M14 4L4 14" stroke="currentColor" stroke-width="1.4"/></svg>',
    "mail": '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><rect x="1.5" y="3" width="13" height="10" stroke="currentColor" stroke-width="1.2"/><path d="M2 4l6 4.5L14 4" stroke="currentColor" stroke-width="1.2"/></svg>',
    "phone": '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 2.5h2.6l1.2 3-1.6 1.2a8 8 0 0 0 3.9 3.9l1.2-1.6 3 1.2V13c0 .6-.4 1-1 1A11.5 11.5 0 0 1 2 3.5c0-.6.4-1 1-1z" stroke="currentColor" stroke-width="1.2"/></svg>',
    "pin": '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M8 14s5-4.4 5-8A5 5 0 0 0 3 6c0 3.6 5 8 5 8z" stroke="currentColor" stroke-width="1.2"/><circle cx="8" cy="6" r="1.8" stroke="currentColor" stroke-width="1.2"/></svg>',
    "wa": '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M2 14l.8-2.6A6 6 0 1 1 8 14H2z" stroke="currentColor" stroke-width="1.2"/><path d="M5.8 5.4c.2-.4.4-.4.6-.4h.5c.2 0 .4 0 .5.4l.6 1.3c.1.2 0 .4-.1.5l-.4.4c.4.8 1.1 1.5 1.9 1.9l.4-.4c.2-.1.3-.2.5-.1l1.3.6c.3.1.4.3.4.5v.5c0 .5-.4 1-1 1-2.6 0-5.2-2.6-5.2-5.2 0-.5.1-1 .5-1z" fill="currentColor"/></svg>',
    "li": '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><rect x="2" y="2" width="12" height="12" stroke="currentColor" stroke-width="1.2"/><path d="M5 7v4M5 5.2v.1M8 11V7m0 1.6c0-.9.6-1.6 1.5-1.6S11 7.7 11 8.6V11" stroke="currentColor" stroke-width="1.2"/></svg>',
    "yt": '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><rect x="1.5" y="4" width="13" height="8" rx="2.2" stroke="currentColor" stroke-width="1.2"/><path d="M7 6.4l3 1.6-3 1.6z" fill="currentColor"/></svg>',
    "pin-social": '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><rect x="2" y="2" width="12" height="12" rx="3" stroke="currentColor" stroke-width="1.2"/><circle cx="8" cy="8" r="3" stroke="currentColor" stroke-width="1.2"/><circle cx="11.5" cy="4.5" r=".9" fill="currentColor"/></svg>',
}


def product_links(cls="", extra=""):
    out = []
    for i, (name, slug, spec) in enumerate(PRODUCTS, 1):
        out.append(
            '<li><a class="%s" href="#catalogue" %s><span class="mega__no">%02d</span>'
            '<span>%s</span></a></li>' % (cls, extra, i, name)
        )
    return "\n".join(out)


def build():
    p = []
    a = p.append

    a('<!doctype html>')
    a('<html lang="en">')
    a('<head>')
    a('<meta charset="utf-8">')
    a('<meta name="viewport" content="width=device-width, initial-scale=1">')
    a('<title>Weinas | Aluminium Windows &amp; Doors Manufacturer in China</title>')
    a('<meta name="description" content="Weinas Window &amp; Door Co., Ltd. manufactures slim-sightline aluminium sliding doors, casement windows, folding and pivot systems with thermally broken profiles. Factory-direct supply for architects, builders and distributors in 60+ countries.">')
    a('<meta name="theme-color" content="#0B2B5B">')
    a('<!-- TODO(上线前): 域名确定后，替换 canonical / og:url / JSON-LD / robots.txt / sitemap.xml 里的 www.weinas.com -->')
    a('<link rel="canonical" href="https://www.weinas.com/">')
    a('<meta property="og:type" content="website">')
    a('<meta property="og:site_name" content="Weinas Window &amp; Door Co., Ltd.">')
    a('<meta property="og:title" content="Weinas | Engineered Aluminium Openings for Modern Architecture">')
    a('<meta property="og:description" content="Slim-sightline aluminium sliding, casement, folding and pivot systems — engineered, extruded and fabricated in our own 40,000 m² facility in Foshan, China.">')
    a('<meta property="og:image" content="assets/img/og-image.jpg">')
    a('<meta property="og:url" content="https://www.weinas.com/">')
    a('<meta name="twitter:card" content="summary_large_image">')
    a('<link rel="icon" href="assets/img/favicon.png" type="image/png" sizes="64x64">')
    a('<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">')
    a('<link rel="preload" href="assets/fonts/inter-latin-UcCo3FwrK3.woff2" as="font" type="font/woff2" crossorigin>')
    a('<link rel="preload" as="image" href="assets/img/hero-villa-1600.jpg" imagesrcset="assets/img/hero-villa-1600.jpg 1600w, assets/img/hero-villa-2400.jpg 2400w" imagesizes="100vw">')
    a('<link rel="stylesheet" href="assets/css/style.css">')
    a('</head>')
    a('<body>')
    a('<a class="skip-link" href="#main">Skip to content</a>')

    # ---------------------------------------------------------------- header
    a('<header class="site-header" id="header">')
    a('  <div class="container header__inner">')
    a('    <a class="brand" href="#top" aria-label="Weinas — home">')
    a('      <img src="assets/img/logo.png" alt="Weinas — Doors And Windows Manufacturer" width="167" height="46">')
    a('    </a>')
    a('    <nav class="nav" aria-label="Primary">')
    a('      <ul class="nav__list">')
    a('        <li><a class="nav__link is-active" href="#top" data-spy>Home</a></li>')
    a('        <li class="nav__item--has-menu">')
    a('          <button class="nav__link nav__toggle" type="button" aria-expanded="false" aria-controls="products-menu">Products ' + I["chevron"] + '</button>')
    a('          <div class="mega" id="products-menu">')
    a('            <p class="mega__head"><span>Product systems · <b>12</b></span><span>Aluminium</span></p>')
    a('            <ul class="mega__list">')
    a(product_links())
    a('            </ul>')
    a('            <div class="mega__foot">')
    a('              <span>Factory-direct · trade only</span>')
    a('              <a href="#catalogue">View catalogue ' + I["arrow-sm"] + '</a>')
    a('            </div>')
    a('          </div>')
    a('        </li>')
    a('        <li><a class="nav__link" href="/videos/" data-coming-soon>Videos</a></li>')
    a('        <li><a class="nav__link" href="#factory" data-spy>About Us</a></li>')
    a('        <li><a class="nav__link" href="#quote" data-spy>Contact Us</a></li>')
    a('        <li><a class="nav__link" href="/news/" data-coming-soon>News</a></li>')
    a('        <li><a class="nav__link" href="#cases" data-spy>Cases</a></li>')
    a('      </ul>')
    a('    </nav>')
    a('    <div class="header__actions">')
    a('      <button class="icon-btn" id="search-open" type="button" aria-label="Search products">' + I["search"] + '</button>')
    a('      <a class="btn header__cta" href="#quote">Get A Quote</a>')
    a('      <button class="burger" id="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-nav"><span></span></button>')
    a('    </div>')
    a('  </div>')
    a('</header>')

    # ------------------------------------------------------------ mobile nav
    a('<div class="mobile-nav" id="mobile-nav" aria-label="Mobile navigation">')
    a('  <ul class="mobile-nav__list">')
    a('    <li><a href="#top">Home</a></li>')
    a('    <li>')
    a('      <button class="mobile-nav__toggle" type="button" aria-expanded="false" aria-controls="mobile-products">Products ' + I["chevron"] + '</button>')
    a('      <ul class="mobile-nav__sub" id="mobile-products">')
    for name, slug, spec in PRODUCTS:
        a('        <li><a href="#catalogue">%s</a></li>' % name)
    a('      </ul>')
    a('    </li>')
    a('    <li><a href="/videos/" data-coming-soon>Videos</a></li>')
    a('    <li><a href="#factory">About Us</a></li>')
    a('    <li><a href="#quote">Contact Us</a></li>')
    a('    <li><a href="/news/" data-coming-soon>News</a></li>')
    a('    <li><a href="#cases">Cases</a></li>')
    a('  </ul>')
    a('  <div class="mobile-nav__foot">')
    a('    <a class="btn" href="#quote">Get A Quote</a>')
    a('    <div class="mobile-nav__contact">')
    a('      <a href="mailto:liangjinhao0213@gmail.com">liangjinhao0213@gmail.com</a>')
    a('      <a href="tel:+8617818819386">+86 178 1881 9386</a>')
    a('    </div>')
    a('  </div>')
    a('</div>')

    # ---------------------------------------------------------------- search
    a('<div class="search" id="search" role="dialog" aria-modal="true" aria-label="Search Weinas products">')
    a('  <div class="search__inner">')
    a('    <div class="search__top">')
    a('      <span>Search · 12 product systems</span>')
    a('      <button class="search__close" id="search-close" type="button" aria-label="Close search">' + I["close"] + '</button>')
    a('    </div>')
    a('    <form class="search__field" role="search" onsubmit="return false">')
    a('      ' + I["search"])
    a('      <label class="sr-only" for="search-input">Search products</label>')
    a('      <input class="search__input" id="search-input" type="search" placeholder="Sliding door, casement, thermal…" autocomplete="off">')
    a('    </form>')
    a('    <p class="search__hint">Type to filter · press Esc to close · “/” opens search from anywhere</p>')
    a('    <div class="search__results" id="search-results">')
    for i, (name, slug, spec) in enumerate(PRODUCTS, 1):
        a('      <a href="#catalogue" data-name="%s"><span class="mega__no">%02d</span><span>%s</span></a>' % (name.lower(), i, name))
    a('    </div>')
    a('  </div>')
    a('</div>')

    # ------------------------------------------------------------------ hero
    a('<main id="main">')
    a('<section class="hero" id="top">')
    a('  <div class="hero__media">')
    a('    <picture>')
    a('      <source media="(max-width: 760px)" srcset="assets/img/hero-villa-mobile.jpg">')
    a('      <img src="assets/img/hero-villa-1600.jpg" srcset="assets/img/hero-villa-1600.jpg 1600w, assets/img/hero-villa-2400.jpg 2400w" sizes="100vw" alt="Dark aluminium-clad villa facade at dusk with slim floor-to-ceiling aluminium windows glowing warm" fetchpriority="high" width="1600" height="787">')
    a('    </picture>')
    a('  </div>')
    a('  <div class="container hero__inner">')
    a('    <div class="hero__copy">')
    a('      <p class="eyebrow eyebrow--light"><span class="eyebrow__no">Weinas</span>Aluminium window &amp; door manufacturer</p>')
    a('      <h1 class="hero__title">Engineered Aluminium Openings for Modern Architecture</h1>')
    a('      <p class="hero__sub">Sliding, Casement, Folding &amp; Pivot Systems — Factory Direct from China</p>')
    a('      <div class="hero__actions">')
    a('        <a class="btn" href="#quote">Get A Quote</a>')
    a('        <a class="btn btn--ghost" href="#systems">Explore product systems ' + I["arrow-sm"] + '</a>')
    a('      </div>')
    a('    </div>')
    a('  </div>')
    a('  <div class="hero__foot">')
    a('    <span class="hero__scroll"><i></i>Scroll</span>')
    a('  </div>')
    a('</section>')

    # ------------------------------------------------------------- spec bar
    a('<section class="specbar" aria-label="Key performance data">')
    a('  <div class="container specbar__inner">')
    for k, v in (("Sightline", "22 mm"), ("Uw value", "1.3 W/m²K"), ("Max panel", "3.2 × 3.4 m"), ("Tested to", "AS 2047 · CE · NFRC")):
        a('    <div class="specbar__item"><span class="specbar__k">%s</span><span class="specbar__v num">%s</span></div>' % (k, v))
    a('  </div>')
    a('</section>')

    # ------------------------------------------------------------ categories
    a('<section class="section" id="systems">')
    a('  <div class="container">')
    a('    <div class="section-head reveal">')
    a('      <div class="section-head__main">')
    a('        <p class="eyebrow"><span class="eyebrow__no">01</span>Product systems</p>')
    a('        <h2 class="h2">Twelve opening systems.<br>One engineering standard.</h2>')
    a('      </div>')
    a('      <div class="section-head__aside">')
    a('        <p class="lead">Every Weinas system is extruded, machined and assembled in our own Foshan facility — thermally broken profiles, German hardware and glass specified for your climate zone.</p>')
    a('        <a class="link-arrow" href="#catalogue">View B2B catalogue ' + I["arrow-sm"] + '</a>')
    a('      </div>')
    a('    </div>')
    a('    <div class="cat-grid">')
    for i, (name, slug, spec) in enumerate(PRODUCTS, 1):
        a('      <a class="cat reveal" href="#catalogue" style="--delay:%dms">' % ((i - 1) % 3 * 70))
        a('        <span class="cat__top"><span>%02d</span><span class="cat__arrow">%s</span></span>' % (i, I["arrow-sm"]))
        a('        <span class="cat__media"><img src="assets/img/products/%s.svg" alt="%s technical elevation" loading="lazy" width="400" height="300"></span>' % (slug, name))
        a('        <h3 class="cat__name">%s</h3>' % name)
        a('        <p class="cat__spec">%s</p>' % spec)
        a('      </a>')
    a('    </div>')
    a('  </div>')
    a('</section>')

    # ------------------------------------------------------------- top picks
    a('<section class="section section--offwhite" id="top-picks">')
    a('  <div class="container">')
    a('    <div class="section-head reveal">')
    a('      <div class="section-head__main">')
    a('        <p class="eyebrow"><span class="eyebrow__no">02</span>Top picks</p>')
    a('        <h2 class="h2">The WS-90 sliding system.</h2>')
    a('      </div>')
    a('      <div class="section-head__aside">')
    a('        <p class="lead">A 22 mm sightline and a 3.4 m panel height — the system most specified for villa, penthouse and terrace openings.</p>')
    a('      </div>')
    a('    </div>')
    a('    <div class="feature">')
    a('      <div class="feature__media reveal">')
    a('        <figure>')
    a('          <img src="assets/img/top-pick-frames.jpg" alt="Black slim-profile aluminium sliding door in a concrete and oak interior" loading="lazy" width="1500" height="1000">')
    a('          <figcaption class="feature__caption"><span>WS-90 · Palm Beach residence</span><span>Sliding door</span></figcaption>')
    a('        </figure>')
    a('      </div>')
    a('      <div class="feature__body reveal" style="--delay:120ms">')
    a('        <h3 class="h3">Two panels. One continuous view.</h3>')
    a('        <p>A 22 mm visible frame carries panels up to 3.4 m high on stainless tandem rollers. Thermally broken polyamide and EPDM double gaskets keep the envelope sealed through wind-driven rain.</p>')
    a('        <dl class="spec-list">')
    for k, v in (("Sightline", "22 mm"), ("Uw value", "1.3 W/m²K"), ("Max panel", "3.2 × 3.4 m"),
                 ("Air / water", "Class 4 / 9A"), ("Acoustic", "38 dB (−1)")):
        a('          <div class="spec-list__row"><dt>%s</dt><dd>%s</dd></div>' % (k, v))
    a('        </dl>')
    a('        <p style="margin-top:22px"><a class="link-arrow" href="#quote">Request this system ' + I["arrow-sm"] + '</a></p>')
    a('      </div>')
    a('    </div>')
    a('    <div class="feature" style="margin-top:clamp(28px,4vw,56px)">')
    a('      <div class="feature__aside reveal">')
    a('        <div class="plate">')
    a('          <img src="assets/img/ws90-section.svg" alt="Section detail through the WS-90 thermally broken head profile showing the polyamide thermal break and 48 mm insulated glazing" loading="lazy" width="800" height="600">')
    a('          <p class="plate__caption"><span>Section A–A · head detail</span><span>Scale 1:2</span></p>')
    a('        </div>')
    a('      </div>')
    a('      <div class="feature__main reveal" style="--delay:100ms">')
    a('        <h3 class="h3">Engineered around the thermal break.</h3>')
    a('        <p class="lead">The profile is split by a 34 mm glass-fibre reinforced polyamide bridge, so the inner face stays close to room temperature while the outer face meets the weather. Condensation on the frame is designed out, not compensated for.</p>')
    a('        <p class="lead" style="margin-top:16px">Every system ships with an assembly drawing, glazing specification and a tested performance report for the project file.</p>')
    a('        <p style="margin-top:22px"><a class="link-arrow" href="/downloads/ws90-datasheet.pdf" data-coming-soon>Download WS-90 datasheet ' + I["arrow-sm"] + '</a></p>')
    a('      </div>')
    a('    </div>')
    a('    <div class="metrics reveal">')
    for v, unit, k in (("1.3", "", "Uw value W/m²K"), ("22", "mm", "Visible sightline"),
                       ("3.4", "m", "Max panel height"), ("38", "dB", "Acoustic rating"),
                       ("5.0", "kPa", "Design wind load")):
        a('      <div class="metrics__item"><span class="metrics__v num">%s%s</span><span class="metrics__k">%s</span></div>'
          % (v, ('<small>%s</small>' % unit) if unit else '', k))
    a('    </div>')
    a('  </div>')
    a('</section>')

    # -------------------------------------------------------------- lifestyle
    a('<section class="lifestyle" aria-labelledby="lifestyle-title">')
    a('  <div class="lifestyle__media">')
    a('    <img src="assets/img/lifestyle-dusk-2400.jpg" srcset="assets/img/lifestyle-dusk-1600.jpg 1600w, assets/img/lifestyle-dusk-2400.jpg 2400w" sizes="100vw" alt="Modern house at dusk with a six-metre folding door opening the living room to a lit terrace" loading="lazy" width="2400" height="1180">')
    a('  </div>')
    a('  <figcaption class="lifestyle__card">')
    a('    <p class="eyebrow"><span class="eyebrow__no">03</span>Indoor / outdoor</p>')
    a('    <h2 class="h2" id="lifestyle-title">The opening disappears. The view remains.</h2>')
    a('    <p>A 6.0 m clear span on a 5 + 1 folding configuration: no fixed mullion in the sightline, a 20 mm floor track flush with the terrace. Warm interior light, cool dusk exterior — the envelope stays sealed on both sides.</p>')
    a('    <a class="link-arrow" href="#catalogue">Aluminium folding doors ' + I["arrow-sm"] + '</a>')
    a('  </figcaption>')
    a('</section>')

    # ---------------------------------------------------------------- factory
    a('<section class="section" id="factory">')
    a('  <div class="container">')
    a('    <div class="section-head reveal">')
    a('      <div class="section-head__main">')
    a('        <p class="eyebrow"><span class="eyebrow__no">04</span>Manufacturing</p>')
    a('        <h2 class="h2">Own extrusion. Own fabrication.<br>Own quality gate.</h2>')
    a('      </div>')
    a('      <div class="section-head__aside">')
    a('        <p class="lead">40,000 m² under one roof in Foshan: extrusion, CNC machining, powder coating, insulated glazing and water testing — so tolerances do not depend on a third party.</p>')
    a('      </div>')
    a('    </div>')
    a('    <div class="factory__grid">')
    a('      <div class="factory__photos reveal">')
    for img, cap in (("factory-facility.jpg", "Facility · 40,000 m²"), ("factory-welding.jpg", "Fabrication · precision welding"),
                     ("factory-warehouse.jpg", "Export packing · FCL loading"), ("factory-workshop.jpg", "Engineering · CNC programming")):
        a('        <figure><img src="assets/img/%s" alt="%s" loading="lazy" width="1100" height="820"><figcaption>%s</figcaption></figure>' % (img, cap, cap))
    a('      </div>')
    a('      <div class="factory__steps reveal" style="--delay:100ms">')
    steps = [
        ("Extrusion", "6063-T6 billets extruded to profile in-house, aged and anodised or powder coated."),
        ("CNC machining", "Five-axis centres cut drainage, hardware and glazing rebates to ±0.2 mm."),
        ("Powder coating", "Nine-stage pre-treatment and automated line, 60–80 µm AkzoNobel finish."),
        ("IGU assembly", "Low-E, argon-filled double and triple glazing, warm-edge spacer, desiccant filled."),
        ("QC &amp; water test", "Air, water and wind testing to AS 2047 / EN 14351 before every shipment."),
        ("Packing", "Foam-cradled, corner-protected, container-optimised crating for sea freight."),
    ]
    for i, (t, d) in enumerate(steps, 1):
        a('        <div class="step"><span class="step__no">%02d</span><div><h3 class="step__title">%s</h3><p class="step__desc">%s</p></div></div>' % (i, t, d))
    a('      </div>')
    a('    </div>')
    a('    <div class="stats reveal">')
    for v, sup, k in (("15", "+", "Years manufacturing"), ("40,000", "", "m² facility"),
                      ("60", "+", "Export countries"), ("7", "", "Days to a sample")):
        a('      <div class="stats__item"><span class="stats__v num">%s%s</span><span class="stats__k">%s</span></div>'
          % (v, ('<sup>%s</sup>' % sup) if sup else '', k))
    a('    </div>')
    a('  </div>')
    a('</section>')

    # ------------------------------------------------------------ certs
    a('<section class="certs section--tight" id="certifications">')
    a('  <div class="container">')
    a('    <div class="certs__row reveal">')
    for name, sub in (("ISO 9001", "Quality management"), ("CE", "EN 14351-1"), ("SGS", "Third-party audit"),
                      ("AS 2047", "Australian standard"), ("NFRC", "US thermal rating"), ("Uw TEST", "Thermal report")):
        a('      <div class="cert"><span class="cert__name">%s</span><span class="cert__sub">%s</span></div>' % (name, sub))
    a('    </div>')
    a('    <div class="certs__note">')
    a('      <p>Certificates and third-party test reports are available on request for every system.</p>')
    a('      <p>Air permeability · water tightness · wind resistance · thermal transmittance</p>')
    a('    </div>')
    a('  </div>')
    a('</section>')

    # --------------------------------------------------------------- cases
    a('<section class="section" id="cases">')
    a('  <div class="container">')
    a('    <div class="section-head reveal">')
    a('      <div class="section-head__main">')
    a('        <p class="eyebrow"><span class="eyebrow__no">05</span>Project cases</p>')
    a('        <h2 class="h2">Specified in 60+ countries.</h2>')
    a('      </div>')
    a('      <div class="section-head__aside">')
    a('        <p class="lead">Villas, apartments, hotels and commercial facades — supplied factory-direct to architects, builders, developers and distributors.</p>')
    a('        <a class="link-arrow" href="/cases/" data-coming-soon>All case studies ' + I["arrow-sm"] + '</a>')
    a('      </div>')
    a('    </div>')
    a('    <div class="cases__grid">')
    for i, (img, loc, typ, sysname, ratio) in enumerate(CASES):
        a('      <a class="case reveal" href="/cases/" data-coming-soon style="--delay:%dms">' % (i % 3 * 80))
        a('        <span class="case__media" style="aspect-ratio:%s"><img src="assets/img/%s" alt="%s — %s" loading="lazy"></span>' % (ratio, img, loc, sysname))
        a('        <span class="case__body"><span class="case__loc">%s</span><span class="case__type"><em>%s</em><span>%s</span></span></span>' % (loc, typ, sysname))
        a('      </a>')
    a('    </div>')
    a('  </div>')
    a('</section>')

    # ----------------------------------------------------------- catalogue
    a('<section class="section section--offwhite" id="catalogue">')
    a('  <div class="container">')
    a('    <div class="section-head reveal">')
    a('      <div class="section-head__main">')
    a('        <p class="eyebrow"><span class="eyebrow__no">06</span>Catalogue</p>')
    a('        <h2 class="h2">Eight best-sellers. Twelve in total.</h2>')
    a('        <p class="catalogue__note"><i></i>B2B only — pricing on request</p>')
    a('      </div>')
    a('      <div class="section-head__aside">')
    a('        <p class="lead">Uniform drawings, datasheets and CAD details for every system. Hover a product to read its performance summary and request a quotation.</p>')
    a('      </div>')
    a('    </div>')
    a('    <div class="prod-grid">')
    for name, slug, spec, rows in CATALOGUE:
        a('      <article class="prod reveal">')
        a('        <div class="prod__media"><img src="assets/img/products/%s.svg" alt="%s technical elevation" loading="lazy" width="400" height="500"></div>' % (slug, name))
        a('        <div class="prod__info"><h3 class="prod__name">%s</h3><p class="prod__spec">%s</p></div>' % (name, spec))
        a('        <div class="prod__hover">')
        a('          <dl>')
        for k, v in rows:
            a('            <div><dt>%s</dt><dd><b>%s</b></dd></div>' % (k, v))
        a('          </dl>')
        a('          <a class="btn btn--sm" href="#quote">Request A Quote</a>')
        a('        </div>')
        a('      </article>')
    a('    </div>')
    a('  </div>')
    a('</section>')

    # --------------------------------------------------------- collections
    a('<section class="section" id="collections" data-tabs>')
    a('  <div class="container">')
    a('    <div class="section-head reveal" style="align-items:end">')
    a('      <div class="section-head__main">')
    a('        <p class="eyebrow"><span class="eyebrow__no">07</span>Featured collections</p>')
    a('        <h2 class="h2">Shop by opening type<br>or by application.</h2>')
    a('      </div>')
    a('      <div class="section-head__aside">')
    a('        <p class="lead">Five groups by opening type, five by where they are installed — the same tested profiles, specified by project.</p>')
    a('      </div>')
    a('    </div>')
    a('    <div class="tabs-row">')
    a('      <div class="tabs" role="tablist" aria-label="Collection groups">')
    a('        <button class="tab" role="tab" id="tab-opening" aria-selected="true" aria-controls="panel-opening">By opening</button>')
    a('        <button class="tab" role="tab" id="tab-application" aria-selected="false" aria-controls="panel-application" tabindex="-1">By application</button>')
    a('      </div>')
    a('      <div class="rail__nav">')
    a('        <button class="rail__btn" type="button" data-rail="prev" aria-label="Previous collections"><svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M14 8H3M7 4L3 8l4 4" stroke="currentColor" stroke-width="1.4"/></svg></button>')
    a('        <button class="rail__btn" type="button" data-rail="next" aria-label="Next collections"><svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.4"/></svg></button>')
    a('      </div>')
    a('    </div>')
    for key, first in (("opening", True), ("application", False)):
        a('    <div class="rail-wrap" id="panel-%s" role="tabpanel" aria-labelledby="tab-%s" data-panel%s>' % (key, key, '' if first else ' hidden'))
        a('      <div class="rail">')
        tech = key == "opening"
        for name, src, count in COLLECTIONS[key]:
            cls = "rail-card rail-card--tech" if tech else "rail-card"
            if tech:
                media = '<img src="assets/img/products/%s.svg" alt="%s technical elevation" loading="lazy" width="400" height="500">' % (src, name)
            else:
                media = '<img src="assets/img/%s" alt="%s" width="900" height="1100">' % (src, name)
            a('        <a class="%s" href="#catalogue">' % cls)
            a('          <span class="rail-card__media">%s</span>' % media)
            a('          <span class="rail-card__row"><span class="rail-card__name">%s</span><span class="rail-card__count">%s</span></span>' % (name, count))
            a('        </a>')
        a('      </div>')
        a('    </div>')
    a('  </div>')
    a('</section>')

    # --------------------------------------------------------------- quote
    a('<section class="section section--offwhite" id="quote">')
    a('  <div class="container">')
    a('    <div class="quote__grid">')
    a('      <div class="quote__intro reveal">')
    a('        <p class="eyebrow"><span class="eyebrow__no">08</span>Start a project</p>')
    a('        <h2 class="h2">Send us your opening schedule.</h2>')
    a('        <p class="lead">Share drawings, sizes or a specification and we will return a factory-direct quotation, lead time and shipping plan — usually within one business day.</p>')
    a('        <dl class="quote__contact">')
    a('          <div><dt>Email</dt><dd><a href="mailto:liangjinhao0213@gmail.com">liangjinhao0213@gmail.com</a></dd></div>')
    a('          <div><dt>WhatsApp</dt><dd><a href="https://wa.me/8617818819386" target="_blank" rel="noopener">+86 178 1881 9386</a></dd></div>')
    a('          <div><dt>Phone</dt><dd><a href="tel:+8617818819386">+86 178 1881 9386</a></dd></div>')
    a('          <div><dt>Address</dt><dd>No. 7, Dalingdi, Zhongxiu Second Village Group, Tangbian Village, Shishan Town, Foshan, Guangdong, China</dd></div>')
    a('        </dl>')
    a('        <div class="quote__badges">')
    for b in ("CAD / DWG welcome", "MOQ 1 set", "FOB · CIF · DDP"):
        a('          <span class="badge">%s</span>' % b)
    a('        </div>')
    a('      </div>')
    a('      <form class="form reveal" id="quote-form" style="--delay:100ms" novalidate>')
    a('        <div class="form__row">')
    a('          <div class="field"><label for="f-name">Name *</label><input id="f-name" name="name" type="text" required autocomplete="name" placeholder="Your name"></div>')
    a('          <div class="field"><label for="f-company">Company</label><input id="f-company" name="company" type="text" autocomplete="organization" placeholder="Company / studio"></div>')
    a('        </div>')
    a('        <div class="form__row">')
    a('          <div class="field"><label for="f-email">Email *</label><input id="f-email" name="email" type="email" required autocomplete="email" placeholder="name@company.com"></div>')
    a('          <div class="field"><label for="f-whatsapp">WhatsApp</label><input id="f-whatsapp" name="whatsapp" type="tel" autocomplete="tel" placeholder="+1 555 000 0000"></div>')
    a('        </div>')
    a('        <div class="field"><label for="f-type">Project type</label>')
    a('          <select id="f-type" name="project-type">')
    a('            <option value="">Select…</option>')
    for o in ("Villa / residence", "Apartment / multi-family", "Hotel / hospitality", "Commercial / office", "Distributor / trade"):
        a('            <option>%s</option>' % o)
    a('          </select>')
    a('        </div>')
    a('        <div class="field"><label for="f-message">Message</label><textarea id="f-message" name="message" rows="4" placeholder="Sizes, quantities, glazing, destination port…"></textarea></div>')
    a('        <div class="field field--file">')
    a('          <label for="f-file">Attach drawings — PDF or DWG, max 20 MB</label>')
    a('          <div class="file-row">')
    a('            <label class="file-btn" for="f-file">Choose file</label>')
    a('            <span class="file-name" id="f-file-name">No file selected</span>')
    a('            <input class="sr-only" id="f-file" name="file" type="file" accept=".pdf,.dwg,.dxf,.jpg,.png">')
    a('          </div>')
    a('        </div>')
    a('        <p class="form__status" id="quote-status" role="status" hidden></p>')
    a('        <div class="form__foot">')
    a('          <p class="form__note">By sending you agree to our privacy policy. No third-party marketing, ever.</p>')
    a('          <button class="btn" type="submit">Send enquiry ' + I["arrow-sm"] + '</button>')
    a('        </div>')
    a('      </form>')
    a('    </div>')
    a('  </div>')
    a('</section>')
    a('</main>')

    # -------------------------------------------------------------- footer
    a('<footer class="site-footer" id="footer">')
    a('  <div class="container">')
    a('    <div class="footer__grid">')
    a('      <div class="footer__brand">')
    a('        <span class="footer__logo"><img src="assets/img/logo-on-dark.png" alt="Weinas — Doors And Windows Manufacturer" width="190" height="52" loading="lazy"></span>')
    a('        <p>Factory-direct aluminium doors and windows for architects, builders and distributors in 60+ countries. Thermally broken systems, engineered in Foshan.</p>')
    a('      </div>')
    a('      <div>')
    a('        <h3 class="footer__title">Products</h3>')
    a('        <ul class="footer__links footer__links--single">')
    for name, slug, spec in PRODUCTS:
        a('          <li><a href="#catalogue">%s</a></li>' % name)
    a('        </ul>')
    a('      </div>')
    a('      <div>')
    a('        <h3 class="footer__title">Company</h3>')
    a('        <ul class="footer__links">')
    for label, href, soon in (("About Us", "#factory", False), ("Videos", "/videos/", True), ("News", "/news/", True),
                              ("Cases", "#cases", False), ("Certifications", "#certifications", False), ("Contact Us", "#quote", False)):
        a('          <li><a href="%s"%s>%s</a></li>' % (href, ' data-coming-soon' if soon else '', label))
    a('        </ul>')
    a('      </div>')
    a('      <div>')
    a('        <h3 class="footer__title">Contact</h3>')
    a('        <div class="footer__contact">')
    a('          <p>' + I["pin"] + '<span>No. 7, Dalingdi,<br>Zhongxiu Second Village Group,<br>Tangbian Village, Shishan Town,<br>Foshan, Guangdong, China</span></p>')
    a('          <a href="mailto:liangjinhao0213@gmail.com">' + I["mail"] + '<span>liangjinhao0213@gmail.com</span></a>')
    a('          <a href="tel:+8617818819386">' + I["phone"] + '<span>+86 178 1881 9386</span></a>')
    a('          <a href="https://wa.me/8617818819386" target="_blank" rel="noopener">' + I["wa"] + '<span>WhatsApp · +86 178 1881 9386</span></a>')
    a('        </div>')
    a('        <form class="newsletter" id="newsletter-form">')
    a('          <p class="newsletter__label">Technical newsletter</p>')
    a('          <div class="newsletter__row">')
    a('            <label class="sr-only" for="newsletter-email">Email address</label>')
    a('            <input id="newsletter-email" type="email" name="email" required placeholder="Email address">')
    a('            <button type="submit" aria-label="Subscribe">' + I["arrow-sm"] + '</button>')
    a('          </div>')
    a('          <p class="form__status" id="newsletter-note" role="status" hidden style="margin-top:12px"></p>')
    a('        </form>')
    a('      </div>')
    a('    </div>')
    a('    <div class="footer__bottom">')
    a('      <p class="footer__legal"><strong>Weinas Window &amp; Door Co., Ltd.</strong> — Doors And Windows Manufacturer</p>')
    a('      <div class="footer__meta">')
    a('        <span>© <span id="year">2026</span> Weinas</span>')
    a('        <a href="/privacy/" data-coming-soon>Privacy</a>')
    a('        <a href="/terms/" data-coming-soon>Terms</a>')
    a('        <div class="footer__social">')
    a('          <a href="https://www.linkedin.com/" target="_blank" rel="noopener" aria-label="LinkedIn">' + I["li"] + '</a>')
    a('          <a href="https://www.youtube.com/" target="_blank" rel="noopener" aria-label="YouTube">' + I["yt"] + '</a>')
    a('          <a href="https://www.instagram.com/" target="_blank" rel="noopener" aria-label="Instagram">' + I["pin-social"] + '</a>')
    a('        </div>')
    a('      </div>')
    a('    </div>')
    a('  </div>')
    a('</footer>')

    a('<a class="floating-quote" id="floating-quote" href="#quote">Get A Quote ' + I["arrow-sm"] + '</a>')

    # -------------------------------------------------------------- toasts
    a('<div class="toast" id="toast" role="status" aria-live="polite" hidden></div>')

    # ------------------------------------------------------------- JSON-LD
    a('<script type="application/ld+json">')
    a('{')
    a('  "@context": "https://schema.org",')
    a('  "@type": "Organization",')
    a('  "name": "Weinas Window & Door Co., Ltd.",')
    a('  "alternateName": "Weinas",')
    a('  "url": "https://www.weinas.com/",')
    a('  "logo": "https://www.weinas.com/assets/img/logo.png",')
    a('  "description": "Aluminium door and window manufacturer producing slim-sightline sliding, casement, folding and pivot systems for export markets.",')
    a('  "address": {')
    a('    "@type": "PostalAddress",')
    a('    "streetAddress": "No. 7, Dalingdi, Zhongxiu Second Village Group, Tangbian Village, Shishan Town",')
    a('    "addressLocality": "Foshan",')
    a('    "addressRegion": "Guangdong",')
    a('    "addressCountry": "CN"')
    a('  },')
    a('  "email": "liangjinhao0213@gmail.com",')
    a('  "telephone": "+86-178-1881-9386",')
    a('  "sameAs": ["https://www.linkedin.com/", "https://www.youtube.com/"]')
    a('}')
    a('</script>')
    a('<script src="assets/js/main.js" defer></script>')
    a('</body>')
    a('</html>')

    return "\n".join(p)


if __name__ == "__main__":
    html = build()
    path = os.path.join(ROOT, "index.html")
    open(path, "w", encoding="utf-8").write(html)
    print("wrote", path, len(html), "bytes")
