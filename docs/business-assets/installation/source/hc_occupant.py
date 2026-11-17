"""50th percentile UK adult male, seated on the ROAM rear seat, side view facing -x (front of van to the left), mm.

Body dimensions, UK men 19-65, 50th percentile (Pheasant, Bodyspace, Table 10.1):
  sitting height 910 and popliteal height 440 checked against a second source; the rest as recalled from the book:
  sitting eye 790, sitting shoulder 595, sitting elbow 245, thigh thickness 160, buttock-knee 595,
  buttock-popliteal 495, knee height 545, chest depth 250, abdominal depth 270, head length 195, foot length 265.
  Head height (vertex to chin) 232 is a general adult figure, not from the table. Shoes add 25mm.
Posture and seat assumptions:
  backrest face taken from the modelled backrest cushion (13 deg); cushion compressed 25mm under the occupant;
  torso against the backrest; head upright (eyes level); upper arm down the side, forearm resting on the thigh;
  lower legs near vertical, shoes flat on the floor.
"""
import json, math, sys
import numpy as np
from shapely.geometry import Polygon, Point, LineString
from shapely.ops import unary_union
J = json.load(open(sys.argv[1]))
def poly(d): return Polygon([tuple(map(float, p.split())) for p in d[1:].replace('Z', '').strip().split(' L')])
cush = [poly(c) for c in J['cushions']]
back = max(cush, key=lambda p: p.bounds[3] - p.bounds[1])       # backrest cushion
base = max(cush, key=lambda p: p.bounds[2] - p.bounds[0])        # base cushion
# backrest front face: front-most cushion point at each height between 600 and 1000mm
ys = np.arange(600, 1001, 25); xs = []
for y in ys:
    seg = back.intersection(LineString([(-2000, y), (500, y)]))
    xs.append(seg.bounds[0])
