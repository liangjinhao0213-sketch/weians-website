# -*- coding: utf-8 -*-
"""Export everything the WordPress importer needs into one JSON file.

Output: weinas-wp/wp-content/themes/weinas/data/products-import.json

Each record:
  category, category_name, title, slug, model, moq, price, delivery, payment,
  detail[][], specs[][], desc[], features[], image (theme-relative),
  gallery[] (theme-relative, already de-duplicated)
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply_source_products as SRC  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))          # default-workspace
SITE = os.path.join(ROOT, "weinas-site")
THEME = os.path.join(ROOT, "weinas-wp", "wp-content", "themes", "weinas")
DATA = os.path.join(THEME, "data")

CATEGORIES = [
    ("aluminium-sliding-doors", "source_products.json", "Aluminium Sliding Doors", 1),
    ("aluminium-casement-windows", "source_casement-windows.json", "Aluminium Casement Windows", 2),
    ("aluminium-sliding-windows", "source_windows.json", "Aluminium Sliding Windows", 3),
    ("interior-sliding-partition-doors", "source_sliding-partition-doors.json", "Interior Sliding Partition Doors", 4),
    ("aluminium-casement-doors", "source_casement-doors.json", "Aluminium Casement Doors", 5),
    ("aluminium-tilt-and-turn-windows", "source_tilt-and-turn-windows.json", "Aluminium Tilt And Turn Windows", 6),
    ("thermal-insulation-windows", "source_thermal-insulation-windows.json", "Thermal Insulation Windows", 7),
    ("aluminium-swing-doors", "source_swing-doors.json", "Aluminium Swing Doors", 8),
    ("aluminium-bathroom-doors", "source_bathroom-doors.json", "Aluminium Bathroom Doors", 9),
    ("aluminium-front-doors", "source_front-doors.json", "Aluminium Front Doors", 10),
    ("aluminium-pivot-doors", "source_pivot-doors.json", "Aluminium Pivot Doors", 11),
    ("aluminium-folding-doors", "source_folding-doors.json", "Aluminium Folding Doors", 12),
]


def load(name):
    p = os.path.join(SITE, "_source", name)
    return json.load(io.open(p, encoding="utf-8")) if os.path.exists(p) else []


def main():
    details = json.load(io.open(os.path.join(SITE, "_source", "source_details.json"), encoding="utf-8"))
    os.makedirs(DATA, exist_ok=True)

    out, cats = [], []
    for slug, fname, name, no in CATEGORIES:
        rows = load(fname)
        cats.append(dict(slug=slug, name=name, no=no, count=len(rows)))

        # how many products in this category share each gallery file
        use = {}
        for r in rows:
            for f in (details.get(r["url"], {}).get("gallery") or []):
                use[f] = use.get(f, 0) + 1

        for r in rows:
            d = details.get(r["url"], {})
            table = dict((k, v) for k, v in (r.get("specs") or []))
            gallery = []
            for f in (d.get("gallery") or []):
                if slug == "aluminium-sliding-doors" and use.get(f, 0) >= 2:
                    continue
                if f not in gallery:
                    gallery.append(f)
            out.append(dict(
                category=slug,
                category_name=name,
                title=r["title"],
                slug=r["slug"],
                model=table.get("Model Number") or table.get("Model") or "",
                moq=table.get("MOQ", ""),
                price=table.get("Price", ""),
                delivery=table.get("Delivery Time") or table.get("Delivery", ""),
                payment=table.get("Payment Terms") or table.get("Payment", ""),
                brand="WEINAS",
                detail=d.get("detail") or [],
                specs=d.get("spec_rows") or [],
                desc=(d.get("desc_paras") or [])[:3],
                features=(d.get("features") or [])[:6],
                image=r.get("local_image") or "",
                gallery=gallery[:4],
                figures=(d.get("desc_files") or [])[:4],
                blurb=(r.get("intro") or "")[:220],
            ))

    path = os.path.join(DATA, "products-import.json")
    io.open(path, "w", encoding="utf-8").write(json.dumps(dict(categories=cats, products=out), ensure_ascii=False))

    print("categories:", len(cats))
    print("products  :", len(out))
    print("with image:", len([p for p in out if p["image"]]))
    print("gallery imgs:", sum(len(p["gallery"]) for p in out))
    print("written   :", path, "%.1f MB" % (os.path.getsize(path) / 1024 / 1024))


if __name__ == "__main__":
    main()
