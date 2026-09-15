# The Playbook

## Anatomy of a loop

```
prd.json (stories, passes flags, verify commands)
   │
   ▼
ralph.sh ──► fresh model instance per iteration (chat completions, NOT tool-calling)
   │             │  reads: story + brief + QWEN.md + source snapshot + progress.txt + LAST_VERIFY.txt
   │             ▼
   │         emits ### FILE: blocks ──► harness writes files (with defenses, see HARNESS.md)
   │             │
   │             ▼
   │         run the story's verify command  ──► exit 0? → commit, passes=true, next story
   │                                              exit ≠0? → LAST_VERIFY.txt, next iteration retries
   ▼
<promise>COMPLETE</promise> when all stories pass → supervisor advances to the next project
```

Chain projects with a dumb bash supervisor: run project loops sequentially,
**one model instance generating at a time** — parallel loops on one box halve
each other's tokens/sec and double wall-clock (we measured it, painfully).

## The three roles — never blur them

1. **The model** writes 100% of app code. All of it. Even fixing its own bugs.
2. **The manager** (you, or a frontier agent) writes: PRDs, briefs, story
   descriptions, verify commands, harness patches, critique findings. When the
   model ruts, the manager tightens the *story*, never touches the code.
   Two curation powers only: delete dead files the model created and won't stop
   tripping on, and `git restore` the model's own earlier commits when it
   clobbers good work. Zero authored lines — with ONE exception (law 13).
3. **The judge** is a shell command. Builds, typechecks, tests, greps. Never an
   opinion, never the model grading itself (self-scores run 4+ points high —
   red-sands measured builders self-scoring 7-8 on work critics scored 2.67).

## Laws (each one paid for in burned iterations)

