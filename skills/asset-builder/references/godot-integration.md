# Godot integration — what "game-ready" means per asset type

A source asset becomes a game asset when the engine can use it the way the gameplay needs.
This file is the checklist per type: what `INTEGRATED` requires before `asset-review` will
even look at it. Only add what the spec says the gameplay requires; the list is the maximum,
the spec is the filter. API detail (node properties, shader syntax, import options) belongs to
the specialist Godot packs the router delegates to — check against the project's version.

## Every asset

- Lives where the Art Bible's *Naming & files* says; source files in an ignored folder
  (`art/source/` with `.gdignore`), outputs under `res://assets/<category>/`.
- Imported headless after being added or changed: `godot --headless --path . --import`.
  Import settings changed in the editor's Import dock (or by editing the generated `.import`
  file's documented keys — never hand-authoring one from scratch).
- Named per the convention; file, root node, and registry `name` agree.
- Has a **test scene** for its family (`res://tests/scenes/props_test.tscn` or similar) where
  it can be seen next to the scale reference under the bible's lighting recipe. One per
  family, not per asset.
- Registry `file … --kind godot` recorded for its scene and resources; `set INTEGRATED` with
  a note saying what was wired.

## Static mesh (decorative prop, architecture piece, kit piece)

- glTF in metres, Y-up, faces -Z; root transform identity, scale 1 on every node
  (`asset-review`'s `inspect-gltf.py` checks this).
- Pivot: centre-bottom for props; grid corner for kit pieces (the bible says which).
- Triangle count within the category budget; normals present and outward; one UV set (a
  second for lightmaps only if baking).
- Materials mapped to the master material `.tres`, not the glTF's embedded one — set in the
  Import dock's material remap, or by the scene wrapper overriding `material_override` /
  surface materials.
- Collision: `-col` (trimesh, static only) or `-convcol` (convex) suffix on the node in the
  source, or a `CollisionShape3D` added by the wrapper. A kit piece that players never touch
  may need none — say so in the spec.
- Kit pieces: snap on the grid at origin; test by assembling a 2×2 room in the test scene.

## Physics / interactive prop (carried, thrown, breakable)

Everything above, plus:

- Scene wrapper: `RigidBody3D` root (mass from spec; physics material for bounce/friction),
  `MeshInstance3D`, `CollisionShape3D` with a **convex** or primitive shape (trimesh
  collision does not work on moving rigid bodies).
- The interaction component the plan names (`CMP_GRABBABLE` or the project's equivalent) as a
  child, with its exported properties set from the spec.
- Multiplayer: `MultiplayerSynchronizer` on transform (and sleeping state) with the authority
  rule the spec states; freeze/unfreeze on grab handled by the component, not the asset.
- Breakable: the swap target (`variants` → the broken entry) referenced by the component;
  impulse threshold from the spec.
- Sound/VFX attachment: a `Marker3D` where the impact effect and audio spawn, if the spec
  asks for them.

## Character (player, NPC)

- Skinned glTF with the shared rig family (`RIG_*` entry); bone names match the family so
  animations are shared; scale 1; root at the feet (pivot at floor).
- Scene wrapper: `CharacterBody3D` root, `CollisionShape3D` capsule matching the bible's
  player dimensions, the imported model as a child (`-noimp` on any helper meshes),
  `AnimationPlayer` (from the import) feeding an `AnimationTree` with the state machine the
  spec lists (idle/walk/run/carry/throw/…); `Skeleton3D` with `BoneAttachment3D` markers for
  hands, head, camera, and any accessory sockets the customisation decision needs.
- Procedural motion nodes where the spec says (look-at, foot IK) — version-appropriate
  (`SkeletonModifier3D` family in 4.3+, `SkeletonIK3D` earlier).
- Ragdoll: `PhysicalBone3D` set generated from the skeleton, if the bible's motion section
  uses it.
- Hurtbox `Area3D` on the relevant bones if combat exists; camera mount `Marker3D` at the
  bible's eye height for first-person.
- Material remap to the character master material; player-distinction hook (palette
  parameter or accessory socket) wired.

## Creature / enemy

As character, plus: the state list from the spec drives the `AnimationTree` state machine;
`NavigationAgent3D` with radius/height from the collision shape; hitbox `Area3D`s on attack
bones with timing that matches the animation windup the readability rule promised;
attachment `Marker3D`s for VFX (eyes, mouth, wounds) and audio; the death treatment (dissolve
shader material / ragdoll / animation) wired to the component that owns death. The visual
state indicators the bible promises (emission on alert, colour on enrage) are material
parameters the state machine sets, not separate meshes.

## Material / shader

- Master material `.tres` in `res://assets/materials/`, parameters exposed and named in the
  bible; every mesh that should use it does, and no mesh carries a duplicate.
- Shader `.gdshader` in `res://assets/shaders/`, one `ShaderMaterial` per distinct use,
  uniforms documented at the top of the file; cost checked against the bible's ceiling (the
  reviewer will look at texture reads and branching).
- Screen-space effects live on the camera or a `CanvasLayer` with a `ColorRect`, toggleable
  by a settings flag the bible's accessibility rule requires.

## VFX

- A scene per effect (`res://assets/vfx/hit_spark.tscn`): `GPUParticles3D` (or 2D) with the
  process material, optional `OmniLight3D` with an energy curve, optional `Decal` spawn;
  `one_shot` where appropriate; a script or the pooling component that frees or returns it
  on `finished`. Particle count and lifetime within the effect class budget.
- Parameterised by surface/material where the plan's VFX library says so (one spark effect,
  a colour and count per surface), not one scene per surface.

## Animation

- Clips in an `AnimationLibrary` shared across the rig family; names per the bible's
  convention; loop flags correct; root motion only where the spec chose it.
- Added to the `AnimationTree` of every character that uses them; transitions wired;
  hitbox/VFX/audio `Marker3D` call tracks where timing matters.

## 2D (sprites, tiles, pixel art)

- Import filter `Nearest` for pixel art; mipmaps off; textures at the decided internal
  resolution; `SpriteFrames` for animated sprites; `TileSet` with physics and navigation
  layers set for tiles; pixel-snap project settings on if the bible says pixel-perfect.
- Collision shapes on characters are rectangles/capsules from the bible's player metrics,
  not from the sprite's bounds.

## UI

- A `Theme` resource in `res://assets/ui/theme.tres` owning fonts, colours, and
  `StyleBoxTexture` 9-slices; scenes use theme types, not per-node overrides.
- Minimum text size and contrast per the bible's UI section; a test scene at the smallest
  target resolution.

## What a reviewer will reject on sight

Scale ≠ 1 on any node; pivot floating; trimesh collision on a rigid body; embedded glTF
material instead of the master; a `.tscn` hand-written with invented uids; no test scene;
`INTEGRATED` set with the engine never having imported the file; a "done" with no
`godot-verify` run.
