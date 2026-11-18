"""Close the holes in the scanned underside with inferred surface, by physical reasoning.

Plan-view (lowest surface) map at 2mm in the corrected frame (X = 0 on the fitted mirror plane).
A cell is 'scanned' if any scanned surface passes through its column (vertical walls included).

Pass 1 - mirror: a hole cell is filled from the mirrored side when that side was scanned there and the
  surface around the cell (within ~60mm) is symmetric: scanned points there lie on average within 2mm of the
  mirrored scan. Next to an asymmetric part (the exhaust, a bracket) the two sides disagree, so nothing is
  copied across there. Each mirrored patch is blended to meet its scanned border (harmonic correction).
Pass 2 - on what is still open, using scanned and mirrored surface as the surroundings:
  - a compact round hole with a flat rim (6-80mm) is taken to be a real hole in the panel and left open;
  - a slit no wider than 12mm is bridged across its width;
  - otherwise the section is continued across the gap along the direction the surface runs, if the
    sections at the two ends match (straight members, crossmembers and ribs);
  - otherwise a small hole in a smooth panel is closed with a membrane surface;
  - anything else is left open and reported.
"""
import sys, json, numpy as np, trimesh
sys.path.insert(0, sys.argv[1])
from raster import raster_min
from scipy import ndimage
from scipy.spatial import cKDTree
import scipy.sparse as sp
from scipy.sparse.linalg import spsolve

new = trimesh.load(sys.argv[2]); old = trimesh.load(sys.argv[3]); M = np.array(json.load(open(sys.argv[4]))['M']); out = sys.argv[5]
g = 2.0; W = 1000.0
x0, z0 = -W, -320.0
nx = int(2 * W / g); nz = int((1300 - z0) / g)


def tf(v):
    return v @ M[:3, :3].T + M[:3, 3]


Hn = raster_min(tf(new.vertices), new.faces, x0, z0, g, (nz, nx))
Ho = raster_min(tf(old.vertices), old.faces, x0, z0, g, (nz, nx), maxcell=80)
H = np.fmin(Hn, Ho)
cov_h = np.isfinite(H)
hit = np.zeros(H.shape, bool)
pts = []
for m_, n_ in ((new, 6000000), (old, 3000000)):
    p_, _ = trimesh.sample.sample_surface(m_, n_, seed=11); q_ = tf(p_); pts.append(q_)
    ii_ = ((q_[:, 0] - x0) / g).astype(int); jj_ = ((q_[:, 2] - z0) / g).astype(int)
    ok_ = (ii_ >= 0) & (ii_ < nx) & (jj_ >= 0) & (jj_ < nz); hit[jj_[ok_], ii_[ok_]] = True
cov = cov_h | hit
region = ndimage.binary_fill_holes(ndimage.binary_closing(cov, structure=np.ones((7, 7))))
holes0 = region & ~cov
print('plan cells scanned: %d (%d with a lowest surface, %d wall-only); holes %.0f cm2' % (cov.sum(), cov_h.sum(), (cov & ~cov_h).sum(), holes0.sum() * g * g / 100))

# ---- symmetry agreement map: how far each scanned cell's surface point is from the mirrored scan
P = np.vstack(pts)
refl = cKDTree(P[::3] * [-1, 1, 1])
Hm = H[:, ::-1]                                     # mirrored lowest surface (NaN where the other side has none)
jj, ii = np.nonzero(cov_h & np.isfinite(Hm))
Q = np.c_[x0 + (ii + 0.5) * g, H[jj, ii], z0 + (jj + 0.5) * g]
d3, _ = refl.query(Q, distance_upper_bound=10.0, workers=-1)
d3 = np.where(np.isfinite(d3), d3, 10.0)
D3 = np.full(H.shape, np.nan); D3[jj, ii] = d3
valid = np.isfinite(D3).astype(float)
win = 31
num = ndimage.uniform_filter(np.nan_to_num(np.minimum(D3, 10.0)), win); den = ndimage.uniform_filter(valid, win)
A = np.where(den > 0, num / np.maximum(den, 1e-9), np.nan)        # local mean distance (clipped at 10mm)
print('symmetry where both sides scanned: median %.2f mm, 75%% %.2f mm' % (np.median(d3), np.percentile(d3, 75)))
lo_loc = ndimage.minimum_filter(np.where(cov_h, H, 1e9), win); hi_loc = ndimage.maximum_filter(np.where(cov_h, H, -1e9), win)


