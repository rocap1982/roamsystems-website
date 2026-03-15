---
doc_type: idea
status: draft
created: 2026-03-13
last_updated: 2026-03-13
owner: "Robert DiCapite"
tags: [sage, accounting, stripe, integration, oauth, invoicing]
related_plans: []
related_sprints: []
---

# Idea: Direct Sage Business Cloud Accounting Integration

## Summary

Replace the planned Amaka bridge with a direct API integration between Stripe and Sage Business Cloud Accounting. When a Stripe checkout completes, the existing webhook automatically creates a contact, sales invoice, and payment record in Sage — providing full accounting sync without a third-party intermediary.

## Problem / Opportunity

### Current State

- Stripe Checkout is fully integrated (Sprint 1 + 2 complete)
- Webhook at `POST /api/webhook` handles `checkout.session.completed` events
- Webhook currently sends confirmation emails via Resend only
- No accounting sync exists — Amaka was planned but not yet configured
- All order data is available in the webhook (line items, customer, shipping, VAT)

### Desired State

- Every completed Stripe payment automatically creates records in Sage:
  1. **Contact** (customer) — matched by email, created if new
  2. **Sales invoice** — with line items, VAT, and shipping
  3. **Contact payment** — linked to the invoice and a designated "Stripe" bank account
- Invoices appear in Sage ready for bank reconciliation
- Failed syncs are logged and retryable without blocking the Stripe webhook response

### Why This Matters

- Manual invoice entry is error-prone and time-consuming
- Direct integration gives full control over field mapping and error handling
- Eliminates dependency on Amaka (third-party service outside Roam's control)
- Enables future features: credit notes, refund sync, reporting

## Constraints

- **Sage API rate limits**: 100 requests/min, 2,500/day per company — adequate for expected order volume
- **OAuth token rotation**: Refresh tokens rotate on every use; must persist the new token atomically
- **No official Node.js SDK**: Must build a thin REST client using `fetch`
- **Railway ephemeral containers**: Token storage requires a persistent volume
- **Sage API v3.1**: Current stable version; base URL `https://api.accounting.sage.com/v3.1`
- **GBP only**: All transactions in pounds sterling (matches existing Stripe config)
- **Single Sage business**: No multi-tenant requirements

## Architecture / Approach

### OAuth 2.0 Flow

1. **One-time setup**: Admin visits `/api/sage/auth` → redirected to Sage login → grants access → callback at `/api/sage/callback` stores tokens
2. **Token storage**: JSON file on a Railway persistent volume (`/data/sage-tokens.json`)
3. **Auto-refresh**: Before each API call, check token expiry; refresh if needed; store new refresh token atomically

**New API routes:**
- `GET /api/sage/auth` — initiates OAuth flow (admin-only, one-time setup)
- `GET /api/sage/callback` — handles OAuth callback, stores tokens
- `GET /api/sage/status` — health check (token valid? last sync time?)

**New env vars:**
- `SAGE_CLIENT_ID` — from Sage developer portal
- `SAGE_CLIENT_SECRET` — from Sage developer portal
- `SAGE_REDIRECT_URI` — callback URL (e.g., `https://roamsystems.co.uk/api/sage/callback`)
- `SAGE_BUSINESS_ID` — target business (discovered after first auth, then stored)
- `SAGE_BANK_ACCOUNT_ID` — the Sage bank account representing Stripe payments
- `SAGE_DEFAULT_LEDGER_ACCOUNT_ID` — default sales ledger account for all products
- `SAGE_DEFAULT_TAX_RATE_ID` — standard UK VAT rate ID in Sage

### Sage API Client (`src/lib/sage.ts`)

Thin wrapper over `fetch` with:
- Automatic token refresh (with rotation handling)
- Rate-limit retry (exponential backoff on HTTP 429)
- Typed request/response interfaces
- Methods: `findOrCreateContact()`, `createSalesInvoice()`, `createContactPayment()`

### Webhook Integration

Extended `checkout.session.completed` handler in `/api/webhook`:

```
1. [existing] Send confirmation email via Resend
2. [new]      Sync to Sage:
              a. Find or create contact (match by customer email)
              b. Create sales invoice (map line items → single ledger account, apply VAT)
              c. Create contact payment (link to invoice + Stripe bank account)
              d. Store sync result (Stripe payment ID → Sage invoice ID)
```

**Error handling**: Sage sync failures are logged but do not block the webhook 200 response (same pattern as email). Stripe event ID is stored as the invoice `reference` for idempotency.

### Product-to-Sage Mapping

- **Single default sales ledger account** for all products (configurable via env var)
- **Standard UK VAT rate** applied to all items (configurable via env var)
- **Shipping** posted as a separate invoice line if present
- **No per-product mapping needed** at this stage

### Sync Status Tracking

- JSON file on Railway volume: `/data/sage-sync-log.json`
- Maps `stripeEventId → { sageContactId, sageInvoiceId, sagePaymentId, syncedAt, error? }`
- Enables idempotency checks on webhook retries
- Simple enough to migrate to a DB later if needed

### File Structure (New)

```
src/
  lib/
    sage.ts              — Sage API client (auth, contacts, invoices, payments)
  pages/
    api/
      sage/
        auth.ts          — OAuth initiation (GET, admin-only)
        callback.ts      — OAuth callback (GET, stores tokens)
        status.ts        — Health check (GET)
      webhook.ts         — Modified: add Sage sync after email
```

## Non-goals

- **Multi-tenant Sage support** — single business account only
- **Sage → Stripe sync** — no polling Sage for changes (one-way push only)
- **Refund/credit note sync** — future enhancement, not in initial scope
- **Per-product ledger mapping** — all products to one sales account
- **Admin UI for Sage config** — env vars and one-time OAuth flow are sufficient
- **Amaka integration** — replaced by this direct integration

## Open Questions

1. **Railway volume setup**: Need to verify Railway volume configuration and mount path for token persistence
2. **Sage developer app registration**: Who registers the app at developer.sage.com? (Likely Robert or Romark's Sage admin)
3. **Sage bank account**: Does a "Stripe Payments" bank account already exist in Sage, or does one need to be created?
4. **Sage ledger account ID**: Which specific sales ledger account should all online orders post to?
5. **VAT handling**: Does Sage's tax rate need to match Stripe's `automatic_tax` calculation exactly, or is Stripe's amount authoritative?
6. **Retry strategy**: Should failed Sage syncs be retried automatically (e.g., via a scheduled task), or is manual re-sync sufficient for the expected low order volume?

## Traceability

Canonical docs that would be impacted:
- `docs/reference/PLATFORM_OVERVIEW_CANONICAL.md` — new integration, env vars, system boundary
- `docs/reference/SCHEMA_AND_CONTRACTS_CANONICAL.md` — new API contracts (sage/auth, sage/callback, sage/status), modified webhook contract
- `docs/reference/GLOBAL_TERMINOLOGY_INDEX_CANONICAL.md` — new terms (Sage Contact, Sales Invoice, Contact Payment, Ledger Account)
