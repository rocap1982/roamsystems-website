<!-- Foundation rules: where to find context, how to load skills, and non-negotiable governance. -->

# Foundation (Always Apply)

This repository uses **progressive disclosure** for AI context:

- **Project state**: read `PROJECT_STATUS.md` first (fast, low token).
- **Session history**: read the latest log under `docs/sessions/` (see `PROJECT_STATUS.md#latest_session_log`).
- **Current work**: read `docs/sprints/CURRENT_STATUS.md`.
- **Skills**: load only the relevant `.claude/skills/*/SKILL.md`.
- **Audits**: check `docs/audits/active/` for unresolved P0/P1 drift relevant to your task.

## Non-negotiables

- **Governance**: if a change impacts canonical contracts (schemas/API/DB/business rules), create a plan and wait for explicit approval before implementing.
- **Don't bloat context**: prefer loading a small number of relevant skills rather than broad repo-wide reading.

## Required session checkpoints

At the start of meaningful work:
- State which "current status" docs you used (prefer `PROJECT_STATUS.md` + `docs/sprints/CURRENT_STATUS.md`).
- State which skill(s) you loaded (by directory name).

At the end of a session:
- State whether a new skill should be created/updated (yes/no + rationale).
- State whether an audit/plan/sprints update is required (yes/no + which file).
