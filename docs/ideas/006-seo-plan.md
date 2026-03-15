---
doc_type: idea
status: accepted
created: 2026-03-15
last_updated: 2026-03-15
owner: "Robert DiCapite"
tags: [seo, meta-tags, structured-data, sitemap, content-strategy]
related_plans: []
related_sprints: []
---

# Idea: Roam Systems SEO Plan

## Summary

Implement a comprehensive SEO strategy across three phases: technical foundations (sitemap, robots.txt, canonical URLs, meta descriptions), rich results and social sharing (Open Graph, JSON-LD structured data), and content/keyword optimisation (blog, alt text, internal linking). All changes are code-level with zero ongoing monetary cost.

## Problem / Opportunity

### Current State

The site has **no SEO infrastructure** beyond a single shared meta description in `Layout.astro`. Specifically:

- No `robots.txt` — search engines have no crawl instructions
- No `sitemap.xml` — Google can't efficiently discover all 20+ pages
- No `site` URL in `astro.config.mjs` — required for sitemap and canonical URLs
- No Open Graph or Twitter Card meta tags — links shared on social media show no preview
- No canonical `<link>` tags — risk of duplicate content from query params (e.g. `?category=Frames`)
- No JSON-LD structured data — no rich snippets (product prices, breadcrumbs, business info)
- Every page uses the same default meta description
- Product detail pages don't pass a custom `description` to the Layout
- No Google Search Console connected

### Desired State

- Every page has a unique, keyword-targeted meta description and title
- `sitemap.xml` auto-generated and submitted to Google Search Console
- `robots.txt` properly configured
- Canonical URLs on all pages
- Open Graph + Twitter Card tags for rich social sharing previews
- JSON-LD structured data for Products, BreadcrumbList, Organization, and LocalBusiness
- Google Search Console verified and monitoring search performance
- Blog/content section driving long-tail organic traffic
- Image alt text optimised across the site

### Why This Matters

Roam Systems is fairly unique in the market (only M1 certified U-shape seating frame). Without SEO, the site relies entirely on direct traffic and social media. Proper SEO would capture organic search traffic from people actively searching for campervan furniture, seating frames, kitchen pods, etc. — high-intent buyers who don't yet know Roam Systems exists.

## Constraints

- Zero ongoing monetary cost — no paid tools or ads
- Must not break existing prerendered/hybrid SSR setup
- Product data lives in `src/data/products.json` — structured data must derive from this
- Images hosted on Shopify CDN — alt text improvements are in Astro templates, not CDN
- Site URL: `https://roamsystems.co.uk`

## Architecture / Approach

### Phase 1 — Technical SEO Foundation

**Files changed**: `astro.config.mjs`, `src/layouts/Layout.astro`, `public/robots.txt`, all page files in `src/pages/`

1. **Add `site: 'https://roamsystems.co.uk'`** to `astro.config.mjs`
2. **Install `@astrojs/sitemap`** — auto-generates `sitemap.xml` at build time for all prerendered routes
3. **Create `public/robots.txt`**:
   ```
   User-agent: *
   Allow: /
   Sitemap: https://roamsystems.co.uk/sitemap-index.xml
   ```
