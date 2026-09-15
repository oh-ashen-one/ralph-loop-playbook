#!/bin/bash
# GUT unit-test gate: verify-gut.sh [TestFile.gd]
# No arg = whole tests/ dir.
# Godot AND GUT both exit 0 on parse errors, silently-skipped test files,
# and even failing tests — the exit code is NOT a gate. Grep the output.
set -uo pipefail
source "$(dirname "$0")/env.sh"
cd "$GAME_ROOT"
if [[ $# -ge 1 ]]; then
  OUT=$("$GODOT" --headless -d -s addons/gut/gut_cmdln.gd -gtest="res://tests/$1" -gexit 2>&1)
else
  OUT=$("$GODOT" --headless -d -s addons/gut/gut_cmdln.gd -gdir=res://tests -gexit 2>&1)
fi
CODE=$?
echo "$OUT"
if echo "$OUT" | grep -qE "SCRIPT ERROR|Parse Error|Failed to load script|Failed loading resource|[1-9][0-9]* failing tests"; then
  echo "verify-gut: failure markers in output (exit code alone is not a gate)"
  exit 1
fi
exit $CODE
