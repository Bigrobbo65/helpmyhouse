"""Trevs 205 under-stair cupboards, drawn to scale from the site measurements.

Run:  python make_trevs_205_open.py              ->  trevs-205-open.svg      (doors open)
      python make_trevs_205_open.py --no-doors   ->  trevs-205-no-doors.svg

All geometry is in mm and converted to pixels with one scale factor, so the
drawing is a true elevation (horizontal and vertical scales are equal).
"""
import sys
from pathlib import Path

SHOW_DOORS = "--no-doors" not in sys.argv
OUT_NAME = "trevs-205-open.svg" if SHOW_DOORS else "trevs-205-no-doors.svg"
SUBTITLE = "doors open, shelves shown" if SHOW_DOORS else "doors removed, shelves shown"

# ---- Site measurements (mm) -------------------------------------------------
LENGTH = 3270            # overall length, bottom of stairs to end wall
HEIGHT = 2270            # floor to underside of landing
DEPTH_A = 700            # depth of cupboards
F = 470                  # low space before cupboard 1 (3270 - 2800)
SLOPE_END = 2485         # assumed: where the stair underside meets the landing
SLOPE = HEIGHT / SLOPE_END
BOARD = 18               # MDF thickness (top board under stringer)
STAIR_DEPTH = 330        # vertical depth of stair above its underside (visual only)
N_STEPS = 10

# name, start x, width, shelves
CUPBOARDS = [
    ("Cupboard 1", F, 600, 1),
    ("Cupboard 2", F + 600, 600, 3),
    ("Cupboard 3", F + 1200, 600, 4),
    ("Double doors 4", F + 1800, 1000, 5),
]

# ---- Drawing scale -----------------------------------------------------------
S = 0.28                 # px per mm
OX, OY = 124, 880        # pixel position of floor at the bottom of the stairs
OBL = (0.8 * 0.5, -0.6 * 0.5)  # oblique direction for depth (half scale)


def X(x):
    return OX + x * S


def Y(h):
    return OY - h * S


def P(pts):
    return " ".join(f"{X(x):.1f},{Y(h):.1f}" for x, h in pts)


def underside(x):
    return min(SLOPE * x, HEIGHT)


def inside_top(x):
    """Inside top of the cupboards (under the 18 mm top board)."""
    return max(underside(x) - BOARD, 0)


def x_at(h):
    """x where the inside top reaches height h on the slope."""
    return (h + BOARD) / SLOPE


INK = "#1f1f1f"
DOOR = "#f1eee7"
DOOR_EDGE = "#d9d3c6"
BACK = "#dcd6ca"
SIDE = "#cbc4b5"
SHELF = "#fbf9f4"

W_PX, H_PX = 1366, 1140
out = []
w = out.append


def opening(x0, x1):
    pts = [(x0, 0), (x1, 0), (x1, inside_top(x1))]
    if x0 < SLOPE_END < x1:
        pts.append((SLOPE_END, inside_top(SLOPE_END)))
    pts.append((x0, inside_top(x0)))
    return pts


def door_open(hinge_x, hinge_h, free_h, leaf_w, direction):
    """Door swung open toward the viewer, drawn as a foreshortened panel (mm)."""
    dw = 0.22 * leaf_w * direction
    fx = hinge_x + dw
    e = 0.05 * free_h
    panel = [(hinge_x, 0), (hinge_x, hinge_h), (fx, free_h + e), (fx, -e)]
    w(f'<polygon points="{P(panel)}" fill="{DOOR}" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>')
    t = 18 * direction
    edge = [(fx, free_h + e), (fx + t, free_h + e - 6), (fx + t, -e + 6), (fx, -e)]
    w(f'<polygon points="{P(edge)}" fill="{DOOR_EDGE}" stroke="{INK}" stroke-width="1.2" stroke-linejoin="round"/>')
    hx = hinge_x + dw * 0.8
    hy = free_h / 2
    w(f'<line x1="{X(hx):.1f}" y1="{Y(hy + 100):.1f}" x2="{X(hx):.1f}" y2="{Y(hy - 100):.1f}" '
      f'stroke="{INK}" stroke-width="2.5" stroke-linecap="round" opacity="0.35"/>')


