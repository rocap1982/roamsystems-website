"""Scan mesh -> trimmed B-spline surface model (STEP), error-bounded.

Each scan triangle is given one of six view directions (down, up, +-x, +-z) from its normal.
Per direction, the projection plane is cut into tiles; inside a tile each connected piece of
triangles is a single-valued height field over that plane. It is sampled exactly on a 1mm grid,
fitted with a cubic B-spline (least squares, knot spacing reduced until every sample is within
TOL), and the surface is trimmed to the exact projected outline of its triangles. A piece that
will not fit (fold, overlap, step) is split into smaller tiles; at the smallest tile its scan
triangles are kept as planar facets. Nothing is filled where the scan has no data.
"""
import math
import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
from scipy.sparse.linalg import spsolve
from scipy.interpolate import BSpline
from scipy import ndimage
import shapely
from shapely.geometry import box, Polygon
from shapely.geometry.polygon import orient
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.ShapeFix import ShapeFix_Face

from OCP.gp import gp_Pnt, gp_Pnt2d
from OCP.TColgp import TColgp_Array2OfPnt, TColgp_Array1OfPnt2d
from OCP.TColStd import TColStd_Array1OfReal, TColStd_Array1OfInteger
from OCP.Geom import Geom_BSplineSurface
from OCP.Geom2d import Geom2d_BSplineCurve
from OCP.GeomAbs import GeomAbs_C0
from OCP.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace,
                                BRepBuilderAPI_MakeVertex, BRepBuilderAPI_MakePolygon)
from OCP.BRepLib import BRepLib

# direction -> (axis used for u, axis used for v, axis used for height); u x v points along the view normal
DIRS = {'down': (0, 2, 1), 'up': (2, 0, 1), '+x': (1, 2, 0), '-x': (2, 1, 0), '+z': (0, 1, 2), '-z': (1, 0, 2)}
R = 1.0            # raster node spacing, mm
TILE = 128         # nodes per tile edge
TOL = 0.4          # max fit error at any raster node, mm
TOL_TRI = 0.8      # max error at any triangle vertex / edge midpoint / centroid, mm
MINRECT = 8        # smallest tile edge (nodes) before keeping raw facets
MARGIN = 3         # extra nodes either side of a tile used for fitting
KS = [24.0, 12.0, 8.0, 5.0, 3.5, 2.5, 1.7]
SIMP = 0.3         # outline simplification, mm
CTOL = 0.02        # tolerance of the 3D edge curves, mm
CDEG = 1           # degree of the 3D edge curves


def assign_dirs(n):
    ny = n[:, 1]
    lab = np.empty(len(n), dtype=object)
    wall = np.abs(ny) <= 0.5
    lab[ny < -0.5] = 'down'
    lab[ny > 0.5] = 'up'
    wx = wall & (np.abs(n[:, 0]) >= np.abs(n[:, 2]))
    wz = wall & ~wx
    lab[wx & (n[:, 0] > 0)] = '+x'
    lab[wx & (n[:, 0] <= 0)] = '-x'
    lab[wz & (n[:, 2] > 0)] = '+z'
    lab[wz & (n[:, 2] <= 0)] = '-z'
    return lab


