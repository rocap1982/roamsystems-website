---
doc_type: audit
audit_type: mini
status: active # active | resolved | superseded
created: 2026-06-08
auditor: "AI (Claude Code)"
scope: "Checkout order-detail capture (phone + vehicle custom fields, confirmation email) + pricing source-of-truth refactor + vehicle fleet expansion to 6"
open_p0: 0
open_p1: 0
---

# Mini Audit Result: Checkout order-detail capture + pricing source-of-truth — 2026-06-08

## Purpose

Verify alignment between recent implementation changes and the canonical
contracts after work that landed since the last documented sprint/audit.
Trigger: commits `28d511a` (10:00 auto-backup — checkout custom fields +
confirmation-email customer block + canonical doc update), `2b05d45`
(remove dev email-preview scaffold), and `cfaa4d3` (price rise + make
`products.json` the sole price source of truth).

## Scope

- **In scope**:
  - `POST /api/checkout` — new `phone_number_collection` + `custom_fields` (vehicle dropdown, vehicleYearReg text).
  - `src/lib/email.ts` — `VEHICLE_LABELS` map, `getCustomFieldValue`, Customer Details block in the order-confirmation email.
  - `POST /api/webhook` — session retrieval / expand list for the email.
  - `docs/reference/SCHEMA_AND_CONTRACTS_CANONICAL.md` — checkout + webhook contract updates.
  - Pricing source-of-truth refactor: homepage trust marquee build-time price (`src/components/home/homeData.ts`), prebuild guard (`scripts/check-blog-prices.mjs`), blog price removal.
  - Vehicle fleet: `src/data/vehicles.json` now has 6 vehicles.
- **Out of scope**:
  - Stripe dashboard state (live Price IDs, tax behaviour) — not re-verified against the live account this pass.
  - Gallery category-filter feature (`40f217a`) — UI-only, no canonical surface.
  - Full content review of the new draft blog post (`draft-campervan-kitchen-pod-guide.md`).
  - End-to-end live checkout (requires a real Stripe test session).

## Canonical references reviewed

- `docs/reference/SCHEMA_AND_CONTRACTS_CANONICAL.md` — `POST /api/checkout` (session params, custom fields), `POST /api/webhook` (handled events, email contents), product schema.
- `PROJECT_STATUS.md` — tech-stack summary (vehicle count, product data).
- `docs/sprints/CURRENT_STATUS.md` — "4 vehicles" claims.

## Summary

- **Total issues**: 6
- **P0**: 0
- **P1**: 0
- **P2**: 3
- **P3**: 3
- **Assessment**: ⚠️ Minor drift

Note: the customer-facing vehicle/product pages render correctly for all 6
vehicles — the compatibility UI is driven by `vehicle.compatibleProducts`
(complete for all 6). The fleet-expansion drift is confined to two trailing-edge
surfaces (the Google Merchant feed's `custom_label_0` and the `/vehicles` page
copy) that were not updated when Renault Trafic + Nissan Primastar were added.

The code↔canonical-contract alignment for the checkout/email change is
**strong** — the canonical doc was updated in the same commit as the code and
matches it precisely (custom-field keys, values, optional/required, max length,
the `VEHICLE_LABELS` sync note). The build passes including the new prebuild
blog-price guard. Drift is confined to (1) one likely-unintended customer-facing
pricing regression in the homepage marquee, and (2) stale status-doc snapshots
(vehicle count, undocumented checkout feature).

## Issues

### AUDIT-2026-06-08-001

- **Priority**: P2
- **Location**: `src/components/home/homeData.ts:137-140`
- **Canonical ref**: `cfaa4d3` commit intent ("trust marquee 'From £1,999' → 'From £2,050'")
- **What is wrong**: The source-of-truth refactor replaced the hardcoded "From £2,050" marquee label with `Math.min(...all variant prices)`, which now resolves to **£356** (the cheapest accessory variant — cushion boards/foam), not the cheapest seating frame. The homepage trust marquee therefore advertises **"From £356 + VAT"**, undercutting the intended ~£2,050 frame entry price.
- **Expected**: Marquee should reflect the intended headline "from" price (cheapest seating frame, ~£2,050), per the originating commit message. Computing `Math.min` over the entire catalogue including low-cost accessories changes the advertised entry price.
- **Status**: Open
- **Fix recommendation**: Decide the intended semantics. Either (a) compute the min over a defined subset (e.g. products in the `Frames` category, or a flagged "headline" product), or (b) if "From £356" is genuinely acceptable, confirm with the owner and update the `cfaa4d3` intent note. Verify the rendered marquee on the homepage after the change.

