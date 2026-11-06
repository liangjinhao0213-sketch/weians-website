# -*- coding: utf-8 -*-
"""Crawl every page of the Weinas sliding-door category, then each product.

Source pattern:
  p1  /supplier-4782834-aluminium-sliding-doors
  p2  /supplier-4782834p2-aluminium-sliding-doors
  p3  /supplier-4782834p3-aluminium-sliding-doors
  ...
Stops when a page yields no new product links.
"""
import html
import io
import json
import os
import re
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.aluminium-windowsdoors.com"
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


def list_url(page):
    if page == 1:
        return BASE + "/supplier-4782834-aluminium-sliding-doors"
    return BASE + "/supplier-4782834p%d-aluminium-sliding-doors" % page


def crawl_links():
    seen, items = set(), []
    page = 1
    while page <= 30:
        try:
            body = get(list_url(page))
        except Exception as exc:  # noqa: BLE001
            print("page %d failed: %s" % (page, exc))
            break
        links = re.findall(r'href="(/sale-\d+-[^"]+\.html)"[^>]*>([^<]{0,200})', body)
        added = 0
        for href, title in links:
            t = text(title)
            if len(t) < 12 or href in seen:
                continue
            seen.add(href)
            items.append({"url": BASE + href, "title": t})
            added += 1
        print("  page %d: +%d (total %d)" % (page, added, len(items)))
        if added == 0:
            break
        page += 1
        time.sleep(0.4)
    return items


def main():
    items = crawl_links()
    print("products found:", len(items))
    os.makedirs(IMG_DIR, exist_ok=True)

    out, seen_slug = [], set()
    for i, it in enumerate(items, 1):
        try:
            d = get(it["url"])
        except Exception as exc:  # noqa: BLE001
            print("  ! detail", it["url"], exc)
            continue

        specs = []
        for label, value in re.findall(
                r'<td class="p_name">\s*([^<]+?)\s*</td>\s*<td class="p_attribute">\s*(.*?)\s*</td>', d, re.S):
            specs.append([text(label).rstrip(":"), text(value)])

        paras = [text(p) for p in re.findall(r"<p[^>]*>(.*?)</p>", d, re.S)]
        paras = [p for p in paras if len(p) > 60 and "aluminium-windowsdoors" not in p]
        paras.sort(key=len, reverse=True)

        imgs = re.findall(r'(https://img\.aluminium-windowsdoors\.com/photo/p[scd]\d+-[^"\s>]+\.(?:jpg|jpeg|png|webp))', d)
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

        slug = slugify(it["title"])
        while slug in seen_slug:
            slug += "-2"
        seen_slug.add(slug)

        rec = dict(
            title=it["title"],
            slug=slug,
            url=it["url"],
            specs=specs[:12],
            intro=(paras[0][:900] if paras else ""),
            body=[p[:900] for p in paras[1:4]],
            images=clean[:4],
        )

        if clean:
            src = clean[0]
            ext = os.path.splitext(src.split("?")[0])[1] or ".jpg"
            rel = "products-src/" + slug + ext
            dst = os.path.join(ROOT, "assets", "img", rel)
            if not os.path.exists(dst):
                try:
                    io.open(dst, "wb").write(get(src, binary=True))
                except Exception as exc:  # noqa: BLE001
                    print("  ! image", exc)
                    rel = None
            rec["local_image"] = rel

        out.append(rec)
        print("  [%2d/%d] %s" % (i, len(items), rec["title"][:66]))

    io.open(os.path.join(ROOT, "_source", "source_products.json"), "w", encoding="utf-8").write(
        json.dumps(out, ensure_ascii=False, indent=2))
    print("wrote", len(out), "products;", len([r for r in out if r.get("local_image")]), "images")


if __name__ == "__main__":
    main()
