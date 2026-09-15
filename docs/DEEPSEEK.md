# DeepSeek-V4-Flash as the loop model (2026-08-17 session)

Porting the gaming Ralph loops from Qwen 3.8-27B to DeepSeek-V4-Flash (284B /
13B-active MoE) on an Apple-silicon box with 256GB unified memory. What it
took, what changed, what stayed true.

## Serving recipe (working, ~20.5 tok/s decode)

- Weights: `mlx-community/DeepSeek-V4-Flash-mxfp8` (~155GB; pick mxfp8 over
  nvfp4 — same footprint, better accuracy).
- mlx-lm PyPI (0.31.3) and upstream main still have NO `deepseek_v4` support;
  LM Studio can't load it either. Use the fork:
  `pip install --force-reinstall 'git+https://github.com/Blaizzy/mlx-lm@pc/add-deepseekv4flash-model'`
  in a python3.11 venv. The fork loads the model repo's `chat_template.jinja`
  and tokenizer fine (the April-era tokenizer workarounds are no longer needed).
- Serve via `mlx_lm.server` (OpenAI-compatible, SSE streaming) wrapped by
  a small `scripts/serve-model.py` wrapper in the project repo, which sets:
  - `mx.set_cache_limit(4GB)` + `mx.set_wired_limit(200GB)`
  - a daemon thread calling `mx.metal.clear_cache()` every 20s
  - `--prefill-step-size 512` (first-run shader compile otherwise trips the
    macOS GPU watchdog: "Caused GPU Timeout Error")

## The 499000 crash (the big one)

Long generations died mid-stream at ~9-11k tokens:
`RuntimeError: [metal::malloc] Resource limit (499000) exceeded` in
deepseek_v4.py rope (`offset // freq_scale`). 499000 = the device's concurrent
Metal resource limit (`mx.device_info()['resource_limit']`). Live buffers
accumulate roughly with generated tokens. Mitigations that got generations past
the crash point: 4GB cache limit + 20s `clear_cache()` janitor + capping loop
replies at 8192 tokens (which law 2 wanted anyway: stories ≤ ~15KB replies).
Not root-caused inside the fork; if a generation must exceed ~10k tokens,
expect it to die — design stories so they never must.

## Runner deltas vs the Qwen harness (ds_iteration.py)

- NO `</think>` assistant prefill, no `enable_thinking:false` stacking.
  DeepSeek answers in `content` directly at `reasoning_effort: "low"`; the
  reasoning_content fallback stays as insurance.
- Sampling per DeepSeek's agentic recommendation: temperature 1.0, top_p 0.95
  (not the Qwen 0.7/0.9/top_k 20).
- `max_tokens` 8192 (see above), chat timeout 1800s unchanged.
- Added `### PATCH:` block support per HARNESS.md (the phased reference runner
  lacked it).
- Write fence is project-shaped (src/, public/, index.html), not Godot-shaped.
- Endpoint: `DS_API` (default :8888 mlx_lm.server), `DS_MODEL` = full local
  model path — mlx_lm.server treats the request's `model` field as a HF repo
  id and 404s on anything else.

## Early behavioral observations (vs 27B priors)

- First US-000 replies ran 27-43KB (too big): even a strong model over-emits
  when a story names 4 files. The fix was the cap + story text, same as law 2.
- When verify returned exact TS errors, the next iterations targeted them —
  the law-6 loop works as well here as with Qwen.
- Iteration pace at ~20 tok/s: ~5-7 min. A phase of 4 stories is an overnight
  quantity, not an evening one. Plan checkpoints accordingly.

## Ops notes

- tmux demo sessions died with the old tmux server during stand-down; restart
  dev servers from their project dirs if wanted.
- The slots dir's `PAUSED` sentinel was stale from the failure-38/39/40 ops
  work; removed for this session. Re-`touch` it to freeze all claims box-wide.
