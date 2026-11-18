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
