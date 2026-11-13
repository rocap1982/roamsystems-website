---
project: roam-systems-website
status: active
last_updated: 2026-11-13

# "Resume context" pointers (keep these current)
sprint_current_status: docs/sprints/CURRENT_STATUS.md
active_work: "No active sprint. 2026-11-13: test-claim wording aligned to the VOSC test summaries and DEPLOYED/LIVE on main (commits d44d84a, 914bf38, f9c5fb6, 55058dc) — product renamed 'M1 Tested U-Shape Seating Frame' (slug/id/mpn unchanged), crash-test and legal-requirement claims removed, terms clause 8 rewritten (test scope + installer responsibilities), 'Approved' -> 'Experienced' installers, /certifications retitled 'Testing & Quality'. Mini-audit RESOLVED 2026-11-13: docs/audits/resolved/2026-11/2026-11-13-m1-claims-terms-clause8-mini.md — both P1s closed on owner confirmation (Full Width has the same rear section as the tested article; rear seat unchanged from V1 to V3). Trade collateral current on main: email template + price list reworded to 'M1 tested', price list repriced (owner-supplied SWB £1,450 / LWB £1,650 Kitchen Pod Package; other rows = products.json) with Romark Engineering Limited footer. A5 flyer out of scope by owner decision. Open: Stripe Product rename (owner); content-pipeline claims rule + old social drafts; website Kitchen Pod Campervan Package is £1,299 single price vs price list £1,450/£1,650 — owner to say which is right. Also on main since 2026-10-06: middleware no longer 301s /api/* on the non-www host (b71544b). Earlier (2026-06-12): SEO/legal audit fully closed 2026-06-12: approved meta trims + certifications scope wording DEPLOYED & VERIFIED LIVE (commit 0ec1a05; all 34 pages <160-char metas, www canonicals, 301s for legacy Shopify URLs). T&Cs overhaul live 2026-06-12 (commit 3b3918d), mini-audit RESOLVED. Open: non-www->www 301 — Cloudflare zone owner IDENTIFIED via Outlook search 2026-06-12: Identity Pixel Design Ltd (spencer@identitypixel.com) kept DNS in their CF account when the domain registration moved to owner's GoDaddy (cust 296089358, Mar 2026). Full DNS inventory captured in docs/reference/DNS_ROAMSYSTEMS_CO_UK.md. Next: either ask Identity Pixel to proxy apex + add 301 rule, or migrate zone to owner's own CF account (registrar access in hand). www canonicals live meanwhile. GSC: domain property covers www; www sitemap-index.xml submitted 2026-06-12 (initial 'Couldn't fetch' is pre-crawl placeholder; sitemap verified serving 200 with www URLs). Also open: optional live Stripe price verification."
latest_session_log: "docs/sessions/2026-06-08.md"
roadmap_next_phase: "Site feature development (Shopify integration, checkout, SEO)"
canonical_architecture_decision: "Hybrid Astro + React islands via @astrojs/react (added 2026-04-10). All interactive homepage sections are React islands; cart/checkout scripts remain in the Astro layout."
active_audits_dir: docs/audits/active/
latest_audit: "docs/audits/resolved/2026-11/2026-11-13-m1-claims-terms-clause8-mini.md (RESOLVED 2026-11-13 — 0 open P0/P1; P2/P3 carried in CURRENT_STATUS). Previous: docs/audits/resolved/2026-06/2026-06-12-terms-acceptance-ip-mini.md (RESOLVED 2026-06-12)"
skills_index: .claude/skills/
canonical_reference_root: docs/reference/
---

This file is the **fastest way to resume work** with minimal context.

## What is this project?

**Roam Systems** — an e-commerce website for Romark Engineering Ltd (Essex, UK) selling premium campervan furniture (U-shape frame with an M1 tested rear travel seat): seating frames, kitchen pods, storage systems, and upholstery.

## Tech stack

- **Framework**: Astro 6 (hybrid mode — `@astrojs/node` adapter for server routes)
- **Styling**: Tailwind CSS v4.2 (Vite plugin)
- **Hosting**: Railway (Node server)
- **Payments**: Stripe Checkout (server-side sessions via `/api/checkout`)
- **Product data**: `src/data/products.json` (9 products, 3 categories, `stripePriceId` + `madeToOrder` + `compatibleVehicles` + `mpn` fields)
- **Vehicle data**: `src/data/vehicles.json` (6 vehicles: VW T5, T6, T6.1, Ford Transit Custom, Renault Trafic, Nissan Primastar)
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
- **Checkout order-detail capture** (small fix, 2026-06-08) — `/api/checkout` now collects phone + a required vehicle dropdown (6 vehicles + "other") and optional year/reg; order-confirmation email includes a Customer Details block. Canonical doc updated. See `docs/audits/resolved/2026-06/2026-06-08-checkout-order-detail-mini.md`.

## Key decisions

- Hybrid site (Astro + `@astrojs/node` adapter) — static pages prerendered, `/api/checkout` is server-rendered
- No Shopify Storefront API integration yet — product data is a local JSON file
- Stripe Checkout for standard products; Resend `/api/contact` for enquiries (replaced FormSubmit.co)
- `stripePriceId` values are live Stripe prices (refreshed 2026-05-11 — price rise to cover materials cost increases; 7 new Prices created with `tax_behavior=exclusive`, old Prices still active for rollback)

Update this file when:
- priorities change,
- the active sprint changes,
- a major decision is made,
- an audit opens/closes meaningful P0/P1 issues,
- canonical references move.
