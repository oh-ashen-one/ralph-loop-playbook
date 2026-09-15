# Assets — where to steal, how to convert, engine-agnostic

The #1 slop tell in AI-built games is programmer art. Never let the model
invent meshes when humans already made better ones for free. Curate assets in
the MANAGER lane; the model only consumes staged files (read-only dir,
write-fenced in the harness).

This file is a map, not a bundle: links + acquisition paths, nothing vendored.
Every entry names how a script fetches it — a loop must be able to pull
programmatically; if it can't, the manager stages it once by hand.

## Godot starter kits & addons

All MIT, all `git clone`. A starter kit is 20 stories you don't have to run.

| Repo | What | ★ |
|---|---|---|
| `godotengine/godot-demo-projects` | Official demos, every subsystem | 9.4k |
| `Whimfoome/godot-4.x-fps-starter` | FPS controller starter | 1k |
| `gdquest-demos/godot-4-3d-third-person-controller` | 3PS controller | 1k |
| `Maaack/Godot-Game-Template` | Menus/options/save scaffolding | 1.6k |
| `nathanhoad/godot_dialogue_manager` | Dialogue runtime + editor | 3.8k |
| `dialogic` | Visual-novel-grade dialogue | 5.9k |
| `ExpressoBits/inventory-system` | Inventory + crafting | 726 |
| `peter-kish/gloot` | Diablo-style grid inventory | 960 |
| `ramokz/phantom-camera` | Camera rigs/blends | 3.5k |
| `bitbrain/beehave` | Behavior trees | 3.2k |
| `limbonaut/limboai` | Behavior trees + state machines | 3k |
| `TokisanGames/Terrain3D` | Heightmap terrain | 4.2k |
| `Zylann/godot_voxel` | Voxel terrain | 3.8k |
| `gaea-godot/gaea` | Node-based procgen | 1.6k |
| `HungryProton/scatter` | Prop scattering | 3k |
| `blackears/cyclopsLevelBuilder` | In-editor CSG level blockout | 1.6k |

Anything not on GitHub: the Godot Asset Library has a JSON API —
`https://godotengine.org/asset-library/api/asset?filter=<query>`.

## Models

| Source | What | License | How to grab |
|---|---|---|---|
| **Kenney.nl** | Low-poly kits: nature, furniture, food, survival, city, town + UI/impact/jingle AUDIO packs | CC0, all packs | Direct zips, scriptable — recipe below. Kits ship `Models/GLB format/*.glb` ready to use. Mirror: `ETdoFresh/kenney.nl` on GitHub |
| **KayKit** (`github.com/KayKit-Game-Assets/*`) | Dungeon, city-builder, restaurant packs; animated characters with ~75 baked animations | CC0 | Plain `git clone`, GLTF/FBX inside |
| **Quaternius** | 60+ packs: animated animals/fish, nature, buildings, UniversalAnimationLibrary (250+ anims) + retarget-ready base characters | CC0 | poly.pizza mirrors, or `gdown` on the Drive links. GitHub staging mirror: `weftspun/quaternius-stage` — `git clone --filter=blob:none --sparse` + `git sparse-checkout set models/<Pack>`; files are **.usda**, convert via headless Blender (recipe below) |
| **poly.pizza** | Searchable index of individual CC0 models (incl. all of Quaternius/Google Poly) | CC0 | API v1.1: free key, `X-Auth-Token` header, per-model `license` field — assert it before download |
| **Poly Haven** | Textures, HDRI skies, some models | CC0 | Keyless public API (`api.polyhaven.com`) |
| `pmndrs/market-assets` | Curated web-ready GLB props | CC0 | `git clone` |
| **Sketchfab** (CC-filtered search) | Anything specific (the video-famous "CC bear") | CC0/CC-BY | ⚠️ OAuth dance for the download API; blender-mcp `search_sketchfab_models`/`download_sketchfab_model` handles it. Decimate; CC-BY → ATTRIBUTION.md |
| **OpenGameArt** | Long tail of 2D/3D/audio | ⚠️ mixed (CC0→GPL) | Direct zips; check the license field per asset, never the site average |
| **AI mesh gen** (Higgs `generate_3d`, Meshy) | Hero characters nothing else has | your credits | concept image → mesh; see character pipeline below. Meshy API is paid-only — Higgs generate_3d or Meshy web free tier instead |

## Textures & HDRI

| Source | What | License | How to grab |
|---|---|---|---|
| **ambientCG** | PBR texture sets | CC0 | Verified zip pattern: `https://ambientcg.com/get?file={ID}_{res}-{fmt}.zip` (e.g. `Bricks059_1K-JPG.zip`) |
| **Poly Haven** | PBR textures + HDRI | CC0 | Keyless API, resolution/format in the URL |
| `RodZill4/material-maker` | Procedural material authoring | MIT (5.8k★) | `git clone`; runs headless — generate textures in a verify step |

## Audio

| Source | What | License | How to grab |
|---|---|---|---|
| **Kenney audio** | `interface-sounds`, `ui-audio`, `music-jingles`, `impact-sounds` | CC0 | Same zip-scrape recipe as the kits |
| **Freesound** | Everything else | ⚠️ mixed | API with `filter license:"Creative Commons 0"` — NC licenses creep in by default, exclude them explicitly |
| **jsfxr** | Retro SFX synthesizer | Unlicense | `git clone`; procedural — infinite variations, no file hunting |
| **BBC Sound Effects** | 33k real-world recordings | ⚠️ RemArc | Research/personal use only — NO shipping in a product. Reference/fit-check only |
| **Sonniss GDC packs** | Film-grade SFX | ⚠️ | No raw redistribution — fine in a shipped mix, never commit the wavs to a public repo |
| **zapsplat** | Broad SFX library | ⚠️ account + attribution | Manual/credentialed; manager-stage only |

## Fonts & UI

| Source | What | License | How to grab |
|---|---|---|---|
| **Kenney UI** | UI kits, icons, cursors | CC0 | Zip-scrape recipe |
| **game-icons.net** | 4k+ SVG game icons | CC-BY | `git clone game-icons/icons`; attribution line per icon set |
| **google/fonts** | Every Google font | OFL | `git clone --depth 1`, fonts ship in products freely |

## Animation

| Source | What | License | How to grab |
|---|---|---|---|
| **Quaternius UniversalAnimationLibrary** | 250+ humanoid anims, retarget-ready | CC0 | As above (poly.pizza / gdown / staging mirror) |
| **KayKit baked animations** | Character packs ship ~75 anims each | CC0 | `git clone` |
| **Mixamo** | Huge mocap library | ⚠️ free w/ Adobe login | No API, no redistribution of raw files — manual download, manager lane only; usually unnecessary with UAL |
| **CMU mocap** | 2500+ academic mocap clips | free | Direct zips; document provenance in ATTRIBUTION.md |
| **LaFAN1** | High-quality locomotion mocap | ⚠️ CC-BY-NC-ND | Research only — never ships |

## Complete games / reskin bases

| Source | What | License | How to grab |
|---|---|---|---|
| `godotengine/tps-demo` | Full third-person shooter | MIT code, ⚠️ mixed art | `git clone`; read the code, re-steal the art from CC0 sources above |
| `gdquest-demos/godot-open-rpg` | Full JRPG loop (dialogue/quests/combat) | MIT | `git clone` |
| `awesome-godot` (10.5k★) / `awesome-unity` (7.1k★) | The indexes, when this file isn't enough | — | `git clone`, then check each entry's license yourself |

## Bulk & audit tooling

- `itchio/butler` — CLI for itch.io; batch-download purchased/free bundles.
- `donmccurdy/glTF-Transform` (MIT, 1.9k★) — CLI inspect/resize/prune/quantize
  GLBs; the normalization pass after any download.
- `FBX2glTF` — batch FBX→GLB for packs that ship FBX only.
- License audit before ship: `licensee` / `scancode` / `reuse lint` over the
  staged asset tree. Keep an `ATTRIBUTION.md` per project; write entries at
  download time, not ship time.

## Recipe: Kenney direct download (no browser)

The download URL is embedded in each asset page with a content hash:

```bash
pack=nature-kit
url=$(curl -sL "https://kenney.nl/assets/$pack" \
  | grep -oE "/media/pages/assets/$pack/[^']*kenney_[^']*\.zip" | head -1)
curl -sL "https://kenney.nl$url" -o "$pack.zip"
```

Audio packs (`interface-sounds`, `ui-audio`, `music-jingles`, `impact-sounds`)
use the same scheme.

## Recipe: Quaternius USDA → GLB (headless Blender)

```python
# blender --background --python convert.py -- <out_dir> <files...>
import bpy, sys
from pathlib import Path
argv = sys.argv[sys.argv.index("--")+1:]
out = Path(argv[0]); out.mkdir(parents=True, exist_ok=True)
for src in argv[1:]:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.wm.usd_import(filepath=src)
    bpy.ops.export_scene.gltf(filepath=str(out/(Path(src).stem+".glb")), export_format="GLB")
```

Gotcha: call this from **bash**, not zsh — an unquoted file list in zsh doesn't
word-split and Blender receives one garbage path.

## The character pipeline (AI-gen heroes without slop)

1. Concept image first (image model): "chibi {species}, full-body T-pose front,
   2-head proportions, rounded toy shapes, flat pastel colors {your bible
   hexes}, white background, no outline". Palette-locked concepts keep every
   character in one art style.
2. Image → 3D (Higgs `generate_3d` / Meshy). Budget-gate it: generate ONE
   character, get it in-engine, human-approve, only then batch the rest.
3. Scripted Blender finish pass: decimate ≤8k tris, quantize texture to the
   color bible (+10% saturation so characters pop), retarget a CC0 rig +
   animation library (Quaternius UniversalBaseCharacters), rename clips to the
   exact names your NPC code expects, export GLB.
4. Realism kills it: AI meshes look best decimated and flat-shaded. "Simple
   shapes + light does the rest."

## Manifest pattern (any engine)

Staging writes `assets/manifest.json`: `{id, path, cat, source, license}` per
prop. Game code loads by manifest, **falls back to a primitive when a file is
missing** (sims must never break on absent art), and dressing stories reference
manifest ids — so code and art lanes never block each other.

## Licensing

CC0 needs nothing. CC-BY needs a line in ATTRIBUTION.md — write it at download
time, not ship time. The ⚠️ flags above are real walls: BBC RemArc and LaFAN1
never ship, Mixamo and Sonniss never redistribute raw, Freesound defaults
include NC (filter them out), Sketchfab needs OAuth, tps-demo's art is not MIT.
Nintendo/IP assets: never; homage-original everything.

## The top 10 (if you memorize one section)

1. **Kenney** — kits + UI + audio, all CC0, scriptable zips
2. **KayKit** — animated characters, dungeon/city kits, CC0
3. **poly.pizza** — the CC0 model index with an API and per-model licenses
4. **Quaternius** — UAL animations + base characters, CC0
5. **Poly Haven** — textures/HDRI, keyless CC0 API
6. **ambientCG** — PBR textures, verified zip pattern
7. **Maaack template + godot-demo-projects** — the scaffolding stories you skip
8. **dialogue_manager / inventory-system / dialogic** — the RPG systems trio
9. **FPS/3PS controllers + phantom-camera** — movement and camera, done
10. **jsfxr + Kenney audio** — every sound a small game needs
