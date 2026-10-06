# Local native error log

Evidence snapshot: 2026-10-06. This supplements the historical
[81-entry catalog](../FAILURES.md), and supports the existing
[skill](../SKILL.md) and [native runbook](LOCAL-NATIVE-LOOPS.md).

**Status language:** implemented/tested means a cited controller check or
native result exists; procedure means a management instruction; recommendation
means future work; pending means the claimed product outcome is unverified.
A source edit, CPU test or earlier subfeature pass is never final game acceptance.
Evidence links below are pinned, sanitized project records or source. No raw
reasoning, credentials, private chat or machine routing is needed to reproduce
the conclusions. Scope is this run, not a universal model capability claim.

## N01 — Stale task context and completed cleanup

- **Symptom:** after context reconstruction, commentary briefly reopened an already completed model/Trash cleanup while the active task was game work and skill maintenance.
- **Cause status:** verified procedural context drift: an old user message was treated as current before the latest operating directive was read. No new Trash/model inspection or deletion occurred in that drift.
- **Failed approach:** trusting the latest visible historical request without checking completion and current scope.
- **Repair/outcome:** read the current directive and restored active scope before any destructive operation; prior deletion remained complete.
- **Prevention/status:** task/completion reconstruction is a **procedure**. Exact resume state checks are **implemented** for specific controller paths; no universal completed-task firewall is claimed. Recheck current scope after every compaction before writes or cleanup.
- **Evidence:** [current operating boundary at the evidence snapshot][boundary]; later decisions supersede historical preparation holds in that file.

## N02 — Planner reads without delivering a plan

- **Symptom:** q0051 stopped after four read-only turns; no `submit_plan`, source edit or native build.
- **Cause status:** verified tool-turn exhaustion. A requested generated prefab did not exist; Bootstrap loaded the actual street asset.
- **Failed approach:** another broad exploratory context without enough exact implementation context to finish.
- **Repair/outcome:** supplied Bootstrap, WorldColliders, VehicleInteraction and Mission with a single completion tool. This resolved the missing-context delivery shape, but q0052 then exhausted output; **no successful plan is claimed**.
- **Prevention/status:** exact context and bounded role tools are **implemented**. Verify requested objects against creation/load sites; monitor submitted actions separately from reading. A planner-completion guarantee remains absent.
- **Evidence:** [map chronology][map].

## N03 — Output budget consumed before a tool call

- **Symptom:** q0052 used 8,192 completion tokens with no tool call; q0053 did the same on a direct module request despite `low` effort.
- **Cause status:** verified output-length stops. Runtime/template inspection showed per-request effort forwarding; no evidence established forced `xhigh`. Internal reasons for consuming the budget remain uncertain.
- **Failed approaches:** one large planning completion, then a whole new module. Merely requesting lower effort did not ensure delivery.
- **Repair/outcome:** two smaller exact source spans yielded the first saved map edit, `506f55a`. This proves an edit was saved, not a working map.
- **Prevention/status:** bounded edit/output tools are **implemented**; task decomposition is a **procedure**. Record token usage, finish reason and tool calls; reject truncated source. Do not claim a universal line limit or model incapability.
- **Evidence:** [map chronology][map], [small-span controller][spans].

**Follow-up, 05:11 UTC:** q0058's combined geometry/complete-route role also stopped at 8,192 output tokens (17,151 prompt tokens, 207.91 s, zero tool calls). No native attempt or changed strategy was submitted. The explicit blocker route worked, but the combined request did not. The next bounded approach separates a short walking/boarding prefix, native proof of that prefix, and a local driving suffix that cannot rewrite the verified inputs. Controller [73fc41f](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/73fc41fc20d1937ca999b95ba1a298f5c34e0f8d/tools/resume_map_walk_first.py) has 183 passing CPU tests on both hosts. This is a changed task shape under validation, not a proven cure for output exhaustion or an accepted map.

**Follow-up, 05:21 UTC:** the compact q0059 walking role reduced prompt size to 4,834 tokens but still exhausted 8,192 output tokens after 200.37 s without a tool call. Smaller context alone therefore did not resolve this failure. One exact-state recovery [b8c5d1a](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/b8c5d1a205b10dbbf2a85c2e681d48af613cf3e8/tools/resume_map_prefix_budget.py) keeps the compact task, allows 16,384 output tokens and a bounded 700-second request, and preserves the original stops. All 184 CPU tests pass on both hosts. The larger allowance is pending native qualification; no claim of effectiveness or new map footage follows from its launch.

## N04 — Complete proposal rejected by a line ceiling

- **Symptom:** q0054 emitted one complete 47-line, 3,041-byte pavement tool call against a 45-line cap.
- **Cause status:** verified edit-size validation, distinct from output truncation.
- **Failed approach:** treating a complete over-limit submission as if no usable tool proposal existed, or regenerating its entire content unnecessarily.
- **Repair/outcome:** hash-pinned recovery accepted the exact tool content with a bounded 50-line cap, preserving the original rejection. Source `b28bf88` saved; later compile failure means this was not native acceptance.
- **Prevention/status:** response/proposal hashes and one-time state validation are **implemented**. Inspect the complete proposal, preserve provenance, and retest resulting source; do not use private reasoning as fallback code.
- **Evidence:** [pavement recovery implementation][pavement], [map chronology][map].

**Repeat, 06:47 UTC:** q0071 submitted a complete 16-line, 789-byte entrance edit against a 14-line ceiling after saving matching asphalt. Controller [51de56b](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/51de56b0c27e7683fe43119724d08b86125f97f2/tools/resume_alley_completed.py) pins both response and exact tool content, preserves the saved asphalt, and accepts only that proposal within 18 lines. It saved `9587c2d3` without regenerating or modifying local gameplay content, then entered the separate local wall-edit request. All 199 CPU tests pass on both hosts. New scenery remains pending native requalification; the prior candidate passed all ten regressions but received visual **FIX**. The repeated incident supports leaving modest formatting headroom in bounded edit requests, not disabling size checks or accepting truncated output.