def harmonic(mask, fixed):
    """Laplace on mask cells; neighbours outside the mask take 'fixed' (NaN = ignored)"""
    cells = np.argwhere(mask)
    if len(cells) == 0:
        return np.full(mask.shape, np.nan)
    idx = -np.ones(mask.shape, int); idx[mask] = np.arange(len(cells))
    rows, cols, vals = [], [], []; b = np.zeros(len(cells)); deg = np.zeros(len(cells)); nfix = np.zeros(len(cells))
    for dj, di in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        j2 = cells[:, 0] + dj; i2 = cells[:, 1] + di
        inb = (j2 >= 0) & (j2 < mask.shape[0]) & (i2 >= 0) & (i2 < mask.shape[1])
        k = np.nonzero(inb)[0]; j2, i2 = j2[inb], i2[inb]
        inm = mask[j2, i2]
        rows += list(k[inm]); cols += list(idx[j2[inm], i2[inm]]); vals += [-1.0] * int(inm.sum()); np.add.at(deg, k[inm], 1)
        fv = fixed[j2[~inm], i2[~inm]]; fk = k[~inm]; okf = np.isfinite(fv)
        np.add.at(b, fk[okf], fv[okf]); np.add.at(deg, fk[okf], 1); np.add.at(nfix, fk[okf], 1)
    rows += list(range(len(cells))); cols += list(range(len(cells))); vals += list(np.maximum(deg, 1) + 1e-9)
    Am = sp.csr_matrix((vals, (rows, cols)), shape=(len(cells), len(cells)))
    o = np.full(mask.shape, np.nan)
    if nfix.sum() == 0:
        return o
    o[mask] = spsolve(Am, b)
    return o


F = np.full(H.shape, np.nan)
method = np.zeros(H.shape, np.int8)       # 1 mirrored, 2 section continued, 3 bridged/smooth/speck
report = []

