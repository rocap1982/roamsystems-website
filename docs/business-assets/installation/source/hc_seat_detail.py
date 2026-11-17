import sys, json, math, pickle
H = pickle.load(open(sys.argv[1], 'rb'))
L = lambda pl: sum(math.dist(pl[i], pl[i+1]) for i in range(len(pl) - 1))
segs = []
for p in H['SEAT_FRAME']:
    mm = [(q[0] - 91, -q[1] + 485) for q in p]
    if all(x > -345 for x, y in mm) and L(mm) > 25: segs.append(mm)
def near(a, b):
    sample = a[::max(1, len(a)//10)]
    return sum(1 for pt in sample if min(math.dist(pt, q) for q in b) < 6) >= 0.7 * len(sample)
kept = []
for s in sorted(segs, key=L, reverse=True):
    if not any(near(s, k) for k in kept): kept.append(s)
def rdp(pts, eps):
    if len(pts) < 3: return pts
    (x1,y1),(x2,y2) = pts[0], pts[-1]; dx,dy = x2-x1, y2-y1; Ln = math.hypot(dx,dy)
    if Ln < 1e-6: return pts
    d = [abs(dy*(x-x1)-dx*(y-y1))/Ln for x,y in pts[1:-1]]; i = max(range(len(d)), key=d.__getitem__)
    return rdp(pts[:i+2], eps)[:-1] + rdp(pts[i+1:], eps) if d[i] > eps else [pts[0], pts[-1]]
j = json.load(open(sys.argv[2]))
j['detail'] = ' '.join('M' + ' L'.join('%.1f %.1f' % q for q in rdp(s, 1.0)) for s in kept)
json.dump(j, open(sys.argv[2], 'w'))
print('candidate', len(segs), 'kept', len(kept), 'chars', len(j['detail']))
