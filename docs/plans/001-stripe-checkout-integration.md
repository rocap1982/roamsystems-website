---
doc_type: plan
status: draft
created: 2026-03-13
last_updated: 2026-03-13
revision: 3
author: "AI (Claude)"
approver: ""
related_issues: []
---

# Plan: Stripe Checkout Payment Integration with Amaka Sage Sync

## Revision Notes

**Rev 2 (2026-03-13)**: Rewrote approach after `/check-plan` found that `stripe.redirectToCheckout` was removed by Stripe in Sept 2025. Now uses server-side Checkout Sessions via Astro API route. Also addresses P1 findings: success page session verification, stale cart handling, helper text updates, CSP notes, made-to-order product handling, and VAT/shipping considerations.

**Rev 3 (2026-03-13)**: Fixed P0s from second `/check-plan`: (1) Removed `output: 'hybrid'` from Astro config — Astro 6 defaults to static with per-route SSR opt-in via `prerender = false`. (2) Documented prior Railway Node adapter history (commits `c5efcdc`→`569412a`) and why it will work this time. (3) Fixed variant count (11 not 15). (4) Added variant selector `data-stripe-price-id` propagation. (5) Added env var guard in API route. (6) Added enquiry modal text update. (7) Noted `product.category` array bug to fix during sprint.

## Problem Statement

### Current State
- Customers browse products and add items to a localStorage cart (`src/layouts/Layout.astro` lines 233–327)
- Checkout is enquiry-based: the "Send Enquiry" button opens a FormSubmit.co modal that emails `sales@roamsystems.co.uk` with basket contents
- Business must manually contact customers to arrange payment offline
- No direct payment processing on the site
- Site is fully static (no Astro adapter, no server-side rendering)

### Desired State
- Customers can pay directly via Stripe Checkout (card, Apple Pay, Google Pay)
- The existing localStorage cart feeds line items to a server-side Stripe Checkout Session
- Successful payments redirect to a confirmation page that verifies the session
- Cancelled checkouts redirect to a cancellation page with option to retry
- Payments auto-sync to Sage accounting via Amaka (external configuration)
- Enquiry flow remains as a fallback for custom/bespoke/made-to-order products
- Made-to-order products (upholstery) are clearly marked as enquiry-only

### Why This Matters
- Reduces purchase friction — customers pay immediately instead of waiting for manual follow-up
- Eliminates manual payment chasing by the business
- Automates accounting sync to Sage via Amaka (free, no monthly fees)
- Estimated fees: ~1.5% + 20p per UK card transaction (Stripe pay-as-you-go)

## Proposed Solution

### Canonical Changes Required

| Document | Change Type | Description |
|----------|-------------|-------------|
| `astro.config.mjs` | Major | Add `@astrojs/node` adapter (pages remain static by default; API route opts into SSR via `prerender = false`) |
| `package.json` | Major | Add `stripe` and `@astrojs/node` dependencies |
| `src/data/products.json` | Major | Add `stripePriceId` per variant; add `madeToOrder` flag for enquiry-only products |
| `src/layouts/Layout.astro` | Major | Replace cart footer with Checkout + Enquiry buttons; add `stripePriceId` to cart item type; add checkout handler that POSTs to API route; update enquiry modal text |
| New: `src/pages/api/checkout.ts` | New | Server-side API route that creates Stripe Checkout Session |
| New: `src/pages/checkout/success.astro` | New | Post-payment success page with session verification |
| New: `src/pages/checkout/cancel.astro` | New | Payment cancelled/retry page |

### Proposed Specification

#### 1. Astro Node Adapter for SSR API Routes

Add the `@astrojs/node` adapter. In Astro 6, all pages are statically prerendered by default. Individual routes opt into SSR via `export const prerender = false`. No `output` field needed in config.

**`astro.config.mjs`**:
```javascript
// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import node from '@astrojs/node';

export default defineConfig({
  adapter: node({ mode: 'standalone' }),
  vite: {
    plugins: [tailwindcss()]
  }
});
```

**`package.json`** new dependencies:
```json
{
  "dependencies": {
    "@astrojs/node": "^9.x",
    "stripe": "^17.x"
  }
}
```

**Railway deployment history and why it will work now**:

The project previously attempted a Node adapter (commit `c5efcdc`) which was reverted (commit `569412a`) because the site was fully static and didn't need SSR — the adapter was unnecessary overhead. The solution was to let Railway's Railpack serve static files via Caddy (`RAILPACK_SPA_OUTPUT_DIR`), which was then further simplified to auto-detection (commit `fea64da`).

This time is different: we genuinely need SSR for the `/api/checkout` endpoint. The Node standalone adapter produces a Node HTTP server that Railway runs natively. Railway supports Node.js apps out of the box. The key change is that we now have a real SSR use case (Stripe session creation) rather than just serving static HTML.

**Deployment note**: Railway will detect the Node adapter and switch from static/Caddy to running the Node server. Env vars `STRIPE_SECRET_KEY` must be set in Railway dashboard. Test on a Railway preview environment before merging to main.

#### 2. Product Data Schema Change

Add `stripePriceId` to each variant and `madeToOrder` flag at product level:

```json
{
  "id": "m1-certified-u-shape-seating-frame",
  "name": "M1 Certified U-Shape Seating Frame",
  "price": 1849.00,
  "madeToOrder": false,
  "variants": [
    { "title": "Black / Long Wheel Base", "price": 1849.00, "stripePriceId": "price_XXXXXXXXXXXX" },
    { "title": "Black / Short Wheel Base", "price": 1849.00, "stripePriceId": "price_XXXXXXXXXXXX" }
  ]
}
```

**Made-to-order products** (upholstery kit, cushion boards) get `"madeToOrder": true` and their variants get `"stripePriceId": null`. These products show "Send Enquiry" instead of "Add to Basket" and cannot be checked out via Stripe (they require fabric selection).

**Products with `madeToOrder: false`**: 7 products (frames, kitchens, storage, panels)
**Products with `madeToOrder: true`**: 2 products (full upholstery kit, cushion boards & foam)

The `stripePriceId` values are placeholders until the Stripe account is configured with matching products/prices.

#### 3. Cart Object Enhancement

The cart item structure in localStorage (`roam-cart`) gains a `stripePriceId` field:

```typescript
// Current
{ id, name, price, variant, image, qty }

// New
{ id, name, price, variant, image, qty, stripePriceId }
```

- The `add()` method and all add-to-cart handlers must pass `stripePriceId` from the selected variant
- The variant selector `<option>` elements in `[id].astro` must carry `data-stripe-price-id` attributes so that when a user changes variant, the `stripePriceId` on the add-to-cart button updates alongside the price (mirroring the existing `data-price` pattern)
- Made-to-order items are added with `stripePriceId: null`
- Cart footer logic checks whether ALL items have a `stripePriceId`:
  - **All items have Price IDs** → show "Checkout — Pay Now" as primary, "Or Send Enquiry" as secondary
  - **Any item lacks a Price ID** (made-to-order or stale) → show "Send Enquiry" as primary, explain why checkout isn't available
  - **Stale cart items** (added before this update, no `stripePriceId`) → treated the same as made-to-order: enquiry-only with a note: "Some items in your basket need to be re-added for checkout"

#### 4. Server-Side API Route (`/api/checkout`)

```typescript
// src/pages/api/checkout.ts
export const prerender = false; // SSR only

import type { APIRoute } from 'astro';
import Stripe from 'stripe';

const secretKey = import.meta.env.STRIPE_SECRET_KEY;
if (!secretKey) {
  throw new Error('STRIPE_SECRET_KEY environment variable is not set');
}
const stripe = new Stripe(secretKey);

export const POST: APIRoute = async ({ request }) => {
  const { items } = await request.json();

  // Validate: all items must have stripePriceId and positive quantity
  const valid = items.every((item: any) =>
    item.stripePriceId && typeof item.qty === 'number' && item.qty > 0
  );

  if (!valid || items.length === 0) {
    return new Response(JSON.stringify({ error: 'Invalid cart items' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  try {
    const session = await stripe.checkout.sessions.create({
      mode: 'payment',
      line_items: items.map((item: any) => ({
        price: item.stripePriceId,
        quantity: item.qty,
      })),
      success_url: `${new URL(request.url).origin}/checkout/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${new URL(request.url).origin}/checkout/cancel`,
    });

    return new Response(JSON.stringify({ url: session.url }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });
  } catch (err) {
    console.error('Stripe session creation failed:', err);
    return new Response(JSON.stringify({ error: 'Unable to create checkout session' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
};
```

