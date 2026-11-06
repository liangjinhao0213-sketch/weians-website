# -*- coding: utf-8 -*-
"""Homepage revamp:
  1. the navy spec bar becomes three capability badges (1:1 / one-stop / shipping)
  2. "View B2B catalogue" goes to the products index, not an anchor
  3. section 02 becomes an ordering-process block with a live progress track

Run: python build_home_process.py
"""
import io
import os
import re

SITE = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
INDEX = os.path.join(SITE, "index.html")

SPECBAR = """<section class="specbar" id="promise" aria-label="What we do">
  <div class="container specbar__inner">
    <div class="specbar__item">
      <span class="specbar__ico" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none"><path d="M4 9V5.5A1.5 1.5 0 0 1 5.5 4H9M15 4h3.5A1.5 1.5 0 0 1 20 5.5V9M20 15v3.5a1.5 1.5 0 0 1-1.5 1.5H15M9 20H5.5A1.5 1.5 0 0 1 4 18.5V15" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><path d="M9 12h6" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>
      </span>
      <span class="specbar__txt">
        <span class="specbar__k">1:1 fully customised</span>
        <span class="specbar__s">Every opening drawn to your site dimensions</span>
      </span>
    </div>
    <div class="specbar__item">
      <span class="specbar__ico" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none"><path d="M3.5 10.5 12 4l8.5 6.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><path d="M5.5 9.5V19h13V9.5" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/><path d="M9.5 19v-5h5v5" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg>
      </span>
      <span class="specbar__txt">
        <span class="specbar__k">One-stop building solution</span>
        <span class="specbar__s">Windows, doors, partitions and facade from one factory</span>
      </span>
    </div>
    <div class="specbar__item">
      <span class="specbar__ico" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="8.5" stroke="currentColor" stroke-width="1.4"/><path d="M3.5 12h17M12 3.5c2.6 2.7 2.6 14.3 0 17M12 3.5c-2.6 2.7-2.6 14.3 0 17" stroke="currentColor" stroke-width="1.4"/></svg>
      </span>
      <span class="specbar__txt">
        <span class="specbar__k">Global shipping service</span>
        <span class="specbar__s">FOB, CIF or DDP to 40+ countries</span>
      </span>
    </div>
  </div>
</section>"""

STEPS = [
    ("Enquiry", "You send drawings, sizes or a photo of the opening. We confirm what the wall is made of, how the door has to drain and what the site can carry.",
     "assets/img/top-pick-frames.jpg", "WS-90 \u00b7 Palm Beach residence",
     "Site check", "Opening schedule reviewed against the drawing"),
    ("Quotation", "A factory-direct price in 24 hours: profile, glass build-up, hardware, packing and the Incoterm you asked for, itemised line by line.",
     "assets/img/factory-sign.jpg", "Shishan \u00b7 Foshan \u2014 quoting desk",
     "24 hours", "Itemised quotation with the Incoterm stated"),
    ("Design", "Our engineers return shop drawings and a cost-optimised alternative. Nothing is released to the floor until you sign the drawing.",
     "assets/img/factory-workshop.jpg", "Engineering \u00b7 CNC programming",
     "Signed drawing", "Elevations, section, glazing and hardware schedule"),
    ("Production", "Extrusion, machining, powder coating and glazing on one site. You get photo updates at each stage, not a tracking number.",
     "assets/img/factory-welding.jpg", "Fabrication \u00b7 precision welding",
     "Stage photos", "Extrusion, coating and glazing updates plus a QC sheet"),
    ("Delivery", "Panels are crated upright, loaded and sealed. We send the loading photos and the container number the day it sails.",
     "assets/img/factory-warehouse.jpg", "Export packing \u00b7 FCL loading",
     "Documents", "Packing list, loading photos and the bill of lading"),
]


def build_section():
    track = []
    panels = []
    for i, (title, text, img, cap, tag, out) in enumerate(STEPS):
        n = i + 1
        track.append(
            '<button class="flow__node%s" type="button" data-flow-step="%d" role="tab" aria-selected="%s">'
            '<span class="flow__dot"></span><span class="flow__no">%02d</span><span class="flow__label">%s</span></button>'
            % (" is-active" if i == 0 else "", i, "true" if i == 0 else "false", n, title)
        )
        panels.append(
            '<div class="flow__panel%s" data-flow-panel="%d" role="tabpanel">'
            '<p class="flow__kicker">Step %02d \u2014 %s</p>'
            '<h3 class="flow__title">%s</h3><p class="flow__text">%s</p>'
            '<p class="flow__out">%s</p></div>'
            % ("" if i == 0 else "", i, n, tag, title, text, out)
        )

    figures = []
    for i, (title, text, img, cap, tag, out) in enumerate(STEPS):
        figures.append(
            '<figure class="flow__shot%s" data-flow-shot="%d">'
            '<img src="%s" alt="%s" loading="lazy">'
            '<figcaption>%s</figcaption></figure>'
            % ("" if i == 0 else "", i, img, cap, cap)
        )

    return """<section class="section" id="top-picks">
  <div class="container">
    <div class="section-head reveal">
      <div class="section-head__main">
        <p class="eyebrow"><span class="eyebrow__no">02</span>How an order runs</p>
        <h2 class="h2">From drawing to container,<br><span class="hl">in five steps</span>.</h2>
      </div>
      <div class="section-head__aside">
        <p class="lead">The same five steps run on every order, whether it is one door for a villa or four hundred units for a project. Nothing moves to the next step until the previous one is signed off.</p>
      </div>
    </div>

    <div class="flow reveal" data-flow>
      <div class="flow__media">
%s
      </div>
      <div class="flow__body">
        <div class="flow__track" role="tablist" aria-label="Ordering process">
          <span class="flow__rail" aria-hidden="true"><i class="flow__rail-fill"></i></span>
%s
        </div>
        <div class="flow__panels">
%s
        </div>
        <p class="flow__meta"><span data-flow-count>01 / 05</span><span>Auto-advances \u2014 click a step to jump</span></p>
      </div>
    </div>
  </div>
</section>""" % ("\n".join(figures), "\n".join(track), "\n".join(panels))


def main():
    s = io.open(INDEX, encoding="utf-8").read()

    # 1) spec bar -> capability badges
    i = s.find('<section class="specbar"')
    if i > 0:
        j = s.find("</section>", i) + len("</section>")
        s = s[:i] + SPECBAR + s[j:]
        print("spec bar replaced")
    else:
        print("spec bar not found")

    # 2) catalogue link -> products page
    s = s.replace('<a class="link-arrow" href="#catalogue">View B2B catalogue',
                  '<a class="link-arrow" href="products/index.html">View B2B catalogue')
    print("catalogue link:", 'href="products/index.html">View B2B catalogue' in s)

    # 3) section 02 -> ordering process
    k = s.find('id="top-picks"')
    if k > 0:
        start = s.rfind("<section", 0, k)
        end = s.find("</section>", k) + len("</section>")
        s = s[:start] + build_section() + s[end:]
        print("section 02 replaced with the process block")
    else:
        print("section 02 not found")

    io.open(INDEX, "w", encoding="utf-8").write(s)
    print("index.html written")


if __name__ == "__main__":
    main()
