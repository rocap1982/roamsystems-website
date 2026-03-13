---
doc_type: idea
status: draft
created: 2026-03-12
last_updated: 2026-03-12
owner: "Robert DiCapite"
tags: [seo, llm-optimization, structured-data, content-strategy, geo, performance]
related_plans: []
related_sprints: []
---

# Idea: SEO & LLM Optimization Overhaul

## Summary

Overhaul the Roam Systems Astro website to be fully SEO-optimized, LLM-discoverable, and performance-tuned. Covers structured data (JSON-LD), meta tags, Open Graph, sitemap/robots.txt, semantic HTML, content strategy, mobile performance fixes, the emerging `llms.txt` standard, and Generative Engine Optimization (GEO) tactics to earn AI citations.

## Problem / Opportunity

### Current State

The Astro site has **solid content and strong product data** but is missing critical SEO infrastructure:

| Area | Status | Notes |
|------|--------|-------|
| Meta descriptions | Partial | Default fallback only; no per-page descriptions |
| Open Graph tags | Missing | No og:title, og:description, og:image |
| Twitter Card tags | Missing | Poor social sharing previews |
| Canonical URLs | Missing | Duplicate content risk |
| Structured data (JSON-LD) | Missing | No Product, Organization, FAQ, BreadcrumbList, or LocalBusiness schema |
| Sitemap.xml | Missing | No `@astrojs/sitemap` integration |
| robots.txt | Missing | No `public/robots.txt` |
| Image optimization | Partial | CDN-served but no srcset/WebP, generic alt text |
| Semantic HTML | Partial | Good heading hierarchy but FAQs use plain divs, no microdata |
| Blog/content marketing | Missing | No long-tail keyword targeting |
| Reviews/testimonials | Missing | No social proof or AggregateRating schema |
| llms.txt | Missing | No AI-readable site summary |
| Mobile performance | Poor | **LCP 6.8s on mobile** (target: <2.5s); desktop is excellent at 1.1s |
| Vehicle-specific pages | Missing | Competitors have per-van-model landing pages |
| Competitor parity | Behind | Captain Seat, Vangear, Campervan Seating UK all have richer schema + content |

### PageSpeed Insights (Lighthouse Lab Data)

| Metric | Mobile | Desktop |
|--------|--------|---------|
| Performance | **76** (needs work) | **98** (excellent) |
| Accessibility | 97 | 97 |
| Best Practices | 92 | 92 |
| SEO | 100 | 100 |
| LCP | **6.8s** (failing) | 1.1s (good) |
| CLS | 0 (good) | 0.002 (good) |
| TBT | 70ms (good) | 40ms (good) |

**Root cause of mobile LCP**: Hero images not served responsively. Full desktop-size images load on throttled mobile connections. ~194 KiB image savings available + 280ms render-blocking resource savings.

### Competitive Landscape

**Top competitors** (ranked for "campervan furniture UK", "M1 certified campervan seat"):

| Competitor | Blog | Reviews | Schema | Vehicle Pages | Content Depth |
|------------|------|---------|--------|---------------|---------------|
| Captain Seat | Active | Trustpilot | Basic | Yes (VW, Merc, LR) | High |
| Vangear UK | No | Testimonials | Comprehensive | Yes (T5/T6, Vito) | Moderate |
| Campervan Seating UK | Guides | 8+ on homepage | Comprehensive | Yes | Moderate |
| **Roam Systems** | **None** | **None** | **Basic only** | **None** | **Low** |

**Key competitor advantages Roam lacks:**
- Vehicle-specific landing pages (capture "campervan seat for VW T6" queries)
- Active blogs explaining M1 testing, installation guides, build showcases
- Customer reviews with Trustpilot integration
- Comprehensive schema markup (AutoPartsStore, BreadcrumbList, etc.)

**Roam's unique differentiators not yet exploited:**
- **Only M1 certified U-shape seating system** (genuinely unique, no competitor matches)
- **Integrated ISOFIX points** (family safety niche)
- **EU Registered Community Design** (4 registered designs, RCD No. 015033319)

### Desired State

