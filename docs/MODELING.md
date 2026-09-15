# MODELING.md — how to make game assets via Blender MCP (teaching file)

This is the manager-authored reference for the "blind attempt → compare →
teach" loop: the local model attempts an asset cold, the manager compares
against THIS file, and the gap gets encoded here permanently. The model
drives Blender through blender-mcp's `execute_blender_code`; everything
below is written to be executable by a 27B through that pipe.

## The method (any asset, always in this order)

1. **Name the real-world dimensions first.** Write them as constants at the
   top of your script (a car is ~4.5m long, ~1.8m wide, ~1.4m tall; a crate
   is 1m). "Looks about right" is how you get a car the size of a house.
   Godot imports GLB at 1 unit = 1 meter, +Y up, -Z forward.
2. **Block the silhouette with primitives, biggest shapes first.** Body,
   then cabin, then wheels. A recognizable low-poly asset is 5–15 boxes and
   cylinders with correct PROPORTIONS, not 200 badly-placed vertices.
3. **Bevel everything man-made.** `bevel` modifier (width ~0.02–0.05m,
   2 segments) is the single biggest cheap quality multiplier. Flat-shaded
   hard edges read as "unfinished"; beveled edges catch light.
4. **Wheels/details are SEPARATE objects** parented to the body — never one
   fused blob. Games need them (wheel spin, damage states), and separate
   objects are easier to place correctly than fused geometry.
5. **Materials: 2–4 flat colors, no textures.** `use_nodes`, Principled BSDF,
   base color + roughness ~0.6–0.9. Assign per-face via material slots.
   Palette discipline: one body color, one dark (trim/glass), one accent.
6. **Verify after EVERY stage** (see the checklist below) — never write 200
   lines blind and export.
7. **Export GLB**: `bpy.ops.export_scene.gltf(filepath=..., export_format='GLB',
   export_apply=True)` — `export_apply=True` applies modifiers so Godot sees
   the bevels. Then RE-OPEN the GLB (or parse it in Godot) and confirm:
   object names, tri count, bounding box size. An unverified export is slop.

## The verification habit (what separates a model from a guesser)

After each build stage, query the scene and CHECK the numbers:
- `obj.dimensions` against your constants (a 4.5m car, not 45 or 0.45)
- `obj.location` of wheels: all four z equal, x/y symmetric (±)
- total poly count: low-poly target 500–5,000 tris; over 20k for a prop
  means you forgot to keep it simple
- material slots actually assigned (not just created)
Print these. Read them. Fix before moving on. This is the same law as the
game loop: verify is not optional, and you grade nothing yourself — the
numbers grade it.

## Worked example: the car (the manager's reference version)

Stage order and bpy idioms that work through blender-mcp:

```
CAR_LEN, CAR_WID, CAR_H = 4.4, 1.85, 1.35   # meters, write these first
WHEEL_R, WHEEL_W = 0.33, 0.24
```

1. **Body**: cube scaled to (CAR_LEN, CAR_WID, 0.55), z = WHEEL_R + 0.28;
   bevel 0.06. This is the floor+doors block.
2. **Cabin**: cube (2.2, 1.7, 0.5), z on top of body, pushed back ~0.3;
   bevel 0.12 (cabins are rounder than bodies). Optionally taper: scale the
   top face loop 0.85 in edit mode — one loop, don't sculpt.
3. **Wheels**: cylinder radius WHEEL_R depth WHEEL_W, rotated 90° on X to
   lie across the car; 4 copies at (±1.35, ±0.82, WHEEL_R). Check: wheel z
   == WHEEL_R means they touch the ground exactly.
4. **Details (greebles)**: headlights = 2 small cubes, amber; dark window
   band = a thin scaled cube inset around the cabin. 2–4 details max.
5. **Materials**: body `#8a1f2d`-ish solid, windows near-black gloss
   (roughness 0.2), tires near-black matte, lights amber emissive-ish
   (emission_strength 0.5 is enough).
6. **Join policy**: body+cabin+details join as `CarBody`; wheels stay
   separate as `Wheel_FL/FR/RL/RR` parented to CarBody.
7. Export + verify per the method above.

A manager-made reference render of this car lives at (path TBD by the
session that builds it) — compare attempts against it, not against memory.

## Failure modes already observed (grow this list)

- **Skipping measurement**: assets at wrong scale (10x house-cars).
  Fix: the constants-first habit, and the bounding-box check at export.
- **Sculpting instead of blocking**: hundreds of edit-mode ops that leave
  broken normals. Fix: primitives + bevel + at most one taper loop.