k, c0 = np.polyfit(ys, xs, 1)                                     # x = k*y + c0
lean = math.degrees(math.atan(k))
SEAT_TOP = base.bounds[3]; COMP = 25.0; YS = SEAT_TOP - COMP; SHOE = 25.0
A = math.radians(lean)
u = np.array([math.sin(A), math.cos(A)])                          # up the backrest
n = np.array([-math.cos(A), math.sin(A)])                         # forward, normal to the backrest
B0 = np.array([k * YS + c0, YS])                                  # backrest face at seat level
def T(l, f): p = B0 + l * u + f * n; return (float(p[0]), float(p[1]))
def cr(pts, closed=True, m=10):
    """Catmull-Rom spline through the points."""
    P = [np.array(p, float) for p in pts]; out = []
    N = len(P); rng = range(N) if closed else range(N - 1)
    for i in rng:
        p0, p1, p2, p3 = P[(i - 1) % N], P[i], P[(i + 1) % N], P[(i + 2) % N]
        if not closed:
            p0 = P[max(i - 1, 0)]; p3 = P[min(i + 2, N - 1)]
        for t in np.linspace(0, 1, m, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    return [tuple(map(float, q)) for q in out]
cosA = math.cos(A)
V = lambda pts: Polygon(pts).buffer(0)
L = lambda h: h / cosA                                            # seated height above seat -> distance along the backrest
# ---- torso (back on the backrest, l along backrest, f forward)
torso = V(cr([T(L(20), 18), T(L(70), -6), T(L(150), 2), T(L(240), 16), T(L(360), 4), T(L(470), -2),
                    T(L(540), 2), T(L(575), 14), T(L(600), 34), T(L(618), 70), T(L(628), 110), T(L(622), 150), T(L(585), 205), T(L(510), 238),
                    T(L(420), 250), T(L(320), 238), T(L(230), 252), T(L(150), 262), T(L(70), 255), T(L(25), 210),
                    T(L(5), 120)]))
# ---- head (upright): vertex at seat + reclined trunk + head height
HEAD_H = 232.0
vertex_y = YS + (910 - HEAD_H) * cosA + HEAD_H
occ_y = vertex_y - 92                                              # back-most point of the skull
occ_x = T(L(605), 58)[0] + 22                                     # skull overhangs the back of the neck by ~22mm (head upright)
hp = [(95, 232), (140, 222), (178, 190), (193, 152), (195, 132), (188, 116), (192, 104), (212, 86), (206, 77),
      (190, 72), (195, 61), (190, 53), (192, 44), (184, 33), (190, 16), (168, 2), (135, 4), (108, 18), (92, 34),
      (60, 38), (30, 58), (8, 92), (0, 140), (10, 185), (40, 218)]
hy0 = vertex_y - HEAD_H
head = V(cr([(occ_x - x, hy0 + y) for x, y in hp], m=8))
neck = V(cr([(occ_x - 30, hy0 + 64), (occ_x - 92, hy0 + 30), T(L(612), 150), T(L(585), 40)], m=6))
# ---- thigh, knee, lower leg, shoe
xb = T(L(20), 0)[0]                                               # back of buttock at seat level
knee_front = xb - 595
pop_x = xb - 495
thigh = V(cr([(xb + 5, YS + 40), (xb - 60, YS), (pop_x + 60, YS + 5), (pop_x, 440 + SHOE + 5),
                    (knee_front + 25, 455 + SHOE), (knee_front, 500 + SHOE), (knee_front + 18, 545 + SHOE),
                    (knee_front + 90, 552 + SHOE), (xb - 300, YS + 160), (xb - 120, YS + 168), (xb - 20, YS + 120)], m=8))
ankle_x = knee_front + 45
leg = V(cr([(knee_front + 2, 505 + SHOE), (knee_front + 15, 300), (ankle_x - 8, 120), (ankle_x + 40, 105),
                  (ankle_x + 80, 160), (pop_x + 15, 330), (pop_x + 25, 440 + SHOE)], m=8))
heel_x = ankle_x + 85
shoe = V(cr([(heel_x, 8), (heel_x + 5, 70), (heel_x - 25, 118), (ankle_x - 20, 118), (ankle_x - 95, 82),
                   (heel_x - 290, 38), (heel_x - 296, 12), (heel_x - 280, 0), (heel_x - 20, 0)], m=6))
body = unary_union([torso, head, neck, thigh, leg, shoe])
head_neck = body.intersection(Polygon([(-2000, hy0 - 120), (500, hy0 - 120), (500, 3000), (-2000, 3000)]))
body = unary_union([body.buffer(3, join_style=1).buffer(-3, join_style=1), head_neck.buffer(12, join_style=1).buffer(-12, join_style=1)])
# ---- arm (drawn on top): upper arm down the side, forearm resting on the thigh
sh = np.array(T(L(560), 115))
acromion_y = YS + 595 * cosA
elbow = np.array([sh[0] - 55, acromion_y - (595 - 245) + 35])
thigh_top_at = lambda x: YS + 160 - (xb - 120 - x) * 0.11
wrist = np.array([elbow[0] - 235, thigh_top_at(elbow[0] - 235) + 40])
fwd = (wrist - elbow) / np.linalg.norm(wrist - elbow); nrm = np.array([-fwd[1], fwd[0]])
def off(p, d): q = p + d * nrm; return (float(q[0]), float(q[1]))
upper = V(cr([(sh[0] - 50, sh[1] + 25), (sh[0] + 40, sh[1] + 15),
                    (elbow[0] + 45, elbow[1] + 5), (elbow[0] + 10, elbow[1] - 42), (elbow[0] - 40, elbow[1] - 15),
                    (sh[0] - 55, sh[1] - 40)], m=8))
fore = V(cr([(elbow[0] + 30, elbow[1] - 40), off(elbow, -40), off(wrist, -28), off(wrist, 26),
                   off(elbow + 0.35 * (wrist - elbow), 45), (elbow[0] + 15, elbow[1] + 38)], m=8))
def along(d, s): q = wrist + fwd * d + nrm * s; return (float(q[0]), float(q[1]))
hand = V(cr([along(0, 27), along(80, 30), along(140, 20), along(182, 2), along(176, -12), along(120, -22),
             along(40, -26), along(0, -27)], m=6))
arm = unary_union([upper, fore, hand]).buffer(2, join_style=1).buffer(-2, join_style=1)
def path(g):
    g = g.simplify(0.5)
    gs = list(g.geoms) if hasattr(g, 'geoms') else [g]
    return ' '.join('M' + ' L'.join('%.1f %.1f' % c for c in list(p.exterior.coords)[:-1]) + ' Z' for p in gs)
J['occupant'] = path(body); J['occupant_arm'] = path(arm)
J['occupant_head_top'] = round(head.bounds[3]); J['occupant_head_centre_x'] = round(occ_x - 97)
J['occupant_note'] = ('50th percentile UK adult male (Pheasant, Bodyspace): sitting height 910mm; cushion compressed 25mm; '
                      'backrest %.1f deg; head upright; shoes 25mm' % lean)
json.dump(J, open(sys.argv[1], 'w'))
print('backrest lean %.1f deg, seat top %.0f, compressed %.0f' % (lean, SEAT_TOP, YS))
print('vertex %.0f  eye %.0f  acromion %.0f  elbow-bottom %.0f  knee-top %.0f  head x %.0f..%.0f' % (
      vertex_y, vertex_y - 120, acromion_y, acromion_y - 350, 545 + SHOE, head.bounds[0], head.bounds[2]))
print('body bounds', [round(v) for v in body.bounds], 'parts', len(body.geoms) if hasattr(body, 'geoms') else 1)