- Every page has unique meta description, OG tags, Twitter cards, and canonical URL
- JSON-LD structured data on every page type (Organization, Product, FAQPage, BreadcrumbList, LocalBusiness)
- Auto-generated sitemap.xml and robots.txt via Astro integrations
- `llms.txt` at site root summarizing the business for AI crawlers
- Mobile LCP under 2.5s via responsive images and render-blocking fixes
- Content-rich product descriptions with benefit-oriented, GEO-optimized copy
- FAQ schema markup for existing FAQ content (8 questions on homepage)
- Gallery images with meaningful alt text
- Breadcrumb schema matching existing visual breadcrumbs on product pages
- Foundation for future content marketing (blog/guides, vehicle-specific pages)

### Why This Matters

1. **Search visibility**: Without structured data, the site cannot appear in rich results (product cards, FAQ dropdowns, knowledge panels)
2. **AI citations**: Sites with structured data see **44% more AI search citations** (BrightEdge). FAQ schema + Q&A format content is the most-cited pattern by LLMs
3. **LLM recommendations**: 83% of product discovery now happens through AI-powered channels. Without machine-readable structured data, the site is invisible to ChatGPT Shopping, Perplexity, Google AI Overviews
4. **Social sharing**: Missing OG/Twitter tags mean shared links have no preview image or description
5. **Mobile performance**: 6.8s LCP on mobile = poor Core Web Vitals = ranking penalty. Pages with FCP under 0.4s average 3.2x more AI citations
6. **Competitive gap**: Competitors have blogs, reviews, vehicle-specific pages, and richer schema. Roam is losing rankings for "kitchen pod" searches despite selling kitchen pods

## Constraints

- No runtime code changes to e-commerce functionality (cart, forms still work as-is)
- Must remain a static Astro site (no SSR required for SEO work)
- Product data stays in `src/data/products.json` (structured data generated at build time from this source)
- Images remain on Shopify CDN (product) and local `public/` (gallery/certs)
- No external SEO services or paid tools required

## Architecture / Approach

### Phase 1: Technical SEO Foundation + Performance (Quick Wins)

**1.1 Layout-level meta infrastructure** (`src/layouts/Layout.astro`)
- Add props for: `canonicalUrl`, `ogImage`, `ogType`, `twitterCard`
- Generate Open Graph tags (`og:title`, `og:description`, `og:image`, `og:url`, `og:type`, `og:site_name`)
- Generate Twitter Card tags (`twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`)
- Add `<link rel="canonical" href={canonicalUrl} />`
- Add `theme-color` meta tag
- Add Organization JSON-LD (global, on every page)

**1.2 Sitemap & robots.txt**
- Install `@astrojs/sitemap` and configure in `astro.config.mjs`
- Set `site` property in Astro config (required for sitemap)
- Create `public/robots.txt` with sitemap reference and standard allow rules

**1.3 Per-page meta descriptions**
- Add unique, keyword-rich 150-160 character descriptions to every page's frontmatter/props
- Product detail pages: auto-generate from `product.description` + key specs

**1.4 Mobile performance fix (LCP)**
- Add responsive `srcset` and `sizes` to hero/banner images
- Use Astro `<Image>` component for automatic WebP/AVIF generation and srcset
- Add explicit `width`/`height` to all images (prevents CLS, helps browser allocate space)
- Inline critical CSS / defer non-critical resources (save ~280ms on mobile)
- Reduce unused JavaScript (~162 KiB savings available)
- Trim preconnect hints to critical 2-3 origins only

### Phase 2: Structured Data (JSON-LD)

**2.1 Organization schema** (Layout-level, every page)
- `name`, `url`, `logo`, `sameAs` (Facebook, YouTube), `contactPoint`

**2.2 Product schema** (`src/pages/products/[id].astro`)
- `Product` with `name`, `description`, `image`, `brand`, `sku`, `gtin` (if available)
- `Offer` per variant with `price`, `priceCurrency: "GBP"`, `availability`, `itemCondition`
- `AggregateOffer` if multiple variants
- Include `deliveryLeadTime`, `shippingDetails` where available

**2.3 FAQPage schema** (`src/pages/index.astro`)
- Wrap existing 8 FAQ items in `FAQPage` + `Question`/`Answer` JSON-LD
- Use semantic `<details>/<summary>` HTML alongside

