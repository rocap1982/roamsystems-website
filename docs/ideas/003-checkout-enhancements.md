---
doc_type: idea
status: accepted
created: 2026-03-13
last_updated: 2026-03-13
owner: "Robert DiCapite"
tags: [stripe, checkout, email, shipping, vat]
related_plans: []
related_sprints: ["docs/sprints/001-stripe-checkout.md"]
---

# Idea: Checkout Enhancements — Shipping, VAT, Order Confirmation & Email

## Summary

Enhance the Stripe Checkout integration with shipping address collection, automatic UK VAT calculation, a rich order confirmation page that displays full order details, and a branded confirmation email sent via Resend. Adds a Stripe webhook handler for reliable post-payment processing.

## Problem / Opportunity

### Current State

- **Success page**: Static thank-you with no order details. The `session_id` query param is passed but never retrieved or used.
- **No email**: The page promises "We'll send you a confirmation email" but nothing sends it.
- **No shipping address**: Stripe session doesn't collect a delivery address — Roam Systems ships physical goods and needs this.
- **No VAT**: UK e-commerce requires VAT; currently no tax calculation.
- **No webhook**: Payment confirmation relies solely on the redirect to `/checkout/success`, which can fail if the customer closes the browser.

### Desired State

1. **Shipping address** collected during Stripe Checkout (UK-only initially)
2. **UK VAT** (20%) calculated automatically by Stripe Tax
3. **Order confirmation page** retrieves the Stripe session server-side and displays: line items, quantities, prices, VAT breakdown, shipping address, total, and order reference
4. **Branded confirmation email** sent via Resend matching the site style (Roam orange `#f47d23`, Barlow headings, dark `#1a1a1a` accents)
5. **Stripe webhook** (`checkout.session.completed`) for reliable email triggering and future order processing

### Why This Matters

- **Legal**: UK e-commerce sites must charge VAT on applicable goods
- **Customer trust**: Professional order confirmation (page + email) is baseline e-commerce expectation
- **Operational**: Shipping address is required to fulfil orders
- **Reliability**: Webhooks ensure confirmation emails are sent even if the customer's browser disconnects

## Constraints

- No database — all order data lives in Stripe. The confirmation page retrieves it on demand from the Stripe API.
- Resend free tier: 100 emails/day, 3,000/month — sufficient for current volume.
- Resend requires a verified sending domain (DNS records on roamsystems.co.uk).
- Stripe Tax requires VAT registration in Stripe Dashboard before enabling.
- Must not break the existing enquiry flow for made-to-order products.

## Architecture / Approach

### 1. Checkout Session Enhancements (API route)

Update `src/pages/api/checkout.ts` to add parameters to `stripe.checkout.sessions.create()`:

```js
shipping_address_collection: {
  allowed_countries: ['GB'],  // UK only initially
},
automatic_tax: {
  enabled: true,
},
customer_creation: 'always',  // Creates Stripe Customer for email + address
```

**Prerequisite**: Register VAT number in Stripe Dashboard → Settings → Tax.

### 2. Order Confirmation Page (server-rendered)

Convert `src/pages/checkout/success.astro` from static to server-rendered (`prerender = false`).

**Server-side logic**:
- Read `session_id` from query params
- Call `stripe.checkout.sessions.retrieve(sessionId, { expand: ['line_items', 'customer_details', 'shipping_details'] })`
- Extract: line items (name, qty, unit price), subtotal, tax, total, shipping address, customer email
- Render in the existing site layout with branded styling

**Graceful fallback**: If session retrieval fails (invalid ID, network error), show the current generic thank-you message rather than an error page.

**Cart clearing**: Keep the existing `localStorage.removeItem('roam-cart')` client-side script.

### 3. Stripe Webhook Handler (new API route)

Create `src/pages/api/webhook.ts` (`prerender = false`):

- Listen for `checkout.session.completed` event
- Verify webhook signature using `STRIPE_WEBHOOK_SECRET` env var
- Extract session data (customer email, line items, shipping, total)
- Send confirmation email via Resend
- Return 200 to acknowledge receipt

**Idempotency**: Use the Stripe event ID as an idempotency key with Resend to prevent duplicate emails.

**Env vars needed**:
- `STRIPE_WEBHOOK_SECRET` — from Stripe Dashboard → Webhooks
- `RESEND_API_KEY` — from Resend dashboard

### 4. Confirmation Email (Resend)

**NPM dependency**: `resend`

**Email template**: Inline HTML matching the site style:
- Header: Roam Systems logo + dark background (`#1a1a1a`)
- Body: Order reference, line items table, subtotal/VAT/total, shipping address
- Footer: Contact info, links to delivery info page
- Fonts: System font stack (web fonts don't work reliably in email clients)
- Accent colour: Roam orange `#f47d23`

**From address**: `orders@roamsystems.co.uk` (requires Resend domain verification — DNS TXT/CNAME records)

### 5. Environment Variables (Railway)

| Variable | Purpose |
|---|---|
| `STRIPE_SECRET_KEY` | Already planned — Stripe API access |
| `STRIPE_WEBHOOK_SECRET` | Webhook signature verification |
| `RESEND_API_KEY` | Email sending |

### Flow Diagram

```
Customer clicks "Checkout — Pay Now"
  → POST /api/checkout (creates session with shipping + tax)
  → Redirect to Stripe hosted page
  → Customer enters card + shipping address
  → Payment succeeds
  → Two parallel paths:
     1. Browser redirect → /checkout/success?session_id=xxx
        → Server retrieves session → renders order details
        → Client clears cart
     2. Stripe webhook → POST /api/webhook
        → Verify signature → retrieve session details
        → Resend API → branded confirmation email to customer
```

## Non-goals

- Order management system or admin dashboard (check Stripe Dashboard directly)
- Inventory tracking or stock management
- Shipping rate calculation (flat rate or free shipping — configured in Stripe Dashboard)
- International shipping (UK only for now)
- Subscription payments
- Refund/cancellation emails (handle manually via Stripe Dashboard for now)

## Open Questions

All resolved:

1. ~~**Domain verification for Resend**~~: **RESOLVED** — DNS managed via Cloudflare. Add Resend TXT/CNAME records there.
2. ~~**VAT registration**~~: **RESOLVED** — Romark Engineering Ltd is VAT-registered. VAT No: 974 5806 77 (Co Reg No: 07411656). Configure in Stripe Dashboard → Settings → Tax.
3. ~~**Shipping rates**~~: **RESOLVED** — UK Mainland Pallet Delivery: £120 + VAT. Configure as a Stripe Checkout shipping rate.
4. ~~**Reply-to address**~~: **RESOLVED** — `sales@roamsystems.co.uk`
5. ~~**BCC/notification**~~: **RESOLVED** — BCC all order confirmations to `rob@romarkengineering.com`

## Traceability

- `docs/reference/SCHEMA_AND_CONTRACTS_CANONICAL.md` — checkout API contract changes (new session params)
- `docs/reference/PLATFORM_OVERVIEW_CANONICAL.md` — new integration (Resend), new env vars
- `PROJECT_STATUS.md` — tech stack update (Resend, webhook)
