import pickle, math, sys, datetime
import ezdxf
from ezdxf.enums import TextEntityAlignment
S=sys.argv[1]; OUT=sys.argv[2]
H=pickle.load(open(S+'/hc/hlr.pkl','rb'))
tx=lambda p:(round(p[0]-91,2),round(-p[1]+485,2))   # front of van to the LEFT; x=0 ski heel, y=0 floor under skis
R=(-427.0,515.0)          # DVSA s31 method on the model cushions: 515 above floor, 427 forward of heel
CUSH=462.0                # top of base cushion (uncompressed), above floor
doc=ezdxf.new('R2018',setup=True); doc.units=ezdxf.units.MM
msp=doc.modelspace()
L={ 'SEAT_FRAME':7,'SEAT_CUSHIONS':30,'HEAD_REST_CONCEPT':40,'DATUM_FLOOR_HEEL':7,'LIP_DATUMS':5,'R_POINT':1,
    'IVA_S12_HEAD_IMPACT_ZONE':3,'VSB5_ADULT_R890_NOT_UK':6,'SAE_HEADROOM_8DEG':4,'HEAD_TOP_LEVELS':2,
    'D_PILLAR_TAPE_1300':1,'VAN_ROOF':8,'VAN_D_PILLAR':8,'VAN_REAR_GLASS':8,'VAN_BELT_REELS':8,
    'REF_CHILD_8-9Y_P95':9,'NOTES':7}
for n,c in L.items(): doc.layers.add(n,color=c)
doc.layers.get('REF_CHILD_8-9Y_P95').off()
def pl(pts,layer,**k): msp.add_lwpolyline(pts,dxfattribs={'layer':layer,**k})
def txt(s,p,h,layer,align=TextEntityAlignment.LEFT,rot=0):
    msp.add_text(s,height=h,rotation=rot,dxfattribs={'layer':layer,'style':'OpenSans'}).set_placement(p,align=align)
for layer,polys in H.items():
    for p in polys: pl([tx(q) for q in p],layer)
# datums
pl([(-1100,0),(500,0)],'DATUM_FLOOR_HEEL'); pl([(0,-60),(0,60)],'DATUM_FLOOR_HEEL')
txt('FLOOR UNDER SKIS',( -1095,-28),14,'DATUM_FLOOR_HEEL'); txt('SKI HEEL (x=0)',(0,-80),14,'DATUM_FLOOR_HEEL',TextEntityAlignment.CENTER)
for d in (80,115,215):
    pl([(d,-40),(d,1450)],'LIP_DATUMS',linetype='DASHED')
    txt('VAN LIP if seat at %dmm'%d,(d-4,1180),13,'LIP_DATUMS',rot=90)
# R point
msp.add_circle(R,8,dxfattribs={'layer':'R_POINT'}); pl([(R[0]-25,R[1]),(R[0]+25,R[1])],'R_POINT'); pl([(R[0],R[1]-25),(R[0],R[1]+25)],'R_POINT')
txt('R POINT (seat reference point)',(R[0]-35,R[1]+14),14,'R_POINT',TextEntityAlignment.RIGHT)
txt('515 above floor, 427 forward of heel',(R[0]-35,R[1]-8),12,'R_POINT',TextEntityAlignment.RIGHT)
# backrest reference line 13 deg from vertical through R (DVSA torso line)
a=math.radians(90-13); pl([R,(R[0]+950*math.cos(a), R[1]+950*math.sin(a))],'R_POINT',linetype='DASHDOT')
txt('backrest line 13 deg',(R[0]+700*math.cos(a)+12,R[1]+700*math.sin(a)),11,'R_POINT')
# IVA s12 head impact zone: head-top reach 736-840 above R (sweep angles not stated in the manual)
for r in (736,840):
    msp.add_arc(R,r,0,180,dxfattribs={'layer':'IVA_S12_HEAD_IMPACT_ZONE','linetype':'DASHED'})
txt('IVA M1 s12 head impact zone: top of 165mm head form',(R[0]-855,R[1]+300),13,'IVA_S12_HEAD_IMPACT_ZONE',TextEntityAlignment.RIGHT)
txt('736-840 above R point. Reach of the test apparatus, not a clearance.',(R[0]-855,R[1]+278),11,'IVA_S12_HEAD_IMPACT_ZONE',TextEntityAlignment.RIGHT)
txt('Sweep angles not stated in the manual.',(R[0]-855,R[1]+258),11,'IVA_S12_HEAD_IMPACT_ZONE',TextEntityAlignment.RIGHT)
# VSB5 adult R890, 45 deg forward (left) to 25 deg rearward (right) of vertical
msp.add_arc(R,890,65,135,dxfattribs={'layer':'VSB5_ADULT_R890_NOT_UK'})
for ang in (65,135):
    t=math.radians(ang); pl([R,(R[0]+890*math.cos(t),R[1]+890*math.sin(t))],'VSB5_ADULT_R890_NOT_UK')
