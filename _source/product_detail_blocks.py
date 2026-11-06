# -*- coding: utf-8 -*-
"""New product-detail blocks: rich specification tables + description with images.

Applied to every generated product page. Falls back to the previous copy-only
layout for products whose detail data has not been scraped yet.
"""
import io
import json
import os
import re

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
_DETAILS = None


def details():
    global _DETAILS
    if _DETAILS is None:
        path = os.path.join(ROOT, "_source", "source_details.json")
        try:
            _DETAILS = json.load(io.open(path, encoding="utf-8"))
        except Exception:  # noqa: BLE001
            _DETAILS = {}
    return _DETAILS


JUNK = re.compile(r"\*?SUPPLY ABILITY.*$|STRING\(\d+\)|-->\s*$", re.I)


def tidy(rows):
    """Clean the source table: labels lose their colon, merged cells get split."""
    out = []
    for label, value in rows:
        label = " ".join(str(label).split()).rstrip(":").strip()
        value = " ".join(str(value).split())
        # "PACKAGING DETAILS: FOAM, POLY BAG ..." -> label/value split
        if ":" in label:
            head, _, tail = label.partition(":")
            if len(head) <= 28 and tail.strip():
                label = head.strip()
                value = (tail.strip() + " " + value).strip()
        def scrub(t):
            t = re.split(r"string\(\d+\)", t, flags=re.I)[0]
            t = re.split(r"supply ability", t, flags=re.I)[0]
            t = re.sub(r"-+\s*>", " ", t)
            t = t.replace('"', "").replace("“", "").replace("”", "")
            t = re.sub(r"\s+", " ", t)
            return t.strip(" ,;-*")

        label, value = scrub(label), scrub(value)
        if not label or not value:
            continue
        out.append([label[0].upper() + label[1:] if label.islower() else label, value])
    return out


def _rows(pairs):
    return "".join(
        '<div class="specs2__row"><dt>%s</dt><dd>%s</dd></div>' % (k, v) for k, v in pairs)


def spec_section(p):
    """Two tables: Detail information + Specifications, styled like the site."""
    d = details().get(p.get("source_url") or "", {})
    detail = d.get("detail") or []
    specs = d.get("spec_rows") or []

    # fall back to the six commercial terms if the page had no detail table
    if not detail:
        detail = [[k, v] for k, v in p["table"]]
    if not specs:
        specs = [[k, v] for k, v in p["options"][:4]]

    def dedupe(rows):
        seen, out = set(), []
        for k, v in rows:
            key = (k.lower(), v.lower()[:40])
            if key in seen:
                continue
            seen.add(key)
            out.append([k, v])
        return out

    left = _rows(dedupe(tidy(detail))[:16])
    right = _rows(dedupe(tidy(specs))[:16])

    return """<section class="section--tight" id="spec">
  <div class="container">
    <div class="section-head reveal">
      <div class="section-head__main">
        <p class="eyebrow"><span class="eyebrow__no">Spec</span>Detail information</p>
        <h2 class="h2">Every number<br><span class="hl">behind this system.</span></h2>
      </div>
      <p class="section-head__note">Taken from the production sheet for this model. Anything not listed is set per project.</p>
    </div>
    <div class="specs2">
      <div class="specs2__col">
        <h3 class="specs2__title">Detail information</h3>
        <dl class="specs2__list">%s</dl>
      </div>
      <div class="specs2__col">
        <h3 class="specs2__title">Specifications</h3>
        <dl class="specs2__list">%s</dl>
      </div>
    </div>
  </div>
</section>""" % (left, right)


def _point(text):
    """'Excellent thermal insulation: Thermal breaks ...' -> (title, body)."""
    m = re.match(r"^([^:.]{6,60})[:：]\s*(.+)$", text)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return None, text


def desc_section(p):
    """Copy on the left, source diagrams on the right, arrows when there are several."""
    d = details().get(p.get("source_url") or "", {})
    paras = [t for t in (d.get("desc_paras") or [])][:3]
    name_key = " ".join(p["full_name"].lower().split())
    # drop a title-like first line: short, no full stop, repeated by the next paragraph
    while len(paras) > 1 and len(paras[0]) < 120 and (
            " ".join(paras[0].lower().split()) in name_key
            or paras[0].lower()[:38] in paras[1].lower()):
        paras = paras[1:]
    if not paras:
        paras = [p["intro"]] if p.get("intro") else []
    feats = d.get("features") or []
    files = d.get("desc_files") or []

    lead = paras[0] if paras else ""
    rest = paras[1:]

    points = []
    for f in feats[:6]:
        title, body = _point(f)
        if title:
            points.append('<li><b>%s</b> — %s</li>' % (title, body))
        else:
            points.append("<li>%s</li>" % body)
    others = "".join("<p>%s</p>" % t for t in rest)

    if files:
        stage = "".join(
            '<img src="../../assets/img/%s" alt="%s" loading="lazy"%s>'
            % (f, (p["full_name"] + " — figure %d" % (i + 1))[:110], "" if i == 0 else " hidden")
            for i, f in enumerate(files))
        nav = ('<div class="pgallery__nav">'
               '<button type="button" class="pgallery__btn" data-gallery-prev aria-label="Previous image">%s</button>'
               '<span class="pgallery__count" data-gallery-count>1 / %d</span>'
               '<button type="button" class="pgallery__btn" data-gallery-next aria-label="Next image">%s</button>'
               '</div>' % (ARROW_L, len(files), ARROW_R)) if len(files) > 1 else ""
        media = ('<div class="pgallery" data-gallery>'
                 '<div class="pgallery__stage" data-gallery-stage>%s</div>%s</div>' % (stage, nav))
    else:
        media = ""

    feat_block = ('<ul class="pdesc__points">%s</ul>' % "".join(points)) if points else ""
    if not (lead or feat_block or media):
        return ""

    return """<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <div class="section-head__main">
        <p class="eyebrow"><span class="eyebrow__no">Description</span>Overview</p>
        <h2 class="h2">What this system does.<br><span class="hl">How it is built.</span></h2>
      </div>
    </div>
    <div class="pdesc">
      <div class="pdesc__text">
        <p class="pdesc__lead">%s</p>
        %s%s
      </div>
      %s
    </div>
  </div>
</section>""" % (lead, others, feat_block, media)


ARROW_L = ('<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
           '<path d="M14 8H3M7 4L3 8l4 4" stroke="currentColor" stroke-width="1.4"/></svg>')
ARROW_R = ('<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
           '<path d="M2 8h11M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.4"/></svg>')
