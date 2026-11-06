"""Technical elevation drawings for the 12 product systems + one profile
cross-section. Hairline architectural style, normalised bounding boxes.
Output: assets/img/products/*.svg"""
import math
import os

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
OUT = os.path.join(ROOT, "assets", "img", "products")
os.makedirs(OUT, exist_ok=True)

INK = "#2B2F33"
GLASS = "#E7EDF1"
GLASS_EDGE = "#C3CAD0"
REBATE = "#AEB5BB"
HINT = "#8A9198"
BRONZE = "#9C7B52"
GROUND = "#DCE0E4"

W, H = 800, 600
GY = 524
LB, RB = 140, 660          # standard object bounds
BOT = 500                  # standard base line


def head():
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" '
            'role="img" focusable="false">')


def glass(x, y, w, h):
    return ('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s" stroke="%s" '
            'stroke-width="1"/>' % (x, y, w, h, GLASS, GLASS_EDGE))


def frame(x, y, w, h, t=8):
    return ('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="none" stroke="%s" stroke-width="3.4"/>'
            '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="none" stroke="%s" stroke-width="1"/>'
            % (x, y, w, h, INK, x + t, y + t, w - 2 * t, h - 2 * t, REBATE))


def leaf(x, y, w, h, t=6):
    return ('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="none" stroke="%s" stroke-width="2.6"/>'
            '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="none" stroke="%s" stroke-width="0.9"/>'
            % (x, y, w, h, INK, x + t, y + t, w - 2 * t, h - 2 * t, REBATE))


def solid(x, y, w, h, fill=INK):
    return '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s"/>' % (x, y, w, h, fill)


def handle(x, y, h=56, horizontal=False, w=4):
    if horizontal:
        return '<rect x="%.2f" y="%.2f" width="%d" height="%.1f" rx="%.1f" fill="%s"/>' % (
            x, y, h, w, w / 2, HINT)
    return '<rect x="%.2f" y="%.2f" width="%.1f" height="%d" rx="%.1f" fill="%s"/>' % (
        x, y, w, h, w / 2, HINT)


def base(x1=LB - 26, x2=RB + 26):
    return '<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1"/>' % (x1, GY, x2, GY, GROUND)


def dim(x1, x2, y):
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#BFC5CB" stroke-width="0.9"/>'
            '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#BFC5CB" stroke-width="0.9"/>'
            '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#BFC5CB" stroke-width="0.9"/>'
            % (x1, y, x2, y, x1, y - 6, x1, y + 6, x2, y - 6, x2, y + 6))


def dash(x1, y1, x2, y2, color="#9FA6AD"):
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="0.9" '
            'stroke-dasharray="5 6"/>' % (x1, y1, x2, y2, color))


def arc(cx, cy, r, a1, a2, color="#9FA6AD"):
    p1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
    p2 = (cx + r * math.cos(math.radians(a2)), cy + r * math.sin(math.radians(a2)))
    large = 1 if abs(a2 - a1) > 180 else 0
    sweep = 1 if a2 > a1 else 0
    return ('<path d="M%.1f,%.1f A%.1f,%.1f 0 %d %d %.1f,%.1f" fill="none" stroke="%s" '
            'stroke-width="0.9" stroke-dasharray="5 6"/>'
            % (p1[0], p1[1], r, r, large, sweep, p2[0], p2[1], color))


def svg(body, vb):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" role="img" focusable="false">'
            % vb) + body + "</svg>\n"


# 01 sliding door -------------------------------------------------------------
def sliding_door():
    x, y, w, h = LB, 56, RB - LB, 444
    mid = x + w / 2
    b = [base(), glass(x, y, w, h), frame(x, y, w, h, 8)]
    b.append(solid(mid - 5, y, 10, h))                       # meeting stiles
    b.append(leaf(mid + 5, y + 8, w / 2 - 13, h - 16, 6))     # sliding leaf, proud
    b.append(glass(mid + 11, y + 14, w / 2 - 25, h - 28))
    b.append(handle(mid - 17, y + h / 2 - 32, 64))
    b.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="0.9"/>'
             % (mid + 5, y + 4, mid + 5, y + h - 4, REBATE))  # panel edge
    return svg("".join(b), "120 20 560 520")


# 02 casement window ----------------------------------------------------------
def casement_window():
    x, y, w, h = LB, 198, RB - LB, 250
    mid = x + w / 2
    b = [base(), glass(x, y, w, h), frame(x, y, w, h, 8)]
    b.append(solid(mid - 4, y, 8, h))
    for sx, sw in ((x + 8, w / 2 - 12), (mid + 4, w / 2 - 12)):
        b.append(leaf(sx, y + 8, sw, h - 16, 5))
        b.append(glass(sx + 5, y + 13, sw - 10, h - 26))
    b.append(handle(mid - 18, y + h / 2 - 26, 52))
    b.append(handle(mid + 12, y + h / 2 - 26, 52))
    b.append(dim(x, x + w, 470))
    return svg("".join(b), "120 158 560 400")


