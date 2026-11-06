# -*- coding: utf-8 -*-
"""Export the six journal posts for the WordPress importer."""
import html
import io
import json
import os

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace"
SITE = os.path.join(ROOT, "weinas-site")
THEME = os.path.join(ROOT, "weinas-wp", "wp-content", "themes", "weinas")


def esc(t):
    return html.escape(t, quote=False)


def main():
    posts = json.load(io.open(os.path.join(SITE, "_source", "posts.json"), encoding="utf-8"))
    out = []
    for p in posts:
        parts = []
        for b in p.get("blocks", []):
            kind = b.get("kind")
            text = b.get("text", "")
            if kind == "h2":
                parts.append("<h2>%s</h2>" % esc(text))
            elif kind == "h3":
                parts.append("<h3>%s</h3>" % esc(text))
            elif kind == "li":
                parts.append("<p>• %s</p>" % esc(text))
            else:
                parts.append("<p>%s</p>" % esc(text))
        out.append(dict(
            slug=p["slug"],
            title=p["title"],
            date=p.get("date_iso") or "",
            excerpt=p.get("excerpt", ""),
            image=p.get("image", ""),
            category=p.get("category", ""),
            content="\n".join(parts),
        ))

    path = os.path.join(THEME, "data", "posts-import.json")
    io.open(path, "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False))
    print("posts:", len(out), "->", path)


if __name__ == "__main__":
    main()
