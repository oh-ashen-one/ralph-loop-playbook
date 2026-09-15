# QUALITY LEDGER — Pitfight (worked example from a shipped 2D fighter loop)

Every claim about this game's quality, with the evidence that backs it and the
gate that keeps it true. A claim with no evidence id is a wish, not a claim.

| Claim | Evidence | Gate | Status |
|---|---|---|---|
| Fighters are sourced CC0 art, never programmer art | `assets/asset-manifest.json` (26 hashed, ship-approved entries); evidence `fight-open` | `preflight_assets.sh` + `tests_staged/test_sprite_fighters.gd` (0 Polygon2D on the fighter) | HELD |
| A punch is a complete feedback atom on a measured clock | contract `actionBeats.primary-action-beat`; evidence `primary-action` | `tests_staged/test_juice.gd` (blood emitting, flash, `hit_landed`) | HELD |
| Combat timing is frame-exact and gameable by the player | punch 4/3/6, kick 7/4/10 asserted | `tests_staged/test_punch.gd`, `test_kick.gd` | HELD |
| A KO resolves the round end-to-end with slow-mo that restores | contract `actionBeats.ko-beat`; evidence `failure` | `tests_staged/test_rounds.gd`, `test_announcer.gd` | HELD |
| The fight always fills the frame | contract `scale and camera`; evidence `fight-open` | `tests_staged/test_camera.gd` (zoom 1.4..2.6, midpoint tracking) | HELD |
| Audio is real measured foley, not synthesis | manifest audio rows carry durationMs / LUFS / peakDb | law-17 manifest validation | PARTIAL — files installed and measured; wiring story open (US-023) |
| Hits have impact-freeze weight | contract `actionBeats.primary-action-beat` channels | US-024 test (hit-pause frames) | OPEN |
| HUD survives a portrait viewport | evidence `mobile` (390x844) | `tests_staged/test_mobile_safe_area.gd` | OPEN |
| Worst scene holds 60fps | contract `performanceTiers.target` | evidence `worst-performance` + frame-time probe | OPEN |
| Provenance: every app line model-written or logged as a manager intervention | `scripts/ralph/prd.json` `interventionLog`, git history | law 13(b) intervention count (10 to date, all logged) | HELD |

## Honest limitations

- Bodies are stylized CC0 (KayKit); the pack caps how brutal this can look. A
  grittier pack is a swap, not a rewrite — the sprite pipeline is
  `tools/render_all.sh` and the game reads clips by name.
- No music bed, no crowd, no voice.
- Legacy scope note: US-001..US-022 predate law 17 and are not retro-fitted
  with `qualityClass` / `acceptanceCriteria`. New stories (US-023+) carry the
  full contract shape. `.ralph-quality-required` is deliberately NOT set on
  this project so the gate advises rather than blocks a finished game; it is
  set on every new scaffold.

## Reference lock

| Reference | Local | SHA-256 | Learn | Never copy |
|---|---|---|---|---|
| KayKit Adventurers 1.0 (Kay Lousberg, CC0) | `quality/references/kaykit-license.txt` | pinned in `quality/contract.json` | readable proportions at ~150px; distinct silhouette per combat clip; flat shading that survives ortho side render | MK/Injustice names, likenesses, logos, fatality staging, HUD layout, arena trade dress, KayKit promo art |
| Kenney Impact Sounds 1.0 (CC0) | `assets/audio/foley/KENNEY-IMPACT-LICENSE.txt` | per-file in `assets/asset-manifest.json` | impact weight and transient shape for punch/kick/block | any referenced game's announcer lines oraudio branding |

## Findings

Open findings become stories; a finding dies exactly once (the fix becomes an
assertion).

| # | Finding | Source | Story | State |
|---|---|---|---|---|
| F-01 | Synth stingers read as placeholder next to real foley | manager critique 2026-08-23 | US-023 | open |
| F-02 | Hits lack impact-freeze; damage registers but has no weight | manager critique 2026-08-23 | US-024 | open |
| F-03 | Arena is flat — braziers barely read, no depth behind the fight | frame critique of `fight-open` | US-025 | open |
| F-04 | HUD untested at portrait; safe area unverified | contract `inputMatrix[1]` | US-026 | open |
| F-05 | `impactMetal_light` measured -70 LUFS (silent) and would have shipped inaudible | law-17 audio measurement | fixed at source (swapped to `impactPlate_medium_001`) | closed |
| F-06 | Blood burst spawns at the victim's ORIGIN — a punch to the head sprays the floor | evidence `primary-action` | US-027 | open |
| F-07 | Hit flash blows the sprite to pure white; reads as a render glitch, not a blow | evidence `primary-action` | US-027 | open |
| F-08 | Brazier reads as an orange cone with no glow pool; both flicker in phase | evidence `fight-open`, `primary-action` | US-025 | open |
| F-09 | Portrait 390x844: health bars merge into one strip, timer clipped, GRIM half off-screen | evidence `mobile` | US-026 | open |
| F-10 | Arena "depth" shipped as a maroon flood — glow widened to 1760x180 @ a=0.35 | evidence `fight-open` after US-025 | US-025 int. #1 | closed |
| F-11 | Braziers sat at x=180/1100, permanently outside the fight camera's framing — decor that never appears | evidence `fight-open` | US-025 int. #1 | closed |
| F-12 | Brazier flame was a fighter-height spike standing in FRONT of the bodies | evidence `fight-open` | US-025 int. #1 | closed |
| F-13 | Structural-only assertions (`z_index < 0`) pass look regressions; restraint needs its own assertion (size/alpha/on-screen) | manager critique | spec tightened in `test_arena_depth.gd` | closed |
