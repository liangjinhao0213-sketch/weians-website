# -*- coding: utf-8 -*-
"""Build dark-background (reversed) variants of the Weinas logo and compare them."""
import os
import numpy as np
from PIL import Image

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
IMG = os.path.join(ROOT, "assets", "img")
OUT = os.path.join(ROOT, "_source", "logo-variants")
os.makedirs(OUT, exist_ok=True)

src = Image.open(os.path.join(IMG, "logo.png")).convert("RGBA")
a = np.asarray(src).astype(np.float32)
rgb, alpha = a[..., :3], a[..., 3]

lum = rgb[..., 0] * 0.2126 + rgb[..., 1] * 0.7152 + rgb[..., 2] * 0.0722
is_blue = (rgb[..., 2] - rgb[..., 0] > 18) & (alpha > 6)

# normalise the blue pixels' own shading range
bl = lum[is_blue]
lo, hi = np.percentile(bl, 4), np.percentile(bl, 96)
shade = np.clip((lum - lo) / max(hi - lo, 1), 0, 1)          # 0..1 inside the blue
shade = np.where(alpha > 0, shade, 0)


def recolor(base_low, base_high, grey_gain=1.0, grey_tint=None):
    """Map blue strokes onto a light ramp, optionally lift the grey letters."""
    low = np.array(base_low, dtype=np.float32)
    high = np.array(base_high, dtype=np.float32)
    ramp = low + (high - low) * shade[..., None]              # per-pixel light ramp

    out = rgb.copy()
    out[is_blue] = ramp[is_blue]

    if grey_gain != 1.0:
        grey = ~is_blue
        lifted = np.clip(out * grey_gain, 0, 255)
        out[grey] = lifted[grey]
    if grey_tint is not None:
        tint = np.array(grey_tint, dtype=np.float32)
        grey = ~is_blue
        out[grey] = out[grey] * 0.72 + tint * 0.28

    rgba = np.dstack([np.clip(out, 0, 255), alpha]).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")


VARIANTS = {
    # A: 蓝 → 冰白（最接近“官方反白版”的感觉）
    "A-ice-white.png": recolor((150, 176, 205), (255, 255, 255), grey_gain=1.10),
    # B: 蓝 → 铝银（与站点银灰 #C7CCD2 呼应）
    "B-aluminium.png": recolor((132, 150, 170), (226, 232, 238), grey_gain=1.06),
    # C: 全白（纯剪影 + 保留明暗）
    "C-all-white.png": recolor((118, 118, 118), (255, 255, 255), grey_gain=1.0),
}

for name, im in VARIANTS.items():
    im.save(os.path.join(OUT, name))
    print("variant", name, im.size)

# comparison strip on the footer navy
NAVY = (11, 43, 91, 255)
W, H = 1120, 300
sheet = Image.new("RGBA", (W, H), NAVY)
x = 40
for name in ("A-ice-white.png", "B-aluminium.png", "C-all-white.png"):
    im = Image.open(os.path.join(OUT, name))
    scale = 230 / im.width
    im = im.resize((230, int(im.height * scale)), Image.LANCZOS)
    sheet.alpha_composite(im, (x, (H - im.height) // 2))
    x += 360
sheet.convert("RGB").save(os.path.join(OUT, "compare-on-navy.jpg"), "JPEG", quality=92)
print("compare written")
