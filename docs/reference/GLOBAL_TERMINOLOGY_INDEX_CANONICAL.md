---
doc_type: canonical_global_terminology_index
status: canonical
created: 2026-03-12
last_updated: 2026-03-13
---

# Global Terminology Index (Canonical)

This document defines the authoritative set of terms and definitions used across the repository.

## Product & Engineering Terms

- **M1 tested**: The rear belted travel seat of the U-shape frame was independently pull tested by VOSC for seat belt anchorage strength to the M1 load requirements of ECE R14.09 (test VO00269, 18/03/2021), and its ISOFIX anchorages to ECE R145 (test VO00270, 23/03/2021). Static pull tests on a steel plate test structure — not in a vehicle, not crash tests. Side bench sections are untested and for stationary use only. Do not use "M1 certified", "crash tested" or "approved installer".
- **ISOFIX**: International standard (ISO 13216) for child seat attachment points integrated into vehicle seating.
- **CNC**: Computer Numerical Control — precision manufacturing method used for cutting plywood and aluminium components.
- **SWB**: Short Wheel Base — a van body length configuration (e.g. VW T5/T6 SWB).
- **LWB**: Long Wheel Base — a van body length configuration (e.g. VW T5/T6 LWB).
- **Powder coat**: A durable textured black finish applied to aluminium and steel components.
- **Phenolic plywood**: High-density plywood used for structural panels (front panels, lids).
- **Birch plywood**: Plywood used for cushion boards and non-structural components.
- **Dual density foam**: Two-layer cushion construction (25mm soft blue + 25mm firm chip foam).

## Business Terms

- **Romark Engineering Ltd**: The parent company behind the ROAM Systems brand, based in Essex, UK.
- **ROAM Systems**: The consumer-facing brand name.
- **Stockist**: An authorised dealer or retailer who sells ROAM products.
- **Enquiry**: A customer request submitted via the basket or contact form (not a direct purchase).
- **Basket**: The client-side cart used to collect products for enquiry submission.

## Technical Terms

- **Product ID**: A kebab-case slug uniquely identifying a product (e.g. `m1-certified-u-shape-seating-frame`). Used as URL path and data key.
- **Category**: A product classification — one of `Frames`, `Kitchens`, or `Upholstery`.
- **Variant**: A selectable product configuration (e.g. SWB/LWB, colour).
- **Resend**: Transactional email API used for order confirmation emails and form submission notifications. Replaces FormSubmit.co.
- **Stripe Checkout**: Hosted payment page for processing card payments. Sessions created server-side via `POST /api/checkout`.
- **Stripe Tax**: Automatic tax calculation service. Enabled on checkout sessions to calculate UK VAT (20%).
- **Stripe Webhook**: Server endpoint (`POST /api/webhook`) that receives Stripe event notifications (e.g. `checkout.session.completed`) for reliable post-payment processing.
- **Idempotency key**: A unique identifier (Stripe event ID) passed via `X-Entity-Ref-ID` header to Resend to prevent duplicate email sends on webhook retries.
- **Shopify CDN**: Content delivery network hosting product images (`cdn.shopify.com`).

## EU Design Registration

- **RCD 015033319**: The EU Registered Community Design number for ROAM's U-shape seating frame, registered with EUIPO.
