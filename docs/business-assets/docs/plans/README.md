# Plans

Formal plan documents for contract-impacting changes. Plans require explicit approval before implementation.

## When a plan is required

- Database schema changes (tables, columns, constraints, migrations)
- API contract changes (endpoints, request/response shapes, error envelopes)
- Integration contract changes (external payloads, webhooks, partner APIs)
- Canonical business rule changes

## When a plan is NOT required

- Internal refactors with no contract change
- Bug fixes restoring compliance with existing specs

## Workflow

1. Create plan via `/new-plan`
2. Review via `/review-plan-doc`
3. Get explicit approval
4. Create sprint via `/new-sprint`
5. Implement and update canonical docs
6. Mark plan as "Implemented"

## Template

See `plan-template.md` in this directory.
