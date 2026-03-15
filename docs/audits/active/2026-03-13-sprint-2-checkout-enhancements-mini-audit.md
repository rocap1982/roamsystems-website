---
doc_type: mini_audit
status: complete
created: 2026-03-13
scope: "Sprint 2: Checkout enhancements + form migration"
surfaces_reviewed:
  - checkout API contract (POST /api/checkout)
  - webhook endpoint (POST /api/webhook)
  - contact/form endpoint (POST /api/contact)
  - email utility (src/lib/email.ts)
  - success page SSR (src/pages/checkout/success.astro)
  - canonical docs (SCHEMA_AND_CONTRACTS, PLATFORM_OVERVIEW, TERMINOLOGY)
---

# Mini Audit: Sprint 2 — Checkout Enhancements + Form Migration

## Canonical Surfaces Reviewed

### POST /api/checkout (modified)

- **Code**: `src/pages/api/checkout.ts`
- **Contract change**: Added `shipping_address_collection`, `automatic_tax`, `customer_creation`, `shipping_options` to Stripe session creation
- **Schema doc updated**: Yes — `docs/reference/SCHEMA_AND_CONTRACTS_CANONICAL.md`
- **Drift**: None detected

### POST /api/webhook (new)

- **Code**: `src/pages/api/webhook.ts`
- **Contract**: Stripe signature verification, `checkout.session.completed` handler, sends confirmation email
- **Schema doc updated**: Yes
- **Drift**: None detected

### POST /api/contact (new)

- **Code**: `src/pages/api/contact.ts`
- **Contract**: Accepts JSON with type/name/email/phone/subject/message/basketItems/basketTotal, sends via Resend
- **Schema doc updated**: Yes — form contracts section updated
- **Drift**: None detected

### Success page (modified)

- **Code**: `src/pages/checkout/success.astro`
- **Change**: Converted from static to SSR (`prerender = false`), server-side Stripe session retrieval
- **Platform doc updated**: Yes — pages table updated, stale "no SSR" invariant removed

### Email utility (new)

- **Code**: `src/lib/email.ts`
- **Functions**: `sendConfirmationEmail()` (order confirmation), `sendFormEmail()` (contact/enquiry forms)
- **Platform doc updated**: Yes — Resend added to architecture

### Contact form + Enquiry form (modified)

- **Code**: `src/pages/contact.astro`, `src/layouts/Layout.astro`
- **Change**: FormSubmit.co removed, replaced with server-side `/api/contact` endpoint using Resend
- **Schema doc updated**: Yes — form contracts section updated
- **Terminology doc updated**: Yes — FormSubmit.co entry replaced with Resend

## Issues Found

| ID | Priority | Description | Status |
|----|----------|-------------|--------|
| — | — | No issues found | — |

## Environment Variables

| Variable | Documented | Required for |
|----------|-----------|-------------|
| `STRIPE_SECRET_KEY` | Yes | Checkout, webhook, success page |
| `STRIPE_WEBHOOK_SECRET` | Yes | Webhook signature verification |
| `STRIPE_SHIPPING_RATE_ID` | Yes | Shipping rate on checkout (optional) |
| `RESEND_API_KEY` | Yes | Email sending (order confirmation + forms) |

## Testing Performed

- `npm run build` — passes cleanly
- Code review via `/check-sprint` — no P0/P1 issues
- Manual test items deferred to user (Stripe Dashboard setup, live payment flow, webhook verification)

## Verdict

All canonical surfaces are in sync with the implementation. No drift detected.
