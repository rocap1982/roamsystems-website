---
doc_type: canonical_schema_contracts
status: canonical
created: 2026-03-12
last_updated: 2026-03-12
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

## Form contracts

### Enquiry submission (basket)

- **Endpoint**: FormSubmit.co
- **Method**: POST
- **Fields**: customer name, email, phone, basket contents (product names, quantities, variants)

### Contact form

- **Endpoint**: FormSubmit.co
- **Method**: POST
- **Fields**: name, email, subject, message

## Cart contract (localStorage)

- **Key**: stored in browser localStorage
- **Shape**: array of `{ id, name, price, quantity, variant, image }`
- **Persistence**: survives page navigation, cleared on explicit user action

## Image contracts

- **Product images**: Shopify CDN URLs (`cdn.shopify.com/s/files/...`)
- **Gallery images**: local `/images/gallery/roam-gallery-{01-44}.jpg`
- **Certification images**: local `/images/certs/`
- **Logo**: local `/images/roam-systems-logo.png`
