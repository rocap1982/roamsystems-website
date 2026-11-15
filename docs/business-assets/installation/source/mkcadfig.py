import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle
import math
HZ=[-72,-36,78,210,340,534]; HEEL=-91; XR=557
# ---------- plan view of fixing holes ----------
fig,ax=plt.subplots(figsize=(9.5,6.2),dpi=170)
ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-980,1010); ax.set_ylim(-260,760)
ax.add_patch(Rectangle((-617,-91),1234,670,fc='none',ec='0.6',lw=0.8,ls='--'))
for sx in (-1,1):
    ax.add_patch(Rectangle((sx*577-40,-91),80,670,fc='0.9',ec='k',lw=1))
    for z in HZ: ax.add_patch(Circle((sx*XR,z),6.25,fc='white',ec='k',lw=1))
ax.text(0,480,'FRONT OF VAN',ha='center',fontsize=9,weight='bold'); ax.annotate('',xy=(0,470),xytext=(0,390),arrowprops=dict(arrowstyle='->',lw=1.2))
ax.text(0,-150,'REAR: heel of each ski (the datum for "heel to lip")',ha='center',fontsize=8.5,weight='bold')
ax.plot([-660,660],[HEEL,HEEL],color='k',lw=0.6,ls=':')
names=['6 (rear)','5','4','3','2','1 (front)']
for z,n in zip(HZ,names):
    ax.plot([XR+12,760],[z,z],color='0.4',lw=0.5)
    ax.text(770,z,f'{z-HEEL:.0f}mm from heel   hole {n}',fontsize=8,va='center')
for a,b in zip(HZ[:-1],HZ[1:]):
    ax.text(-770,(a+b)/2,f'pitch {b-a}mm',fontsize=8,va='center',ha='right'); ax.plot([-760,-XR-12],[(a+b)/2,(a+b)/2],color='0.7',lw=0.4)
ax.annotate('',xy=(-XR,640),xytext=(XR,640),arrowprops=dict(arrowstyle='<->',lw=0.9)); ax.text(0,650,'1114mm between hole rows',ha='center',fontsize=8.5)
ax.text(-577,-125,'Ski (as seated: right)',ha='center',fontsize=8); ax.text(577,-125,'Ski (as seated: left)',ha='center',fontsize=8)
ax.text(0,250,'Seat frame outline\n1234 x 670mm',ha='center',fontsize=8,color='0.4')
ax.text(-980,-235,'12 holes, 12.5mm diameter, measured from the SolidWorks model "2022 Bed system full assy". Holes 3 to 6 pass through the ski plus a 5mm flat and an angle; holes 1 and 2 through the 2mm ski only.',fontsize=7.2,style='italic')
fig.savefig('fig/cad_hole_pattern.png',bbox_inches='tight',pad_inches=0.1); plt.close(fig)

# ---------- side elevation with DVSA reference heights ----------
F=-485.0
def h(y): return y-F
fig,ax=plt.subplots(figsize=(9.5,6.6),dpi=170)
ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-980,1330); ax.set_ylim(-200,1480)
ax.plot([-400,1000],[0,0],'k',lw=1.6); ax.text(985,-45,'Finished floor',ha='right',fontsize=8)
ax.add_patch(Rectangle((-91,0),670,37,fc='0.6',ec='k',lw=0.8)); ax.text(240,-45,'Ski base, 670mm long',ha='center',fontsize=8)
ax.add_patch(Rectangle((153,h(-73)),426,50,fc='#d9d2c5',ec='k',lw=0.8)); ax.text(430,h(-73)-38,'Base cushion, top 462mm above floor',fontsize=8,ha='center')
# backrest cushion: front face from (z=201,y=-23) to (z=62,y=580); thickness ~190 along z
bf=[(201,h(-23)),(62,h(583)),(10,h(591)),(151,h(-28))]
ax.add_patch(Polygon(bf,closed=True,fc='#d9d2c5',ec='k',lw=0.8))
ax.text(-60,h(60),'Backrest, 13 deg\nfrom vertical',fontsize=8,ha='right',va='center')
# R point
Rz,Rh=201+136,h(-23)+53
ax.add_patch(Rectangle((201,h(-23)),136,53,fc='0.75',ec='k',lw=0.6))
ax.plot(Rz,Rh,'ko',ms=4); ax.annotate("R point (DVSA 136 x 53mm block):\n515mm above floor, 427mm forward of heel",xy=(Rz,Rh),xytext=(520,640),fontsize=8,arrowprops=dict(arrowstyle='-',lw=0.7))
# upper anchorage and top
ax.plot(-24,h(484),'ks',ms=5); ax.annotate('Belt upper anchor bolt holes:\n969mm above floor (454mm above R)',xy=(-24,h(484)),xytext=(-960,820),fontsize=8,arrowprops=dict(arrowstyle='-',lw=0.7))
ax.annotate('Top of backrest, where the webbing\ncomes over: about 1066 to 1076mm above floor\n(about 550mm above R)',xy=(40,h(588)),xytext=(-960,1130),fontsize=8,arrowprops=dict(arrowstyle='-',lw=0.7))
# heel
ax.plot([-91,-91],[0,-50],'k',lw=0.6); ax.text(-91,-85,'Heel',ha='center',fontsize=8)
# head impact zone band
for hh,lab in ((Rh+736,'736mm above R = 1251mm above floor'),(Rh+840,'840mm above R = 1355mm above floor')):
    ax.plot([-200,900],[hh,hh],color='0.3',lw=0.8,ls='--'); ax.text(905,hh,lab,fontsize=8,va='center')
ax.add_patch(Rectangle((-200,Rh+736),1100,104,fc='0.9',ec='none',alpha=0.6)); ax.text(480,Rh+788,'Top of DVSA head impact zone (165mm sphere)',ha='center',va='center',fontsize=8.5)
ax.annotate('',xy=(Rz,Rh+736),xytext=(Rz,Rh),arrowprops=dict(arrowstyle='<->',lw=0.7))
ax.annotate('',xy=(830,160),xytext=(640,160),arrowprops=dict(arrowstyle='->',lw=1.3)); ax.text(735,185,'FRONT',ha='center',fontsize=8.5,weight='bold')
ax.text(-960,-185,'Side elevation built from the SolidWorks model (cushions uncompressed). R point located with the DVSA distance-piece method, IVA manual section 31 Figure 2. Not a substitute for measuring a real seat.',fontsize=7.2,style='italic')
fig.savefig('fig/cad_side_elevation.png',bbox_inches='tight',pad_inches=0.1); plt.close(fig)
print('ok')
