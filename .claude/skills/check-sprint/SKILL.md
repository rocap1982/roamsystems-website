---
name: check-sprint
description: Deep code review of a completed sprint. Reads every diff, cross-references against the sprint doc and plan, hunts for bugs and missed requirements. Run this after implementation is done but before /review-sprint.
argument-hint: "[optional: sprint doc path under docs/sprints/]"
---

# /check-sprint — Sprint Code Review

## Goal

Perform a deep, hands-on code review of everything implemented in a sprint. Cross-reference the actual code against the sprint doc and associated plan. Find bugs, missed requirements, convention violations, and regression risks. Produce a prioritized fix list so issues can be resolved before running `/review-sprint`.

**This is NOT `/review-sprint`** (which runs automated verification gates and closes the sprint). This skill reads the code like a senior engineer doing a PR review.

## Inputs

$ARGUMENTS

If no sprint path is provided:
- Read `docs/sprints/CURRENT_STATUS.md` and use `active_sprint`.

## Steps

### 0) Load context

- Read the sprint doc.
- Read the associated plan doc (from the sprint's Contracts/governance section), if one exists.
- Read `PROJECT_STATUS.md` for broader context.
- Read `CLAUDE.md` for project conventions and coding standards.
- Note the sprint's **acceptance criteria**, **work plan tasks**, and **test plan**.

### 1) Identify the sprint's code changes

Find the commit range for this sprint. Use the sprint doc's `dates.start` or the first commit that references the sprint:

```bash
# Find the merge base or the commit just before sprint work began
git log --oneline --since="<sprint-start-date>" --until="now" -- .
```

If the sprint was done in a branch/PR, use that PR's diff instead:

```bash
git diff main...<branch> --stat
```

If the sprint was committed directly to main, identify the commit range from the sprint start date and collect the full file list:

```bash
git diff <pre-sprint-sha>..HEAD --stat
```

Produce a **changed file list** — this is the review surface.

### 2) Read every changed file

For each file in the changed file list:
- Read the full file (not just the diff) to understand context.
- For large files (>500 lines), focus on the changed regions but read enough surrounding context to understand the logic.

Use parallel subagents (Task tool with Explore type) to review files concurrently when there are many changes. Split by domain (e.g., backend, frontend, shared/config).

### 3) Completeness check

Cross-reference every item in the sprint doc against the actual code:

**Acceptance criteria**:
- For each criterion, identify the specific code that satisfies it.
- Flag any criterion where you cannot find corresponding implementation.
- Flag any criterion that is only partially implemented.

**Work plan tasks**:
- For each task marked "Done" in the sprint doc, verify the code exists and is functional.
- For each task marked "To do" or "In progress", flag it as incomplete.

**Plan fidelity** (if a plan doc exists):
- Compare what the plan specified vs what was actually built.
- Flag **scope gaps**: things the plan required but the sprint didn't implement.
- Flag **scope creep**: things built that weren't in the plan (may be fine, but note them).
- Flag **deviations**: where the implementation chose a different approach than the plan specified.

### 4) Bug hunt

Read the new/modified code with a critical eye. Look for:

**Logic errors**:
- Off-by-one errors, wrong comparison operators, inverted conditions
- Missing `await` on async calls
- Unreachable code paths, dead branches
- State mutations in unexpected places

**Missing boundary handling**:
- Null/undefined access on data that comes from DB queries or API responses
- Missing error handling on external calls (DB, third-party APIs, file I/O)
- Unhandled edge cases in switch/if chains (missing default/else)
- Empty array/object access without guards

**Security** (apply project-specific rules from CLAUDE.md, plus general checks):
- Missing authorization/scoping on DB queries (e.g., tenant or user filtering)
- SQL injection vectors (raw string interpolation in queries)
- XSS vectors (unescaped user input rendered in UI)
- Missing auth checks on new API endpoints
- Sensitive data exposed in API responses

**Data integrity**:
- DB writes without transactions where multiple tables are modified
- Missing cascading updates/deletes
- Enum mismatches between frontend and backend
- ID generation not following the project's established pattern

**Concurrency/timing**:
- Race conditions in async operations
- Missing debounce/throttle on user-triggered actions
- Stale closure references in React effects or similar framework patterns

### 5) Convention compliance

Check against CLAUDE.md conventions and established project patterns. Common areas:

- **Project structure**: files placed in the correct directories per the project's conventions.
- **Imports**: using the project's established aliases and import conventions.
- **Validation**: schemas shared between client and server where applicable.
- **Styling**: following the project's established styling approach.
- **Auth/scoping**: queries and endpoints follow the project's authorization model.

Defer to CLAUDE.md and any `.claude/rules/` files for project-specific conventions. Flag violations against whatever conventions the project has established.

### 6) Regression risk assessment

Identify files that were modified but may lack test coverage:

- Cross-reference changed files against the sprint's test plan.
- Flag modified files/functions that have no corresponding automated or manual test.
- Flag changes to shared utilities or core modules that could affect other features.
- Check if any existing tests were deleted or disabled.

### 7) Unused/dead code check

Look for code artifacts from the implementation process:

- Unused imports
- Commented-out code blocks (should be removed, not commented)
- Console.log / debug statements left behind
- TODO/FIXME/HACK comments added during the sprint without corresponding tasks
- Unused variables or functions
- Orphaned files (created but not imported anywhere)

## Output

Produce a structured report in the chat:

### Summary
- Sprint reviewed: `<path>`
- Files changed: `<count>`
- Review approach: full read / parallel subagents / focused review

### Completeness
| Acceptance Criterion | Status | Evidence |
|---|---|---|
| ... | Implemented / Partial / Missing | File:line or explanation |

| Work Plan Task | Sprint Status | Code Status |
|---|---|---|
| ... | Done/In Progress/To Do | Verified / Not found / Partial |

### Plan Fidelity (if applicable)
- Scope gaps: ...
- Scope creep: ...
- Deviations: ...

### Issues Found

Prioritized list:

**P0 — Must fix before review** (bugs, security, broken functionality):
1. ...

**P1 — Should fix before review** (convention violations, missing error handling, incomplete features):
1. ...

**P2 — Nice to fix** (dead code, minor style issues, missing tests for edge cases):
1. ...

### Regression Risks
- Files without test coverage: ...
- Shared code modifications: ...

### Verdict
- **Ready for /review-sprint**: Yes / No (fix P0s first) / No (fix P0s and P1s first)
- **Estimated fix effort**: trivial / small / medium / significant
- **Recommended next step**: fix issues → re-run /check-sprint OR proceed to /review-sprint
