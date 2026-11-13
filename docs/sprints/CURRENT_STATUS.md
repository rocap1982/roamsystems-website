---
last_updated: 2026-11-13
active_sprint: ""
stage: ""
---

# Current Status

## Active Sprint

None — Sprint 005 completed.

## Stage

No active sprint.

## This Week's Priorities

- [ ] **P1 — Owner**: VOSC summaries relate to design revision V1; owner believes current production is V3. Confirm the revision, list what changed in the rear section since V1, and ask VOSC in writing if anything relevant to the tests changed. (AUDIT-2026-11-13-012)
- [x] P1 closed 2026-11-13: owner confirmed the Full Width configuration has the same rear section as the article VOSC tested. (AUDIT-2026-11-13-001)
- [ ] Owner: rename the Stripe Product to "M1 Tested U-Shape Seating Frame" — checkout page, receipts and order emails take the name from Stripe. (AUDIT-2026-11-13-002)
- [ ] Trade collateral follow-ups (AUDIT-2026-11-13-006): claim wording approved and on main. Price list prices are out of date (owner) and its footer names the closed Roam Systems Ltd — awaiting owner confirmation of prices (incl. SWB/LWB Kitchen Pod Package) and footer wording; do not send the price list until confirmed. A5 flyer is out of scope by owner decision 2026-11-13.
- [ ] Content pipeline (AUDIT-2026-11-13-005): add an approved-claims / banned-phrases rule for the weekly generator; old social drafts still carry retracted claims. Owner is checking published social posts.
- [ ] P3s from `docs/audits/active/2026-11-13-m1-claims-terms-clause8-mini.md`: blog "Certification" badge, `homepage-v2/` prototype, FAQ ordering/warranty answers, middleware docs.
- [x] Mini-audit of the T&Cs/consent change — DONE 2026-06-12: Aligned, 0 P0/P1, 3 P3 (`docs/audits/active/2026-06-12-terms-acceptance-ip-mini.md`).
- [x] Fix the 3 audit P3s — DONE 2026-06-12, deployed; audit moved to `docs/audits/resolved/2026-06/2026-06-12-terms-acceptance-ip-mini.md`.
- [x] Lead time confirmed by owner 2026-06-12: standard 2-4 weeks, bespoke trimming up to 6 weeks. All five surfaces updated (products.json leadTime incl. Upholstery products, FAQ.tsx, delivery.astro, shipping.astro, terms.astro) and deployed.
- [ ] Owner: send revised Agile IP email (fabricator customer was refunded in full 2026-06-12 — no drawings released, no bed shipped; licence template at `docs/business-assets/ROAM_Drawing_Release_Installation_Licence.docx` retained for future trade customers).
- [ ] (Optional) Verify live Stripe prices: `node --env-file=.env scripts/verify-stripe-prices.mjs` with a read-only key — confirms each `stripePriceId` charges the products.json amount and uses `tax_behavior=exclusive`.
- [ ] Set `MARKETING_API_TOKEN` env var on Railway
- [ ] Submit Google Merchant feed to Google Merchant Center

## Blockers

None. (2026-06-12: Stripe ToS URL set by owner; terms-acceptance change deployed — deploy da2ffa2a, commit 3b3918d — and verified live: session creation returns consent_collection.terms_of_service=required; terms page, footer marking, product lead-time line all confirmed serving.)

## Recently Closed Work

| Work | Date | Notes |
|------|------|-------|
| Test-claim wording alignment + terms clause 8 (small fixes, 4 commits) | 2026-11-13 | "M1 Certified" -> "M1 Tested"; crash-test and legal-requirement claims replaced with facts from VOSC summaries VO00269/VO00270; clause 8 states what the tests cover and do not cover and installer responsibilities; "Approved" -> "Experienced" installers; certifications page retitled "Testing & Quality". On main and verified live. Mini-audit ACTIVE: `docs/audits/active/2026-11-13-m1-claims-terms-clause8-mini.md` (1 open P1: AUDIT-012 tested revision V1 vs production V3; owner approved wording 2026-11-13). |
| Middleware: no 301 for `/api/*` on non-www host (small fix, PR #2) | 2026-10-06 | Contact form and checkout POSTs on `roamsystems.co.uk` were being 301'd cross-origin and failing with "Failed to fetch". Commit b71544b. |
| T&Cs overhaul + checkout terms-acceptance + design marking (plan 2026-06-11) | 2026-06-11 | Full terms rewrite (IP/design-rights clause citing UK RDs 6266396-9 + EU RCD 015033319, contract-at-dispatch, Romark Engineering company details); Stripe `consent_collection` required checkbox; consent line in order email; refund policy CCR-2013 patch; basket notice; UK design numbers added to certifications page + footer marking. Build passes. AWAITING: Stripe Dashboard ToS URL, then deploy. |
| Checkout order-detail capture (small fix) | 2026-06-08 | `/api/checkout` now collects phone + required vehicle dropdown (6 vehicles + "other") + optional year/reg; confirmation email adds a Customer Details block. Canonical doc updated. Deployed & verified live. |
| Homepage marquee + vehicle-drift fixes (small fix) | 2026-06-08 | Marquee now computes flagship price ("From £2,050", was wrongly "From £356"); all products' `compatibleVehicles` + Merchant-feed label map + `/vehicles` copy updated to 6 vehicles. Deployed & verified live. Audit RESOLVED: `docs/audits/resolved/2026-06/2026-06-08-checkout-order-detail-mini.md` (all 3 P2 fixed). |
| Price rise — materials cost pass-through (small fix) | 2026-05-11 | 9 of 11 variants raised in `products.json`. 7 new Stripe Prices created (GBP, `tax_behavior=exclusive`, attached to existing parent Products); old Price IDs left active for one-line rollback. Locker SWB/LWB unchanged. Build passes; Merchant feed reflects new VAT-inclusive prices. |
| Sprint 005: SEO Marketing System | 2026-03-15 | Vehicle pages, blog, Google Merchant feed, content pipeline, scheduled tasks. All gates pass. |
| Sprint 4: SEO Phase 2 — OG + JSON-LD | 2026-03-15 | OG tags, Twitter Cards, Organization/Product/BreadcrumbList/LocalBusiness JSON-LD. All gates pass. |
| SEO Phase 1 (small fix) | 2026-03-15 | Sitemap, robots.txt, canonical URLs, meta descriptions deployed. Sitemap submitted to Google Search Console. |
| Sprint 3: Video Embed + Social Links | 2026-03-15 | YouTube video on home page, Instagram added to footer + contact. |
| Sprint 2: Checkout Enhancements | 2026-03-13 | Shipping, VAT, SSR success page, webhook, email, form migration to Resend. |
| Sprint 1: Stripe Checkout | 2026-03-13 | Server-side sessions, enquiry fallback, checkout pages. |

## Notes / Decisions

- Plan `docs/plans/005-automated-seo-marketing.md` (approved + implemented)
- 6 vehicles (T5, T6, T6.1, Transit Custom, Renault Trafic, Nissan Primastar). All surfaces now consistent: `vehicle.compatibleProducts`, product-side `compatibleVehicles`, Merchant-feed `custom_label_0` (label map), and `/vehicles` copy all name all 6 (AUDIT-2026-06-08-005/006 resolved).
- Marketing API requires `MARKETING_API_TOKEN` Bearer auth (set on Railway before first use)
