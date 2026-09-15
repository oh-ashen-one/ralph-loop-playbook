# Prompts & Stories

## QWEN.md (the per-project system rules)

Keep it under ~60 lines. Non-negotiables:

- "You are a FRESH agent. Memory is only: prd.json, progress.txt, git,
  LAST_VERIFY.txt, the brief, the snapshot."
- The FILE-block format, with: reply MUST start with `### FILE:`; close fences
  before `### END FILE`; never emit a truncated file — omit the block instead.
- One story per iteration. No placeholders, no "rest here", no `...`.
- Echo the authoritative `VERIFY:` line verbatim as the last line.
- "If LAST_VERIFY.txt exists, fix THAT failure."
- Per-stack landmine list (see ENGINES.md) — e.g. "never emit .meta/.pbxproj",
  "AVSpeechSynthesisDelegate needs import AVFAudio", "class fields cannot be
  comma-separated in TS".
- Anti-slop line: name the clichés your stack produces ("no Inter, no purple
  gradients, no three equal feature cards") — small models emit the median of
  their training data unless you explicitly forbid the median.

## The story template (post-2026-08-19 — these are defaults, not options)

Every story object ships with:
1. `testFile` — the acceptance test, MANAGER-AUTHORED at story-creation time
   (law 15), already on disk, parsing clean, currently RED. Never let the
   model write the test for a story that touches a framework assert API.
2. The test file is EXCLUDED from `allowedFiles` — the model cannot edit the
   spec to fit its code.
3. Sizing for juice/polish stories: ONE node, ONE behavior, ONE gate. Tonight
   failed because stories bundled 2 files × 3 behaviors × a test — each extra
   element multiplies hallucination surface and think-spiral length.
4. `managerInterventions: 0` — incremented by the manager on every edit;
   at 2 the story is restructured, not nursed (law 14).

## Writing stories

A story is a *contract*: description (what + how well) + acceptanceCriteria +
verify (the machine translation of the criteria) + priority + `passes: false`.

- Scope: one sitting's work for a careful junior — one subsystem, 1-4 files.
- Put exact filenames in the description. Put the design-bible values inline
  when the story is visual ("selected slot gets thick #F5842D border").
- Verify = build/test command AND a grep per acceptance criterion. A verify
  that passes on an empty scaffold is a bug in YOUR code.

## Generation settings (prompt-adjacent, non-negotiable)

- `reasoning_effort: xhigh` is the default, always. Speed is free (the box
  runs 24/7), quality isn't. A 30-minute think on one story is normal; never
  trade thinking for wall-clock. PENDING A/B (post-run review): community
  measurement claims `medium` costs no measurable quality at ~1/3 less wait.
  Test ONE night, same stories class, honest gates as the judge — if medium
  passes clean it becomes the default; do not switch on vibes.
- No assistant prefill, no thinking suppressor. The visible reply carries the
  FILE blocks; reasoning_content is where the quality lives.
- **Prefix pinning.** Static prompt parts first (QWEN.md, brief, story, verify
  line, snapshot), volatile parts last (progress.txt tail, LAST_VERIFY.txt).
  LM Studio's prompt cache matches from the front — a stable prefix turns
  minutes of re-prefill into a cache hit.

## The grounding file goes IN the prompt, not in the repo

reference/GODOT_API.md only works if the model SEES it — a grounding doc on
disk changes nothing (learned 2026-08-19: three trap classes killed 7
iterations while GODOT_API.md sat in the repo). Copy the trap section into
the project's QWEN.md (every-prompt system rules) whenever a new API trap
costs an iteration. The repo file is the master list; QWEN.md is the
injection point.

## The architect two-pass (automatic at 3 consecutive failures)

When a story fails 3 times in a row the runner splits the iteration: call A
diagnoses and writes a numbered plan (no FILE/PATCH blocks allowed, under 40
lines, saved to LAST_PLAN.md); call B gets the plan prepended to the normal
prompt and must emit only blocks. Diagnosis and emission stop competing for
one reply. Manager takeaway: if the two-pass still fails, the story is lying —
reread it against the actual tree before the 5-fail block fires.

## The rut playbook (manager moves, in escalation order)

1. **Name the error.** Paste the exact compiler error, file, and line into the
   story description. 80% of ruts die here.
2. **Shrink the emission.** "Emit EXACTLY ONE file: X. Do not emit Y or Z."
   Enforce with `allowedFiles` — the model WILL ignore the prose sometimes.
3. **Stage the story.** "STAGE 1: only the small shared-module extension.
   STAGE 2: the consumer." Re-edit the same story between stages; the runner
   re-reads prd.json every iteration.
4. **Mandate a split.** If a file truncates repeatedly it is too big for the
   model's attention — instruct extracting a module ("move inventory UI to
   inv.ts, under 180 lines"). You get better architecture for free.
5. **Spell the contract in words.** For an error that survives multiple
   phrasings, state the type-level truth: "itemIcon(id) returns a NUMBER, never
   a canvas. Create a canvas locally, draw, and return THE CANVAS."
6. **Protect what keeps breaking.** `protect: {"src/blocks.ts": ["itemIcon",
   "maxStack"]}` — additive-only evolution of shared modules, enforced.
7. **Curate, never author.** Dead unreferenced file the model keeps tripping
   on → delete it. Good file clobbered → `git restore` the model's own commit.
   Then run the verify verbatim yourself; if it exits 0 the story passed on its
   own terms — flip it and let the supervisor advance.

## Design bibles (BRIEF.md)

The model has no taste; it has obedience. Move ALL taste upstream:

- One-line vision ("painted-desert voxel world at golden hour").
- Exact hex palettes, type rules, panel rules — values, not adjectives.
- Feel numbers: FOV, gravity, timing curves, particle counts. "Game juice" is
  a table of constants; write the table.
- Signature element the artifact will be remembered by.
- What NOT to do (the slop list for this medium).

A generic brief produces a generic artifact from ANY model. Write the brief
you'd hand a talented contractor who has never seen your taste.
