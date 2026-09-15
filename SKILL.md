---
name: ralph-loop-playbook
description: >
  Run autonomous "ralph" coding loops where a small LOCAL model (27B-class,
  e.g. Qwen via LM Studio) builds complete software — especially games — for
  hours without human input, without producing slop. Use when: "ralph loop",
  "run ralph", "overnight loop", "local model builds the project", "PRD
  stories", "autonomous game build", "loop is stuck/rutting", "set up a
  prd.json loop", "small model can't tool-call", or when managing, debugging,
  or supervising an already-running loop. Covers the loop harness, story
  authoring, the manager/overseer tier, asset sourcing, anti-slop design
  bibles, and an 81-entry failure catalog.
---

# Ralph Loop Playbook

A ralph loop spawns a **fresh model instance per iteration** against a
`prd.json` of small stories, each with a **mechanical verify command** that
alone decides pass/fail. The model writes 100% of app code; the harness
enforces what may be written; git is the memory; a manager (human, frontier
agent, or the automated overseer) writes specs and unsticks ruts but never
writes app code. This playbook is distilled from running five real projects
to completion this way. Every rule below was paid for in burned GPU-hours —
the receipt is in `FAILURES.md`.

## When to use a ralph loop

Use it when the work decomposes into many small, mechanically-verifiable
stories (games, web apps, tools) and you want hours of unattended progress
from a cheap local model. Do NOT use it when: the verify can't be scripted
(pure taste work), the task is one big irreducible design decision, or you
can just use a frontier agent directly — the loop's whole economics are
"free local tokens + expensive harness honesty". A loop is only as strong as
its judge: pick stacks where the headless verify is excellent
(`docs/ENGINES.md` ranks them).

## The core loop (what the harness does and why)

1. **Chat completions + `### FILE:` extraction — never tool-calling.** Small
   models can't tool-call reliably. The model streams a reply containing
   `### FILE: path` blocks (whole files) and/or `### PATCH:` blocks
   (exact-match search/replace); the harness parses and writes them. State in
   the story text: "you have NO tools; your reply is written straight to
   disk" — stacked thinking-suppressors flip the chat template into
   tool-call XML mode (FAILURES #28, #34).
2. **Thinking ON, always.** `reasoning_effort: xhigh`,
   `enable_thinking`/`preserve_thinking: true`, NO assistant prefill, no
   suppressor. Suppressing reasoning caused a three-day, all-projects
   quality collapse (FAILURES #42). If files hide in `reasoning_content`,
   fall back to it — don't amputate it. A 30-minute think is NORMAL; chat
   timeout 5400s; never kill a long think (#46).
3. **The ~180-line emission limit is an architecture forcing function.**
   Whole-file emission truncates past ~180-200 lines — attention, not
   tokens. Don't fight it: mandate module splits in stories (you wanted the
   modularity anyway), and use `### PATCH:` blocks for surgery on big files
   (prerequisite: the target pinned verbatim in the snapshot, or every patch
   is a paraphrase that never applies — #27).
4. **Write-fences in the harness, not the prompt.** Prompts are requests;
   the harness is law. Per-story `allowedFiles` (hard write whitelist) +
   `protect` (required-symbol maps, derived by GREPPING the current file,
   never from convention — #29) + harness-path protection (`tools/`,
   `scripts/` never writable) + incomplete-last-file skip + planning-prose
   filter. Fresh instances re-derive the world from priors and WILL rewrite
   good files into imagined versions (law 5).
5. **The verify command is the product spec.** Exit codes are never the
   gate (Godot/GUT/Unity all exit 0 on failures — grep output markers, #23,
   #52). Behavioral gates beat greps: click-throughs, input simulation,
   headless sims with measured numbers (laws 9, 12; #36, #44, #49).
   Red-test every gate: a gate you've never seen fail doesn't work (#56).
6. **Typed exit codes** route the supervisor: 0 normal · 42 all-passed (or
   phase-complete in the phased runner — park for a human checkpoint) ·
   43 everything remaining blocked (escalate) · 44 zero-file format-failure
   streak (continue) · 143 = deliberate manager kill, respawn without
   burning the restart ladder (#73).
7. **`regressionVerify`** (top-level prd command) runs after a story's own
   verify passes, before the pass is banked — the fix-A-break-B killer.
   Plus a force-moved git tag `last-known-green` after every
   regression-green commit, so any corruption can be evaluated against a
   PROVEN-green baseline.
8. **Architect two-pass** at 3 consecutive failures: call A emits only a
   numbered diagnosis/plan (no blocks), call B gets the plan prepended and
   emits only blocks. Diagnosis and emission stop competing for one reply.

## The three roles — never blur them

- **The model** writes 100% of app code, even fixing its own bugs.
- **The manager** writes PRDs, briefs, stories, verify commands, acceptance
  tests, harness patches. Zero authored app lines — except law 13's 1%
  rule: at 2 consecutive same-cause fails the manager may apply a minimal
  proven fix (and encodes it as a FAILURES entry). Cap: 2 interventions per
  story, then restructure the story, never nurse a third (law 14).
- **The judge** is a shell command. Never an opinion, never the model
  grading itself (self-scores run 4+ points high).

## Where everything lives

- `FAILURES.md` — **the crown jewel**: 81 failures, symptom → root cause →
  fix. Read it twice before launching anything.
- `docs/PLAYBOOK.md` — loop anatomy, the 16 laws, phases.
- `docs/HARNESS.md` — every runner defense and why it exists; model config
  preset (8-bit MLX, ctx 262144, xhigh, temp 1.0 / top_p 0.95 / top_k 20,
  max_tokens 65536).
- `docs/MANAGER.md` — the manager seat as a runbook: starting a run,
  handover checklist, the 20-min heartbeat, the 2-fail rule, finishing.
- `docs/PROMPTS.md` — QWEN.md system rules, the story template (manager-
  authored test excluded from allowedFiles, ≤2 emitted files/story), the rut
  playbook in escalation order.
- `docs/ENGINES.md` + `docs/TOOLING.md` — stack ranking by verify-
  scriptability; GUT exit-code lies; Unity XML parsing; xcodegen for iOS;
  Movie Maker mode for headless screenshots; MCP for the manager tier only.
- `docs/OVERNIGHT.md` — the 50-point checklist before any 8-hour run.
  `docs/PREMORTEM.md` — write your own before launch; promote hits to
  FAILURES after.
- `docs/STYLE.md` + `docs/DUSK-STYLE.md` + `docs/CRITIC.md` — the anti-slop
  method: decide everything upstream in a design bible (exact hexes, type
  rules, feel constants, a forbidden-defaults list), then a critique phase
  with canonical screenshots, three lenses, and the provenance test
  ("shipped or AI hobby output? list the tells"). Ship bar: no shot below
  5/9.
- `docs/ASSETS.md` — assets-first (law 16): CC0 sourcing map with scriptable
  download recipes and the real license walls. Programmer art is never the
  shipping target; enforced by `reference/preflight_assets.sh` which BLOCKS
  loop launch until licensed art is on disk.
- `docs/MODELING.md` — Blender constants-first method (real-world dimensions
  as constants, primitives + bevel, verify after every stage, re-open the
  GLB) for when nothing CC0 fits.
- `docs/DEEPSEEK.md` — swapping the loop model (MLX serving gotchas, the
  Metal 499000 resource crash, fork requirements).
- `docs/OPS.md` — phase gates (loop physically cannot run ahead of a human
  checkpoint), GPU slot law (max 2 loops/box, mechanical claims), watchdog
  and pager patterns, the overnight scoreboard ritual.
- `docs/GAUNTLET.md` — the arena build process this derives from (goal+bar,
  builder vs fresh-context critic, blind A/B) and how a 27B loop implements
  it honestly.
- `reference/` — the battle-tested runners, supervisor, scaffold, Godot
  verify wrappers, stuck detector, and prompt templates. Copy the WHOLE
  directory into a project as `scripts/ralph/` — never cherry-pick (#69).
- `quality/` — the law-17 production-quality contract layer: BRIEF template,
  `contract.json` schema + preflight validator (blocks launch), quality
  ledger, prd template with the seven quality story classes, red-spec stubs,
  worked examples.
- `overseer/` — the AI-manages-AI tier: read-only telemetry packet, a
  JSON-action-only manager prompt, a dumb capped executor (2-intervention
  cap it cannot be talked past), event-triggered check-ins, pluggable pager.

## The shortest path to a working loop

1. Install LM Studio, load a 27B 8-bit at ctx 262144, CONFIRM `lms ps`
   identifier→weights (#43). Set `QWEN_MODEL` to your identifier.
2. `reference/scaffold_project.sh <root> <name> [2d|3d]` — full harness,
   quality contract, red-spec stubs, launch-blocking preflights.
3. Source art FIRST (`docs/ASSETS.md`), fill both asset manifests. The
   preflight blocks until you do.
4. Complete `QWEN.md`, `BRIEF.md`, `quality/contract.json`,
   `QUALITY-LEDGER.md`. Write the prd: ≤15 stories, ≤2 emitted files each,
   manager-authored test per story staged in `tests_staged/` and EXCLUDED
   from allowedFiles.
5. Red-test every gate; dry-run ONE iteration before any overnight launch.
6. `RALPH_SLOTS_DIR=~/ralph-slots reference/run_loop.sh <name>` — then work
   the heartbeat + 2-fail rule from `docs/MANAGER.md`, or put the loop under
   `overseer/` management.
7. Finish honestly: full suite + real-launch smoke + CRITIQUE PHASE
   (mandatory — green tests without it is "functional", not done) + human
   playtest. Publishing to any live service is ALWAYS a human decision.
