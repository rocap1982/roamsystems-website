# Agents

Custom subagent definitions for Claude Code. Each `.md` file defines a specialized agent with its own system prompt, tool restrictions, and model selection.

## Included Agents

- **verifier** — validates completed work (read-only tools, fast model)
- **test-runner** — runs tests and fixes failures (full tools, fast model)
- **debugger** — root cause analysis specialist (full tools)

## Usage

Claude delegates to these agents automatically based on their `description` field. You can also explicitly request delegation: "use the verifier agent" or "delegate this to the debugger."

## Creating New Agents

Create a new `.md` file in this directory with YAML frontmatter:

```yaml
---
name: my-agent
description: What this agent does and when to use it.
model: haiku           # haiku, sonnet, opus, or inherit
tools: Read, Glob, Grep, Bash   # comma-separated tool list
maxTurns: 20           # max agentic turns
---

System prompt instructions here.
```

See the Claude Code docs for the full list of supported frontmatter fields.
