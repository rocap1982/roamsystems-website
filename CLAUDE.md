---
project: roam-systems-website
status: active
---

# Agent Operating Manual

This repository uses the **Fluid Build System (FBS)** — a governance framework for AI-assisted development with progressive disclosure, approval gates, and drift control.

## Resume fast (read in order)

1. `PROJECT_STATUS.md` — fastest snapshot of current state
2. `docs/sprints/CURRENT_STATUS.md` — what's happening now
3. `.claude/skills/` — load only the relevant skills (2-4 max)
4. `.claude/agents/` — specialized subagents (verifier, test-runner, debugger, + 6 reviewers for --deep mode)
5. `docs/audits/active/` — unresolved P0/P1 drift findings

## Governance (non-negotiable)

- If a change impacts canonical contracts (schemas/API/DB/business rules), create a **plan** in `docs/plans/` and wait for explicit approval before implementing.
- Contract changes follow the full pipeline:

```
/new-idea          → explore architecture and design
/review-idea-doc   → validate idea completeness
/new-plan          → formalize contract changes
/review-plan-doc   → validate plan format and completeness
/check-plan        → deep feasibility review against codebase
  ⏸ wait for explicit user approval
/new-sprint        → create agent-executable work plan
/review-sprint-doc → validate sprint doc before building
/start-sprint      → execute the work plan
/check-sprint      → deep code review after implementation
/review-sprint     → verification gates + close-out → stage: done
```

- `/review-sprint` supports `--deep` for parallel reviewer subagents (architecture, security, performance, data integrity, test quality, docs governance)

## Workflows

- **Small fixes** (1-3 files): follow `.claude/rules/workflow-small-fixes.md`
- **Sprints** (planned work): follow `.claude/rules/workflow-sprints.md`
- **Audits** (drift checks): follow `.claude/rules/workflow-audits.md`

## Progressive disclosure

- Load only what you need. Don't read the entire repo.
- Skills are loaded on demand — descriptions are always in context, full content loads when invoked.
- Keep context lean: prefer 2-4 relevant skills over broad repo-wide reading.

## Session checkpoints

At the start of meaningful work:
- State which status docs you read (`PROJECT_STATUS.md`, `docs/sprints/CURRENT_STATUS.md`).
- State which skill(s) you loaded.

At the end of a session (or use `/close-session`):
- State whether a new skill should be created/updated.
- State whether an audit, plan, or roadmap update is required.

## Documentation (two modes)

- **Install Documentation (one-time)**: establish the repo's canonical documentation set via `/install-documentation`.
- **Ongoing Documentation (per sprint)**: when features or contracts change, load the `documentation-governance` skill and update the correct canonical docs before marking sprint stage `done`.

## MCP Integrations

- **Railway MCP** — available for deployment management. Tools: `check-railway-status`, `list-services`, `list-deployments`, `deploy`, `get-logs`, `list-variables`, `set-variables`, `generate-domain`, `link-service`, `link-environment`, `create-environment`, `create-project-and-link`, `deploy-template`, `list-projects`. Use for all Railway operations instead of the browser. The workspace path is the repo root.
- **Claude in Chrome** — browser automation for tasks that require a GUI (e.g., Cloudflare DNS, Railway custom domains which aren't available via MCP).

## Keep documentation minimal

- Don't create new docs for one-off fixes.
- Prefer updating the single snapshot (`PROJECT_STATUS.md`) + existing sprint/audit docs.
