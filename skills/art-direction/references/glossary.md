# Glossary — art and production terms, and why each one matters to a programmer

One line each. Use these in passing when a term first becomes load-bearing in a decision;
do not read them out as a lecture. Grouped the way they come up.

## Shapes and scale

- **Silhouette** — the outline of a thing with all detail removed. Players read threats and
  roles from silhouette in a fraction of a second; if two enemies share a silhouette, no
  texture will tell them apart in play.
- **Shape language** — the deliberate use of rounded vs angular vs elongated forms to signal
  meaning (friendly / dangerous / elegant). It is the cheapest consistency tool: every asset
  obeys three rules and the game looks designed.
- **Proportions / head count** — body height measured in heads. Realistic ≈ 7.5, heroic 8,
  stylised 5–6, chibi 2–3. Decides whether faces or bodies carry emotion, and every door height.
- **Readability** — whether the player understands what they see at gameplay distance under
  gameplay lighting. The art director's primary success criterion; beauty is secondary.
- **Blockout / greybox** — placeholder geometry (boxes, capsules, planes) placed at real scale
  to validate gameplay: reach, collision, camera, navigation, sightlines, flow. Cheap to change,
  which is the point. Nothing gets pretty before its blockout works.
- **Hero asset** — a piece the player stares at (main character, primary creature, signature
  room). Gets bespoke attention and human approval; everything else is production.
- **Scale reference** — a known-size object (a 1.8 m capsule, a 0.9 × 2.1 m door) kept in every
  scene so scale errors are seen immediately.

## 3D production

- **Topology** — how the polygons of a mesh are arranged. Matters for deformation
  (animation) and for shading artefacts; irrelevant for static props beyond triangle count.
- **Retopology (retopo)** — rebuilding a dense or messy mesh (sculpt, scan, generated) with
  clean, low triangle count. This is why a generated model isn't game-ready.
- **Triangle / poly count** — the mesh's cost to render. Budgets per category stop "make it
  nicer" from being infinite.
- **LOD (level of detail)** — lower-triangle copies of a mesh swapped in at distance. Costs a
  model variant per level; skip until profiling says otherwise, except for kits and crowds.
- **Pivot / origin** — the point a mesh rotates and snaps around. Props: centre-bottom (they sit
  on floors). Kit walls: a corner on the grid (they snap). Wrong pivot = everything floats or
  misaligns, and every instance needs a manual fix.
- **Normals** — the per-vertex direction used for lighting. Flipped normals render inside-out
  (invisible faces); hard vs smooth normals decide whether an edge looks crisp or rounded.
- **UVs / UV unwrap** — the 2D layout that maps a texture onto the mesh. Bad UVs = stretched or
  seamed textures. A second UV set is used for lightmaps.
- **Baking** — precomputing something expensive into a texture: high-poly detail into a normal
  map, lighting into a lightmap, ambient occlusion into a channel. Trades flexibility for speed.
- **PBR (physically based rendering)** — the standard material model: albedo, roughness,
  metallic, normal, plus optional AO/emission. Godot's `StandardMaterial3D` is PBR.
- **Master material** — one material with exposed parameters (colour, roughness, tiling)
  instanced across many assets. Fewer textures, guaranteed consistency, trivial global changes.
- **Trim sheet** — one texture strip of reusable details (mouldings, panels, edges) that a whole
  modular kit maps onto. The standard way a small team textures architecture.
- **Atlas** — many textures packed into one, so many objects can share a material and be
  drawn together.
- **Draw call** — one instruction to the GPU to render something. Roughly: one per mesh per
  material. Hundreds are fine; thousands hurt. Kits and shared materials reduce them;
  `MultiMeshInstance3D` and GPU instancing reduce them for repeated props.
- **Modular kit** — a set of grid-snapping pieces (wall, corner, doorway, window, floor,
  ceiling, trim, stairs) that assemble any room. The single biggest production multiplier.
