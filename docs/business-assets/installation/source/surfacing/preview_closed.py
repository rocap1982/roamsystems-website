import sys, numpy as np, trimesh
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.patches import Patch
# read-back tessellations (model frame) in body order: new scan, first scan, mirrored, continued, best guess
pre = sys.argv[1]; out = sys.argv[2]
cols = [(0.78, 0.82, 0.88), (0.86, 0.84, 0.80), (0.30, 0.72, 0.40), (0.30, 0.52, 0.92), (0.97, 0.62, 0.15)]
labels = ['Scanned (new scan)', 'Scanned (first scan, coarse)', 'Infill: mirrored from the other side', 'Infill: continued across gap', 'Infill: best guess (low confidence)']
meshes = []
for i in range(1, 6):
    try:
        meshes.append((trimesh.load(pre + '_readback_%d.stl' % i), cols[i - 1]))
    except Exception:
        pass


def draw(ax, view, up, mirror=False):
    v = np.asarray(view, float); v /= np.linalg.norm(v); u = np.asarray(up, float); u -= v * (u @ v); u /= np.linalg.norm(u); r = np.cross(u, v)
    L = np.array([0.35, -0.8, 0.45]); L /= np.linalg.norm(L)
    T_, C_, D_ = [], [], []
    for m, col in meshes:
        T = m.vertices[m.faces]
        n = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0]); n /= np.linalg.norm(n, axis=1)[:, None] + 1e-12
        sh = np.abs(n @ L) * 0.75 + 0.2
        T_.append(np.stack([T @ (-r if mirror else r), T @ u], -1)); C_.append(np.asarray(col)[None] * sh[:, None]); D_.append((T @ v).mean(1))
    T = np.concatenate(T_); C = np.concatenate(C_); D = np.concatenate(D_); o = np.argsort(-D)
    ax.add_collection(PolyCollection(T[o], facecolors=np.clip(C[o], 0, 1), edgecolors='none')); ax.set_aspect('equal'); ax.autoscale_view()


fig, ax = plt.subplots(figsize=(14, 13), dpi=120)
draw(ax, [0, 1, 0], [0, 0, 1], mirror=True)
ax.axvline(0, color='r', lw=0.8); ax.grid(True, lw=0.3, alpha=0.5)
ax.set_xlabel('X across (mm), 0 = mirror plane of the underbody'); ax.set_ylabel('Z forward (mm), 0 = seat heel as scanned')
ax.set_title('T6 LWB underside, closed model, STEP read back in. Plan view (X to the right, forward up), lowest surfaces on top.')
ax.legend(handles=[Patch(color=c, label=l) for c, l in zip(cols, labels)], loc='upper right', fontsize=9)
fig.savefig(out + '_plan.png', bbox_inches='tight'); plt.close(fig)
fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
draw(ax, [0.55, 0.45, 0.70], [0, 1, 0]); ax.set_xticks([]); ax.set_yticks([])
ax.set_title('Closed model, oblique view from below and behind')
ax.legend(handles=[Patch(color=c, label=l) for c, l in zip(cols, labels)], loc='upper right', fontsize=9)
fig.savefig(out + '_oblique.png', bbox_inches='tight'); plt.close(fig)
