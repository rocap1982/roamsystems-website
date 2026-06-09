---
last_updated: 2026-06-08
active_sprint: ""
stage: ""
---

# Current Status

## Active Sprint

None — Sprint 005 completed.

## Stage

No active sprint.

## This Week's Priorities

- [ ] (Optional) Verify live Stripe prices: `node --env-file=.env scripts/verify-stripe-prices.mjs` with a read-only key — confirms each `stripePriceId` charges the products.json amount and uses `tax_behavior=exclusive`.
- [ ] Set `MARKETING_API_TOKEN` env var on Railway
- [ ] Submit Google Merchant feed to Google Merchant Center

## Blockers

None. (Stripe price verification needs a read-only key in `.env` from the owner — not blocking other work.)

## Recently Closed Work

| Work | Date | Notes |
|------|------|-------|
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
