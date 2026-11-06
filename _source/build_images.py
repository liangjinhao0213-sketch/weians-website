"""Download, grade and crop all site photography into assets/img/."""
import os, urllib.request
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from PIL import Image, ImageEnhance

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
RAW = os.path.join(ROOT, "_source", "raw")
IMG = os.path.join(ROOT, "assets", "img")
os.makedirs(RAW, exist_ok=True)
os.makedirs(IMG, exist_ok=True)

UNSPLASH = {
    "villa-open":      "photo-1613490493576-7fde63acd811",   # white villa, open sliding doors
    "dusk-house":      "photo-1600585153490-76fb20a32601",   # dark clad house at dusk
    "dusk-sliding":    "photo-1600585154340-be6161a56a0c",   # dusk house, dining opening
    "interior-frames": "photo-1600607687920-4e2a09cf159d",   # black slim frames, concrete, oak
    "interior-pool":   "photo-1600573472550-8090b5e0745e",   # steel framed glass to pool
    "white-house":     "photo-1523217582562-09d0def993a6",   # minimal white house
    "office-glass":    "photo-1497366754035-f200968a6e72",   # glass partition corridor
    "office-showroom": "photo-1497366216548-37526070297c",   # showroom / office
    "atrium":          "photo-1487958449943-2429e8be8625",   # glass atrium building
    "facade-grid":     "photo-1486406146926-c627a92ad1ab",   # high-rise facade looking up
    "bathroom":        "photo-1600566752355-35792bedcfea",   # bathroom, glass screen
    "stair-glazing":   "photo-1502005229762-cf1b2da7c5d6",   # stair / interior
    "garden-room":     "photo-1618221195710-dd6b41faaea6",   # warm living room, garden doors
    "workshop":        "photo-1581094794329-c8112a89af12",   # workshop machine
    "welding":         "photo-1504328345606-18bbc8c9d7d1",   # sparks / fabrication
    "warehouse":       "photo-1553413077-190dd305871c",      # warehouse aisle
    "facility-aerial": "photo-1565793298595-6a879b1d9492",   # aerial facility roofs
    "engineering":     "photo-1581092160562-40aa08e78837",   # engineering / drawings
}


def download(name, pid):
    out = os.path.join(RAW, name + ".jpg")
    if os.path.exists(out) and os.path.getsize(out) > 20000:
        return name, "cached"
    url = "https://images.unsplash.com/%s?w=2400&q=85&fm=jpg" % pid
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=90).read()
        if len(data) < 20000:
            return name, "TOO SMALL"
        open(out, "wb").write(data)
        Image.open(out).verify()
        return name, "ok %d" % len(data)
    except Exception as e:
        return name, "FAIL %s" % e


def grade(im, saturation=0.90, contrast=1.03, brightness=1.0, cool=0.012):
    im = im.convert("RGB")
    im = ImageEnhance.Color(im).enhance(saturation)
    im = ImageEnhance.Contrast(im).enhance(contrast)
    if brightness != 1.0:
        im = ImageEnhance.Brightness(im).enhance(brightness)
    if cool:
        a = np.asarray(im).astype(np.int16)
        a[..., 0] = a[..., 0] * (1 - cool)
        a[..., 2] = a[..., 2] * (1 + cool)
        im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return im


