import numpy as np, trimesh, json, sys
from scipy.spatial import cKDTree
scan = trimesh.load(sys.argv[1]); seat = trimesh.load(sys.argv[2])
sp, sfi = trimesh.sample.sample_surface(scan, 1500000, seed=2); sn = scan.face_normals[sfi]
crop = (sp[:, 0] > -900) & (sp[:, 0] < 900) & (sp[:, 1] > -165) & (sp[:, 1] < 1000) & (sp[:, 2] > -260) & (sp[:, 2] < 700)
S = sp[crop]; SN = sn[crop]
mp, mfi = trimesh.sample.sample_surface(seat, 200000, seed=3); mn = seat.face_normals[mfi]
vis = mn[:, 2] < -0.3                                   # rear-facing surfaces of the seat (visible through the doors)
M = mp[vis]; MN = mn[vis]
print('scan points', len(S), ' seat rear-facing points', len(M))
def Rt(T, P): return P @ T[:3, :3].T + T[:3, 3]
T = np.eye(4); T[:3, 3] = [10.0, 300.0, -63.0]
tree = cKDTree(S)
for it in range(80):
    P = Rt(T, M); d, j = tree.query(P)
    thr = 60 if it < 20 else (25 if it < 50 else 12)
    ok = d < thr
    Q = S[j[ok]]; Pk = P[ok]; Nq = SN[j[ok]]
    # point-to-plane step (small-angle linearisation)
    A = np.c_[np.cross(Pk, Nq), Nq]; b = ((Q - Pk) * Nq).sum(1)
    x, *_ = np.linalg.lstsq(A, b, rcond=None)
    w = x[:3]; t = x[3:]
    Rinc = trimesh.transformations.euler_matrix(*w)[:3, :3]
    Tinc = np.eye(4); Tinc[:3, :3] = Rinc; Tinc[:3, 3] = t
    T = Tinc @ T
    if it % 10 == 9 or it == 79:
        r = np.abs(((Q - Pk) * Nq).sum(1))
        print('it %2d  matched %6d  median plane residual %.1f mm  90pct %.1f' % (it + 1, ok.sum(), np.median(r), np.percentile(r, 90)))
ang = np.degrees(trimesh.transformations.euler_from_matrix(T[:3, :3]))
print('rotation (deg about x,y,z): %.2f %.2f %.2f' % tuple(ang)); print('translation', np.round(T[:3, 3], 1))
np.save(sys.argv[3], T)
