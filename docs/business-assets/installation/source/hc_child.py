"""Silhouette of the owner's child figure (3DHumanModel NL Kima 1993, child 8-9 years, P95, sitting) as placed in
the SolidWorks assembly, projected to the side view in mm (x from ski heel, y above floor)."""
import sys, json
sys.path.insert(0, sys.argv[1])
from cad_lib import *
from OCP.TopAbs import TopAbs_FACE
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.BRep import BRep_Tool
from OCP.TopLoc import TopLoc_Location
from OCP.TopoDS import TopoDS
from OCP.TopExp import TopExp_Explorer
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
T = json.load(open('tree.json'))
o = [x for x in T if x['type'] == 'PART' and 'Human' in x['name']][0]
s = load(o['brep']); BRepMesh_IncrementalMesh(s, 1.0, False, 0.5, True)
tris = []
ex = TopExp_Explorer(s, TopAbs_FACE)
while ex.More():
    f = TopoDS.Face_s(ex.Current()); ex.Next()
    loc = TopLoc_Location(); tr = BRep_Tool.Triangulation_s(f, loc)
    if tr is None: continue
    Tm = loc.Transformation(); pts = [tr.Node(i).Transformed(Tm) for i in range(1, tr.NbNodes() + 1)]
    for k in range(1, tr.NbTriangles() + 1):
        a, b, c = tr.Triangle(k).Get()
        p = Polygon([(-(pts[i-1].Z() + 91), pts[i-1].Y() + 485) for i in (a, b, c)])
        if p.area > 1e-3: tris.append(p)
g = unary_union([t.buffer(0.3) for t in tris]).buffer(4, join_style=1).buffer(-4, join_style=1).simplify(1.0)
gs = sorted(list(g.geoms) if isinstance(g, MultiPolygon) else [g], key=lambda p: -p.area)
main = gs[0]
d = 'M' + ' L'.join('%.1f %.1f' % c for c in list(main.exterior.coords)[:-1]) + ' Z'
j = json.load(open(sys.argv[2]))
j['child'] = d; j['child_head_top'] = round(main.bounds[3])
j['child_note'] = "owner's model figure: 3DHumanModel NL Kima 1993, child 8-9 years, P95, sitting (as placed in the assembly)"
json.dump(j, open(sys.argv[2], 'w'))
print('triangles', len(tris), 'parts', len(gs), 'bounds', [round(v) for v in main.bounds], 'chars', len(d))
