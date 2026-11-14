from docx import Document
from docx.shared import Pt, Mm
import sys
d=Document()
s=d.sections[0]; s.left_margin=s.right_margin=Mm(20); s.top_margin=s.bottom_margin=Mm(18)
st=d.styles['Normal']; st.font.name='Calibri'; st.font.size=Pt(10.5)
def para(text,bold=False,italic=False):
    p=d.add_paragraph(); r=p.add_run(text); r.bold=bold; r.italic=italic; return p
def bullets(items):
    for it in items: d.add_paragraph(it,style='List Bullet')
def steps(items):
    for i,it in enumerate(items,1):
        p=d.add_paragraph(); p.paragraph_format.left_indent=Mm(10); p.paragraph_format.first_line_indent=Mm(-6)
        p.add_run(f'{i}.  {it}')
FIG='fig/'
def fig(name,width,caption):
    d.add_picture(FIG+name,width=Mm(width))
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    d.paragraphs[-1].alignment=WD_ALIGN_PARAGRAPH.CENTER
    p=d.add_paragraph(); r=p.add_run(caption); r.italic=True; r.font.size=Pt(9); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
def quote(text):
    p=d.add_paragraph(); p.paragraph_format.left_indent=Mm(8); r=p.add_run('“'+text+'”'); r.italic=True; return p

d.add_heading('ROAM Systems rear seat system: installation guide',0)
para('Generic guide for experienced vehicle converters. Revision A, 13 November 2026. Approved by Romark Engineering Limited. Replaces the installation guide dated May 2025.',bold=True)
para('ROAM Systems is a trading name of Romark Engineering Limited. sales@roamsystems.co.uk')

d.add_heading('1. Who this guide is for',1)
para('ROAM Systems recommends that this seat is installed by a competent, experienced vehicle converter. This is a generic guide. The seat fits a range of vans and every vehicle is different underneath, so the installer must assess the vehicle in front of them and decide how the guidance applies.')
para('Read the whole guide before drilling. If any step cannot be carried out as written, do not use the seat for travel and contact ROAM Systems before going further.')

d.add_heading('2. What has been tested',1)
para('The rear belted travel seat has been independently tested by the Vehicle Occupant Safety Centre. The seat belt anchorages were pull tested to the M1 load requirements of ECE Regulation 14.09 (test VO00269) and the ISOFIX anchorages were tested to ECE Regulation No. 145 (test VO00270).')
para('Both were static pull tests with the seat fixed to a steel test structure with 12 M12 bolts. They were not carried out in a vehicle and they are not crash tests. The tests do not assess the vehicle floor, the installation, or the clearance between a seated occupant and the vehicle interior. Those are the installer\'s responsibility.')
para('The side bench sections are untested, have no seat belts and are for stationary use only.')

d.add_heading('3. The frame and the fitting kit',1)
para('The rear seat frame sits on two ski bases, one left and one right, running front to back. Each ski has 6 fixing holes, 12 in total. All 12 must be used.')
fig('fig1_overview.png',168,'Figure 1. The three frames: rear seat, small pod and slide-out pod. From the ROAM Systems product drawings.')
fig('fig2_rear_seat.png',120,'Figure 2. Rear seat frame, showing the ski bases, the heel and the M12 fixing holes.')
para('Check the kit before starting:')
bullets([
 '12 x M12 bolts, grade 8.8 minimum, supplied in a range of lengths. Check the grade marking on the head.',
 'M12 washers and M12 nyloc nuts for each bolt',
 '12 x steel underfloor spreader plates, one for each bolt, at least 100 x 100 x 4mm, with radiused edges',
 '2 x 4mm steel chassis plates, one left-hand and one right-hand, for the rear fixings where they meet the rear chassis section',
 '2 x "not for use when travelling" labels, one for each side bench',
 'Copies of test summaries VO00269 and VO00270, and a handover record',
])
para('If any part is missing, stop and contact ROAM Systems. Do not substitute smaller or fewer fixings. If a hole needs a longer bolt than those supplied, use an M12 bolt of grade 8.8 or better.')