1. **Small models can't tool-call reliably.** Use chat completions + whole-file
   `### FILE:` extraction. NEVER suppress reasoning (no `</think>` prefill):
   thinking-off is the 2026-08 three-day quality collapse (FAILURES #31).
   Files hidden in `reasoning_content`? Fall back to it — don't amputate it.
2. **Stories must be small.** A story the model can't finish in one ~15KB reply
   thrashes forever. Split by file, then by stage ("STAGE 1: emit only X").
3. **Files over ~180 lines truncate.** Not a token limit — attention. The fix is
   architecture: mandate file splits in the story. This is a feature: it forces
   the modularity you wanted anyway.
4. **The verify command is the product spec.** Anything not asserted will
   regress. `npm run build && grep -q Essay src/app/page.tsx` — chain greps for
   every acceptance criterion. When a critique finds a flaw, its fix becomes a
   permanent assertion (the "immune system": findings die exactly once).
5. **Fresh instances re-derive the world from priors, not from disk.** They will
   rewrite good files into their imagined versions. You need write-fences
   (allowlists), protected symbols, and additive-only rules — in the HARNESS,
   not in the prompt. Prompts are requests; the harness is law.
6. **Every rut has one root cause.** Read LAST_VERIFY + the model's actual reply
   before tightening a story. Name the exact file, the exact line, the exact
   error text in the story description. Vague stories ("polish the page") make
   the model rewrite the world; surgical stories converge in 1-2 iterations.
7. **Iteration counters are cheap, wall-clock is not.** 2759 truncation-skips
   happened before anyone noticed a 600s curl timeout was killing a slow shared
   GPU mid-file. Watch tokens/sec×timeout vs. expected reply size.
8. **The manager's session must be disposable.** State lives in prd.json,
   progress.txt, git, and a HANDOFF.md runbook — any fresh manager (or human)
   resumes from those in one read.
9. **Runtime gates or it didn't happen.** Compile+grep verifies produced a
   landing page whose content rendered in a 144px column, a "browser
   Minecraft" that never booted, and a prayer app with no product in it — all
   fully green. Any story about runtime behavior gates through a probe that
   RUNS the thing (playwright measure, headless sim, simulator screenshot) and
   prints measured numbers on failure so the next iteration reads real data.
10. **The manager writes the acceptance tests, the model makes them pass.**
   Write-protected XCTest / playwright probes that name the exact API the
   story demands (even one that doesn't exist yet) are the strongest anti-slop
   structure we have: the gate becomes the spec, and the model cannot grade
   its own homework.
11. **When a loop ruts, suspect the harness before the model.** Every
   multi-hour rut in this catalog — all of them — was harness or state:
   a lying story, a truncated baseline, a stale doc in the snapshot, a
   thinking-starved reply budget, an impossible protect list, a gate with a
   substring hole. The model was usually doing the best thing available.
12. **The user's first click is the real final gate.** Every gate can be
   green — boot probes, full-match sims, test suites — and the product still
   dies on contact if the first thing the user clicks does nothing. Before
   calling a project done: click through it the way a stranger would (or make
   a probe that does), and make keyboard-first controls discoverable on
   screen. "Works" is defined by their hands, not our harness.
13. **The 1% rule: the manager may break "zero authored lines" when the
   model repeatedly fails one small thing.** Two trigger shapes: (a) the
   invisible meta-failure — a gate that can't fail, a helper verifying the
   wrong directory — the model produces nothing forever, confidently (#52);
   (b) the VISIBLE-but-repeated rut — the model fails the same small thing
   TWICE (an API prior, a one-line wiring fix, a stuck story) and nursing
   it costs more than the fix. **Trigger is 2 consecutive fails on the same
   root cause, not 3+** (user directive 2026-08-20, tightened same day after
   US-107 burned 5 identical fails / ~4h before intervention: "if it fails
   2x, you intervene then to help — we're wasting time at 6"). The second
   identical failure IS the proof of reproduction; waiting for a third buys
   information you already have. Earlier directive, same law: "if you see the
   problem and can fix it fairly quickly, fix it — don't let the local model
   figure it out for hours." Conditions, all mandatory: the root cause is
   PROVEN (reproduced, not plausible, #37); the fix is minimal and surgical;
   every fixed line becomes a FAILURES entry + the error pattern goes into
   the skill file (traps list, checklist, or story template) so the next
   loop never needs it. The 1% exists to shrink itself: measure success by
   how rarely it's needed on the next run.


14. **The escalation cap — a story gets TWO manager interventions, never a
   third.** Tonight's proof: US-015 burned 9 hours and ~9 iterations while the
   manager fixed it one rut at a time (light_energy, randf_vec3, .material,
   scope creep) — each fix defensible, the sum a lost night. After the SECOND
   intervention on one story the manager MUST stop nursing and change the
   structure: split the story smaller, re-spec it with a manager-authored
   test, or drop it to the next run. Count interventions mechanically in the
   prd (`managerInterventions: n` per story, incremented every manager edit).
   Process faithfulness is not progress; the third rut means the story is
   wrong, not the model.
16. **ASSETS-FIRST — programmer art is never the shipping target.** Before
   the brief is written, source real art: CC0/free-to-use packs (ASSETS.md is
   the map), or author it in Blender (MODELING.md) when nothing fits. The
   brief NAMES the pack and the clips/sprites it uses; `assets/ASSET-MANIFEST.md`
   records pack, source URL, license, local path. Enforced, not advised:
   `reference/preflight_assets.sh` runs inside run_loop.sh and BLOCKS launch
   until art is on disk (user directive 2026-08-22: "no fucking slop ever…
   manager models can create assets in Blender if needed but we always steal
   online free-to-use shit"). Rationale, paid for in a full 18h run: a brief
   that says "fighters built from Polygon2D limbs" gets exactly that — the
   model builds what the spec names, the tests assert what the manager wrote,
   and every gate passes on clipart (#77). The anti-slop line "no primitive
   placeholders where a free asset exists" is MANDATORY in every project's
   QWEN.md and must never be edited out when adapting the template.

15. **The acceptance test is part of the SPEC, authored with the story —
   never a rescue move.** Tonight the model wrote both features and tests and
   lost 6+ iterations per story to test-file hallucinations (FAILURES #58).
   New default: when a story is created, the manager writes its test file in
   the same act, leaves it OUT of allowedFiles, and the story text points at
   it as the spec. The model writes game code to a test it cannot game. A
   story whose test doesn't exist yet is an unfinished story.

## Progress + memory between iterations

- `progress.txt`: append-only; one entry per iteration; a "Codebase Patterns"
  section at top for durable learnings. Future iterations read it.
- git: commit per passing story with `feat: [ID] title`. The commit history IS
  the provenance proof that the model wrote everything.
- `LAST_VERIFY.txt` / `LAST_REPLY.md` / `LAST_THINKING.md`: the forensic trio
  for diagnosing ruts.

## Phases per project

1. **Functional** — the PRD stories, ground out by the loop.
2. **Critique** — see CRITIC.md. Screenshots/play, adversarial provenance test,
   findings → new stories with mechanical verifies. Repeat until a pass files
   nothing. Only then is it done.
3. **Ship** — public repo push, builds. Publishing to live services (App Store,
   Roblox, deploys) is ALWAYS a human decision; wall those scripts off from the
   model at the harness level.
