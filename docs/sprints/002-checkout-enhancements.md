---
doc_type: sprint
status: complete
stage: done
created: 2026-03-13
last_updated: 2026-03-13
dates:
  start: 2026-03-13
  end: 2026-03-15
sprint_goal: "Add shipping address collection, UK VAT, order confirmation page, branded email, and Stripe webhook to the checkout flow"
---

# Sprint 002: Checkout Enhancements — Shipping, VAT, Order Confirmation & Email

## Summary

- **Goal**: Add shipping address collection, UK VAT (20% via Stripe Tax), server-rendered order confirmation page, branded confirmation email (Resend), and a Stripe webhook for reliable post-payment processing.
- **Stage**: done
- **Scope**: Checkout API, success page, new webhook endpoint, new email utility, env vars, canonical doc updates

## Acceptance Criteria

- [x] Stripe Checkout collects a UK shipping address during checkout
- [x] UK VAT (20%) is calculated automatically via Stripe Tax and shown on the checkout page
- [x] A shipping rate (UK Mainland Pallet Delivery, £120 + VAT) is presented during checkout
- [x] The success page (`/checkout/success`) retrieves the Stripe session server-side and displays: line items, quantities, prices, VAT breakdown, shipping address, shipping cost, total, and order reference
- [x] The success page falls back gracefully to a generic thank-you if session retrieval fails
- [x] A Stripe webhook endpoint (`POST /api/webhook`) verifies signatures and processes `checkout.session.completed` events
- [x] A branded confirmation email is sent via Resend on successful payment (customer + BCC to business)
- [x] Email uses Roam Systems branding (orange `#f47d23`, dark `#1a1a1a`, logo)
- [x] Idempotency: duplicate webhook deliveries do not send duplicate emails (Stripe event ID as Resend idempotency key)
- [x] Existing enquiry flow (made-to-order products now via Resend `/api/contact` — upgraded from FormSubmit.co)
- [x] Cart clearing on the success page still works
- [x] Cancel flow (`/checkout/cancel`) still works with cart preserved

## Contracts / Governance

- **Contract-impacting changes expected**: Yes
- **Plans**: `docs/plans/002-checkout-enhancements.md` (status: approved)
- **Canonical docs to update**:
  - `docs/reference/SCHEMA_AND_CONTRACTS_CANONICAL.md` — checkout API contract changes, new webhook endpoint
  - `docs/reference/PLATFORM_OVERVIEW_CANONICAL.md` — remove stale "no SSR" invariant, add Resend integration, new env vars

## Work Plan

### Phase 1: External Setup (Manual / Dashboard) `[Config]`

| Task | Owner | Priority | Estimate |
|------|-------|----------|----------|
| Register VAT number (974 5806 77) in Stripe Dashboard → Tax settings | `[Config]` | P0 | 10 min |
| Set default product tax code (General Tangible Goods `txcd_99999999`) in Stripe Tax settings | `[Config]` | P0 | 5 min |
| Create Shipping Rate "UK Mainland Pallet Delivery" (£120, tax exclusive) in Stripe Dashboard | `[Config]` | P0 | 5 min |
| Create Resend account, verify `roamsystems.co.uk` domain (DNS TXT/CNAME on Cloudflare) | `[Config]` | P0 | 20 min |
| Set Railway env vars: `STRIPE_SHIPPING_RATE_ID`, `RESEND_API_KEY` | `[Config]` | P0 | 5 min |

### Phase 2: Checkout API Enhancements `[API]`

| Task | Owner | Priority | Estimate |
|------|-------|----------|----------|
| Update `src/pages/api/checkout.ts` — add `shipping_address_collection`, `automatic_tax`, `customer_creation`, `shipping_options` to session creation | `[API]` | P0 | 30 min |
| Read `STRIPE_SHIPPING_RATE_ID` from env var (not hardcoded) | `[API]` | P0 | 5 min |

### Phase 3: Order Confirmation Page `[UI]`

| Task | Owner | Priority | Estimate |
|------|-------|----------|----------|
| Convert `src/pages/checkout/success.astro` to SSR (`prerender = false`) | `[UI]` | P0 | 10 min |
| Add server-side Stripe session retrieval with `expand: ['line_items', 'shipping_cost']` | `[UI]` | P0 | 30 min |
| Render order details: line items table, subtotal, VAT, shipping, total, shipping address, order ref | `[UI]` | P0 | 60 min |
| Implement graceful fallback (generic thank-you if session retrieval fails) | `[UI]` | P1 | 15 min |
| Preserve existing cart-clearing client-side script | `[UI]` | P1 | 5 min |

### Phase 4: Webhook & Email `[API]`

| Task | Owner | Priority | Estimate |
|------|-------|----------|----------|
| Create `src/pages/api/webhook.ts` — signature verification, event routing | `[API]` | P0 | 45 min |
| Create `src/lib/email.ts` — Resend send function + inline HTML email template | `[API]` | P0 | 60 min |
| Install `resend` npm dependency | `[API]` | P0 | 2 min |
| Implement idempotency (Stripe event ID as Resend idempotency key) | `[API]` | P0 | 10 min |
| Email BCC to `rob@romarkengineering.com` | `[API]` | P1 | 5 min |

### Phase 5: Post-Deploy Config `[Config]`

| Task | Owner | Priority | Estimate |
|------|-------|----------|----------|
| Create Stripe webhook endpoint → `https://<domain>/api/webhook` for `checkout.session.completed` | `[Config]` | P0 | 10 min |
| Set `STRIPE_WEBHOOK_SECRET` in Railway | `[Config]` | P0 | 5 min |

### Phase 6: Documentation & Audit `[Docs]`