### AUDIT-2026-06-08-002

- **Priority**: P3
- **Location**: `PROJECT_STATUS.md:30` and `docs/sprints/CURRENT_STATUS.md:43`
- **Canonical ref**: `src/data/vehicles.json` (now 6 vehicles)
- **What is wrong**: Status docs still say "4 vehicles (VW T5, T6, T6.1, Ford Transit Custom)" and "All 9 products compatible with all 4 vehicles". `vehicles.json` now has **6** (added Renault Trafic, Nissan Primastar), the build generates 6 vehicle pages, and the checkout dropdown + homepage list both reflect 6.
- **Expected**: Status docs say 6 vehicles and list the two additions.
- **Status**: Open
- **Fix recommendation**: Update `PROJECT_STATUS.md` vehicle line and `CURRENT_STATUS.md` "Notes / Decisions" to 6 vehicles. (Done as part of this audit's status-doc updates — see below.)

### AUDIT-2026-06-08-003

- **Priority**: P3
- **Location**: `PROJECT_STATUS.md`, `docs/sprints/CURRENT_STATUS.md` (Recently Closed Work)
- **Canonical ref**: `28d511a`, `2b05d45` (checkout order-detail capture)
- **What is wrong**: The checkout order-detail capture feature (phone collection + vehicle custom fields + Customer Details email block) is a contract-level change that updated the canonical doc, but is **not** reflected in either status snapshot. A "resume fast" reader would not know this shipped.
- **Expected**: Status docs note the checkout order-detail capture as recently shipped work.
- **Status**: Open
- **Fix recommendation**: Add a Recently Closed Work row and refresh the tech-stack note. (Done as part of this audit — see below.)

### AUDIT-2026-06-08-004

- **Priority**: P3
- **Location**: `src/pages/checkout/success.astro:25`
- **Canonical ref**: `docs/reference/SCHEMA_AND_CONTRACTS_CANONICAL.md#post-apiwebhook` (custom_fields returned by default)
- **What is wrong**: The success page reads only `customer_details.email`; it does not surface the newly captured phone or vehicle/year-reg custom fields. This is not a contract violation (the email is the canonical place those fields surface, and the doc only promises them in the email), but the success page is now slightly behind the data the checkout collects.
- **Expected**: Optional enhancement — the success page could echo the captured vehicle for buyer reassurance. No canonical requirement to do so.
- **Status**: Open (informational / enhancement, not drift against canon)
- **Fix recommendation**: Optional. If desired, surface vehicle + phone on the success page using the same `getCustomFieldValue` pattern. No action required for contract alignment.

### AUDIT-2026-06-08-005

- **Priority**: P2
- **Location**: `src/data/products.json` (every product's `compatibleVehicles`), consumed by `src/pages/feeds/google-merchant.xml.ts:40,68` (`custom_label_0`)
- **Canonical ref**: `PROJECT_STATUS.md` product schema (`compatibleVehicles` field); `src/data/vehicles.json` (6 vehicles)
- **What is wrong**: The fleet grew to 6 vehicles (Renault Trafic, Nissan Primastar added), and `vehicle.compatibleProducts` was populated for all 6 — but the inverse field on each product, `compatibleVehicles`, still lists only the original 4. This field feeds the Google Merchant feed's `g:custom_label_0`, so every product in the feed omits the two new vehicles. (Customer-facing vehicle/product pages are unaffected — they read `vehicle.compatibleProducts`, which is complete.)
- **Expected**: `compatibleVehicles` on each product reflects all vehicles the product fits (all 6), keeping the Merchant feed label consistent with `vehicle.compatibleProducts`.
- **Status**: Open
- **Fix recommendation**: Either add `renault-trafic` + `nissan-primastar` to every product's `compatibleVehicles`, or — better — derive `compatibleVehicles` from `vehicle.compatibleProducts` at build time to eliminate the two-way-sync drift trap (mirrors the products.json price source-of-truth refactor pattern in `cfaa4d3`).

### AUDIT-2026-06-08-006

- **Priority**: P2
- **Location**: `src/pages/vehicles/index.astro:10,16`
- **Canonical ref**: `src/data/vehicles.json` (6 vehicles)
- **What is wrong**: The `/vehicles` listing page's SEO meta description (`<Layout description=...>`) and the visible page subtitle both read "fits VW Transporter T5, T6, T6.1 and Ford Transit Custom" — omitting Renault Trafic and Nissan Primastar. Customer-facing + indexed by search engines.
- **Expected**: Copy names all 6 supported vehicles (or is phrased to not enumerate, e.g. "VW Transporter, Ford Transit Custom, Renault Trafic, Nissan Primastar and more").
- **Status**: Open
- **Fix recommendation**: Update both strings on `vehicles/index.astro`. Consider generating the list from `vehicles.json` to prevent recurrence.

## Documentation completeness check

- **Checkout custom fields / webhook email**: ✅ Documented in `SCHEMA_AND_CONTRACTS_CANONICAL.md` in lockstep with the code (custom-field keys, values, required/optional, max length, VEHICLE_LABELS sync note). No undocumented contract surface.
- **Pricing source-of-truth refactor**: ⚠️ Partially documented. The price rise is in status docs; the "products.json is sole source of truth" refactor + the prebuild guard `scripts/check-blog-prices.mjs` are documented in the commit but not surfaced in any canonical reference (acceptable — it's a build-process guard, low value as canon, but worth a one-line note if a build/scripts reference exists).
- **Vehicle fleet expansion (4→6)**: ❌ Undocumented in status docs (AUDIT-2026-06-08-002).
- **Checkout order-detail feature**: ❌ Undocumented in status docs (AUDIT-2026-06-08-003).

## Test verification performed

- **Automated**:
  - [x] `npm run build` — passes, including `prebuild` blog-price guard (`scripts/check-blog-prices.mjs`) and build-time marquee price computation. 6 vehicle pages + 9 product pages generated.
  - [x] `buildEmailHtml` confirmed internal-only (not exported) after `2b05d45` revert.
  - [x] Dev preview route `src/pages/dev/order-email-preview.ts` confirmed deleted.
- **Manual**:
  - [x] Cross-read `checkout.ts` custom_fields vs `SCHEMA_AND_CONTRACTS_CANONICAL.md` — values, required/optional, max length all match.
  - [x] Cross-read `VEHICLE_LABELS` (email.ts) vs checkout dropdown options — keys match exactly (7 entries incl. `other`).
  - [x] `vehicles.json` keys vs checkout dropdown — 6 vehicle keys consistent.
  - [x] Webhook expand list (`line_items`, `shipping_cost`) — sufficient; `customer_details`/`custom_fields`/`shipping_details` returned by default on session retrieve.
  - [ ] Live Stripe test checkout (vehicle dropdown renders, phone collected, confirmation email shows Customer Details) — NOT performed (requires live test session).

## Resolution / follow-up

- Next steps:
  1. Decide intended marquee "from" price semantics and fix AUDIT-2026-06-08-001 (P2, customer-facing).
  2. Backfill / derive product `compatibleVehicles` for the 2 new vehicles — fixes Merchant-feed `custom_label_0` (AUDIT-2026-06-08-005, P2).
  3. Update `/vehicles` page copy + meta description to all 6 vehicles (AUDIT-2026-06-08-006, P2).
  4. Status-doc drift (002, 003) corrected as part of this audit.
  5. Optionally run a live Stripe test checkout to confirm the dropdown renders and the email Customer Details block populates end-to-end.
- This audit stays **active** until the three P2 issues (001, 005, 006) are resolved. When resolved, move to `docs/audits/resolved/2026-06/` and update `PROJECT_STATUS.md`.
