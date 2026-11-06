# -*- coding: utf-8 -*-
"""Build the Contact Us page (contact-us/index.html) on the shared chrome."""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import build_about as A  # noqa: E402
import icons  # noqa: E402

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
OUT = os.path.join(ROOT, "contact-us")
os.makedirs(OUT, exist_ok=True)

HEADER = A.CHROME["header"].replace("../index.html#quote", "#quote").replace(
    '<a class="nav__link" href="../contact-us/index.html">Contact Us</a>',
    '<a class="nav__link is-active" href="../contact-us/index.html">Contact Us</a>')

META = {
    "title": "Contact Us | Weinas Aluminium Windows &amp; Doors",
    "desc": ("Contact Weinas in Foshan: WhatsApp +86 178 1881 9386, email liangjinhao0213@gmail.com, "
             "No. 7 Dalingdi, Tangxiu Second Village Group, Tangbian Village, Shishan Town, Foshan. "
             "Send drawings for a factory-direct quotation."),
    "canonical": "https://www.weinas.com/contact-us/",
    "url": "https://www.weinas.com/contact-us/",
}

FORM = """<form class="form reveal" id="quote-form" novalidate>
  <div class="form__row">
    <div class="field"><label for="f-name">Name *</label><input id="f-name" name="name" type="text" required autocomplete="name" placeholder="Your name"></div>
    <div class="field"><label for="f-company">Company</label><input id="f-company" name="company" type="text" autocomplete="organization" placeholder="Company / studio"></div>
  </div>
  <div class="form__row">
    <div class="field"><label for="f-email">Email *</label><input id="f-email" name="email" type="email" required autocomplete="email" placeholder="name@company.com"></div>
    <div class="field"><label for="f-whatsapp">WhatsApp</label><input id="f-whatsapp" name="whatsapp" type="tel" autocomplete="tel" placeholder="+1 555 000 0000"></div>
  </div>
  <div class="field"><label for="f-type">Project type</label>
    <select id="f-type" name="project-type">
      <option value="">Select…</option>
      <option>Villa / residence</option>
      <option>Apartment / multi-family</option>
      <option>Hotel / hospitality</option>
      <option>Commercial / office</option>
      <option>Distributor / trade</option>
    </select>
  </div>
  <div class="field"><label for="f-message">Message</label><textarea id="f-message" name="message" rows="4" placeholder="Sizes, quantities, glazing, destination port…"></textarea></div>
  <div class="field field--file">
    <label for="f-file">Attach drawings — PDF or DWG, max 20 MB</label>
    <div class="file-row">
      <label class="file-btn" for="f-file">Choose file</label>
      <span class="file-name" id="f-file-name">No file selected</span>
      <input class="sr-only" id="f-file" name="file" type="file" accept=".pdf,.dwg,.dxf,.jpg,.png">
    </div>
  </div>
  <p class="form__status" id="quote-status" role="status" hidden></p>
  <div class="form__foot">
    <p class="form__note">By sending you agree to our privacy policy. No third-party marketing, ever.</p>
    <button class="btn" type="submit">Send enquiry <svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.4"/></svg></button>
  </div>
</form>"""

SOCIAL = """
<section class="section section--tight">
  <div class="container">
    <div class="social reveal">
      <div>
        <p class="eyebrow"><span class="eyebrow__no">05</span>Social media</p>
        <h2 class="h3" style="margin-top:14px">Follow the factory.</h2>
      </div>
      <ul class="social__list">
%s
      </ul>
    </div>
  </div>
</section>
""" % "\n".join(
    '        <li><a class="social__btn social__btn--%s" href="%s" target="_blank" rel="noopener" aria-label="%s"%s>%s</a></li>'
    % (key, href, label,
       ' data-coming-soon data-toast="%s — profile link to be added."' % note if note else "",
       icons.icon(key, 22))
    for key, label, path, href, note in icons.SOCIALS)


