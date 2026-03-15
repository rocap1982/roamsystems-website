---
doc_type: plan
status: approved
created: 2026-03-15
author: AI
approver: ""
related_issues: []
---

# Plan: Basket Bug Fix & Enhancements

## Problem Statement

### Current State

The basket (cart) system lives in `src/layouts/Layout.astro` (lines 239-362) as a global `window.roamCart` object backed by localStorage. Three issues exist:

1. **Bug — Home page missing `stripePriceId`**: The "Add to Basket" buttons on `src/pages/index.astro` (lines 196-205) don't include `data-product-stripe-price-id` in the HTML, and the JS handler (lines 389-395) doesn't pass `stripePriceId` to `cart.add()`. This means items added from the home page lack a Stripe price ID, causing `canCheckout()` to fail and showing a confusing "re-add items" warning instead of the Pay Now button. The products listing page (`src/pages/products/index.astro:91,187`) handles this correctly.

2. **No "Empty Basket" button**: Users must remove items one-by-one. There is no bulk clear action.

3. **No standalone basket page**: The basket only exists as a sidebar overlay (`#cart-sidebar`). Users cannot review their basket on a dedicated page with more space, which is standard e-commerce UX.

### Desired State

1. Items added from the home page include `stripePriceId` — checkout works regardless of where the item was added.
2. An "Empty Basket" button in the sidebar (and on the basket page) lets users clear all items at once.
3. A `/basket` page provides a full-page basket review experience with item management, totals, and checkout/enquiry actions.

### Why This Matters

- The missing `stripePriceId` bug prevents Stripe checkout for users who add products from the home page — the most prominent product display on the site.
- No empty basket button forces tedious one-by-one removal.
- A dedicated basket page is a standard e-commerce pattern that improves purchase confidence, especially on mobile where the sidebar is cramped.

## Proposed Solution

### Canonical Changes Required

| Document | Change Type | Description |
|----------|-------------|-------------|
| `docs/reference/PLATFORM_OVERVIEW_CANONICAL.md` | Minor (additive) | Add `/basket` to the page list |
| `docs/reference/SCHEMA_AND_CONTRACTS_CANONICAL.md` | Patch | No schema change — cart localStorage format unchanged |

### Proposed Specification

#### Fix 1: Home page `stripePriceId` bug

Add the missing data attribute to the button HTML in `src/pages/index.astro`:

```html
<button
  class="add-to-cart-btn ..."
  data-product-id={product.id}
  data-product-name={product.name}
  data-product-price={product.price}
  data-product-image={product.images[0]}
  data-product-variant={product.variants[0].title}
  data-product-stripe-price-id={product.variants[0].stripePriceId || ''}
>
```

And update the JS handler to pass it:

```javascript
(window as any).roamCart.add({
  id: el.dataset.productId,
  name: el.dataset.productName,
  price: parseFloat(el.dataset.productPrice || '0'),
  variant: el.dataset.productVariant,
  image: el.dataset.productImage,
  stripePriceId: el.dataset.productStripePriceId || null
});
```

#### Fix 2: "Empty Basket" button

Add a `clear()` method to the cart object in `src/layouts/Layout.astro`:

```javascript
clear() {
  this.items = [];
  this.save();
},
```

Add an "Empty Basket" button in the sidebar header area (between the title and close button, or below the items list) that calls `window.roamCart.clear()`. Show it only when items exist. Add a confirmation prompt to prevent accidental clearing.

#### Fix 3: Standalone `/basket` page

Create `src/pages/basket.astro` — a full-page basket view that:

- Reads cart from localStorage on load (same `window.roamCart` object from Layout)
- Displays items in a spacious table/card layout with image, name, variant, price, quantity controls, and remove button
- Shows subtotal per line item and basket total (+ VAT)
- Includes "Empty Basket" button
- Includes "Checkout — Pay Now" and/or "Send Enquiry" buttons (same logic as sidebar)
- Links back to products for continued shopping
- Shows empty state with CTA to browse products
- Add a "View Basket" link in the sidebar footer that navigates to `/basket`

The page reuses the existing `window.roamCart` API — no new state management needed.

## Implementation Impact

### Code Changes Required

| File | Change |
|------|--------|
| `src/pages/index.astro` (lines 196-205) | Add `data-product-stripe-price-id` attribute to button HTML |
| `src/pages/index.astro` (lines 389-395) | Add `stripePriceId` to `cart.add()` call |
| `src/layouts/Layout.astro` (line ~258) | Add `clear()` method to cart object |
| `src/layouts/Layout.astro` (lines 83-119) | Add "Empty Basket" button to sidebar UI + "View Basket" link in footer |

### New Files

| File | Purpose |
|------|---------|
| `src/pages/basket.astro` | Standalone basket page with full item management and checkout actions |

### Test Changes

- Manual: verify add-to-cart from home page now enables Stripe checkout
- Manual: verify "Empty Basket" clears all items and updates UI
- Manual: verify `/basket` page displays correct items, totals, and checkout flow
- Manual: verify basket page stays in sync with sidebar (both use same localStorage)

### Data / Migration Impact

No migration needed. The localStorage cart format (`roam-cart` key) is unchanged — same `{id, name, price, variant, image, stripePriceId, qty}` shape. Existing carts in users' browsers will continue to work.

**Note**: Existing cart items that were added from the home page before this fix will still lack `stripePriceId`. The existing "re-add items" hint in the sidebar already handles this gracefully.

## Migration Plan

No breaking changes. All changes are additive or bug fixes.

## Alternatives Considered

### Alternative 1: Full cart refactor with custom events

- **Description**: Rewrite cart as an event-driven system with `CustomEvent` dispatching for add/remove/clear, allowing decoupled UI updates.
- **Pros**: More extensible, cleaner separation of concerns.
- **Cons**: Over-engineered for the current 9-product catalogue. The synchronous `save()` → `updateUI()` pattern works fine.
- **Why not chosen**: Current architecture is simple and adequate. Refactor when complexity demands it.

### Alternative 2: Basket page as modal instead of new page

- **Description**: Expand the sidebar into a full-screen modal overlay instead of a new route.
- **Pros**: No new page/route to maintain, keeps everything in Layout.
- **Cons**: Not a real URL (can't share/bookmark), worse for SEO, harder to make responsive.
- **Why not chosen**: A real `/basket` page is standard e-commerce UX and gives users a URL they can return to.

## Traceability

- **Idea doc**: N/A (originated from user-reported bug + enhancement request)
- **Canonical docs**: `docs/reference/PLATFORM_OVERVIEW_CANONICAL.md` (page list update)
- **Implementation files**: `src/layouts/Layout.astro`, `src/pages/index.astro`, `src/pages/basket.astro` (new)
- **Test files**: Manual testing (no automated test suite currently)
- **Related audits**: None active

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| "Empty Basket" clicked accidentally | Medium | Low | Add confirmation dialog before clearing |
| Basket page and sidebar show different data | Low | Medium | Both read from same `window.roamCart` object + localStorage; no separate state |
| Stale cart items (pre-fix) confuse users on basket page | Low | Low | Existing "re-add items" hint already handles this case |

## Approval

- **Approver**: Robert Di Capite
- **Date**: 2026-03-15
- **Conditions**: None

## Implementation Record

- **Implemented by**:
- **Date**:
- **Sprint**:
- **Deviations from plan**:
