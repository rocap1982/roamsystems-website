from docx import Document
from docx.shared import Pt, Mm
from docx.enum.section import WD_ORIENT
import sys
d=Document()
s=d.sections[0]; s.orientation=WD_ORIENT.LANDSCAPE; s.page_width=Mm(297); s.page_height=Mm(210)
s.left_margin=s.right_margin=Mm(14); s.top_margin=s.bottom_margin=Mm(13)
st=d.styles['Normal']; st.font.name='Calibri'; st.font.size=Pt(10)
def para(t,bold=False,italic=False):
    p=d.add_paragraph(); r=p.add_run(t); r.bold=bold; r.italic=italic; return p
def bl(items):
    for it in items: d.add_paragraph(it,style='List Bullet')
def table(head,rows,widths):
    t=d.add_table(rows=1,cols=len(head)); t.style='Light Grid Accent 1'
    for i,h in enumerate(head):
        c=t.rows[0].cells[i]; c.text=''; r=c.paragraphs[0].add_run(h); r.bold=True; r.font.size=Pt(9)
    for row in rows:
        cs=t.add_row().cells
        for i,v in enumerate(row):
            cs[i].text=''; r=cs[i].paragraphs[0].add_run(v); r.font.size=Pt(9)
    t.autofit=False
    for i,w in enumerate(widths): t.columns[i].width=Mm(w)
    for row in t.rows:
        for i,w in enumerate(widths): row.cells[i].width=Mm(w)
    d.add_paragraph()

d.add_heading('ROAM Systems product review against the DVSA IVA M1 Inspection Manual',0)
para('Manual reviewed: IVA M1 Inspection Manual, Version 17, 14 July 2025 (335 pages), the file supplied by Rob di Capite on 15 November 2026 and confirmed identical to the GOV.UK copy. Review dated 15 November 2026. Not legal advice.',bold=True)

d.add_heading('1. How the review was done',1)
bl([
 'Read in full: the Foreword (including the motor caravan definition), the summarised list of requirements and the special purpose vehicle exemption table, section 12 Interior Fittings, section 15 Seat Strength, section 19 Seat Belt Anchorages (Basic and Normal versions, with Annexes 1 to 3), section 31 Seat Belts, General Construction, and the motor caravan parts of section 44 Masses and Dimensions.',
 'Read for applicability only: section 10 Electromagnetic Compatibility, section 36 Heating Systems and section 69 Electrical Safety. None applies to the ROAM products.',
 'Checked by title and application line only: the remaining sections (noise, emissions, fuel tanks, steering, brakes, lighting, glazing, tyres, couplings, anti-theft and so on). They concern the base vehicle, not furniture or seating.',
 'Also read: the DVSA seat belt anchorage declaration forms IVA 19a and 19b (version 1.6, January 2025), which the Normal IVA section 19 refers to.',
 'Skimmed, not studied: the wheelchair and seat tracking parts of section 19.',
 'Limit: I have reviewed the product from drawings, the two VOSC test summaries, the installation guide, two installer videos and the owner\'s answers. Where I cannot tell, the status is "Not known".',
])

d.add_heading('2. When the manual applies, and the two routes',1)
table(['Point','What the manual says','What it means for ROAM'],[
 ['What the manual is','"a detailed guide on the examination of vehicles submitted… under the Individual Vehicle Approval (IVA) scheme". "This manual is however not a legal interpretation of the Regulations."','It is the benchmark an examiner uses when a converted vehicle needs approval. It does not bind a private conversion of a van that is already registered.'],
 ['Basic IVA','A "visual inspection… in most cases documentary evidence of compliance is not normally required". It covers, among others, "(g) a motor caravan" (Vehicle Class M).','A conversion that meets the motor caravan definition is inspected visually. Seat belt anchorages are assessed by "Inspection".'],
 ['Normal IVA','For "a vehicle not meeting any Basic IVA vehicle class" (Class R). Seat belt anchorages require "Approval": "satisfactory evidence of compliance".','A conversion that is not a motor caravan (for example a van turned into a passenger vehicle) needs documentary evidence for the seat belt anchorages.'],
 ['Normal IVA evidence','DVSA forms IVA 19a and 19b: "the anchorage system consists of floor, seat and seat leg… all installed components in the system can be traced back to directive tested components". "DVSA is not in a position to approve vehicles where unapproved components have been used in the seatbelt anchorage system."','The ROAM seat is tested as a seat on a steel plate. There is no tested floor or seat-to-floor fixing. [Likely] On the Normal route a converter could not complete IVA 19a with the ROAM kit as it stands.'],
 ['Motor caravan definition','Seats and table, sleeping accommodation "which may be converted from the seats", cooking facilities "of a minimum of a two-ring cooking facility or a microwave… having a fuel/power source", and storage; all "rigidly fixed".','The ROAM system supplies the seats, bed and storage. The kitchen pod has a hob space but "hob not included", so the converter must add the cooking facility for the vehicle to qualify.'],
],[38,118,112])

