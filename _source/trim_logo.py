"""Trim transparent margins from the rendered logo and export site-ready PNGs."""
import os
from PIL import Image

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
SRC = os.path.join(ROOT, "_source")
OUT = os.path.join(ROOT, "assets", "img")


def trim(path, dest, pad=2):
    im = Image.open(path).convert("RGBA")
    bbox = im.getbbox()  # alpha-aware bbox
    if bbox:
        left, top, right, bottom = bbox
        im = im.crop((max(0, left - pad), max(0, top - pad),
                      min(im.width, right + pad), min(im.height, bottom + pad)))
    im.save(dest)
    return im.size


for name, dest in (("logo-raw.png", "logo.png"), ("logo-light-raw.png", "logo-light.png")):
    src = os.path.join(SRC, name)
    if os.path.exists(src):
        print(dest, trim(src, os.path.join(OUT, dest)))