- **glTF / .glb** — the interchange format Godot imports best. Y-up, metres, -Z forward.
  Godot reads node-name suffixes as import hints (`-col`, `-convcol`, `-colonly`, `-rigid`,
  `-navmesh`, `-noimp`) — collision authored by naming.

## Rigging and animation

- **Rig / skeleton / armature** — the bone hierarchy that deforms a character mesh. Building
  it is rigging; per-vertex bone influence is skinning/weight painting.
- **Skeletal animation** — authored keyframes on bones. Controlled and expensive: every action
  is an asset.
- **Procedural animation** — motion computed at runtime (look-at, foot placement, breathing,
  reactive lean). Scales with systems instead of assets; looks alive with little content.
- **IK (inverse kinematics)** — solving a limb's joints so the hand or foot reaches a target.
  Feet on stairs, hands on a carried object. In Godot 4 this is `SkeletonIK3D` or, from 4.3,
  `SkeletonModifier3D`-based solvers — check the project's version.
- **Ragdoll / physical animation** — letting physics drive the skeleton, fully (death,
  comedy) or partially (hit reactions). Cheap once the rig exists; hard to make deterministic
  over the network.
- **Blend tree / `AnimationTree`** — how Godot mixes animations (walk↔run by speed, upper-body
  aim over lower-body locomotion) and sequences them (state machine).
- **Root motion** — the animation moves the character rather than code doing it. Great for
  attacks; complicates networking and navigation.
- **Secondary motion** — cloth, hair, dangling parts that react to the primary motion. Each is
  a system (`SoftBody3D`, jiggle bones, or a shader) — decide which you actually need.
- **Hitbox / hurtbox** — areas that deal or receive damage, usually `Area3D`/`Area2D` attached
  to bones. Gameplay, not visuals — but the animation must line up with them.

## 2D production

- **Sprite sheet / atlas** — frames packed into one texture; Godot uses `AtlasTexture` and
  `SpriteFrames`. Keep the grid consistent per character.
- **Pixel-perfect / pixel snapping** — rendering so every texel lands on a screen pixel.
  Requires a fixed internal resolution, nearest filtering, and integer camera movement —
  decide the internal resolution first, it is a hard rule afterwards.
- **9-slice** — a UI texture whose edges stretch cleanly (`StyleBoxTexture`). One image,
  every panel size.
- **Palette constraint** — a fixed set of colours the whole game uses. In pixel art it is the
  style; elsewhere it is the cheapest consistency rule.

## Technical art and VFX

- **Shader** — a program that decides how surfaces or screen pixels look. Water, fire, dissolve,
  outlines, wobble, damage, wind all belong here instead of in textures or animations.
- **Post-processing** — full-screen effects after the scene renders: colour grading, bloom,
  vignette, film grain, pixelation. Mood at almost no asset cost; also a performance lever.
- **Particles** — many small sprites or meshes moved by rules (`GPUParticles3D` /
  `GPUParticles2D`). Smoke, sparks, blood, dust, magic. Budget them: overdraw is the cost.
- **Decal** — a texture projected onto surfaces (`Decal` node) — bullet holes, blood, dirt.
  Cheaper than unique textures per surface.
- **VFX vs geometry** — an explosion is a particle system and a light, not a model; a crack is
  a decal or a shader, not a new mesh. Choosing wrong costs an order of magnitude.
- **Emission** — a material channel that glows without light. Readability tool for
  interactive objects and enemies' states.
- **Vertex animation** — moving vertices in the shader (grass sway, flags, jelly). Free
  motion for anything that isn't a character.

## Godot-specific

- **Import settings / `.import` file** — per-asset configuration Godot generates on import
  (compression, mipmaps, filter, scale, collision generation). Set in the editor or via the
  import dock, never hand-written; re-run `--import` headless after changing.
- **Scene wrapper** — a `.tscn` that turns a raw imported mesh into a game object: body,
  collision, script, materials, signals. The chair's `.glb` is a source; the wrapper is the
  asset the game uses.
- **`.gdignore`** — an empty file that makes Godot skip a folder. Put one in the source-art
  folder so `.blend`, `.psd`, `.kra` don't get imported.
