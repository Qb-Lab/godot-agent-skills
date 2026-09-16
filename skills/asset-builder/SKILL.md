---
name: asset-builder
description: Execute approved art and asset work for a Godot game — blockouts, concept explorations, models, textures, materials, shaders, VFX, animation, UI art, modular kits — from the project's Art Bible, production plan, and asset registry, choosing the right method (Godot primitives, a @tool or headless script, procedural geometry, a shader, particles, Blender, image generation, a CC0/purchased asset, or a written spec for a human artist) and leaving the result game-ready with its state recorded. Use when the user says "build it", "build phase N", "build the blockout", "make the water shader", "make three concepts for the player", "make a broken version of the chair", "try a darker variant", "make a cheaper version", or asks for any asset, placeholder, or visual to be produced. Reads project state before acting; never builds an asset with no spec or one that contradicts the Art Bible without saying so first.
category: production
---

# Asset Builder

`art-direction` decides; this skill builds. It turns an approved spec into files in the
project, in the right order (blockout before beauty), by the right method (a shader, not a
texture; a kit, not thirty walls), and leaves the registry telling the truth about what now
exists. It is `build-loop` for assets: one asset or one increment at a time, verified, recorded.

Two rules sit above every other:

1. **State first, prompt second.** The user's instruction is combined with the project's
   persistent context — it does not replace it. "Make the chair darker" happens inside the
   Art Bible's palette rule, not instead of it, unless the user explicitly changes the bible.
2. **A file existing is not an asset existing.** `chair.glb` on disk is a *source output*;
   the asset is the imported, wrapped, collided, scripted, replicated scene the game uses.
   Report which one you produced.

## Before anything

Read, every session, in this order — the registry is the memory, not the conversation:

```bash
SKILL_DIR="$(cd "$(dirname "<path of this SKILL.md>")" && pwd)"
R="$SKILL_DIR/../art-direction/scripts/registry.py"   # siblings in every layout
python3 "$R" status
```

Then `docs/design/ART-BIBLE.md`, `docs/design/PRODUCTION.md` (current phase, reusable systems,
production strategy table), and `registry.py show <ID>` for each asset in scope — plus its
`spec_file` and the `DD-` entries it cites in `DECISIONS.md`. If `registry.py` is missing,
`art-direction/references/asset-registry.md` documents the plain-JSON format; if the Art
Bible is missing, stop: there is no direction to build to, and `art-direction` is the skill
that creates one.

## Resolve what "it" is

- **"Build it"** → the asset(s) just specced in this session; failing that, the entries with
  `review approved` at their current stage in the lowest incomplete phase; failing that, ask
  — with the candidates listed from `registry.py status`, recommended one first.
- **"Build phase N"** → `list --phase N`, ordered by dependencies: kits, master materials,
  shared rigs, and components before the pieces that use them (`deps ID`). Stop at every
  human checkpoint the plan names; do not build past an unapproved hero concept.
