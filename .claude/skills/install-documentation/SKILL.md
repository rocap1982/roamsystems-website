---
name: install-documentation
description: Install the canonical documentation set (one-time during FBS setup). Creates the source-of-truth reference docs under docs/reference/.
disable-model-invocation: true
---

# /install-documentation — Install Canonical Documentation Set

## Goal

Create or confirm the canonical documentation set under `docs/reference/`. This is a one-time setup during FBS installation.

## Steps

### 1) Check existing docs

- Check `docs/reference/` for existing canonical docs.
- Report what exists and what's missing.

### 2) Create/confirm the canonical set

Produce the following documents (start with the first, end with the last):

1. `docs/reference/DOCUMENTATION_STANDARDS_CANONICAL.md` — governs all canonical docs (declarative tone, schema+example+semantics, no silent field introduction)
2. `docs/reference/DOCUMENTATION_HIERARCHY_CANONICAL.md` — source-of-truth precedence stack
3. `docs/reference/PLATFORM_OVERVIEW_CANONICAL.md` — what the platform is, users, architecture, invariants
4. `docs/reference/SCHEMA_AND_CONTRACTS_CANONICAL.md` — entity model, API contracts, error model, versioning
5. `docs/reference/DOCUMENTATION_INVENTORY.md` — what docs exist, what's missing, what's out of scope
6. `docs/reference/GLOBAL_TERMINOLOGY_INDEX_CANONICAL.md` — authoritative term definitions

### 3) Rules

- Document what exists (don't invent).
- Raise gaps as plans, not as assumptions.
- Keep canonical docs declarative (state what is, not what to do).
- Use schema + example + semantics for all operational structures.

## Output

1. List of docs created/confirmed
2. Any gaps identified
3. Recommendations for next steps
