# Trevs 205 — under-stair cupboards

Client project for Trev Cupbord.

## Site measurements

| Item | Size (mm) |
|---|---|
| Overall length | 3270 |
| Overall height (floor to underside of landing) | 2270 |
| Depth (A) | 700 |
| F (low space at bottom of stairs) | 470 |
| Cupboards 1, 2, 3 | 600 each |
| Double doors 4 | 1000 (2 × 500 leaves) |
| Where stairs meet landing | ~2485 from left (assumed, B ≈ 785; to be measured) |

## Spec

- Material: 18 mm MDF
- Doors: mid grey · carcass, shelves and stair: white · handles: chrome bar
- Shelves: cupboard 1 = 1, cupboard 2 = 3, cupboard 3 = 4, double doors = 5
  - Shelf sizes: 8 × 564 × 700, 5 × 964 × 700
- Hinges: cupboards 1–3 hinged on the left; double doors open one leaf each way

## Materials

**5 sheets of 2440 × 1220 × 18 mm MDF.** See `trevs-205-cutting.png`.
Door heights in the cutting list are opening sizes. Trim them for the top rail and door gaps (about 20 mm).

## Files

| File | What it is |
|---|---|
| `trevs-205-open.png/.svg` | Elevation to scale, doors open |
| `trevs-205-no-doors.png/.svg` | Elevation to scale, doors removed |
| `trevs-205-cutting.png/.svg` | Cutting diagram for 5 sheets |
| `trevs-205-3d-right.png`, `trevs-205-3d-left.png` | 3D renders |
| `trevs-205-3d.html` | Interactive 3D model (open in a browser; needs internet) |
| `make_trevs_205_open.py` | Draws the elevations (`--no-doors` for the doorless version) |
| `make_trevs_205_cutting.py` | Draws the cutting diagram |