def crop_to(im, w, h, fx=0.5, fy=0.5, zoom=1.0):
    """Centre-ish crop to aspect w:h, focus point fx/fy in 0..1."""
    ar = w / h
    sw, sh = im.size
    if sw / sh > ar:
        nw = int(round(sh * ar))
        nh = sh
    else:
        nw = sw
        nh = int(round(sw / ar))
    left = int(round((sw - nw) * fx))
    top = int(round((sh - nh) * fy))
    im = im.crop((left, top, left + nw, top + nh))
    if zoom > 1.0:
        zw, zh = int(round(w / zoom)), int(round(h / zoom))
        im = im.crop(((w - zw) // 2, (h - zh) // 2, (w - zw) // 2 + zw, (h - zh) // 2 + zh))
    return im.resize((w, h), Image.LANCZOS)


def hero_scrim(im):
    """Bake a subtle left-side tonal falloff so white type stays legible."""
    a = np.asarray(im).astype(np.float32)
    h, w, _ = a.shape
    x = np.linspace(0, 1, w, dtype=np.float32)
    # 0.66 at left edge -> 1.0 by 62% width, smoothstep
    t = np.clip(x / 0.62, 0, 1)
    t = t * t * (3 - 2 * t)
    mask = 0.66 + 0.34 * t
    a *= mask[None, :, None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def save(im, name, quality=82):
    path = os.path.join(IMG, name)
    im.save(path, "JPEG", quality=quality, optimize=True, progressive=True)
    return name, os.path.getsize(path)


JOBS = [
    # (out, source, w, h, fx, fy, quality, scrim)
    ("hero-villa-2400.jpg", "dusk-house", 2400, 1180, 0.52, 0.42, 84, True, 1.28),
    ("hero-villa-1600.jpg", "dusk-house", 1600, 787, 0.52, 0.42, 82, True, 1.28),
    ("hero-villa-mobile.jpg", "dusk-house", 1100, 1400, 0.50, 0.45, 82, False, 1.15),
    ("lifestyle-dusk-2400.jpg", "dusk-sliding", 2400, 1180, 0.50, 0.55, 84, False),
    ("lifestyle-dusk-1600.jpg", "dusk-sliding", 1600, 787, 0.50, 0.55, 82, False),
    ("top-pick-frames.jpg", "interior-frames", 1500, 1000, 0.52, 0.50, 82, False),
    ("top-pick-pool.jpg", "interior-pool", 1200, 900, 0.50, 0.50, 82, False),
    ("project-palm-beach.jpg", "villa-open", 1000, 1250, 0.50, 0.42, 82, False),
    ("project-cottesloe.jpg", "white-house", 1000, 1000, 0.50, 0.50, 82, False),
    ("project-dubai.jpg", "atrium", 1400, 900, 0.50, 0.50, 82, False),
    ("project-tokyo.jpg", "office-glass", 1200, 900, 0.50, 0.50, 82, False),
    ("project-byron.jpg", "bathroom", 1000, 1250, 0.50, 0.50, 82, False),
    ("project-australia.jpg", "garden-room", 1400, 900, 0.50, 0.55, 82, False),
    ("factory-workshop.jpg", "engineering", 1100, 820, 0.50, 0.50, 80, False),
    ("factory-welding.jpg", "welding", 1100, 820, 0.50, 0.45, 80, False),
    ("factory-warehouse.jpg", "warehouse", 1100, 820, 0.50, 0.50, 80, False),
    ("factory-facility.jpg", "facility-aerial", 1100, 820, 0.50, 0.50, 80, False),
    ("collection-villa.jpg", "villa-open", 900, 1100, 0.50, 0.55, 80, False),
    ("collection-casement.jpg", "white-house", 900, 1100, 0.42, 0.45, 80, False),
    ("collection-office.jpg", "office-showroom", 900, 1100, 0.50, 0.50, 80, False),
    ("collection-facade.jpg", "facade-grid", 900, 1100, 0.50, 0.50, 80, False),
    ("collection-balcony.jpg", "stair-glazing", 900, 1100, 0.50, 0.45, 80, False),
    ("quote-bg.jpg", "interior-frames", 1200, 900, 0.30, 0.50, 78, False),
]

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=6) as ex:
        for n, s in ex.map(lambda kv: download(*kv), UNSPLASH.items()):
            print("download", n, s)

    for out, src, w, h, fx, fy, q, scrim, *rest in JOBS:
        zoom = rest[0] if rest else 1.0
        path = os.path.join(RAW, src + ".jpg")
        if not os.path.exists(path):
            print("SKIP (missing source)", out)
            continue
        im = Image.open(path)
        im = crop_to(im, w, h, fx, fy, zoom)
        im = grade(im)
        if scrim:
            im = hero_scrim(im)
        print("save", *save(im, out, q))

