# ralph-loop-playbook

Use the existing [SKILL.md](SKILL.md) to set up and supervise local-model
coding loops, with bounded edits, independent acceptance and honest handoffs.
The repository includes a legacy FILE-block harness and guidance for qualified
native tool controllers. Select the matching profile before copying commands.

The [local native runbook](docs/LOCAL-NATIVE-LOOPS.md) and
[dated error log](docs/LOCAL-NATIVE-ERROR-LOG.md) incorporate the October 2026
Chicago game work. They preserve unsuccessful attempts and distinguish source
changes, accepted subfeatures and unfinished product goals. The game is not
presented as a completed ten-minute release.

## What's inside

| Path | What |
|---|---|
| `SKILL.md` | The router: when to use a loop, the core loop mechanics, the three roles, the map of everything else |
| `FAILURES.md` | 81 historical failure cases, including superseded repairs |
| `docs/LOCAL-NATIVE-LOOPS.md` | Current native tool profile: prompts, budgets, assets, physical/visual gates, ownership and scope |
| `docs/LOCAL-NATIVE-ERROR-LOG.md` | Dated incidents with cause status, failed attempts, effective repairs, pinned evidence and prevention status |
| `docs/` | The playbook, harness internals, manager runbook, story/prompt authoring, engine & tooling rankings, overnight checklist, pre-mortem method, anti-slop design bibles, CC0 asset sourcing, Blender modeling, ops (phase gates, GPU slots, watchdogs) |
| `reference/` | Battle-tested runner scripts: iteration runners (plain + phase-gated), loop script, supervisor with typed exit routing, project scaffold, stuck detector, Godot verify wrappers, prompt/grounding templates |
| `quality/` | The law-17 production-quality contract: brief/contract/prd/ledger templates + a launch-blocking preflight validator + worked examples from a shipped game |
| `overseer/` | The AI-manages-AI tier: telemetry packet, JSON-action-only manager prompt, dumb capped executor, event-triggered check-ins, pluggable pager |

## Quickstart

For an existing qualified native controller, start with the [native runbook](docs/LOCAL-NATIVE-LOOPS.md); preserve its owner, runtime and acceptance. The commands below are only for the legacy harness after the owner has authorized setup and launch.

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
