"""Full underside surface model with a write/read-back safety net.
1. surfaces from each scan (rsurf), 2. write STEP, 3. read it back, 4. any face that comes back invalid or
will not mesh is replaced by exact planar facets of itself, 5. repeat until the read-back is clean,
6. round coordinates, zip, report."""
import sys, time, json, os, re, zipfile, numpy as np, trimesh
sys.path.insert(0, sys.argv[1])
import rsurf
from raster import raster_min
from scipy import ndimage
from OCP.BRep import BRep_Builder, BRep_Tool
from OCP.TopoDS import TopoDS_Shell, TopoDS
from OCP.TopLoc import TopLoc_Location
from OCP.gp import gp_Trsf, gp_Vec, gp_Pnt
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform, BRepBuilderAPI_MakeEdge, BRepBuilderAPI_Sewing
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.XCAFApp import XCAFApp_Application
from OCP.XCAFDoc import XCAFDoc_DocumentTool, XCAFDoc_ColorType
from OCP.TDataStd import TDataStd_Name
from OCP.TDF import TDF_LabelSequence
from OCP.Quantity import Quantity_Color, Quantity_TypeOfColor
from OCP.STEPCAFControl import STEPCAFControl_Writer, STEPCAFControl_Reader
from OCP.STEPControl import STEPControl_AsIs
from OCP.Interface import Interface_Static
from OCP.IFSelect import IFSelect_RetDone

new_p, old_p, out = sys.argv[2], sys.argv[3], sys.argv[4]
CX, Y0, Z0 = 120.0, 216.1, 166.0
NAMES = {1: 'Underside - new scan', 2: 'Underside - first scan (coarse)'}
COLS = {1: (0.62, 0.66, 0.72), 2: (0.90, 0.62, 0.30)}
t0 = time.time()


def clean(m):
    m.merge_vertices()
    nd = int((m.area_faces <= 1e-4).sum())
    m.update_faces(m.area_faces > 1e-4); m.remove_unreferenced_vertices()
    return nd


new = trimesh.load(new_p); old = trimesh.load(old_p)
print('zero-area triangles removed: new %d, first %d' % (clean(new), clean(old)))
# first-scan triangles only where the new scan has nothing, underside only
g = 2.0; x0, z0 = -820.0, -460.0
shape = (int((1080 - z0) / g), int((1000 - x0) / g))
Hn = raster_min(new.vertices, new.faces, x0, z0, g, shape)
newcov = ndimage.binary_dilation(np.isfinite(Hn), iterations=2)
Ho = raster_min(old.vertices, old.faces, x0, z0, g, shape, maxcell=80)
nbmax = ndimage.maximum_filter(np.where(np.isfinite(Ho), Ho, -1e9), size=5)
c = old.triangles_center; n = old.face_normals
ci = np.clip(((c[:, 0] - x0) / g).astype(int), 0, shape[1] - 1); cj = np.clip(((c[:, 2] - z0) / g).astype(int), 0, shape[0] - 1)
keep = (n[:, 1] < 0.5) & (c[:, 1] < -204) & (c[:, 1] <= nbmax[cj, ci] + 1.0) & ~newcov[cj, ci]
keep &= ~(n[:, 1] < -0.5) | (c[:, 1] <= Ho[cj, ci] + 2.0)
oldk = old.submesh([np.nonzero(keep)[0]], append=True); clean(oldk)
oldk.export(out + '_firstscan_used.stl')
new.export(out + '_newscan_used.stl')
print('first-scan triangles used %d (%.3f m2); new scan %d (%.3f m2)' % (len(oldk.faces), oldk.area / 1e6, len(new.faces), new.area / 1e6), flush=True)

from OCP.STEPControl import STEPControl_Writer, STEPControl_Reader
TMP = out + '_face_rt.step'
B0 = BRep_Builder()
tr0 = gp_Trsf(); tr0.SetTranslation(gp_Vec(-CX, Y0, Z0))


NUM = re.compile(r'(-?\d+\.\d{5})\d+')


