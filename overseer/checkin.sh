#!/bin/bash
# checkin.sh <project_root> [--dry-run] — one cloud-manager check-in.
# Builds the packet, asks the manager model, applies validated actions.
set -u
DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="${1:?usage: checkin.sh <project_root> [--dry-run]}"
DRY="${2:-}"

PACKET=$("$DIR/packet.sh" "$ROOT") || { echo "packet failed" >&2; exit 1; }
PROMPT="$(cat "$DIR/manager_prompt.md")

=== TELEMETRY (JSON) ===
$PACKET"

if [ "$DRY" = "--dry-run" ]; then
  echo "===== PROMPT ====="; printf '%s\n' "$PROMPT"
  echo "===== REPLY ====="
fi

# The overseer model call: any CLI that reads a prompt on stdin and writes the
# reply on stdout. Examples: a cloud-LLM CLI, `ollama run <model>`, a curl
# wrapper. Set it before running checkins:
#   export RALPH_MANAGER_LLM_CMD="your-llm-cli --stdin"
LLM_CMD="${RALPH_MANAGER_LLM_CMD:?set RALPH_MANAGER_LLM_CMD to an LLM CLI that reads the prompt on stdin}"
REPLY=$(printf '%s' "$PROMPT" | $LLM_CMD 2>/dev/null)
[ "$DRY" = "--dry-run" ] && printf '%s\n' "$REPLY"

# Extract the first JSON array from the reply (manager may wrap in prose/fences despite the contract)
ACTIONS=$(printf '%s' "$REPLY" | python3 -c '
import sys, json, re
s = sys.stdin.read()
m = re.search(r"\[.*\]", s, re.S)
try:
    arr = json.loads(m.group(0)) if m else []
except json.JSONDecodeError:
    arr = None
print("INVALID" if arr is None else json.dumps(arr))')

if [ "$ACTIONS" = "INVALID" ]; then
  echo '[]' | python3 "$DIR/executor.py" "$ROOT" $DRY
  echo "manager reply unparsable; logged" >&2
  exit 0
fi
printf '%s' "$ACTIONS" | python3 "$DIR/executor.py" "$ROOT" $DRY