# ---- per hole: real hole? mirror? bridge? section? smooth? best guess
HK = np.where(cov_h, H, np.nan)
def process(mask, known_map, do_mirror, do_rest, tag):
    lab, nl = ndimage.label(mask, structure=np.ones((3, 3)))
    for h, sl in enumerate(ndimage.find_objects(lab), start=1):
        pad = 6
        sj = slice(max(sl[0].start - pad, 0), min(sl[0].stop + pad, nz)); si = slice(max(sl[1].start - pad, 0), min(sl[1].stop + pad, nx))
        hm = lab[sj, si] == h
        Kl = known_map[sj, si]; Hml = Hm[sj, si].copy()
        ring = ndimage.binary_dilation(hm, iterations=3) & ~hm & np.isfinite(Kl)
        area = hm.sum() * g * g
        width = 2 * ndimage.distance_transform_edt(hm).max() * g
        rec = dict(area_mm2=float(area), width_mm=float(width),
                   centre_x=float(x0 + (np.nonzero(hm)[1].mean() + si.start + 0.5) * g), centre_z=float(z0 + (np.nonzero(hm)[0].mean() + sj.start + 0.5) * g))
        rv = Kl[ring]
        if len(rv) < 3:
            rec['result'] = 'open: no border'; rec['stage'] = tag; report.append(rec) if do_rest else None; continue
        jr, ir = np.nonzero(ring)
        X = np.c_[np.ones(len(jr)), ir, jr, ir * ir, ir * jr, jr * jr].astype(float)
        coef, *_ = np.linalg.lstsq(X, rv, rcond=None); smooth_p90 = float(np.percentile(np.abs(X @ coef - rv), 90))
        rec['border_smooth_p90'] = smooth_p90
        compact = area <= 1.6 * np.pi * (width / 2) ** 2
        deq = 2 * np.sqrt(area / np.pi)
        if compact and 6 <= deq <= 80 and smooth_p90 <= 1.5 and area > 24 and not np.isfinite(Hml[hm]).mean() > 0.9:
            rec['result'] = 'open: probable real hole in the panel'; rec['stage'] = tag; report.append(rec) if do_rest else None; continue
        done = False
        # mirror: border agreement in 3D, nothing out of the border's height range brought in
        Pr = np.c_[x0 + (ir + si.start + 0.5) * g, rv, z0 + (jr + sj.start + 0.5) * g]
        d3r, _ = refl.query(Pr, distance_upper_bound=10.0)
        near = np.isfinite(d3r)
        mcov = np.isfinite(Hml[hm]).mean()
        if do_mirror and near.mean() >= 0.6 and mcov >= 0.6:
            med, p90 = float(np.median(d3r[near])), float(np.percentile(d3r[near], 90))
            inner = Hml[hm][np.isfinite(Hml[hm])]
            lo_, hi_ = np.percentile(inner, [2, 98])
            guard = lo_ >= rv.min() - 10 and hi_ <= rv.max() + 10
            rec.update(mirror_border_median=med, mirror_border_p90=p90, mirror_cover=float(mcov), mirror_range_ok=bool(guard))
            if med <= 3.0 and p90 <= 7.0 and guard:
                spike = hm & np.isfinite(Hml) & ((Hml < rv.min() - 10) | (Hml > rv.max() + 10)); Hml[spike] = np.nan
                D = np.where(ring & np.isfinite(Hml), Kl - Hml, np.nan); D[np.abs(D) > 4] = np.nan
                C = harmonic(hm, D); C[~np.isfinite(C)] = 0
                fill = Hml + C
                miss = hm & ~np.isfinite(fill)
                rest_w = 2 * ndimage.distance_transform_edt(miss).max() * g if miss.any() else 0
                if rest_w <= 40:
                    if miss.any():
                        fx = np.where(hm & np.isfinite(fill), fill, Kl); f2 = harmonic(miss, fx); fill[miss] = f2[miss]
                    if np.isfinite(fill[hm]).all():
                        F[sj, si][hm] = fill[hm]; method[sj, si][hm] = 1
                        rec['result'] = 'mirrored (border agreement median %.1fmm)' % med; done = True
        if not do_rest:
            if done:
                rec['stage'] = tag; report.append(rec)
            continue
        def loft(ax_):
            """continue the surface across the hole along one axis. Returns the straight join between the two ends
            ('join') and, for a best guess, the face extended from whichever end is steadiest across the hole"""
            Lm = hm if ax_ == 0 else hm.T; Kx = Kl if ax_ == 0 else Kl.T
            runs_ = []
            for k in range(Lm.shape[1]):
                if not Lm[:, k].any():
                    continue
                idx = np.nonzero(Lm[:, k])[0]
                for r_ in np.split(idx, np.nonzero(np.diff(idx) > 1)[0] + 1):
                    a_, b_ = r_[0] - 1, r_[-1] + 1
                    for _s in range(4):
                        if a_ > 0 and not np.isfinite(Kx[a_, k]): a_ -= 1
                        if b_ < Lm.shape[0] - 1 and not np.isfinite(Kx[b_, k]): b_ += 1
                    va = Kx[a_, k] if a_ >= 0 and np.isfinite(Kx[a_, k]) else np.nan
                    vb = Kx[b_, k] if b_ < Lm.shape[0] and np.isfinite(Kx[b_, k]) else np.nan
                    runs_.append((k, r_[0], r_[-1], a_, b_, va, vb))
            if len(runs_) < 3:
                return None
            R_ = np.array(runs_, float)
            def build(mode):
                fill = np.full(Lm.shape, np.nan)
                for k, r0, r1, a_, b_, va, vb in runs_:
                    rng_ = np.arange(r0, r1 + 1)
                    if mode == 'join':
                        if not (np.isfinite(va) and np.isfinite(vb)):
                            continue
                        tt = (rng_ - a_) / (b_ - a_); fill[rng_, k] = va * (1 - tt) + vb * tt
                    elif mode == 'a' and 5 in trend:
                        fill[rng_, k] = trend[5][0] + trend[5][1] * k
                    elif mode == 'b' and 6 in trend:
                        fill[rng_, k] = trend[6][0] + trend[6][1] * k
                fill = fill if ax_ == 0 else fill.T
                if np.isfinite(fill[hm]).mean() < 0.8:
                    return None
                miss = hm & ~np.isfinite(fill)
                if miss.any():
                    fx = np.where(hm & np.isfinite(fill), fill, Kl); f2 = harmonic(miss, fx); fill[miss] = f2[miss]
                return fill if np.isfinite(fill[hm]).all() else None
            trend = {}
            def steadiness(col):
                """robust straight-line trend of one edge across the hole: p90 of inlier residuals (inf if under 60% inliers)"""
                ok_ = np.isfinite(R_[:, col])
                if ok_.sum() < 3:
                    return np.inf
                kk, vv = R_[ok_, 0], R_[ok_, col]
                inl = np.ones(len(kk), bool)
                for _ in range(3):
                    A_ = np.c_[np.ones(inl.sum()), kk[inl]]; cf, *_ = np.linalg.lstsq(A_, vv[inl], rcond=None)
                    res = np.abs(vv - (cf[0] + cf[1] * kk))
                    inl = res <= max(5.0, np.percentile(res, 50))
                if inl.mean() < 0.6:
                    return np.inf
                trend[col] = cf
                return float(np.percentile(res[inl], 90))
            both = np.isfinite(R_[:, 5]) & np.isfinite(R_[:, 6])
            cons = np.inf
            if both.sum() >= 3:
                e = R_[both, 5] - R_[both, 6]
                A_ = np.c_[np.ones(both.sum()), R_[both, 0]]; cf, *_ = np.linalg.lstsq(A_, e, rcond=None)
                cons = float(np.percentile(np.abs(e - A_ @ cf), 90))
            sa, sb = steadiness(5), steadiness(6)
            span = float(np.mean(R_[both, 4] - R_[both, 3]) * g) if both.any() else 0.0
            axn = 'Z' if ax_ == 0 else 'X'
            names = {0: ('rear', 'front'), 1: ('-X side', '+X side')}[ax_]
            return dict(axis=axn, cons=cons, span=span, join=build('join'), steady_a=sa, steady_b=sb,
                        ext_a=build('a') if np.isfinite(sa) else None, ext_b=build('b') if np.isfinite(sb) else None, name_a=names[0], name_b=names[1])
        lofts = [l_ for l_ in (loft(0), loft(1)) if l_ is not None]
        rec['loft_debug'] = [dict(axis=l_['axis'], join_ok=l_['join'] is not None, cons=l_['cons'] if np.isfinite(l_['cons']) else None,
                                  steady_a=l_['steady_a'] if np.isfinite(l_['steady_a']) else None, ext_a=l_['ext_a'] is not None,
                                  steady_b=l_['steady_b'] if np.isfinite(l_['steady_b']) else None, ext_b=l_['ext_b'] is not None) for l_ in lofts]
        good = [l_ for l_ in lofts if l_['join'] is not None and l_['cons'] <= 2.5]
        if good:
            pick = max(good, key=lambda l_: l_['span'])          # both match: continue along the hole's length
            rec.update(section_axis=pick['axis'], section_match_p90=pick['cons'], section_span_mm=pick['span'])
            F[sj, si][hm] = pick['join'][hm]; method[sj, si][hm] = 2 if width > 12 else 3
            rec['result'] = ('section continued along %s (ends match within %.1fmm)' if width > 12 else 'slit closed along %s (ends match within %.1fmm)') % (pick['axis'], pick['cons'])
            done = True
        # best-guess candidate: the face extended from the steadiest edge (a face runs on until it meets what is behind it)
        ext = []
        for l_ in lofts:
            if l_['ext_a'] is not None: ext.append((l_['steady_a'], l_['ext_a'], l_['axis'], l_['name_a']))
            if l_['ext_b'] is not None: ext.append((l_['steady_b'], l_['ext_b'], l_['axis'], l_['name_b']))
        loft_fill = min(ext, key=lambda e_: e_[0]) if ext else None
        if not done and (width <= 12 or area <= 24):
            fill = harmonic(hm, Kl)
            if np.isfinite(fill[hm]).all():
                F[sj, si][hm] = fill[hm]; method[sj, si][hm] = 3
                rec['result'] = 'slit bridged' if area > 24 else 'speck'; done = True
        if not done and smooth_p90 <= 2.0 and width <= 60:
            fill = harmonic(hm, Kl)
            if np.isfinite(fill[hm]).all():
                F[sj, si][hm] = fill[hm]; method[sj, si][hm] = 3
                rec['result'] = 'smooth panel continued'; done = True
        if not done:
            if loft_fill is not None and loft_fill[0] <= 6.0:
                F[sj, si][hm] = loft_fill[1][hm]; method[sj, si][hm] = 4
                rec.update(extend_axis=loft_fill[2], extend_from=loft_fill[3], edge_steadiness_p90=loft_fill[0])
                rec['result'] = 'best guess: face extended from its %s edge (edge steady within %.1fmm) to meet the other side' % (loft_fill[3], loft_fill[0]); done = True
            else:
                fill = harmonic(hm, Kl)
                if np.isfinite(fill[hm]).all():
                    F[sj, si][hm] = fill[hm]; method[sj, si][hm] = 4
                    rec['result'] = 'best guess: smooth surface from the edges'; done = True
        if not done:
            rec['result'] = 'open'
        rec['stage'] = tag; report.append(rec)