#### 5. Client-Side Checkout Handler

In `Layout.astro`, the checkout button handler POSTs cart items to the API route:

```javascript
document.getElementById('cart-checkout')?.addEventListener('click', async () => {
  const btn = document.getElementById('cart-checkout');
  btn.disabled = true;
  btn.textContent = 'Processing...';

  try {
    const response = await fetch('/api/checkout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        items: cart.items.map(item => ({
          stripePriceId: item.stripePriceId,
          qty: item.qty
        }))
      })
    });

    const data = await response.json();
    if (data.url) {
      window.location.href = data.url;
    } else {
      throw new Error(data.error || 'Checkout failed');
    }
  } catch (err) {
    alert('Unable to start checkout. Please try again or send an enquiry instead.');
    btn.disabled = false;
    btn.textContent = 'Checkout — Pay Now';
  }
});
```

Note: Stripe.js `<script>` tag is NOT needed for this approach — we redirect to Stripe's hosted checkout page via server-created URL. No client-side Stripe SDK required.

#### 6. Cart Footer UI (Layout.astro)

Replace the current single "Send Enquiry" button with conditional buttons:

```html
<!-- When all items have stripePriceId -->
<button id="cart-checkout" class="w-full bg-roam-orange hover:bg-roam-orange-dark text-white font-heading font-bold py-3 px-6 rounded-lg transition-colors text-lg">
  Checkout — Pay Now
</button>
<button id="cart-send-enquiry" class="w-full border border-gray-300 text-gray-600 hover:border-roam-orange hover:text-roam-orange font-heading font-semibold py-2 px-6 rounded-lg transition-colors text-sm mt-2">
  Or Send Enquiry Instead
</button>
<p class="text-xs text-gray-500 text-center mt-2">Secure payment via Stripe</p>

<!-- When any item lacks stripePriceId (made-to-order or stale) -->
<button id="cart-send-enquiry" class="w-full bg-roam-orange hover:bg-roam-orange-dark text-white font-heading font-bold py-3 px-6 rounded-lg transition-colors text-lg">
  Send Enquiry
</button>
<p class="text-xs text-gray-500 text-center mt-2">
  Your basket contains made-to-order items — we'll contact you to arrange details and payment
</p>
```

The rendering logic is handled in the `updateUI()` method by checking `cart.items.every(item => item.stripePriceId)`.

#### 7. Success Page (`/checkout/success`)

```
URL: /checkout/success?session_id=cs_XXXXXXXXXXXX
```

- Reads `session_id` from URL query params
- Displays confirmation message with Roam Systems branding
- Clears the localStorage cart
- Shows "Thank you for your order" messaging
- Links back to products and home
- Note: We do NOT server-side verify the session (that would require another SSR page). The `session_id` param is informational. Stripe Dashboard is the source of truth for order confirmation. A future enhancement could add a server-side verification step.

#### 8. Cancel Page (`/checkout/cancel`)

- Cart remains intact (not cleared)
- Shows message: "Your payment was cancelled — your basket is still saved"
- "Return to Basket" button (reopens cart sidebar via JS)
- "Continue Shopping" link to `/products`

#### 9. Helper Text Updates

| Location | Current Text | New Text |
|----------|-------------|----------|
| `[id].astro` below Add to Basket button | "We'll contact you to arrange payment and delivery" | "Secure checkout powered by Stripe" (or "Send us an enquiry for this made-to-order item" for `madeToOrder` products) |
| `index.astro` page header | "Add items to your basket and send us an enquiry" | "Add items to your basket and checkout securely" |
| `Layout.astro` enquiry modal intro | "we'll get back to you to arrange payment and delivery" | "we'll get back to you to discuss your requirements and arrange payment" (reflects that enquiry is now for made-to-order/custom items) |

#### 10. Made-to-Order Product Handling

On product detail pages (`[id].astro`):
- If `product.madeToOrder === true`:
  - Button text: "Send Enquiry" (not "Add to Basket")
  - Clicking opens the enquiry modal directly (skip cart)
  - Helper text: "This is a made-to-order item — we'll contact you to discuss fabric options and arrange payment"