## N05 — Correct lookup intent, incomplete controller-selected span

- **Symptom:** q0055 replaced a pavement lookup, but q0056 could not compile the resulting WorldColliders file. The old search tail and closing brace remained.
- **Cause status:** verified **controller error**. Substring selection for `if (pv0 != null)` matched an inline loop condition, not the following whole-line guard. Separately, the initial lookup searched imported roots although Pavement was its own scene-root object.
- **Failed approaches:** searching only imported roots; replacing the start of a loop without its tail; assuming an accepted exact edit was syntactically sound.
- **Repair/outcome:** whole-line unique boundary selection with a regression test, then local-Qwen replacement of the complete span. Candidate `b54e706` compiled and rendered six frames in q0057. Physical map traversal still failed; the compiler repair did not accept the map.
- **Prevention/status:** boundary helper and inline-match red test are **implemented/tested**; native build independently established this repair. Exact-preimage validation alone cannot validate C# syntax.
- **Evidence:** [boundary helper][pavement], [native compile recovery][compile], [span tests][map-tests], [map chronology][map].

## N06 — Replay syntax and physical behavior are different gates

- **Symptom:** q0055's first replay contained empty/early intervals; the second removed these but used lowercase key names and was rejected. After syntax recovery and compiler repair, the 36-second q0057 replay rendered yet failed the physical extension gate.
- **Cause status:** format causes verified. Native trace then showed the player stopped near X4.535 at Z14.5, and was about 3.85 m from the car when E was pressed. The run never entered vehicle mode. The exact collider responsible for the walking stop needs further diagnosis.
- **Failed approaches:** proposed travel distances based only on speed/time; assuming an E press proves boarding; inferring driving from the intended input sequence.
- **Repair/outcome:** whitelist-only case normalization preserved all timings/captures and rejected unknown keys. This repair is proven at protocol level. Native build passed, new AlleyPavement bounds were X6..22/Z8..20, but neither mode reached the required outside region. No map pass or critic pass occurred; the accepted tree was restored.
- **Prevention/status:** schema, normalization, physical out-and-back, collision/support and outside-capture gates are **implemented/tested**. Next repair is **pending**: inspect the blocking collider and author a locally generated route that actually boards and traverses. Do not weaken acceptance or claim the visible surface is accessible solely from its bounds.
- **Evidence:** [replay contract][replay], [protocol tests][replay-tests], [map native evidence][map].

## N07 — Bytes mistaken for tokens and context omissions

- **Symptom:** an earlier budget path could reject context prematurely; historical snapshot filters also concealed required code.
- **Cause status:** tokenizer audit verified that UTF-8 byte counts were not actual model tokens. Static prior-source inspection found exclusions for scripts, files over 80 KB and a 55,000-character aggregate snapshot; those are not token limits.
- **Failed approaches:** byte-based token estimates as hard proof; omitting a large dependency then asking the model to integrate against it.
- **Repair/outcome:** pinned tokenizer/template audit and explicit working/output/image allowances; exact source retrieval for current tasks. This establishes accounting and retrieval behavior, not that every future request will fit.
- **Prevention/status:** current budget checks are **implemented/tested**; compare actual runtime usage with reservations and disclose omissions as a **procedure**. Leave space for output/tool/image growth.
- **Evidence:** [budget audit][budget], [verified prior-attempt findings][prior].

## N08 — Blender script changes without matching exports

- **Symptom:** a coupe authoring-script change initially had no corresponding engine export.
- **Cause status:** verified script/export mismatch; an edited Python file alone did not change the imported asset.
- **Failed approach:** proceed directly to appearance qualification from the script diff.
- **Repair/outcome:** one local export-only action used the unchanged script; native checks and fresh critique accepted a **bounded coupe silhouette** at `d269dc43`. It did not accept final game art.
- **Prevention/status:** parity checks are **implemented**. Link script/export hashes and check imports/bounds in the engine after asset edits, including shared-mesh dependents.
- **Evidence:** [coupe qualification][coupe].

## N09 — False green from markers, displacement or weak tests

- **Symptom:** prior wrappers showed `GODOT_OK` alongside parse/autoload errors; another integration was deferred because the large player file was missing. An early physics route could count falling as movement.
- **Cause status:** upstream findings are static evidence, not a claimed exploit execution. Physics measurements showed why displacement alone was insufficient.
- **Failed approaches:** success marker/exit code/symbol grep as sole verdict; total displacement without grounded travel or visible support.
- **Repair/outcome:** native green/red movement fixture, parse/runtime log checks, horizontal travel, grounded/drop measures and rendered pavement coverage. These catch the studied false greens; they do not establish all visual or mission quality.
- **Prevention/status:** cited current gates are **implemented/tested**. Keep acceptance external and red-test each meaningful failure condition.
- **Evidence:** [prior findings][prior], [controller qualification][controller], [physics repair][physics].

## N10 — Damage to a collider the camera does not visibly aim at

- **Symptom:** courier candidate q0050 dealt two damaging shots at 7.5 and 9.2 s while visible-target ray intersection and center-viewport tests were false.
- **Cause status:** verified rendered-target/collider disagreement. Changed shared character art and its positioning are relevant; do not claim a fully proven asset root cause from correlation alone.
- **Failed approaches:** collider hit as sufficient aim proof; promoting character art after only earlier movement/vehicle passes.
- **Repair/outcome:** existing visible-aim gate rejected the candidate; its source was preserved and the accepted tree restored. The courier asset itself was **not repaired/accepted** in this stage. Earlier aim work separately validated misses and visible cover.
- **Prevention/status:** damage/visible-ray, deliberate-miss and cover checks are **implemented**. Re-run them after shared character changes; do not reuse unrelated earlier greens.
- **Evidence:** [aim evidence][aim], [courier/process recovery outcome][process].

## N11 — Camera checks pass within a limited scope

