from docx import Document
from docx.shared import Pt, Mm
import sys
d=Document()
s=d.sections[0]; s.left_margin=s.right_margin=Mm(13); s.top_margin=Mm(11); s.bottom_margin=Mm(10)
st=d.styles['Normal']; st.font.name='Calibri'; st.font.size=Pt(9.5)
st.paragraph_format.space_after=Pt(2)
def h(t,size=11):
    p=d.add_paragraph(); r=p.add_run(t); r.bold=True; r.font.size=Pt(size)
def line(t): d.add_paragraph(t)
def bl(items):
    for it in items: d.add_paragraph(it,style='List Bullet')
def table(head,rows,widths=None):
    t=d.add_table(rows=1,cols=len(head)); t.style='Table Grid'
    for i,x in enumerate(head):
        c=t.rows[0].cells[i]; c.text=''; r=c.paragraphs[0].add_run(x); r.bold=True; r.font.size=Pt(8.5)
    for row in rows:
        cs=t.add_row().cells
        for i,x in enumerate(row):
            cs[i].text=''; r=cs[i].paragraphs[0].add_run(x); r.font.size=Pt(8.5)
    if widths:
        for row in t.rows:
            for i,w in enumerate(widths): row.cells[i].width=Mm(w)

# ---------- page 1: underbody survey ----------
h('ROAM Systems rear seat: underbody survey sheet (ramp inspection)',13)
line('Purpose: map the structure under the rear floor so spreaders and plates can be designed for the whole range of seat positions, not for one position. Measure everything from two datums: the lip of the van (rear) and the vehicle centreline. Photograph every row with a tape or rule in the shot.')
h('1. Vehicle')
table(['Reg','Make / model / year','Wheelbase','Rear doors (tailgate / barn)','Date','Surveyed by'],[['','','','','','']])
h('2. Structure under the floor, from the lip forward to about 900mm')
line('One row for each chassis rail, crossmember or other structural member. L = left, R = right, as seated facing forward.')
rows=[[str(i),'','','','','','',''] for i in range(1,9)]
table(['No.','Member: rail / crossmember / other','Runs: front-back or across','Distance from lip: near edge / far edge (mm)','Distance from centreline: near edge / far edge (mm), L or R','Width x depth (mm)','Open or closed (hollow) section; internal walls?','Wall thickness if measurable (mm)'],rows,[9,28,20,26,30,20,28,22])
h('3. Floor panel')
table(['Floor panel thickness (mm)','Rib height and pitch (mm)','Underseal / coating','Corrosion seen? Where'],[['','','','']])
h('4. Obstructions and things that must not be drilled or trapped')
table(['Item','Present? (Y / N)','Position from lip and centreline (mm)','Clearance needed / notes'],[
 ['Spare wheel and cage','','',''],['Exhaust and heat shield','','',''],['Fuel tank, filler and lines','','',''],
 ['Brake lines and handbrake cables','','',''],['Wiring looms and connectors','','',''],['Rear suspension mounts','','',''],['Other','','',''],
],[52,22,52,57])
h('5. Existing strong points worth using')
line('Note any factory threaded points, captive nuts, seat or belt mounting points and lashing ring mounts within reach of the ski positions: position, thread size, what they are for.')
table([''],[['\n\n']])
h('6. Where the ski holes land')
line('Mark the 12 ski holes (L1-L6, R1-R6, front to rear) on the underside for the seat at 80mm, 115mm and 215mm. Use the one-page trial sheet for each position. Photograph the marked underside square-on, with the lip in shot.')

# ---------- page 2: design brief ----------
d.add_page_break()
h('ROAM Systems rear seat: design brief for underbody spreaders and plates',13)
line('Draft for Rob di Capite. This lists what the design has to do and what is still needed before it can be drawn. It is not a design.')
h('What "compliant" can mean')
bl([
 'No regulation gives a plate size for this seat. The benchmark is the DVSA IVA M1 Inspection Manual (July 2025), section 19, which is what an examiner works from.',
 'For a double seat with integral three-point belts, DVSA says it is "extremely difficult to restrain such a seat using simple reinforcements alone" and that "documentary evidence that the installation can satisfy the Directive requirements in-vehicle should be sought".',
 'So the design is compliant when it has been shown to work: by an in-vehicle or representative-floor pull test, or by a calculation a test house accepts. Design to be tested.',
])
h('Requirements taken from the DVSA manual')
table(['Requirement','DVSA wording'],[
 ['Every fixing used','"ALL the mounting holes provided… must be utilized."'],
 ['Load taken into structure','Look for "seats fixed to vehicle structural areas, i.e., box sections" and "spreader plates to spread loads into structural areas". Cause for concern: "seats mounted on flat panels, non-structural areas of vehicle floor".'],
 ['Minimum plate','"load spreading plates at least 100 x 100 x 4mm thick" (figure given for a fixed single seat).'],
 ['Double seats','A plate "in the region of 5mm thick, 150mm long and at least the width of the complete seat"; "angle or channel sections of similar or greater rigidity… may also be used".'],
 ['Under-floor members','Channel "of a minimum nominal size of 50x25x4mm… flanges facing downwards"; ends "free of sharp edges, which may tear the vehicle floor under load". Joints in such members "can weaken the overall structure".'],
 ['Edges','"radiused to a minimum of 2.5mm, the radius must be presented towards the floor".'],
 ['Near a chassis member','Within 50mm, "the plate may be folded (not reduced in size)… the fold should abut snugly against the chassis member".'],
 ['Slots','"Suitable arrangements… (e.g., oversized washers) to prevent the nut or the head of the bolt from pulling through the slot".'],
 ['Hollow sections','Bolts through hollow members "should be fitted with anti-crush tubes".'],
 ['Obstructions','A fastener above an obstruction "must pass into an object of similar strength to the other reinforcing members".'],
 ['Bolts','"grade 8.8 or better", marked on the head.'],
],[42,142])
h('Design points to settle')
bl([
 'Range: the seat can sit from 80mm forward with no fixed limit. Either the spreaders work across that range (slots or hole patterns), or the range is narrowed to what the spreaders cover.',
 'One strip under each ski linking all six fixings, tied to the chassis where it crosses, against twelve loose plates. A strip spreads load better and is harder to fit wrongly; loose plates suit more vehicles.',
 'The rear fixings carry the uplift. DVSA\'s example: on pedestals about 350mm high "the upward load on the rear seat legs might well be in the region of 6 tonnes". The ROAM legs are 395mm.',
 'The hollow rear chassis section: no room for anti-crush tubes because of its internal walls. Options to look at on the ramp: fix through one wall only into a plate inside or behind, clamp around the section, or pick up an existing strong point.',
 'Corrosion: the parts live under the van. Finish and drain so they do not trap water against the floor.',
 'One kit for all vehicles, or one underbody kit per vehicle. The frame is common; the underside of a T6, a Transit Custom and a Trafic is not.',
])
h('Inputs still needed')
bl([
 'The underbody survey (page 1) and the three trial sheets.',
 'The loads actually applied in tests VO00269 and VO00270, from the full VOSC test reports. Only the one-page summaries are on file.',
 'The ski drawing: hole positions along each ski and the spacing between skis (leg span 1230mm on the test summary).',
 'What VOSC would need to see to accept the new underbody parts: a test on a van, on a floor section, or a calculation.',
])
d.save(sys.argv[1])