def face_survives(f):
    """write one face to STEP (moved to the model frame, rounded as in the final file), read it back:
    it must be valid and must mesh"""
    sh = TopoDS_Shell(); B0.MakeShell(sh); B0.Add(sh, f)
    sh = BRepBuilderAPI_Transform(sh, tr0, True).Shape()
    w = STEPControl_Writer(); w.Transfer(sh, STEPControl_AsIs)
    if w.Write(TMP + '.raw') != IFSelect_RetDone:
        return False
    with open(TMP + '.raw') as fi, open(TMP, 'w') as fo:
        for line in fi:
            fo.write(NUM.sub(r'\1', line) if 'CARTESIAN_POINT' in line or line.startswith('    ') else line)
    r = STEPControl_Reader()
    if r.ReadFile(TMP) != 1:
        return False
    r.TransferRoots()
    shp = r.OneShape()
    fl_ = face_list(shp)
    if len(fl_) != 1 or not BRepCheck_Analyzer(fl_[0]).IsValid():
        return False
    m0 = mesh_area_centre(f); m1 = mesh_area_centre(fl_[0])
    if m0 is None or m1 is None:
        return False
    (a0, c0), (a1, c1) = m0, m1
    return abs(a1 - a0) <= 0.005 * a0 + 0.1 and np.linalg.norm(c1 - (c0 + [-CX, Y0, Z0])) <= 0.1


def mesh_area_centre(f):
    BRepMesh_IncrementalMesh(f, 0.2, False, 0.4, False)
    loc = TopLoc_Location()
    tri = BRep_Tool.Triangulation_s(f, loc)
    if tri is None or tri.NbTriangles() == 0:
        return None
    trf = loc.Transformation()
    P = np.array([[q.X(), q.Y(), q.Z()] for q in (tri.Node(i).Transformed(trf) for i in range(1, tri.NbNodes() + 1))])
    T = np.array([tri.Triangle(i).Get() for i in range(1, tri.NbTriangles() + 1)]) - 1
    ar = 0.5 * np.linalg.norm(np.cross(P[T[:, 1]] - P[T[:, 0]], P[T[:, 2]] - P[T[:, 0]]), axis=1)
    if ar.sum() <= 0:
        return None
    cen = (P[T].mean(1) * ar[:, None]).sum(0) / ar.sum()
    return ar.sum(), cen


def area_centre(f):
    from OCP.GProp import GProp_GProps
    from OCP.BRepGProp import BRepGProp
    g_ = GProp_GProps(); BRepGProp.SurfaceProperties_s(f, g_)
    p = g_.CentreOfMass()
    return g_.Mass(), np.array([p.X(), p.Y(), p.Z()])


def face_list(shp):
    fl = []; ex = TopExp_Explorer(shp, TopAbs_FACE)
    while ex.More():
        fl.append(TopoDS.Face_s(ex.Current())); ex.Next()
    return fl


def facets_of(f):
    """exact planar facets of an (in-memory, valid) face, from a fine tessellation"""
    BRepMesh_IncrementalMesh(f, 0.15, False, 0.5, False)
    loc = TopLoc_Location(); t = BRep_Tool.Triangulation_s(f, loc)
    if t is None:
        return []
    trf = loc.Transformation()
    P = [t.Node(i).Transformed(trf) for i in range(1, t.NbNodes() + 1)]
    sew = BRepBuilderAPI_Sewing(1e-5)
    k = 0
    for i in range(1, t.NbTriangles() + 1):
        a, b, c_ = t.Triangle(i).Get()
        ff = rsurf.facet_face(np.array([[P[j - 1].X(), P[j - 1].Y(), P[j - 1].Z()] for j in (a, b, c_)]))
        if ff is not None:
            sew.Add(ff); k += 1
    if k == 0:
        return []
    sew.Perform()
    return face_list(sew.SewedShape())


