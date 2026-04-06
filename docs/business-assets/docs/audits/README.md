---
doc_type: audits_readme
status: active
created: YYYY-MM-DD
---

# Audit System

Audits track **alignment between implementation and canonical documentation** and prevent drift.

## Directory structure

```
docs/audits/
├── active/                  # unresolved issues
├── resolved/YYYY-MM/        # archived audits
└── templates/
    ├── mini-audit-template.md
    └── in-depth-audit-template.md
```

## Audit types

### Mini audit

- **When**: after non-trivial changes or when canonical surfaces are touched
- **Goal**: verify a small set of high-risk points; record P0/P1 issues
 - **Also check**: documentation completeness (new features/contracts shipped are documented)

### In-depth audit

- **When**: monthly, at major milestones, or when drift is suspected
- **Goal**: comprehensive verification + remediation plan

## Operating rules

- Keep **at most one active mini** and **one active in-depth** audit at a time.
- Use issue IDs: `AUDIT-YYYY-MM-DD-###`
- Use fix IDs: `FIX-YYYY-MM-DD-###`
- Don’t paste huge command output; record only what failed and the minimal fix.

## Fast audits (deterministic checks)

Prefer fast, deterministic checks before writing long-form audit docs:

- Starter runner: `scripts/audits/run-fast.sh`
- Customize it to your repo’s real checks (lint/build/tests).

In audit writeups:
- record *which check failed*,
- *why it matters*,
- and the *minimal fix*.

