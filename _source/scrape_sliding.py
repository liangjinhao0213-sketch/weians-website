# -*- coding: utf-8 -*-
"""Scrape the Weinas sliding-door category from the existing site.

Grabs every product on /supplier-4782834-aluminium-sliding-doors, then each
detail page: title, specs (p_name/p_attribute), description, images.
Writes _source/source_products.json and downloads images to assets/img/products-src/.
"""
import html
import io
import json
import os
import re
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.aluminium-windowsdoors.com"
LIST = BASE + "/supplier-4782834-aluminium-sliding-doors"
IMG_DIR = os.path.join(ROOT, "assets", "img", "products-src")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124 Safari/537.36"}


def get(url, binary=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=45) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", "ignore")


def text(s):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", s)).split())


def slugify(s):
    out = []
    for ch in s.lower():
        if ch.isalnum():
            out.append(ch)
        elif ch in " -/&+,.":
            out.append("-")
    t = "".join(out)
    while "--" in t:
        t = t.replace("--", "-")
    return t.strip("-")[:70]


def main():
    page = get(LIST)
    links = re.findall(r'href="(/sale-\d+-[^"]+\.html)"[^>]*>([^<]{0,200})', page)
    seen, items = set(), []
    for href, title in links:
        if href in seen:
            continue
        t = text(title)
        if len(t) < 12:
            continue
        seen.add(href)
        items.append({"url": BASE + href, "title": t})

    print("products:", len(items))
    os.makedirs(IMG_DIR, exist_ok=True)

    out = []
    for i, it in enumerate(items, 1):
        try:
            d = get(it["url"])
        except Exception as exc:  # noqa: BLE001
            print("  !", it["url"], exc)
            continue

        # spec table
        specs = []
        for label, value in re.findall(
                r'<td class="p_name">\s*([^<]+?)\s*</td>\s*<td class="p_attribute">\s*(.*?)\s*</td>', d, re.S):
            specs.append([text(label).rstrip(":"), text(value)])

        # description: the longest run of <p> inside the detail area
        paras = [text(p) for p in re.findall(r"<p[^>]*>(.*?)</p>", d, re.S)]
        paras = [p for p in paras if len(p) > 60 and "aluminium-windowsdoors" not in p]
        paras.sort(key=len, reverse=True)

        # images
        imgs = re.findall(r'(https://img\.aluminium-windowsdoors\.com/photo/p[scd]\d+-[^"\'\s>]+\.(?:jpg|jpeg|png|webp))', d)
        imgs += re.findall(r'(?:src|data-src)="(//img\.aluminium-windowsdoors\.com[^"]+\.(?:jpg|jpeg|png|webp))"', d)
        clean, seen_img = [], set()
        for src in imgs:
            if "logo" in src.lower() or "icon" in src.lower():
                continue
            if src.startswith("//"):
                src = "https:" + src
            if src in seen_img:
                continue
            seen_img.add(src)
            clean.append(src)

        rec = dict(
            title=it["title"],
            slug=slugify(it["title"]),
            url=it["url"],
            specs=specs[:12],
            intro=(paras[0][:900] if paras else ""),
            body=[p[:900] for p in paras[1:4]],
            images=clean[:4],
        )
        out.append(rec)
        print("  [%2d] %s | specs=%d imgs=%d" % (i, rec["title"][:70], len(rec["specs"]), len(rec["images"])))

    io.open(os.path.join(ROOT, "_source", "source_products.json"), "w", encoding="utf-8").write(
        json.dumps(out, ensure_ascii=False, indent=2))
    print("wrote source_products.json with", len(out), "products")

    # download the first image of each product
    for rec in out:
        if not rec["images"]:
            continue
        src = rec["images"][0]
        ext = os.path.splitext(src.split("?")[0])[1] or ".jpg"
        dst = os.path.join(IMG_DIR, rec["slug"] + ext)
        if os.path.exists(dst):
            continue
        try:
            data = get(src, binary=True)
            io.open(dst, "wb").write(data)
            rec["local_image"] = "products-src/" + rec["slug"] + ext
        except Exception as exc:  # noqa: BLE001
            print("  ! image", src, exc)

    io.open(os.path.join(ROOT, "_source", "source_products.json"), "w", encoding="utf-8").write(
        json.dumps(out, ensure_ascii=False, indent=2))
    print("images:", len([r for r in out if r.get("local_image")]))


if __name__ == "__main__":
    main()