- **Symptom:** a bounded target/clearance camera pass still left a tight driving view. A later vehicle-camera branch was never enabled and its replay lacked required mission evidence.
- **Cause status:** initial target identity and clearance measured; follow-up unwired branch verified statically. A claimed visual improvement had not been established.
- **Failed approaches:** source branch existence as runtime proof; resetting before failure and treating that as a failure/retry sequence.
- **Repair/outcome:** original camera checkpoint retained with its limits; follow-up rejected and baseline restored. No final driving-framing acceptance claimed.
- **Prevention/status:** target identity/clearance and representative gameplay gates are **implemented**; visual composition still needs fresh review and explicit scope. Test transitions and actual branch activation.
- **Evidence:** [camera qualification][camera], [follow-up rejection][camera-followup].

## N12 — Process scan error interrupts an otherwise useful qualification

- **Symptom:** resident supervision stopped on `SystemError: proc_cmdline returned a result with an exception set` while courier qualification had six completed checks.
- **Cause status:** native process-query exception verified; a process-exit race is a hypothesis. No measured evidence established a memory shortage or renderer conflict.
- **Failed approach:** treating a partial process inventory as complete or blindly restarting forever would mask uncertainty; neither is the adopted repair.
- **Repair/outcome:** discard partial inventory and retry the specific error once; persistent/unrelated errors stop. One diagnosed resident restart restored health. Sealed, identical-candidate completed checks were reused; the resumed combat gate then correctly rejected the candidate.
- **Prevention/status:** complete-scan retry/red tests and evidence identity checks are **implemented**. Immutable resident revisions prevent incidental controller edits from changing running imports. They do not guarantee future runtime stability.
- **Evidence:** [process-scan incident][process].

## N13 — Reusing success without its exact identity

- **Symptom:** interrupted suites and small post-pass edits tempted reuse of earlier results; a lowercase critic verdict was rejected by an uppercase-only validator.
- **Cause status:** protocol casing can be a complete valid decision with wrong spelling; source/build changes independently invalidate old runtime evidence.
- **Failed approach:** rerun or discard everything indiscriminately, or accept an old green because it has a familiar filename.
- **Repair/outcome:** normalize only recognized complete verdicts; preserve the original rejection. Reuse sealed native results only with exact candidate, harness, build, scenario and capture identity; resume unfinished tests separately. Never let reused checks bypass a later real failure.
- **Prevention/status:** immutable evidence/checkpoint and narrowly scoped recovery checks are **implemented** in the studied controller. Apply integrity validation to all reuse routes; a movable tag alone is insufficient.
- **Evidence:** [review recovery][review], [replay reuse evidence][reuse], [process recovery][process].

## N14 — Test growth and minor polish conceal scope stagnation

- **Symptom:** many validated mechanics and short routes existed while accepted playable bounds remained X−1..6/Z−2..30, a 7 × 32 m corridor. The game was not a polished ten-minute mission.
- **Cause status:** measured geometry and route duration support the limitation. Gross decorative bounds and a 400 × 400 m support collider were not reachable playable area.
- **Failed approach:** use test totals, repeated HUD/camera edits or source commits as the product-completion metric.
- **Repair/outcome:** scope moved to a measured connector, then provisional two streets/side alley, then meaningful mission duration. First-connector gate exists; q0057 still failed it. Final map, pacing and visual acceptance remain open.
- **Prevention/status:** connector traversal gate is **implemented**; larger dimensions and prioritization are **planning/procedure**, not enforced whole-map completion. Track topology, objectives, measured time and representative visual defects beside test counts; stop at the fixed cap with an honest best checkpoint.
- **Evidence:** [map status][map-status], [map gate][map-gate], [delivery policy][delivery].

## N15 — Stale oversight claims and duplicate-owner risk

- **Symptom:** an older running snapshot remained in a handoff after later pauses. A child commentary update was not equivalent to delivery to the supervising thread.
- **Cause status:** observed snapshots had different timestamps; no automatic parent delivery guarantee existed for commentary. No competing owner is claimed to have run.
- **Failed approach:** infer liveness from an earlier launch receipt or rely on local commentary as the only oversight report.
- **Repair/outcome:** timestamped direct reads of controller state/PID, model health and evidence; final handoff through the actual parent route. Preserved one owner and existing reporting schedule.
- **Prevention/status:** ownership locks, single request guard and fixed-cap timer are **implemented**; fresh observation/reporting cadence is a **procedure**. Recheck liveness before saying "running". Do not create a duplicate watchdog or schedule to compensate for a stale message.
- **Evidence:** [controller runbook][runbook], [deadline and delivery policy][delivery], [exact recovery boundary][compile].

## N16 — Recoverable map rejection left the owner idle

- **Symptom:** q0057's real traversal rejection restored the accepted tree and paused the sole controller. The owner observed no GPU activity. At 04:58:51 UTC the model was healthy/loaded-idle and there was no controller PID; this was an actual pause, not merely low GPU utilization during useful work.
- **Cause status:** verified controller policy mismatch. Historical task failures had reached the generic repeated-blocker ceiling, so a new measurable route failure inherited an immediate stop despite the owner's continuous managed-work instruction. Documentation and commentary did not themselves restart or notify the supervising thread.
- **Failed approach:** repeatedly describe recovery as a procedure while leaving this recoverable native failure paused; treat launch admission as proof that a process/request is active.
- **Repair/outcome:** controller `722cb62` adds a map-specific transition: only listed physical replay failures after successful build/player exit can enter at most three local changed-strategy attempts. Exact replay hashes reject identical physical actions despite changed captions or capture times. Counters, accepted checkpoint and deadline remain intact. At **05:05:25 UTC**, the sole controller was live in q0058 with **one actual local-model request and zero waiting requests**. This establishes resumed execution, not native acceptance of the new route.
- **Prevention/status:** routing, attempt cap, unchanged-replay rejection, state persistence and explicit blocker artifact are **implemented/tested** (181 CPU tests on both hosts, including a real Store transition test). Unsupported/resource/permission failures and budget exhaustion take the blocker route. The blocker file is marked **pending existing parent oversight**; no guaranteed immediate delivery or universal recovery is claimed. No second watchdog, schedule or model was launched. A transient SSH failure was resolved by checking the unique receipt and PID rather than duplicating launch.
- **Evidence:** [bounded recovery policy](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/722cb62d9c2d034b7b59d184c638c3fee6efef31/tools/loop_controller/recovery_policy.py), [sole-owner recovery](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/722cb62d9c2d034b7b59d184c638c3fee6efef31/tools/resume_map_traversal.py), [routing/state regression tests](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/722cb62d9c2d034b7b59d184c638c3fee6efef31/tests/test_recovery_policy.py).

