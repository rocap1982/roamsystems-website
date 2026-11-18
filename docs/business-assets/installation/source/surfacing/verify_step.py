"""Read the delivered STEP back, find each body by name, tessellate it and measure two-way 3D deviation
against the scan triangles it was built from (moved into the model frame)."""
import sys, json, numpy as np, trimesh
sys.path.insert(0, sys.argv[1])
import verify2
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.XCAFApp import XCAFApp_Application
from OCP.XCAFDoc import XCAFDoc_DocumentTool
from OCP.TDF import TDF_LabelSequence
from OCP.TDataStd import TDataStd_Name
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE
from OCP.TopoDS import TopoDS

step, new_p, old_p, out = sys.argv[2:6]
fr = json.load(open(out + '_report.json'))['frame']
shift = np.array([-fr['CX'], fr['Y0'], fr['Z0']])
app = XCAFApp_Application.GetApplication_s()
doc = TDocStd_Document(TCollection_ExtendedString('MDTV-XCAF')); app.InitDocument(doc)
r = STEPCAFControl_Reader(); r.SetNameMode(True); r.SetColorMode(True)
assert r.ReadFile(step) == 1
r.Transfer(doc)
st = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
labs = TDF_LabelSequence(); st.GetFreeShapes(labs)
bodies = {}
for i in range(1, labs.Length() + 1):
    lab = labs.Value(i)
    nm = TDataStd_Name()
    name = nm.Get().ToExtString() if lab.FindAttribute(TDataStd_Name.GetID_s(), nm) else '?'
    bodies[name] = st.GetShape_s(lab)
print('bodies in file:', list(bodies))
nm_ = trimesh.load(new_p); nm_.merge_vertices(); nm_.update_faces(nm_.area_faces > 1e-4); nm_.remove_unreferenced_vertices()
meshes = {'Underside - new scan': trimesh.load(out + '_newscan_used.stl'), 'Underside - first scan (coarse)': trimesh.load(out + '_firstscan_used.stl')}
res = {}
for name, src in meshes.items():
    shp = bodies[name]
    nf = 0; ex = TopExp_Explorer(shp, TopAbs_FACE)
    invalid = 0
    while ex.More():
        nf += 1
        if not BRepCheck_Analyzer(TopoDS.Face_s(ex.Current())).IsValid():
            invalid += 1
        ex.Next()
    src = src.copy(); src.apply_translation(shift)
    tm, bad = verify2.tessellate(shp)
    p, d1 = verify2.one_way(src, tm, 1500000, 21)
    q, d2 = verify2.one_way(tm, src, 1500000, 23)
    r1 = verify2.report('scan -> model', d1); r2 = verify2.report('model -> scan', d2)
    print('%s: faces %d, invalid %d, without mesh %d\n  %s\n  %s' % (name, nf, invalid, bad, r1, r2), flush=True)
    res[name] = dict(faces=nf, invalid=invalid, scan_to_model=r1, model_to_scan=r2, max_scan_to_model=float(d1.max()), max_model_to_scan=float(d2.max()))
    np.save(out + '_readback_bad_%d.npy' % len(res), np.vstack([p[d1 > 1.0], q[d2 > 1.0]]))
    tm.export(out + '_readback_%d.stl' % len(res))
json.dump(res, open(out + '_readback.json', 'w'), indent=1)
