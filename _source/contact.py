import os
from PIL import Image, ImageDraw, ImageFont

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
src = os.path.join(ROOT, "_source", "thumbs")
files = sorted(f for f in os.listdir(src) if f.endswith(".jpg"))

COLS, CELL_W, CELL_H = 6, 300, 210
rows = (len(files) + COLS - 1) // COLS
sheet = Image.new("RGB", (COLS * CELL_W, rows * CELL_H), "#111")
draw = ImageDraw.Draw(sheet)
try:
    font = ImageFont.truetype("arial.ttf", 22)
except Exception:
    font = ImageFont.load_default()

for i, name in enumerate(files):
    im = Image.open(os.path.join(src, name)).convert("RGB")
    im.thumbnail((CELL_W - 12, CELL_H - 40))
    x = (i % COLS) * CELL_W + (CELL_W - im.width) // 2
    y = (i // COLS) * CELL_H + 30
    sheet.paste(im, (x, y))
    draw.text(((i % COLS) * CELL_W + 8, (i // COLS) * CELL_H + 4), name[:-4], fill="#7FD1FF", font=font)

out = os.path.join(ROOT, "_source", "contact.jpg")
sheet.save(out, quality=82)
print(out, sheet.size)