- If `product.madeToOrder === false`:
  - Button text: "Add to Basket" (current behaviour)
  - Helper text: "Secure checkout powered by Stripe"

On product listing page (`index.astro`):
- Made-to-order products show "Send Enquiry" button instead of "Add to Basket"
- `data-made-to-order` attribute on button for JS handling

#### 11. Amaka Sage Sync (External)

- Configured entirely outside the codebase in the Amaka dashboard
- Connects Stripe account to Sage account
- Auto-creates Sage invoices from Stripe payments
- No code changes required — this is operational setup

## Implementation Impact

### Code Changes Required

| File | Change Description |
|------|-------------------|
| `astro.config.mjs` | Add `@astrojs/node` adapter (no `output` field needed — Astro 6 defaults to static, SSR routes opt in with `prerender = false`) |
| `package.json` | Add `stripe` and `@astrojs/node` dependencies |
| `src/data/products.json` | Add `stripePriceId` to each variant (9 products, 11 variants); add `madeToOrder` flag per product |
| `src/layouts/Layout.astro` | (1) Conditional cart footer buttons. (2) Add `stripePriceId` to cart item type. (3) Add checkout click handler (POST to /api/checkout). (4) Update `add()` method signature. (5) Update `updateUI()` to conditionally render checkout vs enquiry buttons. (6) Update footer text. |
| `src/pages/products/[id].astro` | (1) Pass `stripePriceId` from selected variant in add-to-cart handler. (2) Add `data-stripe-price-id` to variant selector `<option>` elements. (3) Update variant change handler to propagate `stripePriceId`. (4) Conditional button text/behaviour for made-to-order products. (5) Update helper text. (6) Fix pre-existing bug: `product.category === 'Frames'` should be `product.category.includes('Frames')` since `category` is an array in `products.json`. |
| `src/pages/products/index.astro` | (1) Pass `stripePriceId` from first variant via `data-stripe-price-id` attribute. (2) Conditional button text for made-to-order products. (3) Update page header text. |

### New Files

| File | Purpose |
|------|---------|
| `src/pages/api/checkout.ts` | Server-side API route creating Stripe Checkout Session |
| `src/pages/checkout/success.astro` | Post-payment success confirmation page |
| `src/pages/checkout/cancel.astro` | Payment cancelled / retry page |
| `.env.example` | Template for required env var (`STRIPE_SECRET_KEY`). Note: `STRIPE_PUBLISHABLE_KEY` is not needed — no client-side Stripe SDK is loaded. |

### Test Changes

- No existing test infrastructure in this project
- Manual verification plan:
  1. Set `STRIPE_SECRET_KEY` to Stripe **test mode** secret key
  2. Set `stripePriceId` values in `products.json` to test mode Price IDs
  3. Add items to cart, click Checkout, verify redirect to Stripe
  4. Complete payment with Stripe test card `4242 4242 4242 4242`
  5. Verify redirect to `/checkout/success?session_id=...`
  6. Verify cart is cleared on success page
  7. Test cancel flow: click cancel on Stripe page, verify redirect to `/checkout/cancel`
  8. Verify cart is preserved on cancel page
  9. Test made-to-order product: add upholstery kit, verify enquiry-only flow
  10. Test mixed cart (standard + made-to-order): verify enquiry-only with explanation
  11. Test stale cart items (no `stripePriceId`): verify enquiry fallback with note

### Data / Migration Impact

- `products.json` schema change is additive (new fields `stripePriceId` on variants, `madeToOrder` on products)
- Existing localStorage cart items lack `stripePriceId` — handled gracefully: checkout button is hidden, enquiry shown with message "Some items in your basket need to be re-added for checkout"
- No database migration needed (no DB)
- Deployment changes: Railway must switch from static to Node server (Astro standalone adapter output)

## Migration Plan

### Backward Compatibility
- The enquiry flow (FormSubmit.co) is fully preserved as a secondary option
- Made-to-order products continue with enquiry-only flow
- Cart data structure is extended, not changed — old items degrade gracefully

### Deployment Steps
1. Set Railway env var: `STRIPE_SECRET_KEY`
2. Deploy code changes — Railway auto-detects the Node adapter and runs the standalone server
3. Verify Stripe test mode checkout end-to-end
4. Switch Stripe keys from test to live
5. Configure Amaka dashboard for Stripe → Sage sync

