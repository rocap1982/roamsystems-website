from docx import Document
from docx.shared import Pt, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH
import sys
d=Document()
s=d.sections[0]; s.left_margin=s.right_margin=Mm(16); s.top_margin=s.bottom_margin=Mm(14)
st=d.styles['Normal']; st.font.name='Calibri'; st.font.size=Pt(10)
def para(t,bold=False,italic=False):
    p=d.add_paragraph(); r=p.add_run(t); r.bold=bold; r.italic=italic; return p
def bl(items):
    for it in items: d.add_paragraph(it,style='List Bullet')
def table(head,rows,widths):
    t=d.add_table(rows=1,cols=len(head)); t.style='Light Grid Accent 1'; t.autofit=False
    for i,h in enumerate(head):
        c=t.rows[0].cells[i]; c.text=''; r=c.paragraphs[0].add_run(h); r.bold=True; r.font.size=Pt(9)
    for row in rows:
        cs=t.add_row().cells
        for i,v in enumerate(row):
            cs[i].text=''; r=cs[i].paragraphs[0].add_run(v); r.font.size=Pt(9)
    for i,w in enumerate(widths): t.columns[i].width=Mm(w)
    for row in t.rows:
        for i,w in enumerate(widths): row.cells[i].width=Mm(w)
    d.add_paragraph()
def fig(path,w,cap):
    d.add_picture(path,width=Mm(w)); d.paragraphs[-1].alignment=WD_ALIGN_PARAGRAPH.CENTER
    p=d.add_paragraph(); r=p.add_run(cap); r.italic=True; r.font.size=Pt(8.5); p.alignment=WD_ALIGN_PARAGRAPH.CENTER

d.add_heading('ROAM rear seat: measurements from the SolidWorks model against the DVSA list',0)
para('Model: "2022 Bed system full assy.STEP" (SolidWorks 2025 export, AP214), supplied by Rob di Capite on 15 November 2026. 68 parts read. Review dated 15 November 2026.',bold=True)
para('What this is: measurements taken from the CAD geometry. It shows what was drawn, not what was built or tested. Steel grade, weld sizes, belts and reels are not in the model. The cushions are in the model and were used; they are uncompressed.')

d.add_heading('1. Results against the DVSA items',1)
W=[30,58,62,28]
table(['DVSA item','Requirement','Measured from the model','Result'],[
 ['31 RS18, lower anchorages','"at least 350mm apart"','Four 12mm holes on the belt and ISOFIX bar at x = -564, -192, -108 and +264mm. Each seat\'s pair is 372mm apart.','Meets, 22mm margin'],
 ['31 RS17, upper anchorage offset','"at least 140mm from the longitudinal centre line of the seat"','Upper housings centred at x = -520 and +220mm. Seat centres, taken as midway between each pair of lower anchorages, are -378 and +78mm. Offset 142mm on both.','Meets, 2mm margin'],
 ['31 RS16, upper anchorage height','"at least 450mm above the reference point"','R point found with DVSA\'s 136 x 53mm distance piece on the base cushion: 515mm above the floor. The 11mm upper anchor bolt holes are 454mm above it. The top of the backrest, where the webbing comes over, is about 550mm above it.','Meets. 4mm margin if measured to the bolt holes; about 100mm if measured to the top of the backrest'],
 ['15 RS3, locking','Automatic locking of seat back adjustment and displacement systems','The backrest is a fixed welded frame with no adjustment. The seat base is a separate cushion frame with a "Latch assy" at its front edge. The model does not show whether that latch engages by itself.','Backrest: not applicable. Base: not known'],
 ['15 RS6 to RS8, head restraints','Not required on rear seats. If fitted, top at least 700mm above R','No head restraints. The top of the backrest cushion is 561mm above the R point.','Nothing to meet. See section 2'],
 ['19, all mounting holes','"ALL the mounting holes… must be utilized"','12 holes, 12.5mm diameter, six per ski, in two rows 1114mm apart. From the heel: 19, 55, 169, 301, 431 and 625mm.','Count confirmed'],
 ['19, plates','"at least 100 x 100 x 4mm"; larger or extra reinforcement where mountings are "within approx. 200mm of each other"','Hole pitches along each ski: 36, 114, 132, 130 and 194mm. Every hole is within 200mm of its neighbour. The rear two are 36mm apart, so two separate 100mm plates cannot fit there.','A plate under every bolt cannot be done as separate 100 x 100 plates'],
 ['19 Annex 3, frame','Upper anchorage braced to the lower structure; concern over thin sections','Folded sheet construction, about 2mm: double-skin side frames, a 1230 x 215 x 80mm top beam carrying the upper anchorages, a 161 x 153mm fabricated bar carrying the lower anchorages. 25 x 25 x 1.5mm box bracing. Skis are an 80 x 37mm channel, about 2mm.','Braced by design. Thin sections throughout; this is the frame VOSC pull tested'],
 ['19 Annex 3, ski fixings','"Insufficient bolt capacity" and anchorages in thin panels are causes for concern','Holes 3 to 6 on each ski pass through the ski plus a 5mm flat and an angle. Holes 1 and 2, at the front, pass through the 2mm ski only.','Front two holes per ski bear on 2mm sheet: specify the washer'],
 ['IVA 19a, seat mass','Maximum seat weight is a tested parameter (67.8kg)','Steel and aluminium of the rear seat as modelled: about 54kg. About 90 litres of foam, the cushion boards, belts and reels are extra.','Consistent with 67.8kg being the trimmed seat. Weigh one to confirm'],
 ['IVA 19a, leg height','Maximum leg height is a tested parameter (395mm)','Floor to the underside of the seat base frame: 387mm. Floor to the top of the base cushion: 462mm.','Consistent'],
 ['Tested width','VOSC: "1580mm Width"','Rear seat cushion frame is 1580mm wide. The model\'s side pod is the "FULL WIDTH" version.','Supports the owner\'s statement that Full Width has the tested rear section'],
 ['General Construction, pods','Attachments "of adequate strength"','Pods are held at the floor by 30 x 30 x 3mm corner tabs with 5 and 6mm holes.','Consistent with woodscrews into ply. Gap stands'],
],W)