## N17 — Preserve the working leg and reduce the failing repair to exact fields

- **Symptom:** q0060 finally submitted a 17-second walking prefix and rendered five frames. It reached 6.533 m beyond the accepted boundary but could not return or board. Its automatic correction then exhausted 16,384 output tokens after 402.04 s without submitting anything.
- **Cause status:** native trace verifies the first failed return ended on foot at X7.340/Z10.607 in the pier area. The proposed route treated a gap between columns as clear without resolving the base obstacle on return. Output exhaustion of the next broad correction is separately verified; a larger ceiling was not a reliable cure.
- **Failed approaches:** regenerate the whole walking/boarding plan; retain an obstructed return line; increase the ceiling while keeping a multi-part geometry problem in one response.
- **Repair/outcome:** retain the four actual outward/dwell intervals and ask local Qwen only for three numeric walking durations. The cloud manager explicitly selected measured-clear return waypoints (north to Z17, west to X2, south to Z8) and composed normal input intervals; local Qwen supplied the durations and concise diagnosis. No game code changed. The local call completed in **10.23 s / 395 output tokens** with a **2,048-token ceiling**. Native q0061 verified the outside walk, physical return at **16.70 s**, and real vehicle boarding by **21.83 s**, with five frames. The controller then advanced to local driving; no full-map acceptance is claimed.
- **Prevention/status:** exact prefix hash, immutable source comparison, duration validation, input composition and native walking/boarding checks are **implemented/tested** (186 CPU tests on both hosts). The proven lesson is this specific repair, not that short prompts always work. Decompose the failing operation, preserve successful inputs, and state manager versus model authorship; do not describe manager-specified waypoints as an autonomous local design decision.
- **Evidence:** [small mechanical role and provenance](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/7abe7a7a09203a7b56b028ca474a7bd74778ad3a/tools/resume_map_return_micro.py), [input-preservation tests](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/7abe7a7a09203a7b56b028ca474a7bd74778ad3a/tests/test_map_return_micro.py), [native walking/return/boarding proof](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/e315a86e2dc9e77723ed3d796945166f2aafedf9/diagnostics/map-2026-10-06/walking-return-boarding-pass.json).

## N18 — A diagnostic prefix pass does not prove full surface support

- **Symptom:** q0063 completed both physical roundtrips (walking return 16.70 s; driving 13.772 m outside and return 34.33 s), but the full gate rejected walking and vehicle rendered support. Eleven walking samples crossed the pier base at Z11. The vehicle rose to approximately Y1.378 immediately after boarding, before throttle.
- **Cause status:** the earlier q0061 prefix contract verified traversal and boarding but omitted the full pavement-support contract. Vehicle source compared ground height to the root rather than the collider bottom and injected upward velocity; native proof of the proposed correction remains pending. Thus N17's bounded return/boarding result is valid only for its stated diagnostic scope.
- **Failed approach:** q0064 changed later outward driving time from 0.8 to 0.5 seconds; it repeated both earlier support faults. A later input cannot repair an already-observed prefix failure. The local diagnosis that the distant driving endpoint caused the support failure was unsupported by failure timestamps.
- **Repair/outcome:** controller `c7039b4` classifies failures before the first driving input and refuses driving-only retries for them. It requests local-Qwen vehicle source repair and walking arithmetic through clear Z17, preserving all prior route attempts. **193 CPU tests passed on both Macs**, including early-versus-late fault cases. q0066 supplied both edits/timings, but compilation failed as recorded in N19; no map acceptance resulted.
- **Prevention/status:** stage-aware routing and tests are **implemented/tested**. Applying all relevant support checks to the initial diagnostic prefix is still a **recommendation**; do not claim that guard was already implemented. Always distinguish diagnostic traversal success from complete acceptance.
- **Evidence:** [native support rejection](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/a2eba14d5784831df198015ee33f52fa1ea0d2bf/diagnostics/map-2026-10-06/roundtrip-support-rejection.json), [stage-aware recovery](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/c7039b4fe2db05cd60f1f946830726d489e6925d/tools/loop_controller/recovery_policy.py), [tests](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/c7039b4fe2db05cd60f1f946830726d489e6925d/tests/test_map_support.py).

## N19 — A small exact edit still needs its real component API

- **Symptom:** q0066 saved local vehicle repair `bde6b7a` (1,468 output tokens / 33.91 s) and a new clear walking replay (446 tokens / 10.33 s), then failed native compilation with CS0103: `_collider` does not exist. No player process or new capture ran.
- **Cause status:** verified missing symbol. The prompt supplied collider dimensions and the old selected block, but did not supply a defined collider member. Local Qwen invented `_collider`. Exact edit bounds preserve adjacent source; they cannot establish type/API correctness.
- **Failed approach:** assume a small selected block and physical diagnosis are enough context to produce compilable code.
- **Repair/outcome:** preserve the rejection and accepted fallback; one local one-line correction is given the actual existing Collider component API and world-space bounds. The exact third replay is reused because compilation prevented its first execution. Controller `1b92489` passes **194 CPU tests on both Macs** and preserves the three-strategy history and counters. Native correction/result remains pending at this entry.
- **Prevention/status:** exact state, symbol-specific compiler filter and sealed replay checks are **implemented/tested** for this recovery. Always include referenced declarations or explicit existing APIs as a **procedure**. No general static C# type checker before native compile is claimed.
- **Evidence:** [one-reference compiler recovery](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/1b92489f24bc877b724d694b252278b158954e58/tools/resume_map_support_compile.py), [preserved-budget tests](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/1b92489f24bc877b724d694b252278b158954e58/tests/test_map_support.py).

