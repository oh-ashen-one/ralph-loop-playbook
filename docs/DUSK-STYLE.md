# DUSK — the house design system for game UI

Extracted from Dusk Riders + Dusk Skaters (the two best Qwen 3.8 outputs to date).
Apply to every game project's menus/HUD unless its brief overrides.

## Palette

- Ground/panels: deep plum `#1D1030` … `#241535`; panel fill `#241535` at ~92%
- Display type: cream `#F5E3C0`
- Hard drop shadow on display type: hot pink `#E13F7B`, offset 4-6px, NO blur
- Accent 1 (labels, lines, minimap): teal `#3FE0C5`
- Accent 2 (CTA, highlights, score numerals): orange `#F5842D` / gold `#F0C060`
- Muted text: dusty lavender `#8E7BB8`

## Type rules

- Display: heavy weight, ITALIC, tight tracking, ALL-CAPS ("DUSK RIDERS", "TIME!")
- Sub-lines: light weight, HUGE letterspacing (0.4em+), teal, all-caps
  ("SUNSET GRAND PRIX — LAP 3 OF THE GOLDEN HOUR")
- Data (speed, score, laps): bold italic, cream/gold, tabular
- Key hints: "W / ↑ THROTTLE" pattern — bold key, light action, one line

## Panel rules

- Panels are SKEWED (2-4° parallelogram) with a hot-pink or darker offset shadow
- 2px borders in a darker plum; no border-radius, no blur, no glassmorphism
- Results screens: centered skewed panel, stat rows divided by 1px teal hairlines,
  right-aligned gold values, letter RANK with pink shadow
- Corner HUD: position badge top-left, minimap panel top-right with teal path line,
  gauge bottom-left (teal arc speedometer)

## Feel

- Every sky is golden hour or dusk: painted sun disks, layered horizon bands,
  apricot → cinnabar → plum gradients
- One pulsing CTA ("PRESS ANY KEY") at 0.8Hz, orange, skewed
- No Inter, no purple-glow gradients, no centered-card tutorial slop