def raster(tu, tv, th, U0, V0, i0, i1, j0, j1):
    """exact min/max height of triangles at node centres u=U0+(i+.5)R, v=V0+(j+.5)R over [i0,i1)x[j0,j1)"""
    Nu, Nv = i1 - i0, j1 - j0
    zmin = np.full((Nv, Nu), np.inf)
    zmax = np.full((Nv, Nu), -np.inf)
    ai = np.maximum(np.floor((tu.min(1) - U0) / R - 0.5).astype(int) + 1, i0)
    bi = np.minimum(np.floor((tu.max(1) - U0) / R - 0.5).astype(int), i1 - 1)
    aj = np.maximum(np.floor((tv.min(1) - V0) / R - 0.5).astype(int) + 1, j0)
    bj = np.minimum(np.floor((tv.max(1) - V0) / R - 0.5).astype(int), j1 - 1)
    w = bi - ai + 1
    h = bj - aj + 1
    e1u, e1v, e1h = tu[:, 1] - tu[:, 0], tv[:, 1] - tv[:, 0], th[:, 1] - th[:, 0]
    e2u, e2v, e2h = tu[:, 2] - tu[:, 0], tv[:, 2] - tv[:, 0], th[:, 2] - th[:, 0]
    det = e1u * e2v - e1v * e2u
    good = (w > 0) & (h > 0) & (np.abs(det) > 1e-12)
    if not good.any():
        return zmin, zmax

    def do(idx, di, dj):
        ii = ai[idx] + di
        jj = aj[idx] + dj
        pu = U0 + (ii + 0.5) * R - tu[idx, 0]
        pv = V0 + (jj + 0.5) * R - tv[idx, 0]
        s = (pu * e2v[idx] - pv * e2u[idx]) / det[idx]
        t = (e1u[idx] * pv - e1v[idx] * pu) / det[idx]
        ins = (s >= -1e-9) & (t >= -1e-9) & (s + t <= 1 + 1e-9)
        z = th[idx, 0] + s * e1h[idx] + t * e2h[idx]
        np.minimum.at(zmin, (jj[ins] - j0, ii[ins] - i0), z[ins])
        np.maximum.at(zmax, (jj[ins] - j0, ii[ins] - i0), z[ins])

    small = good & (w <= 8) & (h <= 8)
    sidx = np.nonzero(small)[0]
    if len(sidx):
        ws, hs = w[sidx], h[sidx]
        for di in range(int(ws.max())):
            for dj in range(int(hs.max())):
                m = sidx[(di < ws) & (dj < hs)]
                if len(m):
                    do(m, di, dj)
    for k in np.nonzero(good & ~small)[0]:
        di, dj = np.meshgrid(np.arange(w[k]), np.arange(h[k]))
        do(np.full(di.size, k), di.ravel(), dj.ravel())
    return zmin, zmax


def clamped_knots(a, b, ks):
    n = max(1, int(round((b - a) / ks)))
    inner = np.linspace(a, b, n + 1)
    t = np.r_[[a] * 3, inner, [b] * 3]
    return t, inner


def fit_patch(Z, cov, chk, u_nodes, v_nodes, ua, ub, va, vb):
    """least-squares cubic B-spline height field; returns (ks, coef(ncv,ncu), tu, tv, inner_u, inner_v, maxerr) or None"""
    idx = ndimage.distance_transform_edt(~cov, return_distances=False, return_indices=True)
    Zf = Z[idx[0], idx[1]]
    wv = np.where(cov, 1.0, 0.01).ravel()
    zf = Zf.ravel()
    best = None
    for ks in KS:
        if ks > 2 * max(ub - ua, vb - va) and ks != KS[-1]:
            continue
        tu, iu = clamped_knots(ua, ub, ks)
        tv, iv = clamped_knots(va, vb, ks)
        Bu = BSpline.design_matrix(u_nodes, tu, 3)
        Bv = BSpline.design_matrix(v_nodes, tv, 3)
        A = sp.kron(Bv, Bu, format='csr')
        AW = A.T.multiply(wv)
        N = (AW @ A).tocsc()
        N = N + sp.identity(N.shape[0], format='csc') * 1e-9
        c = spsolve(N, AW @ zf)
        f = (A @ c).reshape(Z.shape)
        err = np.abs(f - Z)[chk]
        me = float(err.max()) if err.size else 0.0
        best = (ks, c.reshape(len(tv) - 4, len(tu) - 4), tu, tv, iu, iv, me)
        if me <= TOL:
            return best
    return None


def greville(t):
    return np.array([t[i + 1:i + 4].mean() for i in range(len(t) - 4)])


