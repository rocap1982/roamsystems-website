---
name: review-idea-doc
description: Review an idea doc for completeness, consistency, and unresolved questions before progressing to a plan. Read-only — reports findings in chat only.
argument-hint: "[path to idea doc under docs/ideas/]"
allowed-tools: Read, Glob, Grep
context: fork
---

# /review-idea-doc — Idea Document Review

## Goal

Review an idea document for completeness, consistency, ambiguity, and unresolved questions. Report findings in the chat so the author can address issues before progressing to a plan.

**Do NOT create, write, or modify any files. Report all findings in the chat only.**

## Inputs

$ARGUMENTS

If no path is provided, ask the user which idea doc to review or list files under `docs/ideas/`.

## Steps

### 1) Load the document

- Read the idea doc at the given path.
- Read the idea template at `docs/ideas/idea-template.md` for reference.

### 2) Frontmatter validation

Check that all required frontmatter fields are present and valid:

- `doc_type`: must be `idea`
- `status`: must be one of `draft`, `accepted`, `parked`, `rejected`
- `created`: valid date
- `last_updated`: valid date, not before `created`
- `owner`: non-empty
- `tags`: non-empty array
- `related_plans`: array (can be empty if no plan exists yet)
- `related_sprints`: array (can be empty)

### 3) Section completeness

Check that all expected sections are present and non-empty:

- **Summary**: concise description of the idea (1-3 sentences)
- **Problem / Opportunity**: clearly states the current state, pain, and desired outcome
- **Constraints**: lists hard boundaries (technical, business, governance)
- **Architecture / Approach**: describes the proposed solution in enough detail to evaluate
- **Non-goals**: explicitly states what is out of scope
- **Traceability**: lists canonical docs that would be impacted

Flag any section that is missing or contains only placeholder text.

### 4) Open questions check

- If an **Open Questions** section exists, flag every item as an unresolved issue.
- Items explicitly marked as "deferred" with a clear reason are acceptable — note them but don't flag as blockers.
- If there is no Open Questions section, confirm this as a pass.

### 5) Ambiguity scan

Scan the document for ambiguous or non-committal language in decision-bearing sections (Summary, Architecture/Approach, Constraints):

- Flag instances of: "maybe", "TBD", "not sure", "possibly", "might", "could potentially", "to be decided", "we'll see", "unclear", "need to figure out"
- Exclude these terms when they appear in Open Questions or Non-goals (where uncertainty is expected).

### 6) Consistency checks

- **Constraints vs Approach**: verify the proposed approach does not contradict any stated constraint.
- **Non-goals vs Goals**: verify nothing listed as a non-goal is also described as part of the approach.
- **Approach options vs Decision**: if multiple approach options are presented, verify a decision has been recorded. Undecided options are flagged.
- **Related plans/sprints**: if `related_plans` or `related_sprints` reference specific files, verify those files exist on disk.

### 7) Implementation readiness

Assess whether the idea has enough detail to become a plan:

- Does the approach describe concrete technical components (tables, endpoints, UI, integrations)?
- Are phased implementation steps outlined?
- Is the scope bounded (clear non-goals)?

This is informational, not a blocker — report as a readiness assessment.

## Output

Report findings in the chat as a structured summary:

1. **Document**: path reviewed
2. **Frontmatter**: pass/fail with issues
3. **Section completeness**: pass/fail per section
4. **Open questions**: count of unresolved items (list them)
5. **Ambiguity**: count of flagged terms with locations
6. **Consistency**: pass/fail per check with details
7. **Implementation readiness**: ready / needs more detail
8. **Overall verdict**: Ready for plan | Needs revisions (with summary of blockers)
