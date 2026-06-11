---
doc_type: plan
status: approved
created: 2026-06-11
author: "Claude (AI)"
approver: "Rob di Capite"
approved: 2026-06-11
related_issues: []
---

# Plan: T&Cs Overhaul (IP/Design-Right Clause) + Mandatory Pre-Payment Terms Acceptance

## Problem Statement

### Current State

- `src/pages/policies/terms.astro` is a thin, stale Terms of Service page:
  - **IP clause covers website content only** ("All content on this website… is protected by copyright law"). There is **no clause covering product designs, design rights, drawings/CAD/documentation, or reverse engineering**.
  - **Contract formation describes the old enquiry flow** ("Submitting an enquiry… does not constitute a binding order. Orders are confirmed once we contact you and payment has been arranged."). The site has taken payment directly via Stripe Checkout since Sprint 1 — the clause no longer describes reality.
  - Terms are attributed to "ROAM Systems" (a trading name); the legal entity **Romark Engineering Ltd is not identified** (company number / registered office / VAT number missing — required by the Companies Act 2006 and E-Commerce Regulations 2002 for a trading website).
  - No governing-law/jurisdiction clause, no consumer-cancellation summary (Consumer Contracts Regulations 2013), no warranty clause, and a blanket liability exclusion that is likely unenforceable against consumers (Consumer Rights Act 2015 — cannot exclude liability for death/personal injury caused by negligence).
- **No acceptance mechanism exists.** `src/pages/api/checkout.ts` creates Stripe Checkout Sessions with no `consent_collection`; a customer can pay without ever seeing the terms. Legally this is "browsewrap" (terms linked in the footer), the weakest form of online terms.
- Live business trigger: a trade customer (fabrication company) has requested CAD files "to assist installation". There is currently **no contractual basis** the customer has agreed to that reserves design rights or limits use of supplied documentation.

### Desired State

- A complete, UK-compliant Terms of Service page naming Romark Engineering Ltd, including a **product IP & design-rights clause** and a **documentation licence clause** (drawings supplied for installation only; no manufacture, reproduction, or reverse engineering).
- **Clickwrap acceptance**: every checkout requires an affirmative "I agree to the Terms of Service" tick **before payment**, via Stripe Checkout `consent_collection.terms_of_service = 'required'`.
- **Evidence trail**: Stripe records consent on the Checkout Session (`session.consent.terms_of_service === 'accepted'`, timestamped by Stripe). The order-confirmation email gains a "Terms accepted at checkout: Yes" line so every order record carries the evidence.

### Why This Matters

- Clickwrap acceptance (required checkbox + recorded consent) **forms a binding agreement** under English law — no wet signature needed. Browsewrap terms are frequently held non-binding because the customer never assented.
- Without a design-rights/documentation clause, refusing or conditioning CAD/drawing requests rests on goodwill rather than contract. With it, any copying becomes a knowing breach of an agreed term plus IP infringement — a far stronger enforcement position.
- The stale enquiry-flow wording and missing company identification are compliance drift on a live, paid e-commerce site.

## Proposed Solution

### Canonical Changes Required

| Document | Change Type (Minor/Major/Patch) | Description |
|----------|------|-------------|
| `docs/reference/SCHEMA_AND_CONTRACTS_CANONICAL.md` | Minor (additive) | `/api/checkout` session creation gains `consent_collection` + `custom_text.terms_of_service_acceptance`; webhook/email contract gains consent status line. |
| `src/pages/policies/terms.astro` (business rules) | Major | Full rewrite — see specification. This page becomes a canonical business-rules surface. |
| `src/pages/policies/refund.astro` | Patch | Align cancellation wording with Consumer Contracts Regulations 2013 + made-to-order exemption; cross-reference new terms. |

### Proposed Specification

#### 1. New Terms of Service content (`src/pages/policies/terms.astro`)

Section outline (full copy drafted at implementation, owner/solicitor to review wording):

