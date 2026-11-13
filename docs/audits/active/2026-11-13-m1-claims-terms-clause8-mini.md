---
doc_type: audit
audit_type: mini
status: active # active | resolved | superseded
created: 2026-11-13
auditor: "AI (Claude Code)"
scope: "Test-claim wording alignment (\"M1 Certified\" -> \"M1 Tested\", crash-test / legal-requirement claims removed), terms clause 8 rewrite, installers rename, and /api/* middleware exemption — commits b71544b, d44d84a, 914bf38, f9c5fb6, 55058dc (all on origin/main, verified live 2026-11-13)"
open_p0: 0
open_p1: 1
---

# Mini Audit Result: M1 test-claim wording + terms clause 8 + middleware — 2026-11-13

## Purpose

Verify that the site's safety/test claims, the rewritten terms clause 8 and the
related naming changes match their source of truth (the two VOSC test summaries
and the gov.uk guidance the blog cites), that no retracted claim survives on any
surface, and that canonical docs and status docs reflect what shipped.

Scope was not given when the audit was invoked. It was inferred as "everything on
`main` since the last audit (2026-06-12) that is not yet covered by an audit":
five commits, 30 files.

## Scope

- **In scope**:
  - `src/pages/policies/terms.astro` — clause 8 "Testing, certification and installation" (d44d84a).
  - Claim wording across `src/` — product data, homepage islands, certifications page ("Testing & Quality"), installers page, four published blog posts, three draft posts, layouts, order/form emails, Merchant feed, content/social calendars (914bf38, f9c5fb6, 55058dc).
  - `src/middleware.ts` — `/api/*` exemption from the non-www -> www 301 (b71544b).
  - Source documents: `public/images/certs/cert-m1-seatbelt-test.jpg` (VO00269), `cert-isofix-test.jpg` (VO00270); the three gov.uk pages linked from the blog.
  - Canonical docs: `PLATFORM_OVERVIEW_CANONICAL.md`, `GLOBAL_TERMINOLOGY_INDEX_CANONICAL.md`, `SCHEMA_AND_CONTRACTS_CANONICAL.md`, `DNS_ROAMSYSTEMS_CO_UK.md`.
  - Live serving spot-checks on `www.roamsystems.co.uk`.
