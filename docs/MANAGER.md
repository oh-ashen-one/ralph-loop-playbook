# MANAGER.md — the manager/monitor tier, as a runbook

How a frontier agent (Claude, Codex, Kimi, a human) runs the manager seat of a
Ralph loop: watching a local model build for hours, deciding when to touch the
work, and leaving every lesson behind for the next session. Written after a
27-story Godot run finished 27/27 with the loop crossing THREE different
manager sessions (frontier agents swapping mid-run) without losing state.

The loop's anatomy is PLAYBOOK.md. This file is the seat you sit in while it
runs. Treat it as a skill: load it, follow it literally.

## The role in one paragraph

You do not write app code. The local model writes every line of the game; you
watch its telemetry, run its gates, keep its harness honest, and intervene
surgically when — and only when — the mechanical trigger fires (below). Your
real output is not the game: it is FAILURES entries, trap-list lines, and law
amendments, pushed to this repo so the next run never re-pays for tonight.
Measure yourself by how little the next manager needs to do.

## Starting a run (do these IN ORDER — skipping is how runs go wrong)

`reference/scaffold_project.sh <root> <name> [2d|3d]` does step 0 for you: full
harness copy (never cherry-pick — #69), QWEN.md with mandatory anti-slop and
originality guards, production BRIEF, human + machine asset manifests, quality
contract/ledger, seven phase stories, red-spec stubs, and both gates wired.

1. **ART FIRST — before a single story is written (law 16).** Source CC0 /
   free-to-use packs (ASSETS.md is the map); author in Blender (MODELING.md)
   only when nothing fits. Fill `assets/ASSET-MANIFEST.md` and
   `assets/asset-manifest.json`: source URL, license, local path, SHA-256,
   `shipApproved`, semantic role, fallback, and for 3D size/axes/root motion +
   complete character clip roles. `preflight_assets.sh` blocks until art is
   real; `preflight_quality.py` verifies the machine registry.
2. **Rules + BRIEF + quality contract**: resolve the engine/trap placeholders
   in `scripts/ralph/QWEN.md`; complete `scripts/ralph/BRIEF.md`,
   `quality/contract.json`, and `quality/QUALITY-LEDGER.md`. Translate every
   "realistic/cinematic/high quality" claim into values, named evidence and a
   gate. References say both what to learn and what IP/trade dress not to copy.
3. **prd.json**: fill the scaffolded seven quality classes; add game-specific
   micro-stories, always **≤2 emitted files each** (#74). A 4-file feature is
   two stories. Asset/feedback/evidence/performance ids resolve to the contract.
4. **Author every acceptance test up front** in `tests_staged/` (law 15),
   staged per story (#59), tolerance-first wherever a later story will
   legally change earlier timing (#75).
5. Run and red-test all preflights: `preflight_assets.sh`,
   `quality/preflight_quality.py`, every manager spec, then **dry-run one
   iteration** (#69) before any overnight launch.
6. Launch, then work the heartbeat + 2-fail rule below.

## Taking over a running loop (the handover checklist)

Any session can pick up any loop mid-run because the state lives on disk, not
in a conversation. In order:

1. **Re-derive live state from the machine, never from prose.** A handoff doc
   is a snapshot with a date; ours said "loop PAUSED" while the loop had been
   running 2.5h. Trust: `pgrep -f ralph.sh`, `pgrep -f qwen_iteration`,
   `prd.json` (passes/blocked/managerInterventions per story),
   `progress.txt` (iteration log), `trajectory.jsonl` (durations,
   think/reply bytes), `LAST_VERIFY.txt` (current failure), `git log`.
2. **Read timestamps in the file's own timezone.** progress.txt logs UTC; the
   box runs local. A 4h misread makes a healthy iteration look hung and
   invites a needless kill.
3. **`git pull` this repo** — the other session may have pushed laws you don't
   have. Read FAILURES.md before touching anything.
4. **Check the model route**: `curl -s http://127.0.0.1:1234/v1/models` (or
   your server) returns 200 and the identifier maps to the weights you think
   (FAILURES #32).
5. **Know what is off-limits** on the box (other tenants' model instances,
   launch agents, ports). Read the machine's AGENTS.md / LOCAL-MODELS.md first.

## The heartbeat (monitoring that actually detects things)

One status line every 20 minutes. That cadence has now caught a silent
supervisor death (#63) and paced three interventions; shorter is noise, longer
misses a rut's second fail. Each beat carries, in one line:

- supervisor alive? (pgrep the loop script)
- current iteration age (pgrep the iteration process)
- model server HTTP status
- banked count / total, current story, its `blocked` flag and intervention count
- the last 2 progress entries (story id + verify_ok)

Build it as a detached watcher process, not a chain of manual checks.
Two traps we paid for:

- **pgrep self-match**: if your watcher's own command line contains the
  pattern it greps for, it reports its own age as the iteration's. Use
  bracket-armor: `pgrep -f "qwen_iteration[.]py"`. Our monitor lied for 2h
  before this was caught.
- **Silence must be distinguishable from health.** The beat must say "loop
  DOWN" explicitly, not just stop mentioning it.

While a generation is in flight, liveness = the think/reply stream file is
growing (`ls -la` twice, 20s apart), not process existence. 30-45 min
generations are NORMAL at 27B with thinking on (#46); check growth before
assuming a hang.

## The 2-fail rule (law 13b, amended — the core of the seat)

**Trigger: the same story fails twice in a row on the same root cause. Not
3+, not "give it one more round" — two.** The second identical failure IS the
reproduction proof (#37's bar); every fail after it buys information you
already have. History: US-107 burned 5 identical fails / ~4h under manager
observation before intervention; under this rule that's ~1h. The night the
rule was written, it fired three times, each at exactly fail #2, and every
single rut turned out to be a trap or a spec bug — not a model capability gap.

On trigger:

1. **Kill the in-flight attempt** (`pkill -f <iteration-script>`). It was
   spawned with pre-diagnosis context and will fail the same way; the
   supervisor respawns fresh. Also kill and respawn after YOU change files —
   an old attempt's emission will clobber your fix (it snapshots context at
   spawn).
2. **Diagnose structurally, not from the log tail.** The fastest diagnoses
   tonight were one-liners:
   - scene rut: `git show HEAD:file.tscn | grep '^\[node'` vs
     `grep '^\[node' file.tscn` — a structural diff names in seconds what 200
     lines of test backtrace bury (#65).
   - "how long is this really taking": read `trajectory.jsonl` durations, not
     your gut.
3. **Suspect the spec before the model** (#61, #67). Probe the manager-authored
   acceptance test against a known-correct hand implementation. Twice now the
   test itself was unpassable-by-construction (a boot-order bug; polling a
   flag that only exists synchronously). Test files are manager-owned (law
   15) — fixing them is your lane and does not count against the model.
4. **Fix minimally, in this order of preference:**
   a. **Curation** — `git checkout -- <file>` back to banked state. US-113's
      whole fix was this: the model kept mangling a file that needed ZERO
      changes.
   b. **Restore + graft** — checkout the banked file, hand-add only what the
      story asks (US-107: one particle node + one handler block).
   c. **Spec repair** — fix the manager test / story text.
   Never refactor, never improve, never touch files the story doesn't name.
5. **Run the story's verify verbatim, then the FULL suite.** A scoped pass
   with a broken sibling is not a pass. Godot: `--import` before the suite
   after any git operation (#62 — stale class cache masked a dropped
   class_name through TWO banked stories).
6. **Log it**: increment `managerInterventions` in prd.json with a dated
   note naming root cause and fix; commit with `[US-nnn]` + law reference.
7. **Encode it**: same sitting, write the FAILURES.md row and the trap-list
   line (QWEN.md / GODOT_API.md), and push. A fix that isn't encoded will be
   re-paid by the next run. Rule of thumb from tonight: *watching a diagnosed
   rut is not monitoring — it is spending GPU-hours to re-learn a known
   fact* (#66).

The cap still holds (law 14): two interventions per story, then the story is
mis-specified — split or re-spec it, don't nurse a third.

## Harness bugs are yours, immediately

The harness (iteration runner, verify wrappers, supervisor) is manager-owned
infrastructure — the 2-fail rule doesn't apply, fix on first diagnosis. When a
crash self-names via traceback armor (#63: an unguarded `parts[0]`), patch
every copy (project + this repo's reference/), **red-test the fix** (feed it
the crashing input, watch it return clean), and mark the FAILURES row
RESOLVED. Arm traceback logging on any recurring mystery crash — one crash
with a traceback beats weeks of guessing.

## Trap-encoding: where each lesson goes

| Lesson type | Destination |
|---|---|
| Engine/API misuse the model repeats | project trap file (QWEN.md) + reference/GODOT_API.md |
| A failure mode with symptom/cause/fix | FAILURES.md row (numbered, terse, greppable) |
| A change to how the loop is RUN | PLAYBOOK.md law amendment (quote the directive and date) |
| The story of a session, with timings | SESSIONS.md block (newest first, sign it — say which model/agent wrote it) |
| Manager-authored acceptance tests | project `tests_staged/`, staged per-story (never all at once — #59) |

Push after every encoding batch. Other sessions `git pull` this repo as their
first act; unpushed knowledge doesn't exist.

## Finishing a run (the last 30 minutes)

"All stories pass" is not done (#52 was a fake-green 14/14):

1. Full suite, zero SCRIPT ERROR / Parse Error lines — grep the output, don't
   trust exit codes.
1b. **THE CRITIQUE PHASE — mandatory, never skip (#76).** Capture every state
   named in `quality/contract.json` plus primary-action motion strips, LOOK at
   them, judge against the BRIEF/reference lock, and file every flaw
   as a new story with a mechanical assert where one exists (camera zoom
   range, node existence, exact colors, bounding-box sizes). Then relaunch
   the loop — the MODEL writes the polish. Green tests without a critique
   pass is "functional", and functional is not done.
2. **Real-launch smoke test**: run the actual game (not headless-import, the
   real window) ~30s, then grep the log for errors. This is the gate that
   caught the fake-green run.
3. Bank the final story with its log; commit.
4. Stop the loop cleanly: supervisor first, then iteration; verify with
   pgrep; confirm the GPU slot is released.
5. Write the SESSIONS.md completion addendum WITH TIMINGS (wall hours,
   iteration count, pass rate, interventions) — the next run calibrates its
   overnight expectations from these numbers.
6. Push. Then tell the human it's done, plainly, with the numbers.

## Calibration numbers (Apple-silicon box, Qwen 3.8-27B 8-bit, thinking on)

From that 27-story close-out: a healthy mid-run story
passes first-try in 12-40 min; a rutted story costs ~30-40 min per failed
attempt; manager intervention ~15-30 min including gates and encoding. The
handover-to-done stretch: 7.5h wall, 11 iterations, 4 model passes, 3
interventions. A model that ruts twice per evening and passes everything else
first-try is a NORMAL good night, not a problem.
