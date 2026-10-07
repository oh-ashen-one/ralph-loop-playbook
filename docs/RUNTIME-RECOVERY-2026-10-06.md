# Same-model runtime recovery, 2026-10-06

Official oMLX 0.7.0 restored useful short-request performance for the existing
Qwen workload. The matched text control improved from **2.60 to 73.37 decode
tokens/second**, about **28.2×**. The upgraded service also passed a typed tool
call and actual-image recognition. This is a verified operational remedy for
this incident; the precise slow kernel, runtime interaction or OS cause was
**not isolated**. A short control is not a sustained-throughput guarantee.

## Exact qualified configuration

| Component | Slow installation | Qualified replacement |
|---|---|---|
| Host | Apple M5 Ultra, 80 GPU cores, 256 GB unified memory | Same machine |
| Model | `mlx-community/Qwen3.8-Flash-Next-oQ6e-mtp` | Same weights |
| Model revision | `e171af86f499f1855b0fb71d781105e8dd609610` | Unchanged |
| Python | 3.12.13 | 3.12.13 |
| oMLX | 0.6.4, commit `1d7826185c5b5b69b38b27cbe57d7597b7551fd7` | Official stable 0.7.0, commit `4d4f5a280bc1739ba2cf39c1cee44fd5cc89cb40` |
| MLX / mlx-metal | 0.32.0 | 0.32.2 |
| mlx-lm | 0.31.3; commit `ab1806e8f5d6aa035973af194a1b9198ab4754dc` | `0.31.4.dev132+g94cdcae13`; commit `94cdcae13b266c337bcaca09b97b9c5a9c0e2cde` |
| mlx-vlm | 0.6.3; commit `78b96eb5462141447b9a6b4943ef553891da56dd` | 0.7.1; commit `ea79808ce1e9a19fcb915a96b0c70e37ad393a99` |
| Transformers | 5.12.1 | 5.17.0 |

