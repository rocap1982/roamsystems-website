---
name: verify-install
description: Verify FBS installation is complete and correctly configured. Use after installing FBS into a repo to confirm everything is in place.
---

# /verify-install — Verify FBS Installation

## Goal

Check that all FBS components are properly installed and report any missing items.

## Steps

### 1) Check required files

Verify these files exist and are non-empty:

**Required:**
- [ ] `CLAUDE.md` (root project instructions)
- [ ] `.claude/agents/` directory with at least one agent definition
- [ ] `PROJECT_STATUS.md` (resume-fast snapshot)
- [ ] `docs/sprints/CURRENT_STATUS.md` (current work status)

**Rules:**
- [ ] `.claude/rules/foundation.md`
- [ ] `.claude/rules/workflow-small-fixes.md`
- [ ] `.claude/rules/workflow-sprints.md`
- [ ] `.claude/rules/workflow-audits.md`

**Skills (minimum set):**
- [ ] `.claude/skills/documentation-governance/SKILL.md`
- [ ] At least 2 additional domain skills

### 2) Check recommended components

**Settings:**
- [ ] `.claude/settings.json` (hooks and permissions)
- [ ] `.mcp.json` (MCP server configuration)

**Agents:**
- [ ] `.claude/agents/` directory exists with at least one agent definition

**Documentation:**
- [ ] `docs/plans/` directory exists with plan template
- [ ] `docs/ideas/` directory exists with idea template
- [ ] `docs/sprints/sprint-template.md` exists
- [ ] `docs/audits/active/` and `docs/audits/resolved/` directories exist
- [ ] `docs/sessions/` directory exists
- [ ] `docs/reference/` directory exists with canonical docs (or `/install-documentation` not yet run)

**Hooks:**
- [ ] `.claude/hooks/` directory exists with hook scripts
- [ ] Hook scripts are executable (`chmod +x`)

### 3) Report results

Provide a structured summary:
- **Required**: pass/fail per item
- **Recommended**: present/missing per item
- **Next steps**: what to do about missing items
