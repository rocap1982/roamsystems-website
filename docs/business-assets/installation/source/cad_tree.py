import sys, json, time
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.XCAFDoc import XCAFDoc_DocumentTool, XCAFDoc_ShapeTool
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.TDF import TDF_LabelSequence, TDF_Label
from OCP.TDataStd import TDataStd_Name
from OCP.IFSelect import IFSelect_RetDone
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
from OCP.TopLoc import TopLoc_Location
from OCP.BRepTools import BRepTools
from OCP.TopAbs import TopAbs_SOLID
from OCP.TopExp import TopExp_Explorer
t0=time.time()
doc=TDocStd_Document(TCollection_ExtendedString("xde"))
r=STEPCAFControl_Reader(); r.SetNameMode(True)
st=r.ReadFile(sys.argv[1]); assert st==IFSelect_RetDone, st
r.Transfer(doc); print('loaded in %.0fs'%(time.time()-t0),flush=True)
tool=XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
def name(lab):
    n=TDataStd_Name()
    return n.Get().ToExtString() if lab.FindAttribute(TDataStd_Name.GetID_s(),n) else '?'
out=[]
def walk(lab,loc,path,depth):
    ref=TDF_Label()
    inst=name(lab)
    if XCAFDoc_ShapeTool.IsReference_s(lab):
        XCAFDoc_ShapeTool.GetReferredShape_s(lab,ref)
        l2=loc.Multiplied(XCAFDoc_ShapeTool.GetLocation_s(lab)); target=ref
    else:
        l2=loc; target=lab
    nm=name(target)
    if XCAFDoc_ShapeTool.IsAssembly_s(target):
        out.append({'depth':depth,'type':'ASM','name':nm,'inst':inst,'path':path+[nm]})
        comps=TDF_LabelSequence(); XCAFDoc_ShapeTool.GetComponents_s(target,comps,False)
        for i in range(1,comps.Length()+1): walk(comps.Value(i),l2,path+[nm],depth+1)
    else:
        shp=XCAFDoc_ShapeTool.GetShape_s(target).Moved(l2)
        b=Bnd_Box(); BRepBndLib.Add_s(shp,b)
        try: xmin,ymin,zmin,xmax,ymax,zmax=b.Get()
        except Exception: xmin=ymin=zmin=xmax=ymax=zmax=0
        g=GProp_GProps(); BRepGProp.VolumeProperties_s(shp,g)
        ns=0; e=TopExp_Explorer(shp,TopAbs_SOLID)
        while e.More(): ns+=1; e.Next()
        fn='p%04d.brep'%len(out); BRepTools.Write_s(shp,fn)
        out.append({'depth':depth,'type':'PART','name':nm,'inst':inst,'path':path+[nm],'bb':[round(v,1) for v in (xmin,ymin,zmin,xmax,ymax,zmax)],'vol':round(g.Mass(),0),'solids':ns,'brep':fn})
roots=TDF_LabelSequence(); tool.GetFreeShapes(roots)
for i in range(1,roots.Length()+1): walk(roots.Value(i),TopLoc_Location(),[],0)
json.dump(out,open('tree.json','w'))
print('nodes',len(out),'parts',sum(1 for o in out if o['type']=='PART'),'time %.0fs'%(time.time()-t0))
