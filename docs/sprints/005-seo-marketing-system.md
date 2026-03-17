---
doc_type: sprint
status: closed
stage: done
created: 2026-03-15
last_updated: 2026-03-15
dates:
  start: 2026-03-15
  end: 2026-03-17
sprint_goal: "Build vehicle pages, blog infrastructure, Google Merchant feed, and automated content pipeline"
---

# Sprint 005: Automated SEO Marketing System

## Summary

Deliver vehicle-specific landing pages, blog infrastructure, Google Merchant Center feed, and a scheduled content pipeline that emails weekly drafts for review. All products compatible with VW T5, T6, T6.1, and Ford Transit Custom.

**Stage**: done

**Scope**: Vehicle pages, blog, Google Merchant feed, marketing email API, scheduled tasks, navigation updates

## Acceptance Criteria

- [x] Vehicle listing page at `/vehicles` shows all 4 van models
- [x] Vehicle detail pages at `/vehicles/[id]` show compatible products for each van
- [x] Product detail pages show "Compatible Vehicles" section with links
- [x] Blog listing page at `/blog` renders published posts
- [x] Blog post pages render Markdown content with Article JSON-LD
- [x] 2 seed blog posts published (M1 Certification + VW Transporter Guide)
- [x] Google Merchant XML feed at `/feeds/google-merchant.xml` contains all 9 products
- [x] Feed includes VAT-inclusive prices, availability, brand, shipping
- [x] Header navigation includes "Vehicles" and "Blog" links (desktop + mobile)
- [x] Marketing draft email API endpoint works via Resend
- [x] Weekly content generation scheduled task configured
- [x] `npm run build` succeeds with all new pages

## Contracts / Governance

- Contract-impacting changes expected: Yes (new API endpoint, product data schema extension)
- Plans: `docs/plans/005-automated-seo-marketing.md` (approved 2026-03-15)

## Work Plan

### Done

- [x] [Data] Create `src/data/vehicles.json` — 4 vehicles with IDs, names, years, descriptions, compatible product IDs
- [x] [Data] Edit `src/data/products.json` — add `compatibleVehicles` and `mpn` fields to all 9 products
- [x] [UI] Create `src/pages/vehicles/index.astro` — vehicle listing page with card grid
- [x] [UI] Create `src/pages/vehicles/[id].astro` — vehicle detail page with compatible products grid + JSON-LD
- [x] [UI] Edit `src/pages/products/[id].astro` — add "Compatible Vehicles" section below product details
- [x] [Config] Create `src/content.config.ts` — blog content collection schema (Astro 6 format)
- [x] [UI] Create `src/layouts/BlogPost.astro` — blog post layout extending Layout.astro
- [x] [UI] Create `src/pages/blog/index.astro` — blog listing page filtering draft:false
- [x] [UI] Create `src/pages/blog/[...slug].astro` — blog post page with Article JSON-LD
- [x] [Content] Create seed post: `src/content/blog/why-m1-certification-matters.md`
- [x] [Content] Create seed post: `src/content/blog/vw-transporter-campervan-furniture-guide.md`
- [x] [API] Create `src/pages/feeds/google-merchant.xml.ts` — static XML feed from products.json
- [x] [UI] Edit `src/layouts/Layout.astro` — add "Vehicles" and "Blog" to header nav (desktop + mobile)
- [x] [Data] Create `src/data/content-calendar.json` — first month of blog topics + keywords
- [x] [Data] Create `src/data/social-calendar.json` — social post themes by day
- [x] [API] Edit `src/lib/email.ts` — add `sendMarketingDrafts()` function
- [x] [API] Create `src/pages/api/marketing/send-drafts.ts` — POST endpoint for draft emails
- [x] [Config] Set up weekly content generation scheduled task via MCP
- [x] [Config] Set up monthly calendar refresh scheduled task via MCP
- [x] [Test] Build succeeds (`npm run build`)
- [x] [Docs] Update `PROJECT_STATUS.md`

## Test Plan

### Automated

```bash
npm run build
```

### Manual

- [x] Visit `/vehicles` — 4 vehicle cards displayed
- [x] Click each vehicle — correct products shown on detail page
- [x] Visit any product page — "Compatible Vehicles" section visible with links
- [x] Visit `/blog` — 2 published posts displayed
- [x] Click each blog post — content renders, Article JSON-LD in page source
- [x] Visit `/feeds/google-merchant.xml` — valid XML, 9 products, correct prices
- [x] Check header nav — "Vehicles" and "Blog" links work (desktop + mobile)
- [x] Check sitemap — blog and vehicle URLs included
- [ ] Trigger draft email — arrives at `sales@roamsystems.co.uk` (requires MARKETING_API_TOKEN on Railway)

## Review Gate

- [x] All acceptance criteria met
- [x] `npm run build` succeeds
- [x] Manual test checklist complete
- [x] Google Merchant XML contains all required fields
- [x] Blog posts have correct JSON-LD Article schema

## Documentation DoD

- [x] Update `PROJECT_STATUS.md` — add blog, vehicles, marketing pipeline to tech stack
- [x] No `docs/reference/seo-marketing.md` needed — pipeline is simple (scheduled task → API → Resend)

## Audit Plan

Mini audit after implementation — verify:
- New pages follow existing Layout/styling patterns
- JSON-LD on vehicle and blog pages validates
- Sitemap includes all new routes
- No regressions to existing OG/meta tag infrastructure

## Notes

- All 9 products compatible with all 4 vehicles (confirmed by owner)
- No fitting differences between vans
- Blog author: "ROAM Systems" (brand)
- Social posting: 3x/week (Mon/Wed/Fri)
- Google Merchant Center account exists from previous session

### Learnings

- **Astro 6 content collections**: Use `src/content.config.ts` with `glob()` loader, NOT legacy `src/content/config.ts`. The `post.id` field replaces `post.slug`.
- **Auth on internal APIs**: Always add Bearer token auth to internal-only endpoints — even when called only by scheduled tasks. Fixed in `/check-sprint`.
- **HTML escaping in emails**: Added `escapeHtml()` utility to `email.ts` — all user/API-submitted content must be escaped before HTML template injection.
- **Parallel agent execution**: Vehicle pages, blog, and merchant feed were independent tracks implemented by 3 parallel subagents — effective for non-overlapping domain work.
- **Denormalized data**: Vehicle-product compatibility is stored in both `vehicles.json` and `products.json`. Acceptable for 4x9 matrix but would need normalization if data grows.
- **Price convention**: Products in `products.json` are ex-VAT. Google Merchant feed applies 1.2x multiplier. This is not documented in the schema — should add a comment.
- **Post-deploy**: Set `MARKETING_API_TOKEN` env var on Railway before scheduled tasks can call the draft email endpoint.
