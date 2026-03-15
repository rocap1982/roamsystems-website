---
name: close-session
description: End-of-session resume-fast checklist. Commits changes, writes session log, updates status docs, and ensures the repo is ready for the next session.
disable-model-invocation: true
---

# /close-session — End-of-session documentation checklist

## Goal

Keep the repo "resume fast" for the next agent/human session and shut down all local services so they don't linger.

## Steps

1. **Commit and push any changes**:
   - Review all uncommitted changes with `git status` and `git diff`
   - Stage and commit changes with a clear commit message
   - Check for unpushed commits and push to remote
   - If remote has diverged, pull/rebase first then push

2. **Confirm which workflow was used**:
   - small fix vs sprint vs audit

3. **Write a session log entry**:
   - Create/update `docs/sessions/YYYY-MM-DD.md` (append-only; 1-10 bullets is enough)
   - Link the relevant sprint doc / plan / audit (if applicable)

4. **Update `PROJECT_STATUS.md`** (rolling snapshot; overwrite-only) if:
   - priorities changed
   - the active sprint changed
   - a major decision was made
   - audit P0/P1 counts changed
   - set `latest_session_log:` to the session log you just wrote

5. **Update `docs/sprints/CURRENT_STATUS.md`** if:
   - active sprint/stage changed
   - blockers changed

   Guardrail: `CURRENT_STATUS.md` is **overwrite-only**. Do not accumulate running history there; put history in `docs/sessions/YYYY-MM-DD.md` and sprint doc Notes.

   Guardrail: Do **not** set sprint `stage: done` here — only `/review-sprint` is allowed to close a sprint.

6. **If contracts changed (or were proposed)**:
   - ensure plan exists in `docs/plans/`
   - ensure canonical docs are updated (only if approved)

7. **Check if roadmap needs updating**:
   - If work advanced a roadmap phase, update `docs/roadmap/ROADMAP.md` if it exists.
   - Update `PROJECT_STATUS.md` if the next phase or milestone changed.

8. **Decide whether a new skill should be created** or an existing skill should be updated.

9. **If you used a sprint/audit workflow**, add a short session summary (1-5 bullets) in the relevant sprint doc or audit doc.

10. **Shut down local services** (if any are running):
    - Kill any dev server processes
    - Stop any database/container services started for this session
    - Verify ports are free

## Suggested session log structure (keep it short)

- **Summary** (1-5 bullets)
- **Closed / shipped** (0-5 bullets)
- **Decisions / notes** (0-5 bullets)
- **Next / blockers** (0-5 bullets)

## Recommended verification

- If marking work "done", run tests/build checks first.
- If substantive code changes were made, verify before closing.
