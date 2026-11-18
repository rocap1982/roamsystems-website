import numpy as np
def raster_min(V, F, x0, z0, g, shape, maxcell=40):
    """Exact lowest surface height (y) at each grid-cell centre, by rasterising every triangle (x-z projection)."""
    H = np.full(shape, np.inf)
    T = V[F]                                   # (n,3,3)
    ax, az = T[:, :, 0], T[:, :, 2]
    i0 = np.floor((ax.min(1) - x0) / g - 0.5).astype(int) + 1; i1 = np.floor((ax.max(1) - x0) / g - 0.5).astype(int)
    j0 = np.floor((az.min(1) - z0) / g - 0.5).astype(int) + 1; j1 = np.floor((az.max(1) - z0) / g - 0.5).astype(int)
    w = np.clip(i1 - i0 + 1, 0, None); h = np.clip(j1 - j0 + 1, 0, None)
    keep = (w > 0) & (h > 0) & (w <= maxcell) & (h <= maxcell)
    T, i0, j0, w, h = T[keep], i0[keep], j0[keep], w[keep], h[keep]
    p0 = T[:, 0]; e1 = T[:, 1] - p0; e2 = T[:, 2] - p0
    det = e1[:, 0] * e2[:, 2] - e1[:, 2] * e2[:, 0]
    good = np.abs(det) > 1e-9
    T, i0, j0, w, h, p0, e1, e2, det = T[good], i0[good], j0[good], w[good], h[good], p0[good], e1[good], e2[good], det[good]
    for di in range(int(w.max())):
        for dj in range(int(h.max())):
            m = (di < w) & (dj < h)
            if not m.any(): continue
            ii = i0[m] + di; jj = j0[m] + dj
            ok = (ii >= 0) & (ii < shape[1]) & (jj >= 0) & (jj < shape[0])
            ii, jj = ii[ok], jj[ok]
            px = x0 + (ii + 0.5) * g - p0[m][ok, 0]; pz = z0 + (jj + 0.5) * g - p0[m][ok, 2]
            E1 = e1[m][ok]; E2 = e2[m][ok]; D = det[m][ok]
            u = (px * E2[:, 2] - pz * E2[:, 0]) / D; v = (E1[:, 0] * pz - E1[:, 2] * px) / D
            inside = (u >= -1e-9) & (v >= -1e-9) & (u + v <= 1 + 1e-9)
            y = p0[m][ok, 1] + u * E1[:, 1] + v * E2[:, 1]
            ii, jj, y = ii[inside], jj[inside], y[inside]
            np.minimum.at(H, (jj, ii), y)
    H[np.isinf(H)] = np.nan
    return H
