from docx import Document
from docx.shared import Pt, Mm
import sys
d=Document()
s=d.sections[0]; s.left_margin=s.right_margin=Mm(15); s.top_margin=s.bottom_margin=Mm(12)
st=d.styles['Normal']; st.font.name='Calibri'; st.font.size=Pt(10)
def h(t,size=11):
    p=d.add_paragraph(); r=p.add_run(t); r.bold=True; r.font.size=Pt(size)
def table(rows,widths=(95,85)):
    t=d.add_table(rows=0,cols=2); t.style='Table Grid'
    for a,b in rows:
        c=t.add_row().cells; c[0].text=a; c[1].text=b
        c[0].width=Mm(widths[0]); c[1].width=Mm(widths[1])
h('ROAM Systems rear seat system: installation handover record',14)
d.add_paragraph('To be completed by the installer and given to the vehicle owner with the copies of test summaries VO00269 and VO00270. See installation guide Revision A, section 11.')
h('Vehicle')
table([('Registration',''),('Make, model and year',''),('Wheelbase (SWB / LWB)',''),('Rear doors (tailgate / barn doors)','')])
h('Installation')
table([
 ('Seat position: distance from the ski heels to the lip of the van (mm, not less than 80)',''),
 ('Seat belt reels at least 20mm clear of the rear window, doors closed (Y / N)',''),
 ('Height of the tallest occupant checked for head clearance',''),
 ('Head clear of the D pillar, roof and fittings for that occupant (Y / N)',''),
 ('All 12 M12 fixings fitted, grade 8.8 or better (Y / N)',''),
 ('A plate fitted under every fixing (Y / N)',''),
 ('At least two full threads showing through every nyloc nut (Y / N)',''),
 ('"Not for use when travelling" label fitted to each side bench (Y / N)',''),
])
h('Installer')
table([('Company',''),('Name',''),('Signature',''),('Date','')])
h('500 mile fixing check')
d.add_paragraph('All 12 seat fixings must be checked for tightness after the first 500 miles.')
table([('Date',''),('Mileage',''),('Checked by','')])
h('For the vehicle owner')
for x in ['The side bench sections are for stationary use only. Passengers must not travel on them.',
          'Anyone taller than the occupant recorded above must not travel in the rear seat until head clearance has been checked for them.',
          'The rear travel seat was independently pull tested for seat belt anchorage strength on a steel test structure. The tests were not carried out in a vehicle and are not crash tests. They do not cover the vehicle floor or the installation.']:
    d.add_paragraph(x,style='List Bullet')
d.save(sys.argv[1])
