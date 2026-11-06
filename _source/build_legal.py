# -*- coding: utf-8 -*-
"""Build /privacy/ and /terms/ on the shared chrome.

These pages are linked from the footer of every page, so they have to exist.
Content is a plain B2B policy: what the enquiry form collects, how long it is
kept, who it is shared with (nobody), and how to ask for deletion.

Run: python build_legal.py
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import build_cases as C  # noqa: E402

ROOT = C.ROOT

PRIVACY = [
    ("h", "Who we are"),
    ("p", "Foshan Weinas Energy Saving Curtain Wall Doors and Windows Technology Co., Ltd. (\u201cWeinas\u201d, \u201cwe\u201d) manufactures aluminium doors and windows at No. 7, Dalingdi, Zhongxiu Second Village Group, Tangbian Village, Shishan Town, Foshan, Guangdong, China. This page explains what we do with the information you send us."),
    ("h", "What we collect"),
    ("p", "When you send an enquiry through this website we receive the name, company, email address, WhatsApp number, project type and message you type into the form, plus the page you sent it from. We do not ask for, and do not want, payment card details through this form."),
    ("p", "Our server records the IP address that submitted the form for thirty seconds so that repeated submissions can be blocked. That record is used only for spam prevention."),
    ("h", "Why we hold it"),
    ("p", "To answer your enquiry: to prepare a quotation, to check a specification against a drawing, to arrange samples, and to keep the commercial record of what was agreed. We rely on our legitimate interest in responding to business enquiries, and on your consent for any follow-up marketing."),
    ("h", "How long we keep it"),
    ("p", "Quotation requests are kept for twenty-four months from the last exchange, so that a re-order can be priced against the same specification. Anything older is deleted. You can ask us to delete your enquiry at any time and we will do so within thirty days."),
    ("h", "Who sees it"),
    ("p", "Our sales and engineering staff in Foshan, and nobody else. We do not sell, rent or trade contact details. We do not run third-party advertising or tracking scripts on this site."),
    ("h", "Cookies"),
    ("p", "The site itself sets no tracking cookies. If your browser stores a session for the enquiry form it expires when you close the tab."),
    ("h", "Your rights"),
    ("p", "You can ask us for a copy of what we hold, ask us to correct it, or ask us to delete it. Write to liangjinhao0213@gmail.com with the subject line \u201cPrivacy request\u201d and we will reply within thirty days."),
    ("h", "Changes"),
    ("p", "If this policy changes we will update this page. The version above is the one in force from 1 November 2026."),
]

TERMS = [
    ("h", "Scope"),
    ("p", "These terms cover the use of this website and the information published on it. They are not the terms of sale: quotations, orders and deliveries are governed by the contract and the Incoterms stated on the quotation itself."),
    ("h", "Information on this site"),
    ("p", "Drawings, dimensions, Uw values, wind-load figures and finish codes describe our standard systems. Actual performance depends on the panel size, the glass build-up, the installation and the building it is fixed to. Confirm the specification with our engineering team before you order."),
    ("p", "Colours shown on screen are approximations. Powder-coat finishes are matched to RAL or to a physical sample, not to a monitor."),
    ("h", "Quotations"),
    ("p", "A quotation is valid for thirty days unless it states otherwise, and is subject to the stated Incoterm, the payment terms on the quotation and the price of aluminium at the time of confirmation."),
    ("h", "Intellectual property"),
    ("p", "The profile drawings, photographs, text and the Weinas name on this site belong to us. You may use them to evaluate or specify our systems. Do not republish them commercially without written permission."),
    ("h", "Liability"),
    ("p", "We keep this site accurate, but it is provided as it stands. We are not liable for a decision taken on the basis of a web page alone \u2014 always work from the issued drawing and the signed confirmation."),
    ("h", "Governing law"),
    ("p", "These website terms are governed by the laws of the People\u2019s Republic of China. Disputes that cannot be settled by discussion go to the courts of Foshan, Guangdong."),
    ("h", "Contact"),
    ("p", "Questions about these terms: liangjinhao0213@gmail.com, or +86 178 1881 9386 on WhatsApp."),
]


def render(blocks):
    out = []
    for kind, text in blocks:
        if kind == "h":
            out.append("        <h2>%s</h2>" % text)
        else:
            out.append("        <p>%s</p>" % text)
    return "\n".join(out)


def build_page(slug, title, label, lead, blocks):
    meta = {
        "title": "%s | Weinas Aluminium Windows &amp; Doors" % title,
        "desc": lead,
        "canonical": "https://www.weinas.com/%s/" % slug,
        "url": "https://www.weinas.com/%s/" % slug,
    }
    body = """<section class="page-hero">
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="../index.html">Home</a><i>/</i><span aria-current="page">%s</span>
    </nav>
    <div class="page-hero__grid">
      <div class="page-hero__main">
        <p class="eyebrow"><span class="eyebrow__no">Legal</span>Weinas 路 Foshan</p>
        <h1 class="page-hero__title">%s</h1>
        <p class="page-hero__lead">%s</p>
      </div>
      <div class="page-hero__aside">
        <dl class="blog-meta">
          <div><dt>Applies to</dt><dd>this website</dd></div>
          <div><dt>Version</dt><dd>1 Nov 2026</dd></div>
          <div><dt>Contact</dt><dd>liangjinhao0213@gmail.com</dd></div>
        </dl>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="prose reveal" style="max-width:72ch">
%s
    </div>
  </div>
</section>
""" % (label, title, lead, render(blocks))

    parts = C.chrome(1)
    page = C.head(meta, 1) + parts["header"] + parts["mobile"] + parts["search"]
    page += '<main id="main">\n' + body + '\n</main>\n' + C.close_page(1)

    out_dir = os.path.join(ROOT, slug)
    os.makedirs(out_dir, exist_ok=True)
    io.open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write(page)
    print("wrote %s/index.html (%d bytes)" % (slug, len(page)))


def main():
    build_page(
        "privacy", "Privacy Policy", "Privacy",
        "What the enquiry form collects, how long we keep it, and how to have it deleted.",
        PRIVACY,
    )
    build_page(
        "terms", "Terms of Use", "Terms",
        "The terms that apply to this website. Quotations and orders are governed by the contract issued with them.",
        TERMS,
    )


if __name__ == "__main__":
    main()