faces = {}
stats = {}
meta = {}
surfacers = {}
for s_, mesh_src, tol, ttol in ((1, new, 0.8, 1.2), (2, oldk, 0.8, 1.2)):
    rsurf.TOL, rsurf.TOL_TRI = tol, ttol
    S = rsurf.Surfacer(mesh_src.vertices, mesh_src.faces, mesh_src.face_normals, mesh_src.face_adjacency)
    for d in rsurf.DIRS:
        S.run_direction(d)
    ff = S.facet_faces()
    sew = BRepBuilderAPI_Sewing(1e-4)
    for f, _ in ff:
        sew.Add(f)
    sew.Perform()
    fl = []
    nrep = 0
    rep_sew = BRepBuilderAPI_Sewing(1e-4); nrep_f = 0
    main_faces = list(S.faces)
    meta_l = []
    for f, ids, dname, rect, loc_ in main_faces:
        if face_survives(f):
            fl.append(f); meta_l.append((dname, rect, loc_))
            continue
        nrep += 1
        S.setup(dname)
        keepF, keepP = S.faces, S.facets
        S.faces, S.facets = [], []
        S.split(loc_, rect)
        subF, subP = S.faces, S.facets
        S.faces, S.facets = keepF, keepP
        pieces = list(subP)
        for f2, ids2, d2, rect2, loc2 in subF:
            if face_survives(f2):
                fl.append(f2); meta_l.append((d2, rect2, loc2))
            else:
                pieces.extend(S.exact_pieces(d2, loc2, rect2))
        for P in pieces:
            ff_ = rsurf.facet_face(P)
            if ff_ is not None:
                rep_sew.Add(ff_); nrep_f += 1
    if nrep_f:
        rep_sew.Perform(); fx = face_list(rep_sew.SewedShape()); fl.extend(fx); meta_l.extend([None] * len(fx))
    print('src %d: %d of %d surface faces failed a STEP round trip on their own -> re-surfaced in quarters, %d exact facets used' % (s_, nrep, len(main_faces), nrep_f), flush=True)
    ex = TopExp_Explorer(sew.SewedShape(), TopAbs_FACE)
    while ex.More():
        fl.append(TopoDS.Face_s(ex.Current())); meta_l.append(None); ex.Next()
    faces[s_] = fl; meta[s_] = meta_l; surfacers[s_] = S
    stats[s_] = dict(S.stats, surface_faces=len(main_faces) - nrep, roundtrip_replaced=nrep, total_faces=len(fl), relabelled=S.relabelled)
    print('src %d: %s  (%.0fs)' % (s_, stats[s_], time.time() - t0), flush=True)

tr = gp_Trsf(); tr.SetTranslation(gp_Vec(-CX, Y0, Z0))
B = BRep_Builder()


def body(fl):
    sh = TopoDS_Shell(); B.MakeShell(sh)
    for f in fl:
        B.Add(sh, f)
    return BRepBuilderAPI_Transform(sh, tr, True).Shape()


def write(path):
    app = XCAFApp_Application.GetApplication_s()
    doc = TDocStd_Document(TCollection_ExtendedString('MDTV-XCAF')); app.InitDocument(doc)
    st = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main()); ct = XCAFDoc_DocumentTool.ColorTool_s(doc.Main())
    cl = BRepBuilderAPI_MakeEdge(gp_Pnt(0, 0, -460 + Z0), gp_Pnt(0, 0, 1080 + Z0)).Edge()
    items = [(body(faces[1]), NAMES[1], COLS[1]), (body(faces[2]), NAMES[2], COLS[2]), (cl, 'Underbody centreline', (0.85, 0.1, 0.1))]
    for shp, name, rgb in items:
        lab = st.AddShape(shp, False)
        TDataStd_Name.Set_s(lab, TCollection_ExtendedString(name))
        col = Quantity_Color(rgb[0], rgb[1], rgb[2], Quantity_TypeOfColor.Quantity_TOC_RGB)
        ct.SetColor(lab, col, XCAFDoc_ColorType.XCAFDoc_ColorSurf); ct.SetColor(lab, col, XCAFDoc_ColorType.XCAFDoc_ColorCurv)
    Interface_Static.SetCVal_s('write.step.unit', 'MM'); Interface_Static.SetCVal_s('write.step.schema', 'AP214IS')
    w = STEPCAFControl_Writer(); w.SetColorMode(True); w.SetNameMode(True)
    w.Transfer(doc, STEPControl_AsIs)
    assert w.Write(path + '_raw.step') == IFSelect_RetDone
    num = re.compile(r'(-?\d+\.\d{5})\d+')
    with open(path + '_raw.step') as fi, open(path, 'w') as fo:
        for line in fi:
            fo.write(num.sub(r'\1', line) if 'CARTESIAN_POINT' in line or line.startswith('    ') else line)
    os.remove(path + '_raw.step')


def read_bodies(path):
    app = XCAFApp_Application.GetApplication_s()
    doc = TDocStd_Document(TCollection_ExtendedString('MDTV-XCAF')); app.InitDocument(doc)
    r = STEPCAFControl_Reader(); r.SetNameMode(True)
    assert r.ReadFile(path) == 1
    r.Transfer(doc)
    st = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    labs = TDF_LabelSequence(); st.GetFreeShapes(labs)
    out_ = {}
    for i in range(1, labs.Length() + 1):
        lab = labs.Value(i); nm = TDataStd_Name()
        name = nm.Get().ToExtString() if lab.FindAttribute(TDataStd_Name.GetID_s(), nm) else '?'
        out_[name] = st.GetShape_s(lab)
    return out_


