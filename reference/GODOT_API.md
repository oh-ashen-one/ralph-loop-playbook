# GODOT_API.md — grounding cheat-sheet (inject into every Godot prompt)

The ~50 API facts this project's code actually uses, with the traps spelled
correctly. A local model's training priors lose to in-context evidence —
this file IS the in-context evidence (FAILURES #55). Grow it per project;
keep it under ~100 lines. Godot 4.7.

## Properties with trap names
- Node3D has NO rotation_y/rotation_x/rotation_z properties — use `rotation.y`; the METHOD rotate_y() exists
- OmniLight3D energy: `light_energy` — there is NO `.energy` (also SpotLight3D)
- MeshInstance3D has NO `.material` property — use `set_surface_override_material(0, mat)`
  or assign to `mesh.material` (reads back via get_surface_override_material(0))
- Light3D range: OmniLight3D `omni_range`, SpotLight3D `spot_range`
- Fog: `fog_density`, `fog_light_color` on Environment
- GPUParticles3D: `emitting`, `one_shot`, `explosiveness`, `amount`,
  `lifetime`, `process_material`; restart with `.restart()` then `emitting=true`
- StandardMaterial3D emission: `emission_enabled`, `emission`, `emission_energy_multiplier`
- Timer: `wait_time`, `one_shot`, `.timeout` signal — node must exist in the scene
- AudioStreamPlayer: `.playing`, `pitch_scale`, `volume_db`, `.stream`
- ColorRect alpha: `color.a`

## Syntax that is NOT GDScript
- `atan2f()` does not exist — `atan2(y, x)` plain
- Godot 3->4 renames: `Basis.xform_inv(v)` is gone — `basis.inverse() * v` (or `v * basis`); Pool*Array -> Packed*Array; instance() -> instantiate()
- Infinity is `INF` / `-INF` — `Infinity` does not exist (Python/JS prior)
- NO brace accessors: `var x { set(v): ... }` is invalid. Use:
  `var x: T = d:\n\tset(value):\n\t\tx = value` (colon + indent, and
  self-assignment inside the setter is direct field access, no recursion)
- NO `has_property()` — use `"prop_name" in object` or get_property_list()
- `var x := value` requires the value's type to be inferrable — when in
  doubt use explicit `var x: Type = value`

## GUT 9.x — only these asserts exist
- assert_eq, assert_ne, assert_true, assert_false, assert_null,
  assert_not_null, assert_gt, assert_lt, assert_almost_eq(got, exp, eps),
  assert_signal_emitted, fail_test("msg"), is_instance_valid(obj)
- DO NOT EXIST: assert_le, assert_ge, assert_that, assert_approx, fail(),
  is_valid()
- GUT exits 0 even with failing tests and SKIPS test files that don't
  parse — never trust the exit code; grep output (harness does this)
- SceneTree.paused is global: any test booting a scene that pauses must
  reset `get_tree().paused = false` in after_each (FAILURES #53)
- In GUT the booted main scene is NOT at /root/Main — use find_child or
  relative paths from the node under test

## RandomNumberGenerator — the ONLY methods
- `randf()`, `randf_range(a,b)`, `randi()`, `randi_range(a,b)`, `randfn(mean,dev)`
- NO randf_vec3 / random_unit_vector / randv — for a random direction use
  Vector3(randfn(0,1), randfn(0,1), randfn(0,1)).normalized()

## Physics / scene-tree
- Never call `_physics_process()` manually on CharacterBody3D —
  move_and_slide uses the ENGINE delta, not your argument. Tests drive the
  engine: `await get_tree().physics_frame`
- Timers that must fire while paused: `create_timer(t, true, false, true)`
  (ignore_time_scale=true)
- `Engine.time_scale` affects physics; restore to 1.0 in every test path
- class_name is required for `SomeType` references in OTHER files
  (tests referencing `Ship.MAX_SPEED` need `class_name Ship` in ship.gd)
- After adding a class_name, run `godot --headless --import` before tests —
  the global class cache is stale otherwise
- .tscn ext_resource tags REQUIRE an id: `[ext_resource type="Script" path="..." id="1_x"]`
- @onready vars are null before the node enters the tree — don't touch them
  in _init or from outside before add_child
- **Re-emitting a .tscn must preserve `instance=ExtResource(...)` and `type=`
  on every node line.** `[node name="Ship" parent="." instance=ExtResource("2")]`
  rewritten as `[node name="Ship" parent="." index="0"]` is not "the same node
  with an index hint" — with no `instance=` and no `type=` it is an *override
  of a child that does not exist*. Godot loads the scene, prints
  `Node './Ship' was modified from inside an instance, but it has vanished`
  per node, and every `$Ship` / `$HUD` / `$GameMenu` resolves to null; the
  first signal connect in `_ready()` dies with
  `Invalid access to property or key '<signal>' on a base object of type
  'null instance'`. The `[ext_resource]` header block can be completely intact
  while this happens — a clean header is not evidence the scene is wired.
  `index="..."` on a child of the root node is the tell.
- `set_deferred("monitoring", true)` lands at FRAME END: a same-frame
  `get_overlapping_areas()` errors ("Can't find overlapping areas when
  monitoring is off") and GUT under -d counts it as a test failure. Guard the
  query: `if area.monitoring:` — the overlap registers next physics frame.
- RectangleShape2D in Godot 4 uses `size`, NOT `extents` (Godot 3). `extents`
  in a .tscn parses but leaves the shape at default size — hits silently whiff.
- An Area2D only sees areas whose collision_layer intersects its
  collision_mask. A projectile that must hit Hurtboxes on layer 1 needs
  `collision_mask = 1` — a fancy mask (16) against default-layer hurtboxes
  overlaps NOTHING, with no error to tell you.
- `create_timer(t, true, true)` — the THIRD arg is process_in_physics, NOT
  ignore_time_scale (that's the FOURTH). A "restore time_scale after slow-mo"
  timer with the wrong arg runs AT the slowed scale and never restores on
  schedule. Slow-mo restore timers are always `create_timer(t, true, false, true)`.
- Every `[node]` in a .tscn except the root MUST carry `parent="..."` — a
  parentless node line makes the whole scene fail instantiate() with
  "node does not specify its parent node" (load() still succeeds; only
  instantiate returns null).
- Theme overrides in .tscn are PROPERTIES (`theme_override_fonts/font = ...`),
  never method calls (`add_theme_font_override(...)`) — a method call as a
  property line silently aborts that node's remaining properties.
- `get_node_or_null(&"Name")` is a Parse Error — the argument is a NodePath,
  and a StringName literal (&"...") does not coerce. Plain string:
  `get_node_or_null("Name")`. (Recurring 27B prior: two projects, three ruts.)
- `signal.connect(method.bind(x))` appends x LAST: health_changed(h) into
  set_health(side, h) via .bind(side) calls set_health(h, side) — args
  swapped, no error. When arg order matters, connect a typed lambda.
- `RandomNumberGenerator()` is NOT a constructor call in GDScript — it is
  `RandomNumberGenerator.new()`. Same for every RefCounted built-in
  (Image, SpriteFrames, Tween handles). A bare `Type()` is a parse error.
- A .tscn node's authored properties ARE its defaults at instantiate() time.
  Code that assigns them every frame (camera zoom, modulate) still leaves a
  freshly-instanced scene at engine defaults until the first physics tick —
  tests that read state right after `instantiate()` will see 1.0, not your
  intended value. Author the value in the scene AND drive it in code.
