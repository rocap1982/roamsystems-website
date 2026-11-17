"""Mesh the visible rear of the ROAM seat from the SolidWorks export (third upload) for registration."""
import sys, json, numpy as np
sys.path.insert(0, sys.argv[1])
from cad_lib import *
from OCP.TopAbs import TopAbs_FACE, TopAbs_SHELL, TopAbs_SOLID
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.BRep import BRep_Tool
from OCP.TopLoc import TopLoc_Location
from OCP.TopoDS import TopoDS
from OCP.TopExp import TopExp_Explorer
import trimesh
T = json.load(open('tree.json'))
names = {'p0012': 'alu back panel', 'p0065': 'drawer panel (rear-facing)', 'p0003': 'rear frame', 'p0014': 'box-section frame', 'p0061': 'cushions'}
V, F, tag = [], [], []
for f, nm in names.items():
    s = load(f + '.brep')
    if f == 'p0003':
        s_list = [sh for sh in sub(s, TopAbs_SHELL) if bb(sh)[1] < 800]
    elif f == 'p0061':
        s_list = [sub(s, TopAbs_SOLID)[i] for i in (4, 5, 6)]
    else:
        s_list = [s]
    for shape in s_list:
        BRepMesh_IncrementalMesh(shape, 1.0, False, 0.5, True)
        ex = TopExp_Explorer(shape, TopAbs_FACE)
        while ex.More():
            fc = TopoDS.Face_s(ex.Current()); ex.Next()
            loc = TopLoc_Location(); tr = BRep_Tool.Triangulation_s(fc, loc)
            if tr is None: continue
            Tm = loc.Transformation(); base = sum(len(v) for v in V)
            pts = np.array([[p.X(), p.Y(), p.Z()] for p in (tr.Node(i).Transformed(Tm) for i in range(1, tr.NbNodes() + 1))])
            tri = np.array([tr.Triangle(k).Get() for k in range(1, tr.NbTriangles() + 1)]) - 1 + base
            V.append(pts); F.append(tri); tag += [f] * len(tri)
m = trimesh.Trimesh(np.vstack(V), np.vstack(F), process=False)
m.export(sys.argv[2]); json.dump(tag, open(sys.argv[2] + '.tags.json', 'w'))
print('seat mesh', len(m.faces), 'faces; bounds', np.round(m.bounds, 0).tolist())