**N18/N19 follow-up, 06:09 UTC:** the one-line local correction compiled as **`bd0187d4`**. Native q0067 then proved the revised walking roundtrip (return **15.97 s**, **188/188** covered samples) and stable vehicle support (rootY **−0.01523..−0.00999**), with nine captures. The old driving timings failed under corrected grounded physics: X remained **1.47..3.36**, Z **7.96..9.46**, so no required outside excursion occurred. This fixes the studied support/compiler faults, not map acceptance. The exact blocking collider/heading behavior still needs diagnosis. The three-strategy budget closed with preserved counters 15/1 and restored accepted source; no regressions/fresh critic ran. A timestamped parent handoff and two actual private Library images report the exhausted blocker. Source edits that change physics require remeasuring input timing; an earlier successful trajectory cannot substitute for current-source execution.

## N20 — A moving actor implemented as an immovable collider

- **Symptom:** the grounded car could not leave X1.47..3.36/Z7.96..9.46 despite throttle and steering. A previous floating route had hidden the obstruction.
- **Cause status:** verified by native q0069 using unchanged source/replay and passive collision callbacks. Ten samples show contact with the Rival's solid capsule, which has no Rigidbody. At t22.70 actual displacement speed was **0.414 m/s** versus commanded **4.5 m/s**, with an opposing contact impulse. The later steering interval also contacts the pier base after the approach was blocked. This establishes an actor-physics defect rather than missing input; it does not prove every part of the remaining route is valid.
- **Failed approaches:** infer the cause from displacement alone; adjust later driving timings; read Rigidbody velocity after the game overwrites it and mistake that command for actual travel.
- **Repair/outcome:** local Qwen saved **`d5260465`**, adding an 80 kg dynamic, gravity-enabled upright rival body and clearing its motion on the legitimate R reset. Solid collider, combat signals and the exact failed replay remain unchanged. At 06:22:45 UTC the sole owner was building that candidate; native acceptance was pending.
- **Prevention/status:** passive contact names/bounds/normals/impulses, actual yaw/input, position-delta motion and the cause-specific repair gate are **implemented/tested** (197 CPU tests on both Macs). The first probe itself failed compilation because this Unity version rejects `GetInstanceID()`; retaining Collider references repaired that cloud-authored instrumentation error. Native q0069 proved the corrected probe runs. A general actor-physics linter is **not implemented**.
- **Evidence:** [actual contact diagnosis](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/cf3b380/diagnostics/map-2026-10-06/static-rival-contact-diagnosis.json), [passive probe](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/a03089a1cdbf931dc5bfb1d45c2b008deffae84d/controller/unity/LoopVehicleObservation.cs), [cause-gated local repair](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/a03089a1cdbf931dc5bfb1d45c2b008deffae84d/tools/resume_vehicle_contact.py).

**N20 native outcome, 06:24 UTC:** q0070 source **`d5260465`** passes the **unchanged** failed map replay after the local body/reset repair. Walking travels 6.533 m outside and returns at15.97 s; vehicle travels13.768 m outside and returns at33.63 s. All188walking support samples and vehicle rendered support pass, with real outside captures. The same owner automatically starts all ten regressions; fresh visual critique and promotion remain pending. This is measured evidence for the collision diagnosis and repair, without changing replay timings or disabling collisions. [Native proof](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/26949bb/diagnostics/map-2026-10-06/rival-repair-native-pass.json).

**N20 qualification, 06:35 UTC:** all ten current-source regressions passed. Fresh local critique returned **FIX**, confirming mechanics but rejecting the unreadable fence opening and bare, visually unbounded slab. No map promotion followed. The same managed queue restores the proven candidate for three small local presentation edits (asphalt material, decorative fence opening, original-mesh outer walls), with unchanged physical inputs and full requalification. Do not convert the successful physics repair into a visual PASS. [Independent visual verdict](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/1daecb9/diagnostics/map-2026-10-06/rival-repair-visual-fix.json).

## N21 — Physical enclosure without readable scenery or junction evidence

- **Symptom:** q0072's matching asphalt and visible outer walls pass native out-and-back traversal and all ten regressions, but the fresh critic returns **FIX** at 07:00:47 UTC. Actual walking/driving frames show a dark, empty corner and a hard-to-see actor. The selected captures omit the boundary crossing itself.
- **Cause status:** darkness, plain walls and absent junction frames are verified visual/evidence defects. The existing traces show the crossing is physically usable; this is not another failed driving trajectory. The exact best lighting/art treatment remains a design choice requiring fresh rendered review.
- **Failed approach:** equate visible bounding meshes and physics passes with a readable alley; capture only the old corridor and distant outside positions while asking the critic to judge the junction.
- **Repair/outcome:** controller [c1718b7](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/c1718b74eda86d5ff06aebd15f42f1a9d4a1602d/tools/resume_alley_readability.py) preserves the rejection and accepted baseline, requests three local visual edits, and adds actual trace-derived boundary capture times without changing physical inputs. Critic selection retains that junction, both distant excursions and the return. All 202 CPU tests pass on both hosts. At 07:18 UTC the local fill-light role is active; native visual improvement is **pending**, not established by controller tests.
- **Prevention/status:** junction selection and input-preserving capture additions are **implemented/tested**. Reviewing actor/floor contrast and the visible route is a **procedure**, not an automatic pixel-quality metric. Keep a visual FIX separate from mechanical acceptance and preserve unfinished quality claims.
- **Evidence:** [complete critic and regression receipts](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/c1718b74eda86d5ff06aebd15f42f1a9d4a1602d/diagnostics/map-2026-10-06/alley-readability-visual-fix.json), [capture/recovery tests](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/c1718b74eda86d5ff06aebd15f42f1a9d4a1602d/tests/test_alley_readability.py).

