---
name: mini-audit
description: Create or update a mini audit for targeted drift checks after non-trivial changes. Use after changes that touch canonical surfaces (schema, API, DB, integrations).
argument-hint: "[scope] [canonical docs to verify]"
context: fork
allowed-tools: Read, Glob, Grep, Bash
---

# /mini-audit — Targeted Drift Check

## Goal

Create or update a mini audit document to verify alignment between implementation and canonical documentation after non-trivial changes.

## Inputs

$ARGUMENTS

If no scope is provided, ask the user what was changed and which canonical docs to verify.

## Steps

### 1) Check for existing active audit

- Check `docs/audits/active/` for an existing mini audit that covers the same scope.
- If one exists: update it rather than creating a new one.
- If superseded: create a new audit.

### 2) Run deterministic checks first

- Prefer fast, deterministic checks before writing long-form audit docs.
- Run tests/build/lint as applicable.
- Record which checks passed/failed.

### 3) Create/update the audit doc

- **Template**: see `docs/audits/templates/mini-audit-template.md` for the canonical structure.
- **Filename**: `docs/audits/active/YYYY-MM-DD-<scope>-mini.md`
- **Frontmatter**: doc_type (audit), audit_type (mini), status (active), created, scope, open_p0, open_p1
- **Contents**:
  - Purpose and scope (in/out)
  - Canonical references reviewed
  - Summary (total issues, P0/P1/P2/P3 counts, assessment)
  - Issues (AUDIT-YYYY-MM-DD-### format, priority, location, canonical ref, what's wrong, fix recommendation)
  - Documentation completeness check (features/contracts shipped but undocumented?)
  - Test verification results

### 4) Update status docs

- Update `PROJECT_STATUS.md` with audit pointer and open P0/P1 count (if any).
- Update `docs/sprints/CURRENT_STATUS.md` if audit changes priorities.

### 5) Resolution

- When P0/P1 issues are resolved, move audit to `docs/audits/resolved/YYYY-MM/`.
- Update `PROJECT_STATUS.md` to reflect resolution.

## Output

1. Audit file path
2. Issues found (count by priority)
3. Assessment: Aligned | Minor drift | Significant drift
4. Status doc updates made