# stage 1: whole holes mirrored where the border agrees
process(holes0, HK, True, False, 'mirror whole hole')
# stage 2: in what is left (nothing was scanned there, so nothing hangs there), mirror single cells where the
# surroundings are broadly symmetric (within 5mm on average) and the mirror brings in nothing lower than the scanned surroundings
rest = holes0 & ~np.isfinite(F)
cand = rest & np.isfinite(Hm) & np.isfinite(A) & (A <= 5.0) & (den >= 0.3) & (Hm >= lo_loc - 3) & (Hm <= hi_loc + 10)
labc, _ = ndimage.label(cand, structure=np.ones((3, 3)))
known1 = np.where(cov_h, H, F)
ncell = 0
for h, sl in enumerate(ndimage.find_objects(labc), start=1):
    pad = 6
    sj = slice(max(sl[0].start - pad, 0), min(sl[0].stop + pad, nz)); si = slice(max(sl[1].start - pad, 0), min(sl[1].stop + pad, nx))
    hm = labc[sj, si] == h
    if hm.sum() < 6:
        continue
    ring = ndimage.binary_dilation(hm, iterations=3) & ~hm & np.isfinite(known1[sj, si])
    D = np.where(ring & np.isfinite(Hm[sj, si]), known1[sj, si] - Hm[sj, si], np.nan); D[np.abs(D) > 4] = np.nan
    C = harmonic(hm, D); C[~np.isfinite(C)] = 0
    F[sj, si][hm] = (Hm[sj, si] + C)[hm]; method[sj, si][hm] = 1; ncell += hm.sum()
