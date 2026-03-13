---
doc_type: canonical_platform_overview
status: canonical
created: 2026-03-12
last_updated: 2026-03-12
---

# Platform Overview (Canonical)

## Purpose

Roam Systems is an e-commerce website for **Romark Engineering Ltd** (Essex, UK) that sells premium M1-certified campervan furniture, seating frames, kitchen pods, storage solutions, and upholstery. The site serves as the company's digital storefront and product catalogue.

## Users and roles

- **Customers**: browse products, view gallery/certifications, submit enquiries via basket or contact form
- **Stockists/dealers**: find information on the Stockists page
- **Site admin**: manages product data via `src/data/products.json`, deploys via Railway

## System boundaries

- **In scope**: product catalogue, product detail pages, gallery, certifications, enquiry basket, contact form, policy pages, delivery information, stockists directory
- **Out of scope**: payment processing (enquiry-based), inventory management, user accounts, order tracking, Shopify admin

## Architecture (high level)

- **UI**: Astro 6 static site with Tailwind CSS v4.2
- **Build**: `astro build` → static HTML/CSS/JS
- **Hosting**: Railway (static file serving, auto-detected)
- **Product data**: `src/data/products.json` (local JSON, 9 products)
- **Product images**: Shopify CDN (`cdn.shopify.com`)
- **Gallery/cert images**: local `public/images/`
- **Form handling**: FormSubmit.co (contact + basket enquiries)
- **Cart state**: Client-side localStorage

## Core domain concepts

- **Product**: A campervan furniture item with id, name, price, category, description, features, specs, variants, and images
- **Category**: Product grouping — Frames, Kitchens, Upholstery
- **Variant**: A product configuration option (e.g. SWB/LWB, colour)
- **Basket/Cart**: Client-side collection of products the customer wants to enquire about
- **Enquiry**: A form submission (via FormSubmit.co) containing the customer's basket and contact details

## Invariants (non-negotiable behavior)

- All seating frames must display M1 certification status
- Product prices are in GBP (£)
- Product IDs are kebab-case slugs matching `products.json` entries
- Cart state persists across page navigations via localStorage
- Static site — no server-side rendering or API routes

## Pages

| Route | File | Purpose |
|-------|------|---------|
| `/` | `src/pages/index.astro` | Homepage with hero, featured products, FAQ |
| `/products` | `src/pages/products/index.astro` | Product listing with category filter |
| `/products/[id]` | `src/pages/products/[id].astro` | Product detail page |
| `/gallery` | `src/pages/gallery.astro` | 44-image product gallery |
| `/certifications` | `src/pages/certifications.astro` | Safety certification gallery |
| `/contact` | `src/pages/contact.astro` | Contact form |
| `/delivery` | `src/pages/delivery.astro` | Delivery information |
| `/stockists` | `src/pages/stockists.astro` | Dealer/stockist directory |
| `/policies/privacy` | `src/pages/policies/privacy.astro` | Privacy policy |
| `/policies/terms` | `src/pages/policies/terms.astro` | Terms and conditions |
| `/policies/refund` | `src/pages/policies/refund.astro` | Refund policy |
| `/policies/shipping` | `src/pages/policies/shipping.astro` | Shipping policy |

## Glossary

- **M1 certification**: ECE 14.09 safety standard for motor vehicle seating
- **SWB**: Short Wheel Base (van configuration)
- **LWB**: Long Wheel Base (van configuration)
- **ISOFIX**: International standard for child seat attachment points
- **CNC**: Computer Numerical Control (precision cutting method)
