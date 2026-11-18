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
