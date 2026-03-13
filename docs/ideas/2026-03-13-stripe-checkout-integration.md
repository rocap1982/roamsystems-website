---
doc_type: idea
status: accepted
created: 2026-03-13
last_updated: 2026-03-13
owner: "Robert DiCapite"
tags: [payments, stripe, checkout, amaka, sage]
related_plans: []
related_sprints: []
---

# Idea: Stripe Checkout Payment Integration with Amaka Sage Sync

## Summary

Replace the current enquiry-based checkout (FormSubmit.co) with direct Stripe Checkout payments. Use Amaka to auto-sync payments to Sage as invoices. No backend required — Stripe Checkout is client-side redirect only.

## Problem / Opportunity

### Current State
- Customers add items to a localStorage cart, then submit an enquiry via FormSubmit.co
- Business manually contacts customers to arrange payment offline
- No direct payment capability on the site

### Desired State
- Customers can pay directly via Stripe Checkout (card, Apple Pay, Google Pay)
- Payments auto-sync to Sage accounting via Amaka
- Enquiry flow remains available as a fallback for custom orders

### Why This Matters
- Reduces friction in the purchase flow — fewer drop-offs
- Eliminates manual payment chasing
- Automates accounting sync (Sage)

## Constraints

- Static Astro site — no backend/server-side code
- Must use Stripe Checkout (hosted page), not Stripe Elements
- Products must be created in Stripe Dashboard (mirrors products.json)
- Amaka is free (Sage partnership) — no monthly fees

## Architecture / Approach

1. Products created in Stripe Dashboard with Price IDs (9 products, matching variants)
2. Client-side JS constructs a Stripe Checkout session URL with line items
3. Customer redirected to checkout.stripe.com for payment
4. On success → redirect to /checkout/success page
5. On cancel → redirect to /checkout/cancel page
6. Amaka configured externally to sync Stripe payments → Sage invoices

## Non-goals

- Server-side Stripe integration (no webhooks, no backend)
- Removing the enquiry flow entirely (keep for custom/bespoke orders)
- Inventory management
- Customer accounts or order history

## Open Questions

- None — strategy was pre-explored and accepted (see memory: payment_strategy)

## Traceability

- `src/data/products.json` — needs `stripePriceId` field per variant
- `src/layouts/Layout.astro` — cart sidebar checkout button changes
- New pages: `src/pages/checkout/success.astro`, `src/pages/checkout/cancel.astro`
