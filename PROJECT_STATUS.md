---
project: roam-systems-website
status: active
last_updated: 2026-03-15

# "Resume context" pointers (keep these current)
sprint_current_status: docs/sprints/CURRENT_STATUS.md
active_work: "Sprint 005 complete — SEO marketing system deployed. No active sprint."
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
- **Product data**: `src/data/products.json` (9 products, 3 categories, `stripePriceId` + `madeToOrder` + `compatibleVehicles` + `mpn` fields)
- **Vehicle data**: `src/data/vehicles.json` (4 vehicles: VW T5, T6, T6.1, Ford Transit Custom)
- **Blog**: Astro Content Collections (`src/content/blog/`), schema in `src/content.config.ts`
- **Google Merchant Feed**: Static XML at `/feeds/google-merchant.xml` (auto-generated from products.json)
- **Images**: Shopify CDN (product images) + local `public/images/` (gallery, certs, logo)
- **Email**: Resend (order confirmations + form submissions + marketing drafts to `sales@roamsystems.co.uk`)
- **Webhooks**: Stripe webhook (`POST /api/webhook`) for post-payment processing
- **Marketing API**: `POST /api/marketing/send-drafts` (Bearer token auth, sends blog + social drafts via Resend)
- **Scheduled tasks**: Weekly content generation (Mon 9AM) + monthly calendar refresh (1st, 10AM)
- **Cart**: Client-side localStorage with sidebar UI

## Current state

- Site is deployed and functional on Railway
- Pages: Home, Products (listing + 9 detail), Vehicles (listing + 4 detail), Blog (listing + posts), Gallery, Certifications, Contact, Delivery, Basket, Installers, 4 policy pages + checkout success/cancel
- FBS governance framework installed (2026-03-12)
- **Stripe Checkout** integrated — server-side sessions, shipping, VAT, SSR success page, webhook, confirmation email (Sprint 2 complete)
- **Forms** migrated from FormSubmit.co to Resend via `/api/contact` server endpoint
- **SEO Marketing System** (Sprint 005) — vehicle pages, blog, Google Merchant feed, content pipeline with scheduled tasks
- **Last closed sprint**: Sprint 005 — `docs/sprints/005-seo-marketing-system.md` (stage: done)

## Key decisions

- Hybrid site (Astro + `@astrojs/node` adapter) — static pages prerendered, `/api/checkout` is server-rendered
- No Shopify Storefront API integration yet — product data is a local JSON file
- Stripe Checkout for standard products; Resend `/api/contact` for enquiries (replaced FormSubmit.co)
- `stripePriceId` values are placeholders until Stripe account is configured with real products

Update this file when:
- priorities change,
- the active sprint changes,
- a major decision is made,
- an audit opens/closes meaningful P0/P1 issues,
- canonical references move.