**N21 follow-up, 07:44 UTC:** q0074's saved lighting/props pass both native traversals, 188/188 support samples and all ten regressions. Actual frames prove brighter floor/actor visibility. Fresh critique supplied **no verdict**: adding a junction frame alongside all previous images exceeded the conservative context budget before inference. This was a **controller selection error**, not model output exhaustion. Controller [75eb086](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/75eb0866eedbd6be27ee4fcd34ccf20708f308c0/tools/continue_game_queue.py) replaces the redundant initial image with the junction, preserving outside foot/car views and return within four actual images plus reference. It archives the original context stop before completing fresh critique. All 207 CPU tests pass on both hosts; renewed critique/native repair are pending at the 07:49 launch snapshot. The earlier service-door role separately exhausted 4,096 output tokens without a tool call; only fully saved lighting/props were qualified, and no truncated code was reused.

## N22 — A cloned imported child loses its parent transform

- **Symptom:** q0074's new bollards and dumpster are effectively invisible despite successful source edits and normal traversal. Existing large props in the junction image could be mistaken for successful new dressing.
- **Cause status:** native renderer/collider measurements verify clone world scale1 versus original imported scale100, plus changed world axes. The new bollard is about2.4mm high and the dumpster body about1.25cm high. Cloning the nested source object and reparenting it did not retain the imported parent transforms.
- **Failed approach:** rely on Instantiate plus SetParent(worldPositionStays=true) and comments promising world-transform preservation, without comparing original/clone native bounds.
- **Repair/outcome:** a bounded local-Qwen request will explicitly copy source world rotation and lossyScale before the existing bounds-based floor-placement calculation. Source objects, target positions and colliders remain intact. A new external gate compares original/clone component sets, world dimensions/axes and grounded placement before success notifications or full regressions. This gate is **implemented/tested**; the local/native repair outcome is **pending**.
- **Prevention/status:** actual import/instance parity checks and red fixtures for tiny/rotated clones, missing colliders and floating placement are **implemented/tested**. Pixel review still determines visual quality; numerical parity alone does not establish useful scenery.
- **Evidence:** [actual failed clone bounds and capture hashes](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/25f2b10/diagnostics/map-2026-10-06/alley-lighting-native-pass.json), [native clone checks](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/75eb0866eedbd6be27ee4fcd34ccf20708f308c0/tools/loop_controller/prop_clone_checks.py), [local repair controller](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/75eb0866eedbd6be27ee4fcd34ccf20708f308c0/tools/resume_alley_prop_transforms.py).

## N23 — Reviewing sealed evidence must not change its manifest

- **Symptom:** the bounded q0075 critic completes a real FIX, then the recovery stops with `Evidence manifest changed` before local game edits.
- **Cause status:** verified controller bug. The review method resealed the same capture directory, changing `sealed_utc`; the surrounding recovery then checked the prior manifest hash. All17 observation-file hashes verified, and the new seal time matched review start. The original context stop and completed review were preserved.
- **Repair/outcome:** [5e0fa48](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/5e0fa48a3f114bb0fa6879a0bdc47d07d62099f0/tools/continue_game_queue.py) reuses an existing seal only after verifying its bytes, candidate and scope. New evidence is sealed once. Changed observation bytes still halt. A one-time continuation pins the inspected manifest and complete critic hashes and does not repeat inference or reuse reasoning as code. All209 CPU tests pass on both hosts; the local prop/detail queue resumed at07:54:50UTC.
- **Prevention/status:** immutable-manifest reuse plus tests for changed pixels and wrong candidate/scope are **implemented/tested**. A generic manifest-change stop is never dismissed as metadata-only without diagnosing the write and checking actual records. The gameplay repair outcome remains pending.
- **Evidence:** [hash-pinned continuation](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/5e0fa48a3f114bb0fa6879a0bdc47d07d62099f0/tools/resume_prop_completed_review.py), [seal and recovery tests](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/5e0fa48a3f114bb0fa6879a0bdc47d07d62099f0/tests/test_prop_clone_checks.py).

**N22/N23 outcome, 08:17 UTC:** local source `2ab4676` passes all eight original/clone component comparisons, actual foot/car out-and-back, rendered support, all ten regressions and a complete independent scoped PASS. Accepted checkpoint `c9bbf1a` preserves the original failures and rough-art caveats. The first connector is accepted; final presentation, second street and ten-minute pacing are not. See the [accepted connector receipt](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/ff01deb/diagnostics/map-2026-10-06/accepted-connector.json).

## N24 — A real capture-time citation is rejected by a filename-only rule

- **Symptom:** q0076's critic returned a complete PASS citing actual times such as `t=10.8/12.9`. The controller rejected it for not naming a frame file; the correction then exceeded the context budget.
- **Cause status:** verified validation mismatch. The original complete tool call and all supplied images were preserved. Its cited times unambiguously round to the real capture schedule; it was not a missing verdict or fabricated observation.
- **Repair/outcome:** validate both actual filenames and unambiguous numeric time citations against the supplied schedule. The one-time recovery pins the original response, source, build, gate and immutable manifest, preserves the original verdict/summary/fixes, and promotes only after all required native evidence verifies. No inference was repeated and no manager verdict substituted. The first connector was accepted at08:17:29UTC.
- **Prevention/status:** time-citation validation and wrong/ambiguous-time red cases are **implemented/tested**. An unsupported citation still fails; a genuine critic FIX must never be upgraded merely because the parser was repaired.
- **Evidence:** [time-citation recovery](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/cd7bf62/tools/resume_timed_map_review.py), [validation](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/cd7bf62/tools/continue_game_queue.py), [accepted receipt](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/ff01deb/diagnostics/map-2026-10-06/accepted-connector.json).

## N25 — A saved presentation edit is routed into an unrelated whole-mission replay

