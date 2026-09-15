#!/bin/bash
# packet.sh <project_root> — build the telemetry JSON blob for one loop project.
# Read-only. Never touches loop state. Output: one JSON object on stdout.
set -u
ROOT="${1:?usage: packet.sh <project_root>}"
RALPH="$ROOT/scripts/ralph"
NAME="$(basename "$ROOT")"
NOW=$(date +%s)

# --- loop liveness (pattern avoids matching our own child processes) ---
LOOP_PID=$(pgrep -f "run_loop.sh $NAME" | head -1 || true)
ITER_COUNT=$(pgrep -f "python.*qwen_iteration" | wc -l | tr -d ' ')

# --- model identity (law: assert YOUR identifier, not server liveness) ---
MODEL_ID=$(sed -nE 's/.*QWEN_MODEL *= *os.environ.get\("QWEN_MODEL", *"([^"]+)".*/\1/p' "$RALPH/qwen_iteration.py" 2>/dev/null | head -1)
ENV_ID=$(grep -hoE 'QWEN_MODEL=[^ "]+' "$RALPH/run_loop.sh" "$RALPH/ralph.sh" 2>/dev/null | head -1 | cut -d= -f2)
[ -n "${ENV_ID:-}" ] && MODEL_ID="$ENV_ID"
MODELS_JSON=$(curl -s --max-time 5 http://127.0.0.1:1234/v1/models 2>/dev/null || true)
if [ -z "$MODELS_JSON" ]; then SERVER_UP=false; MODEL_SERVED=false;
elif [ -z "$MODEL_ID" ]; then SERVER_UP=true; MODEL_SERVED=false;
else SERVER_UP=true; MODEL_SERVED=$(printf '%s' "$MODELS_JSON" | grep -q "$MODEL_ID" && echo true || echo false); fi

# --- prd status ---
PRD="null"
if [ -f "$RALPH/prd.json" ]; then
  PRD=$(jq '{
    total: (.userStories|length),
    passed: ([.userStories[]|select(.passes==true)]|length),
    blocked: ([.userStories[]|select(.blocked==true)|{id,blocked_reason:(.blocked_reason//""|.[0:120])}]),
    interventions: ([.userStories[]|{id,n:(.managerInterventions//0)}]|map(select(.n>0))),
    remaining: ([.userStories[]|select(.passes!=true)|{id,title,priority,blocked:(.blocked//false)}]|.[0:8])
  }' "$RALPH/prd.json" 2>/dev/null || echo null)
fi

# --- trajectory analysis ---
TRAJ="$RALPH/trajectory.jsonl"
T_TAIL="[]"; PASSES_3H=0; ITERS_3H=0; ZERO_STREAK=0
if [ -f "$TRAJ" ]; then
  T_TAIL=$(tail -12 "$TRAJ" | jq -cs 'map({ts,story_id,iteration,verify_ok,exit_status,duration_s,reply_bytes,think_bytes,files:(.files_written|length)})' 2>/dev/null || echo '[]')
  CUTOFF=$((NOW - 10800))
  PASSES_3H=$(jq -r --arg c "$CUTOFF" 'select(.verify_ok==true and (.ts|fromdateiso8601) > ($c|tonumber)) | .ts' "$TRAJ" 2>/dev/null | wc -l | tr -d ' ')
  ITERS_3H=$(jq -r --arg c "$CUTOFF" 'select((.ts|fromdateiso8601) > ($c|tonumber)) | .ts' "$TRAJ" 2>/dev/null | wc -l | tr -d ' ')
  ZERO_STREAK=$(tac "$TRAJ" 2>/dev/null | awk 'BEGIN{n=0} /"files_written": \[\]/{n++} /"files_written": \[{?[^]]/{exit} END{print n}' || echo 0)
fi

# --- stuck detector (stdlib, no LLM) ---
STUCK="null"
if [ -f "$RALPH/stuck_detector.py" ] && [ -f "$TRAJ" ]; then
  STUCK=$(cd "$RALPH" && python3 stuck_detector.py "$TRAJ" 2>/dev/null || echo null)
fi

# --- slots (lockdirs) + queue ---
SLOTS_DIR="${RALPH_SLOTS_DIR:-$HOME/ralph-slots}"
SLOTS=$(find "$SLOTS_DIR" -maxdepth 1 -name "slot-*" 2>/dev/null | while read -r d; do basename "$d"; done | jq -Rsc 'split("\n")|map(select(length>0))' 2>/dev/null || echo '[]')
QUEUE=$(jq -Rsc 'split("\n")|map(select(length>0))' "$SLOTS_DIR/QUEUE" 2>/dev/null || echo '[]')

# --- tails for forensics ---
LV_TAIL=$(tail -30 "$RALPH/LAST_VERIFY.txt" 2>/dev/null | jq -Rs . || echo '""')
PROG_TAIL=$(tail -20 "$RALPH/progress.txt" 2>/dev/null | jq -Rs . || echo '""')
LAST_COMMIT=$(git -C "$ROOT" log -1 --format='%h %s' 2>/dev/null | jq -Rs . || echo '""')

jq -n \
  --arg project "$NAME" \
  --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --arg loop_pid "${LOOP_PID:-}" \
  --arg iter_count "$ITER_COUNT" \
  --arg model_id "$MODEL_ID" \
  --argjson server_up "$SERVER_UP" \
  --argjson model_served "$MODEL_SERVED" \
  --argjson prd "$PRD" \
  --argjson trajectory_tail "$T_TAIL" \
  --argjson passes_3h "${PASSES_3H:-0}" \
  --argjson iters_3h "${ITERS_3H:-0}" \
  --argjson zero_file_streak "${ZERO_STREAK:-0}" \
  --argjson stuck "$STUCK" \
  --argjson slots "$SLOTS" \
  --argjson queue "$QUEUE" \
  --argjson last_verify_tail "$LV_TAIL" \
  --argjson progress_tail "$PROG_TAIL" \
  --argjson last_commit "$LAST_COMMIT" \
  '{project:$project, ts:$ts, loop_alive:($loop_pid!=""), qwen_iteration_processes:($iter_count|tonumber),
    model:{identifier:$model_id, server_up:$server_up, served:$model_served},
    prd:$prd, trajectory_tail:$trajectory_tail,
    passes_last_3h:$passes_3h, iterations_last_3h:$iters_3h, trailing_zero_file_iterations:$zero_file_streak,
    stuck_detector:$stuck, slots_held:$slots, queue:$queue,
    last_verify_tail:$last_verify_tail, progress_tail:$progress_tail, last_commit:$last_commit}'
