# -*- coding: utf-8 -*-
"""Add the global quotation modal and swap the floating quote pill for WhatsApp.

Runs over the already-built static pages (idempotent):
  * every "Get A Quote" anchor gets data-quote-open and opens the modal
  * the floating pill becomes a WhatsApp button, on every page
  * the modal markup is inserted once per page, just before the toast

Run: python add_quote_modal.py
"""
import io
import os
import re

SITE = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"

WA_HREF = "https://wa.me/8617818819386"

WA_SVG = ('<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">'
          '<path d="M12.04 2.5a9.4 9.4 0 0 0-8 14.3L2.5 21.5l4.85-1.5a9.4 9.4 0 1 0 4.69-17.5Z" stroke="currentColor" stroke-width="1.5"/>'
          '<path d="M8.9 7.7c.2-.4.5-.4.8-.4h.5c.2 0 .4 0 .6.4l.8 1.7c.1.3 0 .5-.2.7l-.5.6c-.1.2-.2.4 0 .7.5.8 1.4 1.7 2.4 2.1.3.1.5.1.7-.1l.5-.6c.2-.2.4-.3.7-.2l1.7.8c.3.1.4.3.4.5 0 .7-.3 1.6-.9 2-.6.5-1.6.8-2.7.5-2.5-.6-5-3-5.7-5.5-.2-.8-.1-1.6.2-2.1Z" fill="currentColor"/></svg>')

WA_FLOAT = ('<a class="wa-float" href="%s" target="_blank" rel="noopener" '
            'aria-label="Chat with Weinas on WhatsApp">%s</a>') % (WA_HREF, WA_SVG)

MODAL = """<div class="gquote" id="gquote" hidden>
  <div class="gquote__backdrop" data-gq-close></div>
  <div class="gquote__panel" role="dialog" aria-modal="true" aria-labelledby="gq-title">
    <button class="gquote__close" type="button" data-gq-close aria-label="Close quotation form">
      <svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 3l10 10M13 3L3 13" stroke="currentColor" stroke-width="1.5"/></svg>
    </button>

    <aside class="gquote__side">
      <img class="gquote__img" src="%s" alt="Aluminium sliding doors and windows by Weinas" loading="lazy">
      <div class="gquote__side-body">
        <p class="gquote__kicker">Direct from the factory</p>
        <h2 class="gquote__title" id="gq-title">Tell us about the opening.</h2>
        <ul class="gquote__points">
          <li><span>Quotation</span><span>within 1 business day</span></li>
          <li><span>Drawings</span><span>CAD / DWG welcome</span></li>
          <li><span>Incoterms</span><span>FOB &middot; CIF &middot; DDP</span></li>
        </ul>
        <a class="gquote__wa" href="%s" target="_blank" rel="noopener">
          %s<span>WhatsApp +86 178 1881 9386</span>
        </a>
        <p class="gquote__mail"><a href="mailto:liangjinhao0213@gmail.com">liangjinhao0213@gmail.com</a></p>
      </div>
    </aside>

    <div class="gquote__body">
      <form class="gquote__form" id="gquote-form" novalidate>
        <div class="gquote__row">
          <label class="gfield"><span>Name *</span><input type="text" name="name" required autocomplete="name" placeholder="Your name"></label>
          <label class="gfield"><span>Company</span><input type="text" name="company" autocomplete="organization" placeholder="Company / studio"></label>
        </div>
        <div class="gquote__row">
          <label class="gfield"><span>Email *</span><input type="email" name="email" required autocomplete="email" placeholder="name@company.com"></label>
          <label class="gfield"><span>WhatsApp</span><input type="tel" name="whatsapp" autocomplete="tel" placeholder="+1 555 000 0000"></label>
        </div>
        <label class="gfield"><span>Project type</span>
          <select name="project_type">
            <option value="">Select&hellip;</option>
            <option>Villa / residence</option>
            <option>Apartment / multi-residential</option>
            <option>Hotel / hospitality</option>
            <option>Commercial / office</option>
            <option>Distribution / resale</option>
          </select>
        </label>
        <label class="gfield"><span>Message *</span>
          <textarea name="message" rows="4" required placeholder="Sizes, quantities, glazing, destination port&hellip;"></textarea>
        </label>
        <label class="gfield gfield--hp" aria-hidden="true" tabindex="-1"><span>Website</span><input type="text" name="website" tabindex="-1" autocomplete="off"></label>

        <div class="gquote__foot">
          <p class="gquote__legal">Drawings can follow by email or WhatsApp after we reply.</p>
          <button class="btn gquote__submit" type="submit">Send enquiry
            <svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.4"/></svg>
          </button>
        </div>
        <p class="gquote__status" id="gquote-status" role="status" hidden></p>
      </form>
    </div>
  </div>
</div>
"""


def main():
    changed = 0
    skipped = 0
    pages = 0

    for dp, dn, fs in os.walk(SITE):
        if "_source" in dp:
            continue
        for f in fs:
            if not f.endswith(".html"):
                continue
            p = os.path.join(dp, f)
            s = io.open(p, encoding="utf-8").read()
            orig = s
            depth = os.path.relpath(p, SITE).count(os.sep)
            pref = "../" * depth

            # 1) floating pill -> WhatsApp button
            s = re.sub(r'<a class="floating-quote".*?</a>', WA_FLOAT, s, count=1, flags=re.S)

            # 2) every quote anchor opens the modal
            s = s.replace('<a class="btn header__cta" href="#quote">',
                          '<a class="btn header__cta" href="#quote" data-quote-open>')
            s = s.replace('<a class="btn" href="#quote">',
                          '<a class="btn" href="#quote" data-quote-open>')

            # 3) one modal per page, before the toast
            if 'id="gquote"' not in s:
                img = pref + "assets/img/collection-villa.jpg"
                block = MODAL % (img, WA_HREF, WA_SVG)
                marker = '<div class="toast"'
                i = s.find(marker)
                if i > 0:
                    s = s[:i] + block + s[i:]
                else:
                    s = s.replace("</body>", block + "</body>")

            if s != orig:
                io.open(p, "w", encoding="utf-8").write(s)
                changed += 1
            else:
                skipped += 1
            pages += 1

    print("pages: %d | updated: %d | unchanged: %d" % (pages, changed, skipped))


if __name__ == "__main__":
    main()