def arrow(x1, y1, x2, y2, both=True):
    s = 'marker-start="url(#ah)" ' if both else ''
    w(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{INK}" stroke-width="1.8" {s}marker-end="url(#ah)"/>')


def label(x, y, t, size=26, weight="bold", fill=INK, anchor="middle", extra=""):
    w(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{t}</text>')


w(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W_PX} {H_PX}" width="{W_PX}" height="{H_PX}" font-family="Arial, Helvetica, sans-serif">')
w(f'<rect width="{W_PX}" height="{H_PX}" fill="#ffffff"/>')
w('<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
  f'<path d="M0,0 L10,5 L0,10" fill="none" stroke="{INK}" stroke-width="1.6"/></marker></defs>')

w(f'<text x="60" y="52" font-size="28" font-weight="bold" fill="{INK}">Off staircase</text>')
w(f'<text x="60" y="86" font-size="20" fill="#555">Trevs 205 — {SUBTITLE}</text>')
w(f'<text x="60" y="114" font-size="16" fill="#888">Drawn to scale from site measurements</text>')

# ---- Stairs ------------------------------------------------------------------
going = SLOPE_END / N_STEPS
rise = going * SLOPE
steps = [(0, STAIR_DEPTH)]
x, h = 0, STAIR_DEPTH
for _ in range(N_STEPS):
    x += going
    steps.append((x, h))
    h += rise
    steps.append((x, h))
landing_top = h
steps.append((LENGTH, landing_top))
# light back edge of the treads (stair width receding)
dx, dy = DEPTH_A * S * OBL[0], DEPTH_A * S * OBL[1]
w(f'<polyline points="{X(0) + dx:.1f},{Y(STAIR_DEPTH) + dy:.1f} {X(SLOPE_END) + dx:.1f},{Y(landing_top) + dy:.1f} {X(LENGTH):.1f},{Y(landing_top) + dy:.1f}" '
  f'fill="none" stroke="#aaa" stroke-width="1.2"/>')
w(f'<line x1="{X(0):.1f}" y1="{Y(STAIR_DEPTH):.1f}" x2="{X(0) + dx:.1f}" y2="{Y(STAIR_DEPTH) + dy:.1f}" stroke="#aaa" stroke-width="1.2"/>')
w(f'<line x1="{X(SLOPE_END):.1f}" y1="{Y(landing_top):.1f}" x2="{X(SLOPE_END) + dx:.1f}" y2="{Y(landing_top) + dy:.1f}" stroke="#aaa" stroke-width="1.2"/>')
w(f'<polyline points="{P(steps)}" fill="none" stroke="{INK}" stroke-width="3"/>')
w(f'<line x1="{X(0)}" y1="{Y(0)}" x2="{X(0)}" y2="{Y(STAIR_DEPTH)}" stroke="{INK}" stroke-width="3"/>')

# stair underside, top board line, floor
w(f'<polyline points="{P([(0, 0), (SLOPE_END, HEIGHT), (LENGTH, HEIGHT)])}" fill="none" stroke="{INK}" stroke-width="3"/>')
w(f'<polyline points="{P([(BOARD / SLOPE, 0), (SLOPE_END, HEIGHT - BOARD), (LENGTH, HEIGHT - BOARD)])}" fill="none" stroke="{INK}" stroke-width="1.4"/>')
w(f'<line x1="{X(0)}" y1="{Y(0)}" x2="{X(LENGTH)}" y2="{Y(0)}" stroke="{INK}" stroke-width="3"/>')

# ---- Cupboard interiors and shelves ----------------------------------------------
for i, (name, x0, width, n) in enumerate(CUPBOARDS):
    a, b = x0 + 4, x0 + width - 4          # small gap either side of the 18 mm divider line
    poly = opening(a, b)
    w(f'<clipPath id="c{i}"><polygon points="{P(poly)}"/></clipPath>')
    w(f'<g clip-path="url(#c{i})">')
    w(f'<polygon points="{P(poly)}" fill="{BACK}"/>')
    w(f'<polygon points="{P([(a, 0), (a + 40, 0), (a + 40, HEIGHT), (a, HEIGHT)])}" fill="{SIDE}"/>')
    w(f'<polyline points="{P(poly[2:])}" fill="none" stroke="{SIDE}" stroke-width="20" opacity="0.7"/>')
    tallest = max(h for _, h in poly)
    gap = tallest / (n + 1)
    for k in range(1, n + 1):
        sh = k * gap
        sx0 = max(a, x_at(sh + BOARD) + 6) if sh + BOARD > inside_top(a) else a
        w(f'<rect x="{X(sx0):.1f}" y="{Y(sh) + 5:.1f}" width="{(b - sx0) * S:.1f}" height="6" fill="#000" opacity="0.10"/>')
        w(f'<rect x="{X(sx0):.1f}" y="{Y(sh):.1f}" width="{(b - sx0) * S:.1f}" height="{BOARD * S + 1:.1f}" fill="{SHELF}" stroke="{INK}" stroke-width="1.2"/>')
    w('</g>')
    w(f'<polygon points="{P(poly)}" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>')

# ---- End panel and shelving side ----------------------------------------------------
top_y = Y(landing_top) + 20
base_y = Y(0)
ex = X(LENGTH)
w(f'<polygon points="{ex + 8},{top_y} {ex + 8 + dx:.1f},{top_y + dy:.1f} {ex + 8 + dx:.1f},{base_y + dy:.1f} {ex + 8},{base_y}" '
  f'fill="{DOOR}" stroke="{INK}" stroke-width="1.2"/>')
for frac in (0.2, 0.4, 0.6, 0.8):
    yy = top_y + (base_y - top_y) * frac
    w(f'<line x1="{ex + 8}" y1="{yy:.1f}" x2="{ex + 8 + dx:.1f}" y2="{yy + dy:.1f}" stroke="#777" stroke-width="1"/>')
w(f'<rect x="{ex}" y="{top_y}" width="8" height="{base_y - top_y}" fill="{DOOR}" stroke="{INK}" stroke-width="1.6"/>')

# ---- Open doors ----------------------------------------------------------------------
if SHOW_DOORS:
    x0 = F + 1800
    mid = x0 + 500
    door_open(x0 + 4, inside_top(x0 + 4), inside_top(mid), 500, -1)
    door_open(x0 + 996, inside_top(x0 + 996), inside_top(mid), 500, +1)
    # Hinge side for each single door: "L" or "R"
    HINGES = ["L", "L", "L"]          # cupboards 1, 2, 3
    for i, (name, c0, width, n) in reversed(list(enumerate(CUPBOARDS[:3]))):
        left, right = c0 + 4, c0 + width - 4
        if HINGES[i] == "L":
            door_open(left, inside_top(left), inside_top(right), width, -1)
        else:
            door_open(right, inside_top(right), inside_top(left), width, +1)

# ---- Labels A–F and dimensions -----------------------------------------------------------
arrow(ex + 4, top_y - 22, ex + 4 + dx, top_y - 22 + dy); label(ex + dx + 30, top_y - 22 + dy - 6, "A", extra='')
label(ex + dx + 30, top_y - 22 + dy + 18, "700", size=17, weight="normal", fill="#555")
arrow(X(SLOPE_END), Y(landing_top) - 34, X(LENGTH), Y(landing_top) - 34); label((X(SLOPE_END) + X(LENGTH)) / 2, Y(landing_top) - 46, "B")
arrow(X(LENGTH) - 70, Y(HEIGHT) - 22, X(LENGTH) - 6, Y(HEIGHT) - 22, both=False); label(X(LENGTH) - 92, Y(HEIGHT) - 13, "E")
cx = 5 * SLOPE_END / N_STEPS - 40
label(X(cx), Y(underside(cx) + 150), "C")
d0 = (X(-130), Y(STAIR_DEPTH - 40)); d1 = (X(400), Y(STAIR_DEPTH + 400 * SLOPE + 60))
arrow(*d0, *d1, both=False); label(d0[0] + 12, d0[1] - 40, "D")

# overall height
hx = ex + dx + 70
arrow(hx, Y(0), hx, Y(HEIGHT))
w(f'<rect x="{hx - 12}" y="{(Y(0) + Y(HEIGHT)) / 2 - 34}" width="24" height="68" fill="#fff"/>')
label(hx, (Y(0) + Y(HEIGHT)) / 2, "2270", size=20, anchor="middle", extra=f'transform="rotate(-90 {hx} {(Y(0) + Y(HEIGHT)) / 2})" dy="7"')
w(f'<line x1="{X(LENGTH)}" y1="{Y(HEIGHT)}" x2="{hx + 6}" y2="{Y(HEIGHT)}" stroke="#999" stroke-width="1" stroke-dasharray="4 4"/>')

label(hx + 40, Y(HEIGHT / 2) + 10, "Shelves", size=26, anchor="start")
w(f'<line x1="{hx + 40}" y1="{Y(HEIGHT / 2) + 22}" x2="{hx + 140}" y2="{Y(HEIGHT / 2) + 22}" stroke="{INK}" stroke-width="2"/>')

# bottom dimension chain
dim_y = Y(0) + 40
edges = [0, F] + [c[1] + c[2] for c in CUPBOARDS]
for xx in edges:
    w(f'<line x1="{X(xx)}" y1="{Y(0) + 4}" x2="{X(xx)}" y2="{dim_y + 10}" stroke="#999" stroke-width="1" stroke-dasharray="4 4"/>')
names = ["F", "600", "600", "600", "1000"]
for (a, b), t in zip(zip(edges, edges[1:]), names):
    arrow(X(a) + 2, dim_y, X(b) - 2, dim_y)
    label((X(a) + X(b)) / 2, dim_y + 34, t, size=22)
label(X(F / 2), dim_y + 56, "470", size=15, weight="normal", fill="#555")
captions = [("Cupboard 1", "1 shelf"), ("Cupboard 2", "3 shelves"), ("Cupboard 3", "4 shelves"), ("Double doors 4", "5 shelves")]
for (a, b), (c1, c2) in zip(list(zip(edges, edges[1:]))[1:], captions):
    label((X(a) + X(b)) / 2, dim_y + 64, c1, size=18, weight="normal", fill="#444")
    label((X(a) + X(b)) / 2, dim_y + 86, c2, size=15, weight="normal", fill="#777")
# overall length
ly = dim_y + 128
w(f'<line x1="{X(0)}" y1="{dim_y + 10}" x2="{X(0)}" y2="{ly + 8}" stroke="#999" stroke-width="1" stroke-dasharray="4 4"/>')
w(f'<line x1="{X(LENGTH)}" y1="{dim_y + 10}" x2="{X(LENGTH)}" y2="{ly + 8}" stroke="#999" stroke-width="1" stroke-dasharray="4 4"/>')
arrow(X(0) + 2, ly, X(LENGTH) - 2, ly)
w(f'<rect x="{(X(0) + X(LENGTH)) / 2 - 34}" y="{ly - 13}" width="68" height="26" fill="#fff"/>')
label((X(0) + X(LENGTH)) / 2, ly + 8, "3270", size=22)

w('</svg>')

Path(__file__).with_name(OUT_NAME).write_text("\n".join(out), encoding="utf-8")
print("wrote", OUT_NAME)
