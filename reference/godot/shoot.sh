#!/bin/bash
# tools/shoot.sh [tag] — canonical headless screenshot set into shots/<tag>/
# Uses game/sim/sim_shots.tscn once Qwen builds it (US-000/US-106);
# before that, falls back to a single main-scene frame.
set -uo pipefail
source "$(dirname "$0")/env.sh"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TAG=${1:-$(git -C "$ROOT" rev-parse --short HEAD)}
OUT="$ROOT/shots/$TAG"
mkdir -p "$OUT"
cd "$ROOT/game"
if [ -f sim/sim_shots.tscn ]; then
  "$GODOT" --headless --path . res://sim/sim_shots.tscn -- --outdir="$OUT" --quit-after 3600
else
  "$GODOT" --headless --path . --write-movie "$OUT/frame.png" --quit-after 5 2>/dev/null
fi
ls "$OUT" 2>/dev/null
