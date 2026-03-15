#!/bin/bash
# read-guard.sh — Block reading common secret files into model context
# Hook event: PreToolUse (matcher: Read)
#
# Reads JSON from stdin with tool_input.file_path
# Exit 0 = allow, Exit 2 = block (stderr sent to Claude as feedback)
#
# Customize the BLOCKED_PATTERNS to match your secrets footprint.

if ! command -v jq &>/dev/null; then
  exit 0  # allow if jq is not installed
fi

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

BLOCKED_PATTERNS=(
  ".env"
  ".env.local"
  ".env.production"
  "credentials.json"
  "service-account.json"
  "id_rsa"
  "id_ed25519"
  ".npmrc"
  ".pypirc"
)

for pattern in "${BLOCKED_PATTERNS[@]}"; do
  if [[ "$FILE_PATH" == *"$pattern"* ]]; then
    echo "Blocked: '$FILE_PATH' matches secret file pattern '$pattern'. This file should not be read into context." >&2
    exit 2
  fi
done

exit 0
