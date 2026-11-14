import os, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, FancyArrowPatch
from PIL import Image, ImageDraw, ImageFont
F=os.path.join(matplotlib.get_data_path(),'fonts/ttf/DejaVuSans.ttf')
FB=os.path.join(matplotlib.get_data_path(),'fonts/ttf/DejaVuSans-Bold.ttf')
def font(sz,b=False): return ImageFont.truetype(FB if b else F,sz)
OUT='fig'
def label(dr,xy_text,text,target=None,sz=52,anchor='la'):
    f=font(sz)
    dr.text(xy_text,text,fill='black',font=f,anchor=anchor)
    if target:
        bb=dr.textbbox(xy_text,text,font=f,anchor=anchor)
        y=bb[3]+8
        dr.line([(bb[0],y),(bb[2],y)],fill='black',width=4)
        # leader from nearest end of underline
        sx=bb[0] if abs(bb[0]-target[0])<abs(bb[2]-target[0]) else bb[2]
        dr.line([(sx,y),target],fill='black',width=4)
        dr.ellipse([target[0]-9,target[1]-9,target[0]+9,target[1]+9],fill='black')

# ---------- sheet 1: overview + rear seat ----------
s1=Image.open('fig/src-1.png').convert('RGB'); d1=ImageDraw.Draw(s1)
d1.rectangle([2926,1448,3365,1519],fill='white')           # remove "M10 fixing holes" text, keep leader
d1.text((2932,1456),'M12 fixing holes',fill='black',font=font(54))
d1.text((2932,1534),'(6 in each ski base)',fill='black',font=font(44))
ov=s1.crop((380,150,4760,2735)); ov.save(f'{OUT}/fig1_overview.png')
rs=s1.copy(); dr=ImageDraw.Draw(rs)
dr.rectangle([1850,700,1952,1030],fill='white')          # stray leader from the small pod label
label(dr,(1990,1640),'Ski base: one each side,\nrunning front to back',target=None)
dr.line([(2560,1640),(2738,1393)],fill='black',width=4); dr.ellipse([2729,1384,2747,1402],fill='black')
rs.crop((1960,185,3760,1800)).save(f'{OUT}/fig2_rear_seat.png')

# ---------- sheet 3: plan view ----------
s3=Image.open('fig/src-3.png').convert('RGB'); d3=ImageDraw.Draw(s3)
d3.rectangle([2712,1868,2783,2080],fill='white')            # remove "115mm"
d3.text((2830,1840),'Seat position',fill='black',font=font(56,True))
d3.text((2830,1915),'Measured from the ski heels\nto the lip of the van.\nNot less than 80mm.',fill='black',font=font(48))
d3.text((1100,300),'FRONT OF VAN',fill='black',font=font(54,True))
d3.line([(1700,395),(1700,255)],fill='black',width=6); d3.polygon([(1675,265),(1725,265),(1700,215)],fill='black')
d3.text((1100,2190),'REAR DOORS (lip of van)',fill='black',font=font(54,True))
# forward arrow note at the right of the view
d3.line([(3300,1500),(3300,900)],fill='black',width=6); d3.polygon([(3275,910),(3325,910),(3300,860)],fill='black')
d3.text((3345,1050),'Move the seat forward\nfor more head clearance\nfrom the D pillar',fill='black',font=font(48))
s3.crop((480,190,4250,2290)).save(f'{OUT}/fig3_plan.png')

