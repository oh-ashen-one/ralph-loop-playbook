# OVERNIGHT.md — 50 ways to make an 8-hour loop produce a real game

The question this answers: "we start at midnight, how do we wake up to
significant results instead of slop?" Every item is paid for — most map to
FAILURES.md numbers. Ordered by leverage; grouped for scanning.

## Spec & scope — the run is won before launch

1. Write the prd so the LAST story is "a stranger can play it end-to-end" — never "suite green" (#52).
2. Every story fits one ~15KB reply; split by file, then by stage (law 2).
3. Order stories so the game is PLAYABLE by story 3, then deepened — a run dead at hour 6 still leaves a game.
4. Front-load the riskiest integration — don't learn at hour 7 that scenes don't compose.
5. Cap scope at 12–15 stories/night (measured: 14 stories ≈ 7.3h gen+verify, 31 min/iter, honest gates add iterations — budget 45 min/story).
6. Turn every human playtest complaint into a literal story with a measured gate, within the hour (critic phase).
7. Every story names exact files, constants, and error texts (law 6) — vague stories rewrite the world, surgical stories converge.
8. `allowedFiles` + `protect` derived by GREPPING the current code, never memory (#27, #29).
9. Pre-flight audit by a fresh-eyes agent before any overnight launch — it caught 2 launch-blockers the one night we ran it.
10. The brief carries palette, scale, and feel laws (DUSK-STYLE) so 14 stories don't produce 14 art directions.

## Gate honesty — the master lesson of this week

11. `run_verify` greps output markers; exit code is never the gate (#52).
12. Every gate red-tested before the run: seen FAILING on deliberately broken input (#23). A gate you've never seen fail doesn't work.
13. Parse gate covers every .gd including tests/ — GUT silently skips unparseable test files.
14. Final integration story boots the REAL main scene headless and asserts zero errors — unit suites never exercised composition.
15. Anything clickable gets a click-through gate (#36).
16. Anything pressable gets an input-simulation gate: real key, measured state delta (#49).
17. Visual claims gate on renders/screenshots — material slot names proved nothing (white-lid crate).
18. Scene files referenced by other scenes get their own load-gate (menu.tscn shipped malformed).
19. Verifies print MEASURED numbers on failure so the next iteration reads data, not vibes (law 9).
20. Morning skim of model-written test diffs — the model grades its own homework leniently (PREMORTEM #12/13).

## Model config & bandwidth

21. The validated config, always: 8-bit MLX, thinking xhigh ON, temp 1.0/top_p 0.95/top_k 20, max_tokens 65536, context 262144. Thinking off = the three-day collapse (#42).
22. Verify model IDENTITY at launch (`lms ps` identifier→weights) — a wrong quant serving silently is a real failure mode (#43).
23. Solo bandwidth for the priority run: one generating stream. Two streams = half speed each; the 2-slot cap is mechanical.
24. Chat timeout 5400s. Never kill a long think — 50-min iterations are normal for integration stories (#46).
25. Launch pattern: `QWEN_SSH="" nohup caffeinate -s bash scripts/ralph/run_loop.sh <name> 200 > /tmp/ralph-<name>.log 2>&1 &`, absolute paths only (#32).
26. Claim a slot before starting; release on exit; check `$RALPH_SLOTS_DIR/QUEUE` first.

## During the run — manager hygiene

27. The supervisor (run_loop.sh) owns the lifecycle — managers never arm bare kill timers (#50).
28. trajectory.jsonl + progress.txt current at all times — any fresh manager resumes in one read (law 8).
29. Watchdog pings when the log is stale >30 min with stories remaining (#41).
30. One writer per repo: the manager never builds/imports while an iteration is mid-flight (#31).
31. After ANY manager-side fix, overwrite LAST_VERIFY with the truth and cycle the iteration (#29).
32. One commit per story — green state is always one revert away.
33. Don't touch the box mid-run beyond reads: no model reloads, no editor on the same project, no GPU hogs.

## Content strategy — make 8 hours VISIBLE

34. Steal-first: assets staged BEFORE launch from the ASSETS.md map; don't burn iterations inventing meshes (MODELING.md rule zero).
35. Budget ~70% mechanics, ~30% juice (particles, screen shake, sounds) — juice is what reads as "progress" at 9am.
36. Every mechanic ships with its feedback (sound + particle + HUD tick) in the SAME story — a tractor beam that works but is invisible doesn't exist.
37. Difficulty/pacing constants live in the brief, so tuning = editing numbers, not refactoring.
38. Vertical-slice ordering: a thin complete loop beats deep fragments.
39. Controls card on screen from story 1 — users click first (#36, #49).
40. Demo-ability is a requirement: the user can show someone in 60 seconds or story 1 tomorrow fixes that.

## Escalation hygiene (learned the expensive way, run #2)

- Two manager interventions per story MAX, then restructure (law 14) —
  nursing a loop past the third rut is how a night dies.
- Every story's acceptance test exists before launch, manager-written,
  outside allowedFiles (law 15). A story without its test is unfinished.
- The monitor's job is OUTCOMES, not process: "0 new stories passed in 3h"
  is an alarm that changes strategy, not a status line that says "loop
  healthy." Healthy process + zero passes = failing run.

## Morning harvest — the run isn't done when the loop exits

41. Human playtest first thing — feel can't be gated (PREMORTEM #49).
42. Critic findings become prd stories immediately; the next night starts smarter.
43. Log timing to SESSIONS.md — scope estimates compound in accuracy.
44. Every manager intervention → FAILURES entry + checklist row (law 13: the 1% shrinks itself).
45. Compare against the previous night's log: if tonight wasn't faster/cleaner, find out why before launching another.

## Infrastructure resilience

46. `caffeinate` + `nohup` so sleep/ssh drops can't kill the run.
47. Test the supervisor's crash-restart path once before trusting it overnight.
48. Branch per run (`ralph/<name>`) — main stays clean, shared-box pulls stay safe.
49. The supervisor's final state writes the morning note: what's green, what's suspect, what to play first.
50. When in doubt, reread FAILURES.md — every item on this list is there because we paid for it once. Don't pay twice.
