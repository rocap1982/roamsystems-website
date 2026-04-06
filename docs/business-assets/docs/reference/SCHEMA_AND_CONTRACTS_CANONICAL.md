---
doc_type: canonical_schema_contracts
status: canonical
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
---

# Schema & Contracts (Canonical)

This document is the canonical source for:

- key entities and identifiers
- required fields and constraints
- API envelope conventions (request/response + errors)
- versioning and migration policy

## Identifiers

- **Tenant ID**: [org_id/account_id] — [rules]
- **User ID**: …
- **Entity IDs**: [uuid/int] — [rules]

## Entity model (high level)

### Entity: [Name]

- **Primary key**: …
- **Required fields**: …
- **Relationships**: …
- **Constraints**: …

## API contract conventions

### Request/response envelope

Define the canonical envelope shape (if applicable):

```json
{
  "data": {},
  "error": null,
  "meta": {}
}
```

### Error model

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": {}
  }
}
```

## Versioning policy

- **Minor**: additive/backward compatible
- **Major**: breaking
- **Patch**: clarification

## Migration policy

- How schema changes are rolled out (migrations, backfills, compatibility windows)
- Rollback expectations

