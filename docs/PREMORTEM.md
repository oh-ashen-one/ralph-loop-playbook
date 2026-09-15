# Pre-mortem — 50 ways the overnight 3D loop fails (written BEFORE the run)

Written 2026-08-19 before the first overnight Godot run. Each
row: the failure, what catches it, the mitigation already in place (or the gap).
Layers: HARNESS (code prevents), VERIFY (a gate goes red), STORY (prd text
prevents), MANAGER (human/frontier agent must do it), OPS (machine/process).

After the run: rows that fired get promoted to FAILURES.md with real numbers;
rows that didn't fire get deleted. This file is a bet, not a museum.

## Model / serving (LM Studio, Qwen 27B 8-bit)

1. LM Studio crashes mid-iteration — OPS: supervisor restarts loop; trajectory resumes. Gap: LM Studio itself has no watchdog here.
2. Another session unloads/reloads the ralph-showcase instance — MANAGER law: only this session touches it; preflight `lms ps` identifier→model (#43).
3. A co-tenant job starts generating on the shared GPU mid-run — absorbed (half speed). OPS: morning check includes `lms ps`.
4. xhigh think spirals past 90 min — HARNESS: chat timeout 5400s kills it; iteration fails clean; nothing partial written (#45 fix).
5. Reply truncates mid-file at 65536 — HARNESS: incomplete last block is skipped, not written.
6. Model emits files with wrong case (`Main.tscn`) — macOS FS is case-insensitive; dupes possible. VERIFY: import gate catches broken refs.
7. Model rewrites frozen subsystems — HARNESS: `protect` symbol maps per story.
8. Model emits `project.godot` or `addons/` — HARNESS: allowedFiles whitelist; QWEN.md forbids.
9. Tool-call XML mode flip at temp 1.0 (#34) — STORY: "you have NO tools"; HARNESS: exit 44 on zero-block streaks; stuck detector pattern.
10. Files land in reasoning_content, visible reply empty — HARNESS: reasoning fallback (kept from v1).
11. Model hallucinates GUT API (invented asserts) — VERIFY: red, fed back; stall-breaker blocks story after 5.
12. Model writes tautological tests (`assert_true(true)`) — MANAGER: checklist row "judge smoke-tested both ways"; critic phase audits test honesty. **Biggest honesty risk in the whole system.**
13. Model weakens an existing test to pass — HARNESS: `protect` on test symbols where named; MANAGER: morning `git log -p` skim of test diffs.
14. GUT addon itself broken by a stray edit — HARNESS: addons/ excluded from writes.
15. `godot --headless --import` hangs on a corrupt GLB — VERIFY: 900s timeout; assets are pre-staged (model doesn't import new packs).
16. Kenney GLB path/case mismatch at runtime — STORY: exact asset paths pinned in descriptions.
17. Physics non-determinism flakes tests — STORY: fixed seed 1337, Input.action_press + fixed frame steps, range asserts not equality.
18. Headless can't rasterize (screenshot stories) — TOOLING law: `--rendering-driver vulkan` or Movie Maker; overnight stories avoid screenshots entirely.
19. Audio timing asserts flake — STORY: assert node exists + stream assigned, not `playing`.
20. Spawner RNG drift breaks count asserts — STORY: seed pinned (1337) in prd + BRIEF.

## Godot project mechanics

21. Hand-written .tscn with bad UIDs — VERIFY: import gate; QWEN.md: prefer GDScript-built nodes.
22. class_name collisions across model-written files — VERIFY: import gate (global script class registry).
23. Model references an autoload it can't register (project.godot is frozen) — STORY: input map + scene structure pre-wired by manager at setup (done).
24. Signal name typos — runtime-only errors — VERIFY: GUT runtime tests + `SCRIPT ERROR` output grep (Godot exits 0 on parse errors, #23).
25. Verify suite outgrows the 900s timeout — HARNESS gap: raise to 1800s or split suite when it approaches. Watch: suite runtime in trajectory.
26. Z-fighting / visual slop that passes every assert — MANAGER: morning playtest + critic phase; no gate can see taste yet (VLM judge is advisory-only).
27. Camera clips inside the ship mesh — STORY: camera-distance assert (follow cam min distance) in US-003's test.
28. Win overlay shows but game keeps simulating (or vice versa) — STORY: US-009/010 assert BOTH overlay visibility AND tree pause state.
29. Menu transition dead-ends (no path back) — STORY: US-011 asserts the full loop menu→play→pause→resume→quit→menu.
30. Input action name typos (`"forward"` vs `"move_forward"`) — STORY: exact action names pinned; manager pre-wired the map.

## Harness / loop mechanics

31. Loop finishes all stories at 2 a.m. and idles the box — OPS gap: chain a second prd (critic phase per CRITIC.md) or next project. Acceptable tonight: idle is fine, we're measuring.
32. ralph branch diverges from main all night — OPS: morning merge ritual (document in scoreboard check).
33. trajectory.jsonl grows unbounded — non-issue at night scale (~KB/iter); rotate weekly if a run goes days.
34. progress.txt bloat leaks into prompts — known gap (Beads memory-decay item, not yet implemented); at 14 stories it won't bite tonight.
35. blocked-starvation: everything blocked → exit 43 → supervisor ESCALATEs — MANAGER: that's the phone call, working as intended.
36. Verify flakiness from shared build dirs (#31) — OPS law: manager never builds in the repo mid-run; one writer.
37. VLM judge false-fails if wired blocking — TOOLING law: advisory-only until calibrated. Not wired tonight.
38. MCP session pokes the loop's Godot instance — OPS: manager Godot MCP is read-only during runs.
39. Model re-emits a whole file it was told to PATCH — HARNESS: both paths parse; protect maps guard content.
40. PATCH search text paraphrased from memory (#27) — STORY: target files pinned in allowedFiles → full text in snapshot.

## Ops / machine

41. The box sleeps overnight — OPS: wrap the run in `caffeinate -s`. **Do this at launch.**
42. The box reboots (update, power) — gap: no launchd auto-restart for loops yet. Accepted tonight; noted for supervisor v2.
43. SSH/network drops — irrelevant by design: the loop runs ON the inference box under nohup; a disconnected laptop kills nothing.
44. Ghost timers from manager sessions kill the loop (today's own bug: a stale 30-min killer murdered a relaunched loop) — OPS law: every timed killer must name its target process pattern AND its own expiry; check `pgrep -fl sleep` before relaunching anything.
45. Disk fills (assets_src + .godot + trajectory) — OPS: preflight `df -h`; staged assets are ~50MB, non-issue tonight.
46. tmux stopped-server backlog resurrects killed processes (#38/#39) — OPS: loops run under nohup, not tmux.
47. Slot system double-books or starves — HARNESS: run_loop.sh claims/releases; PAUSED sentinel freezes claims box-wide.
48. Ralph branch checkout eats uncommitted setup work — setup is committed on main before launch (done); ralph.sh does `checkout -B`.
49. The morning scoreboard lies by omission (passes:true but game feels dead) — MANAGER: playtest is part of the ritual; critic phase converts feel into stories.
50. Manager (me) edits the repo mid-run and corrupts state — OPS law: manager works read-only against the project while the loop holds the slot; all fixes land as stories or wait.

## The three to actually lose sleep over

- **#12/#13 (test honesty)** — the only failure that looks like success all night.
- **#4 (spiraling thinks)** — burns the night on one story; the stall-breaker is the backstop.
- **#31 (idle box after early completion)** — not a failure, just wasted throughput; acceptable tonight.