def make_surface(fitres, dname, Y=None):
    ks, C, tu, tv, iu, iv, me = fitres
    du, dv, dh = DIRS[dname]
    gu, gv = greville(tu), greville(tv)
    ncu, ncv = len(gu), len(gv)
    poles = TColgp_Array2OfPnt(1, ncu, 1, ncv)
    p = np.zeros(3)
    for a in range(ncu):
        for b in range(ncv):
            p[du] = gu[a]; p[dv] = gv[b]; p[dh] = C[b, a]
            poles.SetValue(a + 1, b + 1, gp_Pnt(float(p[0]), float(p[1]), float(p[2])))
    uk = TColStd_Array1OfReal(1, len(iu)); um = TColStd_Array1OfInteger(1, len(iu))
    for i, x in enumerate(iu):
        uk.SetValue(i + 1, float(x)); um.SetValue(i + 1, 4 if i in (0, len(iu) - 1) else 1)
    vk = TColStd_Array1OfReal(1, len(iv)); vm = TColStd_Array1OfInteger(1, len(iv))
    for i, x in enumerate(iv):
        vk.SetValue(i + 1, float(x)); vm.SetValue(i + 1, 4 if i in (0, len(iv) - 1) else 1)
    return Geom_BSplineSurface(poles, uk, vk, um, vm, 3, 3), ncu * ncv


def ring_wire(surf, ring):
    P = np.asarray(ring, float)
    n = len(P) - 1
    if n < 3:
        return None
    k = min(n, max(4, int(math.ceil(n / 150))))      # never fewer than 4 edges per loop (2-edge loops break on STEP re-read)
    cuts = np.linspace(0, n, k + 1).astype(int)
    verts = [BRepBuilderAPI_MakeVertex(surf.Value(float(P[c, 0]), float(P[c, 1]))).Vertex() for c in cuts[:-1]]
    verts.append(verts[0])
    mw = BRepBuilderAPI_MakeWire()
    for a in range(k):
        Q = P[cuts[a]:cuts[a + 1] + 1]
        m = len(Q)
        if m < 2:
            return None
        poles = TColgp_Array1OfPnt2d(1, m)
        kn = TColStd_Array1OfReal(1, m); mu = TColStd_Array1OfInteger(1, m)
        for i in range(m):
            poles.SetValue(i + 1, gp_Pnt2d(float(Q[i, 0]), float(Q[i, 1])))
            kn.SetValue(i + 1, float(i)); mu.SetValue(i + 1, 2 if i in (0, m - 1) else 1)
        c2 = Geom2d_BSplineCurve(poles, kn, mu, 1)
        me = BRepBuilderAPI_MakeEdge(c2, surf, verts[a], verts[a + 1], 0.0, float(m - 1))
        if not me.IsDone():
            return None
        mw.Add(me.Edge())
    if not mw.IsDone():
        return None
    return mw.Wire()


def clean_polygons(fp):
    """valid polygons whose holes never touch the outer boundary or each other (OCC rejects touching wires)"""
    out = []
    for g in getattr(fp, 'geoms', [fp]):
        if g.geom_type != 'Polygon' or g.area < 0.3:
            continue
        g = g.simplify(SIMP, preserve_topology=True)
        if g.is_empty or g.geom_type != 'Polygon':
            continue
        stack = [g]
        guard = 0
        while stack:
            q = stack.pop()
            guard += 1
            if guard > 5000:
                return None
            if q.area < 0.3:
                continue
            if not q.is_valid:
                q = shapely.make_valid(q)
                stack.extend([x for x in getattr(q, 'geoms', [q]) if x.geom_type == 'Polygon'])
                continue
            if len(q.interiors) == 0:
                out.append(orient(q, 1.0))
                continue
            # cut through the first hole, along whichever axis the polygon is longer in
            hc = Polygon(q.interiors[0]).representative_point()
            x0, y0, x1, y1 = q.bounds
            if (x1 - x0) >= (y1 - y0):
                halves = (box(x0 - 1, y0 - 1, hc.x, y1 + 1), box(hc.x, y0 - 1, x1 + 1, y1 + 1))
            else:
                halves = (box(x0 - 1, y0 - 1, x1 + 1, hc.y), box(x0 - 1, hc.y, x1 + 1, y1 + 1))
            for hb in halves:
                part = q.intersection(hb)
                stack.extend([x for x in getattr(part, 'geoms', [part]) if x.geom_type == 'Polygon'])
    return out


