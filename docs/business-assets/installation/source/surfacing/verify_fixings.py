"""Read the STEP with fixings back in: every body by name with face count, invalid faces and colour; each fixing's
axis position from its solid's centroid; compare the surface bodies with the earlier verified read-back.
usage: verify_fixings.py with_fixings.step earlier_readback.json fixings.json"""
import sys, json, numpy as np
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.XCAFApp import XCAFApp_Application
from OCP.XCAFDoc import XCAFDoc_DocumentTool, XCAFDoc_ColorType, XCAFDoc_ColorTool
from OCP.TDF import TDF_LabelSequence
from OCP.TDataStd import TDataStd_Name
from OCP.Quantity import Quantity_Color
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE, TopAbs_EDGE, TopAbs_SOLID
from OCP.TopoDS import TopoDS
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp

step, ref, fxj = sys.argv[1:4]
ref = json.load(open(ref)); fx = json.load(open(fxj))
app = XCAFApp_Application.GetApplication_s()
doc = TDocStd_Document(TCollection_ExtendedString('MDTV-XCAF')); app.InitDocument(doc)
r = STEPCAFControl_Reader(); r.SetNameMode(True); r.SetColorMode(True)
assert r.ReadFile(step) == 1
r.Transfer(doc)
st = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main()); ct = XCAFDoc_DocumentTool.ColorTool_s(doc.Main())
labs = TDF_LabelSequence(); st.GetFreeShapes(labs)


def count(shp, kind):
    n = 0; ex = TopExp_Explorer(shp, kind)
    while ex.More():
        n += 1; ex.Next()
    return n


ok = True; fix_found = {}
for i in range(1, labs.Length() + 1):
    lab = labs.Value(i); nm = TDataStd_Name()
    name = nm.Get().ToExtString() if lab.FindAttribute(TDataStd_Name.GetID_s(), nm) else '?'
    shp = st.GetShape_s(lab)
    c = Quantity_Color(); has = False
    for getter in (lambda ty: XCAFDoc_ColorTool.GetColor_s(lab, ty, c), lambda ty: ct.GetColor(shp, ty, c)):
        for ty in (XCAFDoc_ColorType.XCAFDoc_ColorSurf, XCAFDoc_ColorType.XCAFDoc_ColorCurv, XCAFDoc_ColorType.XCAFDoc_ColorGen):
            try:
                has = has or bool(getter(ty))
            except Exception:
                pass
    col = '(%.2f %.2f %.2f)' % (c.Red(), c.Green(), c.Blue()) if has else 'no colour'
    nf = count(shp, TopAbs_FACE); bad = 0; ex = TopExp_Explorer(shp, TopAbs_FACE)
    while ex.More():
        bad += not BRepCheck_Analyzer(TopoDS.Face_s(ex.Current())).IsValid(); ex.Next()
    extra = ''
    if name in ref:
        same = ref[name]['faces'] == nf
        ok &= same and bad == 0
        extra = ' | earlier verified read-back: %d faces -> %s' % (ref[name]['faces'], 'same' if same else 'DIFFERENT')
    if name.startswith('Seat fixing') and 'hole' in name:
        g = GProp_GProps(); BRepGProp.VolumeProperties_s(shp, g); p = g.CentreOfMass()
        fix_found[name] = (p.X(), p.Z(), g.Mass())
        extra = ' | axis X %.2f Z %.2f, volume %.0f mm3' % (p.X(), p.Z(), g.Mass())
    print('%-62s faces %5d invalid %d edges %6d solids %d %s%s' % (name, nf, bad, count(shp, TopAbs_EDGE), count(shp, TopAbs_SOLID), col, extra), flush=True)
exp = {'Seat fixing %s %d (%dmm from heel) - hole 12.5' % (s, k, d): (x, z) for s, k, d, x, z in fx['fixings']}
assert set(exp) == set(fix_found), 'fixings missing or extra'
err = max(max(abs(fix_found[n][0] - x), abs(fix_found[n][1] - z)) for n, (x, z) in exp.items())
pairs = {}
for n, (x, z, v) in fix_found.items():
    pairs.setdefault(n.split('(')[-1].split('mm')[0], []).append(x)      # group the left and right fixing at each station
sym = max(abs(sum(v)) for v in pairs.values())
print('fixings found %d; worst position error vs table %.3f mm; worst left/right asymmetry about X 0: %.3f mm; surface bodies unchanged and valid: %s' % (
    len(fix_found), err, sym, ok))