1. **Who we are** — ROAM Systems is a trading name of Romark Engineering Ltd, company no. `[OWNER TO SUPPLY]`, registered office `[OWNER TO SUPPLY]`, VAT no. `[OWNER TO SUPPLY]`, contact sales@roamsystems.co.uk.
2. **These terms and how you accept them** — terms apply to all orders; acceptance is given by ticking the agreement box at checkout; consumers' statutory rights are unaffected; business customers contract on these terms to the exclusion of their own.
3. **Orders and contract formation** — your order is an offer; the contract forms **when we dispatch the goods**; we may decline or cancel any order with a full refund at any time before dispatch.
4. **Prices and payment** — GBP, VAT, Stripe payment at checkout.
5. **Delivery** — references the Shipping Policy (2–4 week build, 3–5 working days after dispatch).
6. **Cancellation and returns** — consumers' 14-day distance-selling rights under the Consumer Contracts Regulations 2013, including the exemption for goods made to the consumer's specification; references the Refund Policy.
7. **Intellectual property and design rights** (the core new clause):
   - All product designs, and all drawings, CAD models, specifications, installation guides, and other documentation, are and remain the exclusive property of the Romark group, protected by copyright, UK unregistered design right, **UK registered designs Nos. 6266396–6266399 (filed 06/03/2023, proprietor Romark Holdings Ltd, designer Rob di Capite)** and **EU registered Community designs Nos. 015033319-0001 to -0004 (registered 06/09/2023, claiming UK priority)** covering the seat/bed system, its cushions/mattresses, and its frame.
   - **Ownership (confirmed from UKIPO register extract, 2026-06-11):** the UK designs were filed by Romark Engineering Limited and assigned to **Romark Holdings Ltd** (assignment DRC000031033, effective 05/09/2023, recorded 14/09/2023). UK status: **Registered**, renewal due 06/03/2028. Clause wording: designs owned by Romark Holdings Ltd and used under licence by Romark Engineering Ltd. Remaining owner confirmation: whether a written (ideally exclusive) intra-group licence exists — recommended regardless, as exclusivity affects who may bring infringement proceedings. UK attorneys on record: Agile IP LLP (ref D4026/RME).
   - **Purchase of a product transfers ownership of that physical item only.** It grants no licence to manufacture, reproduce, copy, adapt, or commercially exploit the product's design in whole or in part.
   - Any drawings or documentation we supply are licensed **solely for the installation, use, and maintenance of the purchased product**, are confidential, must not be disclosed to third parties, and must not be used to manufacture or have manufactured any product or component, nor for reverse engineering.
8. **Certification and installation** — M1/pull-test certification applies only to genuine products as manufactured by Romark Engineering Ltd and installed per our instructions; it does not extend to copies or modified products.
9. **Warranty and defective goods** — statutory rights under the Consumer Rights Act 2015 unaffected; defective-goods process per Refund Policy.
10. **Liability** — nothing excludes liability for death or personal injury caused by negligence, or for fraud; otherwise liability capped at the price paid; indirect/consequential loss excluded for business customers.
11. **Governing law and jurisdiction** — England and Wales.

#### 2. Checkout consent (`src/pages/api/checkout.ts`)

Additive parameters to `stripe.checkout.sessions.create`:

```ts
consent_collection: {
  terms_of_service: 'required',
},
custom_text: {
  terms_of_service_acceptance: {
    message: `I agree to the [Terms of Service](${origin}/policies/terms), including the intellectual property and design rights provisions.`,
  },
},
```

Behaviour: Stripe Checkout renders a **required checkbox** above the Pay button; payment cannot complete without ticking it. Stripe stores `consent: { terms_of_service: 'accepted' }` on the session — a timestamped, third-party-held record retrievable for any order.

**Prerequisite (manual, must happen first):** set the Terms of Service URL (`https://roamsystems.co.uk/policies/terms`) and Privacy Policy URL in Stripe Dashboard → Settings → Business → Public details. **Session creation fails with an API error if `consent_collection` is enabled without a ToS URL on the account.** Verify in Stripe test mode before deploying.

