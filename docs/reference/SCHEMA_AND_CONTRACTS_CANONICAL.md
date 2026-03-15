---
doc_type: canonical_schema_contracts
status: canonical
created: 2026-03-12
last_updated: 2026-03-13
---

# Schema & Contracts (Canonical)

This document is the canonical source for data structures and contracts in the Roam Systems website.

## Product schema (`src/data/products.json`)

The product catalogue is a JSON array. Each product object:

### Entity: Product

- **Primary key**: `id` (string, kebab-case slug — e.g. `"m1-certified-u-shape-seating-frame"`)
- **Required fields**:
  - `id`: string — unique slug, used in URL routing (`/products/[id]`)
  - `name`: string — display name
  - `price`: number — current price in GBP
  - `compareAtPrice`: number | null — original/comparison price (null if no discount)
  - `category`: string[] — one or more of: `"Frames"`, `"Kitchens"`, `"Upholstery"`
  - `tags`: string[] — searchable labels
  - `description`: string — product description text
  - `features`: string[] — bullet-point feature list
  - `specs`: object — key-value specification pairs (keys and values are strings)
  - `variants`: array of `{ title: string, price: number }`
  - `images`: string[] — URLs (currently Shopify CDN)
- **Constraints**:
  - `id` must be unique across all products
  - `id` must be a valid URL slug (lowercase, hyphens only)
  - `price` must be > 0
  - `category` must contain at least one valid category
  - `variants` must contain at least one entry
  - `images` must contain at least one URL

### Valid categories

| Category | Description |
|----------|-------------|
| `Frames` | Seating frames, storage drawers, panels |
| `Kitchens` | Kitchen pods, overhead lockers, packages |
| `Upholstery` | Upholstery kits, cushion boards, foam |

## API contracts

### `POST /api/checkout`

Creates a Stripe Checkout session for standard products.

- **Request body**: `{ items: [{ stripePriceId: string, qty: number }] }`
- **Response (200)**: `{ url: string }` — Stripe hosted checkout URL
- **Response (4xx/5xx)**: `{ error: string }`
- **Session params**: `shipping_address_collection` (GB only), `automatic_tax` (enabled), `customer_creation` (always), `shipping_options` (from `STRIPE_SHIPPING_RATE_ID` env var)
- **Success redirect**: `/checkout/success?session_id={CHECKOUT_SESSION_ID}`
- **Cancel redirect**: `/checkout/cancel`

### `POST /api/webhook`

Stripe webhook endpoint for post-payment processing.

- **Request body**: Raw Stripe event payload (signature verified via `STRIPE_WEBHOOK_SECRET`)
- **Response (200)**: `{ received: true }`
- **Handled events**: `checkout.session.completed` — retrieves full session (with line_items, shipping_cost expanded), sends confirmation email via Resend
- **Idempotency**: Stripe event ID passed as `X-Entity-Ref-ID` header to Resend for deduplication
- **Error handling**: Email failures return 200 (prevents Stripe retries for transient errors)

### `POST /api/contact`

Server-side form submission endpoint (replaces FormSubmit.co).

- **Request body**: `{ type: "contact" | "enquiry", name: string, email: string, phone?: string, subject?: string, message?: string, basketItems?: string, basketTotal?: string }`
- **Response (200)**: `{ success: true }`
- **Response (4xx/5xx)**: `{ error: string }`
- **Email**: Sent via Resend to `sales@roamsystems.co.uk` with reply-to set to submitter's email

## Form contracts

### Enquiry submission (basket)

- **Endpoint**: `POST /api/contact` (type: `"enquiry"`)
- **Method**: POST (JSON via fetch)
- **Fields**: name, email, phone, message, basketItems (text summary), basketTotal

### Contact form

- **Endpoint**: `POST /api/contact` (type: `"contact"`)
- **Method**: POST (JSON via fetch)
- **Fields**: name, email, phone, subject, message

## Cart contract (localStorage)

- **Key**: stored in browser localStorage
- **Shape**: array of `{ id, name, price, quantity, variant, image }`
- **Persistence**: survives page navigation, cleared on explicit user action

## Image contracts

- **Product images**: Shopify CDN URLs (`cdn.shopify.com/s/files/...`)
- **Gallery images**: local `/images/gallery/roam-gallery-{01-44}.jpg`
- **Certification images**: local `/images/certs/`
- **Logo**: local `/images/roam-systems-logo.png`
