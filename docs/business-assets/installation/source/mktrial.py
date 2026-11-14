from docx import Document
from docx.shared import Pt, Mm
from docx.enum.section import WD_ORIENT
import sys
d=Document()
s=d.sections[0]; s.page_width=Mm(210); s.page_height=Mm(297)
s.left_margin=s.right_margin=Mm(12); s.top_margin=Mm(10); s.bottom_margin=Mm(10)
st=d.styles['Normal']; st.font.name='Calibri'; st.font.size=Pt(9)
st.paragraph_format.space_after=Pt(2); st.paragraph_format.space_before=Pt(0)
def h(text,size=11):
    p=d.add_paragraph(); r=p.add_run(text); r.bold=True; r.font.size=Pt(size); return p
def line(text):
    p=d.add_paragraph(text); return p
def table(headers,rows,widths=None):
    t=d.add_table(rows=1,cols=len(headers)); t.style='Table Grid'
    for i,x in enumerate(headers):
        c=t.rows[0].cells[i]; c.text=''; r=c.paragraphs[0].add_run(x); r.bold=True; r.font.size=Pt(8)
    for row in rows:
        cells=t.add_row().cells
        for i,x in enumerate(row):
            cells[i].text=''; r=cells[i].paragraphs[0].add_run(x); r.font.size=Pt(8.5)
    if widths:
        for row in t.rows:
            for i,w in enumerate(widths): row.cells[i].width=Mm(w)
    return t
h('ROAM Systems rear seat: installation trial sheet, VW Transporter T6',13)
line('Fill in one sheet for each seat position: 80mm, 115mm and 215mm (heel to lip of van). Measure, do not estimate. Take a photo for every row marked (photo). Results go into the revised installation guide.')
h('1. Vehicle and position')
table(['Reg','Model / year','Wheelbase (SWB / LWB)','Rear doors (tailgate / barn)','Frame (Standard / Full Width)'],[['','','','','']])
table(['Floor build-up (ply mm / insulation)','Seat position, heel to lip (mm)','Date','Completed by'],[['','80  /  115  /  215  /  other: ____','','']])
h('2. Checks at this position (rear doors or tailgate closed)')
table(['Check','Left','Right','Notes'],[
 ['Gap between seat belt reel and rear window or door (mm) (photo)','','',''],
 ['Do the rear doors / tailgate close without clashing? (Y / N)','','',''],
 ['Height of person seated for the head check (m or ft/in)','','',''],
 ['Is their head clear of the D pillar, roof and fittings? (Y / N) (photo)','','',''],
 ['Gap from head to D pillar (mm)','','',''],
],[88,22,22,54])
h('3. The 12 fixings at this position')
line('The frame has two ski bases with 6 holes each. L = left ski, R = right ski (as seated, facing forward). Number each ski 1 to 6 from the front of the van to the rear. Look from underneath before drilling.')
rows=[[f'L{i}','','','','','',''] for i in range(1,7)]+[[f'R{i}','','','','','',''] for i in range(1,7)]
table(['Hole','Comes out through: chassis section / floor rib / flat floor','Obstruction underneath? (what)','Plate: LH or RH chassis plate / 100 x 100','Plate sits flat? (Y / N / folded)','Total thickness clamped, head to nut face (mm)','Bolt length needed (mm)'],rows,[10,42,34,30,24,26,20])
h('4. Drilling and bolts')
table(['Drill size used for the M12 holes (mm)','Bolt fit in hole (free / tight)','Bolt grade marked on head','Thread showing below the nut with the bolt length above (mm)'],[['','','','']])
h('5. Torque trial (torque wrench, tighten in steps, stop at first sign of movement)')
table(['Fixing type','Hole no. tried','Torque at which ply, floor or section starts to deform (Nm)','What deformed','Proposed torque (Nm)'],[
 ['Through flat floor or floor rib, with 100 x 100 plate','','','',''],
 ['Through the hollow rear chassis section (no anti-crush tube)','','','',''],
],[60,20,44,36,26])
h('6. Problems, anything that did not fit, photos taken')
table([''],[['\n\n\n']])
d.save(sys.argv[1])