d.add_heading('3. Review against each applicable requirement',1)
para('Status: Meets / Planned (in guide Revision A draft or the agreed kit) / Gap / Not known / Installer (falls to the converter).')
W=[24,92,96,20,36]
H=['Ref','DVSA requirement','ROAM position','Status','Action']

para('Section 15: Seat Strength',bold=True)
table(H,[
 ['15 RS1, RS2','"Every seat must be securely attached to the vehicle structure, or other obvious suitable load bearing parts". "Every seat mounting must be of adequate strength to support the loads likely to be imposed."','12 x M12 grade 8.8 through two ski bases. Proven on a steel plate only. In the van it depends on where the fixings land and what is under them.','Gap','Underbody spreader design; in-vehicle or representative-floor test.'],
 ['15 Note 3','"On a seat to which a seat belt is mounted (integral seat belt) consideration must be given to the seat mounting as part of the seat belt anchorage."','Applies in full: the belts are on the seat.','Gap','As above.'],
 ['15 RS3','"Each seat, seat back adjustment and seat displacement system must incorporate an automatic locking system which operates in all positions provided for normal use." An inertia locking device is acceptable.','The seat converts to a bed. The guide mentions a "lift-up seat", a "shoot bolt" and a "bed catch mech". I cannot tell whether the travel seat back and base lock automatically in the travel position.','Not known','Confirm how the backrest and base lock for travel. A manually set shoot bolt may not satisfy this.'],
 ['15 MoI (d)','"Seats designed for dual function as sleeper beds should be assessed in the seating mode only."','Bed mode is not assessed.','Meets','None.'],
 ['15 MoI (a), (b)','Standards "do not apply to seats intended for use solely while the vehicle is stationary", but such seats "must be clearly identified to users by means of a pictogram or a sign with appropriate text".','Side benches are stationary only. Two labels are in the agreed kit.','Planned','Put the labels in the kit; choose a pictogram, not text alone.'],
 ['15 RS5','"The rear parts of the seats must not have rough or sharp edges likely to increase the risk of injury."','Nothing sits behind the rear seat, but exposed frame edges should still be checked.','Not known','Check exposed frame edges.'],
 ['15 RS6 to RS14','Head restraints are required "on every outboard front seat" only. "Where optional headrests are fitted to seats other than outboard front seats", the top must be "at least 700mm" above the R point, at least 85mm wide each side, securely attached.','Not required on the rear seat. I do not know whether the ROAM seat has head restraints.','Not known','If fitted, check the 700mm height and attachment. If not fitted, consider them in the head clearance design review.'],
],W)

