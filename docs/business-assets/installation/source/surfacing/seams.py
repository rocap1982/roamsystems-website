"""Close the slits left between faces of the surfaced model.
Works on the model itself (read-back tessellations, model frame) at 1mm: every gap inside the underside's outline
that is not a probable real hole is closed from the surrounding model surface (membrane fill). Gaps up to 12mm wide
are bridged seams; anything wider goes to the best-guess class. Output meshes are appended (van frame) to the infill
meshes used by final_build."""
import sys, json, numpy as np, trimesh
sys.path.insert(0, sys.argv[1])
from raster import raster_min
from scipy import ndimage
import scipy.sparse as sp
from scipy.sparse.linalg import spsolve
pre, inf_pre, M = sys.argv[2], sys.argv[3], np.array(json.load(open(sys.argv[4]))['M'])
g = 1.0; x0, z0 = -1000.0, -320.0; nx, nz = int(2000 / g), int(1620 / g)
H = np.full((nz, nx), np.nan); hit = np.zeros((nz, nx), bool)
for i in range(1, 6):
    m = trimesh.load(pre + '_readback_%d.stl' % i)
    Hc = raster_min(m.vertices, m.faces, x0, z0, g, (nz, nx), maxcell=200)
    H = np.fmin(H, Hc)
    steep = np.abs(m.face_normals[:, 1]) < 0.3
    if steep.any():
        ms = m.submesh([np.nonzero(steep)[0]], append=True)
        p, _ = trimesh.sample.sample_surface(ms, int(ms.area * 4), seed=1)
        ii = ((p[:, 0] - x0) / g).astype(int); jj = ((p[:, 2] - z0) / g).astype(int)
        ok = (ii >= 0) & (ii < nx) & (jj >= 0) & (jj < nz); hit[jj[ok], ii[ok]] = True
covh = np.isfinite(H); cov = covh | hit
region = ndimage.binary_fill_holes(ndimage.binary_closing(cov, structure=np.ones((9, 9))))
gaps = region & ~cov


def harmonic(mask, fixed):
    cells = np.argwhere(mask)
    idx = -np.ones(mask.shape, int); idx[mask] = np.arange(len(cells))
    rows, cols, vals = [], [], []; b = np.zeros(len(cells)); deg = np.zeros(len(cells)); nfix = 0
    for dj, di in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        j2 = cells[:, 0] + dj; i2 = cells[:, 1] + di
        inb = (j2 >= 0) & (j2 < mask.shape[0]) & (i2 >= 0) & (i2 < mask.shape[1])
        k = np.nonzero(inb)[0]; j2, i2 = j2[inb], i2[inb]
        inm = mask[j2, i2]
        rows += list(k[inm]); cols += list(idx[j2[inm], i2[inm]]); vals += [-1.0] * int(inm.sum()); np.add.at(deg, k[inm], 1)
        fv = fixed[j2[~inm], i2[~inm]]; fk = k[~inm]; okf = np.isfinite(fv)
        np.add.at(b, fk[okf], fv[okf]); np.add.at(deg, fk[okf], 1); nfix += okf.sum()
    rows += list(range(len(cells))); cols += list(range(len(cells))); vals += list(np.maximum(deg, 1) + 1e-9)
    o = np.full(mask.shape, np.nan)
    if nfix == 0:
        return o
    o[mask] = spsolve(sp.csr_matrix((vals, (rows, cols)), shape=(len(cells), len(cells))), b)
    return o


F = np.full(H.shape, np.nan); cls = np.zeros(H.shape, np.int8)    # 1 seam, 2 wider gap
lab, n = ndimage.label(gaps, structure=np.ones((3, 3)))
kept_open = []
for k, sl in enumerate(ndimage.find_objects(lab), start=1):
    pad = 4
    sj = slice(max(sl[0].start - pad, 0), min(sl[0].stop + pad, nz)); si = slice(max(sl[1].start - pad, 0), min(sl[1].stop + pad, nx))
    hm = lab[sj, si] == k
    area = hm.sum() * g * g; width = 2 * ndimage.distance_transform_edt(hm).max() * g
    Kl = H[sj, si]
    ring = ndimage.binary_dilation(hm, iterations=2) & ~hm & np.isfinite(Kl)
    if ring.sum() < 3:
        continue
    jr, ir = np.nonzero(ring); rv = Kl[ring]
    X = np.c_[np.ones(len(jr)), ir, jr, ir * ir, ir * jr, jr * jr].astype(float)
    coef, *_ = np.linalg.lstsq(X, rv, rcond=None); smooth = float(np.percentile(np.abs(X @ coef - rv), 90))
    deq = 2 * np.sqrt(area / np.pi)
    if width > 12 and area <= 1.6 * np.pi * (width / 2) ** 2 and 6 <= deq <= 80 and smooth <= 1.5:
        kept_open.append(dict(x=float(x0 + (np.nonzero(hm)[1].mean() + si.start + 0.5) * g), z=float(z0 + (np.nonzero(hm)[0].mean() + sj.start + 0.5) * g), diameter_mm=float(deq)))
        continue
    f = harmonic(hm, Kl)
    if np.isfinite(f[hm]).all():
        F[sj, si][hm] = f[hm]; cls[sj, si][hm] = 1 if width <= 12 else 2
print('model plan region %.0f cm2; gaps %.1f cm2; closed as seams %.1f cm2, wider gaps %.1f cm2; kept open (probable real holes) %d: %s' % (
    region.sum() / 100, gaps.sum() / 100, (cls == 1).sum() / 100, (cls == 2).sum() / 100, len(kept_open), [(round(h['x']), round(h['z']), round(h['diameter_mm'])) for h in kept_open]))
filled = np.isfinite(F)
Minv = np.linalg.inv(M)


def mesh_for(mask):
    Zs = np.where(filled, F, H)
    nb = ndimage.binary_dilation(mask, iterations=1) & ~mask & covh
    idx = ndimage.distance_transform_edt(~mask, return_distances=False, return_indices=True)
    nb &= np.abs(Zs - Zs[idx[0], idx[1]]) <= 4.0
    use = mask | nb
    vid = -np.ones(H.shape, int); jj, ii = np.nonzero(use); vid[use] = np.arange(len(jj))
    V = np.c_[x0 + (ii + 0.5) * g, Zs[jj, ii], z0 + (jj + 0.5) * g]
    q = use[:-1, :-1] & use[1:, :-1] & use[:-1, 1:] & use[1:, 1:]
    qj, qi = np.nonzero(q)
    a = vid[qj, qi]; b = vid[qj, qi + 1]; c = vid[qj + 1, qi]; d = vid[qj + 1, qi + 1]
    m = trimesh.Trimesh(V, np.r_[np.c_[a, b, c], np.c_[b, d, c]], process=False)
    ok = np.isfinite(m.vertices).all(1); m.update_faces(ok[m.faces].all(1)); m.remove_unreferenced_vertices()
    m.vertices = m.vertices @ Minv[:3, :3].T + Minv[:3, 3]
    return m


for c_, name in ((1, 'continued'), (2, 'bestguess')):
    add = mesh_for(cls == c_)
    base = trimesh.load(inf_pre + '_infill_%s_vanframe.stl' % name)
    merged = trimesh.util.concatenate([base, add]) if len(add.faces) else base
    merged.export(inf_pre + '_infill_%s_vanframe.stl' % name)
    print('%s: added %d triangles (%.0f cm2)' % (name, len(add.faces), add.area / 100))
json.dump(dict(kept_open=kept_open), open(inf_pre + '_seams_report.json', 'w'), indent=1)
