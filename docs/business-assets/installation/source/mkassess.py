from docx import Document
from docx.shared import Pt, Mm
import sys
d=Document()
s=d.sections[0]; s.left_margin=s.right_margin=Mm(18); s.top_margin=s.bottom_margin=Mm(16)
st=d.styles['Normal']; st.font.name='Calibri'; st.font.size=Pt(10.5)
def para(t,bold=False,italic=False):
    p=d.add_paragraph(); r=p.add_run(t); r.bold=bold; r.italic=italic; return p
def bl(items):
    for it in items: d.add_paragraph(it,style='List Bullet')
def table(head,rows,widths):
    t=d.add_table(rows=1,cols=len(head)); t.style='Light Grid Accent 1'
    for i,h in enumerate(head):
        c=t.rows[0].cells[i]; c.text=''; r=c.paragraphs[0].add_run(h); r.bold=True; r.font.size=Pt(9.5)
    for row in rows:
        cs=t.add_row().cells
        for i,v in enumerate(row):
            cs[i].text=''; r=cs[i].paragraphs[0].add_run(v); r.font.size=Pt(9.5)
    for row in t.rows:
        for i,w in enumerate(widths): row.cells[i].width=Mm(w)
    d.add_paragraph()

d.add_heading('ROAM Systems rear seat system: compliance and product assessment',0)
para('Prepared for Rob di Capite, Romark Engineering Limited. 14 November 2026.',bold=True)
para('This is an assessment against official sources, not legal advice. Every legal statement below was checked on 13 or 14 November 2026 against the source named beside it (GOV.UK, legislation.gov.uk or DVSA). Confidence is marked: [Certain] where the source says it in terms, [Likely] where it is my inference, [Guessing] where I am filling a gap. Section 7 lists what I did not check.')

d.add_heading('1. The five things that matter most',1)
table(['#','Finding','Why it matters','Confidence'],[
 ['1','Seats already fitted in vans are the biggest exposure, not future product. They were installed to a guide that gave one position (115mm), with no head clearance check, and wrongly said M10. You now know that position only suits occupants up to about 5ft 6, and one installer has reported short bolts and only eight supplied.','Once a risk is identified the producer has a duty to warn users, and to notify the authority if the product poses risks incompatible with the general safety requirement. For automotive parts that authority is DVSA.','[Certain] on the duties. [Likely] that they are engaged here; that judgement needs advice.'],
 ['2','There is no in-vehicle evidence. The tests were on a steel plate. DVSA says a double seat with integral three-point belts is "extremely difficult to restrain… using simple reinforcements alone" and that in-vehicle evidence "should be sought".','It is the gap an installer, an examiner or an expert will go to first. The new kit and guide reduce it; they do not close it.','[Certain] on the DVSA wording.'],
 ['3','Design changes are not controlled against the test. The tested article is V1 (March 2021). Production is believed to be V3. Nothing on file shows what changed or why the test still applies.','A defect is judged against what people are entitled to expect, including how the product was marketed. "Tested" is the marketing. The link from test to product must be provable.','[Certain] on the law. [Certain] that no record exists in the repo.'],
 ['4','The kit and the guide do not yet match. Revision A describes 12 spreader plates, labels, a range of bolt lengths and a handover record. The kit on the shelf has two plates.','Instructions for installation are part of what makes a product "safe" in law. Shipping the old guide, or the new guide with the old kit, continues the problem.','[Certain]'],
 ['5','Claims clean-up is not finished. The website is corrected. Still outstanding: social posts, installers\' own websites, the Stripe product name, the A5 flyer, and the HQ description.','Misleading claims can now be fined by the CMA directly, up to 10% of worldwide turnover.','[Certain] on the penalty. [Likely] that small traders are rarely the target.'],
],[8,72,62,32])