t=math.radians(135); txt('VSB 5 adult head space R890 (Australia, NOT UK law)',(R[0]+890*math.cos(t)-10,R[1]+890*math.sin(t)+10),13,'VSB5_ADULT_R890_NOT_UK',TextEntityAlignment.RIGHT)
# SAE headroom line 8 deg rearward of vertical
t=math.radians(82); pl([R,(R[0]+1000*math.cos(t),R[1]+1000*math.sin(t))],'SAE_HEADROOM_8DEG',linetype='DASHDOT')
txt('SAE headroom line, 8 deg rearward of vertical',(R[0]+1000*math.cos(t)-8,R[1]+1000*math.sin(t)+8),12,'SAE_HEADROOM_8DEG',TextEntityAlignment.RIGHT)
# head-top levels, upright, uncompressed cushion: cushion top + sitting height
for lab,sh in (("5th % woman",795),("1.68m person",881),("average man",910),("95th % man",965)):
    y=CUSH+sh; pl([(-760,y),(160,y)],'HEAD_TOP_LEVELS')
    txt('%s  %d above floor (%d above R)'%(lab,y,y-R[1]),(-765,y+3),12,'HEAD_TOP_LEVELS',TextEntityAlignment.RIGHT)
# D pillar underside, owner's tape 15/11/2026; fore-aft position not drawn (lip to door face unknown)
pl([(-200,1300),(400,1300)],'D_PILLAR_TAPE_1300',linetype='DASHED')
txt('D PILLAR UNDERSIDE 1300 (owner tape 15/11/2026, floor datum unconfirmed, fore-aft position not drawn)',(405,1295),12,'D_PILLAR_TAPE_1300')
# placeholders for ramp data
for n in ('VAN_ROOF','VAN_D_PILLAR','VAN_REAR_GLASS','VAN_BELT_REELS'):
    pass
# notes
N=['ROAM REAR SEAT - HEAD CLEARANCE SIDE VIEW (front of van to the left)',
 'Romark Engineering Limited. Drawn 16/11/2026 from SolidWorks export "2022 Bed system full assy" (third upload, 15/11/2026). 1:1, mm.',
 'Section through the rear travel seat only. Side benches, pods and the under-seat drawer are omitted. Owner\'s stand-in D pillar bar removed (not a real van position).',
 'R point placed by the DVSA IVA M1 manual s31 method (136 x 53mm distance piece) on the modelled cushions, backrest 13 deg. Handover offsets (137 fwd / 86 up) would put it 33mm higher.',
 'Head-top levels: upright posture on the uncompressed cushion (462 above floor) + sitting height from the handover (Pheasant, secondary). Cushion compression lowers real heads; the 13 deg recline lowers them about 2.5%.',
 'Lip datums: van lip position for the seat at 80, 115 and 215mm (straight edge across the ski heels to the lip). Van layers VAN_* are empty, for the T6 ramp measurements.',
 'Not a test result. The seat was pull tested on a steel test structure, not in a vehicle; head clearance is not covered by the tests.']
for i,s in enumerate(N): txt(s,(-1100,-150-i*24),14 if i==0 else 11,'NOTES')
# document properties
doc.header['$LASTSAVEDBY']='Robert di Capite'
doc.header.custom_vars.append('Company','Romark Engineering Limited')
doc.header.custom_vars.append('Author','Robert di Capite')
doc.header.custom_vars.append('Title','ROAM Rear Seat - Head Clearance Side View')
from ezdxf.entities import XRecord
xr=doc.objects.add_xrecord(doc.rootdict.dxf.handle)
xr.reset([(1,'DWGPROPS COOKIE'),(2,'ROAM Rear Seat - Head Clearance Side View'),(3,'Rear travel seat, head clearance reference layers'),
          (4,'Robert di Capite'),(6,'Romark Engineering Limited'),(7,'ROAM; head clearance; IVA M1 s12; VSB 5'),(8,'Robert di Capite'),(9,'A'),
          (300,'Company=Romark Engineering Limited')])
doc.rootdict['DWGPROPS']=xr
doc.saveas(OUT); print('saved',OUT)