d.add_heading('4. Base construction',1)
para('Suggested base: 12mm ply with insulation between the floor strengthening ribs. Ensure a flat, one-level floor. Install the seat over the finished floor.')

d.add_heading('5. Getting the seat into the vehicle',1)
steps([
 'Refer to Figures 1 and 2 for the layout of the frames, components and fixings.',
 'With the interior empty, load the rear seat sideways through the rear doors.',
 'Rotate the seat through the side sliding door so that it faces forward.',
 'Move the seat to the rear of the van.',
 'Remove the spare wheel and cage, the underbody plastic trims and panels, and the exhaust heat shield, as needed to see and reach the underside.',
])

d.add_heading('6. Choosing the seat position',1)
para('The seat position is measured from a straight edge laid between the two ski heels to the lip of the van. The position is chosen by the installer with the vehicle owner. It is a trade-off between structure, floor space and head clearance.')
fig('fig3_plan.png',165,'Figure 3. Seat position, seen from above. From the ROAM Systems product drawings.')
fig('fig4_side_view.png',150,'Figure 4. Seat position, head clearance and seat belt reel gap. Schematic, not to scale.')
para('The distances below are reference figures from a VW Transporter T6. On any vehicle, the checks in this section decide the position, not the distances.',italic=True)
bullets([
 'Rear limit, 80mm: the seat must not be set further back than 80mm. It may only be set this far back if the seat belt reels are at least 20mm clear of the rear window and the rear doors close without clashing.',
 '80mm to 115mm: as a guide, suits children and occupants up to approximately 1.68m (5ft 6in). Towards the rear of the range the fixings are closest to the rear chassis section, and there is the most floor space in front of the seat. Head clearance to the D pillar is at its least.',
 'Beyond 115mm: needed where taller occupants will travel in the seat. Moving the seat forward gives more head clearance from the D pillar. As a guide, around 215mm is needed for occupants taller than approximately 1.68m (5ft 6in). It reduces the floor space in front of the seat, and the rear fixings may no longer pass through the rear chassis section.',
 'There is no fixed forward limit. The seat may be set further forward than 215mm, provided every fixing is secured on the underside as set out in section 7.',
])
para('Head clearance check. This must be done before drilling:',bold=True)
steps([
 'Place the seat at the intended position, square to the van.',
 'Seat the tallest person who will travel in the seat, upright, in each belted position.',
 'Check that their head is clear of the D pillar, the roof and any fittings, and that there is nothing hard or sharp within reach of the head.',
 'If it is not clear, move the seat forward and check again.',
 'If clearance cannot be achieved at a position where every fixing can be secured as set out in section 7, the seat must not be used for travel by that person. Tell the vehicle owner in writing.',
])
para('Other checks at the chosen position:')
bullets([
 'The seat belt reels must be at least 20mm clear of the rear door window areas at any position. Check this with the rear doors or tailgate closed.',
 'Check for interference with blinds and curtains.',
 'Double check that the rear doors close without clashing.',
])

