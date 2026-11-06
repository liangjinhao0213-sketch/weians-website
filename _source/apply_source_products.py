# -*- coding: utf-8 -*-
"""Feed scraped Weinas listings into the product pages.

Every category listed in SOURCES gets its products replaced by the real ones
from that JSON file (produced by scrape_category.py). Anything not listed keeps
the hand-written placeholder data.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
import products_data as D  # noqa: E402

ROOT = os.path.dirname(HERE)

# a category only switches to the scraped data once it has at least this many
# products - a half-crawled category with 2-3 items looks broken
MIN_COUNT = 6

# category slug -> scraped json in _source/
SOURCES = {
    "aluminium-sliding-doors": "source_products.json",
    "aluminium-sliding-windows": "source_windows.json",
    "aluminium-casement-windows": "source_casement-windows.json",
    "interior-sliding-partition-doors": "source_sliding-partition-doors.json",
    "aluminium-casement-doors": "source_casement-doors.json",
    "aluminium-tilt-and-turn-windows": "source_tilt-and-turn-windows.json",
    "thermal-insulation-windows": "source_thermal-insulation-windows.json",
    "aluminium-swing-doors": "source_swing-doors.json",
    "aluminium-bathroom-doors": "source_bathroom-doors.json",
    "aluminium-front-doors": "source_front-doors.json",
    "aluminium-pivot-doors": "source_pivot-doors.json",
    "aluminium-folding-doors": "source_folding-doors.json",
}


def load(name):
    path = os.path.join(HERE, name)
    if not os.path.exists(path):
        return []
    return json.load(io.open(path, encoding="utf-8"))


def short_blurb(intro, title):
    text = (intro or "").strip()
    if not text:
        return title[:120]
    for sep in (". ", "! ", "? "):
        i = text.find(sep)
        if 40 < i < 170:
            return text[: i + 1]
    return text[:150].rsplit(" ", 1)[0] + "…"


def synth_intro(cat, title, model, profile, glazing, moq, price, delivery):
    """Fallback copy for products whose source page carries no description."""
    return ("%s. %s The frame is %s and the glazing is %s as standard. "
            "Supplied to measure from our Foshan factory: MOQ %s, %s, delivery %s ex-works. "
            "Hardware and finish are confirmed on the quotation." %
            (title.rstrip("."), cat["tagline"], profile, glazing, moq, price, delivery))


def make(cat, raw, idx):
    specs = [(k, v) for k, v in raw["specs"]]
    table = dict(specs)
    model = table.get("Model Number") or ("WEI-%02d" % (idx + 1))
    moq = table.get("MOQ", "on request")
    price = table.get("Price", "on request")
    delivery = table.get("Delivery Time", "25–35 days")
    payment = table.get("Payment Terms", "T/T")

    title = raw["title"]
    intro = (raw.get("intro") or "").strip()
    if not intro:
        intro = synth_intro(cat, title, model, cat["base"][0][1], cat["base"][2][1],
                            moq, price, delivery)
    words = title.split()
    cut = max(1, len(words) - 3)
    head = (" ".join(words[:cut]), " ".join(words[cut:]))

    return dict(
        code=model,
        name=title,
        blurb=short_blurb(intro, title),
        extra=[("MOQ", moq), ("Price", price)],
        sizes="Made to measure",
        slug=raw["slug"],
        full_name=title,
        head=head,
        chips=[model, price, moq],
        table=[("Brand", "WEINAS"), ("Model", model), ("MOQ", moq), ("Price", price),
               ("Delivery", delivery), ("Payment", payment)],
        options=[
            ("Profile", cat["base"][0][1]),
            ("Thermal break", cat["base"][1][1]),
            ("Glazing", cat["base"][2][1] + " — low-E, laminated or silk-screen on request"),
            ("Hardware", cat["base"][3][1] + " — German brands, RC2 upgrade available"),
            ("Finish", "Powder coat in any RAL, anodised, or wood-grain transfer"),
            ("Size", "Made to the opening; priced per square metre"),
        ],
        source_url=raw.get("url", ""),
        modal_specs=[["Model", model], ["MOQ", moq], ["Price", price],
                     ["Delivery", delivery], ["Payment", payment]],
        image="products-src/" + raw["local_image"].split("/")[-1] if raw.get("local_image") else None,
        intro=intro,
        body=raw.get("body", []),
        source_specs=specs,
        index=idx,
    )


def price_range(products):
    lo, hi = [], []
    for p in products:
        price = p["table"][3][1] if len(p["table"]) > 3 else ""
        m = re.search(r"USD\s*(\d+)\s*[-–]\s*(\d+)", price)
        if m:
            lo.append(int(m.group(1)))
            hi.append(int(m.group(2)))
    return ("USD%d–%d / m²" % (min(lo), max(hi))) if lo else None


def run():
    done = []
    for slug, jf in SOURCES.items():
        raw = load(jf)
        if len(raw) < MIN_COUNT:
            if raw:
                print("skip %s: only %d scraped so far" % (slug, len(raw)))
            continue
        cat = next((c for c in D.CATEGORIES if c["slug"] == slug), None)
        if not cat:
            continue
        cat["products_full"] = [make(cat, r, i) for i, r in enumerate(raw)]
        cat["source_count"] = len(cat["products_full"])
        cat["products"] = [(p["code"], p["name"], p["blurb"], p["extra"], p["sizes"])
                           for p in cat["products_full"]]

        n = len(cat["products_full"])
        price = price_range(cat["products_full"]) or "on request"
        cat["chips"] = ["%d models" % n, price, "MOQ 4–6 m²"]
        cat["lead"] = ("%s %d systems in the range, priced %s, MOQ 4–6 m², "
                       "delivery 25–35 days ex-works Foshan." % (cat["tagline"], n, price))
        done.append((slug, n))
    for slug, n in done:
        print("%s -> %d scraped products" % (slug, n))
    return done


if __name__ == "__main__":
    run()
    print("ok")
