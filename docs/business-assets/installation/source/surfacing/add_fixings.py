"""Add the ROAM seat fixing points to the closed underside STEP (level frame) without re-writing the surfaces.

The fixings are built in their own small STEP (same writer, units and schema) and appended to the verified file at
the text level: the first file's entities stay byte-for-byte as delivered, the new ones are renumbered after them and
share its application context. (Reading the whole model in and writing it out again re-approximated about 45,000
edge curves on the way through and added about 49MB, so that route is not used.)

Fixings: pattern from the SolidWorks seat model (12 holes 12.5mm, six per ski, rows 1114mm apart, 19/55/169/301/431/
625mm forward of the heel). Across the van they are placed symmetric about the midline of the two parallel chassis
members (owner, 19/11/2026): inner walls measured at X -375 and +375 at Z -100..50, 100..250 and 350..600, so the
midline is X = 0 and the rows are X -557 / +557. Fore-aft they are placed from the seat bolt ends found in the
full-resolution scan; the scanned bolt ends go in as separate markers so the difference stays visible.

usage: add_fixings.py closed.step out_prefix
"""
import sys, re, os, zipfile, json, numpy as np
from OCP.STEPCAFControl import STEPCAFControl_Writer
from OCP.STEPControl import STEPControl_AsIs
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.XCAFApp import XCAFApp_Application
from OCP.XCAFDoc import XCAFDoc_DocumentTool, XCAFDoc_ColorType
from OCP.TDataStd import TDataStd_Name
from OCP.Quantity import Quantity_Color, Quantity_TypeOfColor
from OCP.Interface import Interface_Static
from OCP.IFSelect import IFSelect_RetDone
from OCP.gp import gp_Pnt, gp_Ax2, gp_Dir
from OCP.BRepPrimAPI import BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeSphere
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCP.BRep import BRep_Builder
from OCP.TopoDS import TopoDS_Compound

base, out = sys.argv[1], sys.argv[2]
# measured seat bolt ends (level frame): X, Z, lowest Y, and the pattern fixing each one belongs to
bolts = [(-560.7, 29.0, -22.7, 19), (561.1, 29.8, -21.3, 19), (560.7, 67.1, -22.2, 55), (-556.1, 305.1, -88.7, 301), (556.3, 319.1, -85.8, 301)]
heel = float(np.mean([z - d for x, z, y, d in bolts]))
xc_bolts = float(np.mean([(-560.7 + 561.1) / 2, (-556.1 + 556.3) / 2]))
XC = 0.0            # midline of the two parallel chassis members
INNER = 375.0       # member inner walls at XC -/+ 375
HALF = 557.0        # half the 1114mm row spacing of the seat model
fix_from_heel = [19, 55, 169, 301, 431, 625]
Y_TOP, Y_BOT = 40.0, -120.0          # each fixing shown from 40mm above to 120mm below the floor-panel underside datum
print('heel Z from bolt ends %.1f mm (spread %.1f..%.1f); bolt-end centre X %.2f mm; rows at member midline X %.1f -/+ %.1f' % (
    heel, min(z - d for x, z, y, d in bolts), max(z - d for x, z, y, d in bolts), xc_bolts, XC, HALF))

app = XCAFApp_Application.GetApplication_s()
doc = TDocStd_Document(TCollection_ExtendedString('MDTV-XCAF')); app.InitDocument(doc)
st = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main()); ct = XCAFDoc_DocumentTool.ColorTool_s(doc.Main())


def add(shape, name, rgb):
    lab = st.AddShape(shape, False)
    TDataStd_Name.Set_s(lab, TCollection_ExtendedString(name))
    col = Quantity_Color(rgb[0], rgb[1], rgb[2], Quantity_TypeOfColor.Quantity_TOC_RGB)
    ct.SetColor(lab, col, XCAFDoc_ColorType.XCAFDoc_ColorSurf); ct.SetColor(lab, col, XCAFDoc_ColorType.XCAFDoc_ColorCurv)


rows = {'-X (exhaust side)': XC - HALF, '+X': XC + HALF}
table = []
for side, x in rows.items():
    for k, d in enumerate(fix_from_heel, start=1):
        z = heel + d
        cyl = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x, Y_BOT, z), gp_Dir(0, 1, 0)), 6.25, Y_TOP - Y_BOT).Shape()
        add(cyl, 'Seat fixing %s %d (%dmm from heel) - hole 12.5' % (side, k, d), (0.85, 0.10, 0.10))
        table.append((side, k, d, round(x, 1), round(z, 1)))
B = BRep_Builder(); axes = TopoDS_Compound(); B.MakeCompound(axes)
for side, k, d, x, z in table:
    B.Add(axes, BRepBuilderAPI_MakeEdge(gp_Pnt(x, Y_TOP + 60, z), gp_Pnt(x, Y_BOT - 60, z)).Edge())
