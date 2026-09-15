# Critique protocol — phase 2 for every project

Adapted from gillworks/red-sands docs/{PROCESS,CRITIC}.md. Core law:
**the builder never grades the build.** Qwen builds; independent judgment decides.
Every finding becomes a prd.json story with a mechanical verify, and every fixed
defect stays asserted so it can never return.

## When

After a project's functional stories all pass, BEFORE calling it done or pushing
the public repo. Repeat passes until a fresh pass files nothing.

## Instruments (manager runs these)

1. **Canonical shots** — headless screenshot set per project (the Dusk games'
   `tools/shoot.mjs` pattern): title, mid-action, UI-heavy, night/edge states,
   mobile width for web. Same shots every pass so passes are comparable.
2. **Lens critique** — score each shot on the stingy scale below through three
   separate lenses (never averaged): light/atmosphere · material/detail ·
   composition/believability. A finding must name shot + defect + concrete fix +
   owning file, or it is rejected.
3. **Forensic provenance test** — fresh eyes, one frame: "shipped game/site or
   AI-generated hobby output? List the tells." Every tell filed as a story.
   Win condition = "uncertain", not a score.
4. **Scripted regression** — each fixed defect gets a permanent assertion in the
   story's verify chain (grep, pixel probe, fps floor, bundle size, lighthouse).
   Findings die once.

## Scale (stingy on purpose)

1 broken · 3 typical AI/demo output · 5 competent indie · 7 good AA · 9 shipped AAA

Ship bar: no shot below 5, majority at 6+, provenance "uncertain" or better.

## Idea injection

Reference techniques by name in briefs/stories when filing fixes (aerial
perspective, fog = horizon color, instancing, LOD, filmic grade). MIT reference:
red-sands source may be READ for technique study, never pasted into
Qwen-only repos — Qwen writes every line of app code.
