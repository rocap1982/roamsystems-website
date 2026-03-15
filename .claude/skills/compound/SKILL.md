---
name: compound
description: Capture a solved problem as a solution entry with prevention steps. Use after solving a non-obvious problem (debugging required, likely to recur) to compound knowledge.
argument-hint: "[optional: brief context about the solved problem]"
---

# /compound — Document a Solved Problem (Solutions Library)

## Goal

Create a solution entry under `docs/solutions/` for a non-obvious problem that was solved and verified.

This is not canonical documentation. It is a "solved problem" record with prevention.

## Inputs

$ARGUMENTS

If no context is provided, infer from the most recent sprint work and the latest session log under `docs/sessions/`.

## Rules (anti-staleness)

- Do not write a solution for trivial fixes.
- Every solution must include:
  - `last_verified` (today)
  - a fix reference (PR or commit SHA)
  - a prevention step (test, invariant, or repeatable check)
- If the solution is no longer valid, prefer `status: deprecated` rather than deleting history.

## Steps

### 0) Gather evidence (required)

- Identify the solved problem:
  - symptom (error text or user-visible behavior)
  - root cause
  - fix
  - verification performed
- Identify references:
  - sprint doc (if applicable)
  - plan/audit links (if applicable)
  - commit SHA / PR link (if applicable)

### 1) Choose category + filename

Pick a category folder under `docs/solutions/` (create if needed):
- build-errors, test-failures, runtime-errors, performance, database, security, ui, integrations, other

Filename format: `docs/solutions/<category>/YYYY-MM-DD-<short-slug>.md`

### 2) Create the solution doc

- Use the template: `docs/solutions/templates/solution-template.md`
- Fill frontmatter: `status: active`, dates, references, tags
- Fill sections:
  - Symptom (copy/paste error text if possible)
  - Root cause (explain precisely)
  - Fix (what changed + why it works)
  - Prevention (tests/invariants)
  - Canonical impact (if drift revealed, link relevant canonical docs)

### 3) Promotion check (skill vs solution)

If the solution represents a reusable procedure (not just a one-off incident):
- create/update a `.claude/skills/<skill>/SKILL.md`
- set `superseded_by` in the solution to point to that skill

## Output

1. Solution file path created
2. Category selected
3. Prevention step captured (test/invariant)
4. Whether a skill was created/updated
