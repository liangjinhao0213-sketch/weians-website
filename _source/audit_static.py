# -*- coding: utf-8 -*-
"""Static-site audit: links, assets, anchors, ids, alt text, page inventory."""
import io
import os
import re
import json
import collections
from urllib.parse import unquote

SITE = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
REPORT = os.path.join(SITE, "_source", "_audit-static.txt")

SKIP_DIRS = {"_source", ".git"}


def pages():
    for dp, dn, fs in os.walk(SITE):
        rel_dir = os.path.relpath(dp, SITE)
        if any(part in SKIP_DIRS for part in rel_dir.split(os.sep)):
            continue
        for f in fs:
            if f.endswith(".html"):
                yield os.path.join(dp, f)


def main():
    all_pages = list(pages())
    page_set = set(os.path.normpath(p).lower() for p in all_pages)
    ids_by_page = {}
    links = []          # (page, href, kind)
    missing_assets = collections.Counter()
    bad_anchors = []
    no_alt = collections.Counter()
    dup_ids = []
    empty_href = []
    titles = collections.Counter()
    descs = collections.Counter()

    for p in all_pages:
        html = io.open(p, encoding="utf-8", errors="ignore").read()
        rel = os.path.relpath(p, SITE)

        t = re.search(r"<title>(.*?)</title>", html, re.S)
        if t:
            titles[re.sub(r"\s+", " ", t.group(1)).strip()] += 1
        d = re.search(r'<meta name="description" content="([^"]*)"', html)
        if d:
            descs[d.group(1).strip()] += 1
        else:
            bad_anchors.append((rel, "MISSING meta description"))

        # ids on this page
        ids = set(re.findall(r'\sid="([^"]+)"', html))
        ids_by_page[rel.replace("\\", "/")] = ids
        found = collections.Counter(re.findall(r'\sid="([^"]+)"', html))
        dupes = [k for k, v in found.items() if v > 1]
        if dupes:
            dup_ids.append((rel, dupes[:5]))

        # images without alt
        for m in re.finditer(r"<img\b[^>]*>", html):
            tag = m.group(0)
            if "alt=" not in tag:
                src = re.search(r'src="([^"]*)"', tag)
                no_alt[(src.group(1) if src else "?")[:80]] += 1

        # links and assets
        for m in re.finditer(r'(?:href|src)="([^"]+)"', html):
            raw = m.group(1)
            if not raw or raw.startswith(("mailto:", "tel:", "data:", "javascript:")):
                continue
            if raw == "#":
                empty_href.append(rel)
                continue
            links.append((rel, raw))
        # srcset
        for m in re.finditer(r'(?:srcset|imagesrcset)="([^"]+)"', html):
            for part in m.group(1).split(","):
                url = part.strip().split(" ")[0]
                if url and not url.startswith("data:"):
                    links.append((rel, url))

    # resolve
    dead = []
    for rel, raw in links:
        if raw.startswith("http") or raw.startswith("//"):
            continue
        path, _, frag = raw.partition("#")
        path = path.split("?")[0]
        if not path:
            # same-page anchor
            if frag and frag not in ids_by_page.get(rel.replace("\\", "/"), set()):
                bad_anchors.append((rel, "#" + frag))
            continue
        base = os.path.dirname(os.path.join(SITE, rel))
        target = os.path.normpath(os.path.join(base, unquote(path)))
        if os.path.isdir(target):
            target = os.path.join(target, "index.html")
        if not os.path.exists(target):
            dead.append((rel, raw))
            continue
        if frag and target.lower().endswith(".html"):
            trel = os.path.relpath(target, SITE).replace("\\", "/")
            if frag not in ids_by_page.get(trel, set()):
                bad_anchors.append((rel, raw))

    # report
    dead_links = collections.Counter(raw for _, raw in dead)
    out = []
    out.append("STATIC SITE AUDIT")
    out.append("pages: %d" % len(all_pages))
    out.append("")
    out.append("dead internal links: %d (unique targets %d)" % (len(dead), len(dead_links)))
    for raw, n in dead_links.most_common(15):
        sample = next(r for r, x in dead if x == raw)
        out.append("   %-58s x%-4d from %s" % (raw[:58], n, sample))
    out.append("")
    out.append("broken anchors: %d" % len(bad_anchors))
    for rel, a in bad_anchors[:12]:
        out.append("   %-46s %s" % (rel, a))
    out.append("")
    dupes = [t for t, n in titles.items() if n > 1]
    out.append("duplicate <title>: %d" % len(dupes))
    for t in dupes[:8]:
        out.append("   %-70s x%d" % (t[:70], titles[t]))
    ddupes = [t for t, n in descs.items() if n > 1]
    out.append("duplicate meta description: %d" % len(ddupes))
    for t in ddupes[:8]:
        out.append("   %-70s x%d" % (t[:70], descs[t]))
    out.append("")
    out.append("images without alt: %d" % sum(no_alt.values()))
    for src, n in no_alt.most_common(8):
        out.append("   %-64s x%d" % (src, n))
    out.append("")
    out.append("pages with duplicate ids: %d" % len(dup_ids))
    for rel, ids in dup_ids[:8]:
        out.append("   %-52s %s" % (rel, ids))
    out.append("")
    out.append('empty href="#": %d' % len(empty_href))

    text = "\n".join(out)
    io.open(REPORT, "w", encoding="utf-8").write(text)
    print(text)


if __name__ == "__main__":
    main()