para('Section 19: Seat Belt Anchorages (Basic IVA)',bold=True)
table(H,[
 ['19 RS1, Annex 1','Minimum anchorages. Motor caravan, rear seats: 2 (lap belt). "(c) At least anchorages for lap belts are required for all rear seating positions".','Three-point belts on both rear positions.','Meets','None.'],
 ['19 RS2','Stationary-only seats "must be accompanied with a pictogram or sign clearly indicating that the seat is not to be used whilst the vehicle is in motion".','As 15 MoI (b).','Planned','Labels.'],
 ['19 RS3','"The anchorage and surrounding structure must be of adequate strength to withstand the load likely to be imposed in the event of a vehicle frontal impact. Spreader plates, where fitted, must be of adequate size and radiused to 2.5mm."','Anchorages on the seat passed the VOSC pull test. Surrounding structure in the vehicle is unproven. Radiused plates are in the agreed kit.','Gap','Underbody design and test.'],
 ['19 MoI','The examiner needs "a declaration from the vehicle converter or seat manufacturer making reference to the vehicle concerned, confirming that the seats… meet the strength and positional requirements of Directive 76/115/EEC for a category M1 vehicle, and supported by documentary evidence of the seat test results". "Where the evidence provided relates to the seat only, consideration must be given to the seat mounting."','VO00269 says the seat "met the load requirements". It does not mention positional requirements. No ROAM declaration exists.','Gap','Ask VOSC whether belt anchorage position was assessed. Prepare a manufacturer declaration template once it is known what can truthfully be declared.'],
 ['19 Annex 2','Four ways to show strength: type approval, "documentary evidence of testing to the Directive standard", comparison with an approved vehicle, or visual assessment.','ROAM has route 2 for the seat only.','Gap','In-vehicle or representative-floor evidence would complete route 2.'],
 ['19 Annex 3, all vehicles','"Bolts used in structural areas should be of grade 8.8 or better… Bolts should be M8 or larger." "Welding should appear neat and of good quality." Cause for concern: "insufficient bolt capacity".','M12 grade 8.8. Weld quality and procedures not assessed.','Meets (bolts); Not known (welds)','Document weld procedure and inspection.'],
 ['19 Annex 3, integral anchorages','"Where the upper anchorage is mounted on the seat structure, the seat back must be braced to the lower seat structure. This bracing must begin as close as possible to the upper anchorage." Cause for concern: "seat frames constructed of thin wall circular section tube".','The drawings show a triangulated seat back frame. Section sizes and wall thickness not on file.','Not known','Record the frame sections and where the bracing meets the upper anchorage.'],
 ['19 test certificate','It "should typically include… Seat make and model, Vehicle category, Seat type (single/double or triple), Belts fitted (3-point or lap), Pedestal height, Mounting details".','The VOSC summaries give model, M1, double, 3-point, 395mm leg height and the mounting (12 x M12 to a steel plate).','Meets','Get the full test reports as well as the summaries.'],
 ['19 general','"ALL the mounting holes provided… must be utilized."','Guide draft requires all 12.','Planned','None.'],
 ['19 general','Bolts through hollow members "should be fitted with anti-crush tubes".','Not supplied; owner advises no room in the T6 section.','Gap','Find an alternative on the ramp, or justify the departure.'],
 ['19 single seats','"load spreading plates at least 100 x 100 x 4mm thick", under the rear legs and between the front legs and the floor; folded, not cut, within 50mm of a chassis member.','A plate under every bolt is agreed. The ski bases act as the top-side spreader.','Planned','Spreader design.'],
 ['19 double seats','"Double seats fitted with integral three-point belts… it is extremely difficult to restrain such a seat using simple reinforcements alone. Documentary evidence that the installation can satisfy the Directive requirements in-vehicle should be sought."','No in-vehicle evidence.','Gap','The main open item. Discuss with VOSC.'],
],W)

para('Section 19: Seat Belt Anchorages (Normal IVA) and forms IVA 19a and 19b',bold=True)
table(H,[
 ['N19 RS1','"The vehicle as presented must be accompanied by satisfactory evidence of compliance".','See section 2: no tested floor or fixing.','Gap','Decide whether ROAM is sold for motor caravan conversions only, and say so; or obtain a technical service declaration.'],
 ['N19 Note 1','"If attached to a thin metal floor… spreader plates of at least 75mm x 75mm x 4mm mild steel fitted under the floor, of the legs closest to the rear… and between the leg and the top of the floor surface for the leg closest to the front".','Agreed plates are larger (100 x 100 x 4mm).','Planned','None.'],
 ['IVA 19a','"Tested installation parameters": maximum leg height, maximum offset, upper anchorage location, seat variant, maximum seat weight.','Tested: 395mm leg height; "Double Seat Bed 1580mm Width"; seat mass 67.8kg. I do not know whether 67.8kg included upholstery, or what the Full Width seat weighs.','Not known','Weigh the finished seat, Standard and Full Width, with upholstery. Anything fixed to the seat adds to the tested mass.'],
 ['IVA 19b','The installer declares the system was installed "in line with guidance and best practice supplied".','The handover record does a similar job.','Planned','Keep the handover record aligned with 19b.'],
],W)