def trimmed_faces(surf, fp):
    out = []
    polys = clean_polygons(fp)
    if polys is None:
        return None
    for g in polys:
        rings = [list(g.exterior.coords)] + [list(r.coords) for r in g.interiors if len(r.coords) >= 4]
        wires = [ring_wire(surf, r) for r in rings]
        if wires[0] is None or any(w is None for w in wires):
            return None
        mf = BRepBuilderAPI_MakeFace(surf, wires[0], True)
        if not mf.IsDone():
            return None
        for w in wires[1:]:
            mf.Add(w)
        f = mf.Face()
        BRepLib.BuildCurves3d_s(f, CTOL, GeomAbs_C0, CDEG, 10000)
        if not BRepCheck_Analyzer(f).IsValid():
            sf = ShapeFix_Face(f)
            sf.Perform()
            f = sf.Face()
            if not BRepCheck_Analyzer(f).IsValid():
                return None
        out.append(f)
    return out


def facet_face(P):
    mp = BRepBuilderAPI_MakePolygon()
    for p in P:
        mp.Add(gp_Pnt(float(p[0]), float(p[1]), float(p[2])))
    mp.Close()
    if not mp.IsDone():
        return None
    mf = BRepBuilderAPI_MakeFace(mp.Wire(), True)
    return mf.Face() if mf.IsDone() else None


