import sys, json, time, pickle
sys.path.insert(0, sys.argv[1])
from cad_lib import *
from OCP.TopAbs import TopAbs_SOLID, TopAbs_SHELL, TopAbs_EDGE
from OCP.TopoDS import TopoDS_Compound, TopoDS
from OCP.BRep import BRep_Builder
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.HLRBRep import HLRBRep_PolyAlgo, HLRBRep_PolyHLRToShape
from OCP.HLRAlgo import HLRAlgo_Projector
from OCP.gp import gp_Ax2, gp_Pnt, gp_Dir
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.GCPnts import GCPnts_QuasiUniformDeflection
from OCP.TopExp import TopExp_Explorer
T=json.load(open('tree.json'))
def part(fn): return load(fn)
def comp(shapes):
    c=TopoDS_Compound(); b=BRep_Builder(); b.MakeCompound(c)
    for s in shapes: b.Add(c,s)
    return c
SEAT=['p0002','p0003','p0005','p0006','p0007','p0008','p0009','p0010','p0011','p0012','p0013','p0014','p0022','p0023','p0024']
frame=[]
for f in SEAT:
    s=part(f+'.brep')
    if f=='p0003':  # rear frame: drop the owner's stand-in D pillar bar (shell 16)
        for sh in sub(s,TopAbs_SHELL):
            b=bb(sh)
            if b[1]>800: print('dropped stand-in bar shell',b); continue
            frame.append(sh)
    else: frame.append(s)
cush=sub(part('p0061.brep'),TopAbs_SOLID)
groups={'SEAT_FRAME':comp(frame),'SEAT_CUSHIONS':comp([cush[i] for i in (4,5,6)]),'HEAD_REST_CONCEPT':comp([cush[7]])}
child=[o for o in T if o['type']=='PART' and 'Human' in o['name']]
if child: groups['REF_CHILD_8-9Y_P95']=part(child[0]['brep'])
out={}
proj=HLRAlgo_Projector(gp_Ax2(gp_Pnt(0,0,0),gp_Dir(-1,0,0),gp_Dir(0,0,-1)))
for name,shape in groups.items():
    t=time.time(); BRepMesh_IncrementalMesh(shape,0.5,False,0.3,True)
    algo=HLRBRep_PolyAlgo(); algo.Load(shape); algo.Projector(proj); algo.Update()
    h=HLRBRep_PolyHLRToShape(); h.Update(algo)
    polys=[]
    for getter in ('VCompound','OutLineVCompound','Rg1LineVCompound'):
        try: cs=getattr(h,getter)()
        except Exception as e: print(name,getter,'err',e); continue
        if cs.IsNull(): continue
        ex=TopExp_Explorer(cs,TopAbs_EDGE)
        while ex.More():
            e=TopoDS.Edge_s(ex.Current()); ex.Next()
            try:
                c=BRepAdaptor_Curve(e); d=GCPnts_QuasiUniformDeflection(c,0.3)
                pts=[ (round(d.Value(i).X(),2),round(d.Value(i).Y(),2)) for i in range(1,d.NbPoints()+1)]
                if len(pts)>1: polys.append(pts)
            except Exception: pass
    out[name]=polys
    xs=[p[0] for pl in polys for p in pl]; ys=[p[1] for pl in polys for p in pl]
    print(name,len(polys),'polys','x %.0f..%.0f y %.0f..%.0f'%(min(xs),max(xs),min(ys),max(ys)),'%.0fs'%(time.time()-t),flush=True)
# mapping check: project known points
from OCP.gp import gp_Pnt2d
for P in ((0,-485,-91),(0,0,427-91)):
    p2=gp_Pnt2d(); proj.Project(gp_Pnt(*P),p2); print('map',P,'->',round(p2.X(),1),round(p2.Y(),1))
pickle.dump(out,open('../hc/hlr.pkl','wb'))