d.add_heading('2. What the law requires',1)
para('Product safety: General Product Safety Regulations 2005 (GB)',bold=True)
bl([
 '[Certain] They apply to products "intended for or likely… to be used by consumers". A campervan travel seat is one.',
 '[Certain] A "safe product" is judged "under normal or reasonably foreseeable conditions of use including… installation and maintenance requirements", taking into account "instructions for assembly and, where applicable, instructions for installation", "any warnings" and "the categories of consumers at risk… in particular children" (regulation 2).',
 '[Certain] The producer must give consumers the information to assess risks that are "not immediately obvious without adequate warnings" (regulation 7(1)). "The presence of warnings does not exempt any person from compliance with the other requirements" (regulation 7(2)).',
 '[Certain] The producer must, "except where it is not reasonable to do so", mark the product or packaging with "the name and address of the producer" and "the product reference or… batch" (regulation 7(4)(a)).',
 '[Certain] Where reasonable, the producer must sample test marketed products, investigate and "if necessary" keep "a register of complaints concerning the safety of the product", and keep distributors informed (regulation 7(4)(b)).',
 '[Certain] Where a producer "knows that a product he has placed on the market or supplied poses risks to the consumer that are incompatible with the general safety requirement, he shall forthwith notify an enforcement authority in writing" (regulation 9).',
 '[Certain] Installers are caught too. "Producer" includes "other professionals in the supply chain, in so far as their activities may affect the safety properties of a product" (OPSS guidance, December 2024). That adds the installer; it does not remove Romark.',
 '[Certain] Penalties "can include a fine of up to £20,000 or a prison sentence of up to 12 months or both for the most serious offences" (OPSS guidance).',
])
para('Who enforces it for vehicle parts: DVSA',bold=True)
bl([
 '[Certain] "DVSA is the government-appointed authority in the UK responsible for product safety in the automotive sector. A producer or distributor is required to inform the competent authority forthwith of any issues they have with the safety of their aftermarket parts." (DVSA code of practice on safety defects and recalls in the vehicle aftermarket, which covers "motor homes/caravans".)',
 '[Certain] "Under the GPSR, it is the responsibility of the producer or distributor to effectively warn the user of the risk when it has been identified."',
 '[Certain] The code defines a "safety defect" as "a failure due to design and/or construction, which is likely to affect the safe operation of the aftermarket part without prior warning to the user and may pose a significant risk to the driver, occupants and others". A "safety recall" follows a safety defect "that could result in a risk of serious injury". A "non-code action" is "a proactive and proportionate action registered with DVSA, which falls outside the scope of a safety recall".',
 '[Certain] DVSA has a Vehicle Market Surveillance Unit that tests vehicle components, acts on reports "from industry" and the public, can issue fines and "can also take action under the General Product Safety Regulations 2005" (enforcement policy, updated 23 April 2026).',
])
para('Product liability: Consumer Protection Act 1987, Part I',bold=True)
bl([
 '[Certain] "Where any damage is caused wholly or partly by a defect in a product", the producer "shall be liable for the damage" (section 2). No negligence is needed.',
 '[Certain] There is a defect "if the safety of the product is not such as persons generally are entitled to expect", taking into account "the manner in which, and purposes for which, the product has been marketed" and "any instructions for, or warnings with respect to, doing or refraining from doing anything with or in relation to the product" (section 3).',
 '[Certain] This liability "shall not be limited or excluded by any contract term, by any notice or by any other provision" (section 7). Clause 8 of the website terms cannot move this liability to the installer.',
 '[Certain] Claims are extinguished ten years after supply (Limitation Act 1980, section 11A(3)). Keep design, test and build records for at least that long.',
])
para('Claims and advertising: Digital Markets, Competition and Consumers Act 2024',bold=True)
bl([
 '[Certain] In force since 6 April 2025. Misleading actions include "providing false information" and "presenting information in a deceiving way". Misleading omissions include "not telling consumers something they need to know".',
 '[Certain] "The CMA and the courts can now fine traders who do not comply with the law up to 10% of their worldwide turnover" (CMA guidance for businesses, updated 3 December 2025).',
 '[Certain] Consumer Rights Act 2015: goods must be of satisfactory quality (section 9) and as described (section 11).',
])
para('Road vehicle rules that bear on the seat',bold=True)
bl([
 '[Certain] "There are no specific regulations covering the conversion of vans into passenger carrying vehicles. However, Regulation 100 of The Road Vehicles (Construction & Use) Regulations 1986… will apply", so that passengers are carried without danger. "Additional seats should be fitted securely." (DfT/DVSA guidance, 2010, still live.)',
 '[Certain] "When fitting seatbelts, they must comply with the latest British or European standards and be marked accordingly with either the \'e\', \'E\' or BS \'Kitemark\'." (same guidance)',
 '[Certain] DVLA: "Any seat belts and seats installed, that are for use while travelling, must be securely mounted." (updated 6 November 2026)',
 '[Certain] The MOT inspects "anchorage points for all seat belts fitted", and its seat belt tables require belts on forward-facing rear seats of passenger vehicles and motor caravans by date of first use (MOT inspection manual, section 7 and Appendix C).',
 '[Certain] At Individual Vehicle Approval, the examiner works from the DVSA IVA M1 Inspection Manual: all mounting holes used, grade 8.8 bolts, spreader plates, in-vehicle evidence for double seats with integral belts, stationary-only seats signed, and fittings in the head impact zone radiused.',
 '[Certain] Upholstery: the Furniture and Furnishings (Fire) (Safety) Regulations 1988 define "dwelling" to include "any caravan, but… not… motor vehicles". [Likely] So they do not apply to campervan upholstery. The general safety requirement still does.',
])

