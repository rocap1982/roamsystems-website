---
name: review-code
description: Review recent code changes for quality, correctness, and adherence to project conventions. Use after implementation and before committing.
allowed-tools: Read, Glob, Grep, Bash
context: fork
---

# /review-code — Code Review

## Goal

Review recent code changes for quality, correctness, security, and adherence to project conventions. Reports findings in chat — does not modify files.

## Inputs

$ARGUMENTS

Optional: specific files or directories to review, or a git ref range (e.g., `HEAD~3..HEAD`).

## Steps

### 1) Identify changes to review

- If a git ref range is provided, use `git diff <range>` to get the changeset.
- If specific files are provided, read those files.
- If no arguments, use `git diff --cached` (staged changes) or `git diff HEAD` (all uncommitted changes).

### 2) Review checklist

For each changed file, check:

**Correctness**
- Logic errors or off-by-one mistakes
- Missing error handling at system boundaries
- Unhandled edge cases visible in the diff

**Security**
- No hardcoded secrets, tokens, or credentials
- Input validation at API/user boundaries
- No SQL injection, XSS, or command injection vectors

**Code quality**
- Follows existing patterns in the codebase
- No unnecessary complexity or over-engineering
- Variable/function names are clear and consistent
- No dead code or commented-out blocks introduced

**Project conventions**
- Naming conventions match existing code
- File organization follows project structure
- No new dependencies without clear justification

**Tests**
- New behavior has corresponding tests (or note the gap)
- Existing tests not broken by changes

### 3) Canonical alignment (if applicable)

- If changes touch API endpoints, DB schema, or business rules, verify alignment with canonical docs in `docs/reference/`.
- Flag any drift between implementation and canonical specification.

## Output

Report findings as a structured summary:

1. **Files reviewed**: list with line count changes
2. **Issues found**: grouped by severity (critical / warning / note)
3. **Canonical alignment**: pass / drift detected / not applicable
4. **Overall assessment**: Ship it | Minor issues | Needs changes