# ---------- schematic: side view ----------
fig,ax=plt.subplots(figsize=(9,5.2),dpi=200)
ax.set_xlim(0,180); ax.set_ylim(-12,105); ax.axis('off'); ax.set_aspect('equal')
lw=1.6
# van floor, lip, rear door, roof
ax.plot([0,150],[10,10],'k',lw=lw*1.4)                      # floor
ax.plot([150,150],[10,4],'k',lw=lw*1.4)                     # lip drop
ax.plot([152,156,158],[4,55,92],'k',lw=lw)                  # rear door outer
ax.plot([0,150,158],[96,96,92],'k',lw=lw*1.4)               # roof
ax.add_patch(Polygon([[142,96],[149.5,96],[151.5,40],[146,40]],closed=True,fc='0.88',ec='k',lw=1,ls='--'))  # D pillar
ax.text(112,101,'D pillar (rear structural pillar,\nat each side of the van)',ha='center',va='bottom',fontsize=8)
ax.annotate('',xy=(145,90),xytext=(126,101),arrowprops=dict(arrowstyle='-',lw=0.8))
ax.add_patch(Rectangle((152.5,58),3,26,fc='white',ec='k',lw=1))                # rear window
ax.text(164,71,'Rear\nwindow',fontsize=8,va='center')
# seat: ski, legs, base, back
ax.add_patch(Rectangle((92,10),44,2.2,fc='0.6',ec='k',lw=1))                 # ski
ax.text(100,5.2,'Ski base',fontsize=8,ha='center')
ax.plot([98,98],[12.2,38],'k',lw=lw); ax.plot([132,132],[12.2,38],'k',lw=lw)
ax.add_patch(Rectangle((94,38),40,4,fc='0.9',ec='k',lw=1))                   # seat base
ax.plot([132,137],[42,84],'k',lw=lw*1.5)                                      # seat back
ax.add_patch(Rectangle((136.6,68),4,7,fc='0.3',ec='k',lw=0.8,zorder=5))        # belt reel
ax.text(118,60,'Seat belt\nreel',fontsize=8,ha='right',va='center'); ax.annotate('',xy=(136.6,70.5),xytext=(119,61),arrowprops=dict(arrowstyle='-',lw=0.8))
# occupant
ax.add_patch(Circle((128,82),5.2,fc='white',ec='k',lw=1.2))
ax.plot([127,124],[77,46],'k',lw=1.2); ax.plot([124,104],[46,45],'k',lw=1.2); ax.plot([104,102],[45,14],'k',lw=1.2)
ax.text(96,86,'Head must be clear of the\nD pillar, roof and fittings',fontsize=8,ha='right',va='center'); ax.annotate('',xy=(123,83),xytext=(97,86),arrowprops=dict(arrowstyle='->',lw=0.9))
# heel to lip dimension
ax.plot([136,136],[10,-4],'k',lw=0.7); ax.plot([150,150],[4,-4],'k',lw=0.7)
ax.annotate('',xy=(136,-2),xytext=(150,-2),arrowprops=dict(arrowstyle='<->',lw=0.9))
ax.text(143,-9,'Seat position: heel to lip,\nnot less than 80mm',fontsize=8,ha='center',va='center')
ax.text(136,14.5,'Heel',fontsize=8,ha='center'); ax.text(159,1,'Lip of van',fontsize=8,va='center')
# reel gap
ax.annotate('',xy=(140.6,71.5),xytext=(152.5,71.5),arrowprops=dict(arrowstyle='<->',lw=0.9),zorder=6)
ax.text(170,52,'Reel to window:\nat least 20mm,\ndoors closed',fontsize=8,va='center'); ax.annotate('',xy=(149,71),xytext=(169,54),arrowprops=dict(arrowstyle='-',lw=0.8))
# forward arrow
ax.annotate('',xy=(40,26),xytext=(84,26),arrowprops=dict(arrowstyle='->',lw=1.6))
ax.text(62,31,'Move the seat forward for\nmore head clearance',fontsize=8.5,ha='center')
ax.text(8,14,'Van floor',fontsize=8); ax.text(8,90,'Roof',fontsize=8)
ax.text(0,-10.5,'Schematic side view. Not to scale.',fontsize=8,style='italic')
fig.savefig(f'{OUT}/fig4_side_view.png',bbox_inches='tight',pad_inches=0.1); plt.close(fig)

