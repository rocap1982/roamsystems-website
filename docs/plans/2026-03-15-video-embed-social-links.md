---
doc_type: plan
status: implemented
created: 2026-03-15
author: AI
approver: "Robert Di Capite"
related_issues: []
---

# Plan: YouTube Video Embed + Instagram Social Links

## Problem Statement

### Current State

- The home page (`src/pages/index.astro`) has no video content — it's all static text, images, and product cards.
- The site footer (`src/layouts/Layout.astro`, lines ~219-226) has social links for **Facebook** and **YouTube** only.
- The contact page (`src/pages/contact.astro`, lines ~96-101) also has Facebook and YouTube — no Instagram.
- There is no Instagram presence anywhere on the site despite Roam Systems having an active Instagram account (`roamsystems_m1ushape`).

### Desired State

1. **YouTube video embedded on the home page** — directly below the hero section, featuring the main product/brand video with a "Subscribe to our channel" CTA linking to `@roamsystems`.
2. **Instagram link added** to the footer and contact page alongside the existing Facebook and YouTube icons.
3. **Future-ready**: architecture notes for later adding video support to the gallery page.

### Why This Matters

- Video dramatically increases engagement and time-on-page — critical for a premium product where customers want to see quality before buying.
- Instagram is a key channel for the campervan/vanlife community; missing it from the site means lost followers and social proof.
- Consistent social media presence across all touchpoints builds brand trust.

## Proposed Solution

### Canonical Changes Required

No canonical contract changes (no schema, API, DB, or business rule modifications). This is a UI/content addition only.

| Document | Change Type | Description |
|----------|-------------|-------------|
| N/A | N/A | No canonical contracts affected |

### Proposed Specification

#### 1. Home Page Video Section (below hero)

A new section inserted between the hero and the stats banner in `src/pages/index.astro`:

- **Layout**: Centred container, max-width constrained (`max-w-4xl`), with section heading
- **Video embed**: Responsive YouTube iframe (`https://www.youtube-nocookie.com/embed/n5DPLh2mOmY`) with `loading="lazy"` and 16:9 aspect ratio (uses privacy-enhanced `youtube-nocookie.com` domain to avoid third-party cookies for GDPR compliance)
- **CTA below video**: "Subscribe to our channel" text with link to `https://www.youtube.com/@roamsystems`
- **Styling**: Dark background section (`bg-roam-dark`) to match site theme, with padding consistent with other sections

Example structure:
```html
<section class="py-16 bg-roam-dark">
  <div class="max-w-4xl mx-auto px-4 text-center">
    <h2 class="text-3xl font-bold text-white mb-8">See ROAM Systems in Action</h2>
    <div class="relative w-full aspect-video rounded-lg overflow-hidden shadow-xl">
      <iframe
        src="https://www.youtube-nocookie.com/embed/n5DPLh2mOmY"
        title="Roam Systems Video"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
        loading="lazy"
        class="absolute inset-0 w-full h-full"
      ></iframe>
    </div>
    <p class="mt-6 text-gray-300">
      Subscribe to our channel
      <a href="https://www.youtube.com/@roamsystems" target="_blank" rel="noopener noreferrer"
         class="text-roam-orange hover:underline ml-1">
        @roamsystems
      </a>
    </p>
  </div>
</section>
```

#### 2. Instagram Social Link — Footer

Add an Instagram SVG icon link to the footer social links section in `src/layouts/Layout.astro` (alongside existing Facebook and YouTube icons):

- **URL**: `https://www.instagram.com/roamsystems_m1ushape`
- **Icon**: Standard Instagram SVG (outline style, matching existing icon treatment)
- **Styling**: Same `hover:text-roam-orange` pattern as existing social icons

#### 3. Instagram Social Link — Contact Page

Add the same Instagram icon/link to the "Follow Us" section in `src/pages/contact.astro` (alongside existing Facebook and YouTube).

- **Styling**: Same circular button style (`bg-roam-light`, `hover:bg-roam-orange/10`) as existing social buttons on that page

## Implementation Impact

### Code Changes Required

| File | Description |
|------|-------------|
| `src/pages/index.astro` | Add video embed section between hero and stats banner |
| `src/layouts/Layout.astro` | Add Instagram icon/link to footer social links (~line 226) |
| `src/pages/contact.astro` | Add Instagram icon/link to Follow Us section (~line 101) |

### New Files

None.

### Test Changes

No automated tests affected — this is a UI content addition. Manual verification:
- Video loads and plays on home page
- Video is responsive (mobile, tablet, desktop)
- Instagram link opens correct profile in new tab
- All three social icons render correctly in footer
- All three social icons render correctly on contact page

### Data / Migration Impact

None. No data changes required.

## Migration Plan

No breaking changes. This is purely additive — new HTML sections and links.

## Alternatives Considered

### Alternative 1: Self-hosted video instead of YouTube embed
- **Description**: Host the video file directly in `public/videos/` and use an HTML5 `<video>` element
- **Pros**: No third-party dependency, no YouTube branding, faster load if cached
- **Cons**: Large file size impacts page load and Railway bandwidth; no built-in player controls; loses YouTube SEO benefits and subscriber funnelling
- **Why not chosen**: YouTube embed is lighter, provides a familiar player, and directly funnels viewers to the channel for subscriptions

### Alternative 2: Video on a dedicated new page
- **Description**: Create a `/videos` page instead of embedding on the home page
- **Pros**: Keeps home page lean; room for multiple videos
- **Cons**: Lower visibility — most visitors won't navigate to a separate video page; loses the engagement benefit of having video front-and-centre
- **Why not chosen**: Home page placement maximizes visibility for the primary brand video. A dedicated video section can be added to the gallery page later.

### Alternative 3: Thumbnail with play button (click to load iframe)
- **Description**: Show a static thumbnail image; only load the YouTube iframe when the user clicks play
- **Pros**: Better initial page load performance (no iframe until interaction)
- **Cons**: Extra click before video plays; more complex implementation
- **Why not chosen**: For a single video, the performance difference is minimal with `loading="lazy"`. Simplicity wins. Can revisit if multiple videos are added later.

## Traceability

- **Idea doc**: N/A (direct user request)
- **Canonical docs**: No canonical docs affected
- **Implementation files**: `src/pages/index.astro`, `src/layouts/Layout.astro`, `src/pages/contact.astro`
- **Test files**: Manual testing only
- **Related audits**: None

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| YouTube iframe slows page load | Low | Medium | Use `loading="lazy"` attribute; video is below the fold |
| GDPR/privacy — YouTube iframe loads third-party cookies | Medium | Medium | Use `youtube-nocookie.com` privacy-enhanced embed domain to prevent third-party cookie tracking |
| Video removed/unavailable on YouTube | Low | Low | Broken embed shows blank — easy to swap URL later |
| Instagram URL changes | Low | Low | Simple text update if handle changes |

## Future Phase: Gallery Video Support

Not in scope for this plan, but noted for future work:
- Add a "Videos" tab or section to the gallery page (`src/pages/gallery.astro`)
- Support a mix of photos and embedded YouTube videos
- Could use a data file (like `products.json` pattern) to manage gallery media entries
- Would require extending the lightbox to handle video playback

## Approval

- **Approver**: Robert Di Capite
- **Date**: 2026-03-15
- **Conditions**: None

## Implementation Record

- **Implemented by**: AI
- **Date**: 2026-03-15
- **Sprint**: `docs/sprints/003-video-embed-social-links.md`
- **Deviations from plan**: None
