#!/bin/bash
# Shared env for the godot verify helpers.
# WARNING: this file lives THREE dirs deep (scripts/ralph/godot/), so the
# project root is ../../.. — getting this wrong once made every gate
# silently verify an empty directory and exit 0 (FAILURES #52).
export GODOT="${GODOT:-godot}"
export GAME_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
