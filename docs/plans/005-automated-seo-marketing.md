---
doc_type: plan
status: draft
created: 2026-03-15
author: "Claude (AI)"
approver: ""
related_issues: []
---

# Plan: Automated SEO Marketing System

## Problem Statement

### Current State

The site has completed SEO Phases 1-2 (sitemap, robots.txt, OG tags, JSON-LD, meta descriptions) and has a working Stripe Checkout pipeline. However there is zero marketing infrastructure:

- No blog or content pages — zero long-tail keyword targeting
- No vehicle-specific pages — competitors rank for "VW T6 campervan seating"
- No Google Merchant Center feed — invisible in Google Shopping
- No automated content generation — all marketing requires manual effort
- No product-vehicle association — products don't indicate which vans they fit
- Social media posting is sporadic with no content calendar

### Desired State

- Vehicle landing pages for VW T5, T6, T6.1, and Ford Transit Custom (2012+)
- Blog with SEO articles targeting high-value keywords
- Google Merchant Center XML feed auto-generated from product data
- Weekly scheduled content generation (1 blog draft + 3 social posts) emailed for review
- Monthly content calendar refresh
- All products linked to compatible vehicles on product pages

### Why This Matters

- Competitors (Captain Seat, Vangear, Campervan Seating UK) all have vehicle-specific pages, blogs, and richer content
- "VW T6 campervan seat" and "Transit Custom kitchen pod" are high-intent buyer searches where Roam Systems is invisible
- Google Merchant Center is free — products should be listed
- Roam Systems' unique differentiators (only M1 certified U-shape, ISOFIX, EU Registered Design) have no dedicated content

## Proposed Solution

### Canonical Changes Required

| Document | Change Type | Description |
|----------|-------------|-------------|
| `PROJECT_STATUS.md` | Minor | Add blog, vehicles, and marketing pipeline to tech stack and current state |
| `docs/reference/seo-marketing.md` | New | Document content pipeline, feed URL, scheduled task configuration |

### Proposed Specification

#### 1. Vehicle Data Schema (`src/data/vehicles.json`)

```json
[
  {
    "id": "vw-transporter-t5",
    "name": "VW Transporter T5",
    "shortName": "T5",
    "years": "2003-2015",
    "description": "SEO-optimized description of T5 as a campervan conversion base...",
    "image": "/images/vehicles/vw-t5.jpg",
    "compatibleProducts": ["m1-certified-u-shape-seating-frame", "m1-certified-3-4-seating-frame", ...]
  }
]
```

All 9 products are compatible with all 4 vehicles (confirmed by owner).

#### 2. Product Data Enhancement (`src/data/products.json`)

Add two fields to each product:
```json
{
  "compatibleVehicles": ["vw-transporter-t5", "vw-transporter-t6", "vw-transporter-t6-1", "ford-transit-custom"],
  "mpn": "m1-certified-u-shape-seating-frame"
}
```

#### 3. Blog Content Collection Schema (`src/content/config.ts`)

```typescript
import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    publishedDate: z.date(),
    updatedDate: z.date().optional(),
    author: z.string().default('ROAM Systems'),
    category: z.enum(['guides', 'products', 'lifestyle', 'certification', 'news']),
    tags: z.array(z.string()).default([]),
    image: z.string().optional(),
    draft: z.boolean().default(true),
    keywords: z.array(z.string()).default([]),
  }),
});

export const collections = { blog };
```

#### 4. Google Merchant Feed (`/feeds/google-merchant.xml`)

Static XML endpoint reading `products.json`. Per-product fields:
- `g:id`, `g:title`, `g:description`, `g:link`, `g:image_link`
- `g:price` (VAT-inclusive, GBP)
- `g:availability` (`in_stock` or `preorder` based on `madeToOrder`)
- `g:condition` (`new`), `g:brand` (`ROAM Systems`)
- `g:mpn`, `g:product_type`, `g:shipping` (UK, GBP 130.00)
- `g:custom_label_0` (compatible vehicles)

#### 5. Marketing Draft Email API (`POST /api/marketing/send-drafts`)

```typescript
// Request body
{
  blogDraft: { title: string; markdown: string; keywords: string[] };
  socialPosts: Array<{
    day: string;
    caption: string;
    hashtags: string[];
    imageSource: string;
    link: string;
  }>;
}

// Uses existing sendViaResend() from src/lib/email.ts
// Sends formatted HTML to sales@roamsystems.co.uk with tag: marketing-draft
```

#### 6. Scheduled Tasks

| Task | Schedule | Description |
|------|----------|-------------|
| Weekly Content Generation | Monday 9:00 AM | Generate 1 blog draft + 3 social posts, email to owner |
| Monthly Calendar Refresh | 1st of month, 10:00 AM | Propose next month's topics based on keyword gaps |

