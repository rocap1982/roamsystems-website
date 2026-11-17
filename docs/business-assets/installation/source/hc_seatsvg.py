import sys, json, pickle, math
sys.path.insert(0, sys.argv[1])
from cad_lib import *
from OCP.TopAbs import TopAbs_SOLID, TopAbs_EDGE
from OCP.BRepAlgoAPI import BRepAlgoAPI_Section
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCP.gp import gp_Pln, gp_Pnt, gp_Dir
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.GCPnts import GCPnts_QuasiUniformDeflection
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS
HEELX, FLOORY, SC = float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
H = pickle.load(open(sys.argv[2], 'rb'))
def to_svg(xmm, ymm): return (HEELX + xmm*SC, FLOORY - ymm*SC)
def rdp(pts, eps):
    if len(pts) < 3: return pts
    (x1,y1),(x2,y2) = pts[0], pts[-1]; dx,dy = x2-x1, y2-y1; L = math.hypot(dx,dy) or 1e-9
    d = [abs(dy*(x-x1)-dx*(y-y1))/L for x,y in pts[1:-1]]; i = max(range(len(d)), key=d.__getitem__)
    if d[i] > eps: return rdp(pts[:i+2], eps)[:-1] + rdp(pts[i+1:], eps)
    return [pts[0], pts[-1]]
def plen(p): return sum(math.hypot(p[i+1][0]-p[i][0], p[i+1][1]-p[i][1]) for i in range(len(p)-1))
frame = []
for p in H['SEAT_FRAME']:
    mm = [(q[0]-91, -q[1]+485) for q in p]
    if plen(mm) < 6: continue
    mm = rdp(mm, 1.2)
    frame.append('M' + ' L'.join('%.1f %.1f' % to_svg(*q) for q in mm))
# cushion cross-section at the seat centreline (model x = -378)
cush = sub(load('p0061.brep'), TopAbs_SOLID)
face = BRepBuilderAPI_MakeFace(gp_Pln(gp_Pnt(-378,0,0), gp_Dir(1,0,0)), -3000,3000,-3000,3000).Face()
polys = []
for i in (4,5,6):
    sec = BRepAlgoAPI_Section(cush[i], face).Shape()
    segs = []
    ex = TopExp_Explorer(sec, TopAbs_EDGE)
    while ex.More():
        e = TopoDS.Edge_s(ex.Current()); ex.Next()
        c = BRepAdaptor_Curve(e); d = GCPnts_QuasiUniformDeflection(c, 0.3)
        segs.append([(-(d.Value(k).Z()+91), d.Value(k).Y()+485) for k in range(1, d.NbPoints()+1)])
    # chain segments into a closed loop
    loop = segs.pop(0)
    while segs:
        end = loop[-1]
        best = min(range(len(segs)), key=lambda j: min(math.dist(end, segs[j][0]), math.dist(end, segs[j][-1])))
        s = segs.pop(best)
        if math.dist(end, s[-1]) < math.dist(end, s[0]): s = s[::-1]
        loop += s[1:]
    h = len(loop)//2
    simp = rdp(loop[:h+1], 0.8)[:-1] + rdp(loop[h:], 0.8)   # split so a closed loop does not collapse
    polys.append('M' + ' L'.join('%.1f %.1f' % to_svg(*q) for q in simp) + ' Z')
out = {'frame': ' '.join(frame), 'cushions': polys}
json.dump(out, open(sys.argv[6], 'w'))
print('frame paths', len(frame), 'chars', len(out['frame']), 'cushions', [len(p) for p in polys])
