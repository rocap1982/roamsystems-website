import json, math
from OCP.BRep import BRep_Builder, BRep_Tool
from OCP.BRepTools import BRepTools
from OCP.TopoDS import TopoDS_Shape, TopoDS
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID, TopAbs_FACE, TopAbs_SHELL
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder, GeomAbs_Plane
TREE=json.load(open('tree.json'))
def find(sub): return [o for o in TREE if o['type']=='PART' and sub.lower() in o['name'].lower()]
def load(fn):
    s=TopoDS_Shape(); BRepTools.Read_s(s,fn,BRep_Builder()); return s
def bb(s):
    b=Bnd_Box(); BRepBndLib.Add_s(s,b); return [round(v,1) for v in b.Get()]
def vol(s):
    g=GProp_GProps(); BRepGProp.VolumeProperties_s(s,g); return g.Mass()
def area(s):
    g=GProp_GProps(); BRepGProp.SurfaceProperties_s(s,g); return g.Mass()
def sub(s,kind):
    e=TopExp_Explorer(s,kind); out=[]
    while e.More(): out.append(e.Current()); e.Next()
    return out
def cyls(s,rmin=0,rmax=1e9):
    out=[]
    for f in sub(s,TopAbs_FACE):
        a=BRepAdaptor_Surface(TopoDS.Face_s(f))
        if a.GetType()==GeomAbs_Cylinder:
            c=a.Cylinder(); r=c.Radius()
            if rmin<=r<=rmax:
                ax=c.Axis(); d=ax.Direction(); p=ax.Location()
                b=bb(f)
                out.append({'d':round(2*r,2),'axis':(round(d.X(),2),round(d.Y(),2),round(d.Z(),2)),'bb':b,'c':(round((b[0]+b[3])/2,1),round((b[1]+b[4])/2,1),round((b[2]+b[5])/2,1))})
    return out
