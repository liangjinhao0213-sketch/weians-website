# -*- coding: utf-8 -*-
"""Generic, resumable category crawler.

  python scrape_category.py 4782833 aluminium-sliding-windows source_windows.json

Behaviour:
  * walks p1, p2, ... until a page adds no new product
  * writes the JSON after EVERY product (checkpoint), so a dropped connection
    never loses more than the product in flight
  * re-running skips products already stored, and retries ones without an image
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


def get(url, binary=False, attempts=4):
    """Fetch with retries - the source host drops TLS handshakes under load."""
    last = None
    for i in range(attempts):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            return data if binary else data.decode("utf-8", "ignore")
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(1.5 * (i + 1))
    raise last


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


def list_url(cat_id, slug, page):
    if page == 1:
        return "%s/supplier-%s-%s" % (BASE, cat_id, slug)
    return "%s/supplier-%sp%s-%s" % (BASE, cat_id, page, slug)


def crawl(cat_id, slug):
    seen, items, page = set(), [], 1
    while page <= 40:
        try:
            body = get(list_url(cat_id, slug, page))
        except Exception as exc:  # noqa: BLE001
            print("  page %d failed (%s) - keeping what we have" % (page, exc))
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
        time.sleep(0.3)
    return items


def load(path):
    if os.path.exists(path):
        try:
            return json.load(io.open(path, encoding="utf-8"))
        except Exception:  # noqa: BLE001
            return []
    return []


def save(path, rows):
    tmp = path + ".tmp"
    io.open(tmp, "w", encoding="utf-8").write(json.dumps(rows, ensure_ascii=False, indent=2))
    os.replace(tmp, path)


def main(cat_id, slug, outfile):
    out_path = os.path.join(ROOT, "_source", outfile)
    rows = load(out_path)
    by_url = {r["url"]: r for r in rows}
    have_slug = {r["slug"] for r in rows}

    items = crawl(cat_id, slug)
    have_url = set(by_url)

    def pending():
        return [i for i in items if i["url"] not in have_url or not by_url[i["url"]].get("local_image")]

    todo = pending()
    print("products on site: %d | already stored: %d | to fetch: %d"
          % (len(items), len(have_url), len(todo)))
    os.makedirs(IMG_DIR, exist_ok=True)

    for it in todo:
        try:
            d = get(it["url"])
        except Exception as exc:  # noqa: BLE001
            print("  ! detail failed (%s) - stopping here" % exc)
            break

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

        old = by_url.get(it["url"])
        if old:
            s = old["slug"]
        else:
            s = slugify(it["title"])
            while s in have_slug:
                s += "-2"
            have_slug.add(s)

        rec = dict(title=it["title"], slug=s, url=it["url"], specs=specs[:12],
                   intro=(paras[0][:900] if paras else ""),
                   body=[p[:900] for p in paras[1:4]], images=clean[:4])

        if clean:
            src = clean[0]
            ext = os.path.splitext(src.split("?")[0])[1] or ".jpg"
            rel = "products-src/" + s + ext
            dst = os.path.join(ROOT, "assets", "img", rel)
            if not os.path.exists(dst):
                try:
                    io.open(dst, "wb").write(get(src, binary=True))
                except Exception as exc:  # noqa: BLE001
                    print("  ! image failed (%s)" % exc)
                    rel = None
            rec["local_image"] = rel

        if old:
            old.update(rec)
        else:
            rows.append(rec)
            by_url[it["url"]] = rec
            have_url.add(it["url"])

        save(out_path, rows)          # checkpoint after every product
        time.sleep(0.25)
        print("  [%d] %s" % (len(rows), rec["title"][:62]))

    save(out_path, rows)
    have_img = len([r for r in rows if r.get("local_image")])
    print("stored %d products, %d with image -> %s" % (len(rows), have_img, outfile))
    missing = len(items) - len(rows)
    if missing > 0:
        print("still missing %d (re-run this command later to continue)" % missing)


if __name__ == "__main__":
    cid = sys.argv[1]
    slug = sys.argv[2]
    out = sys.argv[3] if len(sys.argv) > 3 else "source_%s.json" % slug
    main(cid, slug, out)
