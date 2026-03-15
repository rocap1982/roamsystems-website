---
doc_type: plan
status: implemented
created: 2026-03-13
last_updated: 2026-03-13
author: "AI (Claude)"
approver: "Rob DiCapite"
related_issues: "None"
---

# Plan: Checkout Enhancements — Shipping, VAT, Order Confirmation & Email

## Problem Statement

### Current State

- **Success page** (`src/pages/checkout/success.astro`): Static thank-you with no order details. The `session_id` query param is passed in the URL but never retrieved or used — no server-side session lookup.
- **No email**: The page says "We'll send you a confirmation email shortly" but nothing sends it.
- **No shipping address**: The checkout session in `src/pages/api/checkout.ts` (line 51) does not include `shipping_address_collection` — Roam Systems ships physical goods and needs a delivery address.
- **No VAT**: UK B2C e-commerce requires VAT display; the current checkout passes prices as-is with no tax configuration.
- **No webhook**: Payment confirmation relies solely on the browser redirect to `/checkout/success`. If the customer closes their browser after paying, no email is sent and no server-side record is created.

### Desired State

1. **Shipping address** collected during Stripe Checkout (UK-only initially)
2. **UK VAT** (20%) calculated automatically via Stripe Tax
3. **Order confirmation page** retrieves the Stripe session server-side and displays: line items, quantities, prices, VAT breakdown, shipping address, total, and order reference
4. **Branded confirmation email** sent via Resend with site styling (Roam orange `#f47d23`, dark `#1a1a1a` accents)
5. **Stripe webhook** (`checkout.session.completed`) for reliable email delivery and future order processing
6. **Shipping rate** — UK Mainland Pallet Delivery (£120 + VAT) configured as a Stripe Shipping Rate

### Why This Matters

- **Legal**: UK e-commerce sites must charge and display VAT on applicable goods
- **Customer trust**: Professional order confirmation (page + email) is baseline e-commerce expectation
- **Operational**: Shipping address is required to fulfil physical orders
- **Reliability**: Webhooks ensure confirmation emails are sent even if the customer's browser disconnects after payment

## Proposed Solution

### Canonical Changes Required