4. **Add canonical URL** to Layout `<head>`:
   ```html
   <link rel="canonical" href={`https://roamsystems.co.uk${Astro.url.pathname}`} />
   ```
5. **Page-specific meta descriptions** — each page passes a unique `description` prop to Layout:
   - Home: "Premium M1 certified campervan furniture — seating frames, kitchen pods, storage & upholstery. UK made by Romark Engineering."
   - Products listing: "Browse our range of campervan seating frames, kitchen pods, storage drawers & upholstery kits. M1 certified. Shop online."
   - Product detail pages: auto-generate from `product.description` (first 155 chars)
   - Contact, Gallery, Certifications, Installers, Delivery — each get unique descriptions

### Phase 2 — Social & Rich Results

**Files changed**: `src/layouts/Layout.astro`, `src/pages/products/[id].astro`

6. **Open Graph meta tags** in Layout `<head>`:
   ```html
   <meta property="og:title" content={title} />
   <meta property="og:description" content={description} />
   <meta property="og:url" content={canonicalUrl} />
   <meta property="og:site_name" content="ROAM Systems" />
   <meta property="og:type" content="website" />
   <meta property="og:image" content={ogImage} />
   ```
   - Add `image` prop to Layout for page-specific OG images
   - Product pages pass the first product image as OG image

7. **Twitter Card meta tags** in Layout:
   ```html
   <meta name="twitter:card" content="summary_large_image" />
   ```

8. **JSON-LD structured data**:

   a. **Organization** (all pages, in Layout):
   ```json
   {
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

   b. **Product** (product detail pages):
   ```json
   {
     "@type": "Product",
     "name": "...",
     "description": "...",
     "image": ["..."],
     "brand": { "@type": "Brand", "name": "ROAM Systems" },
     "manufacturer": { "@type": "Organization", "name": "Romark Engineering Ltd" },
     "offers": {
       "@type": "Offer",
       "price": "...",
       "priceCurrency": "GBP",
       "availability": "https://schema.org/InStock",
       "url": "..."
     }
   }
   ```

   c. **BreadcrumbList** (product detail pages — already have visual breadcrumbs, just add the schema)

   d. **LocalBusiness** (contact page):
   ```json
   {
     "@type": "LocalBusiness",
     "name": "Romark Engineering Ltd",
     "brand": "ROAM Systems",
     "address": { "@type": "PostalAddress", "addressRegion": "Essex", "addressCountry": "GB" },
     "email": "sales@roamsystems.co.uk"
   }
   ```

### Phase 3 — Content & Keyword Optimisation

**Files changed**: all page templates, `src/data/products.json` (alt text source), potentially new `src/pages/guides/` directory

9. **Title tag formula**: `{Page Title} — ROAM Systems | Campervan Furniture` (adds keyword context beyond just brand)

10. **H1 audit** — ensure every page has exactly one H1 with a relevant keyword:
    - Home: "Your Van. Your Way." → good (emotional), but consider adding a subtitle with "campervan furniture"
    - Products: "Our Furniture" → "Campervan Furniture & Accessories"
    - Product detail: product name → already good

11. **Image alt text** — product images should be descriptive:
    - Current: `alt={product.name}` (same alt on every image of same product)
    - Improved: `alt={product.name + ' - ' + imageContext}` (e.g. "M1 Certified U-Shape Seating Frame - interior view")

12. **Internal linking** — cross-link related products on product detail pages (e.g. frame → panels → upholstery)

13. **Blog / Guides section** (future sprint):
    - "What is M1 Certification and Why Does It Matter?"
    - "Choosing the Right Campervan Seating Frame"
    - "Kitchen Pod Buying Guide"
    - "Campervan Conversion Storage Solutions"
    - These target long-tail keywords and establish authority

### External Setup (manual, not code)

14. **Google Search Console** — verify domain via DNS TXT record in Cloudflare, submit sitemap
15. **Google Business Profile** — if Romark Engineering has a physical location, claim/create a profile

## Non-goals

- Paid advertising (Google Ads, social ads)
- Paid SEO tools (Ahrefs, SEMrush, Moz)
- Link building / outreach campaigns
- Shopify SEO (product data is local, not from Shopify API)
- International SEO / multi-language support
- Page speed optimisation (separate concern — Astro is already fast)

## Open Questions

- Should the blog use Astro's content collections, or is a simpler approach (plain `.astro` pages) sufficient for the initial few posts?
- Are there specific keyword phrases Robert wants to target (e.g. "campervan rock and roll bed", "M1 certified seating")?
- Does Romark Engineering have a Google Business Profile already?
- What image should be used as the default OG image for non-product pages? (The logo, or a hero shot of the furniture in a van?)
- Should `made-to-order` products show `availability: PreOrder` or `InStock` in schema?

## Traceability

- `src/layouts/Layout.astro` — primary file for meta tags, OG, JSON-LD, canonical
- `astro.config.mjs` — site URL, sitemap integration
- `src/pages/products/[id].astro` — product-specific structured data
- `src/data/products.json` — source of truth for product schema data
- `public/robots.txt` — new file
- `docs/reference/` — may need a new `seo.md` canonical reference if this grows
