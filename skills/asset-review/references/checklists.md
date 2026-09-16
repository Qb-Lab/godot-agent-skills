# Review checklists by asset kind

Run the one that matches the entry's `type` and status. Each line is checkable; each has an
evidence tier it can be checked at. Rank findings by threat to the game, not by list order.

## Concept / reference (status CONCEPT)

- Serves the gameplay role in the spec — a player could read what it *does* from the image
- Obeys the bible: style family, shape language, proportion rule, palette strategy
- Silhouette distinct from the player and from every other approved creature/prop in its family
  (put the approved concepts side by side)
- Readable when shrunk to gameplay size (view at 25% — does it still read?)
- 2–3 real alternatives were explored, not one image and two crops
- Generation metadata recorded (tool, model, prompt, seed, references) if generated
- **Human call:** mood, appeal, humour, fear — prepare the packet, do not decide

## Blockout (status BLOCKOUT)

- At real scale against the scene's scale reference; bible measurements respected
- Collision present and simple; no gaps a player falls through, no invisible blockers
- Function colour code applied (walkable / blocker / interactive / hazard / trigger / scale)
- Physics bodies where gameplay needs them, with spec masses
- Nav bakes and reaches; camera does not clip; interactive items reachable
- Multiplayer: authority and replication of moving pieces match the spec
- The walk-through checklist was actually run in the game by the user — it is the approval;
  a screenshot is not

## 3D static mesh (status PRODUCTION → INTEGRATED)

- `inspect-gltf.py`: every node scale = 1, root rotation identity; metres (bbox plausible);
  pivot per convention (`min.y ≈ 0` for floor-standing props; grid corner for kit pieces)
- Triangle count ≤ category budget; no absurd density on parts never seen up close
- Normals present, outward (no inside-out faces in the test scene); hard/soft edges per style
- One UV set, no stretching visible on the test-scene lighting; UV2 only if lightmapped
- Materials remapped to the master material; no duplicate material resources created
- Textures: bible sizes, power-of-two where the import expects it, palette compliance for
  stylised looks
- Collision: `-col` for static architecture, `-convcol`/primitive for anything that moves;
  fits the silhouette; no collision on purely decorative pieces the spec excludes
- Kit pieces snap: assemble a 2×2 test room; seams and Z-fighting at joins
- Import settings applied (`.import` present and re-imported headless)
- File and node names per convention; source file recorded; test scene contains it

## Physics / interactive prop (status INTEGRATED)

- Static-mesh list, plus: `RigidBody3D` root, convex/primitive collision, spec mass and
  physics material, interaction component present with spec values
- `MultiplayerSynchronizer` on transform (and sleep) with the spec's authority — if multiplayer
- Breakable: variant referenced, threshold set; the swap does not spawn inside a wall
- Impact VFX/audio marker if specced
- Behaviour: pick up, carry, drop, throw in the test scene — no tunnelling, no jitter at rest
  (user-run; record "confirmed by user" or "unverified")

## Character / creature (status INTEGRATED)

- Skinned to the shared rig family; bone names match; scale 1; pivot at feet
- Proportions and silhouette per bible and spec; reads at gameplay distance against the
  environment palette
- `CharacterBody3D` with the bible's capsule; camera/hand/head `Marker3D`/`BoneAttachment3D`
- `AnimationTree` has every state the spec lists; transitions exist; no missing-track warnings
  on load; loop flags right
- Attack windups are visible for the promised duration (readability rule); hitbox timing
  matches
- Death treatment wired (dissolve / ragdoll / clip); ragdoll does not explode on spawn
- Navigation agent radius/height match the collision; state indicators are material
  parameters the state machine drives
- Player distinction hook works (palette param / accessory socket) — multiplayer
- **Human call:** appeal, scariness, humour — packet with turntable shots at gameplay distance

## Material / shader

- Master material exposes the bible's parameters and nothing else; naming per convention
- Every intended mesh uses it; no embedded glTF materials left in the scene
- Shader: uniforms documented; texture reads and branches within the bible's cost ceiling;
  behaves under the project's renderer (Forward+/Mobile/Compatibility) — say which was tested
- Screen effects toggleable via the accessibility setting the bible requires
- Looks right under the bible's lighting recipe in the test scene (screenshot from user)

## VFX

- Particle count, lifetime, and overdraw within the effect class budget
- One-shot effects free or pool themselves; looping effects have an owner that stops them
- Parameterised by surface where the library says, not duplicated per surface
- Reads at gameplay distance; does not obscure gameplay-critical information (an impact
  cloud hiding an enemy attack windup is a design failure, not a polish note)
- Light energy curve does not blow out the scene; decals do not z-fight

## Animation

- Clips in the shared library with convention names; loop flags right; root motion only
  where chosen
- Wired into every user of the rig family; transitions blend without pops
- Timing matches hitboxes, VFX, and audio call tracks
- Frame-rate independence (an `AnimationTree` driven by `delta`, not by frame count)

## 2D / pixel art

- Palette compliance (count the colours; compare to the bible palette)
- Pixel grid consistent — no mixed pixel sizes, no rotation-blur; filter `Nearest`, mipmaps off
- Sprite size per the decided internal resolution; collision from bible metrics, not bounds
- `SpriteFrames` complete for every state; `TileSet` physics and nav layers set

## UI

- Uses the `Theme`, not per-node overrides; 9-slices scale without distortion
- Minimum text size and contrast met at the smallest target resolution
- Icon language consistent; HUD information budget respected (nothing on screen the bible
  did not allow always-on)

## Godot integration (any INTEGRATED asset)

- Root node type matches the gameplay (Static/Rigid/Character/Area, or plain Node3D for
  decoration) — the wrong body type is blocking
- Scene structure per the wrapper convention; no orphan `.tscn` with invented uids; no
  structural hand edits in the diff (`godot-scene-surgery`)
- `godot --headless --import` + `--quit` clean; no `SCRIPT ERROR` / `Parse Error` /
  `Failed to load` in the output
- Registry: files recorded (source, output, godot), `godot.scene` set, dependencies listed and
  themselves INTEGRATED or better, decisions cited
- Placed in the right folder; source not imported (`.gdignore` present)
- Test scene exists and includes the asset next to the scale reference

## Batch table shape

```markdown
| ID | Verdict | One line |
|---|---|---|
| KIT_MANSION_WALL_01 | pass | grid-snaps, 180 tris, trim UVs clean |
| KIT_MANSION_DOORWAY_01 | REWORK | opening 0.8 m vs bible 0.9 m — player clips |
```
