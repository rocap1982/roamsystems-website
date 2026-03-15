---
name: review-plan-doc
description: Review a plan doc for completeness, consistency, and approval readiness. Read-only — reports findings in chat only.
argument-hint: "[path to plan doc under docs/plans/]"
allowed-tools: Read, Glob, Grep
context: fork
---

# /review-plan-doc — Plan Document Review

## Goal

Review a plan document for completeness, consistency, ambiguity, and unresolved questions. Report findings in the chat so the author can address issues before seeking approval.

**Do NOT create, write, or modify any files. Report all findings in the chat only.**

## Inputs

$ARGUMENTS

If no path is provided, ask the user which plan doc to review or list files under `docs/plans/`.

## Steps

### 1) Load the document

- Read the plan doc at the given path.
- Read the plan template at `docs/plans/plan-template.md` for reference.

### 2) Header / metadata validation

Check that all required metadata fields are present and valid:

- **Status**: must be one of `Draft`, `Review`, `Approved`, `Implemented`, `Rejected`, `Superseded`
- **Created**: valid date
- **Author**: non-empty
- **Approver**: non-empty
- **Related Issues**: present (can be "None")

### 3) Section completeness

Check that all expected sections are present and non-empty:

- **Problem Statement**: clearly defines what problem this plan solves
- **Proposed Solution**: describes the solution with enough specificity to implement
  - **Canonical Changes Required**: lists specific canonical doc paths that will be created or updated
  - **Proposed Specification**: detailed technical specification
- **Implementation Impact**: concrete list of affected areas (DB tables, API endpoints, UI components, packages)
- **Migration Plan**: required if the plan introduces breaking changes; otherwise note its absence as acceptable
- **Alternatives Considered**: at least one alternative with rationale for why it was rejected
- **Traceability**: links back to idea doc (if applicable) and forward to sprint (if created)
- **Risks**: non-empty list of risks with mitigations

Flag any section that is missing or contains only placeholder text.

### 4) Open questions check

- Scan the entire document for unresolved questions (explicit "Open Questions" section, or inline "?" / "TBD" markers).
- Flag every unresolved item. A plan should have zero open questions before approval.

### 5) Ambiguity scan

Scan decision-bearing sections (Problem Statement, Proposed Solution, Specification, Implementation Impact) for ambiguous language:

- Flag instances of: "maybe", "TBD", "not sure", "possibly", "might", "could potentially", "to be decided", "we'll see", "unclear", "need to figure out", "probably"
- Exclude these terms when they appear in Alternatives Considered or Risks (where hedging is acceptable).

### 6) Consistency checks

- **Problem -> Solution alignment**: verify the proposed solution directly addresses the stated problem.
- **Canonical changes specificity**: verify canonical doc paths are specific, not vague wildcards.
- **Implementation impact completeness**: verify all areas mentioned in the specification are covered in the impact section.
- **Migration plan necessity**: if the specification introduces new DB tables, schema changes, or breaking API changes, verify a migration plan exists.
- **Related idea doc**: if the plan references an idea doc, verify the file exists and check that the plan's scope aligns with the idea's accepted direction.
- **Risks vs mitigations**: verify every listed risk has a corresponding mitigation or acceptance statement.

### 7) Approval readiness

Assess whether the plan is ready for approval:

- Zero open questions?
- Zero ambiguous terms in specification?
- All sections complete?
- Canonical changes use specific paths?
- Risks addressed?
- Migration plan present (if needed)?

## Output

Report findings in the chat as a structured summary:

1. **Document**: path reviewed
2. **Metadata**: pass/fail with issues
3. **Section completeness**: pass/fail per section
4. **Open questions**: count of unresolved items (list them)
5. **Ambiguity**: count of flagged terms with locations
6. **Consistency**: pass/fail per check with details
7. **Approval readiness**: pass/fail per criterion
8. **Overall verdict**: Ready for approval | Needs revisions (with summary of blockers)
