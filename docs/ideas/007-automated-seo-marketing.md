---
doc_type: idea
status: draft
created: 2026-03-15
last_updated: 2026-03-15
owner: "Robert DiCapite"
tags: [seo, marketing, automation, blog, vehicles, google-merchant, social-media, content-pipeline]
related_plans: ["docs/plans/005-automated-seo-marketing.md"]
related_sprints: []
---

# Idea: Automated SEO Marketing System

## Summary

Build an automated marketing system that proactively pushes Roam Systems products through vehicle-specific landing pages, a blog targeting long-tail keywords, a Google Merchant Center product feed, and a scheduled content pipeline that generates weekly blog and social media drafts for user review before publishing.

## Problem / Opportunity

### Current State

The site has solid SEO technical foundations (Phases 1-2 complete: sitemap, robots.txt, OG tags, JSON-LD, meta descriptions) and a working e-commerce pipeline (Stripe Checkout live, first payment received). However:

| Area | Status | Impact |
|------|--------|--------|
| Blog/content marketing | **None** | Zero long-tail keyword targeting; competitors have active blogs |
| Vehicle-specific pages | **None** | Competitors rank for "VW T6 campervan seating", "Transit Custom kitchen pod" |
| Google Merchant Center | **No feed** | Invisible in Google Shopping and AI shopping experiences |
| Social media content | **Manual only** | No scheduled content; Facebook, Instagram, YouTube all active but inconsistently posted |
| Content automation | **None** | All marketing requires manual effort each time |
| Product-vehicle association | **None** | Products don't indicate which vans they fit — key purchase decision factor |

### Desired State

- Every product linked to compatible vehicles (VW T5, T6, T6.1, Ford Transit Custom 2012+)
- Dedicated vehicle landing pages capturing "campervan furniture for [van model]" searches
- Blog with SEO-optimized articles targeting high-value keywords
- Google Merchant Center feed syncing products automatically
- Weekly automated content generation: 1 blog draft + 3 social media posts emailed for review
- Monthly content calendar refresh proposing upcoming topics

### Why This Matters

1. **Vehicle keywords**: Competitors (Captain Seat, Vangear, Campervan Seating UK) all have vehicle-specific pages. Searches like "VW T6 campervan seat" and "Transit Custom kitchen pod" have high purchase intent but Roam Systems is invisible for these queries.
2. **Content gap**: Zero blog posts means zero long-tail keyword capture. Competitors publish guides, certification explainers, and build showcases that drive organic traffic.
3. **Google Shopping**: Without a Merchant Center feed, products don't appear in Shopping results or AI shopping experiences (ChatGPT Shopping, Google AI Overviews). Free to list.
4. **Social consistency**: Active accounts exist but posting is sporadic. Automated draft generation removes the creative burden while keeping the user in control of what gets published.
5. **Unique differentiators unexploited**: Only M1 certified U-shape seating system, integrated ISOFIX points, EU Registered Community Design — none of these have dedicated content targeting buyers searching for these features.

## Constraints

- **Generate + approve model**: Nothing publishes automatically. Claude generates drafts, user reviews via email, then approves in a Claude session.
- **Budget**: Under £50/mo for any additional tools (current stack is free: Resend, Railway, Google Merchant Center).
- **No paid advertising**: Organic and content marketing only.
- **Product data source**: `src/data/products.json` remains the single source of truth.
- **Existing SEO preserved**: Phases 1-2 infrastructure (OG tags, JSON-LD, sitemap) must remain intact.
- **Astro hybrid mode**: Blog pages prerendered at build time; API routes remain SSR.

## Architecture / Approach

### Pillar 1: Vehicle-Specific Landing Pages

**Data layer**:
- **New**: `src/data/vehicles.json` — vehicle compatibility data:
  ```json
  [
    {
      "id": "vw-transporter-t5",
      "name": "VW Transporter T5",
      "shortName": "T5",
      "years": "2003-2015",
      "description": "The Volkswagen Transporter T5 is one of the most popular bases for campervan conversions...",
      "compatibleProducts": ["m1-u-shape-frame", "m1-3-4-frame", "kitchen-pod-unit", ...]
    },
    {
      "id": "vw-transporter-t6",
      "name": "VW Transporter T6",
      "shortName": "T6",
      "years": "2015-2019",
      "compatibleProducts": [...]
    },
    {
      "id": "vw-transporter-t6-1",
      "name": "VW Transporter T6.1",
      "shortName": "T6.1",
      "years": "2019-present",
      "compatibleProducts": [...]
    },
    {
      "id": "ford-transit-custom",
      "name": "Ford Transit Custom",
      "shortName": "Transit Custom",
      "years": "2012-present",
      "compatibleProducts": [...]
    }
  ]
  ```

