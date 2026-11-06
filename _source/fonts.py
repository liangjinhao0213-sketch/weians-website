import os, re, urllib.request

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
FONT_DIR = os.path.join(ROOT, "assets", "fonts")
os.makedirs(FONT_DIR, exist_ok=True)

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

URLS = [
    "https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300..700&display=swap",
    "https://fonts.googleapis.com/css2?family=Inter:wght@300..700&display=swap",
]


def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    data = urllib.request.urlopen(req, timeout=45).read()
    return data if binary else data.decode("utf-8")


css = None
for u in URLS:
    try:
        css = get(u)
        print("css ok:", u, len(css))
        break
    except Exception as e:
        print("css fail:", u, e)

blocks = re.findall(r"/\*\s*([\w\-\[\] ]+?)\s*\*/\s*@font-face\s*\{(.*?)\}", css, re.S)
print("subsets:", [b[0] for b in blocks])

out_css = ["/* Inter (self-hosted variable) - latin subsets */"]
kept = 0
for subset, body in blocks:
    if not any(k in subset for k in ("latin", "cyrillic", "greek", "vietnamese")):
        continue
    if any(k in subset for k in ("cyrillic", "greek", "vietnamese")):
        continue  # keep latin + latin-ext only
    m_url = re.search(r"url\((https://[^)]+\.woff2)\)", body)
    if not m_url:
        continue
    remote = m_url.group(1)
    name = "inter-%s-%s.woff2" % (subset.replace(" ", ""), remote.split("/")[-1][:10])
    dest = os.path.join(FONT_DIR, name)
    if not os.path.exists(dest):
        open(dest, "wb").write(get(remote, binary=True))
    local = body.replace(remote, "../fonts/" + name)
    # normalise: drop format hint issues, keep as-is
    out_css.append("@font-face {%s}" % local.strip())
    kept += 1
    print("font:", name, os.path.getsize(dest))

open(os.path.join(ROOT, "assets", "css", "fonts.css"), "w", encoding="utf-8").write("\n".join(out_css) + "\n")
print("kept", kept)
