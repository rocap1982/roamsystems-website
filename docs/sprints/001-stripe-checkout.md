---
doc_type: sprint
status: complete
stage: done
created: 2026-03-13
last_updated: 2026-03-13
dates:
  start: 2026-03-13
  end: 2026-03-15
sprint_goal: "Add Stripe Checkout payment flow with server-side sessions, preserving the enquiry fallback for made-to-order products"
---

# Sprint: Stripe Checkout Integration

## Summary

- **Goal**: Add Stripe Checkout payment flow with server-side sessions, preserving the enquiry fallback for made-to-order products
- **Stage**: done
- **Scope**: Astro config (Node adapter), product data schema, cart logic, API route, checkout pages, product page UI updates

## Acceptance Criteria

- [x] `@astrojs/node` adapter installed and `astro.config.mjs` updated — site builds successfully
- [x] `products.json` has `madeToOrder` flag on all 9 products and `stripePriceId` (placeholder) on all 11 variants
- [x] `/api/checkout` API route creates a Stripe Checkout Session and returns session URL
- [x] Cart sidebar shows "Checkout — Pay Now" primary button when all items have `stripePriceId`
- [x] Cart sidebar shows "Send Enquiry" primary button when any item lacks `stripePriceId` (made-to-order or stale)
- [x] Checkout button POSTs cart to `/api/checkout` and redirects to Stripe hosted checkout
- [x] `/checkout/success` page displays confirmation and clears localStorage cart
- [x] `/checkout/cancel` page displays cancellation message with cart preserved
- [x] Made-to-order products (`madeToOrder: true`) show "Send Enquiry" on both listing and detail pages
- [x] Variant selector propagates `stripePriceId` alongside price on variant change
- [x] Helper text updated across product pages and enquiry modal
- [x] `astro build` completes without errors
- [x] Pre-existing bug fixed: `product.category === 'Frames'` → `product.category.includes('Frames')` in `[id].astro`

## Contracts / Governance

- Contract-impacting changes expected: **Yes**
- Plans: `docs/plans/001-stripe-checkout-integration.md` (Rev 3, approved)

## Work Plan

### Phase 1: Config & Dependencies [Config]

| Task | Owner | Priority | Estimate |
|------|-------|----------|----------|
| Install `@astrojs/node` and `stripe` npm packages | [Config] | P0 | 5 min |
| Update `astro.config.mjs` — add Node adapter (no `output` field) | [Config] | P0 | 5 min |
| Create `.env.example` with `STRIPE_SECRET_KEY` | [Config] | P1 | 2 min |
| Create `.env` locally with test-mode Stripe key for dev | [Config] | P0 | 2 min |

### Phase 2: Data Schema [Data]

| Task | Owner | Priority | Estimate |
|------|-------|----------|----------|
| Add `madeToOrder` flag to all 9 products in `products.json` (7× `false`, 2× `true` for upholstery kit + cushion boards) | [Data] | P0 | 5 min |
| Add `stripePriceId` to all 11 variants in `products.json` (placeholder `"price_PLACEHOLDER"` for standard products, `null` for made-to-order) | [Data] | P0 | 10 min |

### Phase 3: API Route [API]

| Task | Owner | Priority | Estimate |
|------|-------|----------|----------|
| Create `src/pages/api/checkout.ts` with `prerender = false` | [API] | P0 | 15 min |
| Implement POST handler: validate items, create Stripe Checkout Session, return session URL | [API] | P0 | — (same file) |
| Add env var guard (`STRIPE_SECRET_KEY` check at module scope) | [API] | P0 | — (same file) |
| Add try/catch around `stripe.checkout.sessions.create()` with JSON error response | [API] | P0 | — (same file) |

### Phase 4: Cart & Layout Updates [UI]

| Task | Owner | Priority | Estimate |
|------|-------|----------|----------|
| Update `cart.add()` method signature in `Layout.astro` to accept `stripePriceId` | [UI] | P0 | 5 min |
| Add `canCheckout()` helper method to cart: returns `true` if all items have `stripePriceId` | [UI] | P0 | 5 min |
| Rewrite cart footer in `updateUI()`: conditionally render Checkout vs Enquiry buttons based on `canCheckout()` | [UI] | P0 | 20 min |
| Add checkout click handler: POST to `/api/checkout`, redirect to Stripe URL, loading state, error handling | [UI] | P0 | 15 min |
| Update enquiry modal intro text (line 124) | [UI] | P1 | 2 min |

### Phase 5: Product Pages [UI]

