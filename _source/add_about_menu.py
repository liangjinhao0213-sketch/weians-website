# -*- coding: utf-8 -*-
"""Add the About Us dropdown, new sub-pages links, and align company facts with
the real company profile published on aluminium-windowsdoors.com."""
import io
import os

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
PAGE = os.path.join(ROOT, "index.html")
CSS = os.path.join(ROOT, "assets", "css", "style.css")
JS = os.path.join(ROOT, "assets", "js", "main.js")

s = io.open(PAGE, encoding="utf-8").read()

# ------------------------------------------------------------------ 1. facts
FACTS = [
    ("40,000 m² under one roof", "10,000 m² under one roof"),
    ("Facility · 40,000 m²", "Facility · 10,000 m²"),
    ('<span class="stats__v num">40,000</span><span class="stats__k">m² facility</span>',
     '<span class="stats__v num">10,000</span><span class="stats__k">m² facility</span>'),
    ('<span class="stats__v num">60<sup>+</sup></span><span class="stats__k">Export countries</span>',
     '<span class="stats__v num">60–70<sup>%</sup></span><span class="stats__k">Export share</span>'),
    ('<span class="stats__v num">7</span><span class="stats__k">Days to a sample</span>',
     '<span class="stats__v num">100</span><span class="stats__k">Production staff</span>'),
    ("<h2 class=\"h2\">Specified in 60+ countries.</h2>", "<h2 class=\"h2\">Specified worldwide.</h2>"),
    ("distributors in 60+ countries.", "distributors worldwide."),
]
for old, new in FACTS:
    if old not in s:
        print("WARN fact not found:", old[:60])
    s = s.replace(old, new)

# ------------------------------------------------------- 2. desktop About menu
ABOUT_MENU = """<li class="nav__item--has-menu">
          <a class="nav__link" href="about-us/company-profile.html" aria-haspopup="true" aria-expanded="false" aria-controls="about-menu">About Us <svg class="nav__chevron" viewBox="0 0 12 8" fill="none" aria-hidden="true"><path d="M1 1.5l5 5 5-5" stroke="currentColor" stroke-width="1.4"/></svg></a>
          <div class="mega mega--sm" id="about-menu">
            <p class="mega__head"><span>About Weinas</span><span>03 pages</span></p>
            <ul class="mega__list">
              <li><a href="about-us/company-profile.html"><span class="mega__no">01</span><span>Company Profile</span></a></li>
              <li><a href="about-us/factory-tour.html"><span class="mega__no">02</span><span>Factory Tour</span></a></li>
              <li><a href="about-us/quality-control.html"><span class="mega__no">03</span><span>Quality Control</span></a></li>
            </ul>
            <div class="mega__foot">
              <span>Foshan since 2010</span>
              <a href="about-us/company-profile.html">Our story <svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.4"/></svg></a>
            </div>
          </div>
        </li>"""

old_nav = '<li><a class="nav__link" href="#factory" data-spy>About Us</a></li>'
if old_nav not in s:
    raise SystemExit("desktop About link not found")
s = s.replace(old_nav, ABOUT_MENU)

# -------------------------------------------------------- 3. mobile About menu
MOBILE_ABOUT = """<li>
      <button class="mobile-nav__toggle" type="button" aria-expanded="false" aria-controls="mobile-about">About Us <svg class="nav__chevron" viewBox="0 0 12 8" fill="none" aria-hidden="true"><path d="M1 1.5l5 5 5-5" stroke="currentColor" stroke-width="1.4"/></svg></button>
      <ul class="mobile-nav__sub" id="mobile-about">
        <li><a href="about-us/company-profile.html">Company Profile</a></li>
        <li><a href="about-us/factory-tour.html">Factory Tour</a></li>
        <li><a href="about-us/quality-control.html">Quality Control</a></li>
      </ul>
    </li>"""
old_mobile = """<li><a href="#factory">About Us</a></li>
    <li><a href="#quote">Contact Us</a></li>"""
if old_mobile not in s:
    raise SystemExit("mobile About link not found")
s = s.replace(old_mobile, MOBILE_ABOUT + """
    <li><a href="#quote">Contact Us</a></li>""")

