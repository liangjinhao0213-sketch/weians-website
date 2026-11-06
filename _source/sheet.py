import os, sys
from PIL import Image, ImageDraw, ImageFont

folder = sys.argv[1]
out_path = sys.argv[2]
files = sorted(f for f in os.listdir(folder) if f.lower().endswith((".jpg", ".jpeg", ".png")))
items = []
for name in files:
    try:
        im = Image.open(os.path.join(folder, name)).convert("RGB")
        im.load()
        items.append((name, im))
    except Exception:
        continue

COLS, CW, CH = int(sys.argv[3]) if len(sys.argv) > 3 else 6, 300, 210
rows = (len(items) + COLS - 1) // COLS
sheet = Image.new("RGB", (COLS * CW, rows * CH), "#111")
d = ImageDraw.Draw(sheet)
try:
    font = ImageFont.truetype("arial.ttf", 22)
except Exception:
    font = ImageFont.load_default()
for i, (name, im) in enumerate(items):
    im.thumbnail((CW - 12, CH - 40))
    x = (i % COLS) * CW + (CW - im.width) // 2
    y = (i // COLS) * CH + 30
    sheet.paste(im, (x, y))
    d.text(((i % COLS) * CW + 8, (i // COLS) * CH + 4), os.path.splitext(name)[0], fill="#7FD1FF", font=font)
sheet.save(out_path, quality=82)
print(out_path, sheet.size, len(items), "images")