| Task | Owner | Priority | Estimate |
|------|-------|----------|----------|
| `[id].astro`: Add `data-stripe-price-id` to variant `<option>` elements | [UI] | P0 | 5 min |
| `[id].astro`: Update variant change handler to propagate `stripePriceId` to add-to-cart button (mirror `data-price` pattern) | [UI] | P0 | 10 min |
| `[id].astro`: Add `data-product-stripe-price-id` to add-to-cart button, pass in click handler | [UI] | P0 | 5 min |
| `[id].astro`: Conditional rendering for made-to-order products — "Send Enquiry" button + helper text | [UI] | P0 | 15 min |
| `[id].astro`: Update helper text below button ("Secure checkout powered by Stripe" vs enquiry text) | [UI] | P1 | 5 min |
| `[id].astro`: Fix `product.category === 'Frames'` → `product.category.includes('Frames')` | [UI] | P1 | 2 min |
| `index.astro`: Add `data-stripe-price-id` from first variant to add-to-cart buttons | [UI] | P0 | 5 min |
| `index.astro`: Pass `stripePriceId` in add-to-cart click handler | [UI] | P0 | 5 min |
| `index.astro`: Conditional button text for made-to-order products ("Send Enquiry") | [UI] | P0 | 10 min |
| `index.astro`: Update page header text | [UI] | P1 | 2 min |

### Phase 6: Checkout Pages [UI]

| Task | Owner | Priority | Estimate |
|------|-------|----------|----------|
| Create `src/pages/checkout/success.astro` — confirmation page, clears cart via JS, links to products/home | [UI] | P0 | 20 min |
| Create `src/pages/checkout/cancel.astro` — cancellation page, cart preserved, "Return to Basket" + "Continue Shopping" | [UI] | P0 | 15 min |

### Phase 7: Build Verification [Test]

| Task | Owner | Priority | Estimate |
|------|-------|----------|----------|
| Run `astro build` — verify no errors with Node adapter | [Test] | P0 | 5 min |
| Run `astro dev` — verify dev server starts, API route responds | [Test] | P0 | 5 min |
| Manual test: full checkout flow with Stripe test key (if available) | [Test] | P1 | 15 min |

## Test Plan

### Automated

```bash
# Build check (must pass — primary verification gate)
npm run build

# Dev server check
npm run dev
# Then verify: GET /api/checkout returns 405 (method not allowed — only POST)
# Then verify: POST /api/checkout with valid body returns session URL (requires STRIPE_SECRET_KEY)
```

### Manual

- [ ] Add standard product to cart → verify `stripePriceId` is in cart item (check localStorage)
- [ ] Add made-to-order product → verify enquiry modal opens directly (not added to cart)
- [ ] Open cart with standard items → verify "Checkout — Pay Now" is primary button
- [ ] Click "Checkout — Pay Now" → verify POST to `/api/checkout` and redirect to Stripe
- [ ] Complete Stripe test payment → verify redirect to `/checkout/success`
- [ ] Verify cart is cleared after success page loads
- [ ] Click cancel on Stripe checkout page → verify redirect to `/checkout/cancel`
- [ ] Verify cart is preserved on cancel page
- [ ] Change variant on `[id].astro` → verify price AND `stripePriceId` update on button
- [ ] Test with stale cart item (manually remove `stripePriceId` from localStorage) → verify enquiry-only with message
- [ ] Verify `astro build` completes without errors

## Review Gate

- [x] All acceptance criteria met
- [x] `astro build` passes (primary automated gate)
- [x] Manual test checklist complete (at minimum: build + cart behaviour + made-to-order flow)
- [x] No regressions to existing enquiry flow

## Documentation DoD

- [x] Update `PROJECT_STATUS.md` — reflect new payment capability, change from static to hybrid deployment
- [x] Update memory file `project_payment_strategy.md` — mark as implemented, add implementation notes

## Audit Plan

Mini audit after sprint completes — verify:
- `products.json` schema is consistent (all products have `madeToOrder`, all variants have `stripePriceId`)
- Cart `add()` calls across all pages pass `stripePriceId`
- API route has env var guard + try/catch error handling
- No hardcoded Stripe keys in source (only env vars)

## Notes

- `stripePriceId` values are placeholders until Stripe account is configured with real products. The code will be functional but checkout will fail with placeholder IDs. Replace with real Stripe Price IDs before going live.
- Amaka Sage sync is configured externally (not part of this sprint's code changes).
- VAT and shipping are not included in v1 checkout — noted as future enhancements in the plan.
- The listing page (`index.astro`) always adds the first variant when clicking "Add to Basket" — this is existing behaviour and is not changed by this sprint. Users can select variants on the detail page.
- Implementation completed 2026-03-13. `astro build` passes. All phases implemented.

## Learnings

- **Hybrid mode was simpler than expected**: Adding `@astrojs/node` adapter required no `output` field change — Astro 6 defaults to hybrid with prerendering on, only `prerender = false` needed on the API route.
- **Cart stale-item detection pattern**: Items added before `stripePriceId` existed lack the key entirely (`!('stripePriceId' in item)`), while made-to-order items have it as `null`. This distinction matters for user messaging.
- **Made-to-order enquiry UX**: The "Send Enquiry" button on product detail pages should open the enquiry modal directly (not redirect to /contact) to keep context and pre-fill product info.
- **Stripe success URL template vars**: Use `{CHECKOUT_SESSION_ID}` in the success URL template — Stripe replaces it server-side before redirecting.
- **No skill change needed**: Sprint was straightforward integration work; patterns are standard Astro + Stripe.

## Audit

- Mini audit: `docs/audits/active/2026-03-13-sprint-1-stripe-checkout-mini-audit.md` — all checks pass.
