---
project: roam-systems-website
status: active
last_updated: 2026-03-13

# "Resume context" pointers (keep these current)
sprint_current_status: docs/sprints/CURRENT_STATUS.md
active_work: "Sprint 1: Stripe Checkout Integration (done)"
latest_session_log: ""
roadmap_next_phase: "Site feature development (Shopify integration, checkout, SEO)"
canonical_architecture_decision: ""
active_audits_dir: docs/audits/active/
skills_index: .claude/skills/
canonical_reference_root: docs/reference/
---

This file is the **fastest way to resume work** with minimal context.

## What is this project?

**Roam Systems** — an e-commerce website for Romark Engineering Ltd (Essex, UK) selling premium M1-certified campervan furniture: seating frames, kitchen pods, storage systems, and upholstery.

## Tech stack

- **Framework**: Astro 6 (hybrid mode — `@astrojs/node` adapter for server routes)
- **Styling**: Tailwind CSS v4.2 (Vite plugin)
- **Hosting**: Railway (Node server)
- **Payments**: Stripe Checkout (server-side sessions via `/api/checkout`)
- **Product data**: `src/data/products.json` (9 products, 3 categories, `stripePriceId` + `madeToOrder` fields)
- **Images**: Shopify CDN (product images) + local `public/images/` (gallery, certs, logo)
- **Enquiries**: FormSubmit.co (basket/contact form submissions — also fallback for made-to-order products)
- **Cart**: Client-side localStorage with sidebar UI

## Current state

- Site is deployed and functional on Railway
- 9 pages: Home, Products (listing + detail), Gallery, Certifications, Contact, Delivery, Stockists, 4 policy pages + checkout success/cancel pages
- FBS governance framework installed (2026-03-12)
- **Stripe Checkout** integrated — server-side sessions, enquiry fallback for made-to-order products (Sprint 1 complete)
- **Last sprint**: Sprint 1 — `docs/sprints/2026-03-sprint-1-stripe-checkout.md` (stage: done)

## Key decisions

- Hybrid site (Astro + `@astrojs/node` adapter) — static pages prerendered, `/api/checkout` is server-rendered
- No Shopify Storefront API integration yet — product data is a local JSON file
- Stripe Checkout for standard products; FormSubmit.co enquiry fallback for made-to-order products
- `stripePriceId` values are placeholders until Stripe account is configured with real products

Update this file when:
- priorities change,
- the active sprint changes,
- a major decision is made,
- an audit opens/closes meaningful P0/P1 issues,
- canonical references move.