d.add_heading('3. Where ROAM stands against each duty',1)
table(['Duty','Position today','Gap'],[
 ['Safe product, including installation instructions','Revision A guide approved, with head clearance check, plate under every bolt, DVSA extracts. Not yet issued.','Old guide still the one in circulation. Kit does not match Revision A. No in-vehicle evidence.'],
 ['Warn users of risks that are not obvious','Website now carries the test scope, side bench and head clearance notes. Terms clause 8 sets out what the tests do not cover.','Nothing has gone to existing customers or installers. No user guide for the vehicle owner. Side bench labels not yet in the kit.'],
 ['Name, address and product or batch reference on the product','Not known. I have seen no serial plate or label in any drawing or photo.','Confirm. If absent, add a plate: producer name and address, model, revision, serial number, date.'],
 ['Monitor: complaints register, sample testing','No complaints register found. No test since March 2021.','Start the register now, with the installer challenge and the video findings as the first entries. Decide re-test triggers.'],
 ['Notify the authority and warn users when a risk is known','Not done.','Decision needed on field action. See section 5.'],
 ['Claims match the evidence','Website, trade email and price list corrected to "M1 tested".','Social posts, installers\' websites, Stripe product name, A5 flyer, HQ text, URL slug.'],
 ['Evidence that the tested article is the product sold','Owner statements: Full Width has the same rear section; rear seat unchanged V1 to V3.','No drawing comparison, no revision log. Test summaries are in the name of the closed company. Only the one-page summaries are on file, not the full test reports.'],
 ['Seat belts to an approved standard and marked','Not checked. The belts are bought-in parts.','Confirm the E-mark on the belts and reels and keep the supplier\'s approval documents.'],
],[52,62,60])