# 03 sliding window -----------------------------------------------------------
def sliding_window():
    x, y, w, h = LB, 258, RB - LB, 168
    mid = x + w / 2
    b = [base(), glass(x, y, w, h), frame(x, y, w, h, 8)]
    b.append(dash(mid, y + 6, mid, y + h - 6))
    b.append(leaf(mid - 3, y + 8, w / 2 - 6, h - 16, 5))
    b.append(glass(mid + 2, y + 14, w / 2 - 16, h - 28))
    b.append(handle(mid - 18, y + h / 2 - 24, 48))
    return svg("".join(b), "120 218 560 330")


# 04 interior sliding partition ----------------------------------------------
def partition():
    x, y, w, h = 160, 56, 480, 444
    b = [base(x - 30, x + w + 30), glass(x, y, w, h)]
    b.append(solid(x - 30, y - 20, w + 60, 12))               # head track
    b.append(solid(x - 30, y + h - 2, w + 60, 7))              # floor track
    b.append(leaf(x, y, 290, h, 6))
    b.append(glass(x + 6, y + 6, 278, h - 12))
    b.append(leaf(x + 250, y + 8, 290, h - 8, 6))              # panel slid open
    b.append(glass(x + 256, y + 14, 278, h - 20))
    b.append(handle(x + 232, y + 180, 78))
    b.append(dash(x + 546, y + 4, x + 546, y + h - 4))
    return svg("".join(b), "110 26 580 512")


# 05 casement door + fixed light ---------------------------------------------
def casement_door():
    x, y, w, h = LB, 56, RB - LB, 444
    dw = 300
    b = [base(), glass(x, y, w, h), frame(x, y, w, h, 8)]
    b.append(leaf(x + 8, y + 8, dw, h - 16, 6))
    b.append(glass(x + 14, y + 14, dw - 12, 250))
    b.append(solid(x + 14, y + 272, dw - 12, 6))               # mid rail
    b.append(glass(x + 14, y + 286, dw - 12, h - 36 - 272 - 14 + y - y))
    b.append(handle(x + dw - 14, y + 240, 76))
    b.append(solid(x + 8 + dw, y + 8, 7, h - 16))
    fx = x + 15 + dw
    b.append(glass(fx, y + 14, x + w - 16 - fx, h - 28))
    return svg("".join(b), "120 20 560 520")


# 06 tilt and turn window -----------------------------------------------------
def tilt_turn():
    x, y, w, h = 206, 168, 388, 300
    b = [base(), glass(x, y, w, h), frame(x, y, w, h, 8)]
    b.append(leaf(x + 8, y + 8, w - 16, h - 16, 5))
    b.append(glass(x + 13, y + 13, w - 26, h - 26))
    b.append(handle(x + w / 2 - 24, y + h - 42, 48, horizontal=True, w=4))
    b.append(arc(x + 12, y + 12, 72, 4, 80))
    b.append(base(x - 40, x + w + 40))
    return svg("".join(b), "178 148 444 414")


# 07 thermal insulation window ------------------------------------------------
def thermal_window():
    x, y, w, h = 160, 198, 480, 250
    mid = x + w / 2
    b = [base(), glass(x, y, w, h), frame(x, y, w, h, 11)]
    b.append(solid(mid - 5, y, 10, h))
    # deeper profile reads as thermally broken: bronze marker on each jamb
    b.append('<rect x="%.1f" y="%.1f" width="11" height="%.1f" fill="%s"/>'
             % (x, y + h / 2 - 44, 88, BRONZE))
    b.append('<rect x="%.1f" y="%.1f" width="11" height="%.1f" fill="%s"/>'
             % (x + w - 11, y + h / 2 - 44, 88, BRONZE))
    b.append(handle(mid + 20, y + h / 2 - 26, 52))
    return svg("".join(b), "138 158 524 400")


# 08 swing door ---------------------------------------------------------------
def swing_door():
    x, y, w, h = 266, 56, 268, 444
    b = [base(), glass(x, y, w, h), frame(x, y, w, h, 8)]
    b.append(leaf(x + 8, y + 8, w - 16, h - 16, 7))
    b.append(glass(x + 15, y + 15, w - 30, 246))
    b.append(solid(x + 15, y + 268, w - 30, 6))
    b.append(glass(x + 15, y + 282, w - 30, h - 34 - 266))
    b.append(handle(x + w - 68, y + 214, 66, horizontal=True, w=4.4))
    b.append('<circle cx="%.1f" cy="%.1f" r="3" fill="%s"/>' % (x + 16, y + h - 16, INK))
    b.append(arc(x + 16, y + h - 16, 108, 246, 300))
    return svg("".join(b), "246 20 308 520")