def face_list(shp):
    fl = []; ex = TopExp_Explorer(shp, TopAbs_FACE)
    while ex.More():
        fl.append(TopoDS.Face_s(ex.Current())); ex.Next()
    return fl


def centre(f):
    from OCP.GProp import GProp_GProps
    from OCP.BRepGProp import BRepGProp
    g_ = GProp_GProps(); BRepGProp.SurfaceProperties_s(f, g_)
    p = g_.CentreOfMass()
    return np.array([p.X(), p.Y(), p.Z()])


step = out + '.step'
history = []
from scipy.spatial import cKDTree
shift = np.array([-CX, Y0, Z0])


def body_mesh_stats(shp):
    BRepMesh_IncrementalMesh(shp, 0.2, False, 0.4, True)
    out_ = []
    for f in face_list(shp):
        ok = BRepCheck_Analyzer(f).IsValid()
        mc = mesh_area_centre(f)
        out_.append((ok and mc is not None, mc))
    return out_


for it in range(4):
    write(step)
    back = read_bodies(step)
    changed = 0
    for s_ in (1, 2):
        rb = body_mesh_stats(back[NAMES[s_]])
        nbad = sum(1 for ok, _ in rb if not ok)
        good = [(mc[0], mc[1]) for ok, mc in rb if ok]
        Wm = [mesh_area_centre(f) for f in faces[s_]]
        A_r = np.array([g_[0] for g_ in good]); C_r = np.array([g_[1] for g_ in good])
        tree = cKDTree(C_r)
        unmatched = []
        for i, w_ in enumerate(Wm):
            if w_ is None:
                unmatched.append(i); continue
            d_, j_ = tree.query(w_[1] + shift, k=3)
            if not any(dd <= 0.1 and abs(A_r[jj] - w_[0]) <= 0.01 * w_[0] + 0.1 for dd, jj in zip(np.atleast_1d(d_), np.atleast_1d(j_))):
                unmatched.append(i)
        print('iteration %d src %d: read-back faces %d, bad %d; written faces without a good match %d' % (it, s_, len(rb), nbad, len(unmatched)), flush=True)
        history.append(dict(iteration=it, src=s_, read_back=len(rb), bad=nbad, unmatched=len(unmatched)))
        if not unmatched or len(unmatched) > 200:
            continue
        S = surfacers[s_]
        keep_f, keep_m = [], []
        rep_sew = BRepBuilderAPI_Sewing(1e-4); nrep_f = 0
        um = set(unmatched)
        for i, (f, md) in enumerate(zip(faces[s_], meta[s_])):
            if i not in um:
                keep_f.append(f); keep_m.append(md); continue
            changed += 1
            pieces = []
            if md is None:
                continue          # a facet that did not survive: its neighbours cover within tolerance
            dname, rect, loc_ = md
            S.setup(dname)
            kF, kP = S.faces, S.facets
            S.faces, S.facets = [], []
            S.split(loc_, rect)
            subF, subP = S.faces, S.facets
            S.faces, S.facets = kF, kP
            pieces.extend(subP)
            for f2, ids2, d2, rect2, loc2 in subF:
                if it < 2 and face_survives(f2):
                    keep_f.append(f2); keep_m.append((d2, rect2, loc2))
                else:
                    pieces.extend(S.exact_pieces(d2, loc2, rect2))
            for P in pieces:
                ff_ = rsurf.facet_face(P)
                if ff_ is not None:
                    rep_sew.Add(ff_); nrep_f += 1
        if nrep_f:
            rep_sew.Perform(); fx = face_list(rep_sew.SewedShape()); keep_f.extend(fx); keep_m.extend([None] * len(fx))
        faces[s_], meta[s_] = keep_f, keep_m
    if changed == 0:
        break

with zipfile.ZipFile(out + '.zip', 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    z.write(step, os.path.basename(step))
print('step %.1f MB, zip %.1f MB' % (os.path.getsize(step) / 1e6, os.path.getsize(out + '.zip') / 1e6), flush=True)
json.dump(dict(stats=stats, history=history, frame=dict(CX=CX, Y0=Y0, Z0=Z0)), open(out + '_report.json', 'w'), indent=1)
print('done %.0fs' % (time.time() - t0))
