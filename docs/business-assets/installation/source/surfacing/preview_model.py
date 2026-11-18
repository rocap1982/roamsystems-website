import sys, numpy as np, trimesh
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
# preview of the surface model (tessellations, scan frame), seen from below and in an oblique view
t1 = trimesh.load(sys.argv[1]); t2 = trimesh.load(sys.argv[2]); out = sys.argv[3]
CX, Y0, Z0 = 120.0, 216.1, 166.0


def draw(ax, meshes, view, up, title, xlim=None, ylim=None, mirror=False):
    v = np.asarray(view, float); v /= np.linalg.norm(v)
    u = np.asarray(up, float); u -= v * (u @ v); u /= np.linalg.norm(u)
    r = np.cross(u, v)
    L = np.array([0.35, -0.8, 0.45]); L /= np.linalg.norm(L)
    allt, allc, alld = [], [], []
    for m, base in meshes:
        P = m.vertices
        T = P[m.faces]
        X = T @ (-r if mirror else r); Y = T @ u; D = (T @ v).mean(1)
        n = m.face_normals
        sh = np.clip(np.abs(n @ L), 0, 1) * 0.75 + 0.2
        allt.append(np.stack([X, Y], -1)); allc.append(np.asarray(base)[None, :] * sh[:, None]); alld.append(D)
    T = np.concatenate(allt); C = np.concatenate(allc); D = np.concatenate(alld)
    o = np.argsort(-D)
    ax.add_collection(PolyCollection(T[o], facecolors=np.clip(C[o], 0, 1), edgecolors='none'))
    ax.set_aspect('equal'); ax.autoscale_view()
    if xlim: ax.set_xlim(*xlim)
    if ylim: ax.set_ylim(*ylim)
    ax.set_title(title, fontsize=11); ax.grid(True, lw=0.3, alpha=0.5)


meshes = [(t2, (0.95, 0.68, 0.36)), (t1, (0.78, 0.82, 0.88))]
fig, ax = plt.subplots(figsize=(14, 13), dpi=120)
draw(ax, meshes, [0, 1, 0], [0, 0, 1], 'T6 LWB underside, STEP read back in. Plan view (X to the right, forward up), lowest surfaces on top.\nGrey: new scan. Orange: first scan (coarse).', mirror=True)
ax.axvline(0, color='r', lw=0.8); ax.set_xlabel('X across (mm), 0 = underbody centreline'); ax.set_ylabel('Z forward (mm), 0 = seat heel as scanned')
fig.savefig(out + '_below.png', bbox_inches='tight'); plt.close(fig)
fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
draw(ax, meshes, [0.55, 0.45, 0.70], [0, 1, 0], 'Oblique view from below and behind')
ax.set_xticks([]); ax.set_yticks([])
fig.savefig(out + '_oblique.png', bbox_inches='tight'); plt.close(fig)
