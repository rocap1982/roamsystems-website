---
name: review-sprint
description: Verify a sprint and close it (tests + docs + audit/skills gates). The only workflow that should move a sprint to stage done.
argument-hint: "[optional: sprint doc path under docs/sprints/]"
---

# /review-sprint — Sprint Review (Verification + Documentation Gates)

## Goal

Run the sprint verification and documentation gates, then update sprint stage/status and resume-fast docs.

This skill is the **only** workflow that should move a sprint to `stage: done`.

## Inputs

$ARGUMENTS

If no sprint path is provided:
- Read `docs/sprints/CURRENT_STATUS.md` and use `active_sprint`.

Optional flag:
- `--deep` enables heavyweight review using parallel reviewer subagents.

## What this skill owns (no crossover)

- **Verification**: execute the sprint's test plan (automated + manual) and record results.
- **Documentation**: ensure canonical documentation is updated (only if approved when required).
- **Audit + skills decision**: ensure audit state is correct and decide whether a new skill is required.

## Steps

### 0) Load scope

- Read:
  - the sprint doc (argument or `docs/sprints/CURRENT_STATUS.md#active_sprint`)
  - `docs/sprints/CURRENT_STATUS.md`
  - `PROJECT_STATUS.md`
  - `docs/audits/active/` (only if sprint touched canonical surfaces)

If `--deep` is enabled:
- Run parallel reviewer subagents and synthesize findings before proceeding:
  - `architecture-reviewer`
  - `security-reviewer`
  - `performance-reviewer`
  - `data-integrity-reviewer`
  - `test-quality-reviewer`
  - `docs-governance-reviewer`

### 1) Verification (required)

Use the sprint doc's **Test plan** section as the source of truth.

- Run every **Automated** command listed there (tests/lint/typecheck/build as specified).
- Execute the **Manual** checklist and record results.

If the sprint doc is missing automated commands, fall back to standard verification:
- lint, typecheck, test, build (as appropriate for your project)

If anything fails:
- Update sprint `stage: verification` and record blockers in the sprint doc and `docs/sprints/CURRENT_STATUS.md`.
- Stop after documenting what failed and what remains.

### 2) Documentation gates (required when behavior/contracts changed)

Use the sprint doc's **Documentation DoD** as the source of truth.

- If behavior/contracts changed:
  - Load the `documentation-governance` skill
  - Update the correct canonical docs
  - If a contract-impacting change occurred, confirm a plan exists in `docs/plans/` and is approved
  - Do not edit canonical docs unless the plan is approved

### 3) Audit system sync (only when canonical surfaces are touched)

- Ensure a mini audit exists/updated under `docs/audits/active/` when the sprint touched canonical surfaces.
- Ensure the audit includes:
  - canonical refs reviewed
  - issues (if any)
  - testing performed

### 4) Learnings capture (required)

Review the sprint for reusable knowledge before it's lost.

- **Architectural decisions**: record mid-sprint design choices (e.g., "chose X over Y because Z") in the sprint doc Notes section.
- **Patterns discovered**: note new patterns that future work should follow. Examples: a standard integration flow, a data-channel relay pattern, a configuration-over-code approach.
- **Pitfalls encountered**: document anything harder than expected or that caused rework, even if it didn't require a `/compound` entry.

Keep it brief (3-7 bullets max). The goal is to make the *next* sprint in this area faster.

### 5) Skills decision (required)

Decide whether a new skill should be created/updated.

- **Check the sprint doc first**: look for any explicit skill-creation tasks in the sprint. These are requirements, not suggestions.
- If the sprint doc requests a skill: create it.
- If the work introduced a new reusable procedure, repeated pitfall, or standardized pattern worth codifying (even if the sprint doc didn't ask): create or update the relevant `.claude/skills/<skill>/SKILL.md`.
- If neither applies: explicitly record "no skill change" in the sprint Notes.

### 6) Plan/idea review (required when sprint originated from a plan or idea)

If the sprint was born from an approved plan (`docs/plans/`) or idea doc (`docs/ideas/`):

- Compare the outcome against the original vision. Did we build what we planned?
- Note any scope changes, deferred items, or new ideas that emerged.
- Update the source plan/idea doc status if appropriate (e.g., mark phases as complete, add "emerged during Sprint X" notes).

### 7) Optional: Solutions compounding (/compound)

If a non-obvious issue was solved (debugging required, likely to recur), run `/compound` after review to write a solution entry under `docs/solutions/`.

### 8) Close-out updates (required)

- In the sprint doc:
  - ensure acceptance criteria and verification/doc/audit checkboxes are accurate
  - set `stage: done` only when all gates pass
- In `docs/sprints/CURRENT_STATUS.md`:
  - update stage and priorities/blockers
- In `PROJECT_STATUS.md`:
  - update `last_updated` and reflect current active work if it changed

## Output

At the end, provide:

1. Sprint path reviewed
2. Stage before -> after
3. Verification summary (what ran, what passed/failed)
4. Learnings captured (key decisions, patterns, pitfalls - 3-7 bullets)
5. Skills outcome (created/updated/no change - with file links if applicable)
6. Plan/idea alignment (matched / scope changed / deferred items noted)
7. Docs/audit outcomes (with file links)
