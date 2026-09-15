#!/bin/bash
# run_loop.sh — supervisor wrapper around ralph.sh for local-Qwen Ralph loops.
#
#   - claims a GPU slot from the slots dir (max 2 loops generating per box;
#     release via EXIT trap)
#   - restarts ralph.sh on crash, max 5 restarts
#   - routes typed iteration exit codes (see HARNESS.md):
#       0  normal — continue if unpassed stories remain
#       42 all stories passed / phase complete — done
#       43 all remaining stories blocked — stuck_detector + ESCALATE to a human
#       44 repeated format failure — continue (model rutting, not crashed)
#   - runs stuck_detector.py every 10 rounds (advisory)
#
# Usage: run_loop.sh <loop-name> [iterations-per-ralph-run]
# Deploy next to ralph.sh in scripts/ralph/; run from the project root.
set -uo pipefail
# no -e: exit codes below are control flow, not errors.

NAME="${1:?usage: run_loop.sh <loop-name> [iterations]}"
ITERS="${2:-200}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SLOTS="${RALPH_SLOTS_DIR:-$HOME/ralph-slots}"
MAX_RESTARTS=5
DETECT_EVERY=10

# LAW 16 — assets-first launch gate. No slot, no loop, until real licensed
# art is on disk. Override only for a deliberate no-art project:
#   ALLOW_NO_ASSETS=1 run_loop.sh <name>
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
if [[ "${ALLOW_NO_ASSETS:-0}" != "1" ]]; then
  bash "$SCRIPT_DIR/preflight_assets.sh" "$PROJECT_ROOT" || {
    echo "run_loop: asset preflight FAILED — launch blocked (law 16)"; exit 1; }
fi

# LAW 17 — production-quality contract. New scaffolds opt in mechanically via
# .ralph-quality-required; a manually-added contract opts an older project in.
# There is no Qwen-side bypass: the manager completes the contract and tests.
QUALITY_REQUIRED="$PROJECT_ROOT/.ralph-quality-required"
QUALITY_CONTRACT="$PROJECT_ROOT/quality/contract.json"
QUALITY_PREFLIGHT="$SCRIPT_DIR/quality/preflight_quality.py"
if [[ -f "$QUALITY_REQUIRED" || -f "$QUALITY_CONTRACT" ]]; then
  if [[ ! -f "$QUALITY_PREFLIGHT" ]]; then
    echo "run_loop: quality contract required but validator is missing: $QUALITY_PREFLIGHT"
    exit 1
  fi
  python3 "$QUALITY_PREFLIGHT" --root "$PROJECT_ROOT" || {
    echo "run_loop: production-quality preflight FAILED — launch blocked (law 17)"
    exit 1
  }
fi

# GPU slot law: claim before the first iteration, release on any exit.
bash "$SLOTS/claim.sh" "$NAME" "ralph.sh" || { echo "run_loop: no slot; aborting"; exit 1; }
trap 'bash "$SLOTS/release.sh" "$NAME" >/dev/null 2>&1 || true' EXIT

restarts=0
rounds=0
while true; do
  rounds=$((rounds + 1))
  echo "=== run_loop $NAME: round $rounds (restarts $restarts/$MAX_RESTARTS) ==="
  # FAILURES #79: a co-tenant can evict our model mid-run; every iteration then
  # 400s while the server still answers 200. Self-heal before each round.
  bash "$SCRIPT_DIR/ensure_model.sh" || {
    echo "run_loop: model unavailable — pausing 60s before retry"; sleep 60; }
  bash "$SCRIPT_DIR/ralph.sh" --tool qwen "$ITERS"
  rc=$?

  case $rc in
    0)
      # ralph.sh exits 0 on <promise>COMPLETE</promise>; confirm via prd state.
      remaining=$(jq '[.userStories[] | select(.passes | not)] | length' "$SCRIPT_DIR/prd.json" 2>/dev/null || echo 1)
      if [[ "$remaining" == "0" ]]; then
        echo "run_loop: all stories passed — done"
        exit 0
      fi
      ;; # work remains: loop again
    42)
      remaining=$(jq '[.userStories[] | select(.passes | not)] | length' "$SCRIPT_DIR/prd.json" 2>/dev/null || echo 1)
      if [[ "$remaining" == "0" ]]; then
        echo "run_loop: all stories passed — done"
        exit 0
      fi
      phase=$(cat "$SCRIPT_DIR/PHASE" 2>/dev/null || echo "?")
      echo "run_loop: phase $phase complete — GPU slot released; human checkpoint required"
      echo "run_loop: inspect canonical evidence, then bump scripts/ralph/PHASE and relaunch"
      exit 42
      ;;
    43)
      echo "run_loop: all remaining stories BLOCKED (43)"
      python3 "$SCRIPT_DIR/stuck_detector.py" "$SCRIPT_DIR/trajectory.jsonl" || true
      echo "ESCALATE: human manager needed — read blocked_reason in prd.json"
      exit 43
      ;;
    44)
      echo "run_loop: format failure streak (44) — continuing"
      ;;
    143)
      # SIGTERM = a manager deliberately killed the iteration (intervention).
      # Not a crash: restart without burning the ladder (FAILURES #73).
      echo "run_loop: iteration SIGTERMed (manager intervention) — respawning"
      sleep 3
      ;;
    *)
      # ralph.sh exit 1 = crash OR iteration budget exhausted; either way we
      # restart with a fresh budget.
      restarts=$((restarts + 1))
      if [[ $restarts -gt $MAX_RESTARTS ]]; then
        echo "run_loop: $MAX_RESTARTS crashes — giving up (last rc=$rc)"
        exit 1
      fi
      echo "run_loop: ralph.sh exited rc=$rc — restart $restarts/$MAX_RESTARTS"
      sleep 5
      ;;
  esac

  # Advisory rut check every DETECT_EVERY rounds.
  if [[ $((rounds % DETECT_EVERY)) -eq 0 ]]; then
    python3 "$SCRIPT_DIR/stuck_detector.py" "$SCRIPT_DIR/trajectory.jsonl" || true
  fi
done
