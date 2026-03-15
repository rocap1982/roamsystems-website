---
name: documentation-governance
description: Canonical documentation rules and update workflow. Use when implementing features that change behavior, schema, API, or DB contracts, or when updating canonical docs in docs/reference/.
user-invocable: false
---

# Documentation Governance

## Canonical references (must be followed)

- Documentation standards: `docs/reference/DOCUMENTATION_STANDARDS_CANONICAL.md`
- Documentation hierarchy: `docs/reference/DOCUMENTATION_HIERARCHY_CANONICAL.md`

## Non-negotiables

- Do not introduce new fields, enums, or behaviors silently.
- Do not duplicate or redefine schemas across multiple documents.
- When a change is contract-impacting, create a plan in `docs/plans/` and wait for approval before updating canonical contracts.

## Drafting rules (for canonical/spec docs)

- Use declarative specification tone (state what is, not what to do).
- For operational structures, include **Schema + Example + Semantics**.
- Examples must be valid and match the schema exactly.
- Preserve existing wording unless explicitly instructed to change it.
- Operational docs (sprints/audits/plans) are out of scope for these standards.

## Ongoing documentation workflow (per sprint)

- [ ] Identify what changed (feature behavior, schema/API/DB/integrations).
- [ ] Locate the correct canonical doc per the documentation hierarchy.
- [ ] If a contract changed:
  - [ ] Create/ensure a plan exists in `docs/plans/`
  - [ ] Wait for approval (if required by repo governance)
- [ ] Update or create the minimal necessary doc sections (no cross-document leakage).
- [ ] Add a documentation checklist item in the sprint doc.
- [ ] Before sprint stage -> `done`:
  - [ ] Confirm documentation completeness (new behavior and schema are documented)

## Common pitfalls

- **Pitfall**: Writing instructions ("should", "recommended") into canonical docs.
  - **Fix**: Move guidance into skills; keep canonical docs declarative.
- **Pitfall**: Adding an example field not present in schema.
  - **Fix**: Raise a gap and require explicit approval before adding any new field.
