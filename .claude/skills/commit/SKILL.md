---
name: commit
description: Create a well-structured git commit with conventional message format. Use after completing a task or set of related changes.
argument-hint: "[optional: commit message or scope hint]"
---

# /commit — Structured Git Commit

## Goal

Stage and commit changes with a well-structured conventional commit message. Ensures status docs are updated before committing.

## Inputs

$ARGUMENTS

Optional: commit message override or scope hint.

## Steps

### 1) Pre-commit checks

- Run `git status` to see all changed files.
- Run `git diff --stat` to summarize the changes.
- Check if `PROJECT_STATUS.md` or `docs/sprints/CURRENT_STATUS.md` need updating based on what changed. If the work completed a task, moved a sprint stage, or changed priorities, update them before committing.

### 2) Stage files

- Stage all relevant changed files. Exclude:
  - `.env`, credentials, secrets
  - Large generated files (node_modules, build artifacts)
  - Files unrelated to the current task

### 3) Generate commit message

Use conventional commit format:

```
<type>(<scope>): <short summary>

<body - what changed and why>
```

**Types**: feat, fix, refactor, docs, test, chore, style, perf
**Scope**: the subsystem or area affected (e.g., auth, api, ui, sprint, audit)

Rules:
- Summary line under 72 characters
- Body explains *what* and *why*, not *how*
- Reference sprint doc or plan if applicable
- If multiple logical changes, suggest splitting into separate commits

### 4) Commit

- Execute the commit.
- Show the commit hash and summary.

## Output

1. Files committed (count and list)
2. Commit message used
3. Status doc updates made (if any)
