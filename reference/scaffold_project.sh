#!/bin/bash
# scaffold_project.sh — start a new Ralph game project with every earned
# defense wired in from minute one. Run this instead of hand-assembling a
# project; hand-assembly is how guards get skipped (FAILURES #69, #77).
#
#   scaffold_project.sh <project-root> <project-name> [2d|3d]
#
# Produces:
#   scripts/ralph/{runner, supervisor, gates, preflight, QWEN.md, BRIEF.md, prd.json}
#   assets/{ASSET-MANIFEST.md,asset-manifest.json}
#   quality/{contract.json,QUALITY-LEDGER.md} + hard-gate sentinel
#   tests/ tests_staged/
# and leaves the loop BLOCKED until real licensed art, tests, budgets and
# canonical evidence contracts are complete (laws 16-17).
set -uo pipefail
ROOT="${1:?usage: scaffold_project.sh <project-root> <project-name>}"
NAME="${2:?usage: scaffold_project.sh <project-root> <project-name>}"
DIMENSIONS="${3:-3d}"
if [[ "$DIMENSIONS" != "2d" && "$DIMENSIONS" != "3d" ]]; then
  echo "scaffold_project: dimensions must be 2d or 3d" >&2
  exit 1
fi
REF="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "$ROOT/scripts/ralph" "$ROOT/assets" "$ROOT/quality/references" "$ROOT/tests" "$ROOT/tests_staged" "$ROOT/tools"

# Escape manager-supplied values for sed replacement templates.
ESCAPED_NAME="${NAME//\\/\\\\}"
ESCAPED_NAME="${ESCAPED_NAME//&/\\&}"
ESCAPED_NAME="${ESCAPED_NAME//|/\\|}"
render_template() {
  sed -e "s|{{PROJECT}}|$ESCAPED_NAME|g" -e "s|{{DIMENSIONS}}|$DIMENSIONS|g" "$1" > "$2"
}

# Harness: copy the WHOLE reference dir — never cherry-pick files (#69: a
# missing strip_markers.py killed every iteration of a fresh project).
cp -R "$REF"/* "$ROOT/scripts/ralph/"
rm -f "$ROOT/scripts/ralph/scaffold_project.sh"
chmod +x "$ROOT/scripts/ralph"/*.sh "$ROOT/scripts/ralph"/godot/*.sh 2>/dev/null

# QWEN.md from the template, with the anti-slop block already in it.
render_template "$REF/QWEN-TEMPLATE.md" "$ROOT/scripts/ralph/QWEN.md"
rm -f "$ROOT/scripts/ralph/QWEN-TEMPLATE.md"

# Production brief: every section stays blocked until the manager replaces the
# explicit FILL_ME contracts with values and measurements.
if [[ ! -f "$ROOT/scripts/ralph/BRIEF.md" ]]; then
  render_template "$REF/quality/BRIEF.template.md" "$ROOT/scripts/ralph/BRIEF.md"
fi

# Asset manifest stub — the gate reads this.
if [[ ! -f "$ROOT/assets/ASSET-MANIFEST.md" ]]; then
cat > "$ROOT/assets/ASSET-MANIFEST.md" <<MAN
# ASSET MANIFEST — $NAME

Required by law 16. The loop is blocked until every row is real and on disk.

| Asset | Source URL | License | Local path | Used by |
|---|---|---|---|---|
| FILL_ME | FILL_ME | FILL_ME | FILL_ME | FILL_ME |

Programmer art (Polygon2D limbs, ColorRect characters, untextured primitives)
is never a shipping target.

The machine-readable source of truth is \`assets/asset-manifest.json\`; every
shipping file is hashed and explicitly approved there.
MAN
fi

[[ -f "$ROOT/assets/asset-manifest.json" ]] || \
  render_template "$REF/quality/asset-manifest.template.json" "$ROOT/assets/asset-manifest.json"
[[ -f "$ROOT/quality/contract.json" ]] || \
  render_template "$REF/quality/contract.template.json" "$ROOT/quality/contract.json"
[[ -f "$ROOT/quality/QUALITY-LEDGER.md" ]] || \
  render_template "$REF/quality/QUALITY-LEDGER.template.md" "$ROOT/quality/QUALITY-LEDGER.md"
[[ -f "$ROOT/scripts/ralph/prd.json" ]] || \
  render_template "$REF/quality/prd.template.json" "$ROOT/scripts/ralph/prd.json"
[[ -f "$ROOT/scripts/ralph/PHASE" ]] || printf '1\n' > "$ROOT/scripts/ralph/PHASE"

# Manager-owned acceptance specs start RED and unimplemented. The quality gate
# rejects these stubs; Qwen never sees a writable test spec.
for test_name in \
  test_q01_vertical_slice.sh \
  test_q02_look_lock.sh \
  test_q03_asset_integration.sh \
  test_q04_feedback_atom.sh \
  test_q05_camera_input.sh \
  test_q06_performance_resilience.sh \
  test_q07_critique_ship.sh; do
  if [[ ! -f "$ROOT/tests_staged/$test_name" ]]; then
    cp "$REF/quality/red_test_stub.sh" "$ROOT/tests_staged/$test_name"
    chmod +x "$ROOT/tests_staged/$test_name"
  fi
done

# New projects require the full quality contract before run_loop claims a GPU.
touch "$ROOT/.ralph-quality-required"

echo "scaffolded $NAME at $ROOT"
echo
echo "NEXT, in order (MANAGER.md 'starting a run'):"
echo "  1. Source the art. Fill both asset manifests + BRIEF asset roles."
echo "  2. Complete QWEN engine laws, BRIEF.md, quality/contract.json + QUALITY-LEDGER.md."
echo "  3. Replace every FILL_ME in the seven quality stories; <=2 emitted files."
echo "  4. Author EVERY acceptance test in tests_staged/ up front (law 15),"
echo "     tolerance-first where later stories change flow (#75)."
echo "  5. RED-TEST asset, quality, and story gates (#56), then dry-run one iteration."
echo "  6. Launch: run_loop.sh $NAME  (laws 16-17 preflights run first)"
bash "$REF/preflight_assets.sh" "$ROOT" || echo "(expected: gate blocks until you do step 1)"
python3 "$REF/quality/preflight_quality.py" --root "$ROOT" --max-errors 12 || \
  echo "(expected: quality gate blocks until you complete steps 1-5)"