print('stage 2 mirrored cells: %.0f cm2' % (ncell * g * g / 100))
# stage 3: everything still open, with scanned + mirrored surface as the surroundings
known2 = np.where(cov_h, H, F)
process(holes0 & ~np.isfinite(F), known2, False, True, 'continue')
filled = np.isfinite(F)
tot = holes0.sum() * g * g
for k, nm in ((1, 'mirrored'), (2, 'section continued'), (3, 'bridged/smooth/speck'), (4, 'best guess')):
    print('%-22s %7.0f cm2 (%.0f%% of hole area)' % (nm, (method == k).sum() * g * g / 100, 100 * (method == k).sum() * g * g / tot))
op = holes0 & ~filled
print('%-22s %7.0f cm2 (%.0f%%), of which probable real holes %.0f cm2' % ('left open', op.sum() * g * g / 100, 100 * op.sum() * g * g / tot,
      sum(r['area_mm2'] for r in report if r['result'].startswith('open: probable')) / 100))
json.dump(report, open(out + '_report.json', 'w'), indent=1)
np.savez_compressed(out + '_grid.npz', H=H, F=F, method=method, holes=holes0, x0=x0, z0=z0, g=g)


Minv = np.linalg.inv(M)


def save_vanframe(mesh, name):
    mv = mesh.copy(); mv.vertices = mv.vertices @ Minv[:3, :3].T + Minv[:3, 3]
    mv.export(out + '_infill_%s_vanframe.stl' % name)