| Document | Change Type | Description |
|----------|-------------|-------------|
| `docs/reference/SCHEMA_AND_CONTRACTS_CANONICAL.md` | Major | `/api/checkout` POST session gains `shipping_address_collection`, `automatic_tax`, `customer_creation`, `shipping_options` params (request body unchanged). New endpoint: `POST /api/webhook` (Stripe-signed payload; responds `{ received: true }`). Success page becomes SSR with `prerender = false`. |
| `docs/reference/PLATFORM_OVERVIEW_CANONICAL.md` | Major | **Remove stale invariant** "Static site — no server-side rendering or API routes" (already violated by Sprint 1's `/api/checkout`). Add Resend integration, webhook architecture, new env vars (`STRIPE_WEBHOOK_SECRET`, `RESEND_API_KEY`, `STRIPE_SHIPPING_RATE_ID`). |
| `docs/reference/GLOBAL_TERMINOLOGY_INDEX_CANONICAL.md` | Minor | Add terms: webhook, Resend, Stripe Tax |

### Proposed Specification

#### 1. Checkout Session Enhancements (`src/pages/api/checkout.ts`)

Add shipping address collection, automatic tax, and customer creation to the existing `stripe.checkout.sessions.create()` call:

```typescript
const session = await stripe.checkout.sessions.create({
  mode: 'payment',
  line_items: body.items.map((item) => ({
    price: item.stripePriceId,
    quantity: item.qty,
  })),
  shipping_address_collection: {
    allowed_countries: ['GB'],
  },
  automatic_tax: {
    enabled: true,
  },
  customer_creation: 'always',
  shipping_options: [
    { shipping_rate: 'shr_XXXXXXXXXXXX' }, // UK Mainland Pallet Delivery £120+VAT — created in Stripe Dashboard
  ],
  success_url: `${origin}/checkout/success?session_id={CHECKOUT_SESSION_ID}`,
  cancel_url: `${origin}/checkout/cancel`,
});
```

**Prerequisites** (Stripe Dashboard, before code deployment):
- Register VAT number (974 5806 77) in Stripe → Settings → Tax
- Set a **default product tax code** (e.g., `txcd_99999999` — General Tangible Goods) in Stripe → Settings → Tax → Product and prices tax settings, or assign individual tax codes to each Product/Price. Without this, `automatic_tax` may error or apply no tax.
- Create a Shipping Rate: "UK Mainland Pallet Delivery" at £120.00 (tax behaviour: exclusive — Stripe Tax adds 20% VAT)
- Copy the `shr_` ID into an env var (`STRIPE_SHIPPING_RATE_ID`) to avoid hardcoding

**New env var**: `STRIPE_SHIPPING_RATE_ID` — the Stripe Shipping Rate ID for UK pallet delivery.

#### 2. Order Confirmation Page — Server-Rendered (`src/pages/checkout/success.astro`)

Convert from static to SSR (`export const prerender = false` in frontmatter script). This follows the same pattern already working in `src/pages/api/checkout.ts` — the Astro config has no `output` field, which in Astro 6 defaults to `static` with per-route SSR opt-in via `prerender = false`. The success page will no longer be pre-rendered at build time (slightly slower cold-start), which is acceptable since it needs live Stripe data.

**Server-side logic**:
```typescript
export const prerender = false;

import Stripe from 'stripe';

const sessionId = Astro.url.searchParams.get('session_id');
let session = null;
let lineItems = null;

if (sessionId && import.meta.env.STRIPE_SECRET_KEY) {
  try {
    const stripe = new Stripe(import.meta.env.STRIPE_SECRET_KEY);
    session = await stripe.checkout.sessions.retrieve(sessionId, {
      expand: ['line_items', 'shipping_cost'],
    });
    // Note: customer_details and shipping_details are returned by default (not expandable sub-objects).
    // shipping_cost must be expanded to get the shipping rate details.
    lineItems = session.line_items?.data ?? [];
  } catch (err) {
    console.error('Failed to retrieve checkout session:', err);
    // Fall through to generic thank-you
  }
}
```

**Rendering**:
- If session retrieved successfully: display line items table (name, qty, unit price), subtotal, tax amount, shipping, total, shipping address, customer email, order reference (`session.payment_intent` or `session.id` truncated)
- If session retrieval fails: show the current generic thank-you message (graceful fallback)
- Cart clearing: keep existing `localStorage.removeItem('roam-cart')` client-side script

#### 3. Stripe Webhook Handler (`src/pages/api/webhook.ts` — new file)

```typescript
export const prerender = false;

import type { APIRoute } from 'astro';
import Stripe from 'stripe';

const stripe = new Stripe(import.meta.env.STRIPE_SECRET_KEY);
const webhookSecret = import.meta.env.STRIPE_WEBHOOK_SECRET;

export const POST: APIRoute = async ({ request }) => {
  if (!webhookSecret) {
    return new Response('Webhook secret not configured', { status: 500 });
  }

  const payload = await request.text();
  const sig = request.headers.get('stripe-signature');

  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(payload, sig!, webhookSecret);
  } catch (err) {
    console.error('Webhook signature verification failed:', err);
    return new Response('Invalid signature', { status: 400 });
  }

  if (event.type === 'checkout.session.completed') {
    const session = event.data.object as Stripe.Checkout.Session;
    // Retrieve full session with expanded data
    const fullSession = await stripe.checkout.sessions.retrieve(session.id, {
      expand: ['line_items', 'shipping_cost'],
    });
    // customer_details and shipping_details are returned by default (not expandable).
    // Send confirmation email via Resend (see §4)
    await sendConfirmationEmail(fullSession, event.id);
  }

  return new Response(JSON.stringify({ received: true }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  });
};
```

**Key behaviours**:
- Verifies webhook signature using `STRIPE_WEBHOOK_SECRET`
- Only processes `checkout.session.completed` events
- Uses `event.id` as Resend idempotency key to prevent duplicate emails
- Returns 200 promptly to avoid Stripe retries

**Env var**: `STRIPE_WEBHOOK_SECRET` — from Stripe Dashboard → Webhooks after configuring the endpoint URL.

#### 4. Confirmation Email via Resend

**NPM dependency**: `resend` (add to `package.json`)

**Email content**:
- **From**: `orders@roamsystems.co.uk` (requires Resend domain verification — DNS TXT/CNAME records on Cloudflare)
- **Reply-To**: `sales@roamsystems.co.uk`
- **BCC**: `rob@romarkengineering.com` (business notification)
- **Subject**: "Order Confirmed — Roam Systems [order ref]"
- **Body** (inline HTML):
  - Header: Roam Systems logo on dark background (`#1a1a1a`)
  - Order reference
  - Line items table: product name, qty, unit price
  - Subtotal, VAT, shipping, total
  - Shipping address
  - Footer: contact info, link to delivery info page
  - Accent colour: Roam orange `#f47d23`
  - Fonts: system font stack (web fonts unreliable in email clients)

**Idempotency**: Pass `event.id` (Stripe webhook event ID) as Resend's `Idempotency-Key` header to prevent duplicate sends on webhook retries.

**Env var**: `RESEND_API_KEY` — from Resend dashboard.

**DNS setup** (Cloudflare): Add Resend's verification TXT and CNAME records for `roamsystems.co.uk` to enable sending from `orders@roamsystems.co.uk`.

#### 5. Environment Variables Summary

| Variable | Purpose | Where to set |
|---|---|---|
| `STRIPE_SECRET_KEY` | Stripe API access | Already configured in Railway |
| `STRIPE_WEBHOOK_SECRET` | Webhook signature verification | Railway — after Stripe webhook configured |
| `STRIPE_SHIPPING_RATE_ID` | Shipping rate for checkout sessions | Railway — after Stripe shipping rate created |
| `RESEND_API_KEY` | Email sending via Resend | Railway — after Resend account setup |

### Flow Diagram

```
Customer clicks "Checkout — Pay Now"
  → POST /api/checkout (creates session with shipping + tax + shipping rate)
  → Redirect to Stripe hosted page
  → Customer enters card + shipping address
  → Payment succeeds
  → Two parallel paths:
     1. Browser redirect → /checkout/success?session_id=xxx
        → Server retrieves session → renders order details (line items, VAT, shipping address, total)
        → Client clears cart
     2. Stripe webhook → POST /api/webhook
        → Verify signature → retrieve session details
        → Resend API → branded confirmation email to customer + BCC to business
```

## Implementation Impact

### Code Changes Required

| File | Change Description |
|------|-------------------|
| `src/pages/api/checkout.ts` | Add `shipping_address_collection`, `automatic_tax`, `customer_creation`, `shipping_options` to session creation |
| `src/pages/checkout/success.astro` | Convert to SSR (`prerender = false`); add server-side Stripe session retrieval; render order details with fallback |
| `package.json` | Add `resend` dependency |

### New Files

| File | Purpose |
|------|---------|
| `src/pages/api/webhook.ts` | Stripe webhook handler — signature verification, email dispatch |
| `src/lib/email.ts` | Email template and Resend send function (keeps webhook handler clean). Note: `src/lib/` does not exist yet — create it. This follows Astro's conventional utility directory. |

### Test Changes

No existing test infrastructure. Manual verification plan:

1. **Stripe Dashboard setup**: Register VAT, create shipping rate, create webhook endpoint pointing to `<railway-url>/api/webhook`
2. **Resend setup**: Create account, verify `roamsystems.co.uk` domain, get API key
3. **DNS setup**: Add Resend verification records to Cloudflare
4. **Railway env vars**: Set `STRIPE_WEBHOOK_SECRET`, `STRIPE_SHIPPING_RATE_ID`, `RESEND_API_KEY`
5. **Checkout flow** (Stripe test mode):
   - Add items to cart → click Checkout → verify Stripe page shows shipping address form, shipping rate, and tax
   - Complete with test card `4242 4242 4242 4242` + UK shipping address
   - Verify redirect to `/checkout/success?session_id=...` shows order details (line items, VAT breakdown, shipping address, total)
   - Verify cart is cleared
6. **Webhook + email**: Verify confirmation email arrives at test email address with correct content, styling, and BCC
7. **Webhook raw body**: Verify `request.text()` returns the raw body (not pre-parsed by middleware) for Stripe signature verification. The `@astrojs/node` standalone adapter should pass through the raw body, but this is a known failure point in Node frameworks — test explicitly by checking that `stripe.webhooks.constructEvent()` succeeds.
8. **Idempotency**: Replay webhook event from Stripe Dashboard → verify no duplicate email
9. **Fallback**: Visit `/checkout/success` without `session_id` → verify generic thank-you message (no error)
10. **Cancel flow**: Cancel on Stripe page → verify `/checkout/cancel` still works, cart preserved
11. **Made-to-order flow**: Verify enquiry-only flow is unaffected

### Data / Migration Impact

- No database — all order data lives in Stripe
- No schema changes to `products.json`
- No localStorage changes
- Deployment is additive: new endpoint + converted page; existing routes unchanged

## Migration Plan

No breaking changes.

- The checkout API route gains new parameters — all additive
- The success page gains SSR + order display — falls back gracefully if session retrieval fails
- The webhook endpoint is new — Stripe only calls it after configuration
- Existing enquiry flow is completely unaffected

### Deployment Steps

1. **Pre-deployment** (manual, external):
   - Stripe Dashboard: register VAT number, create shipping rate, note `shr_` ID
   - Resend: create account, verify `roamsystems.co.uk` domain (Cloudflare DNS records)
   - Railway: set `RESEND_API_KEY` and `STRIPE_SHIPPING_RATE_ID` env vars
2. **Deploy code** — Railway rebuilds and restarts Node server
3. **Post-deployment**:
   - Stripe Dashboard: create webhook endpoint → `https://<domain>/api/webhook` → select `checkout.session.completed`
   - Copy webhook signing secret → set `STRIPE_WEBHOOK_SECRET` in Railway
4. **Verify** end-to-end in Stripe test mode
5. **Go live**: switch Stripe keys to live mode, update webhook endpoint to live

### Rollback

- Remove webhook endpoint from Stripe Dashboard (stops events)
- Revert code: success page goes back to static, checkout.ts loses shipping/tax params
- Email sending stops (no webhook = no trigger)
- Core checkout flow (pay and redirect) continues to work even with partial rollback

## Alternatives Considered

### Alternative 1: Send email from success page (no webhook)

- **Description**: Trigger email send from the success page server-side render instead of a webhook
- **Pros**: Simpler — no webhook infrastructure needed
- **Cons**: Email only sends if customer's browser reaches the success page. If browser closes after payment, no email. Also, page refreshes could trigger duplicate sends without careful idempotency tracking.
- **Why not chosen**: Unreliable for a critical business communication. Webhooks are the industry standard for post-payment processing.

### Alternative 2: AWS SES instead of Resend

- **Description**: Use Amazon SES for transactional email
- **Pros**: Very low cost at scale, high deliverability
- **Cons**: More complex setup (IAM credentials, SES sandbox approval, region selection). Overkill for current volume (<100 orders/month). No built-in React email or template system.
- **Why not chosen**: Resend is simpler to set up, has a generous free tier (100/day, 3,000/month), and a cleaner developer API. SES can be considered if volume exceeds Resend's free tier.

### Alternative 3: Stripe Receipts (no custom email)

- **Description**: Enable Stripe's built-in email receipts instead of custom emails
- **Pros**: Zero code — toggle in Stripe Dashboard. Automatic.
- **Cons**: No branding control (generic Stripe template). No shipping address in receipt. No BCC to business. Cannot include delivery information or custom messaging.
- **Why not chosen**: Doesn't meet the business requirement for branded, informative order confirmations. Could be enabled as a backup alongside custom emails.

### Alternative 4: Handle VAT in application code instead of Stripe Tax

- **Description**: Calculate VAT (20%) in the checkout API route and pass tax-inclusive prices to Stripe
- **Pros**: No Stripe Tax setup required
- **Cons**: Tax calculation logic lives in application code — must be maintained. Stripe receipts won't show tax breakdown. Doesn't scale to multiple tax jurisdictions. Stripe Tax handles edge cases (reverse charge, exemptions).
- **Why not chosen**: Stripe Tax is the correct solution — it handles UK VAT correctly, shows tax on the checkout page and receipts, and requires zero application-side tax logic.

## Traceability

- **Idea doc**: `docs/ideas/003-checkout-enhancements.md`
- **Previous plan**: `docs/plans/001-stripe-checkout-integration.md` (Sprint 1 — base checkout)
- **Canonical docs**:
  - `docs/reference/SCHEMA_AND_CONTRACTS_CANONICAL.md` — checkout API contract updates
  - `docs/reference/PLATFORM_OVERVIEW_CANONICAL.md` — Resend integration, new env vars
- **Implementation files**:
  - `src/pages/api/checkout.ts` — modify (add shipping, tax, customer params)
  - `src/pages/checkout/success.astro` — modify (convert to SSR, add session retrieval + order display)
- **New files**:
  - `src/pages/api/webhook.ts` — Stripe webhook handler
  - `src/lib/email.ts` — email template + Resend send function (new directory `src/lib/`)
- **Test files**: None (no test infrastructure)
- **Related audits**: None currently active for this scope

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Resend domain verification fails or delays | Medium | High (no emails) | Verify DNS records in advance. Stripe receipts as temporary fallback. |
| Stripe Tax misconfigured (wrong VAT rate) | Low | High | Test with Stripe test mode. Verify VAT registration in Stripe Dashboard. UK standard rate (20%) is well-supported. |
| Webhook endpoint unreachable (Railway downtime) | Low | Medium | Stripe retries webhook delivery for up to 3 days with exponential backoff. Emails will be delayed but not lost. |
| Duplicate confirmation emails | Low | Medium | Idempotency key (Stripe event ID) passed to Resend. Resend deduplicates on this key. |
| Success page session retrieval fails | Medium | Low | Graceful fallback to generic thank-you. Email (via webhook) still sends regardless. |
| Shipping rate ID changes in Stripe | Low | Medium | Stored as env var (`STRIPE_SHIPPING_RATE_ID`), not hardcoded. Easy to update. |
| Resend free tier exceeded | Low | Low | 100/day, 3,000/month is well above current order volume. Monitor and upgrade plan if needed. |
| `STRIPE_WEBHOOK_SECRET` not set in Railway | Low | High | Webhook returns 500, Stripe retries. Add to deployment checklist. Env var guard in code logs clear error. |
| Webhook signature verification fails due to body parsing | Low | High | Stripe requires the raw request body for signature verification. Astro's `request.text()` should return raw body in standalone mode, but middleware could interfere. Test explicitly during verification. Fallback: use `request.arrayBuffer()` and convert. |
| Stripe Tax errors due to missing product tax codes | Medium | High | `automatic_tax: { enabled: true }` requires either a default tax code on the Stripe account or individual tax codes on each Price/Product. Without this, Stripe returns an error. Add to Stripe Dashboard prerequisites: set default product tax code before deployment. |

## Approval

- **Approver**: Rob DiCapite
- **Date**: 2026-03-13
- **Conditions**: None

## Implementation Record

- **Implemented by**:
- **Date**:
- **Sprint**:
- **Deviations from plan**:
