---
doc_type: plan
status: approved
created: 2026-03-15
author: "Claude"
approver: "Robert DiCapite"
related_issues: []
---

# Plan: SEO Phase 2 — Open Graph, Twitter Cards & JSON-LD Structured Data

## Problem Statement

### Current State

Phase 1 SEO (sitemap, robots.txt, canonical URLs, meta descriptions) is deployed and live. However:

- No Open Graph meta tags — links shared on Facebook, LinkedIn, WhatsApp show no image/description preview
- No Twitter Card tags — same issue on Twitter/X
- No JSON-LD structured data — Google cannot display rich snippets (product prices, breadcrumbs, business info in search results)
- The Layout component (`src/layouts/Layout.astro`) only accepts `title` and `description` props — no `image` prop for OG images

### Desired State

- Every page renders Open Graph + Twitter Card meta tags in `<head>`
- Product pages pass product images as OG images; other pages use a default OG image
- JSON-LD `Organization` schema on all pages (brand identity in Google Knowledge Panel)
- JSON-LD `Product` schema on each product detail page (rich snippets with price, availability)
- JSON-LD `BreadcrumbList` on product detail pages (enhanced breadcrumb display in search)
- JSON-LD `LocalBusiness` on the contact page (business info in local search)

### Why This Matters

- **Social sharing**: When someone shares a product link on Facebook/WhatsApp, a rich preview with image and description drives significantly more click-throughs than a plain URL
- **Rich search results**: Product structured data can show price, availability, and review stars directly in Google results — increasing click-through rate
- **Knowledge Panel**: Organization schema helps Google surface the Roam Systems brand in a Knowledge Panel
- **Zero cost**: All code-level changes, no ongoing spend

## Proposed Solution

### Canonical Changes Required

| Document | Change Type | Description |
|----------|-------------|-------------|
| None | N/A | No canonical contracts impacted — this is presentation-layer metadata only |

### Proposed Specification

#### 1. Layout Props Extension

Add `image` prop to `Layout.astro`:

```typescript
interface Props {
  title: string;
  description?: string;
  image?: string;       // OG image URL (absolute)
  type?: string;        // og:type — default "website", product pages pass "product"
}
```

Default OG image: `/images/roam-systems-og.png` (the logo or a hero shot — needs to exist in `public/images/`).

#### 2. Open Graph Tags (in Layout `<head>`)

```html
<meta property="og:title" content={title} />
<meta property="og:description" content={description} />
<meta property="og:url" content={canonicalURL.href} />
<meta property="og:site_name" content="ROAM Systems" />
<meta property="og:type" content={type} />
<meta property="og:image" content={ogImage} />
<meta property="og:locale" content="en_GB" />
```

#### 3. Twitter Card Tags (in Layout `<head>`)

```html
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content={title} />
<meta name="twitter:description" content={description} />
<meta name="twitter:image" content={ogImage} />
```

#### 4. JSON-LD: Organization (all pages, in Layout)

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "ROAM Systems",
  "url": "https://roamsystems.co.uk",
  "logo": "https://roamsystems.co.uk/images/roam-systems-logo.png",
  "sameAs": [
    "https://www.facebook.com/roamsystems",
    "https://www.youtube.com/@roamsystems",
    "https://www.instagram.com/roamsystems_m1ushape"
  ]
}
```

#### 5. JSON-LD: Product (product detail pages)

Derived from `products.json` data:

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{product.name}",
  "description": "{product.description}",
  "image": ["{product.images[0]}", ...],
  "brand": { "@type": "Brand", "name": "ROAM Systems" },
  "manufacturer": { "@type": "Organization", "name": "Romark Engineering Ltd" },
  "offers": {
    "@type": "Offer",
    "price": "{product.price}",
    "priceCurrency": "GBP",
    "availability": "https://schema.org/InStock",
    "url": "https://roamsystems.co.uk/products/{product.id}"
  }
}
```

- Made-to-order products (`madeToOrder: true`): use `availability: "https://schema.org/MadeToOrder"`
- Products with variants: use `AggregateOffer` if variant prices differ, otherwise single `Offer`

#### 6. JSON-LD: BreadcrumbList (product detail pages)

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://roamsystems.co.uk/" },
    { "@type": "ListItem", "position": 2, "name": "All Furniture", "item": "https://roamsystems.co.uk/products" },
    { "@type": "ListItem", "position": 3, "name": "{product.name}" }
  ]
}
```

#### 7. JSON-LD: LocalBusiness (contact page only)

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Romark Engineering Ltd",
  "brand": { "@type": "Brand", "name": "ROAM Systems" },
  "address": {
    "@type": "PostalAddress",
    "addressRegion": "Essex",
    "addressCountry": "GB"
  },
  "email": "sales@roamsystems.co.uk",
  "url": "https://roamsystems.co.uk"
}
```

## Implementation Impact

### Code Changes Required

| File | Change |
|------|--------|
| `src/layouts/Layout.astro` | Add `image` and `type` props; add OG tags, Twitter Card tags, Organization JSON-LD |
| `src/pages/products/[id].astro` | Pass `image` prop to Layout; add Product + BreadcrumbList JSON-LD scripts |
| `src/pages/contact.astro` | Add LocalBusiness JSON-LD script |

### New Files

| File | Purpose |
|------|---------|
| `public/images/roam-systems-og.png` | Default OG image for non-product pages (1200x630px recommended) |

### Test Changes

No automated tests exist. Verification via:
- Google Rich Results Test (paste URL to validate JSON-LD)
- Facebook Sharing Debugger (paste URL to validate OG tags)
- Manual inspection of `<head>` in browser dev tools

### Data / Migration Impact

No breaking changes. No migration required.

## Migration Plan

No breaking changes — additive meta tags and JSON-LD scripts only.

## Alternatives Considered

### Alternative 1: Use a dedicated Astro SEO integration (e.g. astro-seo)

- **Description**: Install `astro-seo` package which provides a `<SEO>` component
- **Pros**: Handles OG/Twitter/JSON-LD with less manual markup
- **Cons**: Adds a dependency for what is ~30 lines of HTML meta tags; less control over exact output
- **Why not chosen**: The manual approach is simple, zero-dependency, and gives full control

## Traceability

- **Idea doc**: `docs/ideas/006-seo-plan.md`
- **Canonical docs**: None impacted
- **Implementation files**: `src/layouts/Layout.astro`, `src/pages/products/[id].astro`, `src/pages/contact.astro`
- **Test files**: N/A (manual verification via Google Rich Results Test)
- **Related audits**: None

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Invalid JSON-LD syntax | Low | Low | Validate with Google Rich Results Test before deploy |
| OG image not rendering on social platforms | Low | Low | Test with Facebook Sharing Debugger |
| Default OG image missing or wrong size | Low | Low | Ensure `public/images/roam-systems-og.png` exists at 1200x630px |

## Approval

- **Approver**: Robert DiCapite
- **Date**: 2026-03-15
- **Conditions**: None

## Implementation Record

- **Implemented by**: Claude
- **Date**: 2026-03-15
- **Sprint**: `docs/sprints/004-seo-phase2-og-jsonld.md`
- **Deviations from plan**: None — all specified items implemented as designed
