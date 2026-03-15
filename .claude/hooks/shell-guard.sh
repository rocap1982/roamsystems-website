#!/bin/bash
# shell-guard.sh — Block risky shell commands before execution
# Hook event: PreToolUse (matcher: Bash)
#
# Reads JSON from stdin with tool_input.command
# Exit 0 = allow, Exit 2 = block (stderr sent to Claude as feedback)
#
# Customize the RISKY_PATTERNS for your stack (deploy tools, DB tooling, etc.)

if ! command -v jq &>/dev/null; then
  exit 0  # allow if jq is not installed
fi

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Patterns that should be blocked or require confirmation
RISKY_PATTERNS=(
  "rm -rf"
  "drop table"
  "drop database"
  "truncate"
  "git push.*--force"
  "git reset --hard"
  "git clean -f"
  "kubectl delete"
  "docker system prune"
)

for pattern in "${RISKY_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -iqE "$pattern"; then
    echo "Blocked: command matches risky pattern '$pattern'. Rephrase or get explicit user approval." >&2
    exit 2
  fi
done

exit 0
