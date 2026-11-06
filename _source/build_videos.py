# -*- coding: utf-8 -*-
"""Build the Videos page (videos/index.html) on the shared chrome.

Cards play YouTube embeds in a light box. While a card has no video id it shows
the poster and a "coming soon" note instead of an iframe, so the page can go live
before the channel is filled.
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import build_about as A  # noqa: E402
import build_cases as C  # noqa: E402

ROOT = C.ROOT
OUT = os.path.join(ROOT, "videos")
os.makedirs(OUT, exist_ok=True)

HEADER = A.CHROME["header"].replace(
    '<a class="nav__link" href="../videos/index.html" data-coming-soon>Videos</a>',
    '<a class="nav__link is-active" href="../videos/index.html">Videos</a>'
).replace(
    '<a class="nav__link" href="../index.html">Home</a>',
    '<a class="nav__link" href="../index.html">Home</a>'
)

META = {
    "title": "Videos | Weinas Aluminium Windows &amp; Doors",
    "desc": ("Watch the Weinas systems in motion: sliding and folding doors, casement windows, "
             "the Foshan factory floor, water testing and installation on site."),
    "canonical": "https://www.weinas.com/videos/",
    "url": "https://www.weinas.com/videos/",
}

# key, title, category, poster, duration, youtube id ("" = not uploaded yet)
VIDEOS = [
    ("sliding", "WS-90 sliding door: 3.4 m leaves, one hand",
     "Systems", "assets/img/collection-villa.jpg", "0:48", ""),
    ("folding", "6 m clear span on a 5 + 1 folding door",
     "Systems", "assets/img/lifestyle-dusk-1600.jpg", "1:12", ""),
    ("casement", "Casement window: compression seal and drainage",
     "Systems", "assets/img/collection-casement.jpg", "0:56", ""),
    ("factory", "Inside the Foshan factory: extrusion to packing",
     "Factory", "assets/img/factory-welding.jpg", "3:24", ""),
    ("testing", "Water and wind test on a 3.2 m sliding unit",
     "Factory", "assets/img/factory-workshop.jpg", "2:05", ""),
    ("install", "Fitting a flush track in a 20 mm floor slot",
     "Installation", "assets/img/factory-warehouse.jpg", "1:40", ""),
    ("pivot", "Pivot door: offset axis, no visible hinge",
     "Systems", "assets/img/collection-office.jpg", "0:37", ""),
    ("case", "Palm Beach: twelve leaves across three elevations",
     "Case studies", "assets/img/project-palm-beach.jpg", "1:58", ""),
    ("paint", "Powder coating line and the RAL colour check",
     "Factory", "assets/img/factory-facility.jpg", "2:31", ""),
]

TABS = ["All", "Systems", "Factory", "Installation", "Case studies"]

PLAY = ('<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<circle cx="12" cy="12" r="21" stroke="currentColor" stroke-width="1.4"/>'
        '<path d="M10 8.5l6 3.5-6 3.5z" fill="currentColor"/></svg>')

VIDEO_SVG = ('<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">'
             '<rect x="3" y="6" width="13" height="12" rx="1" stroke="currentColor" stroke-width="1.4"/>'
             '<path d="M16 10.5l5-3v9l-5-3z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg>')


def card(v, i):
    key, title, cat, poster, dur, vid = v
    return """      <button class="video-card reveal" type="button"
              data-video="%s" data-title="%s" data-cat="%s"
              style="--delay:%dms">
        <span class="video-card__media">
          <img src="../%s" alt="%s" loading="lazy">
          <span class="video-card__play">%s</span>
          <span class="video-card__dur">%s</span>
        </span>
        <span class="video-card__body">
          <span class="video-card__cat">%s</span>
          <span class="video-card__title">%s</span>
        </span>
      </button>""" % (vid, title.replace('"', '&quot;'), cat, (i % 3) * 70,
                      poster, title.replace('"', '&quot;'), PLAY, dur, cat, title)


def build():
    cards = "\n".join(card(v, i) for i, v in enumerate(VIDEOS))
    tabs = "".join(
        '<button class="tab%s" type="button" data-filter="%s">%s</button>'
        % (" is-active" if t == "All" else "", t, t) for t in TABS)

    body = """<section class="page-hero page-hero--videos">
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="../index.html">Home</a><i>/</i><span aria-current="page">Videos</span>
    </nav>
    <div class="page-hero__grid">
      <div class="page-hero__main">
        <p class="eyebrow"><span class="eyebrow__no">Videos</span>Systems 路 factory 路 site</p>
        <h1 class="page-hero__title">The opening, <span class="hl">in motion</span>.</h1>
        <p class="page-hero__lead">Sliding and folding leaves, casement compression, the extrusion line in Foshan and the moments where a door is actually tested. Short clips, no music, no voice-over.</p>
      </div>
      <div class="page-hero__aside">
        <dl class="blog-meta">
          <div><dt>Clips</dt><dd>%d</dd></div>
          <div><dt>Longest</dt><dd>3 min 24 s</dd></div>
          <div><dt>Language</dt><dd>no narration</dd></div>
        </dl>
      </div>
    </div>
  </div>
</section>

<section class="section--tight">
  <div class="container">
    <div class="video-tabs reveal">
      %s
    </div>
    <div class="video-grid" data-video-grid>
%s
    </div>
    <p class="video-note">New clips are added as each system is installed. Ask for a specific detail and we will film it on the next build.</p>
  </div>
</section>

<section class="cta-band">
  <div class="container cta-band__grid">
    <div>
      <h2>Want to see a specific detail?</h2>
      <p>Tell us the profile, glazing or the site condition and we will film it on the next order, then send the clip by WhatsApp.</p>
    </div>
    <div class="cta-band__actions">
      <a class="btn" href="../contact-us/index.html">Ask the factory</a>
      <a class="btn btn--ghost" href="../products/index.html">Browse systems</a>
    </div>
  </div>
</section>

<div class="vmodal" id="vmodal" hidden>
  <div class="vmodal__backdrop" data-vclose></div>
  <div class="vmodal__panel" role="dialog" aria-modal="true" aria-label="Video player">
    <button class="vmodal__close" type="button" data-vclose aria-label="Close video">
      <svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 3l10 10M13 3L3 13" stroke="currentColor" stroke-width="1.4"/></svg>
    </button>
    <div class="vmodal__stage" id="vstage"></div>
    <p class="vmodal__cap" id="vcap"></p>
  </div>
</div>
""" % (len(VIDEOS), tabs, cards)

    page = C.head(META, 1) + HEADER + A.CHROME["mobile"] + A.CHROME["search"]
    page += '<main id="main">\n' + body + '\n</main>\n' + C.close_page(1)
    io.open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(page)
    print("wrote videos/index.html (%d bytes, %d clips)" % (len(page), len(VIDEOS)))


if __name__ == "__main__":
    build()