def build_heightfield_mesh(cls_name, cls_mask):
    """continued / best-guess infill: its cells, plus scanned neighbour cells only where they continue the same
    surface (within 4mm), so the infill never drops a curtain down to whatever hangs below"""
    Zs = np.where(np.isfinite(F), F, H)
    nb = ndimage.binary_dilation(cls_mask, iterations=1) & ~cls_mask & cov_h
    # nearest infill value for each neighbour cell
    idx = ndimage.distance_transform_edt(~cls_mask, return_distances=False, return_indices=True)
    near_val = Zs[idx[0], idx[1]]
    nb &= np.abs(Zs - near_val) <= 4.0
    use = cls_mask | nb
    vid = -np.ones(H.shape, int); jj, ii = np.nonzero(use); vid[use] = np.arange(len(jj))
    V = np.c_[x0 + (ii + 0.5) * g, Zs[jj, ii], z0 + (jj + 0.5) * g]
    q = use[:-1, :-1] & use[1:, :-1] & use[:-1, 1:] & use[1:, 1:]
    qj, qi = np.nonzero(q)
    a = vid[qj, qi]; b = vid[qj, qi + 1]; c = vid[qj + 1, qi]; d = vid[qj + 1, qi + 1]
    Fc = np.r_[np.c_[a, b, c], np.c_[b, d, c]]
    mesh = trimesh.Trimesh(V, Fc, process=False)
    ok = np.isfinite(mesh.vertices).all(1)
    mesh.update_faces(ok[mesh.faces].all(1)); mesh.remove_unreferenced_vertices()
    print('infill %s: %d triangles, %.0f cm2' % (cls_name, len(mesh.faces), mesh.area / 100))
    save_vanframe(mesh, cls_name)


def build_mirrored_mesh(cls_mask):
    """mirrored infill: the scanned triangles of the other side, reflected in the mirror plane, wherever their plan
    position falls in a mirror-filled cell (walls and undercuts come across exactly as scanned)"""
    keep = ndimage.binary_dilation(cls_mask, iterations=1)
    parts = []
    for m_ in (new, old):
        V = tf(m_.vertices) * [-1, 1, 1]
        Fm = m_.faces[:, ::-1]                       # reflection flips orientation: reverse the winding
        c = V[Fm].mean(1)
        ii = ((c[:, 0] - x0) / g).astype(int); jj = ((c[:, 2] - z0) / g).astype(int)
        inb = (ii >= 0) & (ii < nx) & (jj >= 0) & (jj < nz)
        sel = np.zeros(len(Fm), bool); sel[inb] = keep[jj[inb], ii[inb]]
        if sel.any():
            mm = trimesh.Trimesh(V, Fm[sel], process=False); mm.remove_unreferenced_vertices(); parts.append(mm)
    mesh = trimesh.util.concatenate(parts)
    print('infill mirrored: %d triangles, %.0f cm2 (scanned triangles of the other side)' % (len(mesh.faces), mesh.area / 100))
    save_vanframe(mesh, 'mirrored')


build_mirrored_mesh(method == 1)
build_heightfield_mesh('continued', (method == 2) | (method == 3))
build_heightfield_mesh('bestguess', method == 4)

import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
img = np.ones(H.shape + (3,))
Hs = np.clip((H - np.nanpercentile(H, 2)) / (np.nanpercentile(H, 98) - np.nanpercentile(H, 2)), 0, 1)
img[cov_h] = (0.35 + 0.6 * Hs[cov_h])[:, None] * np.array([0.8, 0.85, 0.9])
img[method == 1] = [0.15, 0.65, 0.30]; img[method == 2] = [0.20, 0.45, 0.85]; img[method == 3] = [0.20, 0.45, 0.85]; img[method == 4] = [0.95, 0.60, 0.10]
img[op] = [0.9, 0.2, 0.2]
fig, ax = plt.subplots(figsize=(13, 11), dpi=110)
ax.imshow(img, origin='lower', extent=[x0, x0 + nx * g, z0, z0 + nz * g]); ax.axvline(0, color='k', lw=0.6)
for r in report:
    if r['result'].startswith('open: probable'):
        ax.plot(r['centre_x'], r['centre_z'], 'o', mfc='none', mec='k', ms=9)
ax.set_xlim(-900, 900); ax.set_ylim(-320, 1260)
ax.set_title('Infill (plan). Green: mirrored from the other side. Blue: continued across the gap.\nAmber: best guess (low confidence). Red: left open (black rings: probable real holes in the panel).')
ax.set_xlabel('X (mm), 0 = fitted mirror plane'); ax.set_ylabel('Z (mm)')
fig.savefig(out + '_infill_plan.png', bbox_inches='tight')
