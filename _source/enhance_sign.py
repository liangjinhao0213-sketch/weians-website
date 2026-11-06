# -*- coding: utf-8 -*-
"""Best-effort enhancement of the (small) factory photo.

No generative upscaling is used: crop -> tone/contrast -> micro-contrast ->
2x Lanczos -> unsharp mask. Compared side by side before picking.
"""
import os

import numpy as np
from PIL import Image, ImageFilter

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
SRC = os.path.join(ROOT, "_source", "factory-sign-source.png")
OUT = os.path.join(ROOT, "_source", "sign-variants")
os.makedirs(OUT, exist_ok=True)


def crop(im):
    w, h = im.size
    # trim the left white wall sliver and the car at the right edge
    return im.crop((16, 0, 646, h))


def tone(im, low=0.02, high=0.985, sat=1.06, clarity=0.28):
    a = np.asarray(im).astype(np.float32) / 255.0
    lo, hi = np.percentile(a, low * 100), np.percentile(a, high * 100)
    a = np.clip((a - lo) / max(hi - lo, 1e-6), 0, 1)
    # local contrast (unsharp in the luminance channel, large radius)
    lum = a.mean(axis=2)
    blur = np.asarray(Image.fromarray((lum * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(9))).astype(np.float32) / 255.0
    a = np.clip(a + (lum - blur)[..., None] * clarity, 0, 1)
    # saturation
    g = a.mean(axis=2, keepdims=True)
    a = np.clip(g + (a - g) * sat, 0, 1)
    return Image.fromarray((a * 255).round().astype(np.uint8))


def upscale(im, factor=2, pre_blur=0.0):
    if pre_blur:
        im = im.filter(ImageFilter.GaussianBlur(pre_blur))
    return im.resize((im.width * factor, im.height * factor), Image.LANCZOS)


def sharpen(im, radius, percent, threshold):
    return im.filter(ImageFilter.UnsharpMask(radius=radius, percent=percent, threshold=threshold))


src = Image.open(SRC).convert("RGB")
base = tone(crop(src))

VARIANTS = {
    "A": sharpen(upscale(base), 1.4, 135, 2),
    "B": sharpen(upscale(base), 2.2, 110, 4),
    "C": sharpen(upscale(base, pre_blur=0.6), 1.8, 150, 3),
    "D": sharpen(sharpen(upscale(base), 2.0, 100, 3), 0.8, 70, 2),
}
for name, im in VARIANTS.items():
    im.save(os.path.join(OUT, "%s.png" % name))

# comparison crop: the sign area at 1:1
box = (150, 60, 620, 300)
tiles = [("original x2 (nearest)", crop(src).resize((crop(src).width * 2, crop(src).height * 2), Image.NEAREST))]
tiles += [(n, v) for n, v in VARIANTS.items()]

cw, ch = 470, 240
sheet = Image.new("RGB", (cw * 2 + 30, (ch + 26) * 3 + 20), "white")
from PIL import ImageDraw, ImageFont
d = ImageDraw.Draw(sheet)
try:
    font = ImageFont.truetype("arialbd.ttf", 14)
except Exception:
    font = ImageFont.load_default()

for idx, (name, im) in enumerate(tiles):
    part = im.crop(box)
    part = part.resize((cw, int(part.height * cw / part.width)), Image.LANCZOS)
    x = 10 + (idx % 2) * (cw + 10)
    y = 10 + (idx // 2) * (ch + 26)
    d.text((x, y), name, fill="#222", font=font)
    sheet.paste(part, (x, y + 18))

sheet.save(os.path.join(OUT, "compare.jpg"), quality=92)
print("variants written:", list(VARIANTS))
print("compare:", os.path.join(OUT, "compare.jpg"))
