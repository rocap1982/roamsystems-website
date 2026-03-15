#!/bin/bash
# format.sh — Auto-format files after agent edits
# Hook event: PostToolUse (matcher: Edit|Write)
#
# Reads JSON from stdin with tool_input.file_path
# Exit 0 = success (formatting applied or no formatter found)
#
# Customize for your repo's formatter (prettier, ruff, gofmt, etc.)

if ! command -v jq &>/dev/null; then
  exit 0  # skip formatting if jq is not installed
fi

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [ -z "$FILE_PATH" ]; then
  exit 0
fi

# Uncomment and customize for your stack:

# JavaScript/TypeScript (Prettier)
# npx prettier --write "$FILE_PATH" 2>/dev/null

# Python (Ruff)
# ruff format "$FILE_PATH" 2>/dev/null

# Go
# gofmt -w "$FILE_PATH" 2>/dev/null

exit 0