- **Symptom:** q0077 saved only a door-depth correction after nine read turns and one edit. The separate replay role then exhausted8192output tokens after215.83seconds, with25550prompt tokens and no tool call. No street expansion, facade change or mission-pacing change was saved.
- **Cause status:** verified task-granularity/routing mismatch: a measured0.07m panel offset inherited the entire ten-minute polish task. The output stop is observed; internal reasons for spending the budget are not inferred.
- **Repair/outcome:** controller `d5bbfaf` verifies the exact saved diff and original stop, then reuses the immutable accepted connector inputs for fresh native qualification. A passive gate rejects the old hidden-wood geometry and excessive displacement. All ten regressions and a fresh scoped critic remain required. The subsequent street role receives exact preloaded source and separate bounded source/replay contracts; its acceptance measures travel beyond the union of both already accepted rectangles, so repeating the old alley cannot qualify. At08:43:57UTC the same owner is actually playing the fresh Unity build; native acceptance remains **pending**.
- **Prevention/status:** exact recovery, layer-order checks and a red old-alley replay against the new boundary are **implemented/tested**, with217CPU tests passing on both hosts. Small task decomposition remains a **procedure**, not a guarantee that local output or future topology will succeed. Original counters and the fixed project cap remain intact.
- **Evidence:** [bounded recovery and street roles](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/d5bbfaf/tools/resume_saved_door.py), [native geometry check](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/d5bbfaf/tools/loop_controller/prop_clone_checks.py), [red cases](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/d5bbfaf/tests/test_saved_door.py).

**N25 outcome and continuation, 09:05 UTC:** q0078 passes the unchanged physical route, all eight prop comparisons, measured wood/stone layer order and all ten regressions. The fresh critic returns **FIX** for door contrast/depth readability and oblique evidence; no door acceptance is claimed. One statement incorrectly identifies native frame001 as the AI target; that identity error is annotated separately without rewriting the verdict. Controller [8eaf29d](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/8eaf29d/tools/resume_second_street.py) preserves the exact review, candidate, counters and accepted fallback, carries the visual findings as unfinished work, and starts the independent second-street scope. This is advancement to other authorized work, not conversion of a FIX to PASS. Qwen has one active source request at09:05UTC; no second-street code or native outcome exists yet. All220CPU tests pass on both hosts. See the [complete native/critic receipt](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/fb029aa/diagnostics/map-2026-10-06/door-visual-fix-next-street.json).

## N26 — An ambiguous tool path wastes a complete local submission

- **Symptom:** q0079 submitted a complete 124-line, 6,971-byte street helper as `ConnectedStreet.cs`. The controller allowed only `Assets/Game/ConnectedStreet.cs`, but its error named the file rather than the actual permitted paths. The remaining role turns guessed other paths; no source was saved and no native build ran.
- **Cause status:** verified controller contract/guidance mismatch. The first submission finished normally with a real `create_file` call. Its 124 lines also exceeded the initial arbitrary 120-line wrapper limit by four; this was separate from the path rejection actually observed.
- **Failed approach:** repeat a generic rejection while expecting the author to infer a project-relative path from omitted inventory. Do not mistake the resulting lack of saved code for an absent implementation.
- **Repair/outcome:** controller [ba356d4](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/ba356d4/tools/resume_street_submission.py) lists the same two permitted paths in the prompt and schema enum, so invalid arguments return the exact choices. The one-time recovery verifies the original response hash, complete finish reason, single action, exact basename and reviewed size, then saves the unchanged helper at its sole permitted destination. It does not replay later placeholder/probing submissions. Six separate local-Qwen edits expose existing APIs and open/connect the new street. Integrated source **`6f9244b9`** is saved and published; at09:19UTC its local replay role is active and native qualification is pending.
- **Prevention/status:** exact path guidance, schema validation, hash-bound recovery, source/stop identity checks and narrow integration spans are **implemented/tested**, with224CPU tests passing on both hosts. Tests reject changed/truncated/multiple submissions, path traversal, unrelated paths and wrong source/state. The helper was preserved byte-for-byte; no source was extracted from private reasoning and file permissions were not broadened.
- **Evidence:** [source and provenance](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/b176e18/diagnostics/map-2026-10-06/second-street-source.json), [path and recovery tests](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/ba356d4/tests/test_street_submission.py), [local game source](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/6f9244b9045039e0749cd85489e55114b345e448/game/Assets/Game/ConnectedStreet.cs).

## N27 — A capped scene recorder misdiagnoses pavement and prop failures

- **Symptom:** q0081's unchanged second street physically traversed and returned, yet the prop gate reported missing dumpster components and the support analysis reported 52 uncovered samples out of 281.
- **Cause status:** verified infrastructure defect. The native recorder silently selected only the first 2,048 renderers. Its records omitted AlleyPavement and some original/clone components. Full recording observes 2,538 renderers and 46 colliders. Original and rerun physical traces are identical; checking the original trace against the complete scene records gives zero uncovered samples.
- **Failed approach:** interpret an incomplete component list as proof of a game defect. The first recorder repair then used an API that Unity 6000.6.4f1 rejects: `GetInstanceID()` is obsolete as an error. Its compile failure was incorrectly routed to the local gameplay author before the controller was stopped. Both speculative local edits remain preserved in Git ancestry.
- **Repair/outcome, 2026-10-06 09:58 UTC:** [7bc5a41](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/commit/7bc5a41e4a5afad37114eeb7382a2ec3c4cb26ca) uses `GetEntityId()`, records every renderer/collider after initialization, and checks explicit totals, completeness, time and unique component identities. Incomplete inventories and harness compile failures halt before gameplay edits. All235 CPU tests pass on both hosts. Native q0085 compiles and completes50.85seconds on Metal with zero runtime errors; unchanged source passes281/281 support samples, actual foot/car out-and-back, eight prop comparisons and door geometry. Full regressions and fresh scoped visual criticism are still pending at this snapshot; accepted `c9bbf1ac` remains unchanged.
- **Prevention/status:** complete-inventory metadata, truncation/count/duplicate-identity red cases, infrastructure compile-error routing and exact preserved-state recovery are **implemented/tested**. Snapshot completeness does not establish whole-run dynamic coverage or final visual quality. Source and acceptance criteria were unchanged, and the original failed evidence remains hash-identical.
- **Evidence:** [original/new hashes and measured diagnosis](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/da578ab/diagnostics/map-2026-10-06/complete-inventory-diagnosis.json), [recorder](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/7bc5a41/controller/unity/LoopRuntime.cs), [validation and recovery tests](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/7bc5a41/tests/test_scene_inventory.py).

