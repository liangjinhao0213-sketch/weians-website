# -*- coding: utf-8 -*-
"""Turn the scraped article dumps into clean, structured posts."""
import io
import json
import os
import re

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
RAW = os.path.join(ROOT, "_source", "articles.json")

# slug -> (hero image, category label)
META = {
    "rainwater-protection-coastal-residences": ("project-palm-beach.jpg", "Water management"),
    "wind-pressure-high-rise-balconies": ("collection-facade.jpg", "Structural"),
    "water-leakage-coastal-high-rises": ("project-dubai.jpg", "Water management"),
    "chinese-new-year-orders": ("factory-warehouse.jpg", "Factory"),
    "heavy-duty-aluminium-sliding-door": ("top-pick-frames.jpg", "Systems"),
    "macaroon-colour-casement-doors": ("project-cottesloe.jpg", "Finishes"),
}

SLUGS = [
    "rainwater-protection-coastal-residences",
    "wind-pressure-high-rise-balconies",
    "water-leakage-coastal-high-rises",
    "chinese-new-year-orders",
    "heavy-duty-aluminium-sliding-door",
    "macaroon-colour-casement-doors",
]

BOILER = {
    "Blog Details", "Home", "Blog", "Contact Us", "Send", "Social Media", "Quick Link",
    "About Us", "Products", "Solutions", "Video", "VR", "Quote", "Contact Now",
    "Previous", "Next", "Latest News", "Hot Products", "Related Products",
}

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def tidy(text):
    text = text.replace("？？", "?").replace("??", "?").replace("\u00a0", " ")
    text = text.replace("Oders", "Orders")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def is_heading(line):
    if len(line) > 110:
        return False
    if re.match(r"^\d+\.\s", line):
        return True
    if line.endswith(":") or line.endswith("?"):
        return True
    if line.endswith("."):
        return False
    # short title-cased line without a full stop
    return len(line) < 60


def main():
    raw = json.load(io.open(RAW, encoding="utf-8"))
    posts = []
    for slug, item in zip(SLUGS, raw):
        lines = [tidy(l) for l in item["lines"]]
        lines = [l for l in lines if l]

        # title: the H1 sits immediately above the date line
        date_idx = next((i for i, l in enumerate(lines) if re.match(r"^\d{4}-\d{2}-\d{2}$", l)), 0)
        title = lines[date_idx - 1] if date_idx > 0 else lines[0]

        # date
        date_iso = None
        for l in lines:
            m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", l)
            if m:
                date_iso = "%s-%s-%s" % m.groups()
                break

        start = date_idx + 1
        body_lines = []
        for l in lines[start:]:
            if l in BOILER:
                continue
            if l == title:
                continue
            body_lines.append(l)

        blocks = []
        for l in body_lines:
            kind = "h2" if is_heading(l) else "p"
            if not blocks and kind == "h2":
                kind = "p"
            blocks.append((kind, l))

        # first paragraph becomes the excerpt
        excerpt = next((t for k, t in blocks if k == "p"), "")
        if len(excerpt) > 190:
            excerpt = excerpt[: excerpt.rfind(" ", 0, 185)] + "…"

        y, m, d = (date_iso or "2026-01-01").split("-")
        display = "%d %s %s" % (int(d), MONTHS[int(m) - 1], y)

        image, category = META[slug]
        posts.append({
            "slug": slug,
            "title": title,
            "date_iso": date_iso,
            "date": display,
            "excerpt": excerpt,
            "image": image,
            "category": category,
            "blocks": [{"kind": k, "text": t} for k, t in blocks],
        })

    posts.sort(key=lambda p: p["date_iso"], reverse=True)
    out = os.path.join(ROOT, "_source", "posts.json")
    io.open(out, "w", encoding="utf-8").write(json.dumps(posts, ensure_ascii=False, indent=2))
    for p in posts:
        print("%s | %s | %s | %d blocks" % (p["date_iso"], p["slug"], p["title"][:60], len(p["blocks"])))


if __name__ == "__main__":
    main()
