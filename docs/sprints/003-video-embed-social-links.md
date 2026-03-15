---
doc_type: sprint
status: active
stage: verification
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

- **Stage**: verification
- **Scope**: Home page (`index.astro`), footer (`Layout.astro`), contact page (`contact.astro`)
- **Contract changes**: None — UI/content additions only

## Acceptance Criteria

- [ ] YouTube video is embedded on the home page directly below the hero section
- [ ] Video uses privacy-enhanced `youtube-nocookie.com` embed domain
- [ ] Video is responsive across mobile, tablet, and desktop viewports
- [ ] "Subscribe to our channel" CTA with link to `https://www.youtube.com/@roamsystems` appears below the video
- [ ] Instagram icon/link (`https://www.instagram.com/roamsystems_m1ushape`) is present in the site footer
- [ ] Instagram icon/link is present on the contact page "Follow Us" section
- [ ] All three social icons (Facebook, Instagram, YouTube) render correctly in the footer
- [ ] All three social icons render correctly on the contact page
- [ ] Video section uses `loading="lazy"` for performance
- [ ] Build passes with no errors (`npm run build`)

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

### Manual

- [ ] Home page: video section visible below hero
- [ ] Home page: video plays when clicked
- [ ] Home page: video container is responsive (resize browser to mobile/tablet widths)
- [ ] Home page: "Subscribe to our channel" link opens `https://www.youtube.com/@roamsystems` in new tab
- [ ] Footer: Instagram icon visible alongside Facebook and YouTube
- [ ] Footer: Instagram link opens `https://www.instagram.com/roamsystems_m1ushape` in new tab
- [ ] Contact page: Instagram icon visible in "Follow Us" section
- [ ] Contact page: Instagram link opens correct profile in new tab
- [ ] All social icons have correct hover effects

## Review Gate

- [ ] All acceptance criteria met
- [ ] `npm run build` passes
- [ ] Manual test checklist complete
- [ ] No visual regressions on home, contact, or footer

## Documentation DoD

- [ ] No canonical docs affected (UI-only change)
- [ ] Update `PROJECT_STATUS.md` page count if applicable (no new pages added)

## Audit Plan

None needed — no canonical surfaces (schema, API, DB, business rules) are touched. This is a purely additive UI/content change.

## Notes

<!-- Decisions, links, trade-offs recorded during implementation -->
- Video URL: https://www.youtube.com/watch?v=n5DPLh2mOmY
- Subscribe channel: https://www.youtube.com/@roamsystems
- Instagram: https://www.instagram.com/roamsystems_m1ushape
