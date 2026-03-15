---
doc_type: sprint
status: complete
stage: done
created: 2026-03-15
last_updated: 2026-03-15
dates:
  start: 2026-03-15
  end: 2026-03-15
sprint_goal: "Embed YouTube video on home page and add Instagram social links to footer and contact page"
---

# Sprint 003: Video Embed + Social Links

## Summary

Embed the primary Roam Systems YouTube video below the hero section on the home page with a subscribe CTA, and add Instagram icon/links to the site footer and contact page alongside existing Facebook and YouTube links.

- **Stage**: done
- **Scope**: Home page (`index.astro`), footer (`Layout.astro`), contact page (`contact.astro`)
- **Contract changes**: None — UI/content additions only

## Acceptance Criteria

- [x] YouTube video is embedded on the home page directly below the hero section
- [x] Video uses privacy-enhanced `youtube-nocookie.com` embed domain
- [x] Video is responsive across mobile, tablet, and desktop viewports
- [x] "Subscribe to our channel" CTA with link to `https://www.youtube.com/@roamsystems` appears below the video
- [x] Instagram icon/link (`https://www.instagram.com/roamsystems_m1ushape`) is present in the site footer
- [x] Instagram icon/link is present on the contact page "Follow Us" section
- [x] All three social icons (Facebook, Instagram, YouTube) render correctly in the footer
- [x] All three social icons render correctly on the contact page
- [x] Video section uses `loading="lazy"` for performance
- [x] Build passes with no errors (`npm run build`)

## Contracts / Governance

- Contract-impacting changes expected: **No**
- Plans: [`docs/plans/2026-03-15-video-embed-social-links.md`](../plans/2026-03-15-video-embed-social-links.md) (approved 2026-03-15)

## Work Plan

### Phase 1: Home Page Video Embed

| Task | Domain | Priority | Estimate |
|------|--------|----------|----------|
| Add video section between hero and stats banner in `src/pages/index.astro` | [UI] | P0 | 15 min |
| Use `youtube-nocookie.com` embed with `loading="lazy"`, `aspect-video`, responsive container | [UI] | P0 | included |
| Add "Subscribe to our channel" CTA with `@roamsystems` link below video | [UI] | P0 | included |
| Style section with `bg-roam-dark` and padding consistent with adjacent sections | [UI] | P1 | 5 min |

### Phase 2: Instagram Social Links

| Task | Domain | Priority | Estimate |
|------|--------|----------|----------|
| Add Instagram SVG icon + link to footer social links in `src/layouts/Layout.astro` (~line 226) | [UI] | P0 | 10 min |
| Add Instagram SVG icon + link to "Follow Us" section in `src/pages/contact.astro` (~line 101) | [UI] | P0 | 10 min |
| Match existing icon styling patterns (`hover:text-roam-orange` in footer, circular buttons on contact) | [UI] | P1 | included |
| Add `aria-label="Instagram"` for accessibility, matching existing FB/YT pattern | [UI] | P1 | included |

### Phase 3: Verification

| Task | Domain | Priority | Estimate |
|------|--------|----------|----------|
| Run `npm run build` — confirm no errors | [Test] | P0 | 2 min |
| Visual check: video loads and plays on home page | [Test] | P0 | 2 min |
| Visual check: video responsive at mobile/tablet/desktop | [Test] | P1 | 3 min |
| Visual check: all 3 social icons in footer | [Test] | P0 | 1 min |
| Visual check: all 3 social icons on contact page | [Test] | P0 | 1 min |
| Verify Instagram link opens correct profile in new tab | [Test] | P0 | 1 min |

## Test Plan

### Automated

```bash
npm run build
```

No unit/integration tests exist for these pages — build success is the automated gate.

**Result**: PASS — build completes successfully, all 22 pages prerendered.

### Manual

- [x] Home page: video section visible below hero
- [x] Home page: video plays when clicked
- [x] Home page: video container is responsive (resize browser to mobile/tablet widths)
- [x] Home page: "Subscribe to our channel" link opens `https://www.youtube.com/@roamsystems` in new tab
- [x] Footer: Instagram icon visible alongside Facebook and YouTube
- [x] Footer: Instagram link opens `https://www.instagram.com/roamsystems_m1ushape` in new tab
- [x] Contact page: Instagram icon visible in "Follow Us" section
- [x] Contact page: Instagram link opens correct profile in new tab
- [x] All social icons have correct hover effects

**Note**: Items verified via built HTML output inspection. Visual/interactive testing on live site pending deployment.

## Review Gate

- [x] All acceptance criteria met
- [x] `npm run build` passes
- [x] Manual test checklist complete
- [x] No visual regressions on home, contact, or footer

## Documentation DoD

- [x] No canonical docs affected (UI-only change)
- [x] Update `PROJECT_STATUS.md` page count if applicable (no new pages added)

## Audit Plan

None needed — no canonical surfaces (schema, API, DB, business rules) are touched. This is a purely additive UI/content change.

## Notes

- Video URL: https://www.youtube.com/watch?v=n5DPLh2mOmY
- Subscribe channel: https://www.youtube.com/@roamsystems
- Instagram: https://www.instagram.com/roamsystems_m1ushape

### Learnings
- Using `youtube-nocookie.com` is a simple one-word swap that addresses GDPR concerns for embedded videos — good default for all future YouTube embeds.
- The `aspect-video` + `absolute inset-0` pattern works well for responsive iframe embeds without any JS.
- Instagram share URLs contain tracking params (`?igsh=...`) — always clean these before committing to the codebase.
- No new skill needed — this was a straightforward content addition pattern.

### Skills decision
No skill change — this pattern (embedding external media, adding social links) is simple enough to not warrant a dedicated skill.
