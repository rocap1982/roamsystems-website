---
doc_type: idea
status: draft
created: 2026-03-13
last_updated: 2026-03-13
owner: "Robert DiCapite"
tags: [images, gemini, marketing, product-photography]
related_plans: []
related_sprints: []
---

# Idea: Gemini-Powered Product Image Generation

## Summary

Use Google Gemini's image generation API to produce photorealistic lifestyle images of the M1 Certified U-Shape Seating/Bed System installed inside a VW Transporter T6 campervan. The product's exact form must be preserved — Gemini is used for scene composition, lighting, and context, not product design.

## Problem / Opportunity

### Current State
- Product images are studio/workshop photos hosted on Shopify CDN
- An initial generation script exists (`scripts/generate-t6-images.mjs`) but outputs distort the product form — Gemini invents its own version of the seat system rather than preserving the real design
- 6 detailed CAD renders and 3 real product photos are available as reference material

### Desired State
- 10+ high-quality lifestyle images per generation batch showing the seat/bed system in camping contexts
- Product form (U-shape frame, backrest, storage boxes, slat structure, side bracing) accurately preserved from reference images
- Varied scenes: different van angles, locations (UK coastal, forest, campsite), times of day, seating vs bed configuration
- Owner curates output manually, selecting best images for website use

### Why This Matters
- Professional lifestyle photography is expensive and time-consuming
- Lifestyle/in-context images convert better than studio shots for campervan products
- Iterative generation allows rapid testing of different marketing angles

## Constraints

- Product form accuracy is non-negotiable — the U-shape geometry, backrest angle, storage boxes, cup holders, and powder-coated black finish must match the CAD reference exactly
- Gemini API (gemini-2.5-flash-image model) is the generation engine
- API key already provisioned
- Output is static image assets — no runtime API integration on the website
- Manual curation step required before any image goes on the site

## Architecture / Approach

### Reference image strategy
Send all available reference material per request to maximise form accuracy:
- 6 CAD renders (`Gemini generated imges/sample drawings and photos for gemini/1-6.PNG`) — show exact geometry from multiple angles
- 3 real product photos (`Roam SYstems Images/website-images/product-images/m1-certified-u-shape-seating-frame/`) — show real-world appearance and finish

### Prompt engineering
- Explicitly describe the product's physical form in each prompt (U-shape, steel tube frame, black powder coat, storage boxes with cup holders, folding backrest, cross-member slats)
- Instruct Gemini to preserve the product exactly as shown in reference images
- Vary only the scene context (location, lighting, configuration, camera angle)

### Scene variety (10 prompts)
1. Rear doors open, bed mode, coastal sunset — wide angle from behind
2. Interior seating mode, couple having breakfast, campsite morning
3. Bed mode with cozy bedding, forest dawn, shot from inside looking out
4. Overhead interior shot, seating mode, showing full U-shape layout
5. Side door open, seating mode, lake/mountain backdrop
6. Bed mode converted, evening camp with fairy lights
7. Close-up detail shot of frame quality, powder coat finish, cup holders
8. Full system with kitchen pod and overhead locker, lifestyle morning coffee
9. Rear view, tailgate camping setup, chairs outside, bed visible inside
10. Split-angle showing seating-to-bed conversion capability

### Script improvements over current version
- Load all 9 reference images (6 CAD + 3 photos) instead of 4
- Much more explicit product-form descriptions in prompts
- Generate 10 images in sequence (1 per prompt)
- Output to timestamped folder for batch review
- Include prompt text in output filename for easy identification

### Output workflow
1. Script generates ~10 images to `Gemini generated imges/batch-YYYY-MM-DD/`
2. Owner reviews and selects winners
3. Selected images are optimized and placed in `public/images/` or used to replace Shopify CDN URLs

## Non-goals

- No runtime Gemini API calls from the website
- No automated quality filtering — owner curates manually
- Not generating images for other products (kitchen pods, lockers, etc.) in this iteration
- Not modifying website code to consume new images (separate task)

## Open Questions

- Does Gemini's current image generation model handle form preservation well enough with 9 reference images + detailed prompts, or will we need to iterate on prompting strategy?
- Should we also try generating images with the upholstery/cushions visible (showing the finished product vs bare frame)?
- What image resolution/aspect ratio is ideal for the website hero sections vs product gallery?
- Should failed/distorted outputs be kept for prompt iteration analysis?

## Traceability

- No canonical doc changes needed — this is an asset generation pipeline, not a contract change
- If generated images replace Shopify CDN URLs in `src/data/products.json`, that would be a minor data change (covered by a small fix workflow)
