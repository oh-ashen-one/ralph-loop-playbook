# ralph-loop-playbook

**Feed this repo to your AI agent (Claude Code / Codex / Kimi / etc.) — e.g.
copy it into your agent's skills directory or paste the `SKILL.md` — and it
can run autonomous "ralph" loops where a small local model (27B-class, e.g.
Qwen via LM Studio) builds complete, non-slop software for hours at a time,
and manage those loops the way a senior engineer would.**

This is a methodology repo, not a source release: the hard-won lessons,
harness code, failure catalog, and manager/overseer patterns extracted from
real projects that were built 100% by a local model writing to mechanical
gates. The difference between "local model slop" and "shipped product" was
never the model — it was the harness, the stories, and the judging. That is
what lives here.

## What's inside

| Path | What |
|---|---|
| `SKILL.md` | The router: when to use a loop, the core loop mechanics, the three roles, the map of everything else |
| `FAILURES.md` | 81-entry failure catalog: symptom → root cause → fix. The crown jewel — read it twice |
| `docs/` | The playbook, harness internals, manager runbook, story/prompt authoring, engine & tooling rankings, overnight checklist, pre-mortem method, anti-slop design bibles, CC0 asset sourcing, Blender modeling, ops (phase gates, GPU slots, watchdogs) |
| `reference/` | Battle-tested runner scripts: iteration runners (plain + phase-gated), loop script, supervisor with typed exit routing, project scaffold, stuck detector, Godot verify wrappers, prompt/grounding templates |
| `quality/` | The law-17 production-quality contract: brief/contract/prd/ledger templates + a launch-blocking preflight validator + worked examples from a shipped game |
| `overseer/` | The AI-manages-AI tier: telemetry packet, JSON-action-only manager prompt, dumb capped executor, event-triggered check-ins, pluggable pager |

## Quickstart

1. Read `SKILL.md`, then `docs/PLAYBOOK.md`, then skim `FAILURES.md`.
2. `reference/scaffold_project.sh /path/to/project my-game 3d` — full
   harness + quality contract, launch-blocked until art and tests are real.
3. Follow `docs/MANAGER.md` "Starting a run" — art first, then brief, then
   prd, then red-tested gates, then one dry-run iteration.
4. Launch with `reference/run_loop.sh <name>`; supervise per
   `docs/MANAGER.md` or hand the loop to `overseer/`.

Prerequisites: LM Studio (or any OpenAI-compatible local server) with a
27B-class model, an Apple-silicon Mac with ≥64GB RAM (or equivalent), plus
`python3`, `jq`, `git`, and per-stack verify tools (node/playwright, Godot 4
headless, Blender headless) as needed.

## Credits / lineage

- Ralph pattern: Geoffrey Huntley, `snarktank/ralph`
- Judging/critique protocol: adapted from `gillworks/red-sands`
  (PROCESS/CRITIC)
- Arena build process: somethingbig.ai gauntlet-loop + Matt Schumer's
  `mshumer/Claude-of-Duty` (MIT)
- Story pre-flight checklist idea: inspired by Claude-Code-Game-Studios
- Capture/metrics instruments: `achimala/TheLongSilence`

## License

MIT — see `LICENSE`.
