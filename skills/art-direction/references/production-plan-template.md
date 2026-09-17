# Production plan — template and guidance

`docs/design/PRODUCTION.md` is the *work*: phases, checkpoints, reusable systems, and the
production method per category. Direction lives in `ART-BIBLE.md`; per-asset state lives in
the registry. The plan uses `write-plan`'s skeleton — same progress tracker, same execution
rule — so any session that knows how to build a phase of a plan knows how to build a phase
of this one. The executing skill is `asset-builder`; the judge is `asset-review`.

## Shaping phases

Phases are seams where the user must **see something before the next thing is built**, or
where the output determines the next phase's design. Never phase by kind of work. The
recurring shape — adapt it, don't copy it:

- **Visual discovery** — reference board, palette, shape-language sheet, proportion
  studies, and the **visual concept exploration**: five images of one gameplay moment in
  five curated directions, compared, refined over at most three rounds, one approved
  (`art-direction/references/concept-exploration.md`). Output: an approved visual target;
  bible sections go APPROVED on it. Cheap; mostly generated images and written rules.
- **Gameplay blockout** — player placeholder at real scale, enemy placeholders, environment
  greybox, gameplay props as primitives with collision and physics, a scale reference in every
  scene. Output: the loop is playable with ugly assets. This phase is the prototype
  `scope-control` wants; it does not wait for the visual direction.
- **Visual prototype** — *one* representative environment, *one* hero character, *one*
  creature, a handful of props, a first lighting pass, one or two representative VFX, all to
  final quality in the approved style, built to the approved visual-target image. Purpose:
  prove the direction works **inside the game**, in motion, at gameplay distance. Output: bible sections go APPROVED or get changed
  cheaply. This is the most important checkpoint in the whole pipeline.
- **Core production kit** — the modular kit(s), master materials, trim sheets, shared rig and
  base animation set, the shader library, the VFX library, UI theme. Output: content can be
  produced fast and consistently. Gated on verified fun (`playtest-review`) unless the
  concept is art-led.
- **Content production** — rooms, creatures, props, animations built *from* the kit. Batch
  approvals. Output: the game's content at MVP scope (`GAME.md` → Current MVP scope).
- **Polish** — LODs where profiling demands, secondary motion, post stack, decals, UI icons,
  the last 10% of hero assets. Only after the above; polishing before content is the trap.

Merge or split against the game: a 2D pixel game folds discovery and prototype together (the
palette and tile size *are* the prototype); a first-person horror game may need lighting as
its own early phase because the mood is the pitch.

## Skeleton

```markdown
# <Game> — art & asset production plan

## Goal
One paragraph: what is true of the game's look and asset base when this plan is done.
**Non-goals:** what this plan deliberately does not produce (e.g. no cosmetics, no LODs
until profiled, no second biome).

## Progress
| Phase | Status | Checkpoint |
|---|---|---|
| 0. Visual discovery | done | visual target `CONCEPT_VISUAL_R2_A` approved 2026-09-02 |
| 1. Gameplay blockout | in progress | walkthrough with user |
| 2. Visual prototype | not started | hero character + room approved |
| 3. Core production kit | not started | kit assembles the prototype room |
| 4. Content production | not started | batch approvals per room |

Current phase: 1 · Recommended next: finish 1 (2 blockouts in REWORK) — see `registry.py status`
> Executing agent: update this table at the end of your run and note any deviation in one
> line each, below this block.

## Direction & constraints
- Direction: see `ART-BIBLE.md` (do not restate it here). Load-bearing decisions: DD-001…DD-006.
- Engine: Godot 4.3 · 3D · first-person · 4-player co-op (transforms of held props replicated)
- Tools available: Godot headless, Blender 4.x CLI, image generation via <tool>; no human artist
- Read first: `ART-BIBLE.md`, `GAME.md`, `registry.py status`

## Execution rule
At the start of each phase, verify this plan against the live repo, the registry, and any
deviations recorded above. Do not reopen settled decisions without new evidence. If an
assumption is invalidated, update this file and say so.

## Reusable systems
Build these once; everything else instances them. Each is a registry entry other entries
depend on.
- `KIT_MANSION_MODULAR` — 1 m grid, corner pivot: wall, inner/outer corner, doorway, window
  wall, trim, floor, ceiling, stairs. Trim sheet `MAT_MANSION_TRIM_01`.
- `MAT_MASTER_WOOD_01`, `MAT_MASTER_FABRIC_01` — master materials with colour/wear params.
- `RIG_HUMANOID_SHORT_01` — one rig + base locomotion set shared by player and human NPCs.
- `SHADER_DISSOLVE_01` — death/despawn for every creature (no per-creature death animation).
- `VFX_IMPACT_LIB_01` — hit sparks / dust / blood variants driven by a surface parameter.
- `CMP_GRABBABLE` — the interaction + replication component every physics prop uses.

## Production strategy
| Category | Method | Notes |
|---|---|---|
| Concepts & reference | image generation + reference boards | prompts recorded in the registry |
| Blockouts | Godot primitives via `@tool`/headless script | never hand-written `.tscn` |
| Architecture kit | Blender (bpy script) → glTF; trim sheet | `-col` suffix collision |
| Props | Blender or CC0 base (Kenney/Quaternius/Poly Haven) + master materials | record licence |
| Hero character | Blender; human artist pass on the face if budget allows | approval at concept and at prototype |
| Creatures | Blender + shared rig family; procedural reactions in code | dissolve death |
| Shaders / VFX | Godot shading language; GPUParticles | budget per effect class |
| UI | Godot Theme + 9-slice textures | after visual prototype |

## Phase 0 — Visual discovery
**Goal:** one sentence.
**Build:** the registry entries this phase produces (ids) — the `CONCEPT_VISUAL_R<n>_<x>`
candidates among them — and the bible sections it promotes.
**Checkpoint:** the user picks the visual target from the concept round(s)
(`registry.py review CONCEPT_VISUAL_… approve`); rejected candidates are `REJECTED` with reasons.
**Exit criteria:** one approved visual-target concept; every other listed entry ≥ CONCEPT
with `review approved`; the bible sections the image settles at APPROVED, the rest at
PROVISIONAL; `registry.py validate` clean.

## Phase 1 — Gameplay blockout
**Goal:** the loop is playable end-to-end with placeholder assets at real scale.
**Build:** `CHAR_PLAYER_01` (BLOCKOUT), `CREATURE_STALKER_01` (BLOCKOUT), `ENV_MANSION_GROUNDFLOOR_BLOCKOUT`,
props `ENV_PROP_*` as primitives with `CMP_GRABBABLE`, `REF_SCALE_HUMAN` in every scene.
**Checkpoint:** user walks the blockout — reach, camera, door widths, throw arcs, nav — and
approves each blockout entry.
**Exit criteria:** every phase-1 entry at BLOCKOUT with `review approved`; the project
imports and loads headless (`godot-verify`); the playtest question for this build is written
(`playtest-review`).

## Phase 2 — Visual prototype
...
```

## Rules the plan enforces

- Nothing enters PRODUCTION while its BLOCKOUT is unapproved (the registry gate enforces
  it; the plan says why).
- Hero assets get a human checkpoint at CONCEPT and again at INTEGRATED; small assets are
  approved in batches named in the phase.
- Phases beyond the blockout are gated on the loop being verified fun unless the plan says
  the concept is art-led and why.
- The plan never restates the bible. If a phase needs a rule, it links the section.