d.add_heading('4. The product: what to do better',1)
table(['Area','Finding','Recommended change','Priority'],[
 ['Load path into the vehicle','Tested on a steel plate only. Rear fixings see the uplift; on 395mm legs DVSA\'s own example suggests loads of several tonnes on the rear legs.','Commission an in-vehicle or representative-floor pull test with the final kit, on the most common van first (T6). Ask VOSC what they would accept.','High'],
 ['Fixing kit','Two handed plates for twelve bolts; bolt lengths short on at least one job; no solution for the hollow chassis section.','Build the universal kit already agreed. Consider a steel strip under each ski linking fixings, in place of loose plates, where it fits. Find an anti-crush solution for the chassis section, or a torque limit proven on a van.','High'],
 ['Head clearance','At the rear positions the seat suits occupants up to about 5ft 6. This is a product limit, not only an installation choice.','Design review: can the default position move forward, the seat height come down, or the D pillar trim be padded? Decide whether head restraints should be fitted. State the limit wherever the seat is sold.','High'],
 ['Design control','V1 to V3 with no record of what changed.','Drawing register with revision log. Every change to the rear section assessed in writing against the test, signed by you. Define what V3 is.','High'],
 ['Traceability and build records','A kit reached an installer with eight bolts.','Serial number on every frame. Kit packing checklist signed at dispatch. Build record per serial: drawing revision, welder, inspection, date.','High'],
 ['Welding and inspection','Not assessed. Nothing on file about weld procedures, welder qualification or inspection.','Write down what is done now. [Likely] A documented weld procedure and a final inspection sheet are the minimum an expert would expect for a seat belt anchorage structure.','Medium'],
 ['ISOFIX and child seats','Two ISOFIX positions tested to R145. I do not know whether a top tether anchorage is provided or was tested.','Ask VOSC. Publish plain guidance on which child seats can be used, and tell buyers to check the child seat maker\'s fitting list.','Medium'],
 ['Owner information','There is an installer guide but nothing for the person who owns and uses the van.','One-page user guide: who can travel where, head clearance, side benches, belts and ISOFIX, the 500 mile check, what to do after a collision.','Medium'],
 ['Installer network','"Experienced installers" are listed on the website with no written criteria.','Written criteria and a short agreement: follow the current guide, complete the handover record, report problems. Use the trial sheet as the feedback loop.','Medium'],
 ['Other products','Upholstery foam and fabric specification not assessed. Kitchen pods involve a hob space, 12V lighting and USB points.','Separate short assessment of upholstery materials and of the kitchen pod (gas, ventilation, electrics).','Low'],
],[30,52,68,18])

d.add_heading('5. The field action decision',1)
para('This is the decision I cannot make for you, and the one with a clock on it.',bold=True)
bl([
 'What is known: seats were installed to a guide with one position and no head clearance check; that position suits occupants up to about 5ft 6; the guide said M10; one installer found the bolts about 20mm short and reported eight supplied.',
 'What the sources say: the producer must "effectively warn the user of the risk when it has been identified", and must notify the authority "forthwith" where the product "poses risks… incompatible with the general safety requirement". DVSA offers a lighter route, the "non-code action", for a proportionate action short of a recall.',
 '[Likely] The proportionate first step is a written safety notice to every known installer and customer: the head clearance limit and check, a check that all 12 M12 fixings and plates are fitted with thread showing through the nuts, and the 500 mile check.',
 '[Likely] Whether that notice should be registered with DVSA as a non-code action, or whether the facts amount to a safety defect, is a judgement to take with your solicitor and your insurer. I would not send the notice before speaking to both, and I would not delay speaking to them.',
 'Whatever is decided, write down the decision, the reasons and the date. A recorded, reasoned decision is far better than none.',
])

d.add_heading('6. Action plan',1)
para('Now',bold=True)
bl([
 'Withdraw the May 2025 installation guide. Do not send it with any kit.',
 'Start a safety and complaints register. First entries: the installer challenge and the two videos.',
 'Pull the list of every rear seat sold, with customer or installer, date and variant.',
 'Call your insurance broker: tell them about the installer challenge and ask what your product liability policy requires you to notify.',
 'Brief a solicitor on section 5 and on clause 8 of the terms.',
])
para('Within 30 days',bold=True)
bl([
 'Decide and carry out the field action in section 5.',
 'Build the universal kit and issue Revision A with it, the handover record and the labels.',
 'Add a serial plate and a kit packing checklist.',
 'Write the V1 to V3 change record and sign it.',
 'Ask VOSC three things: the cost and form of an in-vehicle or representative-floor test, whether the 2021 results apply to V3, and reissue of the summaries in Romark Engineering\'s name. Ask for the full test reports.',
 'Confirm the E-mark on the seat belts and file the supplier\'s documents.',
 'Finish the claims clean-up: social posts, installers\' websites, Stripe name.',
])
para('Within 90 days',bold=True)
bl([
 'Carry out the in-vehicle test.',
 'Complete the head clearance design review.',
 'Issue the owner\'s user guide.',
 'Put the installer criteria and agreement in place.',
 'Set a routine: review the register quarterly; re-assess against the test at every design change.',
])