d.add_heading('2. Head clash with the rear header',1)
para('The owner\'s photograph marks the rear header rail and the tops of the D pillars, above and behind the backrest, as the potential head clash point.')
bl([
 'The top of the backrest cushion is 1076mm above the finished floor and 561mm above the R point. An adult\'s head is above it. There is no head restraint, so nothing limits rearward movement of the head before the header rail and the rear window.',
 'DVSA\'s head impact zone reaches from 736mm to 840mm above the R point. On this seat that is 1251mm to 1355mm above the finished floor.',
 'With the seat set at a heel-to-lip distance L, the front face of the backrest top is L + 153mm forward of the lip, and the R point is L + 427mm forward of the lip. At L = 80mm the backrest top is 233mm from the lip; at L = 215mm it is 368mm.',
 'What the model cannot give: the height of the header rail\'s lower edge above the floor, and how far forward of the lip it sits. Those two measurements from the van, or the scan, turn "about 5ft 6" into a figure for each seat position.',
 'DVSA\'s manual does not prohibit this. Its roof standard does not apply "to parts covered with a non-rigid material", and it excepts "the header rail of glazed surfaces and door frames" from the limit on downward projection. The concern is a safety judgement, not an IVA failure.',
])

d.add_heading('3. Where the belted seats are',1)
bl([
 'The two belted positions are not centred on the frame. Their centres are at -378mm and +78mm from the frame centreline, on a frame 1234mm wide and cushions 1580mm wide.',
 'So one occupant sits near the middle and the other about 240mm inside the frame edge on the small side pod side. That outboard occupant is the one closest to a D pillar.',
 'Both belts come over the same shoulder. The ISOFIX rod is a continuous 6mm bar across the width, tied back at -400mm and +60mm, close to the two seat centres.',
])
fig('fig/cad_hole_pattern.png',175,'Figure 1. Fixing hole pattern, measured from the model.')
fig('fig/cad_side_elevation.png',165,'Figure 2. Side elevation with the DVSA reference heights, measured from the model.')

d.add_heading('4. What this means for the spreader design',1)
bl([
 'Design one part per ski, not twelve plates. The hole pitches (36 to 194mm) put every fixing inside DVSA\'s 200mm rule, and the rear pair cannot take separate plates at all.',
 'The part is 1114mm apart side to side and has to cover holes spread over 606mm front to back, from 19mm to 625mm ahead of the heel.',
 'The rear two holes on each side are the ones that reach the rear chassis section and carry the uplift. They are 36mm apart, which suits a single shaped plate into the chassis section, as the existing handed plates do.',
 'The front two holes on each ski go through 2mm sheet. Under load the front of the seat pushes down, so the ski needs a firm, flat seat on the floor there and a washer sized for the 2mm sheet.',
 'The model holes are 12.5mm. The guide calls for a 13mm drill through the van. With twelve holes over 1.1m by 0.6m, half a millimetre of clearance in the ski leaves little room for error when marking through.',
])

d.add_heading('5. Assumptions and limits',1)
bl([
 'R point: located with the distance piece shown in the DVSA manual (section 31, Figure 2), on the uncompressed CAD cushion, 50mm thick. A thicker cushion lowers the 454mm figure one for one.',
 'Seat centreline: taken as midway between each seat\'s lower anchorages. If the upholstery marks the seats differently, the 142mm offset changes.',
 'Thicknesses are estimated from each body\'s volume and surface area, and are good to about 0.1mm for sheet parts.',
 'The effective upper anchorage is where the webbing changes direction. The photograph shows it coming over the top of the backrest. The exact slot height was not extracted.',
 'Left and right: the model\'s axes suggest the small side pod is on the occupant\'s right. Confirm before relying on it.',
 'Not in this model: the overhead locker, the van, and the Standard-width variant.',
])
d.save(sys.argv[1])
