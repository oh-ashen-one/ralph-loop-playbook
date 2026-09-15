# Production-quality launch kit

This directory converts the Rork game study into a hard Ralph preflight. It is
copied into every newly scaffolded project under `scripts/ralph/quality/`.

The gate requires, before Qwen starts:

- sourced, locally staged, ship-approved assets with source, license, SHA-256,
  semantic roles, fallbacks, dimensions/axes, root-motion policy, and complete
  character clip roles; locomotion has a measured gait cycle and action/fail
  clips have a measured contact frame;
- an original product fantasy and decomposed references that say what to learn
  and what recognizable IP/trade dress not to copy; local reference evidence is
  staged and hash-pinned so the visual target cannot silently drift;
- a complete boot/loading/menu/play/pause/failure/restart/settings shell with
  persistence and missing-media behavior, without forcing irrelevant meta bloat;
- one authoritative source for rendering/gameplay quantities that must agree;
- seven story classes: vertical slice, look lock, asset integration, feedback
  atom, camera/input, performance/resilience, and critique/ship;
- no more than two emitted source files per story;
- a manager-owned, implemented red test for every story, outside allowedFiles;
- deterministic canonical evidence for title, traversal, primary action,
  failure, mobile, and worst-performance states;
- a complete state/motion/visual/audio/HUD action beat;
- target-device input and performance budgets;
- explicit pool capacity, asset-load concurrency and resident-asset budgets;
- a deterministic debug bridge and human checkpoints after look lock and before
  ship;
- a quality ledger and honest proof boundaries.

Run manually:

```bash
python3 scripts/ralph/quality/preflight_quality.py --root "$PWD"
```

Run its own red/green tests from this playbook repository:

```bash
python3 -m unittest reference/quality/test_preflight_quality.py
python3 -m unittest reference/test_phase_gating.py
bash reference/test_preflight_assets.sh
bash reference/test_scaffold_quality.sh
```

`reference/scaffold_project.sh` creates `.ralph-quality-required`; when that
sentinel exists, `run_loop.sh` executes this validator before claiming a GPU
slot. The sentinel is present by default for every future scaffold.