def build():
    body = """<section class="page-hero page-hero--contact">
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="../index.html">Home</a><i>/</i><span aria-current="page">Contact us</span>
    </nav>
    <div class="page-hero__grid">
      <div class="page-hero__main">
        <p class="eyebrow"><span class="eyebrow__no">Contact</span>Foshan · Guangdong</p>
        <h1 class="page-hero__title">Talk to <span class='hl'>the factory</span>, not a trading desk.</h1>
        <p class="page-hero__lead">Send drawings, sizes or a specification and you will hear back from the engineering team — usually within one business day.</p>
      </div>
      <div class="page-hero__aside">
        <dl class="blog-meta">
          <div><dt>Reply</dt><dd>within 1 business day</dd></div>
          <div><dt>Incoterms</dt><dd>FOB · CIF · DDP</dd></div>
          <div><dt>Drawings</dt><dd>CAD / DWG welcome</dd></div>
        </dl>
      </div>
    </div>
  </div>
</section>

<section class="contact-band">
  <img src="../assets/img/factory-sign.jpg" alt="Weinas factory loading bay with packed window and door sets" width="1800" height="931">
  <div class="container">
    <figcaption class="contact-band__cap"><span>Shishan · Foshan — loading bay</span><span>10,000 m² facility</span></figcaption>
  </div>
</section>

<section class="section--tight">
  <div class="container">
    <div class="contact-grid reveal">
      <div class="contact-item">
        <svg viewBox="0 0 24 24" fill="none"><rect x="3" y="5" width="18" height="14" rx="1" stroke="currentColor" stroke-width="1.4"/><path d="M3.5 6.5 12 13l8.5-6.5" stroke="currentColor" stroke-width="1.4"/></svg>
        <h3>Email</h3>
        <a href="mailto:liangjinhao0213@gmail.com">liangjinhao0213@gmail.com</a>
      </div>
      <div class="contact-item">
        <svg viewBox="0 0 24 24" fill="none"><path d="M4 20l1.2-3.8A8.5 8.5 0 1 1 12 20H4Z" stroke="currentColor" stroke-width="1.4"/><path d="M9.2 8.4c.2-.4.4-.4.6-.4h.5c.2 0 .3.1.4.4l.6 1.4c.1.2 0 .3-.1.4l-.4.5c.4.8 1.1 1.5 1.9 1.9l.5-.4c.1-.1.3-.2.4-.1l1.4.6c.2.1.4.2.4.4v.5c0 .5-.4 1-1 1-2.6 0-5.2-2.6-5.2-5.2 0-.5.1-1 .5-1Z" fill="currentColor"/></svg>
        <h3>WhatsApp</h3>
        <a href="https://wa.me/8617818819386" target="_blank" rel="noopener">+86 178 1881 9386</a>
      </div>
      <div class="contact-item">
        <svg viewBox="0 0 24 24" fill="none"><path d="M6 3h3l1.6 4-2 1.6a12 12 0 0 0 5.8 5.8l1.6-2 4 1.6V18c0 .8-.6 1.4-1.4 1.4A15.6 15.6 0 0 1 4.6 4.4C4.6 3.6 5.2 3 6 3Z" stroke="currentColor" stroke-width="1.4"/></svg>
        <h3>Phone</h3>
        <a href="tel:+8617818819386">+86 178 1881 9386</a>
      </div>
      <div class="contact-item">
        <svg viewBox="0 0 24 24" fill="none"><path d="M12 21s7-6.3 7-11.5A7 7 0 0 0 5 9.5C5 14.7 12 21 12 21Z" stroke="currentColor" stroke-width="1.4"/><circle cx="12" cy="9.5" r="2.6" stroke="currentColor" stroke-width="1.4"/></svg>
        <h3>Factory</h3>
        <p>No. 7, Dalingdi, Zhongxiu Second Village Group, Tangbian Village, Shishan Town, Foshan, Guangdong, China</p>
      </div>
    </div>
  </div>
</section>

<section class="section" id="quote">
  <div class="container">
    <div class="quote__grid">
      <div class="quote__intro reveal">
        <p class="eyebrow"><span class="eyebrow__no">03</span>Enquiry</p>
        <h2 class="h2">Send us your <span class='hl'>opening schedule</span>.</h2>
        <p class="lead">The more we know up front, the faster the quote is useful. Attach drawings if you have them — a sketch with sizes is enough to start.</p>
        <ul class="checklist">
          <li>Opening sizes, quantities and floor-to-head height</li>
          <li>Glazing and thermal requirement (Uw, acoustic, wind load)</li>
          <li>Finish: RAL / anodised / wood grain</li>
          <li>Destination port and required-on-site date</li>
        </ul>
        <p class="contact-note">Visiting Foshan? We can arrange a factory walk-through — mention it in the message.</p>
        <figure class="contact-photo">
          <img src="../assets/img/collection-office.jpg" alt="Weinas showroom with full-size window and door mock-ups" loading="lazy" width="900" height="1100">
        </figure>
      </div>
      %s
    </div>
  </div>
</section>

%s
""" % (FORM, SOCIAL)

    page = A.head(META) + HEADER + A.CHROME["mobile"] + A.CHROME["search"]
    page += '<main id="main">\n' + body + '\n</main>\n'
    page += A.CHROME["footer"] + A.CHROME["floating"].replace("../index.html#quote", "#quote") + "\n" + A.CHROME["toast"] + "\n"
    page += """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ContactPage",
  "name": "Contact Weinas",
  "url": "https://www.weinas.com/contact-us/",
  "mainEntity": {
    "@type": "Organization",
    "name": "Weinas Window & Door Co., Ltd.",
    "email": "liangjinhao0213@gmail.com",
    "telephone": "+86-178-1881-9386",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "No. 7, Dalingdi, Zhongxiu Second Village Group, Tangbian Village, Shishan Town",
      "addressLocality": "Foshan",
      "addressRegion": "Guangdong",
      "addressCountry": "CN"
    }
  }
}
</script>
<script src="../assets/js/main.js" defer></script>
</body>
</html>
"""
    io.open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(page)
    print("wrote contact-us/index.html (%d bytes)" % len(page))


if __name__ == "__main__":
    build()
