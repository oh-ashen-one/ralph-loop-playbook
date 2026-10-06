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

## N04 — Complete proposal rejected by a line ceiling

- **Symptom:** q0054 emitted one complete 47-line, 3,041-byte pavement tool call against a 45-line cap.
- **Cause status:** verified edit-size validation, distinct from output truncation.
- **Failed approach:** treating a complete over-limit submission as if no usable tool proposal existed, or regenerating its entire content unnecessarily.
- **Repair/outcome:** hash-pinned recovery accepted the exact tool content with a bounded 50-line cap, preserving the original rejection. Source `b28bf88` saved; later compile failure means this was not native acceptance.
- **Prevention/status:** response/proposal hashes and one-time state validation are **implemented**. Inspect the complete proposal, preserve provenance, and retest resulting source; do not use private reasoning as fallback code.
- **Evidence:** [pavement recovery implementation][pavement], [map chronology][map].

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

## Add the next incident

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