para('Section 31: Seat Belts',bold=True)
table(H,[
 ['31 RS3','"Each seat belt must bear the appropriate approval marks or have the equivalent characteristics".','Bought-in belts. Marks not checked.','Not known','Confirm the E-mark; file the supplier documents.'],
 ['31 RS4, Notes 2, 3','Belts "attached by an appropriate fixing". A suitable single bolt is "at least 11mm (7/16") diameter of grade 8.8". The bolt must be "secured into a \u201cfixed\u201d threaded hole or captive nut" unless there is access behind.','Not known how the belts and reels are bolted to the frame.','Not known','Record the belt fixing bolts and threads on the drawing.'],
 ['31 RS9, Notes 6, 7','"A retractor mechanism must be correctly positioned". An automatically locking retractor "is not permitted" except for child restraint use.','Reels sit on the seat back, near the rear window.','Not known','Confirm reel type with the supplier.'],
 ['31 RS10, RS11, RS12','The belt "must sit correctly across the wearers torso". "There must not be any sharp edges / objects in the seat belt area likely to cause damage to the belt." The belt must be stored "so it is always readily accessible".','Not assessed.','Not known','Check on the van: belt path over the frame and upholstery, and stowage.'],
 ['31 RS16','"A harness or three-point belt \'effective upper anchorage\' location must be at least 450mm above the reference point."','Not on file.','Not known','Measure from the CAD model or the 3D scan.'],
 ['31 RS17','Upper anchorage "at least 140mm from the longitudinal centre line of the seat".','Not on file.','Not known','Measure.'],
 ['31 RS18','"The lower anchorages must be at least 350mm apart."','Not on file.','Not known','Measure.'],
 ['31 Annex 1','Motor caravan, rear outboard seats: "2 Point lap belt" minimum; "a 3-point retractor belt may be fitted".','Three-point retractor belts.','Meets','None.'],
],W)

para('Section 12: Interior Fittings',bold=True)
table(H,[
 ['12 MoI','For a motor caravan "this section will only apply to the areas determined to be within the head impact zone for any designated seating position in the rear of the vehicle".','The zone in front of and around the heads of the two rear travel seat occupants.','-','-'],
 ['12 RS1','Fittings in the zone "contactable with a 165mm sphere in a forward direction must have a radius of curvature of 2.5mm or greater", or be blunted where they project less than 3.2mm.','[Likely] ROAM items that can sit in that zone: the overhead locker, the kitchen pod and worktop edge, the table, and the tops of the pods. Folded aluminium and worktop edges have not been checked.','Not known','Check edge radii on every ROAM product that can be within reach of a rear occupant\'s head. The 3D scan can show which are in the zone.'],
 ['12 RS11','Rigid parts of the inner roof and attached components that the sphere can touch: edges of 5mm radius (structure) or 3.2mm (attached). Not applied "to parts covered with a non-rigid material".','Roof and D pillar trim are the vehicle\'s and the converter\'s.','Installer','Covered by the head clearance check in the guide.'],
 ['12 Annex 2','The specified zone starts "250mm to the rear of the front of the seat backrest" and above a plane "150mm above the top of the lowest seat cushion".','Sets the limits for the check.','-','Use in the scan analysis.'],
 ['Head height','No minimum headroom anywhere in the manual.','The "about 5ft 6" guide is ROAM\'s own.','-','-'],
],W)