#### 3. Evidence in order records (`src/pages/api/webhook.ts` + `src/lib/email.ts`)

- `webhook.ts` already retrieves the full session; pass `fullSession.consent` through (no extra API call needed).
- `email.ts`: add a line to the order-confirmation email's Customer Details block: `Terms accepted at checkout: Yes (Stripe consent record)` when `consent.terms_of_service === 'accepted'`. Since `sales@roamsystems.co.uk` receives every confirmation, every order's evidence is also in the business inbox.

#### 4. Basket notice (belt and braces)

Above/near the checkout button in the basket UI: small print — "By placing an order you agree to our [Terms of Service](/policies/terms)." Non-blocking; the Stripe checkbox is the binding act.

#### 5. Design-number marking on the website (attorney-advised)

Agile IP advised in writing (12/03/2024, reporting the EU certificates) that products and associated literature should be marked with the registered design numbers, **otherwise damages recoverable in an infringement action may be reduced** (in the UK, marking defeats the innocent-infringement defence under s.24B Registered Designs Act 1949). The site currently shows no design numbers anywhere. Add a marking line to the certifications page and product detail pages (and footer small print), e.g.:

> Protected by UK Registered Designs Nos. 6266396–6266399 and EU Registered Design No. 015033319.

#### Out of scope (noted for completeness)

- A standalone countersigned **drawings-release licence letter** for trade customers requesting technical documentation (e.g. the current fabricator case) — recommended, but it is an offline business document, not a website change. Website terms apply to **new orders only**; existing orders are not retroactively bound.
- Renewal management for the existing registrations: UK designs 6266396–6266399 first renewal due **06/03/2028**; EU RCD 015033319 expires **06/09/2028** unless renewed (renewable in 5-year periods to 25 years max). Agile IP's renewals team sends reminders (confirmed in their 12/03/2024 letter); calendar backstops still recommended.
- Physical product / printed literature marking with the design numbers — same attorney advice as spec item 5, but outside website scope.

## Implementation Impact

### Code Changes Required

- `src/pages/policies/terms.astro` — full content rewrite (structure/layout pattern unchanged).
- `src/pages/api/checkout.ts` — add `consent_collection` + `custom_text` to session creation.
- `src/pages/api/webhook.ts` — no structural change; consent already present on retrieved session object passed to email.
- `src/lib/email.ts` — add consent line to Customer Details block.
- `src/pages/policies/refund.astro` — patch cancellation wording (CCR 2013 + made-to-order exemption).
- Basket UI (sidebar in `src/layouts/Layout.astro` and/or `src/pages/basket.astro`) — add small-print agreement notice near checkout button.

### New Files

None.

### Test Changes

No automated test suite exists for these routes. Verification:
1. `npm run build` passes.
2. Stripe **test mode**: create a checkout session → required ToS checkbox renders → payment blocked until ticked → completed session shows `consent.terms_of_service: 'accepted'`.
3. Webhook test event → confirmation email contains the consent line.
4. Confirm session creation succeeds (i.e. Dashboard ToS URL was set).

### Data / Migration Impact

No database (site is stateless; orders live in Stripe). No data migration. Applies to sessions created after deploy only.

## Migration Plan

No breaking changes for customers. Deployment-order requirement:

1. Owner supplies company number, registered office, VAT number for the terms page.
2. Set ToS + Privacy URLs in Stripe Dashboard (live **and** test mode).
3. Verify consent flow in test mode.
4. Deploy code (terms page + checkout consent together, one deploy).
5. Place a live £-smallest test order or verify first real order's session shows consent accepted.

Rollback: remove `consent_collection`/`custom_text` params and redeploy (one-line revert); terms page content can stay.

## Alternatives Considered

