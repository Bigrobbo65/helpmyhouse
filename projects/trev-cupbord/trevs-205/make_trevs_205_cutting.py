"""Cutting diagram for Trevs 205 under-stair cupboards.

5 sheets of 2440 x 1220 x 18 MDF. All sizes in mm, 3 mm saw kerf.
Run:  python make_trevs_205_cutting.py  ->  trevs-205-cutting.svg
"""
from pathlib import Path

SW, SH = 2440, 1220
S = 0.36                       # px per mm
MX, TOP = 70, 150             # left margin, title area
GAP = 150                      # vertical space between sheets
INK, MUTED = "#1f1f1f", "#666"
DOOR_FILL, SHELF_FILL, WASTE = "#f3e3c8", "#dbe7f0", "#f2f2f2"

# Each piece: (kind, label, size text, polygon in sheet mm coords [x along 2440, y along 1220])
def rect(x, y, w, h):
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]

SHEETS = [
    ("Sheet 1", "Cut lengthways into 700 + 517 strips", [
        ("shelf", "Shelf DD", "964 × 700", rect(0, 0, 964, 700)),
        ("shelf", "Shelf C", "564 × 700", rect(967, 0, 564, 700)),
        ("shelf", "Shelf C", "564 × 700", rect(1534, 0, 564, 700)),
        ("door", "Double door – left leaf", "2270 × 500", rect(0, 703, 2270, 500)),
    ]),
    ("Sheet 2", "Cut lengthways into 700 + 517 strips", [
        ("shelf", "Shelf DD", "964 × 700", rect(0, 0, 964, 700)),
        ("shelf", "Shelf C", "564 × 700", rect(967, 0, 564, 700)),
        ("shelf", "Shelf C", "564 × 700", rect(1534, 0, 564, 700)),
        ("door", "Double door – right leaf", "2270 × 500", rect(0, 703, 2270, 500)),
    ]),
    ("Sheet 3", "Cut lengthways into 600 + 617 strips · Doors 1 &amp; 2 nest on one angled cut", [
        ("door", "Door 3", "600 wide · 2074 / 1526", [(0, 0), (2074, 0), (1526, 600), (0, 600)]),
        ("door", "Door 2", "600 wide · 1526 / 977", [(0, 603), (1526, 603), (977, 1203), (0, 1203)]),
        ("door", "Door 1 (rotated)", "600 wide · 977 / 429", [(1529, 603), (1958, 603), (1958, 1203), (980, 1203)]),
    ]),
    ("Sheet 4", "Cut across the sheet into three 700 strips", [
        ("shelf", "Shelf DD", "964 × 700", rect(0, 0, 700, 964)),
        ("shelf", "Shelf DD", "964 × 700", rect(703, 0, 700, 964)),
        ("shelf", "Shelf DD", "964 × 700", rect(1406, 0, 700, 964)),
    ]),
    ("Sheet 5", "Cut across into two 700 strips, then each into two shelves · rest is spare", [
        ("shelf", "Shelf C", "564 × 700", rect(0, 0, 700, 564)),
        ("shelf", "Shelf C", "564 × 700", rect(0, 567, 700, 564)),
        ("shelf", "Shelf C", "564 × 700", rect(703, 0, 700, 564)),
        ("shelf", "Shelf C", "564 × 700", rect(703, 567, 700, 564)),
    ]),
]

W = int(MX * 2 + SW * S + 40)
H = int(TOP + len(SHEETS) * (SH * S + GAP) + 60)
out = []
w = out.append
w(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Arial, Helvetica, sans-serif">')
w(f'<rect width="{W}" height="{H}" fill="#fff"/>')
w('<defs><pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
  f'<rect width="8" height="8" fill="{WASTE}"/><line x1="0" y1="0" x2="0" y2="8" stroke="#d4d4d4" stroke-width="2"/></pattern></defs>')
w(f'<text x="{MX}" y="52" font-size="28" font-weight="bold" fill="{INK}">Trevs 205 — cutting diagram</text>')
w(f'<text x="{MX}" y="84" font-size="17" fill="{MUTED}">5 sheets · 2440 × 1220 × 18 mm MDF · 3 mm saw kerf · door heights are opening sizes, trim for top rail and gaps</text>')

# legend
lx = MX
for i, (fill, name) in enumerate(((DOOR_FILL, "Door"), (SHELF_FILL, "Shelf"), ("url(#hatch)", "Offcut / waste"))):
    x = lx + i * 110
    w(f'<rect x="{x}" y="104" width="18" height="18" fill="{fill}" stroke="{INK}" stroke-width="1"/>')
    w(f'<text x="{x + 25}" y="118" font-size="15" fill="{INK}">{name}</text>')


def P(ox, oy, pts):
    return " ".join(f"{ox + x * S:.1f},{oy + y * S:.1f}" for x, y in pts)


for i, (title, note, pieces) in enumerate(SHEETS):
    oy = TOP + 40 + i * (SH * S + GAP)
    ox = MX
    w(f'<text x="{ox}" y="{oy - 14}" font-size="20" font-weight="bold" fill="{INK}">{title}</text>')
    w(f'<text x="{ox + 95}" y="{oy - 14}" font-size="16" fill="{MUTED}">{note}</text>')
    w(f'<rect x="{ox}" y="{oy}" width="{SW * S}" height="{SH * S}" fill="url(#hatch)" stroke="{INK}" stroke-width="2"/>')
    for kind, label, size, pts in pieces:
        fill = DOOR_FILL if kind == "door" else SHELF_FILL
        w(f'<polygon points="{P(ox, oy, pts)}" fill="{fill}" stroke="{INK}" stroke-width="1.5"/>')
        cx = sum(x for x, _ in pts) / len(pts)
        cy = sum(y for _, y in pts) / len(pts)
        px, py = ox + cx * S, oy + cy * S
        w(f'<text x="{px:.1f}" y="{py - 4:.1f}" font-size="15" font-weight="bold" fill="{INK}" text-anchor="middle">{label}</text>')
        w(f'<text x="{px:.1f}" y="{py + 15:.1f}" font-size="14" fill="{INK}" text-anchor="middle">{size}</text>')
    # sheet dimensions
    w(f'<text x="{ox + SW * S / 2}" y="{oy + SH * S + 22}" font-size="13" fill="{MUTED}" text-anchor="middle">2440</text>')
    w(f'<text x="{ox + SW * S + 10}" y="{oy + SH * S / 2}" font-size="13" fill="{MUTED}" transform="rotate(90 {ox + SW * S + 10} {oy + SH * S / 2})" text-anchor="middle">1220</text>')

w(f'<text x="{MX}" y="{H - 30}" font-size="15" fill="{MUTED}">Shelf C = cupboards 1–3 (8 needed) · Shelf DD = double-door section (5 needed) · Door sizes: width · tall side / short side</text>')
w('</svg>')

Path(__file__).with_name("trevs-205-cutting.svg").write_text("\n".join(out), encoding="utf-8")
print("wrote trevs-205-cutting.svg", W, H)