## Implementation Impact

### Code Changes Required

| File | Change |
|------|--------|
| `src/data/products.json` | Add `compatibleVehicles` and `mpn` fields to all 9 products |
| `src/pages/products/[id].astro` | Add "Compatible Vehicles" section with links to vehicle pages |
| `src/layouts/Layout.astro` | Add "Vehicles" and "Blog" to header nav (desktop + mobile) |
| `src/lib/email.ts` | Add `sendMarketingDrafts()` function reusing `sendViaResend()` |

### New Files

| File | Purpose |
|------|---------|
| `src/data/vehicles.json` | Vehicle compatibility data (4 vehicles) |
| `src/pages/vehicles/index.astro` | Vehicle listing page |
| `src/pages/vehicles/[id].astro` | Per-vehicle page with compatible products |
| `src/content/config.ts` | Blog content collection schema |
| `src/content/blog/*.md` | Blog posts (2 seed posts) |
| `src/pages/blog/index.astro` | Blog listing page |
| `src/pages/blog/[...slug].astro` | Blog post page |
| `src/layouts/BlogPost.astro` | Blog post layout |
| `src/pages/feeds/google-merchant.xml.ts` | Google Merchant Center XML feed |
| `src/data/content-calendar.json` | Planned blog topics + keywords |
| `src/data/social-calendar.json` | Social post themes by day |
| `src/pages/api/marketing/send-drafts.ts` | Draft email delivery endpoint |

### Test Changes

No existing tests to update. Manual verification:
- Blog pages render correctly with content filtering
- Vehicle pages show correct product grids
- Google Merchant XML validates against spec
- Draft email arrives at `sales@roamsystems.co.uk`
- Sitemap includes new blog + vehicle URLs

### Data / Migration Impact

No database or migration required. Changes are additive:
- New fields added to `products.json` (existing fields unchanged)
- New data files created (`vehicles.json`, calendars)
- New content collection created (`src/content/blog/`)

## Migration Plan

No breaking changes. All additions are backwards-compatible:
- Existing pages unaffected
- Existing API routes unchanged
- Existing JSON-LD and OG tags preserved
- New nav links are additive

## Alternatives Considered

### Alternative 1: WordPress Blog (External)

- **Description**: Host blog on separate WordPress instance, link from main site
- **Pros**: Mature blogging platform, SEO plugins, easy content management
- **Cons**: Separate hosting cost, different tech stack, no shared styling, split domain authority
- **Why not chosen**: Keeping everything in Astro maintains domain authority, consistent design, and zero additional hosting cost

### Alternative 2: Fully Automated Posting (No Review)

- **Description**: Claude generates and posts directly to social media and publishes blog posts automatically
- **Pros**: Zero manual effort
- **Cons**: Risk of off-brand content going live, requires Meta API setup, no quality control
- **Why not chosen**: Owner prefers generate + approve model. Manual review ensures brand consistency.

### Alternative 3: Third-Party Content Tools (Buffer, Hootsuite)

- **Description**: Use paid scheduling tools for social media
- **Pros**: Built-in analytics, multi-platform posting, team collaboration
- **Cons**: Monthly cost (£15-50/mo), another tool to learn, doesn't solve blog/SEO content
- **Why not chosen**: Claude scheduled tasks + email achieves the same result at zero cost

## Traceability

- **Idea doc**: `docs/ideas/007-automated-seo-marketing.md`
- **Canonical docs**: `PROJECT_STATUS.md`, `docs/reference/seo-marketing.md` (new)
- **Implementation files**: See "New Files" and "Code Changes Required" tables above
- **Test files**: Manual verification (no test framework in project)
- **Related audits**: None currently active

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Blog content quality varies | Medium | Low | `draft: true` default + email review ensures nothing publishes without approval |
| Google Merchant feed rejected | Low | Medium | Include all required fields; validate XML before submission |
| Scheduled task can't call Railway API | Low | Medium | Task can call Resend API directly via fetch, bypassing Railway endpoint |
| Vehicle pages add minimal SEO value initially | Medium | Low | Pages improve over time as Google indexes them; immediate internal linking benefit |
| Content calendar runs out of topics | Low | Low | Monthly refresh task proposes new topics; 7+ keywords already identified |
| Nav bar gets crowded with Blog + Vehicles | Low | Low | Can use dropdown/sub-menu if needed |

## Approval

- **Approver**:
- **Date**:
- **Conditions**:

## Implementation Record

- **Implemented by**:
- **Date**:
- **Sprint**:
- **Deviations from plan**:
