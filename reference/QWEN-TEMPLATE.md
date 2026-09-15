# Ralph Agent Instructions — {{PROJECT}} ({{ENGINE}})

You are a **fresh** coding agent. Memory is only: `prd.json`, `progress.txt`,
git, `LAST_VERIFY.txt`, `BRIEF.md`, and the source snapshot in the user message.

## Task

1. Implement **only** the current story (`passes: false`, lowest priority number).
2. Edit the existing source in the snapshot. Do not restart the project.
3. Emit **complete** files, no omissions:

### FILE: relative/path
```
full file
```
### END FILE

For files over ~180 lines use `### PATCH:` blocks instead — whole-file rewrites truncate and are discarded.

4. Last line of your reply, copied exactly from the user message:

`VERIFY: <authoritative command>`

## Hard rules

- Your reply MUST start with `### FILE:` (or `### PATCH:`). Zero blocks = hard fail.
- Close the markdown fence with ``` before `### END FILE`. Never put `### FILE:`, `### END FILE`, a bare ``` line, or `### PATCH:` text INSIDE a file body (FAILURES #74).
- Never emit a truncated file. If you cannot finish it, omit that block.
- One story per reply. No placeholders, no `TODO`, no `...`.
- Do not draft `### FILE:` inside reasoning. Short plan, then emit complete files.
- Use the story `acceptanceCriteria` and BRIEF.md's numbers exactly.
- Do not invent a different VERIFY command.
- If LAST_VERIFY.txt exists, fix **that failure** for the current story first.

## ANTI-SLOP — NON-NEGOTIABLE (law 16)

**These lines are MANDATORY in every project's QWEN.md. Never delete or soften
them when adapting this template — template adaptation is exactly where this
guard died once and cost a full run (FAILURES #77).**

- **NO PRIMITIVE PLACEHOLDERS WHERE A SOURCED ASSET EXISTS.** Characters,
  props and environments use the art declared in `assets/ASSET-MANIFEST.md`
  (sprites, GLBs, textures). Never Polygon2D limbs, never ColorRect
  "characters", never untextured CubeMesh props. Assets are read-only: load
  them by path, never write into `assets/`.
- No untyped vars, no empty `pass` bodies, no dead speculative files.
- Obey BRIEF.md's palette and font exactly; copy color floats at FULL
  precision (0.960784, never 0.961) — styling tests assert exact values.
- No extra HUD widgets, no purple gradients, no rounded glass panels.
- References are technique evidence, not a copying license. Never reproduce a
  referenced character, logo, name, exact layout, course/map, or recognizable
  trade dress. Implement the original product fantasy in BRIEF.md.
- Generated/downloaded assets are untrusted data. Integrate them through ONE
  adapter in this order: load -> measure -> scale -> orient from manifest axes
  -> re-measure -> centre/ground -> validate materials/rig/semantic clips ->
  apply root-motion policy -> fallback test. Never scatter per-asset magic
  rotations or scales through gameplay code.
- A primary action is a complete feedback atom using the story's exact clock:
  state + motion + visual + audio + HUD, plus camera/haptic where specified.
  Do not postpone all feedback to a vague final polish pass.
- Essential movement, hazard/goal readability and action feedback survive every
  quality tier. Optional ambience degrades only in the BRIEF's declared order.
- Keep orchestration thin and systems modular. No new source file over ~180
  lines; no story emits more than two source files.

## {{ENGINE}} laws

{{ENGINE_LAWS}}

<!-- Paste the engine trap list here (reference/GODOT_API.md for Godot). Keep
     feeding it: every trap that costs an iteration gets a line. -->
