---
doc_type: audit
audit_type: mini
status: resolved # active | resolved | superseded
resolved: 2026-06-12
created: 2026-06-12
auditor: "AI (Claude Code)"
scope: "T&Cs overhaul + mandatory checkout terms-acceptance + design-number marking (plan 2026-06-11-terms-acceptance-and-ip, deployed 2026-06-12)"
open_p0: 0
open_p1: 0
---

# Mini Audit Result: T&Cs overhaul + checkout terms-acceptance + design marking — 2026-06-12

## Purpose

Verify alignment between the implemented/deployed terms-acceptance change and
its approved plan + canonical contracts. Trigger: plan
`docs/plans/2026-06-11-terms-acceptance-and-ip.md` (approved 2026-06-11),
implemented in commit `eb9f9e5`, deployed 2026-06-12 (deploy `da2ffa2a`,
commit `3b3918d`) after the owner set the Stripe Dashboard ToS URL.

## Scope

- **In scope**:
  - `src/pages/policies/terms.astro` — full rewrite vs plan section outline (11 sections).
  - `src/pages/api/checkout.ts` — `consent_collection` + `custom_text.terms_of_service_acceptance`.
  - `src/pages/api/webhook.ts` / `src/lib/email.ts` — consent evidence line in the order-confirmation email.
  - `src/pages/policies/refund.astro` — CCR 2013 patch.
  - Basket UI notice (`src/pages/basket.astro`, `src/layouts/Layout.astro` cart sidebar).
  - Design-number marking (`src/pages/certifications.astro`, `src/components/home/Footer.astro`, `src/pages/products/[id].astro`).
  - `docs/reference/SCHEMA_AND_CONTRACTS_CANONICAL.md` — checkout + webhook/email contract updates.
  - Live serving spot-checks (terms page, basket notice, product-page marking).
- **Out of scope**:
  - Legal sufficiency of the drafted wording (plan risk register already recommends solicitor review — AI-drafted terms are a baseline, not legal advice).
  - End-to-end live paid order with ticked checkbox → email consent line (will be evidenced by the first real order; every confirmation BCCs the business inbox).
  - Offline items the plan explicitly excluded: drawings-release licence letter, design-renewal calendar backstops, physical product marking.
  - Stripe live price verification (separate optional task in CURRENT_STATUS).

## Canonical references reviewed

- `docs/plans/2026-06-11-terms-acceptance-and-ip.md` (spec items 1–5, Implementation Record)
- `docs/reference/SCHEMA_AND_CONTRACTS_CANONICAL.md` (POST /api/checkout, POST /api/webhook sections)

## Summary

- **Total issues**: 3
- **P0**: 0
- **P1**: 0
- **P2**: 0
- **P3**: 3
- **Assessment**: ✅ Aligned — all contract-bearing surfaces (terms content, checkout consent params, email evidence line, canonical doc) match the approved plan and the deployed code exactly. The three P3s are cosmetic completeness items on non-binding, belt-and-braces surfaces.

### Verified aligned (core surfaces)

| Plan spec | Implementation | Status |
|---|---|---|
| Terms rewrite, 11-section outline | `terms.astro` contains all 11 sections; real company details (Co. 07411656, registered office, VAT GB 974 5806 77 — no placeholders shipped); IP clause names Romark Holdings Ltd as owner / Romark Engineering Ltd as licensee; UK RDs 6266396–6266399 + EU RCDs 015033319-0001..0004; documentation-licence + no-reverse-engineering wording; CRA 2015 / CCR 2013 carve-outs; contract-at-dispatch; England & Wales law | ✅ |
| `consent_collection.terms_of_service: 'required'` + `custom_text` message | `checkout.ts:91–98` — message text matches plan verbatim, links `${origin}/policies/terms`; additive only, all pre-existing params intact | ✅ |
| Consent evidence in order email | `email.ts:174–176` — "Terms: Accepted at checkout (Stripe consent record)" row rendered when `session.consent?.terms_of_service === 'accepted'`; webhook passes the full retrieved session (consent present by default — plan deviation note confirmed correct) | ✅ |
| Refund policy CCR 2013 patch | `refund.astro:13–16` — 14-day distance-selling right + made-to-order/personalised exemption | ✅ (cross-ref gap → AUDIT-003) |
| Basket notice | `basket.astro:41` — "By placing an order you agree to our Terms of Service" at the checkout button | ✅ on /basket (sidebar gap → AUDIT-001) |
| Design-number marking (certs page, product pages, footer) | `certifications.astro:138–139, 200` UK + EU numbers with dates; `Footer.astro:20–21, 85–86` badge chips + small-print marking line + Co. Reg/VAT line (sitewide, including all product pages) | ✅ (product badge gap → AUDIT-002) |
| Canonical doc update | `SCHEMA_AND_CONTRACTS_CANONICAL.md` checkout section gains consent params + Stripe account ToS-URL prerequisite; webhook section gains consent/email line — matches code exactly | ✅ |
| Deploy-order condition (ToS URL before deploy) | Honoured: implementation committed `[skip ci]`; deployed only after owner set the Dashboard ToS URL; live session creation verified returning `consent_collection.terms_of_service=required` (2026-06-12); re-check script `scripts/verify-tos-consent.mjs` added | ✅ |

## Issues

### AUDIT-2026-06-12-001

