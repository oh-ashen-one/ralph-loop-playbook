# THE GAUNTLET — the arena's build process (stolen wholesale, MIT sources)

Sources: somethingbig.ai/gauntlet-loop + mshumer/Claude-of-Duty (MIT,
pinned in fixtures/). This is THE method for every arena build, cloud or
local. Not adapted per-lane in philosophy — only in mechanism (§5).

## 1. The method (verbatim principles)

1. **Actual agentic harness.** Claude Code / Codex / Kimi CLI / the ralph
   loop. Never a plain chat.
2. **Goal, not implementation.** The brief names the destination and the
   bar. The lead agent chooses the route. Do NOT prescribe architecture.
3. **A real bar.** Concrete, inspectable reference: frames pulled from
   cinematic game footage, staged locally (runs/ep02/references/).
   "Amazing" is not a bar; a frame you can blind-A/B against is.
4. **The lead splits the work.** Smallest independently-judgeable pieces
   (grass, lighting, water, horse gait, character, sky…). The lead decides
   the pieces, not us.
5. **Builder + fresh-context critic per piece.** The critic gets goal +
   bar + the artifact's REAL PIXELS — never the builder's history or
   explanation. Blind A/B where possible: "which looks better?" Ours loses
   → critic names the biggest gap → builder fixes → gauntlet again.
6. **No arbitrary final round.** Loop until the output wins or the
   director stops the run. Budget caps exist for safety (manifest records
   which fired), never as quality targets.
7. **Live progress page.** Every contestant maintains a live HTML page
   with evolving screenshots. The director watches from anywhere; steering
   checkpoints (RULES.md) coexist — the page makes waiting visible.
8. **Smoothing pass between waves.** One fresh agent unifies separately
   improved pieces into one coherent artifact. Not a redesign.
9. **Ultracode on mains** (Claude lane: /effort ultracode). Accepted
   quota burn; the manifest logs it.

## 2. The main-brief template (his style — SHORT)

> Build [GOAL — e.g. a cinematic-reference-vibes open field in Three.js:
> spawn on foot in a golden-hour grassland, walk, mount a horse,
> ride]. The bar is [reference frames — attached]. Break the work among
> subagents. Put every important piece through its own loop with a
> separate, harsh visual critic that compares our output side by side
> with the reference. When ours loses, keep improving it. Use the staged
> assets in ./assets (ronin GLB, kits). Keep a live progress page updated
> with screenshots. Use subagents and ultracode.

## 3. The engine contract (OVERWATCH, adapted from his ARCHITECTURE.md)

1. You own your directory. Never edit outside it.
2. No cross-subsystem imports — runtime `ctx.get('name')` only.
3. No new dependencies without manager approval.
4. Seeded RNG only — capture reproducibility depends on it.
5. Allocate nothing per-frame; preallocate in init().
6. Dispose what you create.
7. Build + boot must pass after every change. Break the boot, everyone
   stops.

## 4. Staged assets (manager's job, pre-brief)

- Ronin GLB (runs/ep02/staging/ — concept V4, Hunyuan v3 mesh, rigging
  next), village/prop kits, reference frames. Every contestant gets the
  IDENTICAL staging. Models never start from a gray box.

## 5. Local-lane mechanism (same gauntlet, different engine)

The 27B cannot orchestrate a subagent fleet. Its gauntlet: the ralph loop
— prd stories ARE the pieces, manager-authored verifies ARE the critics,
CRITIC.md phase IS the blind-A/B round (screenshot vs reference, "list
the tells", file as new stories, repeat until a fresh pass finds nothing).
Disclosed in the manifest; same philosophy, honest mechanism.

## 6. What we add that he doesn't have

- Director checkpoints (steering without touching code)
- Blind cross-model judging + price-performance table
- The local division (overnight home-machine runs)
- The 3x consistency gauntlet on the anchor test
