# -*- coding: utf-8 -*-
"""Re-parse products whose stored detail record predates the gallery capture."""

import io
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scrape_details as S  # noqa: E402

ROOT = os.path.dirname(HERE)
PATH = os.path.join(ROOT, "_source", "source_details.json")


def main():
    store = json.load(io.open(PATH, encoding="utf-8"))
    todo = [u for u, v in store.items() if not v.get("gallery")]
    print("entries:", len(store), "| missing gallery:", len(todo))
    if not todo:
        return

    products = {}
    for f in sorted(os.listdir(os.path.join(ROOT, "_source"))):
        if f.startswith("source_") and f.endswith(".json") and "detail" not in f:
            for row in json.load(io.open(os.path.join(ROOT, "_source", f), encoding="utf-8")):
                products[row["url"]] = row

    for i, url in enumerate(todo, 1):
        row = products.get(url)
        if not row:
            continue
        try:
            info = S.parse(S.get(url))
        except Exception as exc:  # noqa: BLE001
            print("  ! %-40s %s" % (row["slug"][:38], exc))
            continue
        shots = []
        for k, u in enumerate((info.get("gallery_urls") or [])[:5], 1):
            rel = S.save_image(u, row["slug"], k, "g")
            if rel:
                shots.append(rel)
        old = store[url]
        old["gallery"] = shots
        old.setdefault("gallery_urls", info.get("gallery_urls") or [])
        json.dump(store, io.open(PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("  [%3d/%3d] %-42s shots=%d" % (i, len(todo), row["slug"][:40], len(shots)))
        time.sleep(0.15)
    print("done")


if __name__ == "__main__":
    main()