- **Texture ambition**: local models try UV unwrapping and fail silently.
  Fix: flat-color materials only; texture work is a human/staged-asset job.
- **Export without re-open**: GLB written but corrupt/empty/wrong-axis.
  Fix: the re-open verify step is law.
- **Material slots ≠ material colors (observed 2026-08-19, Qwen crate):**
  the lid rendered bright white though a dark material was "assigned" —
  slots existed but faces/base colors were wrong. Fix: the verify stage
  includes a RENDER (workbench/eevee PNG) and the rule "look at the render;
  the palette must match the spec" — slot names prove nothing.
- **Accent colors that can't be seen**: amber material existed but was on
  bolt heads invisible from any normal view. Fix: every accent must be
  visible in the default 3/4 turntable view; if not, move it.
- **Proportions drift under spec**: crate spec said 1m cube; result was
  1.0×1.0×0.79 (squat). Fix: bbox assert covers ALL THREE axes against the
  constants, not just footprint.
- **What it got RIGHT (absorb into reference):** corner brackets + a front
  latch beat plain side panels as greebles; 8-step inspect→build→join→
  export→verify sequencing; self-checking export with os.path.exists.

## Feed results back

Every blind attempt teaches this file: what the model got right stays
silent; what it got wrong becomes a numbered entry above. The file is the
teacher — sessions change, it doesn't.

## Rule zero: steal first, build second

The #1 quality law from ASSETS.md applies to Blender work too: humans have
already made better assets than any local model will sculpt, and they are
free (CC0). Building from scratch is for (a) learning, (b) tiny props no
pack covers, (c) fixing/extending a stolen asset. Everything else: steal.

**The steal-and-adapt pipeline via Blender MCP:**

1. **Acquire**: pull a CC0 asset from the sources in ASSETS.md (Kenney,
   Quaternius, Poly Pizza, KayKit). Prefer GLB/GLTF — FBX imports fine,
   OBJ loses materials. `curl -L` the zip, `unzip -l` FIRST to see real
   filenames (FAILURES #25), then unpack.
2. **Import**: `bpy.ops.import_scene.gltf(filepath=...)` — then immediately
   verify: object count, dimensions vs. your target size, material count.
3. **Normalize scale**: stolen assets are routinely 100x or 0.01x. Measure
   `obj.dimensions`, compute the scale factor to hit your target size,
   `obj.scale = (f, f, f)`, then `bpy.ops.object.transform_apply(scale=True)`
   — unapplied scale breaks Godot physics and bevel widths later.
4. **Adapt, don't rebuild**: recolor via material slot base colors, decimate
   if over budget (`modifier_decimate`, ratio to hit <5k tris for props),
   delete what you don't need, join what's static. Small, surgical ops.
5. **Re-export GLB + re-open verify** — same law as scratch builds.

**Decision rule:** if ASSETS.md has a category for the thing, steal it.
If the model starts sculpting something Kenney already made, that's a
process failure — log it below.

## Worked example: the house (steal + adapt, not sculpt)

A house from primitives is 30+ ops and still looks like a shoebox. A stolen
Kenney/KayKit building is 6 ops and looks like a game:

1. Fetch (example): Kenney "City Kit" or KayKit "Builder Pack" building GLB.
2. Import, measure: a cottage is ~8×8×6m. If it imports at 0.08m (common
   with FBX→GLB chains), scale ×100, apply.
3. Adapt: shift materials toward the project palette (DUSK-STYLE law:
   pull hue/sat toward the brief, don't invent new ones); kill interior
   objects you won't see; add ONE project-consistent accent (door glow).
4. Verify: footprint fits its plot in the game world; door faces -Z or +Z
   consistently with your other buildings (pick one, note it in the brief);
   tris < 20k for a background building.
5. Export GLB named for its ROLE (`house_cottage_a.glb`), not its source
   filename — the game brief references roles.

## Scratch-build quick reference (when the pack truly lacks it)

Same method as the car — constants first, primitives, bevel, 2–4 flat
materials, separate moving parts, verify per stage. Targets:

| Asset | Real size | Tri budget | Scratch-buildable? |
|---|---|---|---|
| Crate/barrel/props | 0.5–1m | <1k | YES — 5 ops |
| Vehicle | 4–5m long | 1–5k | YES — the worked example above |
| Rock/tree/nature | 1–10m | <2k | Borderline — icosphere + 2 noise displaces max; prefer stealing |
| House/building | 6–15m | <20k | NO — steal + adapt (above) |
| Character | 1.8m | 5–15k + rig | NO — steal (rigging is beyond loop scope) |
| Weapon/tool prop | 0.3–1m | <1k | YES — primitives read well at this size |
