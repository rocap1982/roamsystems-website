"""Seated 50th percentile UK adult male, built from clean geometric shapes (side view, facing -x), mm.
H-point at the R point (-427, 515), backrest 13 deg, seat surface 462mm, sitting height 910mm (Pheasant via handover).
Other proportions approximate, for illustration only."""
import json, math, sys
from shapely.geometry import Polygon, LineString, Point, box
from shapely.ops import unary_union
from shapely import affinity
R = (-427.0, 515.0); A = 13.0
def rrect(x0, y0, x1, y1, r): return box(x0, y0, x1, y1).buffer(-r, join_style=1).buffer(r, join_style=1)
# torso in its own frame (x forward is negative, so build facing -x): back at x=+128, front at x=-112; H-point at origin
torso = unary_union([rrect(-112, -45, 128, 600, 70), rrect(-100, 420, 128, 640, 95)])
torso = affinity.rotate(torso, -A, origin=(0, 0))            # lean back with the backrest
torso = affinity.translate(torso, R[0], R[1])
sh_top = (R[0] + 600 * math.sin(math.radians(A)), R[1] + 600 * math.cos(math.radians(A)))
neck = rrect(sh_top[0] - 46, sh_top[1] - 20, sh_top[0] + 50, sh_top[1] + 80, 18)
# head: oval skull + simple face profile, upright
cx, cy = sh_top[0] - 6, sh_top[1] + 152
skull = affinity.scale(Point(cx, cy).buffer(100), 0.97, 1.18)
face = Polygon([(cx - 70, cy + 70), (cx - 99, cy + 20), (cx - 97, cy - 2), (cx - 118, cy - 30), (cx - 100, cy - 42),
                (cx - 103, cy - 62), (cx - 94, cy - 92), (cx - 70, cy - 112), (cx - 30, cy - 118), (cx, cy - 60)])
head = unary_union([skull, face])
# legs: thigh horizontal on the cushion, lower leg vertical, shoe flat on the floor
thigh = rrect(-905, 452, R[0] + 60, 612, 75)
shin = rrect(-905, 95, -800, 560, 45)
shoe = unary_union([rrect(-1080, 0, -792, 78, 34), Polygon([(-905, 60), (-905, 115), (-800, 115), (-792, 40), (-960, 40)])])
body = unary_union([torso, neck, head, thigh, shin, shoe]).buffer(4, join_style=1).buffer(-4, join_style=1)
# arm drawn separately on top
el = (R[0] + 250 * math.sin(math.radians(A)) - 20, R[1] + 250 * math.cos(math.radians(A)))
upper = LineString([(sh_top[0] - 25, sh_top[1] - 60), el]).buffer(47)
fore = LineString([el, (-760.0, 652.0)]).buffer(40)
hand = affinity.scale(Point(-790.0, 645.0).buffer(45), 1.3, 0.85)
arm = unary_union([upper, fore, hand]).buffer(2).buffer(-2)
def path(g):
    return 'M' + ' L'.join('%.1f %.1f' % c for c in list(g.simplify(0.6).exterior.coords)[:-1]) + ' Z'
j = json.load(open(sys.argv[1]))
j['occupant'] = path(body); j['occupant_arm'] = path(arm)
j['occupant_head_top'] = round(head.bounds[3]); j['occupant_head_centre_x'] = round(cx)
json.dump(j, open(sys.argv[1], 'w'))
print('head top', j['occupant_head_top'], 'bounds', [round(v) for v in body.bounds])