### Rollback
- Remove `@astrojs/node` adapter from config → reverts to static
- Remove `src/pages/api/checkout.ts` → API route disappears
- Cart footer falls back to enquiry-only (no `stripePriceId` on new items since products.json still has them, but the checkout handler is gone)
- Full rollback: revert the git commit

## Alternatives Considered

### Alternative 1: Client-side `redirectToCheckout` (Original Plan v1)
- **Description**: Use Stripe.js `redirectToCheckout()` with Price IDs — no backend
- **Pros**: No server needed, simpler deployment
- **Cons**: **Stripe removed this method in Sept 2025** (API version 2025-09-30). Not functional.
- **Why not chosen**: The API no longer exists

### Alternative 2: Stripe Payment Links / Buy Buttons
- **Description**: Create individual Payment Links in Stripe Dashboard, embed `<stripe-buy-button>` components
- **Pros**: Zero backend code, works on static sites
- **Cons**: Cannot support multi-item cart checkout (one button = one product). Would require abandoning the existing cart UX. No variant selection via Buy Button.
- **Why not chosen**: Breaks the existing multi-item cart experience

### Alternative 3: Opayo/Elavon (formerly Sage Pay)
- **Description**: Native Sage payment gateway with direct accounting integration
- **Pros**: No Amaka needed, direct Sage integration
- **Cons**: Requires backend code, ~£25/month fees, more complex PCI compliance, similar transaction rates
- **Why not chosen**: Higher cost and complexity for equivalent functionality

## Traceability

- **Idea doc**: `docs/ideas/002-stripe-checkout-integration.md`
- **Canonical docs**: No existing canonical docs for payment integration (first implementation)
- **Implementation files**: `astro.config.mjs`, `package.json`, `src/layouts/Layout.astro`, `src/pages/products/[id].astro`, `src/pages/products/index.astro`, `src/data/products.json`
- **New files**: `src/pages/api/checkout.ts`, `src/pages/checkout/success.astro`, `src/pages/checkout/cancel.astro`, `.env.example`
- **Related audits**: None

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Railway deployment config change (static → Node) | Medium | High | Test deployment on a Railway preview environment first. Rollback is simple (remove adapter). |
| `stripePriceId` values entered incorrectly in products.json | Medium | High | Test every product in Stripe test mode before going live. API route validates items before session creation. |
| Stale localStorage cart items (no `stripePriceId`) | High (at launch) | Low | Checkout button hidden for stale carts. Clear messaging to re-add items. Self-resolving as users refresh carts. |
| CSP headers blocking Stripe redirect | Low | High | Verify Railway doesn't set restrictive CSP headers. No Stripe.js loaded client-side, so only redirect domain `checkout.stripe.com` matters. |
| `STRIPE_SECRET_KEY` not set on Railway | Low | High | API route returns 500. Add `.env.example` with required vars. Document in deployment notes. |
| Amaka sync fails or lags | Low | Medium | Monitor Amaka dashboard. Manual Sage entry as fallback. Amaka has auto-retry. |
| Customer completes payment but doesn't reach success page | Low | Medium | Stripe Dashboard shows all payments. Business reconciles from Stripe directly. Future: add webhooks. |
| Made-to-order products accidentally get `stripePriceId` | Low | Medium | Clear `madeToOrder` flag in products.json. Code review checks during sprint. |

## Open Considerations (not blocking approval)

### VAT
- UK B2C sales require VAT-inclusive prices. Current prices in `products.json` are assumed VAT-inclusive.
- Stripe Checkout can display tax via Stripe Tax, but this adds complexity. For v1, prices are passed as-is (VAT-inclusive). Stripe receipts will show the total paid. Amaka/Sage handles the VAT accounting breakdown.
- Future: enable Stripe Tax for automatic VAT calculation and display.

### Shipping
- The Delivery page describes delivery costs (free collection, or delivery quotes). Currently not reflected in cart totals.
- For v1, shipping is NOT included in Stripe Checkout. The checkout total is product-only. Delivery is arranged separately (as it is today).
- Future: add Stripe Shipping Rates to Checkout Sessions for calculated delivery.

## Approval

- **Approver**:
- **Date**:
- **Conditions**:

## Implementation Record

- **Implemented by**:
- **Date**:
- **Sprint**:
- **Deviations from plan**:
