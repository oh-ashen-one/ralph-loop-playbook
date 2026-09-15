# Anti-Slop

Slop is what a model produces when nobody made the decisions for it: Inter on a
purple gradient, three equal feature cards, a rotating cube, gray-box levels,
default-lit noon scenes. Small models emit the median of their training data.
The counter is never "be creative" — it is **decide everything upstream**.

## The three layers

1. **Design bible in every prompt** (BRIEF.md, injected into each iteration):
   exact palette hexes, type rules, panel rules, feel constants, a signature
   element, and an explicit slop-list of forbidden defaults. See
   `DUSK-STYLE.md` for a complete worked example that shipped across a kart
   racer, a skate game, a voxel game's UI, a football broadcast package, and a
   Roblox round-game UI — one house system, reused.
2. **Verifies that encode the bar**: greps for the tokens/values the bible
   demands, line-count minimums on CSS, screenshot-diff gates once you have
   capture tooling. "Substantial CSS, multiple components" as assertions.
3. **The critique phase** (CRITIC.md): after functional, screenshot everything,
   run the provenance test ("shipped or AI hobby output? list the tells"),
   file every tell as a story with a mechanical verify. Repeat until a fresh
   pass finds nothing. The stingy scale matters: 3 = typical AI output,
   5 = competent indie; ship bar is nothing below 5.

## Where taste actually enters the pipeline

- The manager picks the vision (one line) and derives values from it.
- Mine your own best outputs: when a generation is good, extract its palette,
  type, and layout into the house system and reuse it forever. (Dusk came from
  two lucky good runs; codifying it made every later project start good.)
- Mine great open-source projects for TECHNIQUE NAMES, not code: "fog color =
  horizon color", "vertex AO", "aerial perspective", "trade resolution never
  features". A named technique in a story is an idea the model can execute;
  pasted code is provenance contamination.

## Copy is design too

Menus, HUD labels, results screens: plain verbs, sentence-consistent register,
no lorem, no "Submit". The bible should include the game's voice ("SUNSET
GRAND PRIX — LAP 3 OF THE GOLDEN HOUR" is a vibe decision, written down).