**Pages**:
- **New**: `src/pages/vehicles/index.astro` — "Compatible Vehicles" listing page with card for each van model
- **New**: `src/pages/vehicles/[id].astro` — per-vehicle page showing:
  - Van model info (name, years, description)
  - Grid of compatible products (pulled from products.json via compatibleProducts IDs)
  - Vehicle-specific fitting notes
  - JSON-LD `Vehicle` or `Product` schema with vehicle compatibility
  - Meta description targeting "[van model] campervan furniture"

**Product enhancements**:
- **Edit**: `src/data/products.json` — add `compatibleVehicles` array to each product
- **Edit**: `src/pages/products/[id].astro` — add "Compatible Vehicles" section with links to vehicle pages
- **Edit**: `src/layouts/Layout.astro` — add "Vehicles" to header navigation

**Target keywords**:
| Keyword | Page |
|---------|------|
| VW T5 campervan furniture | `/vehicles/vw-transporter-t5` |
| VW T6 campervan seating | `/vehicles/vw-transporter-t6` |
| VW T6.1 kitchen pod | `/vehicles/vw-transporter-t6-1` |
| Transit Custom campervan seat | `/vehicles/ford-transit-custom` |
| campervan seat VW Transporter | `/vehicles/` index |

### Pillar 2: Blog Infrastructure

**Astro content collections**:
- **New**: `src/content/config.ts` — blog collection schema:
  - `title`, `description`, `publishedDate`, `updatedDate`, `author`, `category` (guides/products/lifestyle/certification/news), `tags`, `image`, `draft` (boolean), `keywords`
- **New**: `src/content/blog/` — Markdown blog post directory

**Pages**:
- **New**: `src/pages/blog/index.astro` — listing page (filters `draft: false`, card grid matching product listing style)
- **New**: `src/pages/blog/[...slug].astro` — post page (reuse `[id].astro` pattern for getStaticPaths)
- **New**: `src/layouts/BlogPost.astro` — extends Layout.astro with date, author, category, reading time, related posts, product CTAs

**JSON-LD**: `Article` schema on blog posts (headline, datePublished, dateModified, author, image, publisher)

**Navigation**: Add "Blog" to header nav (desktop + mobile)

**Seed content** (2 posts, `draft: false` to launch with):
1. "Why M1 Certification Matters for Your Campervan" → "M1 certified campervan seat"
2. "VW Transporter Campervan Furniture Guide" → "VW T6 campervan furniture"

### Pillar 3: Google Merchant Center Feed

- **New**: `src/pages/feeds/google-merchant.xml.ts` — static endpoint reading `products.json`
- Prerendered at build time (zero runtime cost)
- Fields per Google spec: `g:id`, `g:title`, `g:description`, `g:link`, `g:image_link`, `g:price` (VAT-inclusive), `g:availability` (in_stock / preorder based on `madeToOrder`), `g:condition` (new), `g:brand` (ROAM Systems), `g:product_type`, `g:shipping`
- **Edit**: `src/data/products.json` — add `mpn` field per product for Merchant compliance
- Vehicle compatibility included via `g:custom_label_0` for Google filtering
- User manually submits feed URL to Google Merchant Center (one-time setup)

### Pillar 4: Automated Content Pipeline

**Content calendar**:
- **New**: `src/data/content-calendar.json` — planned blog topics with keywords, categories, scheduled weeks
- **New**: `src/data/social-calendar.json` — social post themes per day (Mon: product highlight, Wed: education/certification, Fri: lifestyle/community)

**Draft delivery**:
- **Edit**: `src/lib/email.ts` — add `sendMarketingDrafts()` function (reuses existing Resend integration)
- **New**: `src/pages/api/marketing/send-drafts.ts` — POST endpoint that emails draft content via Resend with `marketing-draft` tag