# 09 bathroom door ------------------------------------------------------------
def bathroom_door():
    x, y, w, h = 312, 56, 176, 444
    b = [base(x - 30, x + w + 30), frame(x, y, w, h, 8)]
    b.append('<defs><pattern id="frost" width="8" height="8" patternUnits="userSpaceOnUse">'
             '<circle cx="2.2" cy="2.2" r="0.9" fill="#C0C7CD"/></pattern></defs>')
    b.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#F4F6F8" stroke="%s" stroke-width="1"/>'
             % (x + 8, y + 8, w - 16, h - 16, GLASS_EDGE))
    b.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="url(#frost)" opacity="0.65"/>'
             % (x + 8, y + 8, w - 16, h - 16))
    b.append(leaf(x + 8, y + 8, w - 16, h - 16, 6))
    b.append(solid(x + 7, y + h * 0.78, w - 14, 6))
    b.append(handle(x + w - 34, y + h * 0.5, 42))
    return svg("".join(b), "290 20 220 520")


# 10 front door ---------------------------------------------------------------
def front_door():
    x, y, w, h = 300, 56, 200, 444
    b = [base(x - 30, x + w + 30), frame(x, y, w, h, 9)]
    b.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#F4F6F7" stroke="%s" stroke-width="1"/>'
             % (x + 9, y + 9, w - 18, h - 18, GLASS_EDGE))
    b.append(leaf(x + 9, y + 9, w - 18, h - 18, 3))
    # two horizontal rails only: planked security leaf, no tic-tac-toe
    b.append(solid(x + 9, y + 128, w - 18, 4))
    b.append(solid(x + 9, y + 300, w - 18, 4))
    b.append('<rect x="%.1f" y="%.1f" width="7" height="146" rx="3.5" fill="#C7CCD2"/>'
             % (x + w - 40, y + 168))
    b.append('<circle cx="%.1f" cy="%.1f" r="4" fill="none" stroke="%s" stroke-width="1.4"/>'
             % (x + w / 2, y + 64, HINT))
    return svg("".join(b), "278 20 244 520")


# 11 pivot door ---------------------------------------------------------------
def pivot_door():
    x, y, w, h = 296, 56, 208, 444
    b = [base(x - 30, x + w + 30), glass(x, y, w, h), frame(x, y, w, h, 8)]
    b.append(leaf(x + 8, y + 8, w - 16, h - 16, 8))
    b.append(glass(x + 16, y + 16, w - 32, h - 58))
    b.append(solid(x + 16, y + h - 50, w - 32, 6))
    px = x + 54
    b.append(dash(px, y - 16, px, y + h + 16, "#0B2B5B"))
    for py in (y - 16, y + h + 16):
        b.append('<circle cx="%.1f" cy="%.1f" r="3.4" fill="#0B2B5B"/>' % (px, py))
    b.append(arc(px, y - 16, 120, 12, 78, "#0B2B5B"))
    b.append(handle(x + w - 34, y + h / 2 - 30, 60))
    return svg("".join(b), "274 8 252 552")


# 12 folding door -------------------------------------------------------------
def folding_door():
    x, y, w, h = LB, 56, RB - LB, 444
    n = 5
    panel = (w - 16) / n
    b = [base(), glass(x, y, w, h), frame(x, y, w, h, 8)]
    for i in range(n):
        px = x + 8 + i * panel
        b.append(leaf(px + 1, y + 8, panel - 2, h - 16, 5))
        b.append(glass(px + 6, y + 13, panel - 12, h - 26))
        if i < n - 1:
            b.append('<circle cx="%.1f" cy="%.1f" r="2.6" fill="%s"/>'
                     % (px + panel, y + h / 2, HINT))
    b.append(dim(x + 8, x + w - 8, 476))
    return svg("".join(b), "120 20 560 520")


