# Production methods — which tool makes which thing

The most expensive mistake in asset work is producing the right thing by the wrong method: a
death *animation set* where a dissolve *shader* would do; a *texture* of wet stone where a
*material parameter* would do; thirty *unique walls* where a *kit* would do. Choose the
method before opening any tool. Where a tool is unavailable, produce the best honest
substitute — a spec, a script, a prompt package — and say what is missing.

## Detecting what is available

```bash
command -v godot godot4 || ls /Applications/Godot.app/Contents/MacOS/Godot   # or $GODOT_BIN
command -v blender || ls /Applications/Blender.app/Contents/MacOS/Blender
python3 -c "import PIL" 2>/dev/null && echo pillow                         # image manipulation
command -v magick convert                                                  # ImageMagick
```

Image generation depends on what the host session exposes (an MCP tool, an API the user
configured, or nothing). Check the tools available in the session; do not assume. Record the
answer in `PRODUCTION.md → Direction & constraints → Tools available` so later sessions do
not re-discover it.

## The decision table

| Need | Method | When it is wrong |
|---|---|---|
| Validate scale / reach / collision / camera / flow | **Blockout** — Godot primitives via script (`blockout.md`) | never wrong as the *first* step for gameplay-heavy assets |
| Explore how something could look | **Concept**: 2–3 generated images from a prompt built from the Art Bible + spec; or a written reference board when no image tool exists | one image is a guess, not exploration; a concept without bible rules in the prompt drifts |
| A surface that is *about* its material (wood, metal, fabric) | **Master material** (`StandardMaterial3D`/`ShaderMaterial` `.tres`) with parameters; meshes reuse it | unique textures per prop — consistency and texture budget die |
| Architecture detail across a kit | **Trim sheet** texture + UVs mapped to it | per-wall textures |
| Water, fire, smoke, fog, wind, foliage sway, dissolve, damage, outlines, PSX wobble, pixelation | **Shader** (`.gdshader`, Godot shading language) — surface or screen-space | modelling or animating it; baking it into a texture |
| Explosions, impacts, sparks, dust, blood, magic, rain | **VFX**: `GPUParticles3D/2D` + `ParticleProcessMaterial`, a light, a decal | geometry, sprite-sheet-only |
| Bullet holes, blood on walls, dirt, posters | **Decal** node / `Decal`-style quad | new textures per surface |
| A lot of the same thing (grass, debris, crowd props) | `MultiMeshInstance3D` / GPU instancing / `Scatter`-style tooling | individual nodes |
| Reaction, breathing, look-at, foot placement, lean | **Procedural animation** in code (`SkeletonModifier3D` in 4.3+, `SkeletonIK3D` earlier — check the version), or a vertex shader for non-characters | an authored clip per case |
| Death, knockback, comedy flailing | **Ragdoll / physical animation** (`PhysicalBone3D`) or a dissolve shader | authored death animations per creature |
| Locomotion and signature actions | **Skeletal animation** — authored in Blender, or keyframed via script into an `AnimationLibrary`; blended in `AnimationTree` | procedural for anything that must read as *intentional* |
| Rooms and buildings | **Modular kit** — grid-snapping pieces, corner pivots, one trim sheet, exported as glTF with `-col` suffixes | unique room meshes |
| Generic props (barrel, crate, rock, tree, bottle) | **CC0 / purchased base** — Kenney, Quaternius, Poly Haven, ambientCG, Sketchfab CC0 — re-materialed with the master material; licence in a note | modelling from scratch |
| Hero character body, creature body, signature prop | **Blender** (`blender -b -P script.py` for procedural or batch work; interactive for sculpting) → glTF | primitives past the blockout stage |
| Hero face, final creature look, key art | **Human artist**, with a spec package (bible sections, spec, blockout screenshots, concept picks) | generated images presented as final |
| Pixel art, sprites, tiles | drawn in Aseprite/Krita by a human or generated + hand-cleaned; palette-constrained | generated pixel art used raw — palette and grid will be wrong |
| UI panels, HUD | Godot `Theme` + `StyleBoxTexture` 9-slices + `StyleBoxFlat`; icons as SVG where the style allows | screenshots of generated menus |
| Textures for stylised looks | procedural (shader noise, gradient ramps) or generated + palette-quantised | photo textures in a stylised game |

## Per-method notes

### Godot primitives and scripts (blockouts, placeholders, procedural geometry)

Build with `BoxMesh`, `CylinderMesh`, `CapsuleMesh`, `SphereMesh`, `PlaneMesh`,
`PrismMesh`, or `CSGBox3D`/`CSGCombiner3D` for quick boolean shapes (CSG is for blockouts,
not shipping geometry — it is slow and has no proper UVs). Procedural meshes use
`SurfaceTool` or `ArrayMesh`; save as `.tres`/`.res` with `ResourceSaver`. Always by script —
the scene-file guard denies structural hand edits, and a script is reproducible.

### Blender (CLI)

`blender -b -P build_kit.py -- --out res/assets/kit/` runs headless. Export glTF with
`export_format='GLB'`, `export_yup=True`, apply transforms, `export_apply=True`, metres.
Name nodes with Godot's import suffixes: `-col` (trimesh collision), `-convcol` (convex),
`-colonly` (collision without mesh), `-rigid`, `-navmesh`, `-noimp`. Blender's +Y is
Godot's -Z: face the model down -Y in Blender so it faces -Z in Godot. If Blender is absent,
write the `.py` and the `EXPORT.md` anyway — a human with Blender runs it in a minute.

### Image generation (concepts, reference, textures)

The prompt is assembled from the Art Bible, not improvised: style family, shape language,
palette words, camera/perspective, the asset's spec, and a negative prompt for what the
bible forbids. Generate 2–3 variations for a concept; one image is not exploration. Record
tool, model, prompt, negative prompt, seed, and any reference input on the file entry.
Generated *textures* need palette quantisation and seam checks before use; generated
*models* need retopology and are almost never game-ready as produced — treat them as
concepts unless reviewed.

### Shaders

Godot shading language, `.gdshader` in `res://assets/shaders/`, one `ShaderMaterial` `.tres`
per use with parameters exposed via `uniform`. Keep hero effects (water) as their own
registry entry; keep the shader cheap enough for the bible's budget (instruction count,
texture reads, overdraw). Version-specific API (e.g. `hint_screen_texture`, 4.x) is the other
packs' territory — check the project's version.

### VFX

`GPUParticles3D` with `ParticleProcessMaterial` for anything numerous; `CPUParticles` only
when GPU particles are unsupported on the target (GL Compatibility mobile). One-shot effects
set `one_shot = true`, `explosiveness` near 1, and are pooled or freed on `finished`. Each
effect class has a budget in the bible; a hit-spark that spawns 2,000 particles is a REWORK.

### Animation

Authored clips live in an `AnimationLibrary` shared by a rig family; the `AnimationTree` state
machine is part of the character's INTEGRATED checklist. Procedural motion is code and is
therefore versioned, testable, and reviewable — prefer it for everything reactive.

### CC0 / purchased

Record source URL, licence, and any modification in a registry note. Re-material to the
master materials so bought assets do not look bought. Check scale on import (many packs are
not in metres) and re-pivot.

### Human artist

The spec package: the bible sections that apply, the registry spec, `spec_file`, blockout
screenshots with measurements, the approved concept, the budgets, the file format and pivot
rules, and the checklist `asset-review` will run. Status stays where it is; note who has it.
