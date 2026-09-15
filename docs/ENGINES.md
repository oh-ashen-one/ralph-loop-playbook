# Engines & Toolchains

Ranked by how well they fit a small-model Ralph loop. The ranking criterion is
one thing: **how good is the headless, scriptable verify?** A loop is only as
strong as its judge.

## Tier 1 — best fits

### Web (Vite + TypeScript) — the default choice
- Verify: `npx tsc --noEmit` (seconds, surgical errors with file:line), plus
  `npm run build`, plus greps. Best error messages of any stack = best
  self-correction loop.
- The model knows this stack cold. Whole games are possible (we shipped a voxel
  game: chunk meshing, vertex AO, day/night, mobs).
- Landmines: comma-separated class fields (invalid TS the model loves), imports
  after the component body, inventing modules that don't exist. Files >180
  lines truncate — mandate module splits.

### Godot 4 (GDScript) — best native-game fit
- Fully CLI-able: `godot --headless --path game` boots, parses every script,
  runs sim scenes; exit codes + parse errors are scriptable. `--check-only` for
  fast parse gates. Headless full-match/level sims make superb final verifies.
- GDScript is Python-shaped — small models write it well.
- Meshes: pair with Blender CLI (`blender --background --python export.py`) —
  the model writes the export script, the harness runs it. Never let the model
  emit binary .glb.
- Landmines: .tscn is hand-editable text but brittle — prefer code-built scenes;
  @onready references to nodes that don't exist.
- **Godot 4.7 verify gotchas (earned on a shipped Godot 4.7 loop):**
  - `--check-only` (and headless runs generally) **exit 0 even on parse
    errors** — a judge that trusts the exit code can never fail. Grep the
    output for `SCRIPT ERROR|Parse Error|Failed to load script` instead, and
    smoke-test your gate BOTH ways (a judge that can't fail is worse than none).
  - Sim-scene contract: every sim script ends `get_tree().quit(0)` on success,
    `quit(1)` on failure, plus an outer `perl -e 'alarm N; exec @ARGV'` timeout
    and `--quit-after <frames>` as a double safety net.
  - Reference wrappers in `reference/godot/`: verify-parse / verify-gut (Gut
    CLI) / verify-sim, plus the phase-gated runner variant.
  - GDScript landmine list for QWEN.md: `await` not `yield`; floats need
    `0.0`; `Array[Node]` typed-array syntax; signals via `.connect(fn)`;
    no class_name colliding with autoload names; scenes built in code.

### Roblox (Luau + Rojo toolchain)
- Verify: `stylua --check && selene && rojo build && lune run tests` — a
  four-gate chain, all fast, all scriptable (manage via rokit).
- Server-authoritative architecture is a great forcing function for stories.
- CRITICAL: wall off any Open Cloud publish script at the harness level.
  Building locally = loop's job; pushing to a live game = human's job.

## Tier 2 — workable with harness support

### Unity 6 (C#)
- Verify: `Unity -batchmode -nographics -runTests -testPlatform EditMode` +
  `-executeMethod` for custom smoke/build entry points. Slow (minutes/verify)
  but thorough; requires a licensed editor on the box.
- The model must NEVER emit .meta/.unity/.asset/ProjectSettings — Unity
  generates those. All content code-driven: bootstrap MonoBehaviours from code,
  build UI from code, generate materials at runtime.
- EditMode tests (deterministic, no frames) per mechanic story keep the judge
  honest.

### iOS (SwiftUI + xcodegen)
- The model CANNOT write project.pbxproj (machine-generated UUID soup). Use
  **xcodegen**: model emits a 20-line `project.yml`, harness generates the
  project. This single decision took the project from unbuildable to 5 stories
  in 2 hours.
- Verify without simulator runtimes: `xcodebuild -sdk iphonesimulatorX.Y
  CODE_SIGNING_ALLOWED=NO build` — the SDK ships with Xcode; named-device
  destinations need multi-GB runtime downloads.
- Landmines: tuples aren't Hashable (ForEach), missing framework imports,
  invented SwiftData preview initializers.

## Tier 3 — possible, not recommended for small models

### Unreal Engine 5 (C++/Blueprints)
- Headless exists (`UnrealEditor-Cmd -run=`, UAT BuildCookRun, Functional
  Tests) but: C++ compile cycles are minutes-long, error spew is enormous,
  Blueprints are binary (model can't write them), and boilerplate-per-feature
  is huge. A 27B drowns. If you must: C++-only project, one module,
  FunctionalTest-based verifies, expect 3-5× the iterations of Godot for the
  same game. For small-model loops, Godot delivers the same game faster.

### Native consoles / 3DS homebrew etc.
- devkitPro toolchains are scriptable (make-based verifies work) but domain
  knowledge in small models is thin; expect heavy manager staging.

## Cross-cutting rules

- The inference box runs the loop AND the toolchain — no ssh hop in the verify
  path (each hop adds a resolution/timeout failure mode; we hit both).
- Verify wrappers live in `tools/` (write-protected) and must work in
  local mode (`hostname` check) — a wrapper that rsync+ssh'd to a fixed
  hostname silently breaks every judgment when the loop moves to another box.
- Screenshot/capture tooling per engine (playwright for web, --headless
  viewport dumps for Godot, batchmode screenshots for Unity) feeds the critique
  phase — build it once, reuse per project.
