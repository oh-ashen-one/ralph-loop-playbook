#!/bin/bash
# preflight_assets.sh — LAUNCH GATE (law 16, "assets-first").
#
# A loop MUST NOT start until the project has real, licensed art on disk.
# Programmer-art primitives (Polygon2D limbs, ColorRect "characters",
# untextured CubeMesh props) are SLOP and are never an acceptable shipping
# target when a CC0/free-to-use asset exists — which it essentially always
# does (see ASSETS.md). The manager may also AUTHOR assets in Blender
# (MODELING.md) — but sourcing free-to-use assets is tried first.
#
# Enforced by run_loop.sh before the GPU slot is claimed. Exit 1 blocks launch.
#
# Usage: preflight_assets.sh <project-root>
set -uo pipefail
ROOT="${1:?usage: preflight_assets.sh <project-root>}"
BRIEF="$ROOT/scripts/ralph/BRIEF.md"
MANIFEST="$ROOT/assets/ASSET-MANIFEST.md"
FAIL=0

say() { echo "preflight_assets: $*"; }

# 1) An asset manifest must exist: what pack, where from, what license.
if [[ ! -f "$MANIFEST" ]]; then
  say "MISSING $MANIFEST — every project declares its art sources."
  say "  Create it: pack name, source URL, license (CC0/CC-BY/…), local path,"
  say "  and which stories consume it. See ASSETS.md for where to source."
  FAIL=1
else
  grep -qiE "cc0|public domain|cc-by|mit|apache|free to use|authored in blender" "$MANIFEST" || {
    say "$MANIFEST names no license — state it explicitly per asset."; FAIL=1; }
  # every declared local path must actually exist
  while IFS= read -r p; do
    [[ -e "$p" ]] || { say "manifest path does not exist: $p"; FAIL=1; }
  done < <(grep -oE '(~|/)[A-Za-z0-9._/\-]+\.(glb|gltf|fbx|usda|usdz|blend|png|jpg|jpeg|webp|svg|ogg|wav|mp3|ttf|otf|woff2)' "$MANIFEST" \
             | sed "s|^~|$HOME|" | sort -u)
fi

# 2) The brief must not specify programmer art as the shipping target.
if [[ -f "$BRIEF" ]]; then
  if grep -qiE "polygon2d limb|colorrect (fighter|character|player)|primitive (mesh|placeholder)|built from (polygon|cube|capsule)" "$BRIEF"; then
    say "BRIEF specifies PROGRAMMER ART as the target — that is slop, rewrite it"
    say "  to name the sourced asset pack and its animation clips instead."
    FAIL=1
  fi
  grep -qiE "asset|sprite|model|glb|texture|atlas" "$BRIEF" || {
    say "BRIEF has no asset section — it must name what art the game uses."; FAIL=1; }
fi

# 3) Real art files must be on disk (not just declared).
COUNT=$(find "$ROOT/assets" -type f \( -name '*.glb' -o -name '*.gltf' -o -name '*.fbx' \
        -o -name '*.usda' -o -name '*.usdz' -o -name '*.blend' -o -name '*.png' \
        -o -name '*.jpg' -o -name '*.jpeg' -o -name '*.webp' -o -name '*.svg' \) \
        2>/dev/null | wc -l | tr -d ' ')
if [[ "${COUNT:-0}" -lt 3 ]]; then
  say "only ${COUNT:-0} art files under $ROOT/assets — source them BEFORE launching."
  FAIL=1
fi

if [[ $FAIL -eq 0 ]]; then
  say "OK — art sourced, licensed, and on disk ($COUNT files)."
else
  say "BLOCKED (law 16). Fix the above, then relaunch."
fi
exit $FAIL
