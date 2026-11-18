"""van (scan) frame -> corrected model frame: X normal to the fitted mirror plane (X = 0 on it), Y up, Z forward"""
import json, sys, numpy as np
CX, Y0, Z0 = 120.0, 216.1, 166.0
def matrix(mirror_json):
    mp = json.load(open(mirror_json)); n = np.array(mp['n']); d = mp['d']
    x = np.array([1.0, 0, 0]); v = np.cross(n, x); s = np.linalg.norm(v); c = n @ x
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    R = np.eye(3) + K + K @ K * ((1 - c) / s ** 2)
    t = R @ np.array([-CX, Y0, Z0]) - np.array([d, 0, 0])
    M = np.eye(4); M[:3, :3] = R; M[:3, 3] = t
    return M
if __name__ == '__main__':
    M = matrix(sys.argv[1]); json.dump(dict(M=M.tolist()), open(sys.argv[2], 'w'), indent=1)
    print(np.round(M, 5))