**2.4 BreadcrumbList schema** (`src/pages/products/[id].astro`)
- Match existing visual breadcrumbs (Home > All Furniture > Product Name)

**2.5 LocalBusiness schema** (`src/pages/stockists.astro`)
- One entry per stockist with name, address, URL, region

**2.6 WebSite schema with SearchAction** (homepage)
- Enables sitelinks search box in Google

**2.7 HowTo schema** (homepage "How It Works" section)
- 4-step process is a natural fit for HowTo rich results

### Phase 3: Content & Image Optimization (GEO Tactics)

**3.1 Product description enrichment** (GEO-optimized)
- Expand descriptions from feature lists to **conversational, benefit-oriented copy**
- Front-load the answer: explain who it's for and what problem it solves in the first 2 sentences (44.2% of AI citations come from the first 30% of content)
- Add comparison-ready attributes (materials, compatibility, use cases)
- Include statistics and specific data points (GEO research: stats increase AI visibility by 22%)
- Add `brand: "ROAM Systems"`, `sku`, and `mpn` fields to product data

**3.2 Image optimization**
- Product images: descriptive alt text with product name, variant, and brand
- Gallery images: individual captions/descriptions (requires gallery data restructure)
- Certification images: include cert number and standard in alt text
- Use Astro `<Image>` for automatic format optimization

**3.3 Semantic HTML improvements**
- FAQ section: migrate from `<div>` toggles to `<details>/<summary>` elements
- Product cards: add `<article>` wrapper with semantic structure
- Gallery: add `<figure>/<figcaption>` for context

**3.4 Homepage H1 optimization**
- Current: "Your Van. Your Way." (brand-first, no keywords)
- Proposed: Keep tagline as brand identity, add keyword-rich subtitle/H2
- Example: H1 "Your Van. Your Way." / H2 "Premium M1-Certified Campervan Furniture, Engineered in the UK"

### Phase 4: LLM Optimization (Generative Engine Optimization)

**4.1 `llms.txt` file** (`public/llms.txt`)
- Follows llmstxt.org specification: H1 header, blockquote summary, H2 sections with linked resources
- Contents: business description, product categories with links, key differentiators (M1 cert, UK-made, ISOFIX, EU Registered Design), pricing ranges, contact info
- 844K+ websites have adopted this standard; low cost, high potential

**4.2 Content structure for AI consumption**
- Ensure every page has a clear, descriptive H1 that answers the primary query
- Structure content as Q&A where possible (most-cited format by LLMs)
- Include expert quotes and specific statistics (37% and 22% AI visibility boosts respectively)
- Add "Last updated" timestamps (content updated within 30 days gets 3.2x more AI citations)
- Ensure FAQ answers are comprehensive enough for AI to extract and cite

**4.3 Entity establishment**
- Consistent NAP (Name, Address, Phone) across all pages
- Link to social profiles (sameAs in Organization schema)
- Reference certifications with specific test numbers (ECE R14.09, ECE R145)
- Cite the testing body (VOSC Ltd) as an authoritative source

**4.4 AI shopping readiness**
- Ensure Product schema includes all fields ChatGPT Shopping consumes: price, currency, availability, brand, images, description
- Maintain stable HTML identifiers across pages (AI agents need consistent DOM)
- Minimize aggressive pop-ups/modals that block AI agent navigation
- Consider Google Merchant Center feed (feeds directly into AI shopping experiences)

### Phase 5: Content Strategy (Future — Separate Idea/Sprint)

**5.1 Vehicle-specific landing pages** (high priority)
- Competitors rank for "campervan seat VW T6", "Sprinter kitchen pod" etc.
- Create pages for each compatible van model with model-specific specs, fitting info
- Natural long-tail keyword capture

**5.2 Blog / Content Hub**
- "Why M1 Certification Matters" (competitor Captain Seat already publishes this)
- "Rock and Roll Bed vs U-Shape Seating" (comparison content, GEO gold)
- "DVLA V5 Campervan Seat Change Guide" (informational query, high search volume)
- Installation tutorials, customer build showcases
- Publishing cadence: minimum 2 articles/month for AI authority building

