# -*- coding: utf-8 -*-
"""Re-download product images that ended up empty (0 bytes) after a failed fetch."""
import io
import json
import os
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_source")
IMG = os.path.join(ROOT, "assets", "img")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124 Safari/537.36"}


def get(url, attempts=5):
    last = None
    for i in range(attempts):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(1.5 * (i + 1))
    raise last


def main():
    fixed = failed = 0
    for f in sorted(os.listdir(SRC)):
        if not (f.startswith("source_") and f.endswith(".json")):
            continue
        path = os.path.join(SRC, f)
        rows = json.load(io.open(path, encoding="utf-8"))
        dirty = False
        for r in rows:
            rel = r.get("local_image")
            if not rel:
                continue
            dst = os.path.join(IMG, rel.replace("/", os.sep))
            if os.path.exists(dst) and os.path.getsize(dst) > 2000:
                continue
            urls = r.get("images") or []
            if not urls:
                failed += 1
                continue
            try:
                data = get(urls[0])
                if len(data) < 2000:
                    raise ValueError("tiny payload")
                io.open(dst, "wb").write(data)
                fixed += 1
                print("  fixed %-60s %d KB" % (os.path.basename(dst)[:58], len(data) // 1024))
            except Exception as exc:  # noqa: BLE001
                failed += 1
                print("  ! %-60s %s" % (os.path.basename(dst)[:58], exc))
        if dirty:
            json.dump(rows, io.open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("images refilled:", fixed, "| still failing:", failed)


if __name__ == "__main__":
    main()
