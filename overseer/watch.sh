#!/bin/bash
# watch.sh <project_root> — event-triggered early check-in. Fires checkin.sh
# only when a mechanical trigger holds; silent otherwise. Dedupes to one
# event-checkin per 45 min per project.
set -u
DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="${1:?usage: watch.sh <project_root>}"
NAME="$(basename "$ROOT")"
STAMP="/tmp/ralph-overseer-watch-$NAME"
RALPH="$ROOT/scripts/ralph"

# dedupe
if [ -f "$STAMP" ] && [ $(( $(date +%s) - $(stat -f %m "$STAMP") )) -lt 2700 ]; then
  exit 0
fi

fire() {
  touch "$STAMP"
  echo "[watch] $1 — firing check-in for $NAME"
  "$DIR/checkin.sh" "$ROOT"
}

# loop dead with unfinished stories?
if [ -f "$RALPH/prd.json" ]; then
  REMAINING=$(jq '[.userStories[]|select(.passes!=true)]|length' "$RALPH/prd.json" 2>/dev/null || echo 0)
  if [ "$REMAINING" -gt 0 ] && ! pgrep -f "run_loop.sh $NAME" >/dev/null; then
    fire "loop dead, $REMAINING stories remain"; exit 0
  fi
fi

# stuck detector?
if [ -f "$RALPH/stuck_detector.py" ] && [ -f "$RALPH/trajectory.jsonl" ]; then
  STUCK=$(cd "$RALPH" && python3 stuck_detector.py "$RALPH/trajectory.jsonl" 2>/dev/null | jq -r .stuck 2>/dev/null || echo false)
  [ "$STUCK" = "true" ] && { fire "stuck detector fired"; exit 0; }
fi

# failing-but-alive: iterations happening, nothing passing for 3h?
if [ -f "$RALPH/trajectory.jsonl" ]; then
  CUTOFF=$(( $(date +%s) - 10800 ))
  ITERS=$(jq -r --arg c "$CUTOFF" 'select((.ts|fromdateiso8601) > ($c|tonumber)) | .ts' "$RALPH/trajectory.jsonl" 2>/dev/null | wc -l | tr -d ' ')
  PASSES=$(jq -r --arg c "$CUTOFF" 'select(.verify_ok==true and (.ts|fromdateiso8601) > ($c|tonumber)) | .ts' "$RALPH/trajectory.jsonl" 2>/dev/null | wc -l | tr -d ' ')
  if [ "${ITERS:-0}" -ge 3 ] && [ "${PASSES:-0}" -eq 0 ]; then
    fire "0 passes in 3h across $ITERS iterations"; exit 0
  fi
fi
exit 0