The official CPython 3.12 universal2 wheel SHA-256 was
`42ff3d25a40468781110933a64dc7037dcbe8590ab93851db82a12a5df81617b`,
verified against its GitHub release asset digest before installation. Its
declared dependencies, including upstream Git pins, were installed in a new
virtual environment. Native extensions imported successfully on the M5;
Metal was available. Startup recorded Qwen compatibility, resident packed PLE,
96 exact hybrid projection pairs, 97 compiled decode paths and the release's
fused MoE optimizations. These logs establish enabled setup, not execution
of every optimized branch on every request. See the [official release](https://github.com/jundot/omlx/releases/tag/v0.7.0).

Settings retained: one loaded model and one concurrent request; native context
262,144; server default output cap 8,192; MTP, DFlash, KV quantization, APC and
PLE SSD offload disabled; remote code disabled; offline weights. The internal
custom memory ceiling remains 192 GiB. External guards retain at least 64 GiB
available memory, at most 512 MiB additional swap, desktop/access/thermal checks,
actual shared-slot locks and the original fixed project deadline. No privileged
wired-memory setting, OS power change, community patch or other-job intervention
was used. The two installations and configuration directories remain separate.

Game sampling remains temperature 1, top-p .95, top-k 20, min-p 0, repetition
penalty 1, presence penalty 0, with thinking and history preservation enabled.
Role effort is deliberate: the resumed complete-character save uses `low`.
The short diagnostics alone used temperature 0, top-p 1 and thinking disabled.
Do not accidentally copy diagnostic thinking settings into the game roles.

## Measured controls and limits

| Control | Output tokens | 0.6.4 decode | 0.7.0 decode | Replacement outcome |
|---|---:|---:|---:|---|
| Matched text, about 2,000 tokens of code context | 160 | 2.60 tok/s | 73.37 tok/s | Numeric-output sanity passed |
| Typed inert tool call | 38 on 0.7.0 | Correctness passed in baseline | 90.92 tok/s | Exact requested integer/string arguments |
| Actual native image and structured observation | 40 on 0.7.0 | Correctness passed in baseline | 89.47 tok/s | Correct blue car and visible person |

The matched text request used 2,065 prompt tokens in both versions. Wall time
fell from 66.9917 to 8.2283 seconds; first visible content took 5.6063 and
6.2592 seconds respectively. Decode rates above are server usage measurements,
separate from prefill and total elapsed time. The 0.6.4 image timing control
also showed 2.64 tok/s for 32 tokens, but its prompt/output differ from the
new image correctness call; **do not claim a matched image speedup**.

The replacement's three requests completed at 22:11:34 UTC. Swap growth was
zero and approximately 92.4 GiB remained available after the image check.
Other authorized workloads were left alone, so this is not an isolated
hardware benchmark. The service was promoted based on these limited speed
and correctness checks; native game quality remained unqualified. The first
resumed real character request then saved a complete source file: 13,242 prompt
tokens, 7,822 output tokens, 108.4 seconds total and 77.53 decode tok/s. This
confirms useful performance on one substantive request, not an unlimited
sustained guarantee. Its first Blender export failed because the local source
called nonexistent `Matrix.Euler`; the complete file is preserved and a
separate local API/transform repair follows. Runtime recovery is not asset
correctness or native visual acceptance.

## Cost of the failed strategy

Two character-authoring requests ended with `length`, without a parsed tool
call, source save, Blender export or native preview:

- Broad character/camera author: 16,384 output tokens, 4,117.70 seconds
  (**68m 37.70s**), completed 21:03:29 UTC.
- Focused complete-character author: 8,192 output tokens, 3,082.65 seconds
  (**51m 22.65s**), completed 21:58:05 UTC.

Together they consumed about **two hours without an artifact**. The smaller
prompt did not restore runtime speed. Advancing tokens were incorrectly
allowed to stand in for useful progress; a stall-only watchdog could not
catch very slow generation. Both private responses, histories and failed
outcomes remain preserved. Partial code and private reasoning were not
executed or published. The subsequent low-effort local continuation receives
the inspected private response as retained work; a complete tool submission
must still pass the unchanged source boundary before export.

## Deployed controls versus operating procedure

**Deployed in the game controller:** [fd06f35](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/commit/fd06f359af82052be272907b25b6ee131c5d1d06)
adds opt-in monitoring around model requests. Current configuration enables it
for subsequent role sessions. It samples read-only token counters every five
seconds, requires the same request over at least 60 seconds, then two consecutive
slow observations below 20% of the qualified text rate (14.674 tok/s here,
with an 8 tok/s minimum floor). A separate ten-minute elapsed request ceiling
still applies if telemetry is unavailable. It verifies the owning controller's
PID creation time and round before signaling that controller gracefully.
It never restarts inference, signals another job, or edits source. Missing
telemetry is recorded rather than called a proven stall. Tests cover slow,
healthy, too-short, changed-request and counter-reset observations.

The continuation separately verifies the exact paused source, accepted checkpoint,
fault history, prior response digest and qualified runtime. It allows one
low-effort character recovery with at most two tool turns. Source save, Blender
export, native preview and actual pixel inspection are distinct boundaries.
No source/quality success is inferred from token rate. Five relevant CPU tests
passed on the M5; eight character/camera/recovery tests passed on the controller.

**Procedure for future setup and deviations:**

1. Start from a published compatible configuration. Verify hardware, exact model
   revision, stable runtime release, dependency commits, native extension imports,
   effective settings, one service/owner, source checkpoint and existing workload
   boundaries. Keep a small provenance record. Do not start by inventing a new stack.
2. Run only a short representative speed request and required tool/image checks.
   Record token counts, prefill, decode, total time and memory. Compare the same
   workload where claiming a speedup. Preserve thinking/sampling differences.
3. If performance is far below a relevant published setup, pause long authoring.
   Check installed versions, supported settings, logs and exact deviations first.
   Inspect source/kernel eligibility only to investigate an observed discrepancy.
   Do not default to a broad benchmark campaign or repeated long requests.
4. At a safe idle boundary, preserve old environment/configuration and pinned
   weights, then trial an official update in isolation. Stop the old owned service
   gracefully before loading its replacement. Never load two copies for an A/B.
5. Promote only after identity, correctness, memory and short speed checks pass.
   If startup, tools, images, pressure or throughput fail, preserve evidence and
   restore the old qualified service/config at an idle boundary. Do not overwrite
   either environment. Restoration is a deliberate recovery, not a restart loop.
6. During authoring, monitor sustained speed and artifact delivery separately.
   A guarded stop requires a concrete diagnosis or supported configuration change
   before another bounded request. A second unchanged output-limit failure is
   evidence to change strategy, not permission to increase budgets indefinitely.

These startup and recovery steps are **documented procedures**, not a universal
automated preflight or automatic rollback installer. The project-specific
watchdog and state checks above are implemented; success cannot be guaranteed
for other models, request shapes, host loads or future versions.

## Preserve the other lessons

Shared admission must inspect actual locks and pressure. The deployed
[one-free-slot repair](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/28499bc/tools/shared_capture_slots.py)
reaches both controller and resident; mere presence of another authorized
application does not veto this task. Exclusive reservations, both occupied
slots, shared pause and real ownership/resource faults still stop admission.
Never raise limits or alter another project to manufacture a pass. See N48/N50.

Visual authoring must receive actual relevant target/native image bytes with
request receipts. Broad visual review needs all five targets. A scoped mechanical
PASS is not broad visual approval. Keep movement/hit/camera/native gates,
source-matched screenshots, independent criticism and accepted checkpoints;
require the next actual export/render after every asset change. The earlier
140 of 158 image-free builder sessions and primitive character are workflow
findings, not evidence that the model is incapable or that final quality has
been reached. See N52 and the [native runbook](LOCAL-NATIVE-LOOPS.md).

The [published M5 setup](https://github.com/sethforprivacy/Qwen3.8-Flash-Next-M5-Ultra-oMLX/blob/main/docs/RESULTS.md)
was a useful compatibility/performance reference, not a script to execute
blindly: its runtime prerelease, request methodology, thinking mode and wired
memory setting differed. This recovery used official stable dependencies and
existing authorized memory settings. Root-cause hypotheses remain separate
from the measured benefit of the official update.

## Subsequent integration evidence, 23:21 UTC

Restored decode speed did not remove other failure modes. Two later resident
stops measured available memory below the unchanged64GiB floor, with no swap
growth. The game now deliberately separates authoring and native validation:
stop only the idle owned model before native work, preserve shared admission,
and reload deliberately only after measured headroom returns. The native-only
controller retains the original memory/swap/thermal/ownership guards and an
exclusive reservation of the inference port. No automatic restart loop is
implemented. A temporarily unavailable port after graceful unload was preserved
as a pre-engine interruption; recovery followed a successful exclusive bind.

The owner now requires high reasoning for substantive integration. Actual
reticle request receipts verify supported `xhigh`, thinking preservation and
the supplied reference/native image hashes. An8192-token high-effort response
and a separate16384-token shader response each reached their output caps without
saving. Retaining the exact private local work, rather than repeating the fresh
request, produced complete submissions in22.98and30.91seconds. Neither response
was parsed for partial code, and reasoning was not published. This is a measured
recovery technique, not evidence that larger budgets always solve non-delivery.

The first complete reticle submission still used nonexistent Unity GL methods.
Installed API documentation caught that incompatibility before an engine run.
The final local-authored C#/shader candidate compiled and visibly drew the
center reticle in both a normal player framebuffer and an explicit
`Camera.Render` target. It also passed the current-source95-second route and
camera-clearance check. Comments claiming capture support and a green gameplay
gate had not established that visible requirement. Give the local author actual
API context and enough permitted source scope to implement the dependency; an
existing-shader-only restriction had been too narrow here.

Capture UTC now records actual PNG-write completion in the native harness.
Keep that distinct from a render exposure timestamp, file-copy mtime and Library
upload time. When the supported prepared-upload route reported unavailable,
the explicitly authorized direct Library create route succeeded; returned file
identities and metadata were applied without altering PNG bytes. This observed
fallback is not a claim that all installations expose both routes.

See the [source-linked integration audit and remaining findings](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/352de31/docs/INTEGRATION-AUDIT-2026-10-06.md).
The segmented character, missing demonstrated rig/animation, chapter death
gating, material lifetime and HUD-state issues are not resolved by the reticle
pass. Native zero-health diagnostics are running before the next local repair.

## Native boundary precision, October 7

The six chapter death diagnostics subsequently reached valid live states and
reproduced dead-player controls. One setup was initially rejected because Unity
serialized float32 `59.6` as `59.599998474121094`, below the Python validator's
decimal-double lower bound. Compare the native representable boundary, not an
arbitrary wider tolerance. A regression must still reject an earlier frame and
the missing required input. Preserve the original rejected gate and trace;
record a separate hashed reconciliation and rerun only unfinished cases.
This acceptance correction is not a gameplay repair. See the
[six-case findings](https://github.com/oh-ashen-one/M5-Ultra-Qwen-3.8-Gaming-Loop/blob/3926414/docs/INTEGRATION-AUDIT-2026-10-06.md).
