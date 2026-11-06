import os, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
OUT = os.path.join(ROOT, "_source", "thumbs2")
os.makedirs(OUT, exist_ok=True)

CAND = {
"f01":"photo-1581092918056-0c4c3acd3789","f02":"photo-1581093458791-9f3c3900df4b",
"f03":"photo-1565043666747-69f6646db940","f04":"photo-1537462715879-360eeb61a0ad",
"f05":"photo-1581092795360-fd1ca04f0952","f06":"photo-1581093588401-fbb62a02f120",
"f07":"photo-1518709268805-4e9042af2176","f08":"photo-1587293852726-70cdb56c2866",
"f09":"photo-1590959651373-a3db0f38a961","f10":"photo-1611273426858-450d8e3c9fce",
"f11":"photo-1553413077-190dd305871c","f12":"photo-1558618666-fcd25c85cd64",
"a01":"photo-1600607687644-c7171b42498b","a02":"photo-1600573472550-8090b5e0745e",
"a03":"photo-1600566752355-35792bedcfea","a04":"photo-1517646287270-a5a9ca602e5c",
"a05":"photo-1470723710355-95304d8aece4","a06":"photo-1541888946425-d81bb19240f5",
"a07":"photo-1486406146926-c627a92ad1ab","a08":"photo-1494145904049-0dca59b4bbad",
"a09":"photo-1431576901776-e539bd916ba2","a10":"photo-1524230572899-a752b3835840",
"a11":"photo-1487958449943-2429e8be8625","a12":"photo-1615529182904-14819c35db37",
}

def fetch(it):
    k, pid = it
    out = os.path.join(OUT, k + ".jpg")
    if os.path.exists(out) and os.path.getsize(out) > 4000:
        return k, "cached"
    try:
        req = urllib.request.Request("https://images.unsplash.com/%s?w=380&q=70&fm=jpg" % pid,
                                     headers={"User-Agent": "Mozilla/5.0"})
        open(out, "wb").write(urllib.request.urlopen(req, timeout=40).read())
        return k, "ok"
    except Exception as e:
        return k, "FAIL %s" % e

with ThreadPoolExecutor(max_workers=8) as ex:
    res = {k: s for k, s in ex.map(fetch, CAND.items())}
ok = [k for k, s in res.items() if s != "cached" and not s.startswith("FAIL")]
print("available:", len(ok), "of", len(CAND))
for k in CAND:
    if res[k].startswith("FAIL"):
        print("missing", k, CAND[k])

files = sorted(os.listdir(OUT))
files = [f for f in files if f.endswith(".jpg")]
COLS, CW, CH = 6, 300, 210
rows = (len(files) + COLS - 1) // COLS
sheet = Image.new("RGB", (COLS * CW, rows * CH), "#111")
from PIL import ImageDraw, ImageFont
try:
    font = ImageFont.truetype("arial.ttf", 22)
except Exception:
    font = ImageFont.load_default()
d = ImageDraw.Draw(sheet)
for i, name in enumerate(files):
    im = Image.open(os.path.join(OUT, name)).convert("RGB")
    im.thumbnail((CW - 12, CH - 40))
    x = (i % COLS) * CW + (CW - im.width) // 2
    y = (i // COLS) * CH + 30
    sheet.paste(im, (x, y))
    d.text(((i % COLS) * CW + 8, (i // COLS) * CH + 4), name[:-4], fill="#7FD1FF", font=font)
sheet.save(os.path.join(ROOT, "_source", "contact2.jpg"), quality=82)
print("sheet", sheet.size)
