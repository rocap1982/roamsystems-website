---
name: start-session
description: Start a working session by reviewing project status, active sprint, and blockers. Use at the beginning of any work session to get oriented.
---

# /start-session — Start session with status review

## Goal

Start a new working session by reviewing the current project status and providing a summary of where things stand.

## Steps

### 1. Review project status

- Read `PROJECT_STATUS.md` to understand:
  - Current active work (sprint/phase)
  - Latest session log (see `latest_session_log:`)
  - Any active audits or blockers
  - Latest architectural decisions

### 2. Review current sprint status

- Read `docs/sprints/CURRENT_STATUS.md` to understand:
  - Active sprint and stage
  - This week's priorities
  - Blockers

### 3. Check for active audits

- Check `docs/audits/active/` for any unresolved P0/P1 issues that need attention.

### 4. Summarize status in chat

Write a brief summary for the user including:

**Project status**:
- What sprint/phase is currently active
- The next 1-3 concrete priorities
- Any important architectural decisions or changes
- Any blockers or open issues

**Audit status** (if applicable):
- Any active P0/P1 audit findings

**Suggested next steps**:
- What to work on based on current priorities

## Notes

- This skill helps you "resume fast" by providing immediate context
- For deeper context, the user can also check:
  - `docs/sprints/` (sprint details)
  - `docs/sessions/` (session-by-session history)
  - `docs/audits/active/` (unresolved issues)
  - `.claude/skills/` (skill-specific context)
