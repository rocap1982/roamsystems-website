import sys, numpy as np, trimesh, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
def render(mesh, view, up, out, title='', size=(9, 9), light=None, colour_by=None):
    """Orthographic shaded render: view = direction we look along, up = screen up."""
    v = np.asarray(view, float); v /= np.linalg.norm(v); u = np.asarray(up, float); u -= v * (u @ v); u /= np.linalg.norm(u)
    r = np.cross(u, v)                              # screen right
    P = mesh.vertices; F = mesh.faces
    X = P @ r; Y = P @ u; D = P @ v                 # depth along view (larger = further)
    tri = np.stack([np.c_[X[F[:, k]], Y[F[:, k]]] for k in range(3)], 1)
    depth = D[F].mean(1); order = np.argsort(-depth)  # far first
    n = mesh.face_normals; L = -v if light is None else np.asarray(light, float) / np.linalg.norm(light)
    shade = np.clip(np.abs(n @ L), 0, 1) * 0.8 + 0.15
    if colour_by is not None:
        cmap = plt.get_cmap('viridis'); c = colour_by[F].mean(1); c = (c - c.min()) / (np.ptp(c) + 1e-9)
        col = cmap(c)[:, :3] * shade[:, None]
    else:
        col = np.c_[shade, shade, shade] * np.array([0.75, 0.82, 0.9])
    fig, ax = plt.subplots(figsize=size, dpi=110); ax.set_aspect('equal'); ax.set_facecolor('white')
    ax.add_collection(PolyCollection(tri[order], facecolors=np.clip(col[order], 0, 1), edgecolors='none'))
    ax.set_xlim(X.min(), X.max()); ax.set_ylim(Y.min(), Y.max()); ax.set_title(title); ax.grid(True, lw=0.3, alpha=0.5)
    fig.savefig(out, bbox_inches='tight'); plt.close(fig)
    return r, u, v
if __name__ == '__main__':
    m = trimesh.load(sys.argv[1]); o = sys.argv[2]
    lat = np.array([-0.97, -0.09, 0.22]); lat /= np.linalg.norm(lat)
    A = np.array([0.17, 0.65, 0.74]); B = np.array([0.20, -0.73, 0.65])
    render(m, lat, A, o + '_side.png', 'looking along the van width (side view)')
    render(m, A, B, o + '_A.png', 'looking along normal of plane A')
    render(m, B, A, o + '_B.png', 'looking along normal of plane B')