d.add_heading('7. What I did not check',1)
bl([
 'The Product Regulation and Metrology Act 2025 and any new product safety regulations made under it. The December 2024 OPSS guidance was the current GOV.UK text when I read it.',
 'Whether selling seat belts, ISOFIX anchorages or seats as parts requires component approval, and under which regulation.',
 'ECE R145 itself, including top tether requirements. I could not reach the UNECE website from this session.',
 'Sales into Northern Ireland or the EU. OPSS states that in Northern Ireland the 2005 Regulations "were superseded on 13 December 2024 by the EU Regulation on General Product Safety 2023/988", which has different duties.',
 'Workplace health and safety at Romark (HSE), gas and electrical rules for the kitchen pods, and your insurance policy wording.',
 'Anything physical. I have not seen a seat, a kit or a van. Everything about the product comes from drawings, the test summaries, two installer videos and your answers.',
])

d.add_heading('8. Sources',1)
for t in [
 'General Product Safety Regulations 2005, regulations 2, 5, 7 and 9: https://www.legislation.gov.uk/uksi/2005/1803',
 'OPSS, General Product Safety Regulations 2005: Great Britain (updated 13 December 2024): https://www.gov.uk/government/publications/general-product-safety-regulations-2005/general-product-safety-regulations-2005-great-britain',
 'DVSA, Safety defects and recalls in the vehicle aftermarket: code of practice (updated 14 May 2021): https://www.gov.uk/government/publications/code-of-practice-on-safety-defects-and-recalls-vehicle-aftermarket/code-of-practice-on-safety-defects-and-recalls-vehicle-aftermarket',
 'DVSA, Recall vehicles, parts or accessories in the UK (manufacturers\' guide): https://www.gov.uk/government/publications/manufacturers-guide-to-recalls-in-the-uk-automotive-sector',
 'DVSA, Vehicle Market Surveillance Unit: enforcement policy (updated 23 April 2026): https://www.gov.uk/government/publications/how-dvsa-makes-sure-businesses-make-or-sell-safe-vehicles-or-parts/vehicle-market-surveillance-unit-enforcement-policy',
 'Consumer Protection Act 1987, sections 2, 3, 4 and 7: https://www.legislation.gov.uk/ukpga/1987/43/part/I',
 'Limitation Act 1980, section 11A: https://www.legislation.gov.uk/ukpga/1980/58/section/11A',
 'CMA, What businesses need to know about unfair commercial practices (updated 3 December 2025): https://www.gov.uk/government/publications/what-businesses-need-to-know-about-unfair-commercial-practices/what-businesses-need-to-know-about-unfair-commercial-practices',
 'Consumer Rights Act 2015, sections 9 and 11: https://www.legislation.gov.uk/ukpga/2015/15',
 'DfT/DVSA, Converting a van to carry passengers in the rear: https://www.gov.uk/government/publications/converting-a-van-to-carry-passengers-in-the-rear/converting-a-van-to-carry-passengers-in-the-rear',
 'DVLA, Converting a vehicle into a motor caravan: https://www.gov.uk/government/publications/converting-a-vehicle-into-a-motor-caravan/converting-a-vehicle-into-a-motor-caravan',
 'DVSA, MOT inspection manual, section 7 and Appendix C: https://www.gov.uk/guidance/mot-inspection-manual-for-private-passenger-and-light-commercial-vehicles',
 'DVSA, IVA M1 Inspection Manual (July 2025): https://www.gov.uk/government/publications/iva-manual-for-vehicle-category-m1',
 'Furniture and Furnishings (Fire) (Safety) Regulations 1988, regulation 3: https://www.legislation.gov.uk/uksi/1988/1324/regulation/3',
]: d.add_paragraph(t,style='List Bullet')
d.save(sys.argv[1])