### Alternative 1: Own checkbox in the basket UI only (no Stripe consent)
- **Description**: required checkbox on our basket page before redirecting to Stripe.
- **Pros**: full UI control; no Stripe dashboard dependency.
- **Cons**: the site has no database — we'd have no durable record of who ticked what and when; a client-side flag is weak evidence; checkbox is one step removed from payment.
- **Why not chosen**: Stripe's consent record is timestamped, stored by a third party against the payment itself, and costs zero infrastructure.

### Alternative 2: Browsewrap strengthening only ("by ordering you agree…" text + footer links)
- **Description**: add notice text without any required affirmative act.
- **Pros**: trivial to implement; zero friction.
- **Cons**: courts regularly decline to enforce terms without affirmative assent; doesn't meet the owner's "signed and forms an agreement" requirement.
- **Why not chosen**: insufficient enforceability — this is the current (broken) state with more words.

### Alternative 3: E-signature (DocuSign or similar) per order
- **Description**: require a signed agreement document before/after payment.
- **Pros**: strongest evidential form.
- **Cons**: severe checkout friction; subscription cost; wholly non-standard for e-commerce product sales.
- **Why not chosen**: clickwrap is the established, enforceable standard for online sales. Reserve countersigned documents for the offline drawings-release licence (out of scope here).

## Traceability

- **Idea doc**: none (direct business requirement from owner, 2026-06-11 session — trade-customer CAD request).
- **Canonical docs**: `docs/reference/SCHEMA_AND_CONTRACTS_CANONICAL.md` (checkout/webhook/email contract section).
- **Implementation files**: `src/pages/policies/terms.astro`, `src/pages/api/checkout.ts`, `src/pages/api/webhook.ts`, `src/lib/email.ts`, `src/pages/policies/refund.astro`, basket UI (`src/layouts/Layout.astro` / `src/pages/basket.astro`).
- **Test files**: none (manual verification per Test Changes).
- **Related audits**: none active; recommend mini-audit after implementation (canonical surfaces touched).

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Session creation fails because Stripe account ToS URL not set | Medium | High (checkout down) | Set Dashboard URLs (test + live) **before** deploy; verify in test mode; rollback is a one-line revert |
| Checkout conversion dip from extra checkbox | Low | Low | Standard e-commerce practice; single tick; message kept short |
| Drafted legal wording insufficient or partially unenforceable | Medium | Medium | Clauses follow standard UK e-commerce patterns with CRA 2015/CCR 2013 carve-outs; **recommend solicitor review of final copy** — AI-drafted terms are a strong baseline, not legal advice |
| Terms not binding on orders placed before deploy (incl. current fabricator order) | Certain | Medium | Acknowledged: use standalone watermarked drawings + cover-note licence for the existing customer; website terms govern future orders |
| Owner company details (number/registered office/VAT) unavailable at build time | Low | Low | Placeholders blocked in review checklist; page ships only with real details |
| IP clause names wrong proprietor (registered designs held by Romark Holdings Ltd; site trades as Romark Engineering Ltd) | Low | Medium | UKIPO register extract confirms Holdings as proprietor (assignment effective 05/09/2023). Clause names Holdings as owner, Engineering as licensee; owner to confirm a written intra-group licence exists |

## Approval

- **Approver**: Rob di Capite ("PROCEED WITH BOTH", 2026-06-11 session)
- **Date**: 2026-06-11
- **Conditions**: Stripe Dashboard Terms of Service URL must be set before production deploy.

## Implementation Record

- **Implemented by**: Claude (AI), same session as approval
- **Date**: 2026-06-11
- **Sprint**: None — implemented directly (contained scope, ~8 files)
- **Deviations from plan**:
  - Webhook needed no change (consent arrives on the retrieved session passed to `email.ts`).
  - Certifications page already displayed the EU RCD; updated to add the previously-missing UK registered design numbers rather than creating a new section.
  - Footer also gained company number/VAT line (Companies Act display requirement) alongside the design-marking line.
  - Deployed with `[skip ci]` pending the Stripe Dashboard ToS URL (approval condition).