# profile cross-section -------------------------------------------------------
def cross_section():
    b = ['<defs>',
         '<pattern id="alu" width="9" height="9" patternUnits="userSpaceOnUse" '
         'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="9" '
         'stroke="#2B2F33" stroke-width="1" opacity="0.5"/></pattern>',
         '<pattern id="pola" width="8" height="8" patternUnits="userSpaceOnUse" '
         'patternTransform="rotate(-45)"><line x1="0" y1="0" x2="0" y2="8" '
         'stroke="#9C7B52" stroke-width="1.3" opacity="0.85"/></pattern>',
         '<marker id="ar" viewBox="0 0 8 8" refX="4" refY="4" markerWidth="7" markerHeight="7" '
         'orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#6E757C"/></marker>',
         '</defs>']

    b.append('<line x1="50" y1="504" x2="750" y2="504" stroke="%s" stroke-width="1"/>' % GROUND)

    # head profile
    b.append('<rect x="80" y="92" width="500" height="104" fill="url(#alu)" stroke="%s" stroke-width="1.6"/>' % INK)
    b.append('<rect x="80" y="92" width="500" height="104" fill="#FFFFFF" opacity="0.62"/>')
    b.append('<rect x="80" y="92" width="500" height="104" fill="none" stroke="%s" stroke-width="1.6"/>' % INK)
    b.append('<rect x="80" y="150" width="500" height="28" fill="url(#pola)" stroke="%s" stroke-width="1.1"/>' % BRONZE)

    # sash profile
    b.append('<rect x="404" y="196" width="104" height="180" fill="url(#alu)" stroke="%s" stroke-width="1.6"/>' % INK)
    b.append('<rect x="404" y="196" width="104" height="180" fill="#FFFFFF" opacity="0.62"/>')
    b.append('<rect x="404" y="196" width="104" height="180" fill="none" stroke="%s" stroke-width="1.6"/>' % INK)
    b.append('<rect x="458" y="196" width="50" height="180" fill="#FFFFFF"/>')
    b.append('<rect x="458" y="196" width="50" height="180" fill="none" stroke="%s" stroke-width="1.1"/>' % INK)

    # IGU
    b.append('<rect x="272" y="196" width="16" height="250" fill="#EEF3F5" stroke="#6E757C" stroke-width="1.4"/>')
    b.append('<rect x="308" y="196" width="16" height="250" fill="#EEF3F5" stroke="#6E757C" stroke-width="1.4"/>')
    b.append('<rect x="288" y="196" width="20" height="250" fill="#FFFFFF" opacity="0.9"/>')
    for gx in (288, 308):
        b.append('<line x1="%.1f" y1="196" x2="%.1f" y2="446" stroke="#B3BAC1" stroke-width="0.8" '
                 'stroke-dasharray="3 4"/>' % (gx, gx))

    # gaskets
    for gx, gy in ((252, 196), (252, 418), (336, 196), (336, 418)):
        b.append('<rect x="%.1f" y="%.1f" width="20" height="30" fill="%s"/>' % (gx, gy, INK))

    # sill
    b.append('<rect x="80" y="446" width="500" height="13" fill="%s" opacity="0.9"/>' % INK)

    # sightline dimension
    b.append('<line x1="80" y1="480" x2="252" y2="480" stroke="#6E757C" stroke-width="1" '
             'marker-start="url(#ar)" marker-end="url(#ar)"/>')
    for xx in (80, 252):
        b.append('<line x1="%.1f" y1="466" x2="%.1f" y2="494" stroke="#6E757C" stroke-width="1"/>' % (xx, xx))
    b.append('<text x="166" y="462" font-family="Helvetica,Arial,sans-serif" font-size="17" '
             'fill="%s" text-anchor="middle" letter-spacing="1.4">22 MM</text>' % INK)

    labels = [
        (330, 120, 616, 96, "AL 6063-T6"),
        (330, 164, 616, 168, "POLYAMIDE 34"),
        (288, 320, 616, 300, "IGU 48 MM"),
        (456, 340, 616, 400, "SASH 22 MM"),
    ]
    for lx, ly, tx, ty, text in labels:
        b.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#B3BAC1" stroke-width="1"/>'
                 % (lx, ly, tx + (8 if tx > lx else -8), ty))
        b.append('<circle cx="%.1f" cy="%.1f" r="2.8" fill="#6E757C"/>' % (lx, ly))
        b.append('<text x="%.1f" y="%.1f" font-family="Helvetica,Arial,sans-serif" font-size="20" '
                 'fill="#4E555B" text-anchor="%s" letter-spacing="1.2">%s</text>'
                 % (tx, ty + 4, "start" if tx > lx else "end", text))
    return svg("".join(b), "40 56 730 500")


FILES = {
    "aluminium-sliding-doors": sliding_door,
    "aluminium-casement-windows": casement_window,
    "aluminium-sliding-windows": sliding_window,
    "interior-sliding-partition-doors": partition,
    "aluminium-casement-doors": casement_door,
    "aluminium-tilt-and-turn-windows": tilt_turn,
    "thermal-insulation-windows": thermal_window,
    "aluminium-swing-doors": swing_door,
    "aluminium-bathroom-doors": bathroom_door,
    "aluminium-front-doors": front_door,
    "aluminium-pivot-doors": pivot_door,
    "aluminium-folding-doors": folding_door,
}

if __name__ == "__main__":
    for name, fn in FILES.items():
        open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8").write(fn())
    open(os.path.join(ROOT, "assets", "img", "ws90-section.svg"), "w", encoding="utf-8").write(cross_section())
    print("generated", len(FILES) + 1, "svgs")

