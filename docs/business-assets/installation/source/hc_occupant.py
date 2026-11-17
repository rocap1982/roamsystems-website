"""Seated 50th percentile UK adult male, side view, facing the front of the van (-x), mm.
Anchored on the ROAM seat: H-point at the R point (-427, 515), seat surface 462mm, backrest 13 deg.
Body dimensions: sitting height 910 (handover, Pheasant); other segment sizes are approximate
50th percentile UK male values (Pheasant, Bodyspace) used for drawing only."""
import json, math, sys
from shapely.geometry import Polygon, LineString, Point
from shapely.ops import unary_union
from shapely import affinity
R = (-427.0, 515.0); SEAT = 462.0; A = math.radians(13)
u = (math.sin(A), math.cos(A))      # up the torso (leans rearward, +x)
n = (-math.cos(A), math.sin(A))     # forward, normal to the torso
def P(l, f=0.0, base=R): return (base[0] + l*u[0] + f*n[0], base[1] + l*u[1] + f*n[1])
SIT = 910.0
top = SIT - (R[1] - SEAT)            # head top along torso axis from the H-point (857)
# torso: back against the backrest, chest forward
torso = Polygon([P(-60, -118), P(0, -126), P(200, -128), P(420, -126), P(560, -112), P(620, -80), P(652, -20),
                 P(636, 55), P(560, 125), P(450, 160), P(330, 158), P(230, 135), P(120, 140), P(30, 150), P(-45, 70)])
neck = LineString([P(600, -5), P(690, 10)]).buffer(55)
# head profile (side view, face forward); local coords: x forward, y up from the chin line
hp = [(0,0),(30,-5),(60,8),(80,35),(95,60),(88,78),(100,100),(112,118),(104,132),(102,150),(108,175),(100,205),
      (75,228),(35,240),(-10,236),(-55,220),(-88,190),(-100,150),(-96,110),(-80,75),(-55,45),(-30,25)]
cb = P(top - 240, 5)                  # chin-line point on the torso axis; head kept upright (eyes level)
head = Polygon([(cb[0] - x + 10, cb[1] + y) for x, y in hp])
hip = P(0, 0)
knee = (R[0] - 440, 520.0)
ankle = (knee[0] - 25, 85.0)
thigh = LineString([P(10, 10), knee]).buffer(80, cap_style=1)
shin = LineString([knee, ankle]).buffer(55, cap_style=1)
foot = Polygon([(ankle[0] + 70, 0), (ankle[0] + 70, 60), (ankle[0] + 20, 115), (ankle[0] - 60, 110),
                (ankle[0] - 150, 55), (ankle[0] - 200, 30), (ankle[0] - 200, 0)])
body = unary_union([torso, neck, head, thigh, shin, foot]).buffer(6).buffer(-6)
# arm: shoulder to elbow down the torso, forearm forward along the thigh
sh = P(555, 10); el = P(300, 20); hand = (R[0] - 330, 600.0)
arm = unary_union([LineString([sh, el]).buffer(48, cap_style=1), LineString([el, hand]).buffer(40, cap_style=1),
                   Point(hand).buffer(46)]).simplify(1.0)
def path(g):
    gs = list(g.geoms) if hasattr(g, 'geoms') else [g]
    return ' '.join('M' + ' L'.join('%.1f %.1f' % c for c in list(p.exterior.coords)[:-1]) + ' Z' for p in gs)
j = json.load(open(sys.argv[1]))
j['occupant'] = path(body.simplify(1.0)); j['occupant_arm'] = path(arm)
hb = head.bounds; j['occupant_head_top'] = round(max(c[1] for c in head.exterior.coords))
j['occupant_note'] = '50th percentile UK adult male, sitting height 910mm (Pheasant via handover); other proportions approximate'
json.dump(j, open(sys.argv[1], 'w'))
print('head top above floor', j['occupant_head_top'], 'toe x', round(body.bounds[0]), 'body bounds', [round(v) for v in body.bounds])