# ------------------------------------------------------- 4. footer About link
if '<li><a href="#factory">About Us</a></li>' not in s:
    raise SystemExit("footer About link not found")
s = s.replace('<li><a href="#factory">About Us</a></li>',
              '<li><a href="about-us/company-profile.html">About Us</a></li>')

io.open(PAGE, "w", encoding="utf-8").write(s)
print("index.html patched")

# ------------------------------------------------------------------- 5. CSS
c = io.open(CSS, encoding="utf-8").read()

c = c.replace(""".nav__item--has-menu.is-open > .nav__link .nav__chevron { transform: rotate(180deg); }""",
""".nav__item--has-menu { position: relative; }
.nav__item--has-menu.is-open > .nav__link .nav__chevron { transform: rotate(180deg); }""")

c = c.replace(""".mega {
  position: absolute;
  top: calc(100% - 6px);
  left: 50%;
  width: 520px;""",
""".mega {
  position: absolute;
  top: calc(100% + 14px);
  left: 50%;
  width: 520px;""")

c = c.replace(""".mega__list {
  display: grid;
  grid-template-columns: 1fr 1fr;
  padding: 8px 0;
}""",
""".mega__list {
  display: grid;
  grid-template-columns: 1fr 1fr;
  padding: 8px 0;
}
.mega--sm { width: 348px; }
.mega--sm .mega__list { grid-template-columns: 1fr; }""")

# mobile accordion chevron already rotates; keep parity for the new item
io.open(CSS, "w", encoding="utf-8").write(c)
print("css patched")

# -------------------------------------------------------------------- 6. JS
j = io.open(JS, encoding="utf-8").read()

start = j.index("  /* ---------------------------------------------------------- mega menu */")
end = j.index("  /* --------------------------------------------------------- mobile nav */")
new_js = '''  /* --------------------------------------------------------- mega menus */
  var menuItems = $$(".nav__item--has-menu");

  function menuTrigger(item) {
    return $(".nav__toggle", item) || $(".nav__link", item);
  }
  function closeItem(item) {
    item.classList.remove("is-open");
    var t = menuTrigger(item);
    if (t) t.setAttribute("aria-expanded", "false");
  }
  function openItem(item) {
    menuItems.forEach(function (other) {
      if (other !== item) closeItem(other);
    });
    item.classList.add("is-open");
    var t = menuTrigger(item);
    if (t) t.setAttribute("aria-expanded", "true");
  }
  function isOpen(item) {
    return item.classList.contains("is-open");
  }

  menuItems.forEach(function (item) {
    var trigger = $(".nav__toggle", item);
    var timer = null;

    if (trigger) {
      /* button trigger: click toggles */
      trigger.addEventListener("click", function (e) {
        e.preventDefault();
        if (isOpen(item)) closeItem(item);
        else openItem(item);
      });
    } else {
      /* link trigger: click navigates, menu is hover/focus driven */
      var link = $(".nav__link", item);
      if (link) link.addEventListener("click", function () { closeItem(item); });
    }

    item.addEventListener("mouseenter", function () {
      if (!mqlFine.matches) return;
      window.clearTimeout(timer);
      openItem(item);
    });
    item.addEventListener("mouseleave", function () {
      if (!mqlFine.matches) return;
      window.clearTimeout(timer);
      timer = window.setTimeout(function () { closeItem(item); }, 160);
    });
    item.addEventListener("focusin", function () {
      if (mqlFine.matches) openItem(item);
    });
    item.addEventListener("focusout", function (e) {
      if (!item.contains(e.relatedTarget)) closeItem(item);
    });
  });

  doc.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    menuItems.forEach(function (item) {
      if (isOpen(item)) {
        closeItem(item);
        var t = menuTrigger(item);
        if (t) t.focus();
      }
    });
  });
  doc.addEventListener("click", function (e) {
    menuItems.forEach(function (item) {
      if (isOpen(item) && !item.contains(e.target)) closeItem(item);
    });
  });

'''
j = j[:start] + new_js + j[end:]
io.open(JS, "w", encoding="utf-8").write(j)
print("js patched")
