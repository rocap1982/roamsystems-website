---
project: roam-systems-website
status: active
last_updated: 2026-07-02

# "Resume context" pointers (keep these current)
sprint_current_status: docs/sprints/CURRENT_STATUS.md
active_work: "No active sprint. 2026-07-02 (small fix): catalogue aligned to canonical roam_code across Stripe/Sage/website; both Upholstery products wired to Stripe checkout (madeToOrder true->false) — now all 9 products purchasable. Branch feat/roam-code-catalogue-alignment pushed (commit 384725e); NOT yet merged/deployed. Open question: bespoke upholstery fabric choice not captured at checkout. PRIOR: SEO/legal audit fully closed 2026-06-12: approved meta trims + certifications scope wording DEPLOYED & VERIFIED LIVE (commit 0ec1a05; all 34 pages <160-char metas, www canonicals, 301s for legacy Shopify URLs). T&Cs overhaul live 2026-06-12 (commit 3b3918d), mini-audit RESOLVED. Open: non-www->www 301 — Cloudflare zone owner IDENTIFIED via Outlook search 2026-06-12: Identity Pixel Design Ltd (spencer@identitypixel.com) kept DNS in their CF account when the domain registration moved to owner's GoDaddy (cust 296089358, Mar 2026). Full DNS inventory captured in docs/reference/DNS_ROAMSYSTEMS_CO_UK.md. Next: either ask Identity Pixel to proxy apex + add 301 rule, or migrate zone to owner's own CF account (registrar access in hand). www canonicals live meanwhile. GSC: domain property covers www; www sitemap-index.xml submitted 2026-06-12 (initial 'Couldn't fetch' is pre-crawl placeholder; sitemap verified serving 200 with www URLs). Also open: optional live Stripe price verification."
latest_session_log: "docs/sessions/2026-07-02.md"
roadmap_next_phase: "Site feature development (Shopify integration, checkout, SEO)"
canonical_architecture_decision: "Hybrid Astro + React islands via @astrojs/react (added 2026-04-10). All interactive homepage sections are React islands; cart/checkout scripts remain in the Astro layout."
active_audits_dir: docs/audits/active/
latest_audit: "docs/audits/resolved/2026-06/2026-06-12-terms-acceptance-ip-mini.md (RESOLVED 2026-06-12 — Aligned; 0 P0/P1; all 3 P3 fixed same day: sidebar terms small print, product-badge UK design numbers, refund→terms cross-link)"
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
- **Product data**: `src/data/products.json` (9 products, 3 categories, `roam_code` [canonical cross-system code] + `stripePriceId` + `madeToOrder` + `compatibleVehicles` + `mpn` fields). All 9 now purchasable via Stripe checkout (both Upholstery products wired 2026-07-02).
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
