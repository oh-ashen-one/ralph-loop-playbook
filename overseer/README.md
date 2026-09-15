# The Overseer — an AI manager that watches an AI builder

The ralph loop's local model writes 100% of the app code. This directory is the
**manager tier as a machine**: a frontier/cloud model that watches the loop's
telemetry and intervenes — but only through a dumb, capped executor that can
refuse it. The overseer never writes app code either.

The pattern, in one line: **the smart model proposes structured actions; a dumb
script disposes.** The smart model is read-only against the world. All state
mutation lives in one small auditable file.

## Files

- `packet.sh <project_root>` — read-only telemetry. Emits one JSON object:
  loop liveness, whether YOUR model identifier (not just the server) is being
  served, prd pass/block/intervention counts, trajectory tail, zero-file
  streak, passes-vs-iterations over the last 3h, the stdlib stuck-detector
  verdict, slots/queue, and forensic tails (LAST_VERIFY, progress, last
  commit). Never touches loop state.
- `manager_prompt.md` — the overseer model's runbook. Encodes the laws from
  the failure catalog (2-fail rule, 2-intervention cap, "healthy process +
  zero passes = failing run", "suspect the harness before the model") and a
  hard output contract: **the entire reply is one JSON array of actions, no
  prose**.
- `checkin.sh <project_root> [--dry-run]` — one full check-in: packet →
  overseer model → extract first JSON array (the model WILL wrap it in prose
  sometimes) → executor. Set `RALPH_MANAGER_LLM_CMD` to any CLI that reads a
  prompt on stdin and writes a reply on stdout.
- `watch.sh <project_root>` — event-triggered early check-in. Fires only when
  a mechanical trigger holds (loop dead with stories remaining, stuck detector
  fired, 3+ iterations and 0 passes in 3h). Dedupes to one check-in per 45
  min per project. Silent otherwise — cron it every 5 minutes.
- `executor.py <project_root> [--dry-run]` — the ONLY path that mutates loop
  state. Validates each action against the caps and applies it. Everything —
  applied, refused, capped, paged — is appended to an audit log
  (`RALPH_MANAGER_LOG`, default `~/ralph-overseer/overseer-log.jsonl`).
- `install.sh <project_root> [...]` — registers hourly check-in + 5-min watch
  in crontab, idempotently (marker block).
- `pager.example.sh` — the human-paging hook. Point `RALPH_MANAGER_PAGER` at
  your own script (chat webhook, push service, email — anything that takes
  the message as `$1`).

## The action schema (the whole contract)

```json
[]                                              — healthy; the correct answer most of the time
[{"action":"edit_story","id":"US-xxx","append":"surgical text naming exact file/line/error"}]
[{"action":"unblock","id":"US-xxx","note":"why it is safe to retry"}]
[{"action":"kill_iteration"}]                   — in-flight iteration is running on stale rules
[{"action":"relaunch_loop"}]                    — loop dead, stories remain
[{"action":"page_human","reason":"one factual sentence"}]
```

## The caps (executor-enforced — the model cannot talk its way past them)

- `edit_story` / `unblock` count as interventions: **max 2 per story, ever**
  (tracked as `managerInterventions` in prd.json). At the cap the executor
  refuses and pages: restructure the story, don't nurse it.
- `kill_iteration` only when this project's supervisor is alive AND exactly
  one iteration process exists box-wide — it refuses to guess which process
  to kill.
- `relaunch_loop` only when the loop is actually dead.
- Non-JSON replies are rejected and logged; unknown actions are dropped.
- When in doubt between acting and paging: page.

## Why this shape (each property was paid for)

- **JSON-action-only output** — prose replies can't be validated. A schema
  can. The executor is the policy; the model is an advisor.
- **Dumb capped executor** — the failure catalog's worst manager mistakes were
  all "nursed a rut too long" or "acted on a plausible-but-unreproduced
  diagnosis". Caps make over-intervention mechanically impossible.
- **Event-triggered check-ins** — polling hourly misses a rut's second fail;
  polling every 5 min is noise. Mechanical triggers (dead loop, stuck
  detector, 0 passes in 3h) fire the expensive model call exactly when it's
  worth one.
- **Telemetry asserts YOUR identifier, not server liveness** — a shared
  inference server answers 200 while serving someone else's model; the loop
  burns rounds against HTTP 400. `model.served` checks the identifier string.
- **Everything dry-runnable** — `--dry-run` on checkin and executor prints
  what WOULD happen. Always dry-run by hand before trusting the cadence
  overnight.