d.add_heading('7. Floor structure and fixing rules',1)
p=d.add_paragraph(); r=p.add_run('Where the strength comes from. '); r.bold=True
p.add_run('The 12 M12 grade 8.8 bolts are not the weak point of the installation. In the tests the seat held the M1 loads when fixed with 12 M12 bolts to a steel structure. In a vehicle, what decides whether the seat stays in place is the floor and how the load is spread into the vehicle structure: where each fixing lands, what it bears on underneath, and the plate under it. Give the floor, the chassis fixings and the spreader plates the most attention.')
para('Before drilling, go underneath and establish where every one of the 12 holes (6 in each ski) will come out at the chosen position. The rules below follow the DVSA guidance reproduced in Appendix A.')
bullets([
 'Use all 12 fixing holes. Do not leave a fixing out because of an obstruction underneath. Move the seat, or stop and contact ROAM Systems.',
 'Fix into structure wherever the position allows. Towards the rear of the range the rear holes pass through the rear chassis section; the holes forward of them pass through the thin floor section. As the seat is moved forward, fewer fixings meet the chassis section.',
 'Every fixing must be secured on the underside with a plate. Where the rear fixings meet the rear chassis section, use the left-hand and right-hand chassis plates. At every other fixing use one of the 12 spreader plates, fitted with its radiused edges towards the floor.',
 'Where a bolt is within 50mm of a chassis member, fold the spreader plate so the fold sits snugly against the member. Do not cut the plate down.',
 'Do not fix the seat only to flat, unsupported floor panel. Where fixings do not meet structure, the load must be spread into structure.',
 'Do not use self-tapping screws or rivnuts for any seat fixing.',
 'Anti-crush tubes are not supplied. On the VW Transporter T6 the internal walls of the rear chassis section leave no room for them. Where a bolt passes through a hollow section that does allow one, fit an anti-crush tube.',
 'The installer is responsible for confirming that the vehicle structure at every fixing point is sound and suitable. If the floor or chassis at any fixing is corroded, damaged, or cannot be fixed to as set out here, stop.',
 'Make sure no hole will damage any component attached to the van, including brake lines, fuel lines, wiring and the exhaust.',
])

fig('fig5_fixing_section.png',140,'Figure 5. Section through one fixing. Schematic, not to scale.')
fig('fig6_folded_plate.png',130,'Figure 6. Spreader plate folded against a chassis member. Schematic, not to scale.')
d.add_heading('8. Drilling',1)
steps([
 'Mark all hole positions through the fixing holes in the skis.',
 'Drill using a long series 13mm drill bit (clearance for M12). A 250mm long bit is needed where a hole passes through the rear chassis section.',
 'Keep the drill bit perpendicular to the floor.',
])

d.add_heading('9. Bolting down',1)
steps([
 'Fit all 12 M12 bolts with washers, the underfloor plates and nyloc nuts.',
 'Choose the bolt length for each hole. After tightening, each bolt must pass fully through its nyloc nut with at least two full threads showing.',
 'Tighten each fixing until the ski, the floor and the plate are fully seated and the joint is solid. Do not tighten to the point where the ply, the floor or the chassis section starts to distort. Take particular care with bolts through the hollow chassis section.',
 'Check every fixing again once all 12 are tight.',
])

d.add_heading('10. Pods, bed frame and labels',1)
bullets([
 'Small pod: place through the side door and attach to the rear seat using 2 M6 x 40mm dome head bolts. Fix the 2 floor brackets to the 12mm flooring ply using 16mm woodscrews.',
 'Slide-out pod: place through the side door and attach to the rear seat using 4 M6 x 40mm dome head bolts. Fix the 2 floor brackets to the 12mm flooring ply using 16mm woodscrews.',
 'With all three seat frames installed, check the operation of the lift-up seat. Ensure the shoot bolt aligns with the slotted pin hole.',
 'On the slide-out pod, release the catches and pull out the bed frame. Check the slot on the underside of the bed frame aligns with the bed catch mechanism on the small pod. The catch should secure the bed frame from closing.',
 'Fit one "not for use when travelling" label to each side bench, where anyone sitting there can see it.',
])

d.add_heading('11. Record and handover',1)
para('Complete the handover record and give a copy to the vehicle owner, with the copies of the test summaries:')
bullets([
 'Vehicle registration, model and wheelbase',
 'Seat position used: distance from the ski heels to the lip of the van, in mm (not less than 80)',
 'Height of the tallest occupant checked for head clearance',
 'Confirmation that all 12 M12 fixings and their plates are fitted and tightened',
 'Installer name, signature and date',
 'Space for the 500 mile fixing check: date, mileage, checked by',
])
para('Tell the vehicle owner that:')
bullets([
 'all 12 seat fixings must be checked for tightness after the first 500 miles;',
 'the side bench sections are for stationary use only;',
 'anyone taller than the occupant checked must not travel in the seat until head clearance has been checked for them.',
])