# ---------- schematic: section through one fixing ----------
fig,ax=plt.subplots(figsize=(7.5,5.2),dpi=200)
ax.set_xlim(0,150); ax.set_ylim(0,104); ax.axis('off'); ax.set_aspect('equal')
cx=60
def layer(y,h,x0,x1,fc,hatch=None): ax.add_patch(Rectangle((x0,y),x1-x0,h,fc=fc,ec='k',lw=1,hatch=hatch))
layer(70,5,22,98,'0.6')                       # ski base
layer(58,12,8,112,'#e9d8b6')                  # ply
layer(55,3,8,112,'0.45')                      # van floor
# spreader plate with radiused edges (top corners rounded towards floor)
from matplotlib.patches import FancyBboxPatch
ax.add_patch(FancyBboxPatch((38,51),44,4,boxstyle='round,pad=0,rounding_size=1.8',fc='0.75',ec='k',lw=1))
layer(48.6,2.4,52,68,'0.9')                   # washer
layer(41,7.6,53,67,'0.55')                    # nyloc nut
layer(75,2.2,52,68,'0.9')                     # washer under head
layer(77.2,7,53,67,'0.35')                    # bolt head
ax.add_patch(Rectangle((cx-3,33),6,44.2,fc='0.85',ec='k',lw=1))   # shank
for yy in (34.5,36.5,38.5): ax.plot([cx-3,cx+3],[yy,yy+0.8],'k',lw=0.6)
def lab(txt,xy,xt,yt): 
    ax.annotate(txt,xy=xy,xytext=(xt,yt),fontsize=8,va='center',arrowprops=dict(arrowstyle='-',lw=0.8))
lab('M12 bolt, grade 8.8 minimum\n(check marking on head)',(66,81),118,90)
lab('Washer',(68,76),118,80)
lab('Ski base of seat frame',(96,72.5),118,72)
lab('12mm ply floor',(110,64),118,64)
lab('Van floor or chassis section',(110,56.5),118,56)
lab('Spreader plate under every bolt,\nat least 100 x 100 x 4mm,\nradiused edges towards the floor',(80,53),118,46)
lab('M12 nyloc nut',(67,44),118,36)
lab('At least two full threads\nshowing through the nut',(63,36),118,27)
ax.text(0,22,'Section through one fixing. Not to scale.\n12 fixings in total: 6 in each ski.',fontsize=8,style='italic')
fig.savefig(f'{OUT}/fig5_fixing_section.png',bbox_inches='tight',pad_inches=0.1); plt.close(fig)

# ---------- schematic: plate folded against a chassis member ----------
fig,ax=plt.subplots(figsize=(7.5,3.6),dpi=200)
ax.set_xlim(0,150); ax.set_ylim(18,78); ax.axis('off'); ax.set_aspect('equal')
ax.add_patch(Rectangle((5,60),105,3,fc='0.45',ec='k',lw=1))                 # floor
ax.text(66,66,'Van floor (side view; underside below)',fontsize=8)
ax.add_patch(Rectangle((20,34),16,26,fc='0.8',ec='k',lw=1))                 # chassis member
ax.text(28,47,'Chassis\nmember',fontsize=8,ha='center',va='center')
# folded plate: horizontal leg under floor, vertical leg down the member face
ax.plot([36.8,82],[58.6,58.6],color='k',lw=4,solid_capstyle='butt'); ax.plot([37.2,37.2],[59,40],color='k',lw=4,solid_capstyle='butt')
ax.add_patch(Rectangle((51,38),5,28,fc='0.85',ec='k',lw=1))                 # bolt
ax.add_patch(Rectangle((47,50.5),13,6.5,fc='0.55',ec='k',lw=1))             # nut
ax.annotate('',xy=(36,31),xytext=(53.5,31),arrowprops=dict(arrowstyle='<->',lw=0.9)); ax.text(44.5,25,'Bolt within 50mm\nof the member',fontsize=8,ha='center',va='center')
ax.annotate('Fold the plate so the fold sits snugly\nagainst the member.\nDo not cut the plate down.',xy=(37.5,45),xytext=(92,44),fontsize=8,va='center',arrowprops=dict(arrowstyle='->',lw=0.9))
ax.annotate('Spreader plate',xy=(72,58.4),xytext=(92,56),fontsize=8,va='center',arrowprops=dict(arrowstyle='-',lw=0.8))
ax.text(92,24,'Schematic. Not to scale.',fontsize=8,style='italic')
fig.savefig(f'{OUT}/fig6_folded_plate.png',bbox_inches='tight',pad_inches=0.1); plt.close(fig)
print('figs ok')