class Surfacer:
    def __init__(self, V, F, normals, adjacency):
        self.V, self.F = V, F
        n = len(F)
        a = adjacency
        self.adj = sp.coo_matrix((np.ones(len(a)), (a[:, 0], a[:, 1])), shape=(n, n)).tocsr()
        self.adj = (self.adj + self.adj.T).tocsr()
        # view direction from area-weighted normals smoothed over ~3 rings of neighbours, so scan noise
        # does not shatter a surface into specks; a triangle keeps its own direction if the smoothed one
        # would fold it (its own normal less than ~84 degrees from that view direction is required)
        area = 0.5 * np.linalg.norm(np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]]), axis=1)
        ns = normals * area[:, None]
        M = self.adj + sp.identity(n, format='csr')
        for _ in range(3):
            ns = M @ ns
        ns /= np.linalg.norm(ns, axis=1)[:, None] + 1e-12
        lab = assign_dirs(ns)
        own = assign_dirs(normals)
        axis = {'down': (1, -1), 'up': (1, 1), '+x': (0, 1), '-x': (0, -1), '+z': (2, 1), '-z': (2, -1)}
        dot = np.array([normals[i, axis[l][0]] * axis[l][1] for i, l in enumerate(lab)])
        bad = dot < 0.1
        lab[bad] = own[bad]
        # merge fragments under 2mm2 into the neighbouring direction (if that does not fold them)
        names = list(DIRS)
        L = np.array([names.index(x) for x in lab])
        ax_i = np.array([axis[nm][0] for nm in names]); ax_s = np.array([axis[nm][1] for nm in names])
        A = self.adj.tocoo()
        for _ in range(4):
            same = L[A.row] == L[A.col]
            G = sp.coo_matrix((np.ones(same.sum()), (A.row[same], A.col[same])), shape=(n, n))
            k, comp = connected_components(G, directed=False)
            carea = np.bincount(comp, weights=area, minlength=k)
            small = carea[comp] < 2.0
            if not small.any():
                break
            # votes of neighbours with a different label, weighted by neighbour area
            diff = L[A.row] != L[A.col]
            rows = A.row[diff]; cols = A.col[diff]
            votes = sp.coo_matrix((area[cols], (rows, L[cols])), shape=(n, len(names))).toarray()
            cand = votes.argmax(1)
            ok = small & (votes.max(1) > 0)
            ok &= normals[np.arange(n), ax_i[cand]] * ax_s[cand] > 0.05
            if not ok.any():
                break
            L[ok] = cand[ok]
        lab = np.array([names[i] for i in L], dtype=object)
        self.lab = lab
        self.relabelled = int((lab != own).sum())
        self.faces = []          # (TopoDS_Face, list of triangle ids represented)
        self.facets = []         # planar pieces of scan triangles kept as facets (3D point loops)
        self.stats = dict(patches=0, poles=0, fit_fail=0, conflict=0, small=0, occ_fail=0, tri_cut=0)

    def components(self, idx):
        if len(idx) == 1:
            return [idx]
        sub = self.adj[idx][:, idx]
        k, lab = connected_components(sub, directed=False)
        order = np.argsort(lab, kind='stable')
        cuts = np.flatnonzero(np.diff(lab[order])) + 1
        return np.split(idx[order], cuts)

    def setup(self, dname):
        du, dv, dh = DIRS[dname]
        sel = np.nonzero(self.lab == dname)[0]
        if len(sel) == 0:
            self.cur = None
            return False
        T = self.V[self.F[sel]]
        tu, tv, th = T[:, :, du], T[:, :, dv], T[:, :, dh]
        self.cur = dict(d=dname, sel=sel, tu=tu, tv=tv, th=th,
                        U0=math.floor(tu.min()) - 4.0, V0=math.floor(tv.min()) - 4.0,
                        umin=tu.min(1), umax=tu.max(1), vmin=tv.min(1), vmax=tv.max(1))
        return True

    def exact_pieces(self, dname, loc, rect):
        """the scan triangles behind one face, clipped to its tile, as 3D point loops"""
        self.setup(dname)
        keep = self.facets
        self.facets = []
        self.to_facets(loc, rect)
        out = self.facets
        self.facets = keep
        return out

    def run_direction(self, dname, progress=None):
        du, dv, dh = DIRS[dname]
        sel = np.nonzero(self.lab == dname)[0]
        if len(sel) == 0:
            return
        T = self.V[self.F[sel]]
        tu, tv, th = T[:, :, du], T[:, :, dv], T[:, :, dh]
        self.cur = dict(d=dname, sel=sel, tu=tu, tv=tv, th=th,
                        U0=math.floor(tu.min()) - 4.0, V0=math.floor(tv.min()) - 4.0,
                        umin=tu.min(1), umax=tu.max(1), vmin=tv.min(1), vmax=tv.max(1))
        c = self.cur
        # tile buckets by bounding-box overlap
        ti0 = np.floor((c['umin'] - c['U0']) / (TILE * R)).astype(int); ti1 = np.floor((c['umax'] - c['U0']) / (TILE * R)).astype(int)
        tj0 = np.floor((c['vmin'] - c['V0']) / (TILE * R)).astype(int); tj1 = np.floor((c['vmax'] - c['V0']) / (TILE * R)).astype(int)
        buckets = {}
        for k in range(len(sel)):
            for a in range(ti0[k], ti1[k] + 1):
                for b in range(tj0[k], tj1[k] + 1):
                    buckets.setdefault((a, b), []).append(k)
        for n_done, ((a, b), ks) in enumerate(sorted(buckets.items())):
            rect = (a * TILE, (a + 1) * TILE, b * TILE, (b + 1) * TILE)   # node index ranges
            for comp in self.components_local(np.array(ks)):
                self.handle(comp, rect)
            if progress:
                progress(dname, n_done + 1, len(buckets))

    def components_local(self, loc):
        gl = self.cur['sel'][loc]
        comps = self.components(gl)
        pos = {g: l for g, l in zip(gl, loc)}
        return [np.array([pos[g] for g in comp]) for comp in comps]

    def overlap(self, loc, rect):
        c = self.cur
        i0, i1, j0, j1 = rect
        ua, ub = c['U0'] + i0 * R, c['U0'] + i1 * R
        va, vb = c['V0'] + j0 * R, c['V0'] + j1 * R
        m = (c['umax'][loc] >= ua) & (c['umin'][loc] <= ub) & (c['vmax'][loc] >= va) & (c['vmin'][loc] <= vb)
        return loc[m]

    def to_facets(self, loc, rect):
        c = self.cur
        i0, i1, j0, j1 = rect
        ua, ub = c['U0'] + i0 * R, c['U0'] + i1 * R
        va, vb = c['V0'] + j0 * R, c['V0'] + j1 * R
        du, dv, dh = DIRS[c['d']]
        bx = box(ua, va, ub, vb)
        for k in loc:
            tu, tv, th = c['tu'][k], c['tv'][k], c['th'][k]
            if tu.min() >= ua and tu.max() <= ub and tv.min() >= va and tv.max() <= vb:
                P2 = np.c_[tu, tv]
            else:
                q = Polygon(np.c_[tu, tv]).intersection(bx)
                if q.is_empty or q.geom_type != 'Polygon' or q.area < 1e-4:
                    continue
                P2 = np.asarray(q.exterior.coords)[:-1]
            # back to 3D on the triangle's own plane
            e1 = np.array([tu[1] - tu[0], tv[1] - tv[0]]); e2 = np.array([tu[2] - tu[0], tv[2] - tv[0]])
            det = e1[0] * e2[1] - e1[1] * e2[0]
            if abs(det) < 1e-12:
                continue
            d = P2 - [tu[0], tv[0]]
            s = (d[:, 0] * e2[1] - d[:, 1] * e2[0]) / det
            t_ = (e1[0] * d[:, 1] - e1[1] * d[:, 0]) / det
            hh = th[0] + s * (th[1] - th[0]) + t_ * (th[2] - th[0])
            P3 = np.zeros((len(P2), 3)); P3[:, du] = P2[:, 0]; P3[:, dv] = P2[:, 1]; P3[:, dh] = hh
            self.facets.append(P3)

    def split(self, loc, rect):
        i0, i1, j0, j1 = rect
        if (i1 - i0) <= MINRECT:
            self.to_facets(loc, rect)
            return
        im, jm = (i0 + i1) // 2, (j0 + j1) // 2
        for r in ((i0, im, j0, jm), (im, i1, j0, jm), (i0, im, jm, j1), (im, i1, jm, j1)):
            sub = self.overlap(loc, r)
            if len(sub):
                for comp in self.components_local(sub):
                    self.handle(comp, r)

    def handle(self, loc, rect):
        c = self.cur
        i0, i1, j0, j1 = rect
        ua, ub = c['U0'] + i0 * R, c['U0'] + i1 * R
        va, vb = c['V0'] + j0 * R, c['V0'] + j1 * R
        polys = shapely.polygons(np.stack([c['tu'][loc], c['tv'][loc]], -1))
        fp = shapely.union_all(polys).intersection(box(ua, va, ub, vb))
        if fp.is_empty:
            return
        if fp.area < 0.3:
            # specks and tile-edge slivers: keep the scan triangles (clipped to this tile) as exact facets
            cu, cv = c['tu'][loc].mean(1), c['tv'][loc].mean(1)
            inside = (cu >= ua) & (cu < ub) & (cv >= va) & (cv < vb)
            if inside.any():             # a real fragment of this tile: keep it exactly
                self.stats['specks'] = self.stats.get('specks', 0) + 1
                self.to_facets(loc[inside], rect)
            else:                        # a hairline poke of a neighbouring tile's triangles: drop
                self.stats['slivers'] = self.stats.get('slivers', 0) + 1
            return
        # fitting domain (node indices)
        ci0 = int(math.floor((c['umin'][loc].min() - c['U0']) / R)); ci1 = int(math.ceil((c['umax'][loc].max() - c['U0']) / R))
        cj0 = int(math.floor((c['vmin'][loc].min() - c['V0']) / R)); cj1 = int(math.ceil((c['vmax'][loc].max() - c['V0']) / R))
        di0, di1 = max(i0 - MARGIN, ci0), min(i1 + MARGIN, ci1)
        dj0, dj1 = max(j0 - MARGIN, cj0), min(j1 + MARGIN, cj1)
        # keep the domain at least 4 nodes wide
        if di1 - di0 < 4:
            di0 -= (4 - (di1 - di0)) // 2 + 1; di1 = di0 + 4 + 1
        if dj1 - dj0 < 4:
            dj0 -= (4 - (dj1 - dj0)) // 2 + 1; dj1 = dj0 + 4 + 1
        zmin, zmax = raster(c['tu'][loc], c['tv'][loc], c['th'][loc], c['U0'], c['V0'], di0, di1, dj0, dj1)
        cov = np.isfinite(zmin)
        ii = np.arange(di0, di1); jj = np.arange(dj0, dj1)
        inrect = ((ii >= i0) & (ii < i1))[None, :] & ((jj >= j0) & (jj < j1))[:, None]
        chk = cov & inrect
        if chk.sum() < 6:
            self.stats['small'] += 1
            self.to_facets(loc, rect)
            return
        if np.any((zmax - zmin)[cov] > 0.3):
            self.stats['conflict'] += 1
            self.split(loc, rect)
            return
        Z = np.where(cov, zmin, 0.0)
        u_nodes = c['U0'] + (ii + 0.5) * R
        v_nodes = c['V0'] + (jj + 0.5) * R
        fr = fit_patch(Z, cov, chk, u_nodes, v_nodes, c['U0'] + di0 * R, c['U0'] + di1 * R, c['V0'] + dj0 * R, c['V0'] + dj1 * R)
        if fr is None:
            self.stats['fit_fail'] += 1
            self.split(loc, rect)
            return
        # check the fitted surface against every triangle (vertices, edge midpoints, centroid) inside the
        # tile; triangles it misses by more than TOL_TRI are cut out of the face and kept as facets
        ks, C, tu, tv, iu, iv, me = fr
        T3u, T3v, T3h = c['tu'][loc], c['tv'][loc], c['th'][loc]
        W = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1], [.5, .5, 0], [0, .5, .5], [.5, 0, .5], [1/3, 1/3, 1/3],
                      [.75, .25, 0], [.25, .75, 0], [0, .75, .25], [0, .25, .75], [.25, 0, .75], [.75, 0, .25],
                      [2/3, 1/6, 1/6], [1/6, 2/3, 1/6], [1/6, 1/6, 2/3]])
        mids = lambda a: a @ W.T
        Pu, Pv, Ph = mids(T3u), mids(T3v), mids(T3h)
        dom = (Pu >= tu[3]) & (Pu <= tu[-4]) & (Pv >= tv[3]) & (Pv <= tv[-4])
        inr = dom & (Pu >= ua) & (Pu <= ub) & (Pv >= va) & (Pv <= vb)
        err = np.zeros(Pu.shape)
        if inr.any():
            pu, pv = Pu[inr], Pv[inr]
            Bu = BSpline.design_matrix(np.clip(pu, tu[3], tu[-4] - 1e-9), tu, 3)
            Bv = BSpline.design_matrix(np.clip(pv, tv[3], tv[-4] - 1e-9), tv, 3)
            BvC = np.asarray(Bv @ C)                                   # (points, ncu)
            val = np.asarray(Bu.multiply(BvC).sum(1)).ravel()          # surface height at each check point
            err[inr] = np.abs(val - Ph[inr])
        badtri = err.max(1) > TOL_TRI
        if badtri.any():
            self.stats['tri_cut'] += int(badtri.sum())
            self.to_facets(loc[badtri], rect)
            good = loc[~badtri]
            if len(good) == 0:
                return
            polys = shapely.polygons(np.stack([c['tu'][good], c['tv'][good]], -1))
            fp = shapely.union_all(polys).intersection(box(ua, va, ub, vb))
            if fp.is_empty or fp.area < 0.3:
                self.to_facets(good, rect)
                return
        surf, npoles = make_surface(fr, c['d'])
        fs = trimmed_faces(surf, fp)
        if not fs:
            self.stats['occ_fail'] += 1
            self.split(loc, rect)
            return
        self.stats['patches'] += 1
        self.stats['poles'] += npoles
        tri_ids = c['sel'][loc]
        for f in fs:
            self.faces.append((f, tri_ids, c['d'], rect, loc.copy()))

    def facet_faces(self):
        out = []
        for P in self.facets:
            f = facet_face(P)
            if f is not None:
                out.append((f, None))
        return out
