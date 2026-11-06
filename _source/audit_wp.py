# -*- coding: utf-8 -*-
"""WordPress audit: crawl every sitemap URL, check status, PHP notices, images.

Run: python audit_wp.py
"""
import io
import os
import re
import json
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor

HOST = "http://127.0.0.1"
SITE_HOST = "wwweinas"
SITEMAP = "/wp-sitemap.xml"
REPORT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site\_source\_audit-wp.txt"


def get(path, timeout=30):
    req = urllib.request.Request(HOST + path, headers={"Host": SITE_HOST, "User-Agent": "Mozilla/5.0 (audit)"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode("utf-8", "ignore")


def head(path, timeout=25):
    req = urllib.request.Request(HOST + path, headers={"Host": SITE_HOST, "User-Agent": "Mozilla/5.0 (audit)"}, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


def norm(url):
    return url.replace("http://wwweinas", "").replace("https://wwweinas", "")


def main():
    _, idx = get(SITEMAP)
    subs = re.findall(r"<loc>([^<]+)</loc>", idx)

    urls = []
    for s in subs:
        try:
            _, xml = get(norm(s))
            urls.extend(re.findall(r"<loc>([^<]+)</loc>", xml))
        except Exception as e:
            urls.append("__ERR__" + s)

    urls = [u for u in urls if not u.startswith("__ERR__")]
    paths = [norm(u) for u in urls]
    # a few pages that are not in the sitemap
    for extra in ("/videos/", "/contact-us/", "/cases/", "/blog/", "/products/"):
        if extra not in paths:
            paths.append(extra)

    results = []
    images = set()

    def check(p):
        try:
            status, html = get(p)
        except urllib.error.HTTPError as e:
            return {"path": p, "status": e.code, "issues": ["HTTP %d" % e.code]}
        except Exception as e:
            return {"path": p, "status": 0, "issues": [str(e)[:80]]}

        issues = []
        low = html.lower()
        for marker, label in (
            ("fatal error", "PHP fatal"),
            ("warning:", "PHP warning"),
            ("notice:", "PHP notice"),
            ("deprecated:", "PHP deprecated"),
        ):
            if marker in low:
                issues.append(label)

        t = re.search(r"<title>(.*?)</title>", html, re.S)
        if not t or not t.group(1).strip():
            issues.append("no <title>")
        if 'name="description"' not in html:
            issues.append("no meta description")

        for m in re.finditer(r'<img\b[^>]*src="([^"]+)"', html):
            src = m.group(1)
            if "/wp-content/" in src:
                images.add(norm(src))
        return {"path": p, "status": status, "issues": issues, "bytes": len(html)}

    with ThreadPoolExecutor(max_workers=8) as pool:
        for r in pool.map(check, paths):
            results.append(r)

    bad = [r for r in results if r["status"] != 200 or r["issues"]]

    img_bad = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        for src, code in zip(sorted(images), pool.map(head, sorted(images))):
            if code != 200:
                img_bad.append((src, code))

    out = []
    out.append("WORDPRESS AUDIT")
    out.append("crawled urls: %d" % len(results))
    out.append("non-200 or with issues: %d" % len(bad))
    for r in bad[:25]:
        out.append("   %-64s %s %s" % (r["path"][:62], r["status"], ",".join(r["issues"])[:60]))
    out.append("")
    out.append("images checked: %d | missing: %d" % (len(images), len(img_bad)))
    for src, code in img_bad[:15]:
        out.append("   %-70s %s" % (src[:68], code))
    out.append("")
    statuses = {}
    for r in results:
        statuses[r["status"]] = statuses.get(r["status"], 0) + 1
    out.append("status spread: %s" % json.dumps(statuses))
    text = "\n".join(out)
    io.open(REPORT, "w", encoding="utf-8").write(text)
    print(text)


if __name__ == "__main__":
    main()