- **Priority**: P3
- **Location**: `src/layouts/Layout.astro:103–107` (cart sidebar checkout section)
- **Canonical ref**: `docs/plans/2026-06-11-terms-acceptance-and-ip.md` spec item 4 (basket notice)
- **What is wrong**: The sidebar "Checkout — Pay Now" button's small print reads only "Secure checkout powered by Stripe". The terms-agreement line was added to `/basket` only, so a customer checking out from the cart sidebar (available on every page) never sees the on-site notice.
- **Expected**: Agreement small print near every checkout button. (Plan wording was "Layout.astro and/or basket.astro", so this is within the plan's latitude — and legally moot, since the required Stripe checkbox is the binding act on every path.)
- **Status**: Resolved 2026-06-12 (FIX-2026-06-12-001 — sidebar small print now reads "Secure checkout powered by Stripe • By placing an order you agree to our Terms of Service" (Layout.astro), mirroring basket.astro.)
- **Fix recommendation**: Append "• By placing an order you agree to our [Terms of Service](/policies/terms)" to the sidebar small-print line, mirroring `basket.astro:41`.

### AUDIT-2026-06-12-002

- **Priority**: P3
- **Location**: `src/pages/products/[id].astro:141–150` (Registered Design badge)
- **Canonical ref**: plan spec item 5 (design-number marking, s.24B RDA 1949)
- **What is wrong**: The product-page badge still names only "EU Registered Design — RCD No. 015033319"; the UK Registered Designs Nos. 6266396–6266399 (the ones that matter for the UK innocent-infringement defence) are not in the badge. The badge also renders only for Frames-category products, though the registrations also cover cushions/mattresses.
- **Expected**: Product detail pages marked with UK + EU numbers. **Mitigation**: the sitewide footer marking line renders on every product page (verified serving live), so the marking purpose is already met on all pages; the badge is supplementary.
- **Status**: Resolved 2026-06-12 (FIX-2026-06-12-002 — badge now reads "UK & EU Registered Designs / UK Nos. 6266396–6266399 • Registered 06/03/2023 • EU RCD No. 015033319 • Registered 06/09/2023". Kept Frames-only rendering deliberately: badge is supplementary; the sitewide footer marking line covers all product pages.)
- **Fix recommendation**: Extend the badge text to "UK Registered Designs Nos. 6266396–6266399 • EU RCD No. 015033319" and consider rendering it for upholstery/cushion products too.

### AUDIT-2026-06-12-003

- **Priority**: P3
- **Location**: `src/pages/policies/refund.astro`
- **Canonical ref**: plan Canonical Changes table — refund.astro: "…cross-reference new terms"
- **What is wrong**: CCR 2013 wording and the made-to-order exemption are present, but the page contains no link to `/policies/terms`. The cross-reference is one-way (terms §6 and §9 link to the Refund Policy; the reverse link was not added).
- **Expected**: Refund Policy cross-references the Terms of Service per the plan.
- **Status**: Resolved 2026-06-12 (FIX-2026-06-12-003 — made-to-order paragraph now ends "...See also our Terms of Service." linking /policies/terms (refund.astro).)
- **Fix recommendation**: Add one sentence to the intro, e.g. "Refunds and cancellations are governed by our [Terms of Service](/policies/terms)."

## Documentation completeness check

- `docs/reference/SCHEMA_AND_CONTRACTS_CANONICAL.md` — updated in the same commit; verified to match deployed code exactly (consent params, account prerequisite, email consent line). ✅
- Plan carries a complete Implementation Record with deviations (webhook no-op, certifications-page approach, footer Co. Reg/VAT addition, `[skip ci]` deploy gating) — all deviations confirmed accurate against the diffs. ✅
- `PROJECT_STATUS.md` / `docs/sprints/CURRENT_STATUS.md` — updated at deploy time; updated again by this audit. ✅
- Note (no issue raised): `scripts/verify-tos-consent.mjs` (added in `3b3918d`) is not referenced in any status/reference doc; it is self-documenting (usage comment in-file) and mirrors the existing `verify-stripe-prices.mjs` pattern.
- No undocumented shipped features or contracts found in this scope.

## Test verification performed

- **Automated**:
  - [x] `npm run build` — PASS (2026-06-12, this audit; all pages incl. terms/refund/certifications/products prerendered, sitemap generated).
- **Manual / live (2026-06-12, this audit)**:
  - [x] `https://www.roamsystems.co.uk/policies/terms` serves the new content (company no. 07411656, UK design numbers, Romark Holdings wording — 4/4 markers present).
  - [x] `https://www.roamsystems.co.uk/basket` serves the terms-agreement notice.
  - [x] Product detail page serves the UK design-number marking (via sitewide footer).
- **Previously recorded (2026-06-12 deploy verification, per CURRENT_STATUS)**:
  - [x] Live session creation returns `consent_collection.terms_of_service=required` (Stripe Dashboard ToS URL set by owner; `scripts/verify-tos-consent.mjs` available for re-checks).
- **Not re-run this pass**: live `POST /api/checkout` (avoided creating live checkout sessions); full paid order → email consent line (first real order will evidence it; confirmations BCC the business inbox).

## Resolution / follow-up

- 2026-06-12: all three P3s fixed in a single small-fix pass; build PASS; deployed with this commit. Original next steps: fix the three P3s as a single small-fix pass (3 files, ~5 lines total: `Layout.astro` sidebar small print, `products/[id].astro` badge text, `refund.astro` cross-reference), then move this audit to `docs/audits/resolved/2026-06/`.
- Standing recommendation carried from the plan (not an audit issue): solicitor review of the final terms wording.
- If resolved, move this file to `docs/audits/resolved/2026-06/` and update `PROJECT_STATUS.md`.