**Scheduled tasks** (via Claude scheduled-tasks MCP):

| Task | Schedule | Action |
|------|----------|--------|
| Weekly Content Generation | Monday 9:00 AM | Reads products.json + content-calendar.json, generates 1 blog draft (~800-1200 words) + 3 social posts, emails to sales@roamsystems.co.uk |
| Monthly Calendar Refresh | 1st of month, 10:00 AM | Reviews published content + keyword gaps, proposes next month's 2 blog topics + 12 social themes |

**Approval workflow**:
1. Monday 9 AM: scheduled task generates + emails drafts
2. User reviews email
3. User starts Claude session: "publish this week's blog post"
4. Claude creates `.md` file with `draft: false`, commits, deploys via Railway
5. User manually posts social content from email (or optionally via Claude in Chrome)

### Pillar 5: Social Media Drafts

**Content types**:
- Product highlights (feature a specific product with benefits and specs)
- Certification education (M1 testing, ISOFIX safety, EU Registered Design)
- Lifestyle/community (van life, conversion showcases, customer stories)
- Vehicle-specific (T5 conversion tips, T6 furniture options, Transit Custom builds)

**Draft format** (per social post in email):
- Platform: Facebook + Instagram (same content works for both)
- Caption text (150-300 words)
- Hashtag suggestions (10-15 relevant tags)
- Image suggestion (which existing product/gallery image to use)
- Link to include (product page, vehicle page, or blog post)

**YouTube**: Not automated (video content). Pipeline generates video description text and tags when user uploads manually.

## Non-goals

- Fully automated posting (user reviews all content before publishing)
- Paid advertising (Google Ads, Facebook Ads, Instagram Ads)
- Email newsletter subscriber list (separate future initiative)
- TikTok, Pinterest, LinkedIn content
- Customer review/testimonial system (separate initiative)
- Page speed / image optimization (separate concern from idea 001)
- llms.txt / GEO optimization (can be added to a future sprint from idea 001)
- Meta Business Suite API integration (manual posting is fine for current volume)

## Open Questions

1. ~~**Product-vehicle compatibility**~~: **RESOLVED** — All 9 products are compatible with all 4 vehicles (VW T5, T6, T6.1, Ford Transit Custom 2012+). Every product gets `compatibleVehicles: ["vw-transporter-t5", "vw-transporter-t6", "vw-transporter-t6-1", "ford-transit-custom"]`.

2. ~~**Vehicle fitting notes**~~: **RESOLVED** — No fitting differences between vans. Same installation for all models. Vehicle pages will focus on product compatibility, not vehicle-specific fitting instructions.

3. ~~**Blog author**~~: **RESOLVED** — Posts attributed to "ROAM Systems" (brand).

4. ~~**Google Merchant Center account**~~: **RESOLVED** — Account exists from a previous session. Will use existing account.

5. ~~**Social posting frequency**~~: **RESOLVED** — 3 posts per week (Monday, Wednesday, Friday).

6. ~~**Content calendar starting topics**~~: **RESOLVED** — Confirmed: 1. "Why M1 Certification Matters" 2. "VW Transporter Campervan Furniture Guide".

## Traceability

### Files to create
- `docs/ideas/007-automated-seo-marketing.md` (this doc)
- `src/data/vehicles.json`
- `src/content/config.ts`
- `src/content/blog/*.md`
- `src/pages/vehicles/index.astro`
- `src/pages/vehicles/[id].astro`
- `src/pages/blog/index.astro`
- `src/pages/blog/[...slug].astro`
- `src/layouts/BlogPost.astro`
- `src/pages/feeds/google-merchant.xml.ts`
- `src/data/content-calendar.json`
- `src/data/social-calendar.json`
- `src/pages/api/marketing/send-drafts.ts`

### Files to modify
- `src/data/products.json` — add `compatibleVehicles`, `mpn`
- `src/pages/products/[id].astro` — add compatible vehicles section
- `src/layouts/Layout.astro` — add Blog + Vehicles nav links
- `src/lib/email.ts` — add `sendMarketingDrafts()`

### Canonical docs potentially impacted
- `docs/reference/` — may need new `seo-marketing.md` reference if this grows
- `PROJECT_STATUS.md` — update active work + tech stack (blog, vehicles)
