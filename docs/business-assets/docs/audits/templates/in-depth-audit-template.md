---
doc_type: audit
audit_type: in_depth
status: active # active | resolved | superseded
created: YYYY-MM-DD
auditor: "AI (Claude Code)"
scope: ""
open_p0: 0
open_p1: 0
---

# In-Depth Audit Result: [Subsystem / Platform] — [YYYY-MM-DD]

## Purpose

This in-depth audit provides comprehensive verification of alignment between implementation and canonical specs.

## Scope

- **Components audited**: [list]
- **Out of scope**: [list]

## Canonical references reviewed

- `docs/reference/<doc>.md` (sections …)

## Summary

- **Total issues**: 0
- **P0**: 0
- **P1**: 0
- **P2**: 0
- **P3**: 0
- **Assessment**: ✅ Well aligned | ⚠️ Minor drift | ❌ Significant drift

## Issues (by priority)

### P0

#### AUDIT-YYYY-MM-DD-001

- **Location**: `path/to/file`
- **Canonical ref**: `docs/reference/<doc>.md#<section>`
- **Details**: …
- **Fix**: …
- **Testing required**: …

### P1

#### AUDIT-YYYY-MM-DD-002

[same structure]

### P2 / P3

[same structure]

## Remediation plan

### FIX-YYYY-MM-DD-001

- **Issues covered**: AUDIT-YYYY-MM-DD-001
- **Steps**:
  1. …
  2. …
- **Tests**:
  - …
- **Risk**: Low | Medium | High

## Verification checklist

- [ ] Build/lint clean
- [ ] Automated tests run and passing
- [ ] Manual checks completed for core flows
- [ ] Canonical docs updated (if approved and applicable)

## Close-out

If resolved:

- Move this file to `docs/audits/resolved/YYYY-MM/`
- Update `PROJECT_STATUS.md` and `docs/sprints/CURRENT_STATUS.md` if priorities changed

