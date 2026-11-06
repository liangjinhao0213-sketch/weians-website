# -*- coding: utf-8 -*-
"""Scrape the rich detail block of every product page.

Captures, per product:
  * detail[]      - the "Detail Information" label/value pairs (place of origin,
                    certification, material, profile thickness, glass, ...)
  * spec_rows[]   - the "Specifications" table rows inside the description
  * desc_paras[]  - the description paragraphs
  * features[]    - the "Features" bullet list
  * desc_images[] - the diagrams below the copy (structure / thermal system)

Images are downloaded to assets/img/products-detail/ and re-encoded to at most
1000 px wide so 400 products do not blow up the folder.

Resumable: writes source_details.json after every product and skips what it
already has.
"""
import io
import json
import os
import re
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_source")
IMG_DIR = os.path.join(ROOT, "assets", "img", "products-detail")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124 Safari/537.36"}

try:
    from PIL import Image
except Exception:  # noqa: BLE001
    Image = None


def get(url, binary=False, attempts=3):
    last = None
    for i in range(attempts):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            return data if binary else data.decode("utf-8", "ignore")
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(1.2 * (i + 1))
    raise last


def clean(s):
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("&nbsp;", " ").replace("&amp;", "&").replace("&#39;", "'")
    s = s.replace("&quot;", '"').replace("&lt;", "<").replace("&gt;", ">")
    return " ".join(s.split())


def parse(html):
    out = {"detail": [], "spec_rows": [], "desc_paras": [], "features": [], "desc_images": []}

    m = re.search(r'<div class="details_list_wrap">(.*?)</section>', html, re.S)
    if m:
        pairs = re.findall(
            r'<div class="itemTitle">(.*?)</div>\s*<div class="itemValue">(.*?)</div>',
            m.group(1), re.S)
        for raw_label, raw_value in pairs:
            label, value = clean(raw_label).rstrip(":"), clean(raw_value)
            if label and value:
                out["detail"].append([label, value])

    i = html.find('<section id="sention2">')
    if i > 0:
        sec = html[i:html.find("</section>", i)]
        # table rows inside the description
        for tr in re.finditer(r"<tr[^>]*>(.*?)</tr>", sec, re.S):
            cells = [clean(c) for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr.group(1), re.S)]
            cells = [c for c in cells if c]
            if len(cells) == 2:
                out["spec_rows"].append(cells)
        # paragraphs
        for p in re.findall(r"<p[^>]*>(.*?)</p>", sec, re.S):
            t = clean(p)
            if len(t) < 45:
                continue
            if re.fullmatch(r"[A-Za-z ]{0,25}:?", t):
                continue
            out["desc_paras"].append(t[:700])
        # feature bullets
        for li in re.findall(r"<li[^>]*>(.*?)</li>", sec, re.S):
            t = clean(li)
            if 25 < len(t) < 400:
                out["features"].append(t)
        # diagrams
        for m in re.finditer(r'data-original="(//[^"]+)"', sec):
            url = "https:" + m.group(1)
            if url not in out["desc_images"]:
                out["desc_images"].append(url)

    # the product's own photo set: the same numeric id appears as ps / pl / py sizes
    pics = {}
    for m in re.finditer(r'(?:https?:)?//img\.aluminium-windowsdoors\.com/photo/(p[lsty])(\d+)-([^"\s>]+\.(?:jpg|jpeg|png))', html):
        size, pid, tail = m.group(1), m.group(2), m.group(3)
        pics.setdefault(pid, {})[size] = "https://img.aluminium-windowsdoors.com/photo/%s%s-%s" % (size, pid, tail)
    gallery = []
    for pid, by_size in pics.items():
        for size in ("pl", "py", "ps", "pt"):
            if size in by_size:
                gallery.append(by_size[size])
                break
    out["gallery_urls"] = gallery[:6]

    # de-duplicate paragraphs that repeat the title
    seen, paras = set(), []
    for p in out["desc_paras"]:
        key = p.lower()[:60]
        if key in seen:
            continue
        seen.add(key)
        paras.append(p)
    out["desc_paras"] = paras[:4]
    out["features"] = out["features"][:6]
    out["detail"] = out["detail"][:24]
    out["spec_rows"] = out["spec_rows"][:20]
    return out


def save_image(url, slug, idx, prefix="d"):
    os.makedirs(IMG_DIR, exist_ok=True)
    name = "%s-%s%d.jpg" % (slug, prefix, idx)
    dst = os.path.join(IMG_DIR, name)
    if os.path.exists(dst) and os.path.getsize(dst) > 5000:
        return "products-detail/" + name
    try:
        raw = get(url, binary=True)
    except Exception:  # noqa: BLE001
        return None
    if len(raw) < 5000:
        return None
    if Image is not None:
        try:
            import io as _io
            im = Image.open(_io.BytesIO(raw)).convert("RGB")
            if im.width > 1000:
                im = im.resize((1000, round(im.height * 1000 / im.width)), Image.LANCZOS)
            im.save(dst, "JPEG", quality=78, optimize=True, progressive=True)
        except Exception:  # noqa: BLE001
            io.open(dst, "wb").write(raw)
    else:
        io.open(dst, "wb").write(raw)
    return "products-detail/" + name


def main(limit=None):
    out_path = os.path.join(SRC, "source_details.json")
    store = {}
    if os.path.exists(out_path):
        store = json.load(io.open(out_path, encoding="utf-8"))

    products = []
    for f in sorted(os.listdir(SRC)):
        if f.startswith("source_") and f.endswith(".json") and "detail" not in f:
            for row in json.load(io.open(os.path.join(SRC, f), encoding="utf-8")):
                products.append(row)

    todo = [p for p in products if p["url"] not in store]
    print("products: %d | already parsed: %d | to fetch: %d"
          % (len(products), len(store), len(todo)))
    if limit:
        todo = todo[:limit]

    for i, p in enumerate(todo, 1):
        try:
            info = parse(get(p["url"]))
        except Exception as exc:  # noqa: BLE001
            print("  ! %-50s %s" % (p["slug"][:48], exc))
            continue
        files = []
        for k, url in enumerate(info["desc_images"][:4], 1):
            rel = save_image(url, p["slug"], k, "d")
            if rel:
                files.append(rel)
        info["desc_files"] = files

        shots = []
        for k, url in enumerate((info.get("gallery_urls") or [])[:5], 1):
            rel = save_image(url, p["slug"], k, "g")
            if rel:
                shots.append(rel)
        info["gallery"] = shots
        store[p["url"]] = info
        io.open(out_path, "w", encoding="utf-8").write(json.dumps(store, ensure_ascii=False, indent=1))
        print("  [%3d/%3d] %-44s detail=%2d spec=%2d imgs=%d"
              % (i, len(todo), p["slug"][:42], len(info["detail"]), len(info["spec_rows"]), len(files)))

    print("stored:", len(store))


if __name__ == "__main__":
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else None
    main(lim)
