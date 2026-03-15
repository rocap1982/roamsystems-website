---
last_updated: 2026-03-15
active_sprint: docs/sprints/003-video-embed-social-links.md
stage: verification
---

# Current Status

## Active Sprint

Sprint 003: Video Embed + Social Links — `docs/sprints/003-video-embed-social-links.md`

## Stage

**verification** — Implementation complete, awaiting code review and verification.

## This Week's Priorities

- [ ] Sprint 003: YouTube video embed on home page + Instagram social links
- [ ] Complete Phase 1 external setup (Stripe VAT, shipping rate, Resend domain verification)
- [ ] Complete Phase 5 post-deploy config (Stripe webhook endpoint, env vars)
- [ ] Manual testing of full checkout + email flow

## Blockers

None.

## Recently Closed Work

| Work | Date | Notes |
|------|------|-------|
| Sprint 2: Checkout Enhancements | 2026-03-13 | Shipping, VAT, SSR success page, webhook, email, form migration to Resend. All code gates pass. Manual testing pending (Stripe/Resend dashboard setup required). |
| Sprint 1: Stripe Checkout | 2026-03-13 | Server-side sessions, enquiry fallback, checkout pages. All gates pass. |
| Railway deployment | 2026-03 | Static Astro site deployed successfully |
| FBS installation | 2026-03-12 | Governance framework populated with project data |

## Notes / Decisions

- Plan `docs/plans/2026-03-15-video-embed-social-links.md` (approved)
- Plan `docs/plans/002-checkout-enhancements.md` (implemented)
- Forms migrated from FormSubmit.co to Resend via `/api/contact` endpoint
- `stripePriceId` values are placeholders until Stripe account is configured
- Site uses `@astrojs/node` adapter (hybrid mode) for server routes
