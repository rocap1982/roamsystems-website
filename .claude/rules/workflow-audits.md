---
paths: ["docs/audits/**"]
---

# Workflow: Audits

Applies when working on audits, drift checks, or comparing against canonical documentation.

## Start checklist (required)

- Check `docs/audits/active/` and summarize unresolved **P0/P1** issues relevant to the task.
- Load the relevant audit skill (`mini-audit` or `in-depth-audit`) and any domain skill(s) being audited.
- If the audit touches documentation completeness, load the `documentation-governance` skill.
- Decide audit type:
  - **Mini audit**: targeted check after changes
  - **In-depth audit**: broad check for subsystem/platform

## Audit outputs (required)

- Write audit results under `docs/audits/active/` using the appropriate template.
- Use consistent issue IDs: `AUDIT-YYYY-MM-DD-###` and fix IDs `FIX-YYYY-MM-DD-###`.
- Include documentation completeness findings when relevant (features/contracts shipped but undocumented).
- When P0/P1 issues are resolved, move the audit to `docs/audits/resolved/YYYY-MM/`.

## Finish checklist

- Update `PROJECT_STATUS.md` with audit state (latest audit + open P0/P1 count).
- If audit changes priorities, update `docs/sprints/CURRENT_STATUS.md`.
