---
name: check-plan
description: Deep review of a plan document before approval. Reads the full plan, cross-references against codebase reality, and checks for gaps, risks, and feasibility. Run this before approving a plan.
argument-hint: "[optional: plan doc path under docs/plans]"
context: fork
allowed-tools: Read, Glob, Grep
---

# /check-plan — Plan Document Review

## Goal

Perform a thorough review of a plan document before it is approved. Cross-reference the plan against the actual codebase to verify feasibility, check for gaps in the specification, and identify risks that weren't considered. Produce a prioritized findings list so the plan can be improved before approval.

**This is NOT `/review-plan-doc`** (which checks structural completeness of the document format). This skill reads the plan like a senior engineer evaluating whether it will actually work.

## Inputs

$ARGUMENTS

If no plan path is provided:
- Look for the most recent "Draft" plan in `docs/plans/`.

## Steps

### 0) Load context

- Read the plan doc.
- Read `PROJECT_STATUS.md` for broader project context.
- Read `CLAUDE.md` for project conventions and coding standards.
- Note the plan's **problem statement**, **proposed solution**, **implementation impact**, and **risks**.

### 1) Verify the problem statement

- Search the codebase for the files/systems described in "Current State".
- Confirm the problem actually exists as described.
- Flag any inaccuracies (e.g., "field X doesn't exist" when it does, or "we don't support Y" when we do).
- Check if the problem has already been partially or fully solved elsewhere.

### 2) Validate the proposed solution

**Schema/data model review** (if applicable):
- Read the existing schema files referenced in the plan.
- Check that proposed new tables/columns don't conflict with existing ones.
- Verify that foreign key relationships make sense with the existing data model.
- Check for missing indexes, constraints, or cascade rules.

**API/endpoint review** (if applicable):
- Read existing routes/controllers to understand current patterns.
- Verify the proposed API signatures follow existing conventions.
- Check for conflicts with existing endpoints.
- Verify auth/authorization patterns are consistent.

**Integration review** (if applicable):
- Verify external service assumptions are correct.
- Check that proposed webhook/callback patterns match existing integrations.

### 3) Implementation feasibility check

For each file listed in "Code Changes Required":
- Verify the file exists (or that the parent directory exists for new files).
- If modifying an existing file, read it and assess whether the proposed changes are compatible with what's there.
- Flag any files that would need changes but aren't listed in the plan.

For each "New File":
- Verify the proposed location follows project conventions.
- Check for naming conflicts with existing files.

### 4) Migration risk assessment

If the plan includes database migrations:
- Check if existing data would be affected (look at current table sizes, relationships).
- Verify the rollback procedure is actually feasible.
- Flag any irreversible operations.

If the plan includes breaking API changes:
- Search for all callers of affected endpoints/functions.
- Verify the migration plan accounts for all consumers.

### 5) Test coverage gap analysis

- Review the plan's "Test Changes" section.
- Search for existing tests that cover the affected areas.
- Flag any existing tests that would likely break from the proposed changes but aren't mentioned.
- Check if the proposed new tests adequately cover the critical paths.

### 6) Alternatives evaluation

- Review each alternative listed in the plan.
- Assess whether the pros/cons analysis is accurate.
- Flag if a dismissed alternative might actually be better given what you've seen in the codebase.
- Note if there are obvious alternatives that weren't considered.

### 7) Risk completeness check

- Cross-reference the plan's risk table against what you found during review.
- Flag any risks discovered during the review that aren't in the table.
- Assess whether the stated mitigations are realistic (not vague "we'll be careful" type).
- Check for common risks that are often overlooked:
  - Performance impact on hot paths
  - Race conditions in concurrent scenarios
  - Data consistency across services/modules
  - Backward compatibility with existing clients

### 8) Cross-cutting concerns

Check whether the plan addresses:
- **Authorization**: are new endpoints/data properly scoped?
- **Validation**: is input validation specified for new surfaces?
- **Error handling**: are failure modes documented?
- **Observability**: are logging/monitoring changes needed?
- **Documentation**: are all affected canonical docs listed?

## Output

Produce a structured report in the chat:

### Summary
- Plan reviewed: `<path>`
- Problem statement: verified / inaccurate / partially correct
- Solution feasibility: feasible / feasible with changes / significant concerns

### Specification Quality
| Section | Status | Notes |
|---|---|---|
| Problem Statement | Accurate / Inaccurate | ... |
| Proposed Solution | Complete / Gaps found | ... |
| Implementation Impact | Complete / Incomplete | ... |
| Migration Plan | Sound / Risky / Missing | ... |
| Alternatives | Thorough / Superficial | ... |
| Risks | Complete / Gaps found | ... |

### Issues Found

Prioritized list:

**P0 — Must fix before approval** (incorrect assumptions, missing critical requirements, feasibility blockers):
1. ...

**P1 — Should fix before approval** (incomplete specs, missing edge cases, understated risks):
1. ...

**P2 — Consider addressing** (minor gaps, enhancement suggestions, style):
1. ...

### Codebase Conflicts
- Files that need changes but aren't listed: ...
- Existing patterns that conflict with the proposal: ...
- Tests that would break: ...

### Verdict
- **Ready for approval**: Yes / No (fix P0s first) / No (fix P0s and P1s first)
- **Estimated revision effort**: trivial / small / medium / significant
- **Recommended next step**: revise plan -> re-run /check-plan OR approve and proceed to /new-sprint
