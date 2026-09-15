# Tooling — agent-drivable 3D toolchains (MCP for the manager, CLI for the loop)

The division of labor, one law: **the bash loop gates through CLI commands;
MCP servers are for the MANAGER tier** (frontier-agent sessions) to inspect a
running game, unstick a rut, and gather critique evidence. A loop story's
verify never depends on an MCP session — MCP is stateful, the loop is not.

Second law: **MCP servers run where the heavy tool runs.** If the editor lives
on a remote box, register the server as `ssh <box> <server command>` (stdio
over SSH) in the agent's MCP config — never run the editor on a laptop.

Stars as of 2026-08-18. Fit beats fame — the most-starred option is not the
loop fit, see Godot below.

## Godot MCP

- **satelliteoflove/godot-mcp (144★)** — the loop/manager fit. Exposes runtime
  introspection, not just editor lifecycle: `godot_exec` (run GDScript in the
  live game), `godot_game_time` (`step_until` — advance N frames deterministically),
  `godot_runtime_state` (scene tree as JSON), input injection,
  `screenshot_game`. Install: `npx @satelliteoflove/godot-mcp` +
  `--install-addon` per project. Requires Godot 4.5+.
- **Coding-Solo/godot-mcp (5.2k★)** — lifecycle-only (launch editor, run
  project, stop). 40x the stars, a fraction of the leverage: you cannot assert
  on game state with it. Use satelliteoflove for anything a judge would read.

## Unity

- **CoplayDev/unity-mcp (13.5k★)** — manager-tier control of the editor.
- The loop tier stays batchmode:

```bash
Unity -batchmode -projectPath "$PWD" -runTests -testPlatform EditMode \
  -testResults results.xml -logFile unity.log -nographics
```

Law: **NEVER trust Unity's exit code.** It exits 0 with failing tests. Parse
the NUnit XML (`results.xml`) — a verify that greps the log instead is a judge
that can't fail (FAILURES.md #23 applies to every engine).

## Blender

- **ahujasid/blender-mcp (26k★)** — interactive sculpting/scene work from a
  manager session; Poly Haven and Hyper3D (Rodin) integrations built in, so
  asset search → import happens in one session.
  Setup gotchas (earned 2026-08-19, Blender 5.2 / blender-mcp 1.29):
  - **GUI Blender is mandatory** — the addon refuses to start its socket in
    background mode ("cannot start server in background mode"). Launch the
    app, then `nc -z 127.0.0.1 9876` to confirm; it auto-starts on load.
  - **Rename the addon file to `blender_mcp.py` before addon_install** —
    single-file addons take the module name from the filename.
  - Curate the tool surface hard for local models: `get_scene_info`,
    `get_object_info`, `execute_blender_code` only (drop the 22
    PolyHaven/Sketchfab/Hunyuan tools). `get_scene_info` has a REQUIRED
    `user_prompt` arg (telemetry hook) — runner must pass it or calls 422.
  - Blender 5.2: render engine enum is `BLENDER_EEVEE` (EEVEE_NEXT is gone);
    `export_scene.gltf(export_apply=True, export_yup=True)` → Godot-clean GLB.
  - Qwen 3.8 27B drove this stack 8 steps / 7 calls / zero malformed to a
    verified crate GLB in 3.6 min — bpy-in-chunks through
    `execute_blender_code` plays to the 27B's strengths.
- The loop tier stays headless bpy:

```bash
blender --background --python gen.py -- --out x.glb
```

Asset generation, normalization (decimate/retarget/export), and the USDA→GLB
conversion (ASSETS.md) are all headless-bpy jobs — deterministic, scriptable,
no session state.

## The 3D verification stack (ordered gates)

1. **Static pre-gate** — `godot --headless --import` (parses every script and
   resource) + a GDScript lint pass (`GDQuest/GDScript-formatter`). Cheap,
   catches parse errors before anything runs. Remember: Godot exits 0 on parse
   errors — grep the output (FAILURES.md #23).
2. **Headless test runner** — GUT (bitwes/Gut, 2.7k★):

   ```bash
   godot --headless -d -s addons/gut/gut_cmdln.gd -gdir=res://tests \
     -gexit -gjunit_xml_file=results.xml
   ```

   or gdUnit4 (1.2k★) when you need its scene-runner input injection
   (simulated keys/clicks inside a live scene).
3. **MCP state assertions** — satelliteoflove tools from a manager session:
   step the game N frames, dump `godot_runtime_state`, assert on node
   positions/counts. This is the "did the thing actually happen" gate for
   stories a unit test can't reach.
4. **Screenshot trap** — Godot 4 headless **cannot rasterize**; a headless
   screenshot is black. Either run with `--rendering-driver vulkan` (needs a
   GPU session, not `--headless`), or Movie Maker mode: `godot --write-movie
   out.avi` renders frame-perfect output headlessly. Choose per box.
5. **VLM judge** — screenshot → local LM Studio vision endpoint, "list the
   tells" prompt. ADVISORY ONLY until calibrated against human scores; the
   mechanical gates above stay the pass/fail authority (the builder never
   grades the build — and an uncalibrated VLM is a builder with eyes).

## Local generation (on the inference box)

- **mflux** — MLX-native image gen; concept art, textures, character concepts
  for the ASSETS.md character pipeline. Runs on Apple silicon, no cloud.
- **VAST-AI-Research/TripoSR** — image → 3D mesh, runs on Mac. Feeds the
  finish pass (decimate/retarget in headless Blender).
- Skip Hunyuan3D-2: better output, but the CUDA friction isn't worth it on an
  all-Apple pipeline. TripoSR quality + a good finish pass ships sooner.
