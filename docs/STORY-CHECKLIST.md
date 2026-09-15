# Story pre-flight checklist

Run EVERY new/edited story through this before a loop sees it. Each row exists
because skipping it burned hours (failure #s in parens). Inspired by the
gate-at-authoring-time idea in Claude-Code-Game-Studios; adapted to ralph loops.

## The verify
- [ ] Runtime gate for runtime behavior — probe/sim/screenshot, not compile+grep (law 9)
- [ ] Greps are exact declarations (`func do_pass`), never bare words (#24); scoped to source dirs only (#22)
- [ ] No `a && b || c` precedence holes — group alternates: `a && { b || c; }` (pre-flight audit)
- [ ] Judge smoke-tested BOTH ways: seen failing on broken input and passing on good (#23)
- [ ] Every file/dir the verify references is visible to the model (not snapshot-excluded) and inside grep scope (#35)
- [ ] Anything a user can click has a click-through gate (#36, law 12)
- [ ] Anything a user can PRESS has an input-simulation gate: send the real key, assert the state delta — never grep for `KeyW` (#49)
- [ ] Godot/GUT: the gate greps OUTPUT markers (`SCRIPT ERROR|Parse Error|Failed to load|N failing tests`) — the exit code is 0 even on failures and GUT silently skips unparseable test files (#52)
- [ ] The final integration story boots the REAL main scene headless and asserts zero errors — per-story unit suites do not exercise scene composition (#52)
- [ ] Gate helper scripts proven to run against the real project root (cd printed and eyeballed once) — a wrong root makes a gate vacuously green (#52)
- [ ] Spawn/load positions validated against the world (embedded player = frozen everything, #48); camera height asserted against terrain, not assumed (#47)

## The story text
- [ ] Every sentence is currently TRUE (stale claims freeze the model — #21, #26, #29)
- [ ] Exact error text / measurements / line numbers included when retrying (law 6); diagnosis REPRODUCED, not plausible (#37)
- [ ] Scope fits one reply: target files under ~200 lines for whole-file emission, else mandate PATCH blocks (#26, law 3)
- [ ] States "you have NO tools; blocks are written straight to disk" for models that flip into tool-call mode (#34)

## The fences
- [ ] `allowedFiles` set — and every file in it fits the snapshot budget verbatim (PATCH prerequisite, #27)
- [ ] `protect` symbols derived by GREPPING the current file, never from convention (#29 old catalog / impossible-gate class)
- [ ] Additive-only stated when extending a shared module (#4)

## The environment
- [ ] One writer per repo: no manager builds while an iteration is in flight (#31)
- [ ] Loop invoked by ABSOLUTE path so slot/watchdog patterns match (#32)
- [ ] After any manager-side fix: LAST_VERIFY overwritten with the truth, iteration cycled (#29)

## Scope-shrink defense (post-run review, 2026-08-19)
- [ ] Every story gets at least one gate asserting behavior the story text does NOT spell out mechanically — property-style ("drift speed equals 0.5 + 0.35×salvage_count for ANY count"), not example-style. Otherwise the model implements the literal test and calls it the feature (silent scope shrink).
- [ ] The prompt carries the project grounding file (reference/GODOT_API.md or engine equivalent): the ~50 APIs this project actually uses, with the trap names spelled correctly. Priors lose to in-context evidence; FAILURES #55 is what happens without it.
