# Ops — phase gates, checkpoints, and phone-visible loops

A loop that runs 8 hours unwatched produces 8 hours of confident slop. These
patterns keep a human's taste in the loop without a human at the desk.

## Phase-gated PRD (the anti-8-hours-of-slop mechanism)

Tag every story with a `phase`. The runner only selects unpassed stories in
the current phase (a one-line `PHASE` file at repo root); when the phase's
stories all pass it exits with a distinct code (42) instead of continuing.
The supervisor catches 42, screenshots, notifies, and **parks in a sleep loop
until a human bumps the PHASE file**. The loop physically cannot run ahead of
approval.

Phase order that works for games: 0 graybox+sims → 1 look (shaders, lighting
presets) → 2 systems → 3 characters/content → 4 arc+polish → 5 critique.
**Lock the look before content**: iterating on shaders over a graybox is cheap;
after 30 content stories it isn't.

## Checkpoint duties (manager, at the halt)

Each checkpoint is more than "keep going?": CP-look is kill-or-continue with
the full lighting-preset shot set; a mid-project CP proposes names/roster (the
model needs them later — record decisions at the top of progress.txt where
every future iteration reads them); the asset-budget CP pipelines ONE paid
generation before approving the batch.

## Phone/pager notifications via any bot CLI

- Text: pipe through a no-LLM CLI send (any chat-bot CLI works —
  `your-bot send --to <channel>`), creds stay on the box that owns them.
- Images: bot CLIs often can't attach; read the bot token server-side and call
  the chat API's photo endpoint directly (e.g. curl a `sendPhoto` endpoint).
  Never let the token appear in another machine's scripts or logs.
- Message taxonomy that works: ✅ per passed story (one line, done/total),
  screenshot set every ~3 passes and at phase ends, 🔁 rut alert at 5
  consecutive fails on one story (include the verify tail — you diagnose from
  the phone), 🛑 checkpoint with images, 🚨 watchdog incidents.

## Watchdog (unchanged laws + two new ones)

Cron on a DIFFERENT machine; one ssh call for vitals; dumb-fix once per new
incident; dead-man threshold > max iteration time. New: (1) a state-file
`started` marker so the watchdog stays silent before the loop's first launch —
you can install ops early without alert spam; (2) vitals include the PRD's
mtime, not just process liveness — a wedged-but-alive loop looks identical to
a healthy one otherwise.

## Screenshot instrument = ops + critique, one build

A headless `sim_shots` scene that renders a FIXED set of named vantages (and
accepts a lighting-preset arg) serves three masters: progress pings, checkpoint
evidence, and the critique phase's comparable canonical shots. Build it as the
very first story (US-000) with a fallback single-frame path so ops work before
the game exists.

## GPU slot law (multi-loop boxes)

Hard cap: **2 loops generating per box** — bandwidth splits evenly, so 2 ≈
half speed each (aggregate equal; fills verify-time gaps), 3+ adds nothing but
timeout-amputated replies. Enforce mechanically, not in prose: a slots dir
(`$RALPH_SLOTS_DIR`, default `~/ralph-slots/`) where claiming = atomic `mkdir slot-<name>` gated on
count < 2 AND queue-head match, each slot records a pgrep pattern so crashed
loops are auto-reaped, and every supervisor claims before its first iteration
and releases via EXIT trap. Loaded-but-IDLE instances cost only RAM; only
GENERATING counts. Choosing 1 vs 2: sequential ships the first project ~2x
sooner; two slots start everything sooner at equal total time — with a queue
of projects, fill both slots; racing one deadline, run one.

## Supervisor: run_loop.sh

`reference/run_loop.sh <name> [iters]` is the dumb supervisor: claims a slot
(dies queued if both are taken, releases via EXIT trap), runs ralph.sh in a
restart loop (max 5 restarts — ralph's exit 1 means crash OR budget exhausted,
either way it gets a fresh budget), and routes the typed iteration exits that
ralph.sh now propagates: 0 = continue if prd.json still has unpassed stories,
42 = done, 43 = all remaining stories blocked → runs stuck_detector and prints
ESCALATE (human territory), 44 = format-failure streak → keep going.

## Stuck detector + trajectory postmortem

`reference/stuck_detector.py [trajectory.jsonl]` — stdlib, no LLM. Classifies
the last ~20 trajectory events into the four ruts (identical emission,
zero-file streak, pass/fail oscillation, repeated identical failure) and prints
`{stuck, pattern, suggestion}`. run_loop.sh runs it every 10 rounds and on
every 43; run it by hand whenever a loop "feels" slow.

Postmortem workflow when a loop ruts overnight:

1. `stuck_detector.py` for the pattern.
2. `jq -r 'select(.verify_ok==false) | [.iteration,.story_id,.exit_status] | @tsv' scripts/ralph/trajectory.jsonl | tail` for the failure shape.
3. Read the forensic trio (LAST_VERIFY / LAST_REPLY / LAST_THINKING) for the
   LAST iteration only — earlier ones are in git + the trajectory.
4. Manager move from the rut playbook (PROMPTS.md); a blocked story gets
   unblocked by editing the story and clearing `"blocked"`, never by nudging
   the model.

## Overnight scoreboard ritual

Morning check, in order, from the phone or the desk:

1. `jq '[.userStories[] | select(.passes)] | length' prd.json` — passes count.
2. `git log --oneline -10` — the commit cadence IS the health metric; a quiet
   night with commits is fine, a busy night without them is a rut.
3. `jq '.userStories[] | select(.blocked) | {id, blocked_reason}' prd.json` —
   the blocked list is your work queue; each one names its own verify tail.
4. stuck_detector verdict + `lms ps` (right model still loaded? FAILURES.md #32).

**Pause sentinel:** `touch $RALPH_SLOTS_DIR/PAUSED` freezes every `claim.sh`
box-wide (each waiter re-checks every 120s); `rm` it to resume. This is the
only pause that survives other manager sessions re-queuing loops — killing
processes alone does not (failure 40). Running loops still finish; the
sentinel stops new claims, so pair it with the kill order below for a hard
pause.

**Hard-pause order** (from failure 40): 1) find respawners — take the ppid of
anything that comes back after a kill; chain scripts and queued-start waiters
outlive their children — and kill wrappers first; 2) supervisors + claim
waiters; 3) `qwen_iteration` workers; 4) `lms unload --all`; 5) re-verify
BOTH `pgrep` and `lms ps` a few minutes later — backlogged commands (e.g.
from a stopped tmux server, failure 39) can resurrect either.

**Stale slot-holders:** reaping is pgrep-based, so an alive-but-wedged
supervisor holds its slot forever (failure 41). The watchdog should also
alert on slot-holder log mtime stale > 30 min while the queue is non-empty.