para('General Construction, Masses, and the motor caravan definition',bold=True)
table(H,[
 ['GC RS1, RS4','"All aspects of the design and construction of the vehicle must be such that no immediate danger is caused… to any person in the vehicle." "The vehicle structure and all components including their attachment must be suitable and of adequate strength", including "all fastenings".','The pods are bolted to the rear seat with M6 bolts and their floor brackets are fixed "to the 12mm flooring ply using 16mm woodscrews". A 16mm woodscrew holds in the ply only, not in the vehicle.','Gap','Review how the pods, kitchen pod and overhead locker are fixed. [Likely] woodscrews into ply would not be judged adequate for a loaded storage unit in a collision.'],
 ['Foreword (g)','Motor caravan: "The seats must be secured directly to the vehicle floor and/or sidewall… as a permanent feature, (bolted riveted, screwed, or welded)." The same for storage and cooking facilities.','Rear seat is bolted through the floor. Pods are fixed to the seat and to the ply.','Not known','Confirm whether ply-only fixing counts as "directly to the vehicle floor". Safer to fix through to the floor.'],
 ['GC RS8, RS9','Wiring "secured at intervals of at least every 300mm" (400mm for motor caravans). "All electrical components must be secure, be of adequate capacity, and be insulated".','The frame has USB points; the overhead locker has LED lighting.','Not known','Check wiring runs, fusing and fixing on the ROAM electrical items; give the converter a wiring note.'],
 ['44 MoI','Passenger weight "68kg in each seat… designated for use while the vehicle is travelling", plus 7kg per seat. For motor caravans add "10kg x the number of designated seats", "10kg per metre in length" and 90% full water and gas.','The converter calculates this. ROAM does not publish component weights.','Gap','Publish the weight of each ROAM component so converters can do the payload calculation.'],
 ['Foreword','Seat count: "Where seat belts are fitted each seat space with a belt… is to constitute a seat and any remaining seat base measured to be 400mm or greater is to constitute a seat."','Two belted seats. The unbelted side benches are over 400mm.','Not known','Understand how an examiner counts the side benches once they are signed as stationary only.'],
 ['ISOFIX','The manual does not mention ISOFIX or child restraint anchorages at all.','IVA does not assess the ISOFIX points. The R145 test stands on its own.','-','No IVA action. Keep the ISOFIX guidance for owners.'],
],W)

d.add_heading('4. What this adds to the earlier assessment',1)
bl([
 'The route matters. For a motor caravan (Basic IVA) the seat is inspected and the VOSC evidence helps. For any other conversion (Normal IVA) DVSA wants every part of the anchorage system, floor included, traced to tested components, and the ROAM kit cannot offer that today.',
 'Automatic locking of the seat back and base (15 RS3) has not been looked at before.',
 'Belt geometry (450mm, 140mm, 350mm) is not evidenced. The VOSC summary speaks to load, not position.',
 'The tested seat mass of 67.8kg is a limit. Upholstery, the Full Width variant and anything fixed to the seat need checking against it.',
 'The pods are fixed with woodscrews into ply. This is a separate risk from the seat.',
 'ROAM products in front of the rear occupants (overhead locker, kitchen pod, table) fall inside the head impact zone check.',
])
d.add_heading('5. Actions, in order',1)
bl([
 'On the ramp and with the scan: underbody survey; measure belt anchorage positions against 31 RS16 to RS18; identify which ROAM parts sit in the head impact zone.',
 'At the bench: confirm how the travel seat locks (15 RS3); weigh the finished seats; check belt marks, fixings and reel type; check edge radii on locker, pod and table.',
 'With VOSC: full test reports; whether position was assessed; what in-vehicle or floor-section evidence they would accept; whether they can act as the technical service for an IVA 19a declaration.',
 'Design: underbody spreaders; pod and locker fixings through to the vehicle; an answer for the hollow chassis section.',
 'Documents: component weights; a manufacturer declaration template; a statement of which conversions the seat is intended for.',
])
d.add_heading('6. Sources',1)
bl([
 'DVSA, IVA M1 Inspection Manual, Version 17, 14 July 2025: https://www.gov.uk/government/publications/iva-manual-for-vehicle-category-m1',
 'DVSA, Seat belt anchorage installation declaration form IVA 19a and IVA 19b, v1.6 January 2025: https://www.gov.uk/government/publications/iva-declaration-form-for-seat-belt-anchorage-compliance-iva-19a-and-19b',
])
d.save(sys.argv[1])
