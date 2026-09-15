# The Harness

`reference/qwen_iteration.py` is a battle-tested runner. This file explains every
defense in it and why it exists. If you write your own runner, you will re-earn
each of these the hard way; copy ours instead.

## Core mechanics

- **Transport**: raw chat-completions against an OpenAI-compatible local server
  (LM Studio `:1234`). Streaming SSE. `QWEN_SSH=""` → local urllib; set a host to
  hop over ssh (but run the loop ON the inference box — a remote hop halves your
  effective tok/s and adds a timeout failure mode).
- **Thinking ON, always.** No assistant prefill, no suppressor. Reasoning
  streams into `reasoning_content`; the visible reply carries the FILE blocks.
  Thinking off = garbage; this was the 2026-08 three-day bug (FAILURES.md #31).
- **Timeouts**: 5400s. A 30-minute think at xhigh is NORMAL — budget for it;
  killing a long think amputates the reply and looks like model stupidity.
- **Prompt composition**: QWEN.md (rules) + BRIEF.md (design bible) + current
  story + source snapshot + progress.txt tail + LAST_VERIFY.txt + the verbatim
  authoritative VERIFY line the model must echo back. Static parts first,
  volatile tails last, so the LM Studio prompt cache hits (prefix pinning).

## Model config (the default preset)

| Setting | Value |
|---|---|
| weights | 8-bit MLX — weight-only quant, ~equal quality to bf16 at ~2x tok/s. bf16 only when removing all doubt for a one-off verdict. Verify `lms ps` identifier→model |
| context | 262144 |
| reasoning_effort | `xhigh` |
| enable_thinking / preserve_thinking | true / true |
| assistant prefill | none — never `</think>` |
| max_tokens | 65536 |
| temperature / top_p / top_k | 1.0 / 0.95 / 20 |

## Loop-state mechanics

- **Trajectory log** — every iteration appends one JSON line to
  `scripts/ralph/trajectory.jsonl` (gitignored), written in a `finally` so
  crashes still log: `{ts, story_id, iteration, files_written, patch_or_file,
  verify_ok, exit_status, duration_s, reply_bytes, think_bytes, emission_hash,
  verify_hash}`. `emission_hash` is sha1 of the whitespace-normalized reply —
  identical-emission loops become greppable. This is the postmortem record;
  progress.txt is the model's memory, trajectory.jsonl is yours.
- **Typed exits** — the iteration exits 0 (normal), 42 (all stories passed; in
  the phased variant also phase-complete), 43 (no eligible story: everything
  remaining is blocked or dependency-starved — escalate to a human), 44 (3+
  consecutive iterations with zero FILE/PATCH blocks). ralph.sh propagates them;
  run_loop.sh routes on them.
- **Blocked state** — 5 consecutive failures on one story (counted from the
  trajectory) sets `"blocked": true` + `"blocked_reason"` (last verify tail,
  ≤500 chars) on that story in prd.json, and the loop moves on. A manager
  unblocks by editing the story and clearing the flag.
- **`blockedBy`** (per story, optional) — `["US-xxx"]` ids that must all be
  `passes: true` before this story is selected. Story selection = lowest
  priority among unpassed, unblocked, dependency-satisfied stories.
- **`regressionVerify`** (top-level prd.json, optional) — a shell command run
  after a story's own verify passes, before `passes` flips and the commit
  lands. Its failure = story failure (output goes to LAST_VERIFY.txt). This is
  the fix-A-break-B killer.
- **Architect two-pass** — at 3 consecutive failures on a story, the iteration
  splits into two calls: call A emits a diagnosis + numbered fix plan only (no
  blocks, kept in LAST_PLAN.md); call B gets the plan prepended to the normal
  prompt and must emit only FILE/PATCH blocks. Diagnosis and emission stop
  competing for the same reply.

## Rut detection + supervision

- `reference/stuck_detector.py` — stdlib, no LLM. Reads trajectory.jsonl and
  classifies the last ~20 events: identical emission ≥3×, ≥4 consecutive
  zero-file iterations, pass/fail oscillation ≥3 cycles, same story failing
  with identical verify output. Prints a JSON `{stuck, pattern, suggestion}`.
- `reference/run_loop.sh` — supervisor: claims a `$RALPH_SLOTS_DIR` slot (release
  via EXIT trap), restarts ralph.sh on crash (max 5), routes the typed exits,
  runs the stuck detector every 10 rounds and on every 43 (ESCALATE).

## Write-path defenses (the important part)

In order, each writes' gauntlet — every rule exists because a real loop broke
without it. Files are written ONCE, after the stream completes; mid-stream the
runner only refreshes LAST_REPLY/LAST_THINKING for observability (a mid-stream
write lands half-generated files on disk — FAILURES.md #34):

1. **Incomplete-last-file skip** — the final FILE block in a truncated reply is
   dropped; the on-disk copy survives. (Without it: half-files corrupt the tree.)
2. **Planning-prose filter** — replies that leak reasoning ("Let me…", "Wait,…")
   into a FILE body are rejected. (Without it: prose overwrote a verify wrapper
   AND a game file, silently breaking all judging.)
3. **Harness-path write-protection** — `tools/`, `scripts/` are never writable
   by the model. Your publish scripts, your verify wrappers, your runner live
   there. (Without it: see #2. Also walls off live-service publishing.)
4. **`allowedFiles`** (per story) — hard whitelist of writable paths. The single
   biggest rut-killer: converts "please only touch X" from a request into law.
5. **`protect`** (per story) — map of file → required substrings; a write that
   drops a protected symbol is rejected. Stops fresh instances from rewriting a
   shared module and silently deleting exports its siblings import.
6. **CSS/asset sanity** — unbalanced-brace CSS rejected; shorter-than-85%
   rewrites of good CSS rejected; "valid existing css" never overwritten unless
   the verify failure names a CSS syntax error.
7. **Path traversal guard** (`safe_rel`) and dotfile preservation.

## Verify runner

- Run with cwd = repo root, generous timeout (Unity/Xcode verifies take minutes).
- Write full output to LAST_VERIFY.txt — it is the next iteration's memory of
  what failed, and your forensic record.
- On pass: mark `passes: true` in prd.json, `git add -A && git commit`.
- The runner re-reads prd.json live, so a manager can enrich a story while an
  iteration is mid-generation.

## Supervisor + ops

- `ralph.sh`: N-iteration loop, `<promise>COMPLETE</promise>` early-exit.
- Chain script: sequential project loops in tmux under `caffeinate`.
- Watchdog (cron, on a DIFFERENT machine than the loop): one ssh call collects
  vitals (loop up? model loaded? prd mtime? fail-streak from progress.txt?);
  alerts a human channel; dumb-fix (reload model, restart tmux) at most once
  per new incident. The external machine matters: it still reports when the
  loop box wedges entirely.
- A read-only localhost dashboard (loop state, per-project story checklists,
  log tail, `lms ps`) pays for itself the first night.

## PATCH blocks (big-file surgery)
Whole-file emission truncates past ~180-200 lines (law 3). The runner accepts, alongside `### FILE:`:

```
### PATCH: relative/path
<<<<
(exact current text, copied verbatim from the snapshot)
====
(replacement)
>>>>
```

Runner rules (see reference implementation in the project runners):
- Tolerant regex: `<{4,}` / `={4,}` / `>{4,}`, optional code fences — models drift toward git-conflict syntax (failure #28).
- Apply only if the search text exists and is UNIQUE in the target; skip with a printed reason otherwise.
- Harness paths stay write-protected for patches too.
- Patched files count toward `written` so the verify runs.
- Prompt scaffold: "for files over ~200 lines ALWAYS use PATCH blocks — whole-file rewrites truncate and are discarded."
- Prerequisite: the target file must be pinned verbatim in the snapshot (allowedFiles), or every patch is a paraphrase that never matches (failure #27).

## Supervisor: last-known-green tag (post-run review)

run_loop.sh maintains a git tag `last-known-green` force-moved to the commit
after every story whose regression verify passes. Any iteration that corrupts
the tree can be evaluated — and if needed reverted — against a tag that is
PROVEN green by the honest gates, not by "it committed so it passed."