add(axes, 'Seat fixing axes (12)', (0.85, 0.10, 0.10))
marks = TopoDS_Compound(); B.MakeCompound(marks)
for x, z, y, d in bolts:
    B.Add(marks, BRepPrimAPI_MakeSphere(gp_Pnt(x, y + 8.0, z), 8.0).Shape())
add(marks, 'Seat bolt ends as scanned (5)', (0.80, 0.20, 0.80))
walls = TopoDS_Compound(); B.MakeCompound(walls)
for x in (XC - INNER, XC + INNER):
    B.Add(walls, BRepBuilderAPI_MakeEdge(gp_Pnt(x, 0.0, -100.0), gp_Pnt(x, 0.0, 650.0)).Edge())
add(walls, 'Chassis member inner walls X -375 / +375 (midline X 0)', (0.10, 0.45, 0.85))

Interface_Static.SetCVal_s('write.step.unit', 'MM'); Interface_Static.SetCVal_s('write.step.schema', 'AP214IS')
w = STEPCAFControl_Writer(); w.SetColorMode(True); w.SetNameMode(True)
w.Transfer(doc, STEPControl_AsIs)
add_path = out + '_fixings_only.step'
assert w.Write(add_path) == IFSelect_RetDone

TOK = re.compile(r"'(?:[^']|'')*'|#(\d+)")       # a quoted string (left alone) or an entity reference
TAIL = b'\nENDSEC;\nEND-ISO-10303-21;\n'


def entities(text):
    """DATA-section entities of an Open CASCADE STEP file, in file order, as (id, text)."""
    data = text.split('\nDATA;\n', 1)[1].rsplit('\nENDSEC;', 1)[0]
    ents = []
    for line in data.split('\n'):
        m = re.match(r'#(\d+) = ', line)
        if m:
            ents.append([int(m.group(1)), [line]])
        else:
            ents[-1][1].append(line)
    return [(i, '\n'.join(lines)) for i, lines in ents]


def schema(text):
    return re.search(r"FILE_SCHEMA\(\(('[^']*')\)\)", text).group(1)


Bt = open(base, 'rb').read()
assert Bt.endswith(TAIL), 'unexpected end of the base file'
At = open(add_path).read()
assert schema(At) == schema(Bt[:4000].decode()), 'schemas differ'
ctx_base = int(re.search(rb'\n#(\d+) = APPLICATION_CONTEXT\(', Bt[:20000]).group(1))
off = max(int(v) for v in re.findall(rb'\n#(\d+) = ', Bt))
ents = entities(At)
kind = {i: t.split(' = ', 1)[1].split('(', 1)[0] for i, t in ents}
apd = [i for i in kind if kind[i] == 'APPLICATION_PROTOCOL_DEFINITION']; ctx = [i for i in kind if kind[i] == 'APPLICATION_CONTEXT']
assert len(apd) == 1 and len(ctx) == 1
keep = [(i, t) for i, t in ents if i not in (apd[0], ctx[0])]
new_ids = {i + off for i, _ in keep}


def ren(t):
    return TOK.sub(lambda m: m.group(0) if m.group(1) is None else '#%d' % (ctx_base if int(m.group(1)) == ctx[0] else int(m.group(1)) + off), t)


body = '\n'.join(ren(t) for i, t in keep)
refs = {int(v) for v in re.findall(r'#(\d+)', re.sub(r"'(?:[^']|'')*'", "''", body))}
assert refs <= new_ids | {ctx_base}, 'dangling references: %s' % sorted(refs - new_ids - {ctx_base})[:10]
with open(out + '.step', 'wb') as f:
    f.write(Bt[:-len(TAIL)]); f.write(b'\n'); f.write(body.encode('ascii')); f.write(TAIL)
print('appended %d entities (#%d..#%d) after #%d; base kept byte-for-byte (%d bytes)' % (len(keep), min(new_ids), max(new_ids), off, len(Bt) - len(TAIL)))
with zipfile.ZipFile(out + '.zip', 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    z.write(out + '.step', os.path.basename(out) + '.step')
json.dump(dict(heel_z=heel, member_midline_x=XC, member_inner_walls_x=[XC - INNER, XC + INNER], row_half_spacing=HALF,
               bolt_end_centre_x=xc_bolts, fixings=table, bolt_ends=bolts), open(out + '_fixings.json', 'w'), indent=1)
print('fixing table (side, n, mm from heel, X, Z):')
for t in table:
    print('  ', t)
print('step %.1f MB, zip %.1f MB' % (os.path.getsize(out + '.step') / 1e6, os.path.getsize(out + '.zip') / 1e6))