- **"Build X except Y"**, **"all dining-room props"** → filter the list, say what you excluded.
- **A custom instruction on an existing asset** ("broken version", "longer arms, same front
  silhouette", "cheaper version") → a variant or a superseding entry (below), never a silent
  overwrite of the approved one.
- **An asset with no entry** → if it is small and obviously implied by the plan (a fourth
  chair variant), add the entry yourself with a spec that inherits the family's; anything
  larger goes back to `art-direction` for a spec. Never build from a one-line prompt what
  needs a decision.

## Check for conflicts before building

Compare the request against the Art Bible section it touches and the `DD-` entries the asset
cites. When they conflict, do not follow the request silently:

```markdown
This conflicts with **DD-004** — all mansion furniture uses exaggerated proportions
(readability in 4-player chaos). A realistic chair would read as a different game's asset.

**A. Keep DD-004; build the chair exaggerated (recommended)** — consistent with the six props
already validated; the "realistic" feel you want is achievable through wear and material.
**B. Build it as an explicit exception** — recorded as a variant with the reason; risks a
visible odd-one-out in the dining room.
**C. Change DD-004 globally** — reopens the six validated props (`registry.py list --kit KIT_MANSION_MODULAR`).

Recommendation: A.
```

One question, then follow the answer. An override becomes a `DD-` entry (via
`design-record`) and a note on the asset — so the next session does not "fix" it back.

## Choose the production method

Do not treat every request as image generation. `references/production-methods.md` has the
table; the calls that come up most:

| The request is really… | Produce |
|---|---|
| validating scale, reach, collision, camera, flow | a **blockout** from Godot primitives, by script |
| exploring how something could look | 2–3 **concepts** (generated images or written boards), not one |
| water, fire, fog, wobble, dissolve, damage, outlines, wind | a **shader** (+ particles), not a texture or mesh |
| explosions, impacts, sparks, dust, blood, magic | **VFX** (GPUParticles + light + decal), not geometry |
| thirty similar architectural pieces | a **modular kit** + trim sheet, then instances |
| twelve furniture pieces in one material | **one master material**, meshes reuse it |
| a reaction, a death, breathing, look-at | **procedural or physics animation** in code, or a shader |
| a generic barrel, crate, rock, tree | a **CC0/purchased base** (record the licence) + the master material |
| a hero face, a signature creature's final look | a **spec for a human artist**, if the plan budgets one |

When the better method differs from what the user asked for, say so once with the cost
difference, then build what they choose.

## Blockout first

For any entry flagged `blockout: true` — and for anything you are unsure of — the first
build is a blockout: primitives at real scale, collision, physics where the gameplay needs
it, a scale reference in the scene, colour-coded by function. Validate with the user in the
game (reach, camera, doors, throw arcs, nav bake, multiplayer authority) before anything
gets a real mesh. `references/blockout.md` covers how, and the checklist to walk. The
registry gate refuses `PRODUCTION` until the blockout is approved; do not `--force` it
because the geometry "seems fine".

## Produce

- **Scenes are generated, never hand-written.** The control layer denies structural `.tscn`
  edits; build scenes from a `@tool`/`EditorScript` or a headless `SceneTree` script that
  constructs nodes and saves with `PackedScene.pack()` + `ResourceSaver.save()`. Then run
  `godot --headless --path . --import` and load-check. `godot-scene-surgery` applies.
- **Source vs game-ready.** Source (`.blend`, `.kra`, `.psd`, generation inputs) goes in
  `art/source/…` with a `.gdignore`; game-ready outputs (`.glb`, `.png`, `.gdshader`, `.tres`,
  `.tscn`) under `res://assets/<category>/` — or wherever the project already keeps them.
  Follow the bible's *Naming & files* section; a fresh project gets the default proposed there.
- **Game-ready means the checklist for its type passed** — import settings, materials mapped
  to the master material, collision (glTF `-col`/`-convcol` suffixes or a generated shape),
  the right body type, scene wrapper with the interaction component, replication where the
  spec says, a test scene. `references/godot-integration.md` per type. Only add what the
  gameplay actually requires — a decorative vase needs no physics body.
- **Reproducibility.** Every generated concept or texture records its tool, model, prompt,
  negative prompt, seed, and reference input on the file entry (`registry.py file … --tool
  … --prompt … --seed …`). Every CC0/purchased asset records source and licence in a note.
- **Variants and replacements.** A variant ("broken chair") is a new entry that
  `depends_on` the original and is listed in its `variants`. A replacement ("v2 with
  shorter legs") is `supersede OLD NEW`: the old entry stays, marked, with its files; the
  new one is authoritative. Never overwrite an approved asset's files in place.
- **When a tool is unavailable** — no Blender, no image generation, no engine binary — do
  the parts you can (the spec, the shader code, the scene script, the prompt package), mark
  the entry's status honestly (a written spec is still `PLANNED`; a prompt package without
  an image is not `CONCEPT`), and say exactly what a human or another tool must do. Never
  imply an asset exists because its description does.
- **Reusability.** Before building an isolated asset, check `PRODUCTION.md → Reusable
  systems` and `registry.py list --type kit|material|shader`. Build the system when the
  plan names it and this asset is its first real use; do not invent a system without one.

## Record, verify, report

After each asset or increment:

```bash
python3 "$R" file ID <path> --kind source|output|godot [--tool … --prompt … --seed …]
python3 "$R" set  ID CONCEPT|BLOCKOUT|PRODUCTION|INTEGRATED --note "what was done"
python3 "$R" review ID request --note "what to look at"        # at a human checkpoint
python3 "$R" validate
```

Never set `VALIDATED` — that is `asset-review`'s verdict, from a session that did not build
the thing. If Godot files changed, run `godot-verify` before reporting; the Stop hook will
insist anyway. Then update the phase table in `PRODUCTION.md` and report in this shape:

```markdown
**Produced:** ENV_PROP_DINING_CHAIR_01 → INTEGRATED — glb + wrapper scene + convex collision,
CMP_GRABBABLE wired; headless import/load clean.
**Needs your review:** CHAR_PLAYER_01 concept sheet (3 proportion studies, B recommended) —
`registry.py review CHAR_PLAYER_01 approve` when chosen.
**Could not do here:** no Blender on PATH — the kit's glb export is specced in
`art/source/kit/EXPORT.md`; entry stays PRODUCTION.
**Next:** review the chair (`asset-review`), then the remaining phase-1 props.
```

## Where this sits

`art-direction` (spec, `PLANNED`) → **asset-builder** (CONCEPT / BLOCKOUT / PRODUCTION /
INTEGRATED, `review request` at checkpoints) → the user approves → `asset-review` (VALIDATED
or REWORK) → `design-record` for anything decided on the way → `session-handoff` as usual.