## N28 — A fence-only change repeats a long route-authoring failure

- **Symptom, 2026-10-06 10:13 UTC:** q0086 saved a four-line original-fence placement as `b651a9f`, then its replay role exhausted8,192 output tokens in205.83seconds with no tool call. The route already had a sealed complete-inventory native pass and all ten regressions at q0085. The visual FIX concerned camera/street readability rather than missing physical traversal.
- **Cause status:** verified controller routing mismatch. A boundary presentation edit was sent through fresh route synthesis even though the exact tested inputs remained available for fresh candidate qualification. This repeats the earlier saved-edit replay problem; the earlier fix was too narrowly scoped to other recovery paths.
- **Repair/outcome:** [e420423](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/commit/e420423563e69ac7ae8b932d21f7d5f68141e354) pins the exhausted response, saved source, prior complete native gate, original FIX, immutable capture manifest and scenario. The same queue resumes with a fresh native fence diagnostic using those unchanged inputs, then a bounded local-Qwen camera-clearance span edit, existing near/middle/endpoint wall tests, full street suite and fresh criticism. Reuse never changes the FIX into PASS. All238 CPU tests pass on both hosts. At10:26:51UTC the owned native fence player is running; its complete inventory records2,770 renderers and47 colliders. Camera correction and final qualification remain **pending** at this snapshot.
- **Prevention/status:** this route reuse and exact-pause guard are **implemented/tested**; missing regressions, changed source identity, incomplete inventory and altered verdicts fail closed. This is not a generic permission to reuse inputs after arbitrary mechanics changes. Fresh native tests still decide whether the current candidate follows the route. Parent-requested mission pacing remains a separate subsequent scope.
- **Evidence:** [recovery and focused local camera role](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/e420423/tools/resume_street_readability.py), [red tests](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/e420423/tests/test_street_readability.py), [prior full native pass and preserved FIX](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/6863fc6/diagnostics/map-2026-10-06/second-street-visual-fix.json).

## Recording future incidents

Record: timestamp and scope; observed symptom; proven cause and separate
hypotheses; approaches actually attempted; effective repair and its measured
outcome level; pinned evidence; prevention status and meaningful regression
check. Preserve unresolved failures. Update old conclusions when new evidence
changes them, without deleting the earlier rejection or pretending a
recommendation had already prevented it.

[boundary]: https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/a66ecf8c925143ba373c932397356b1c23e63ffa/AGENTS.md
[map]: https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/a66ecf8c925143ba373c932397356b1c23e63ffa/diagnostics/map-2026-10-06/README.md
[spans]: https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/a66ecf8c925143ba373c932397356b1c23e63ffa/tools/resume_map_spans.py
[pavement]: https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/a66ecf8c925143ba373c932397356b1c23e63ffa/tools/resume_pavement_completion.py
[compile]: https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/a66ecf8c925143ba373c932397356b1c23e63ffa/tools/resume_map_compile.py
[map-tests]: https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/a66ecf8c925143ba373c932397356b1c23e63ffa/tests/test_map_extension.py
[replay]: https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/a66ecf8c925143ba373c932397356b1c23e63ffa/tools/loop_controller/replay_contract.py
[replay-tests]: https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/a66ecf8c925143ba373c932397356b1c23e63ffa/tests/test_replay_contract.py
[budget]: https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/a66ecf8c925143ba373c932397356b1c23e63ffa/diagnostics/framing-budget-2026-10-05/token-and-settings-audit.json
[prior]: https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/a66ecf8c925143ba373c932397356b1c23e63ffa/docs/PRIOR-ATTEMPTS.md
[coupe]: https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/a66ecf8c925143ba373c932397356b1c23e63ffa/diagnostics/coupe-2026-10-06/README.md
[controller]: https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/a66ecf8c925143ba373c932397356b1c23e63ffa/diagnostics/controller-2026-10-05/native-green-red.json
[physics]: https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/a66ecf8c925143ba373c932397356b1c23e63ffa/diagnostics/physics-repair-2026-10-05/README.md
[aim]: https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/a66ecf8c925143ba373c932397356b1c23e63ffa/diagnostics/aim-2026-10-05/README.md
[process]: https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/a66ecf8c925143ba373c932397356b1c23e63ffa/diagnostics/process-scan-2026-10-06/README.md
[camera]: https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/a66ecf8c925143ba373c932397356b1c23e63ffa/diagnostics/camera-2026-10-06/README.md
[camera-followup]: https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/a66ecf8c925143ba373c932397356b1c23e63ffa/diagnostics/camera-followup-2026-10-06/README.md
[review]: https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/a66ecf8c925143ba373c932397356b1c23e63ffa/tools/resume_review_case.py
[reuse]: https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/a66ecf8c925143ba373c932397356b1c23e63ffa/diagnostics/replay-2026-10-06/README.md
[map-status]: https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/a66ecf8c925143ba373c932397356b1c23e63ffa/docs/MAP-STATUS.md
[map-gate]: https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/a66ecf8c925143ba373c932397356b1c23e63ffa/tools/qualify_map_extension.py
[delivery]: https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/a66ecf8c925143ba373c932397356b1c23e63ffa/docs/THREE-DAY-DELIVERY.md
[runbook]: https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/a66ecf8c925143ba373c932397356b1c23e63ffa/docs/CONTROLLER-RUNBOOK.md
