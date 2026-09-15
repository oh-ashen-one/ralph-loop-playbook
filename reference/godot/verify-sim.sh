#!/bin/bash
# Sim-scene gate: tools/verify-sim.sh <sim_scene.tscn> [timeout_s]
# The sim script must call get_tree().quit(0) on success, quit(1) on failure.
set -uo pipefail
source "$(dirname "$0")/env.sh"
SCENE=${1:?usage: verify-sim.sh <sim_scene.tscn> [timeout_s]}
TIMEOUT=${2:-120}
cd "$(dirname "$0")/../game"
[ -f "sim/$SCENE" ] || { echo "missing sim scene: sim/$SCENE"; exit 1; }
# --quit-after is a frame-count safety net; the sim should quit itself sooner.
perl -e 'alarm shift; exec @ARGV' "$TIMEOUT" \
  "$GODOT" --headless --path . "res://sim/$SCENE" --quit-after 3600
CODE=$?
[ $CODE -eq 142 ] && { echo "sim timed out after ${TIMEOUT}s"; exit 1; }
exit $CODE
