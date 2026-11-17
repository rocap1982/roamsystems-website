import numpy as np, trimesh, json, sys
m = trimesh.load(sys.argv[1]); n = m.face_normals; a = m.area_faces; c = m.triangles_center
def fit(dirn, tol=0.93):
    d = np.asarray(dirn, float); d /= np.linalg.norm(d)
    s = np.abs(n @ d) > tol
    C = (n[s] * np.sign(n[s] @ d)[:, None] * a[s, None]).sum(0); C /= np.linalg.norm(C)
    return C, s
A, sA = fit([0.17, 0.65, 0.74]); B, sB = fit([0.20, -0.73, 0.65])
B = B - A * (A @ B); B /= np.linalg.norm(B)                     # make exactly perpendicular
up = -A                                                           # floor underside normal points down/out
cen = m.vertices.mean(0)
fwd = B if ((c[sA] - c[sB].mean(0)).mean(0) @ B) > 0 else -B      # from the door opening towards the floor
lat = np.cross(up, fwd)                                           # left/right
R = np.vstack([lat, up, fwd])                                     # rows: x lateral, y up, z forward
P = (m.vertices - cen) @ R.T
# rear door plane position (z) and floor underside height (y) from the two surface groups
F = m.faces
zB = np.median(((c[sB] - cen) @ fwd)); yA = np.median(((c[sA] - cen) @ up))
print('angle A-B %.1f deg' % np.degrees(np.arccos(abs(np.dot([0.17,0.65,0.74],[0.20,-0.73,0.65])/np.linalg.norm([0.17,0.65,0.74])/np.linalg.norm([0.20,-0.73,0.65])))))
print('door-plane z %.0f   floor-underside y %.0f' % (zB, yA))
print('bounds in van frame (x lat, y up, z fwd):', np.round(P.min(0)), np.round(P.max(0)))
json.dump({'cen': cen.tolist(), 'R': R.tolist(), 'zB': float(zB), 'yA': float(yA)}, open(sys.argv[2], 'w'))
mm = trimesh.Trimesh(P, F, process=False); mm.export(sys.argv[3])
