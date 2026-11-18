import sys, json, numpy as np, trimesh
from scipy.spatial import cKDTree
new = trimesh.load(sys.argv[1]); old = trimesh.load(sys.argv[2]); out = sys.argv[3]
CX, Y0, Z0 = 120.0, 216.1, 166.0
pts = []; nrm = []
for m, n in ((new, 400000), (old, 200000)):
    p, fi = trimesh.sample.sample_surface(m, n, seed=7); pts.append(p + [-CX, Y0, Z0]); nrm.append(m.face_normals[fi])
P = np.vstack(pts); N = np.vstack(nrm)
tree = cKDTree(P)
n = np.array([1.0, 0.0, 0.0]); d = 0.0
def reflect(X, n, d):
    s = X @ n - d
    return X - 2 * s[:, None] * n[None, :]
rng = np.random.default_rng(0)
Q = P[rng.choice(len(P), 120000, replace=False)]
for it in range(40):
    R = reflect(Q, n, d)
    dist, j = tree.query(R)
    thr = 30 if it < 10 else (10 if it < 25 else 4)
    ok = dist < thr
    # point-to-plane residual of reflected points to their matches; linearise in (dn_y, dn_z, dd) with n = (1, ny, nz) normalised
    Pm = P[j[ok]]; Nm = N[j[ok]]; Rq = R[ok]; Qo = Q[ok]
    r0 = ((Rq - Pm) * Nm).sum(1)
    J = np.zeros((ok.sum(), 3)); eps = 1e-4
    base = np.array([n[1] / n[0], n[2] / n[0], d])
    for k in range(3):
        b = base.copy(); b[k] += eps
        nn = np.array([1.0, b[0], b[1]]); nn /= np.linalg.norm(nn)
        J[:, k] = ((((reflect(Qo, nn, b[2]) - Pm) * Nm).sum(1)) - r0) / eps
    step, *_ = np.linalg.lstsq(J, -r0, rcond=None)
    base = base + step
    n = np.array([1.0, base[0], base[1]]); n /= np.linalg.norm(n); d = base[2]
    if it % 10 == 9 or it == 39:
        print('it %d: matched %d, median |r| %.2f mm, p75 %.2f; plane normal (%.5f, %.5f, %.5f) offset %.2f mm -> roll %.2f deg, yaw %.2f deg' % (
            it + 1, ok.sum(), np.median(np.abs(r0)), np.percentile(np.abs(r0), 75), n[0], n[1], n[2], d, np.degrees(np.arcsin(n[1])), np.degrees(np.arcsin(n[2]))))
json.dump(dict(n=n.tolist(), d=float(d)), open(out, 'w'))
