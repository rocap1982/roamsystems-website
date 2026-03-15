---
doc_type: sprint
status: active
stage: done
created: 2026-03-15
last_updated: 2026-03-15
dates:
  start: 2026-03-15
  end: 2026-03-15
sprint_goal: "Add Open Graph tags, Twitter Cards, and JSON-LD structured data to all pages for rich social previews and Google rich snippets"
---

# Sprint 004: SEO Phase 2 — OG Tags, Twitter Cards & JSON-LD

## Summary

Add Open Graph meta tags, Twitter Card tags, and JSON-LD structured data (Organization, Product, BreadcrumbList, LocalBusiness) so that shared links show rich previews on social media and Google can display rich snippets in search results.

**Stage**: done

**Scope**: `src/layouts/Layout.astro`, `src/pages/products/[id].astro`, `src/pages/contact.astro`, `public/images/` (OG image asset)

## Acceptance Criteria

- [x] Every page renders `og:title`, `og:description`, `og:url`, `og:site_name`, `og:type`, `og:image` meta tags
- [x] Every page renders `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image` meta tags
- [x] Product detail pages pass the first product image as the OG image
- [x] Non-product pages use a default OG image (`/images/roam-systems-og.png`)
- [x] All pages include Organization JSON-LD in a `<script type="application/ld+json">` tag
- [x] Product detail pages include Product JSON-LD with correct price, currency, and availability
- [x] Made-to-order products use `schema.org/MadeToOrder` availability
- [x] Product detail pages include BreadcrumbList JSON-LD matching the visual breadcrumb
- [x] Contact page includes LocalBusiness JSON-LD
- [x] `npm run build` succeeds with no errors
- [x] JSON-LD validates via built HTML inspection (Google Rich Results Test deferred to post-deploy)

## Contracts / Governance

- Contract-impacting changes expected: **No** (additive presentation-layer metadata only)
- Plans: `docs/plans/004-seo-phase2-social-rich-results.md` (approved 2026-03-15)

## Work Plan

### Phase 1: Asset Preparation
| Task | Domain | Priority | Estimate |
|------|--------|----------|----------|
| Create/source default OG image (1200x630px) at `public/images/roam-systems-og.png` | [UI] | P0 | 5 min |

### Phase 2: Layout Changes (OG + Twitter + Organization JSON-LD)
| Task | Domain | Priority | Estimate |
|------|--------|----------|----------|
| Add `image` and `type` props to Layout.astro Props interface | [UI] | P0 | 5 min |
| Add Open Graph meta tags to Layout `<head>` | [UI] | P0 | 10 min |
| Add Twitter Card meta tags to Layout `<head>` | [UI] | P0 | 5 min |
| Add Organization JSON-LD `<script>` to Layout `<head>` | [UI] | P0 | 5 min |

### Phase 3: Product Page (Product + Breadcrumb JSON-LD)
| Task | Domain | Priority | Estimate |
|------|--------|----------|----------|
| Pass `image` and `type="product"` props from `[id].astro` to Layout | [UI] | P0 | 5 min |
| Add Product JSON-LD script to `[id].astro` (derive from product data) | [UI] | P0 | 15 min |
| Add BreadcrumbList JSON-LD script to `[id].astro` | [UI] | P1 | 5 min |

### Phase 4: Contact Page (LocalBusiness JSON-LD)
| Task | Domain | Priority | Estimate |
|------|--------|----------|----------|
| Add LocalBusiness JSON-LD script to `contact.astro` | [UI] | P1 | 5 min |

### Phase 5: Verification
| Task | Domain | Priority | Estimate |
|------|--------|----------|----------|
| Run `npm run build` — confirm no errors | [Test] | P0 | 2 min |
| Inspect `<head>` output in dev server for OG/Twitter/JSON-LD tags | [Test] | P0 | 5 min |
| Validate JSON-LD with Google Rich Results Test (post-deploy) | [Test] | P1 | 10 min |

### To Do

(none)

### In Progress

(none)

### Done

- [x] Create default OG image at `public/images/roam-systems-og.png` (copied from logo)
- [x] Add `image` and `type` props to Layout.astro Props interface
- [x] Add Open Graph meta tags to Layout `<head>`
- [x] Add Twitter Card meta tags to Layout `<head>`
- [x] Add Organization JSON-LD `<script>` to Layout `<head>`
- [x] Pass `image` and `type="product"` props from `[id].astro` to Layout
- [x] Add Product JSON-LD script to `[id].astro` (with AggregateOffer for multi-price variants)
- [x] Add BreadcrumbList JSON-LD script to `[id].astro`
- [x] Add LocalBusiness JSON-LD script to `contact.astro`
- [x] `npm run build` — succeeded, all 22 pages prerendered

## Test Plan

### Automated

```bash
npm run build
```

Build must succeed. No automated test suite exists beyond the build check.

### Manual

- [x] Open home page in dev tools → verify OG tags present in `<head>` with default image
- [x] Open a product page → verify OG tags use product image, `og:type` is "product"
- [x] Open contact page → verify LocalBusiness JSON-LD in page source
- [x] View source on product page → verify Product JSON-LD has correct price/name/availability
- [x] View source on product page → verify BreadcrumbList JSON-LD has 3 items
- [x] Check a made-to-order product (upholstery) → verify availability is "MadeToOrder"
- [x] After deploy: paste a product URL into Google Rich Results Test → confirm valid (2 valid items: Product snippets + Breadcrumbs, 2 non-critical optional warnings: missing review/aggregateRating)
- [x] After deploy: paste home page URL into Facebook Sharing Debugger → confirm preview renders (all OG + Twitter Card tags detected, product image renders correctly)

## Review Gate

- [x] All acceptance criteria met
- [x] `npm run build` passes
- [x] Manual test checklist complete (8/8)
- [x] JSON-LD validated via Google Rich Results Test (post-deploy)

## Documentation DoD

- [x] No canonical docs impacted (presentation-layer only)
- [x] Update `PROJECT_STATUS.md` after sprint completion
- [x] Update `CURRENT_STATUS.md` after sprint completion

## Audit Plan

None needed — no canonical surfaces (schema, API, DB, business rules) are touched. This sprint adds additive HTML meta tags and JSON-LD scripts only.

## Notes

- Phase 1 SEO (sitemap, robots.txt, canonical URLs, meta descriptions) was deployed as a small fix prior to this sprint
- Default OG image: can use the existing logo or a hero product shot — using logo for now, can be swapped later
- Idea doc: `docs/ideas/006-seo-plan.md`

### Learnings

- Astro's `set:html` directive on `<script>` tags works well for injecting JSON-LD — avoids double-encoding issues
- AggregateOffer vs Offer: only use AggregateOffer when variant prices actually differ (M1 frame: £1850/£1995), not when all variants share the same price (overhead locker: £399/£399)
- Product JSON-LD scripts placed inside `<Layout>` slot render inside `<main>` in built output, not in `<head>` — this is valid per schema.org spec but worth noting
- The OG image for non-product pages is a copy of the logo — not ideal dimensions (1200x630px recommended). Should be replaced with a proper hero shot when available
- No new skill needed — SEO meta tag patterns are standard and well-documented in the plan/sprint docs