**5.3 Review/testimonial system**
- Trustpilot integration or on-site testimonials
- AggregateRating schema
- Verified purchase reviews are weighted more heavily by AI engines (3x higher citation chance with review platform presence)

**5.4 Unique differentiator content**
- Dedicated landing page: "The Only M1 Certified U-Shape Seating System"
- ISOFIX family safety angle: "Safe Campervan Seating with Child Seat Compatibility"
- EU Registered Design showcase with technical details

### Implementation Strategy

| Phase | Effort | Files Touched | Impact | Priority |
|-------|--------|---------------|--------|----------|
| Phase 1: Technical SEO + Performance | 6-8 hours | Layout.astro, astro.config.mjs, all pages, public/robots.txt | Very High | Sprint 1 |
| Phase 2: Structured Data | 4-6 hours | Layout.astro, [id].astro, index.astro, stockists.astro | Very High | Sprint 1 |
| Phase 3: Content & Image Optimization | 4-6 hours | products.json, gallery.astro, index.astro, all page files | High | Sprint 1-2 |
| Phase 4: LLM Optimization | 3-4 hours | public/llms.txt, index.astro, Layout.astro | High | Sprint 2 |
| Phase 5: Content Strategy | Ongoing | New pages, blog infrastructure | Very High (long-term) | Separate idea |

**Recommended execution**: Phases 1-2 as Sprint 1 (highest ROI, ~12 hours). Phase 3-4 as Sprint 2. Phase 5 as a separate ongoing initiative.

## Target Keywords

Based on competitor analysis and search landscape:

| Keyword | Current Ranking | Priority | Content Needed |
|---------|----------------|----------|----------------|
| "M1 certified campervan seat" | Page 1 | Defend + strengthen | Deeper content, dedicated page |
| "campervan furniture UK" | Not ranking | High | Homepage optimization, content |
| "campervan kitchen pod UK" | Not ranking | High | Dedicated content page |
| "campervan U-shape seating" | Opportunity | Very High | Unique differentiator page |
| "campervan ISOFIX seating" | Opportunity | High | Safety-focused landing page |
| "campervan seat VW T6/T5" | Not ranking | Medium | Vehicle-specific pages |
| "rock and roll bed vs U-shape" | Opportunity | Medium | Comparison blog post |

## Non-goals

- No e-commerce functionality changes (cart, checkout, FormSubmit.co)
- No Shopify Storefront API integration (separate initiative)
- No paid SEO tools or services
- No server-side rendering (remains static Astro)
- No full blog/content hub implementation in initial sprints (flagged as Phase 5)
- No Google Analytics / tracking setup (separate concern)
- No A/B testing infrastructure
- No Google Merchant Center feed setup (noted as future optimization)

## Open Questions

- Should the homepage H1 ("Your Van. Your Way.") be replaced with a keyword-rich heading, or kept as brand identity with keywords in H2 subtitle?
- Should `llms.txt` be auto-generated from product data at build time, or manually curated?
- Are there customer testimonials or reviews available to add for social proof + Review schema?
- Should the gallery images get individual captions/descriptions (significant content effort)?
- Is there a preferred social sharing image (OG default) for pages without product images?
- Are SKU/GTIN/MPN numbers available for products? (needed for rich Product schema)
- Which van models are compatible with each product? (needed for vehicle-specific pages)
- Is Google Merchant Center registration on the roadmap?
- What is the appetite for ongoing content creation (blog posts, guides)?

## Traceability

- `src/layouts/Layout.astro` — meta tags, OG, Twitter, canonical, Organization JSON-LD
- `src/pages/index.astro` — FAQPage schema, HowTo schema, homepage H1 optimization
- `src/pages/products/[id].astro` — Product schema, BreadcrumbList schema
- `src/pages/products/index.astro` — CollectionPage meta
- `src/pages/stockists.astro` — LocalBusiness schema
- `src/data/products.json` — brand/sku fields, description enrichment
- `astro.config.mjs` — sitemap integration, site URL
- `public/robots.txt` — new file
- `public/llms.txt` — new file
