# Scan to STEP surface model (underside of the T6 LWB)

Builds a trimmed B-spline surface model from a scan mesh and checks it against the scan.

- `rsurf.py`: the surfacer. Splits the scan into six view directions (normals smoothed over neighbours), cuts each into 128mm tiles, fits a cubic B-spline height field per connected piece (every 1mm sample within 0.8mm, every triangle check point within 1.2mm) and trims it to the exact outline of its triangles. Pieces that will not fit become exact planar facets of the scan triangles. Nothing is filled where the scan has no data.
- `final_build.py`: runs both scans (new scan; first scan only where the new one has none), tests every surface face with its own STEP round trip, writes the STEP (names, colours, coordinates to 0.00001mm), reads it back and repairs any face that does not survive, then zips it.
- `verify_step.py` and `verify2.py`: read the delivered STEP back and measure two-way 3D deviation against the scan triangles.
- `preview_model.py`: plan and oblique previews from the read-back meshes.

Model frame: X across the van, 0 = underbody centreline (mirror line of studs, members, shocks and floor steps; the diagonal pipe is on the -X side). Y up, 0 = floor panel underside. Z forward, 0 = seat heel as scanned.

Result 18/11/2026 (`T6_LWB_underside_surfaces.step`, 84.7MB, zip 16.8MB), measured on the file read back:
- new-scan body: 8,647 faces, 0 invalid; scan to model max 1.51mm, model to scan max 1.19mm
- first-scan body: 1,614 faces, 0 invalid; scan to model max 1.75mm, model to scan max 1.44mm

Run (Python with OCP/cadquery, trimesh, scipy, shapely, numpy):
`python final_build.py <this folder> <new scan in van frame>.stl <first scan in van frame>.stl <output prefix>`
`python verify_step.py <this folder> <output>.step <new scan>.stl <first scan>.stl <output prefix>`

## Closed model (18/11/2026): gaps filled by inference, kept in separate bodies

- `mirror_fit.py`: fits the underbody's mirror plane by reflecting the scan onto itself. The two sides agree to a median of 0.95mm. The plane showed the earlier frame had a 1.0 degree roll.
- `frame_corr.py`: the corrected (level) model frame. X = 0 on the mirror plane, Y = 0 at the floor panel underside on the centreline, Z = 0 at the seat heel as scanned.
- `infill.py`: closes holes in this order:
  1. mirrored 3D scan triangles from the other side, where the border agrees (median within 3mm, 90% within 7mm) and nothing deeper is brought in;
  2. section continued across the gap where the two ends match;
  3. slits bridged and smooth panels continued;
  4. best guess: the face extended from its steadiest edge, otherwise a smooth surface.
  Compact round holes with a flat rim are treated as real holes and left open.
- `seams.py`: bridges the slits up to 12mm wide that are left between faces of the surfaced model.
- `final_build.py` now takes the frame file and the infill prefix: `python final_build.py <code> <new>.stl <first>.stl <out> frame_corr.json <infill prefix>`

Result `T6_LWB_underside_closed2.step` (136.8MB, zip 29.5MB). Bodies and their share of the plan area:

| Body | Plan share | Faces |
|---|---|---|
| new scan | 35.9% | 8,647 |
| first scan | 53.7% | 1,614 |
| infill mirrored | 4.0% | 1,516 |
| infill continued | 2.0% | 8,779 |
| infill best guess | 3.1% | 158 |

Still open: 0.4%, made up of one real round hole (about 38mm across, at X -590 Z 848) and hairline slivers.

Every body has 0 invalid faces on read-back.
- Scanned bodies: within 1.51 and 1.75mm of the scans, both ways.
- Infill bodies: within 2.6mm of the inferred surface they were built from. Their accuracy against the van is unknown.

## Seat fixings added (19/11/2026)

- `add_fixings.py` adds the 12 seat fixings to the closed model. They follow the hole pattern from the SolidWorks seat model:
  - 12.5mm holes, six per ski;
  - rows 1114mm apart;
  - 19, 55, 169, 301, 431 and 625mm forward of the heel.
- Across the van, the rows sit at X -557 and +557. That is symmetric about the midline of the two parallel chassis members (owner ruling, 19/11/2026).
  - The members' inner walls measure X -375 and +375 at all three stations checked: Z -100 to 50, 100 to 250 and 350 to 600.
  - So the midline is X 0, the same line as the underbody mirror plane.
  - Each row is 182mm outboard of its member's inner wall.
- Fore and aft, the heel is placed from the five seat bolt ends found in the scan (heel at Z 11.0).
  - The heel is the rear of the seat, so fixing 1 (19mm) is the rearmost.
  - The three bolt ends at 19 and 55mm agree with the pattern within about 1mm fore and aft, and sit about 4mm outboard of the rows.
  - The pair at 301mm (fixing 4) sit about 1mm inboard of the rows. They were scanned 7mm behind the pattern on -X and 7mm ahead on +X, so the two sides are 14mm apart fore and aft. A tape check on the van settles it: from fixing 1 to fixing 4 the pattern gives 282mm; the scan gives 276mm on -X and 289mm on +X.
  - The scanned bolt ends go in as separate markers, so the difference stays visible.
- The fixings are built as a small STEP of their own and appended to the verified file as text. The surfaces stay byte-for-byte as delivered.
  - Reading the whole model in and writing it out again re-approximated about 45,000 edge curves and added about 49MB, so that route is not used.
- `verify_fixings.py` reads the result back and checks:
  - every body's face count and validity against the earlier verified read-back;
  - each fixing's axis position.
- `preview_fixings.py` draws a plan of the seat area with the fixings, the scanned bolt ends and the member walls.

Run: `python add_fixings.py <closed>.step <out prefix>`, then `python verify_fixings.py <out>.step <closed>_readback.json <out>_fixings.json`.

Result `T6_LWB_underside_with_fixings.step` (136.9MB, zip 29.5MB), read back:
- The five surface bodies have the same face counts as the verified closed model and 0 invalid faces.
- All 12 fixings are present, each axis within 0.02mm of the table.
- The two rows mirror each other about X 0 to 0.000mm.
- The fixings, axes, bolt-end markers and wall lines all carry their colours in the file.