d.add_page_break()
d.add_heading('Appendix A. DVSA guidance referred to in this guide',1)
para('The extracts below are quoted from the DVSA IVA M1 Inspection Manual (July 2025), sections 12, 15 and 19. This is the manual DVSA examiners use when a vehicle is presented for Individual Vehicle Approval. It is reproduced here as a benchmark for the installer. It is not a statement that an installation made with this kit will pass IVA.')
def item(title,quotes,note=None):
    para(title,bold=True)
    for q in quotes: quote(q)
    if note: para(note)
item('Use every fixing hole',['ALL the mounting holes provided in each pedestal for securing the seat to the vehicle or tracking must be utilized.'])
item('Bolt grade',['Bolts used in structural areas should be of grade 8.8 or better. Such bolts will be marked 8.8 or 12.9 on the hexagonal head'])
item('Loads on the fixings',['On pedestals about 350mm high the upward load on the rear seat legs might well be in the region of 6 tonnes (three tonnes per seat pedestal).','In view of the extremely high loads, it is important that a thorough assessment of the load path from each anchorage to the vehicle structure is made.'])
item('Double seats with integral belts',['Double seats fitted with integral three-point belts and two or three pedestals impart significantly higher loads into the vehicle floor than a single seat imparts. As a result, it is extremely difficult to restrain such a seat using simple reinforcements alone. Documentary evidence that the installation can satisfy the Directive requirements in-vehicle should be sought.'],
 'The ROAM rear seat is a double seat with integral three-point belts on two ski bases with six fixings each. The ROAM tests were carried out on a steel test structure, not in a vehicle.')
item('Spreader plates',['load spreading plates at least 100 x 100 x 4mm thick.','spreader plates between the rear leg securing nuts and the underside of the vehicle floor.','Where the rear mounting bolts are located within 50mm of a chassis member, the plate may be folded (not reduced in size) to clear the obstruction and the fold should abut snugly against the chassis member.','Where spreader plates are fitted to seat or seat belt mountings they must be of adequate size and radiused to a minimum of 2.5mm, the radius must be presented towards the floor of the vehicle to avoid tearing the floor in the event of a frontal impact.'],
 'The plate size quoted is DVSA\'s figure for a typical fixed single seat.')
item('Slotted plates',['Suitable arrangements must be in place (e.g., oversized washers) to prevent the nut or the head of the bolt from pulling through the slot in the plate.'])
item('Hollow sections',['Seat or tracking mounting bolts that pass through hollow section reinforcing members should be fitted with “anti-crush tubes”.'])
item('Obstructions',['In cases where a fastener lies above a box section, heat shield, fuel tank or other obstruction, it must pass into an object of similar strength to the other reinforcing members.'],
 'DVSA says this about seat tracking. The same principle is applied in this guide to the seat fixings.')
item('Fixings that are not acceptable',['“Self-tapping” screws and “riv-nuts” are not considered as being of equivalent strength (unless documentary evidence can be provided).'])
item('Causes for concern',['Seats mounted on flat panels, non-structural areas of vehicle floor or open channel section material.','Lack of load spreading plates.'])
item('Seats for stationary use only (motor caravans)',['Any seats which are not for use when travelling on a public road must be clearly identified to users by means of a pictogram or a sign with appropriate text.'])
item('Head impact zone',['“Head Impact Zone” is the area contactable by a spherical head 165mm in diameter, the top of which is adjustable between 736mm and 840mm above the seat reference point','In the case of a Motor caravan, Ambulance, Hearse or wheelchair accessible vehicle this section will only apply to the areas determined to be within the head impact zone for any “designated seating position in the rear of the vehicle”.'],
 'Fittings within the head impact zone must have radiused or blunted edges.')
para('Source: Driver and Vehicle Standards Agency, IVA M1 Inspection Manual, July 2025. © Crown copyright 2025. Contains public sector information licensed under the Open Government Licence v3.0. https://www.gov.uk/government/publications/iva-manual-for-vehicle-category-m1',italic=True)
d.save(sys.argv[1])
