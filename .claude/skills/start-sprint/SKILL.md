---
name: start-sprint
description: Start implementing a sprint work plan (execution only, no verification gates). Use when ready to begin coding against a sprint doc. Supports parallel sub-agent execution by domain.
argument-hint: "[optional: sprint doc path under docs/sprints/]"
---

# /start-sprint — Execute a Sprint (Implementation Only)

## Goal

Start implementing the sprint work plan and keep the sprint doc up to date.

This skill does not run the sprint verification gates and does not move a sprint to `stage: done`. Use `/review-sprint` for verification + documentation + close-out.

## Inputs

$ARGUMENTS

If no sprint path is provided:
- Read `docs/sprints/CURRENT_STATUS.md` and use `active_sprint`.

## Steps

### 0) Load scope

- Read:
  - the sprint doc (argument or `docs/sprints/CURRENT_STATUS.md#active_sprint`)
  - `docs/sprints/CURRENT_STATUS.md`
  - `PROJECT_STATUS.md`

### 1) Confirm stage transition (planning -> in_progress)

- If sprint is `stage: planning`, set it to `stage: in_progress`.
- Update `docs/sprints/CURRENT_STATUS.md#stage` accordingly.

### 2) Execute the work plan

- Convert sprint **Work plan** tasks into an explicit task list.
- Implement tasks in a logical order (DB -> API -> UI -> tests scaffolding -> docs scaffolding).
- When tasks are tagged by domain (`[DB]`, `[API]`, `[UI]`, etc.), independent tracks can be executed in parallel using sub-agents. Group non-overlapping domain tasks and delegate to parallel sub-agents where possible.
- Update the sprint doc continuously:
  - move tasks from To do -> In progress -> Done
  - record key decisions in Notes

### 3) Testing while implementing (allowed, not the gate)

- Run targeted checks as needed while implementing to avoid accumulating failures.
- Standard verification commands (adapt to your project):
  - lint
  - typecheck
  - test
  - build (only if relevant to the sprint)
- Scoped checks are fine when only one area is being changed.
- Do not treat this as "verification complete".

### 4) Handoff to code review and verification

When implementation is functionally complete:
- Update sprint stage to `verification`.
- Run `/check-sprint` for a deep code review of the implementation.
- Fix any P0/P1 issues found by `/check-sprint`.
- Run `/review-sprint` to execute the verification + documentation gates and close the sprint.

## Output

1. Sprint path being executed
2. Stage before -> after
3. What was completed in this run
4. What remains
