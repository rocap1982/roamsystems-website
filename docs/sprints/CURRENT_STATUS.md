---
last_updated: 2026-03-15
active_sprint: ""
stage: idle
---

# Current Status

## Active Sprint

None — between sprints.

## Stage

**idle** — Sprint 004 completed.

## This Week's Priorities

- [x] Sprint 004: SEO Phase 2 — OG tags, Twitter Cards, JSON-LD (done)
- [x] Deploy Sprint 004 and validate with Google Rich Results Test
- [ ] Complete Phase 1 external setup (Stripe VAT, shipping rate, Resend domain verification)
- [ ] Complete Phase 5 post-deploy config (Stripe webhook endpoint, env vars)
- [ ] Manual testing of full checkout + email flow

## Blockers

None.

## Recently Closed Work

| Work | Date | Notes |
|------|------|-------|
| Sprint 4: SEO Phase 2 — OG + JSON-LD | 2026-03-15 | OG tags, Twitter Cards, Organization/Product/BreadcrumbList/LocalBusiness JSON-LD. All gates pass. |
| SEO Phase 1 (small fix) | 2026-03-15 | Sitemap, robots.txt, canonical URLs, meta descriptions deployed. Sitemap submitted to Google Search Console. |
| Sprint 3: Video Embed + Social Links | 2026-03-15 | YouTube video on home page, Instagram added to footer + contact. |
| Sprint 2: Checkout Enhancements | 2026-03-13 | Shipping, VAT, SSR success page, webhook, email, form migration to Resend. |
| Sprint 1: Stripe Checkout | 2026-03-13 | Server-side sessions, enquiry fallback, checkout pages. |

## Notes / Decisions

- Plan `docs/plans/004-seo-phase2-social-rich-results.md` (implemented)
- SEO Phase 1 deployed as small fix — sitemap live and submitted to GSC
- Post-deploy validation complete: JSON-LD valid (Google Rich Results Test), OG tags valid (Facebook Sharing Debugger)