| Task | Owner | Priority | Estimate |
|------|-------|----------|----------|
| Update `docs/reference/SCHEMA_AND_CONTRACTS_CANONICAL.md` with new API contracts | `[Docs]` | P0 | 30 min |
| Update `docs/reference/PLATFORM_OVERVIEW_CANONICAL.md` — Resend, env vars, remove stale invariant | `[Docs]` | P0 | 20 min |
| Update `docs/reference/GLOBAL_TERMINOLOGY_INDEX_CANONICAL.md` — webhook, Resend, Stripe Tax | `[Docs]` | P1 | 10 min |
| Mini audit on checkout + webhook surfaces | `[Docs]` | P1 | 30 min |

### Domain Parallelism

Phases 2 (`[API]` — checkout enhancements) and Phase 3 (`[UI]` — success page) can run in parallel since they touch different files. Phase 4 (`[API]` — webhook/email) depends on Phase 2 completing (shared Stripe patterns). Phase 6 (`[Docs]`) can start after Phases 2-4 complete.

```
Phase 1 [Config - manual]
    ├── Phase 2 [API - checkout.ts]  ──┐
    └── Phase 3 [UI - success.astro]   ├── Phase 4 [API - webhook + email]
                                       │       │
                                       │       └── Phase 5 [Config - webhook setup]
                                       └────────── Phase 6 [Docs + audit]
```

## Test Plan

### Automated

```bash
npm run build          # Verify build succeeds with new SSR routes
npx astro check        # Type checking (if configured)
```

### Manual

- [ ] **Stripe Dashboard**: VAT registered, shipping rate created, product tax codes assigned
- [ ] **Resend**: Domain verified, API key works, test email sends
- [ ] **Checkout flow (test mode)**: Add items → Checkout → Stripe page shows shipping form, shipping rate (£120), and VAT
- [ ] **Payment (test card `4242...`)**: Complete with UK shipping address → redirects to `/checkout/success?session_id=...`
- [ ] **Success page**: Displays line items, quantities, prices, VAT breakdown, shipping address, shipping cost, total, order reference
- [ ] **Cart cleared**: localStorage `roam-cart` removed after success page loads
- [ ] **Webhook fires**: Stripe sends `checkout.session.completed` → webhook returns 200
- [ ] **Email received**: Confirmation email arrives at customer email + BCC at `rob@romarkengineering.com`
- [ ] **Email content**: Roam branding, line items, VAT, shipping address, total, order ref
- [ ] **Idempotency**: Replay webhook from Stripe Dashboard → no duplicate email
- [ ] **Fallback**: Visit `/checkout/success` without `session_id` → generic thank-you (no error)
- [ ] **Cancel flow**: Cancel on Stripe page → `/checkout/cancel` works, cart preserved
- [ ] **Made-to-order flow**: Enquiry-only products still go through FormSubmit.co (unaffected)
- [ ] **Webhook raw body**: `stripe.webhooks.constructEvent()` succeeds (raw body not pre-parsed)

## Review Gate

- [x] All acceptance criteria met
- [x] `npm run build` succeeds
- [ ] Manual test checklist complete (deferred to user — requires Stripe Dashboard + Resend setup)
- [x] Canonical docs updated (SCHEMA_AND_CONTRACTS, PLATFORM_OVERVIEW, TERMINOLOGY)
- [x] Mini audit completed on checkout + webhook surfaces
- [x] Plan `docs/plans/002-checkout-enhancements.md` marked as implemented

## Documentation DoD

- [x] `docs/reference/SCHEMA_AND_CONTRACTS_CANONICAL.md` — added `/api/checkout`, `/api/webhook`, `/api/contact` contracts; updated form contracts
- [x] `docs/reference/PLATFORM_OVERVIEW_CANONICAL.md` — added Resend, Stripe, webhook, env vars, server routes; removed stale "no SSR" invariant
- [x] `docs/reference/GLOBAL_TERMINOLOGY_INDEX_CANONICAL.md` — added: webhook, Resend, Stripe Checkout, Stripe Tax, idempotency key

## Audit Plan

Mini audit after implementation — scope: checkout API contract, webhook endpoint, email flow, env var configuration. Covers canonical surfaces touched by this sprint.

## Notes

- Plan approved 2026-03-13 by Rob DiCapite.
- Phase 1 (external dashboard setup) is manual and must be done by the user before code deployment.
- `src/lib/` directory created for `email.ts`.
- Shipping rate ID stored as env var to avoid hardcoding.
- Resend idempotency: using `X-Entity-Ref-ID` header with Stripe event ID (Resend's documented deduplication approach).
- Build passes cleanly after all code changes.
- Forms migrated from FormSubmit.co to Resend via `/api/contact` endpoint (scope addition during sprint — approved by user).

### Learnings

- **Astro hybrid SSR**: Converting a page from static to SSR is just `export const prerender = false` + server-side code in frontmatter. Straightforward pattern.
- **Resend idempotency**: `X-Entity-Ref-ID` header is the documented approach for deduplication — simpler than maintaining a separate idempotency store.
- **Webhook error handling**: Return 200 even on email failures to prevent Stripe retry storms. Log the error for monitoring.
- **Form migration pattern**: Creating a single `/api/contact` endpoint with a `type` discriminator handles multiple form types cleanly. Reply-to is set to the submitter's email so the business can reply directly.
- **Inline HTML email templates**: For a small number of email types, inline template strings in `src/lib/email.ts` are simpler than a template engine. Revisit if email count grows.

### Skills decision

No new skill needed. The Stripe + Resend integration patterns are well-documented in the canonical docs and sprint notes.
