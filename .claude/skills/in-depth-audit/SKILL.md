---
name: in-depth-audit
description: Create or update an in-depth audit for comprehensive subsystem verification. Use monthly, at major milestones, or when drift is suspected.
argument-hint: "[scope] [target date range or sprint context]"
context: fork
allowed-tools: Read, Glob, Grep, Bash
---

# /in-depth-audit — Comprehensive Subsystem Audit

## Goal

Create or update an in-depth audit document for comprehensive verification of a subsystem against canonical documentation, with a full remediation plan.

## Inputs

$ARGUMENTS

If no scope is provided, ask the user what subsystem to audit and the date range.

## Steps

### 1) Check for existing active audit

- Check `docs/audits/active/` for an existing in-depth audit that covers the same scope.
- At most one active in-depth audit should exist at a time.

### 2) Run deterministic checks first

- Prefer fast, deterministic checks before writing long-form audit docs.
- Record results.

### 3) Create/update the audit doc

- **Template**: see `docs/audits/templates/in-depth-audit-template.md` for the canonical structure.
- **Filename**: `docs/audits/active/YYYY-MM-DD-<scope>-in-depth.md`
- **Frontmatter**: doc_type (audit), audit_type (in_depth), status (active), created, scope, open_p0, open_p1
- **Contents**:
  - Purpose and scope (components audited, out of scope)
  - Canonical references reviewed
  - Summary (total issues, P0/P1/P2/P3 counts, assessment)
  - Issues by priority (P0, P1, P2/P3) with AUDIT-YYYY-MM-DD-### IDs
  - Remediation plan (FIX-YYYY-MM-DD-### IDs, steps, tests, risk level)
  - Verification checklist (build/lint clean, tests passing, manual checks, canonical docs updated)

### 4) Update status docs

- Update `PROJECT_STATUS.md` with audit pointer and open P0/P1 counts.
- Update `docs/sprints/CURRENT_STATUS.md` if audit changes priorities.

### 5) Close-out

- When all issues resolved, move to `docs/audits/resolved/YYYY-MM/`.
- Update `PROJECT_STATUS.md` and `docs/sprints/CURRENT_STATUS.md`.

## Output

1. Audit file path
2. Issues found (count by priority)
3. Remediation plan summary
4. Assessment: Aligned | Minor drift | Significant drift
