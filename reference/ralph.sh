#!/bin/bash
# Ralph loop — based on https://github.com/snarktank/ralph (Geoffrey Huntley pattern).
# Each iteration is a FRESH model instance. Memory = git + prd.json + progress.txt.
# Default tool is the local model server (Qwen via LM Studio).
#
# Usage: ./ralph.sh [--tool qwen|claude|amp] [max_iterations]
set -euo pipefail

TOOL="qwen"
MAX_ITERATIONS=200

while [[ $# -gt 0 ]]; do
  case $1 in
    --tool) TOOL="$2"; shift 2 ;;
    --tool=*) TOOL="${1#*=}"; shift ;;
    *)
      if [[ "$1" =~ ^[0-9]+$ ]]; then MAX_ITERATIONS="$1"; fi
      shift
      ;;
  esac
done

case "$TOOL" in
  qwen|claude|amp) ;;
  *) echo "Error: --tool must be qwen, claude, or amp"; exit 1 ;;
esac

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PRD_FILE="$SCRIPT_DIR/prd.json"
PROGRESS_FILE="$SCRIPT_DIR/progress.txt"
ARCHIVE_DIR="$SCRIPT_DIR/archive"
LAST_BRANCH_FILE="$SCRIPT_DIR/.last-branch"

if [[ ! -f "$PRD_FILE" ]]; then
  echo "Missing $PRD_FILE — copy prd.json.example and fill stories."
  exit 1
fi

if [[ ! -d "$(git rev-parse --show-toplevel 2>/dev/null)" ]]; then
  echo "Ralph requires a git repo (cd to the project first, scripts/ralph/ lives inside it)."
  exit 1
fi

# Archive previous run if branchName changed (snarktank behavior)
if [[ -f "$LAST_BRANCH_FILE" ]]; then
  CURRENT_BRANCH=$(jq -r '.branchName // empty' "$PRD_FILE")
  LAST_BRANCH=$(cat "$LAST_BRANCH_FILE" 2>/dev/null || true)
  if [[ -n "$CURRENT_BRANCH" && -n "$LAST_BRANCH" && "$CURRENT_BRANCH" != "$LAST_BRANCH" ]]; then
    FOLDER_NAME="${LAST_BRANCH#ralph/}"
    ARCHIVE_FOLDER="$ARCHIVE_DIR/$(date +%Y-%m-%d)-$FOLDER_NAME"
    echo "Archiving previous run: $LAST_BRANCH -> $ARCHIVE_FOLDER"
    mkdir -p "$ARCHIVE_FOLDER"
    cp "$PRD_FILE" "$PROGRESS_FILE" "$ARCHIVE_FOLDER/" 2>/dev/null || true
    printf '# Ralph Progress Log\nStarted: %s\n---\n' "$(date)" > "$PROGRESS_FILE"
  fi
fi

CURRENT_BRANCH=$(jq -r '.branchName // empty' "$PRD_FILE")
if [[ -n "$CURRENT_BRANCH" ]]; then
  echo "$CURRENT_BRANCH" > "$LAST_BRANCH_FILE"
  git checkout -B "$CURRENT_BRANCH" 2>/dev/null || git checkout -b "$CURRENT_BRANCH"
fi

if [[ ! -f "$PROGRESS_FILE" ]]; then
  printf '# Ralph Progress Log\nStarted: %s\n---\n' "$(date)" > "$PROGRESS_FILE"
fi

echo "Starting Ralph — tool=$TOOL max=$MAX_ITERATIONS"
echo "PRD: $PRD_FILE"

for i in $(seq 1 "$MAX_ITERATIONS"); do
  echo ""
  echo "==============================================================="
  echo "  Ralph iteration $i / $MAX_ITERATIONS ($TOOL)"
  echo "==============================================================="

  OUTPUT=""
  RC=0
  if [[ "$TOOL" == "qwen" ]]; then
    OUTPUT=$(python3 "$SCRIPT_DIR/qwen_iteration.py" 2>&1 | tee /dev/stderr) || RC=$?
    python3 "$SCRIPT_DIR/strip_markers.py" >/dev/null 2>&1 || true
  elif [[ "$TOOL" == "amp" ]]; then
    OUTPUT=$(cat "$SCRIPT_DIR/prompt.md" | amp --dangerously-allow-all 2>&1 | tee /dev/stderr) || true
  else
    OUTPUT=$(claude --dangerously-skip-permissions --print < "$SCRIPT_DIR/CLAUDE.md" 2>&1 | tee /dev/stderr) || true
  fi

  if echo "$OUTPUT" | grep -q "<promise>COMPLETE</promise>"; then
    echo "Ralph completed all stories at iteration $i"
    exit 0
  fi
  # Typed iteration exits (42/43/44, or a crash) go straight to the supervisor.
  if [[ "$RC" -ne 0 ]]; then
    echo "Iteration exited $RC — propagating to supervisor"
    exit "$RC"
  fi
  sleep 1
done

echo "Ralph hit max iterations ($MAX_ITERATIONS). See $PROGRESS_FILE"
exit 1
