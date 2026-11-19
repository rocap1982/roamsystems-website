"""Plan view of the seat area from the read-back model with the fixings, the scanned bolt ends and the member
inner walls drawn on, for a visual check of the symmetry.
usage: preview_fixings.py readback_prefix fixings.json out.png"""
import sys, json, numpy as np, trimesh
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.patches import Patch, Circle
from matplotlib.lines import Line2D

pre, fxj, out = sys.argv[1:4]
fx = json.load(open(fxj))
cols = [(0.78, 0.82, 0.88), (0.86, 0.84, 0.80), (0.30, 0.72, 0.40), (0.30, 0.52, 0.92), (0.97, 0.62, 0.15)]
labels = ['Scanned (new scan)', 'Scanned (first scan, coarse)', 'Infill: mirrored', 'Infill: continued across gap', 'Infill: best guess']
XL, ZL = (-720, 720), (-170, 760)
BOX = dict(fc='white', ec='none', alpha=0.85, pad=1.5)
L = np.array([0.35, -0.8, 0.45]); L /= np.linalg.norm(L)
T_, C_, D_ = [], [], []
for i in range(1, 6):
    m = trimesh.load(pre + '_readback_%d.stl' % i)
    T = m.vertices[m.faces]
    c = T.mean(1); keep = (c[:, 0] > XL[0] - 20) & (c[:, 0] < XL[1] + 20) & (c[:, 2] > ZL[0] - 20) & (c[:, 2] < ZL[1] + 20)
    T = T[keep]
    n = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0]); n /= np.linalg.norm(n, axis=1)[:, None] + 1e-12
    sh = np.abs(n @ L) * 0.75 + 0.2
    T_.append(T[:, :, [0, 2]]); C_.append(np.asarray(cols[i - 1])[None] * sh[:, None]); D_.append(T[:, :, 1].mean(1))
T = np.concatenate(T_); C = np.concatenate(C_); D = np.concatenate(D_); o = np.argsort(-D)      # lowest surfaces on top

fig, ax = plt.subplots(figsize=(15, 10.5), dpi=130)
ax.add_collection(PolyCollection(T[o], facecolors=np.clip(C[o], 0, 1), edgecolors='none'))
xm, (wl, wr), half = fx['member_midline_x'], fx['member_inner_walls_x'], fx['row_half_spacing']
ax.axvline(xm, color='r', lw=1.0)
for x in (wl, wr):
    ax.plot([x, x], [-100, 650], color=(0.10, 0.45, 0.85), lw=1.6, ls='--')
for side, k, d, x, z in fx['fixings']:
    ax.add_patch(Circle((x, z), 6.25, color=(0.85, 0.10, 0.10), zorder=5))
    ax.add_patch(Circle((x, z), 16, fill=False, ec=(0.85, 0.10, 0.10), lw=1.2, zorder=5))
    if x > 0:
        ax.text(x + 24, z, '%d from heel  (Z %.0f)' % (d, z), va='center', fontsize=8.5, color=(0.6, 0.05, 0.05), bbox=BOX)
for x, z, y, d in fx['bolt_ends']:
    ax.plot(x, z, marker='x', ms=11, mew=2.2, color=(0.75, 0.15, 0.75), zorder=6)
zd = 715
for a, b, txt in ((xm - half, xm, '%.1f' % half), (xm, xm + half, '%.1f' % half)):
    ax.annotate('', (a, zd), (b, zd), arrowprops=dict(arrowstyle='<->', lw=1.1))
    ax.text((a + b) / 2, zd + 10, txt, ha='center', fontsize=10, fontweight='bold', bbox=BOX)
for a, b in ((xm - half, wl), (wr, xm + half)):
    ax.annotate('', (a, 668), (b, 668), arrowprops=dict(arrowstyle='<->', lw=1.0, color=(0.10, 0.45, 0.85)))
    ax.text((a + b) / 2, 676, '%.0f' % abs(b - a), ha='center', fontsize=9.5, color=(0.10, 0.45, 0.85), bbox=BOX)
ax.annotate('', (wl, 668), (wr, 668), arrowprops=dict(arrowstyle='<->', lw=1.0, color=(0.10, 0.45, 0.85)))
ax.text(xm, 676, '%.0f between member inner walls' % (wr - wl), ha='center', fontsize=9.5, color=(0.10, 0.45, 0.85), bbox=BOX)
ax.set_xlim(*XL); ax.set_ylim(*ZL); ax.set_aspect('equal'); ax.grid(True, lw=0.3, alpha=0.5)
ax.set_xlabel('X across the van (mm); 0 = midline of the two chassis members (and the mirror plane of the underbody)')
ax.set_ylabel('Z forward (mm); 0 = seat heel as scanned')
ax.set_title('Seat fixings in the STEP: symmetric about the chassis members. Plan from below, drawn with X to the right.')
hand = [Line2D([], [], marker='o', ls='', color=(0.85, 0.10, 0.10), label='Seat fixing, 12.5mm hole (pattern from the seat model)'),
        Line2D([], [], marker='x', ls='', mew=2, color=(0.75, 0.15, 0.75), label='Seat bolt end found in the scan'),
        Line2D([], [], ls='--', color=(0.10, 0.45, 0.85), label='Chassis member inner wall (measured)'),
        Line2D([], [], color='r', label='Member midline, X 0')] + [Patch(color=c, label=l) for c, l in zip(cols, labels)]
ax.legend(handles=hand, loc='lower center', fontsize=8.5, ncol=3, framealpha=0.92)
fig.savefig(out, bbox_inches='tight'); plt.close(fig)
print('saved', out)
