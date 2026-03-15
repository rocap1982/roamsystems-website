<!-- Applies to all small fix/refactor/tweak tasks that don't require a sprint plan. -->

# Workflow: Small Fixes

Applies when the task is a small fix/refactor/UI tweak that does not require a sprint plan.

## Start checklist

- Confirm scope is "small fix" (1-3 files, limited blast radius).
- Load only the needed skill(s).
- If the change might impact canonical contracts, switch to the **plan workflow** instead.

## Implementation checklist

- Keep diffs small and localized.
- Prefer existing patterns.
- Avoid creating new documentation unless it's truly reusable reference.

## Finish checklist

- State what changed (files).
- State how verified (tests/build/manual).
- If priorities/status changed, update `PROJECT_STATUS.md` and/or `docs/sprints/CURRENT_STATUS.md`.
