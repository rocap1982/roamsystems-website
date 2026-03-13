---
doc_type: documentation_inventory
status: active
created: 2026-03-12
last_updated: 2026-03-13
---

# Documentation Inventory

This document records what documentation exists, what is missing, and what is explicitly out of scope for the current documentation installation.

## Canonical set (required)

- Documentation Standards: `docs/reference/DOCUMENTATION_STANDARDS_CANONICAL.md` — status: present
- Documentation Hierarchy: `docs/reference/DOCUMENTATION_HIERARCHY_CANONICAL.md` — status: present
- Platform Overview: `docs/reference/PLATFORM_OVERVIEW_CANONICAL.md` — status: present
- Schema & Contracts: `docs/reference/SCHEMA_AND_CONTRACTS_CANONICAL.md` — status: present
- Global Terminology Index: `docs/reference/GLOBAL_TERMINOLOGY_INDEX_CANONICAL.md` — status: present
- Documentation Inventory: `docs/reference/DOCUMENTATION_INVENTORY.md` — status: present (this document)

## Missing (to be created later)

- API contract docs — not needed until server-side API routes are added (currently static site with FormSubmit.co)
- Database contract docs — not needed until a database is introduced (currently JSON file + localStorage)

## Out of scope (explicit)

- Shopify admin documentation — product data is managed via local JSON, not Shopify APIs
- FormSubmit.co internal documentation — third-party service, not owned by this project
- Railway platform documentation — deployment platform, referenced but not documented here
