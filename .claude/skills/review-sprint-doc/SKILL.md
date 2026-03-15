---
name: review-sprint-doc
description: Review a sprint doc for completeness, consistency, and implementation readiness. This is NOT /review-sprint (which runs verification gates and closes a sprint). Read-only — reports findings in chat only.
argument-hint: "[path to sprint doc under docs/sprints/]"
allowed-tools: Read, Glob, Grep
context: fork
---

# /review-sprint-doc — Sprint Document Review

## Goal

Review a sprint document for completeness, consistency, ambiguity, and unresolved questions. Report findings in the chat so the author can address issues before starting implementation.

**This is NOT `/review-sprint`** (which runs verification gates and closes a sprint). This skill reviews the sprint doc's quality and readiness before or during work.

**Do NOT create, write, or modify any files. Report all findings in the chat only.**

## Inputs

$ARGUMENTS

If no path is provided:
- Read `docs/sprints/CURRENT_STATUS.md` and use `active_sprint` as the default.
- If no active sprint is found, ask the user which sprint doc to review or list files under `docs/sprints/`.

## Steps

### 1) Load the document

- Read the sprint doc at the given path.
- Read the sprint template at `docs/sprints/sprint-template.md` for reference.

### 2) Frontmatter validation

Check that all required frontmatter fields are present and valid:

- `doc_type`: must be `sprint`
- `status`: must be one of `active`, `completed`, `cancelled`
- `stage`: must be one of `planning`, `in_progress`, `verification`, `done`
- `created`: valid date
- `last_updated`: valid date, not before `created`
- `dates.start`: valid date
- `dates.end`: valid date, not before `dates.start`
- `sprint_goal`: non-empty, single clear sentence

### 3) Section completeness

Check that all expected sections are present and non-empty:

- **Summary**: concise description of what the sprint delivers
- **Acceptance criteria**: list of measurable/verifiable criteria
- **Contracts / governance**: references to approved plans (if schema/API/contract changes are involved)
- **Work plan**: task breakdown with To do / In progress / Done columns or lists
- **Test plan**: must include both **Automated** (commands to run) and **Manual** (checklist items)
- **Review gate**: describes what must pass before the sprint can close
- **Documentation DoD**: lists specific canonical docs to create or update
- **Audit plan**: describes audit approach (mini audit, in-depth, or "none needed" with rationale)
- **Notes**: section exists (can be empty at planning stage)

Flag any section that is missing or contains only placeholder text.

### 4) Open questions check

- Scan the entire document for unresolved questions.
- Flag every unresolved item. A sprint doc should have zero open questions before starting implementation.

### 5) Ambiguity scan

Scan decision-bearing sections (Acceptance criteria, Work plan, Test plan) for ambiguous language:

- **Acceptance criteria**: flag vague criteria that cannot be objectively verified. Look for: "improve", "better", "faster", "cleaner", "should work", "mostly", "as needed"
- **Work plan**: flag tasks that are too vague to act on. Look for: "handle", "deal with", "look into", "figure out", "misc", "various"
- **Test plan**: flag test items without clear pass/fail conditions.

### 6) Consistency checks

- **Governance compliance**: if the work plan includes DB schema changes, new API endpoints, or contract-impacting work, verify the Contracts/governance section references an approved plan in `docs/plans/`. Check that the referenced plan file exists and has `Status: Approved`.
- **Acceptance criteria vs Work plan**: verify every acceptance criterion has corresponding work plan tasks.
- **Work plan vs Test plan**: verify key work plan deliverables have corresponding test items.
- **Documentation DoD specificity**: verify doc paths are specific, not vague ("update relevant docs").
- **Date validity**: verify start/end dates are reasonable.
- **Related plan alignment**: if a related plan is referenced, verify the sprint scope does not exceed the plan scope.

### 7) Implementation readiness

Assess whether the sprint is ready to start:

- Zero open questions?
- Zero ambiguous acceptance criteria?
- All sections complete?
- Governance references valid (if applicable)?
- Test plan has runnable automated commands?
- Work plan tasks are actionable?

## Output

Report findings in the chat as a structured summary:

1. **Document**: path reviewed
2. **Frontmatter**: pass/fail with issues
3. **Section completeness**: pass/fail per section
4. **Open questions**: count of unresolved items (list them)
5. **Ambiguity**: count of flagged items with locations
6. **Consistency**: pass/fail per check with details
7. **Implementation readiness**: pass/fail per criterion
8. **Overall verdict**: Ready to implement | Needs revisions (with summary of blockers)
