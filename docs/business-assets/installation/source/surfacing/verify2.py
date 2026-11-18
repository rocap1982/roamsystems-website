import numpy as np, trimesh
from scipy.spatial import cKDTree
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE
from OCP.TopoDS import TopoDS
from OCP.BRep import BRep_Tool
from OCP.TopLoc import TopLoc_Location


def tessellate(shape, defl=0.05, ang=0.2):
    BRepMesh_IncrementalMesh(shape, defl, False, ang, True)
    V, F = [], []
    nv = 0
    ex = TopExp_Explorer(shape, TopAbs_FACE)
    bad = 0
    while ex.More():
        f = TopoDS.Face_s(ex.Current())
        loc = TopLoc_Location()
        t = BRep_Tool.Triangulation_s(f, loc)
        if t is None:
            bad += 1
        else:
            tr = loc.Transformation()
            n = t.NbNodes()
            P = np.empty((n, 3))
            for i in range(1, n + 1):
                p = t.Node(i).Transformed(tr)
                P[i - 1] = (p.X(), p.Y(), p.Z())
            T = np.empty((t.NbTriangles(), 3), int)
            for i in range(1, t.NbTriangles() + 1):
                T[i - 1] = t.Triangle(i).Get()
            V.append(P); F.append(T - 1 + nv); nv += n
        ex.Next()
    return trimesh.Trimesh(np.vstack(V), np.vstack(F), process=False), bad


def one_way(a, b, n, seed):
    """distances from points sampled on mesh a to surface of mesh b"""
    p, _ = trimesh.sample.sample_surface(a, n, seed=seed)
    p = np.vstack([p, a.vertices])
    sb, _ = trimesh.sample.sample_surface(b, max(4 * n, 2000000), seed=seed + 1)
    d, _ = cKDTree(np.vstack([sb, b.vertices])).query(p, workers=-1)
    f = d > 0.5
    if f.any():
        _, dd, _ = trimesh.proximity.closest_point(b, p[f])
        d[f] = dd
    return p, d


def report(name, d):
    return '%s: n=%d median %.3f p99 %.3f p99.9 %.3f max %.3f mm; over 1mm %d, over 2mm %d' % (
        name, len(d), np.median(d), np.percentile(d, 99), np.percentile(d, 99.9), d.max(), (d > 1).sum(), (d > 2).sum())