- **Out of scope**:
  - Legal sufficiency of the clause 8 wording (AI-drafted; solicitor review remains the standing recommendation from the 2026-06-11 plan).
  - Stripe account data (no API key in this environment) — see AUDIT-2026-11-13-002.
  - Live behaviour of the apex host `roamsystems.co.uk` (blocked by this environment's network policy) — see AUDIT-2026-11-13-008.
  - Content already published to Facebook/Instagram, Google Merchant Center state, printed material in circulation.
  - Unmerged branches (`feat/roam-code-catalogue-alignment`, `claude/relaxed-turing-2fwctd`). Checked only that neither adds claim wording: neither does.

## Canonical references reviewed

- VOSC "Seat Belt Anchorage Test Summary" VO00269 (18 March 2021) and VO00270 (23 March 2021), as published in `public/images/certs/`
- gov.uk: "Converting a van to carry passengers in the rear" (DfT/DVSA); "Converting a vehicle into a motor caravan" (DVLA); MOT inspection manual section 7.1
- `docs/reference/PLATFORM_OVERVIEW_CANONICAL.md` (Purpose, Invariants, Pages, Glossary)
- `docs/reference/GLOBAL_TERMINOLOGY_INDEX_CANONICAL.md` (Product & Engineering Terms)
- `docs/reference/SCHEMA_AND_CONTRACTS_CANONICAL.md` (Product entity, checkout, webhook)
- `docs/reference/DNS_ROAMSYSTEMS_CO_UK.md` (open item: non-www redirect)
- `CLAUDE.md` governance section (plan + approval for business-rule changes)

## Summary

- **Total issues**: 12 (7 open; 001, 003, 004, 006 resolved and 007 closed by owner decision, all 2026-11-13; 012 added and open)
- **P0**: 0
- **P1**: 2 — 001 resolved (owner confirmed Full Width has the same rear section); **012 open** (tested article is V1, owner believes production is V3)
- **P2**: 6 (2 open: 002, 005) plus follow-ups from 006 (price list prices and company details, flyer)
- **P3**: 4 open
- **Assessment**: ⚠️ Minor drift — the deployed site itself is clean and matches the test documents; drift is in what surrounds it (one unconfirmed test-scope question, Stripe-held product names, the content pipeline and trade collateral).

### Verified aligned (core surfaces)

| Claim / change | Source of truth | Status |
|---|---|---|
| Seat belt anchorage pull test, M1 category, ECE R14.09 + 76/115/EEC as amended by 2005/41/EC, test VO00269, 18 March 2021, 3-point belts | VO00269 summary, field by field | ✅ |
| ISOFIX test to ECE Regulation No. 145, 2 places, strength and positional, test VO00270, 23 March 2021 | VO00270 summary | ✅ |
| "Fixed to a steel plate test structure with 12 M12 bolts", "not carried out in a vehicle" | Both summaries: "m12 x 12 bolts to fix to floor", "Fixed to a Steel Plate Structure (I.e. not in Vehicle)" | ✅ |
| "Passed" | Summaries: "met the load requirements" | ✅ |
| "Not a crash test" | Summaries describe a pull test only | ✅ |
| Terms clause 8 — tests cover / do not cover / installation / "nothing limits clause 10" | Consistent with the summaries; clause 10 is the liability clause, cross-reference resolves; last-updated date 13 November 2026 | ✅ |
| FAQ installation answer, product `safetyNote`, certifications page and blog all state the same scope as clause 8 | Cross-read | ✅ |
| "17 experienced installers" | `installers.astro` lists 17 | ✅ |
| gov.uk attributions in the blog (securely fitted seats; anchorages "capable of withstanding the high forces of an impact"; tell your insurer; MOT tester inspects anchorage points of all seat belts fitted; "no formal checking procedure for private conversions"; registered keeper to demonstrate work safely completed; seats and belts "must be securely mounted") | Fetched all three pages 2026-11-13; each statement is present | ✅ (one omission -> AUDIT-007) |
| No retracted wording in the built site | `dist/client` HTML + XML + JS bundles: zero hits for "crash tested", "approved installer", "only steel", "legal requirement"; every "certified" hit is the retained URL slug or an image filename | ✅ |
| Middleware exempts `/api/*` from the 301 | `src/middleware.ts:23` | ✅ (code); live apex unverified -> AUDIT-008 |
| Meta descriptions | 34 pages, 0 over 160 characters, 0 non-www canonicals | ✅ |

## Issues

### AUDIT-2026-11-13-001

- **Priority**: P1
- **Location**: `src/data/products.json:24-27,48-53`; `src/pages/certifications.astro:26`; all "M1 tested rear travel seat" statements
- **Canonical ref**: VOSC summaries VO00269 / VO00270, "Model" field
- **What is wrong**: Both test summaries identify the tested article as **"M1 Smart U Bed V1 Double Seat Bed 1580mm Width"**. The site sells the frame in two configurations, **Standard** (max frame width 158 cm, which matches) and **Full Width** (£2,150), and applies the tested claim to the product as a whole without saying which configuration was tested. Nothing in the repo records whether the Full Width rear travel seat is the same assembly as the 1580 mm article that VOSC tested, or whether current production is still the "V1" design.
- **Expected**: The claim is limited to the article that was tested. If the Full Width rear section is physically identical to the tested one, say so on record; if it differs (width, leg span, fixings), the Full Width variant must not be described as tested.
- **Status**: Resolved 2026-11-13 — owner confirmation
- **Resolution**: The owner (Rob di Capite) stated on 2026-11-13: "Full width is the same rear section", and earlier the same day: "It is the rear section which has the seatbelts and isofix only that is tested." The "M1 tested" claim therefore stands for both the Standard and Full Width configurations, on the owner's statement. This rests on the owner's knowledge of the product; the repo holds no drawing or part-number evidence. Whether current production is still the "V1" design named on the summaries is now AUDIT-2026-11-13-012.

### AUDIT-2026-11-13-002

- **Priority**: P2
- **Location**: Stripe account (Product objects); consumed by `src/pages/api/checkout.ts:51-52` and `src/lib/email.ts:110-120`
- **Canonical ref**: Commit 55058dc ("product and badges renamed 'M1 Certified' -> 'M1 Tested'")
- **What is wrong**: Checkout sends Stripe `price` IDs only, so the product name shown on the Stripe-hosted checkout page, on Stripe receipts, and in the order-confirmation email (`item.description`) comes from the Stripe Product, not from `products.json`. The repo rename cannot have changed it, and the commit does not mention a Stripe change. The name is probably still "M1 Certified U-Shape Seating Frame" at the point of sale and on the customer's order record. Not verified: no Stripe key available here.
- **Expected**: The name at checkout and on the confirmation matches the site.
- **Status**: Open — needs verification
- **Fix recommendation**: In Stripe Dashboard -> Product catalogue, check the U-shape frame Product name and description, plus the panel/upholstery Products that mention it, and rename to "M1 Tested U-Shape Seating Frame". Renaming a Product keeps its Price IDs, so no code change is needed.

### AUDIT-2026-11-13-003

- **Priority**: P2
- **Location**: `docs/plans/` (no plan), `docs/sessions/` (no log); commit messages 914bf38 and 55058dc
- **Canonical ref**: `CLAUDE.md` Governance — business-rule changes need a plan and explicit approval
- **What was flagged**: No approval record in the repo for the clause 8 wording and the claim changes; commits 914bf38 and 55058dc say "Not merged or deployed - awaiting owner approval" yet the change is live.
- **Status**: Resolved 2026-11-13 — approval record added here
- **Resolution**: The commit messages were accurate when written; approval came afterwards, in the same working session, before the merge. Record of the owner's decisions (Rob di Capite, 2026-11-13):
  1. Owner set the brief: clause 8 wording (commit d44d84a) was written first and was not to be changed without his approval; all other wording to be shown as an old/new table before merging.
  2. Round 1 table (commits 914bf38, f9c5fb6) and the full text of clause 8 were shown to the owner.
  3. Owner rulings in reply: installers are "experienced", not "approved"; only the rear section with the seat belts and ISOFIX is tested; the term is "M1 tested", not "M1 certified"; remove claims that are not verified true.
  4. Round 2 table (commit 55058dc) was shown to the owner with clause 8 unchanged.
  5. Owner replied "approved". Main was then fast-forwarded to 55058dc and Railway auto-deployed.
  The change was handled under the small-fixes workflow at the owner's instruction; no plan document was created. Legal review of clause 8 by a solicitor has not been done and remains the standing recommendation.

### AUDIT-2026-11-13-004

- **Priority**: P2
- **Location**: `docs/reference/GLOBAL_TERMINOLOGY_INDEX_CANONICAL.md:14`; `docs/reference/PLATFORM_OVERVIEW_CANONICAL.md:12,50,71,87`
- **Canonical ref**: the same documents
- **What is wrong**: Canonical docs still assert what the site has retracted. Terminology index: "**M1 Certification**: ECE 14.09 safety standard for motor vehicle seating. All ROAM seating frames carry this certification." Platform overview: "premium M1-certified campervan furniture"; invariant "All seating frames must display M1 certification status"; `/certifications` described as "Safety certification gallery"; glossary "M1 certification". These documents are what future AI sessions and the content pipeline read first, so they are the likeliest route for the old claims to return.
- **Expected**: Terminology and invariants match the test scope: the rear belted travel seat of the U-shape frame was pull tested to ECE R14.09 (M1 loads) and its ISOFIX anchorages to ECE R145; side benches untested; "tested", not "certified".
- **Status**: Resolved 2026-11-13 — terminology index entry, platform overview purpose line, invariant, page description and glossary entry reworded to "M1 tested" with the test scope. The wider staleness of the platform overview (`/stockists`, missing vehicles/blog/feed/middleware) is not fixed; see AUDIT-008.

### AUDIT-2026-11-13-005

- **Priority**: P2
- **Location**: `src/data/social-drafts-2026-03-17.json`, `-03-22.json`, `-04-06.json`; scheduled content-generation tasks (defined outside the repo); `docs/reference/seo-marketing.md` (planned in plan 005, never created)
- **Canonical ref**: `docs/plans/005-automated-seo-marketing.md` section 6
- **What is wrong**: The calendars were updated, but the stored social drafts still contain the retracted claims verbatim: "Rear campervan seating is only legal for passenger use if the seat frame has been independently tested and certified to M1 standard", "The only steel M1 certified U-shape seating frame on the market", "crash-tested", `#m1certified`. The weekly generator has no written claims rule in the repo, and its prompt lives outside the repo, so nothing stops the next run producing the same wording. Posts already published from these drafts are outside the repo and unreviewed.
- **Expected**: A claims rule the generator must follow, no stored drafts carrying retracted claims, and published posts reviewed.
- **Status**: Open
- **Fix recommendation**: (1) Add a short "approved claims / banned phrases" block to the content calendars or a canonical marketing doc, and reference it in the scheduled task prompts. (2) Delete or annotate the three old draft files. (3) Owner reviews Facebook/Instagram posts published since March 2026 for "only legal", "crash tested", "only steel M1 certified".

### AUDIT-2026-11-13-006

- **Priority**: P2
- **Location**: `docs/business-assets/ROAM Systems - Email Template.html:26,37,41,49`; `docs/business-assets/ROAM_Systems_Price_List_Email.html:37,89`; `docs/business-assets/create_price_list.py:100`; `docs/business-assets/ROAM_Systems_Price_List.pdf`; `RoamSystems-Flyers-A5-incVAT-EMAIL-v2.pdf`
- **Canonical ref**: Commits 914bf38 / 55058dc
- **What is wrong**: Trade-facing collateral kept in the repo still makes the retracted claims: "M1 crash tested seating system with integrated seatbelts and ISOFIX points", "fully certified travel seating to ECE M1 standards", "M1 Certified U-Shape Bed System", and "M1 certified U-shape frame" on the A5 flyer and price list. These go to conversion companies, the audience most likely to rely on them.
- **Expected**: Outbound collateral uses the same wording as the site.
- **Status**: Resolved 2026-11-13 for the claim wording — owner approved the redraft ("approved"); email template, price list email HTML, generator and regenerated PDF are on `main`.
- **Follow-ups (owner statements 2026-11-13)**:
  - The price list price of £1,850 for the U-shape frame is out of date. Price list prices have not been changed yet; a draft matched to `products.json` is awaiting owner confirmation. Do not send the price list until then.
  - "Company was closed down, roam systems is under romark now": the price list footer (PDF and email HTML) and the A5 flyer still name "Roam Systems Ltd", Unit 3, 47 King Street, Company No. 1318982. A footer draft using the Romark Engineering Limited details from terms clause 1 is awaiting owner confirmation.
  - The A5 flyer (`RoamSystems-Flyers-A5-incVAT-EMAIL-v2.pdf`, Illustrator artwork, no source in repo) still says "M1 certified U-shape frame", carries the old prices and the closed company's details. Owner: "We will re-do the flyer at a later date". It should not be sent in the meantime.

### AUDIT-2026-11-13-007

- **Priority**: P2
- **Location**: `src/content/blog/why-m1-certification-matters.md:22,38`
- **Canonical ref**: gov.uk "Converting a van to carry passengers in the rear"
- **What is wrong**: The post reports that guidance "says there are no specific regulations covering the conversion of vans to carry passengers". The source sentence continues: "However, Regulation 100 of The Road Vehicles (Construction & Use) Regulations 1986 … will apply", requiring passengers to be carried so that no danger is caused, and it goes on to cite section 40A of the Road Traffic Act 1988. Quoting the first half alone reads as "unregulated". Likewise "no formal checking procedure for private conversions" omits the next sentence, which advises a seatbelt installation check (class IVa) at an MOT station when new belts are fitted.
- **Expected**: Commit f9c5fb6 set out to quote the guidance rather than draw conclusions; a partial quote draws one by omission.
- **Status**: Closed 2026-11-13 — owner decision, no change
- **Resolution**: A sentence adding the Regulation 100 point was proposed to the owner, who rejected it ("Reject .gov sentence"). The blog wording stays as approved.

### AUDIT-2026-11-13-008

- **Priority**: P3
- **Location**: `src/middleware.ts`; `docs/reference/PLATFORM_OVERVIEW_CANONICAL.md`; `docs/reference/DNS_ROAMSYSTEMS_CO_UK.md:40-43`
- **Canonical ref**: `docs/reference/DNS_ROAMSYSTEMS_CO_UK.md` open item
- **What is wrong**: The app-level non-www -> www 301 and its `/api/*` exemption (b71544b, merged 2026-10-06) appear in no canonical doc, and the DNS doc still frames the redirect as a Cloudflare-only open item. The fix was also never recorded in the status docs. Live apex behaviour could not be confirmed from this environment (requests to `roamsystems.co.uk` are blocked by network policy); `www` `/api/contact` answers 405 to GET with no redirect, as expected.
- **Expected**: Middleware behaviour documented; live apex check recorded.
- **Status**: Open
- **Fix recommendation**: Add a "Middleware" paragraph to the platform overview (hosts, 301, `/api/*` exempt and why). From any normal network: `curl -sI https://roamsystems.co.uk/certifications` should 301 to www, and `curl -si -X POST https://roamsystems.co.uk/api/contact` should not redirect.

### AUDIT-2026-11-13-009

- **Priority**: P3
- **Location**: `homepage-v2/` (tracked prototype, not built or deployed) — `src/components/Hero.tsx:103,160`, `FAQ.tsx:8,20`, `WhyRoam.tsx:7-8,26`, `FeaturedProduct.tsx:70,81`, `src/data/products.ts:12-13,90,94`, `index.html:8`
- **Canonical ref**: Commit 55058dc
- **What is wrong**: The prototype the live homepage was ported from keeps every retracted claim, including "The only steel M1 certified U-shape frame" and "best fitted by an approved installer to keep certification valid". Harmless while unused; a trap if anyone copies from it.
- **Expected**: No source in the repo that reads as current and carries the old claims.
- **Status**: Open
- **Fix recommendation**: Delete `homepage-v2/` if the port is complete, or add a README line marking it superseded.

### AUDIT-2026-11-13-010

- **Priority**: P3
- **Location**: product `id`/`mpn` and URL `/products/m1-certified-u-shape-seating-frame`; blog URL `/blog/why-m1-certification-matters`; blog category badge "Certification" (`src/pages/blog/index.astro`, `src/layouts/BlogPost.astro`, `src/content.config.ts:13`); route `/certifications`; `draft-isofix-campervan-safety.md:20`
- **Canonical ref**: Commit 55058dc ("URL slug, id and mpn unchanged", "URL unchanged")
- **What is wrong**: "Certified"/"certification" survives in URLs, the Merchant feed `mpn`, and a visible "Certification" category badge on the blog. The slugs were kept deliberately, which protects SEO and existing links; the badge was probably just missed. The unpublished ISOFIX draft also says ISOFIX "dramatically reduces the risk of the child seat moving during a collision", an unsourced claim of the kind the published posts no longer make.
- **Expected**: Deliberate retentions recorded as accepted; visible labels consistent.
- **Status**: Open (slug retention: accepted by owner ruling)
- **Fix recommendation**: Relabel the badge to "Testing" (display label only; the enum value can stay). Give the three draft posts a claims pass before any is published. If the slugs are ever changed, add 301s.

### AUDIT-2026-11-13-011

- **Priority**: P3
- **Location**: `src/components/home/FAQ.tsx:11-12`
- **Canonical ref**: `src/pages/policies/terms.astro` clauses 3 and 9; `SCHEMA_AND_CONTRACTS_CANONICAL.md` (POST /api/checkout)
- **What is wrong**: Pre-existing, noticed because this file was edited. "How do I place an order?" still describes an enquiry-and-phone-call process with "no surprise checkouts", while the site takes payment through Stripe Checkout. "Do you offer a warranty?" promises "a manufacturer warranty. Full terms are supplied with your order"; terms clause 9 offers repair/replace/refund and statutory rights and mentions no separate warranty document.
- **Expected**: FAQ matches the checkout flow and the terms.
- **Status**: Open
- **Fix recommendation**: Rewrite both answers; confirm with the owner whether a written warranty exists before keeping that claim.

### AUDIT-2026-11-13-012

- **Priority**: P1
- **Location**: every "M1 tested" statement on the site and in the trade collateral; `src/pages/policies/terms.astro` clause 8 ("These tests apply only to genuine ROAM Systems products as manufactured by Romark Engineering Limited")
- **Canonical ref**: VOSC summaries VO00269 / VO00270 — "This report relates to the performance of the M1 Smart U Bed **V1** Double Seat Bed 1580mm Width as tested on a surrogate vehicle floor"
- **What is wrong**: Both test summaries relate to design revision **V1**, tested in March 2021. Asked whether current production is still V1, the owner replied on 2026-11-13: "V3 i believe". The repo holds no record of what changed between V1 and V3. If any change affected the tested rear section (frame members, welds, leg type or height, leg span, the 12 x M12 floor fixings, seat belt or ISOFIX anchorage positions or parts), the summaries may not describe the product sold today, and the site's test claims and clause 8 would not be supported for current production.
- **Expected**: Either evidence that the rear section is unchanged from V1 in every respect relevant to the tests, or the test house's written view that the V1 results still apply, or a re-test of the current revision.
- **Status**: Open — owner to confirm the production revision and what changed
- **Fix recommendation**: (1) Owner confirms the current revision from the drawing register. (2) List every change to the rear section between V1 and current. (3) If nothing relevant to the tests changed, record that here with the drawing revisions and close. (4) If anything relevant changed, ask VOSC in writing whether VO00269 and VO00270 still apply, and decide on a re-test. Until closed, no new claim should be added that current production "is" tested; the present wording says the rear travel seat "has been" tested, which is true of the V1 article.

## Documentation completeness check

- Clause 8 and the claim changes shipped with no plan or session log; the owner approval record is now in AUDIT-003. Status docs updated by this audit.
- Middleware behaviour is undocumented (AUDIT-008).
- Canonical terminology corrected (AUDIT-004, resolved).
- `SCHEMA_AND_CONTRACTS_CANONICAL.md` Product entity omits fields the site relies on (`safetyNote`, `leadTime`, `metaDescription`, `madeToOrder`, `compatibleVehicles`, `mpn`, variant `stripePriceId`). Pre-existing, not introduced by these commits; note for the next documentation pass.
- `docs/audits/active/` still holds two March 2026 sprint audits marked pass/complete with no open issues. They belong in `docs/audits/resolved/2026-03/`.

## Test verification performed

- **Automated**:
  - [x] `npm run build` — passes (prebuild `check-blog-prices`: clean; 34 pages prerendered; draft posts correctly excluded)
  - [x] `node scripts/audit-meta.mjs` — 34 pages, 0 meta descriptions over 160 characters, 0 non-www canonicals
  - [x] Pattern search of `src/`, `dist/client`, `dist/server`, `docs/`, `homepage-v2/`, `public/` for retracted wording
  - [ ] Stripe Product names — not run, no API key (AUDIT-002)
- **Manual**:
  - [x] Read both VOSC summaries and compared every stated fact on the certifications page, clause 8, FAQ, product data and blog
  - [x] Fetched the three gov.uk pages and checked each attributed statement
  - [x] Live `www.roamsystems.co.uk`: `/certifications` titled "Testing & Quality"; `/installers` "Experienced Installers"; `/policies/terms` shows clause 8 "Testing, certification and installation", last updated 13 November 2026; product page and homepage show "M1 Tested" with no old wording; Merchant feed title and description updated
  - [x] `git`: `main` == `origin/main` == `terms-test-scope` at 55058dc; working tree clean before this audit
  - [ ] Live apex-host redirect and `/api/*` exemption — blocked by network policy here (AUDIT-008)

## Resolution / follow-up

- **Re-opened 2026-11-13**: AUDIT-001 was closed on the owner's confirmation and this audit was briefly moved to resolved. The owner then stated that current production is "V3 i believe", while the VOSC summaries relate to V1. That is recorded as AUDIT-012 (P1, open), so the audit is back in `docs/audits/active/`.
- Owner decisions recorded 2026-11-13: Full Width has the same rear section as the tested article (001); proposed gov.uk sentence rejected (007); collateral wording approved (006); owner will check social posts and rename the Stripe Product himself (005, 002); the old Roam Systems company is closed and ROAM Systems now trades under Romark; the flyer will be redone later; on the recommendation that a solicitor read clause 8, the owner replied "C8: ok" — no solicitor review is recorded.
- Still open: **012 (P1)**; Stripe Product names (002, owner); content-pipeline claims rule and old social drafts (005); price list prices and company details, and the flyer (006 follow-ups); P3 items 008-011.
- When AUDIT-012 is resolved, move this file to `docs/audits/resolved/2026-11/` and update `PROJECT_STATUS.md`.
