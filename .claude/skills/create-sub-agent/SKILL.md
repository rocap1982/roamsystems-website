---
name: create-sub-agent
description: Interactive wizard for creating custom subagents. Walks the user through purpose, tools, model, and permissions to generate a ready-to-use agent definition. Use when the user wants to create a new agent.
argument-hint: "[agent name or purpose]"
---

# /create-sub-agent — Interactive Agent Builder

## Goal

Walk the user through an interactive conversation to design and create a custom subagent definition file at `.claude/agents/<name>.md`.

## Inputs

$ARGUMENTS

If a name or purpose is provided, use it as the starting point. Otherwise begin from scratch.

## Process

Work through the following steps **one at a time**. Ask the user each question, wait for their answer, then move to the next. Do NOT dump all questions at once.

### Step 1: Purpose & Name

Ask the user:
- **What should this agent do?** Get a clear, specific description of the agent's purpose and when it should be used.
- **What should it be called?** Suggest a name based on the purpose (lowercase, hyphens only). Let them override.

### Step 2: Tools

Present the available tools and ask which ones the agent needs:

| Tool | What it does |
|------|-------------|
| `Read` | Read files |
| `Glob` | Find files by pattern |
| `Grep` | Search file contents |
| `Bash` | Run shell commands |
| `Edit` | Modify existing files |
| `Write` | Create new files |
| `WebSearch` | Search the web |
| `WebFetch` | Fetch web page content |
| `Task` | Spawn other subagents |

Then ask: **Are there any tools this agent should NOT have access to?**

Common patterns to suggest:
- **Read-only agents** (reviewers, scanners, validators): `Read, Glob, Grep, Bash` with `disallowedTools: Edit, Write`
- **Full-access agents** (fixers, builders, writers): `Read, Glob, Grep, Bash, Edit, Write`
- **Research agents**: `Read, Glob, Grep, WebSearch, WebFetch`
- **Orchestrators**: Add `Task` or `Task(agent1, agent2)` to delegate to specific agents

### Step 3: Permission Mode

Explain the options and ask which fits:

| Mode | Behavior | Best for |
|------|----------|----------|
| `default` | Prompts user for permission on risky actions | Read-only agents, validators |
| `acceptEdits` | Auto-approves file edits, prompts for Bash | Agents that fix code |
| `dontAsk` | Auto-denies permission prompts (only listed tools work) | Tightly scoped agents |
| `plan` | Read-only exploration, cannot modify anything | Research and planning agents |
| `bypassPermissions` | Skips all permission checks | Fully trusted automation (use with caution) |

### Step 4: Model

Explain the tradeoffs and ask which model to use:

| Model | Speed | Cost | Best for |
|-------|-------|------|----------|
| `haiku` | Fastest | Lowest | Simple, well-defined tasks (test running, validation, formatting) |
| `sonnet` | Balanced | Medium | Tasks requiring judgment (code review, planning, security analysis) |
| `opus` | Slowest | Highest | Complex reasoning (architecture, difficult debugging) |

Default recommendation: `haiku` for execution-focused agents, `sonnet` for judgment-focused agents.

### Step 5: Additional Options

Ask about optional features:

- **Memory** — Should this agent remember things across sessions? (`project` = shared with team, `local` = personal, `user` = across all projects)
- **Max turns** — How many iterations before stopping? (default: 20 for simple agents, 30-40 for complex ones)
- **Skills preload** — Should any skills be baked into this agent's context? List available skills from `.claude/skills/`.
- **Isolation** — Should this agent work in a separate git worktree? (useful for risky changes like refactoring)
- **Background** — Should this agent run in the background while the user continues working?

Only ask about features relevant to the agent's purpose. Don't overwhelm with options that don't apply.

### Step 6: System Prompt

Based on all the answers, draft the agent's system prompt (the markdown body after the frontmatter). A good system prompt includes:

1. **Role statement** — one sentence defining what the agent is
2. **Workflow** — numbered steps for how it should operate
3. **Output format** — what it should report back

Keep it under 20 lines. Show the user the draft and ask for adjustments.

### Step 7: Create the File

Assemble the complete agent definition and write it to `.claude/agents/<name>.md`.

Show the user the final file and explain how to use it:
- Claude will automatically delegate to it when the description matches a task
- They can explicitly request it: "Use the <name> agent to..."
- They can view all agents with `/agents`

## Reference

See [references/field-reference.md](references/field-reference.md) for the complete frontmatter field specification.

## Example Output

```markdown
---
name: api-tester
description: Tests API endpoints for correctness, error handling, and contract compliance. Use after implementing or modifying API routes.
model: haiku
tools: Read, Glob, Grep, Bash
disallowedTools: Edit, Write
permissionMode: default
memory: project
maxTurns: 25
---

You are an API testing specialist.

When invoked:
1. Identify the API endpoints that were changed or created
2. Read the canonical API contract docs (if they exist) for expected behavior
3. Run endpoint tests using curl, httpie, or the project's test framework
4. Verify response shapes, status codes, error handling, and edge cases

Report:
- Endpoints tested (method + path)
- Pass/fail per endpoint with details
- Contract drift (if canonical docs exist)
- Missing test coverage
```
