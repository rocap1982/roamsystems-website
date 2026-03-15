---
last_updated: 2026-03-15
active_sprint: ""
stage: idle
---

# Current Status

## Active Sprint

None — between sprints.

## Stage

**idle** — Sprint 003 completed.

## This Week's Priorities

- [x] Sprint 003: YouTube video embed on home page + Instagram social links (done)
- [ ] Complete Phase 1 external setup (Stripe VAT, shipping rate, Resend domain verification)
- [ ] Complete Phase 5 post-deploy config (Stripe webhook endpoint, env vars)
- [ ] Manual testing of full checkout + email flow

## Blockers

None.

## Recently Closed Work

| Work | Date | Notes |
|------|------|-------|
| Sprint 3: Video Embed + Social Links | 2026-03-15 | YouTube video on home page, Instagram added to footer + contact. All gates pass. |
| Sprint 2: Checkout Enhancements | 2026-03-13 | Shipping, VAT, SSR success page, webhook, email, form migration to Resend. |
| Sprint 1: Stripe Checkout | 2026-03-13 | Server-side sessions, enquiry fallback, checkout pages. |
| Railway deployment | 2026-03 | Static Astro site deployed successfully |
| FBS installation | 2026-03-12 | Governance framework populated with project data |

## Notes / Decisions

- Plan `docs/plans/2026-03-15-video-embed-social-links.md` (implemented)
- Plan `docs/plans/002-checkout-enhancements.md` (implemented)
- Forms migrated from FormSubmit.co to Resend via `/api/contact` endpoint
- `stripePriceId` values are placeholders until Stripe account is configured
- Site uses `@astrojs/node` adapter (hybrid mode) for server routes
