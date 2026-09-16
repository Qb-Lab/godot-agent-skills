---
name: asset-review
description: Review a produced asset, concept, blockout, model, material, shader, VFX, animation, or Godot integration against the game's concept, Art Bible, asset spec, technical budgets, and Godot best practice — the separated judge that issues VALIDATED or REWORK, kept apart from the session that built the thing. Use when the user asks to review, check, QA, approve, or validate an asset or a batch of assets; before an asset is integrated or marked done; when something "looks off", "doesn't match the style", or "feels out of scale"; or when the registry shows entries awaiting review. Inspects the real files and scenes rather than trusting that they exist.
category: production
---

# Asset Review

The session that built an asset will grade it generously and in perfect good faith. This
skill is the other pair of eyes: it reads the spec and the Art Bible, opens the actual files,
runs the actual checks, and says whether the asset is what the game needs — not whether the
builder worked hard. It is `playtest-review`'s separation of judge from builder, applied to
art; it is also the only thing that can set `VALIDATED` in the registry.

## Evidence tiers — state the tier with every finding

**Inspected in the engine** (headless import + load, scene dump, a test scene the user ran)
> **inspected in the file** (`inspect-gltf.py`, reading the `.tscn`/`.gdshader`/`.tres`,
viewing the image) > **argued from the spec and bible**. Never blur them. If you cannot view
an image in this session, say so and ask for the file or a screenshot — do not review a
concept from its prompt. If Godot is not on PATH, the integration review is *file-level* and
the report says so.

## Before reviewing

```bash
SKILL_DIR="$(cd "$(dirname "<path of this SKILL.md>")" && pwd)"
R="$SKILL_DIR/../art-direction/scripts/registry.py"
python3 "$R" status && python3 "$R" list --needs-review
python3 "$R" show <ID>                    # spec, files, decisions, history (incl. any FORCED gate)
```

Then read: the bible sections the asset touches, its `spec_file`, the `DD-` entries it cites,
and the checklist for its type in `references/checklists.md`. The review compares the asset
to **those** — not to your taste, and not to the builder's description of it.

## What to review against, in order of weight

1. **Concept & spec** — does it do the gameplay job? A chair the player cannot read as
   grabbable fails before its topology is discussed.
2. **Art Bible** — style family, shape language, proportions, palette rule, material
   conventions, readability at gameplay distance, silhouette against the player.
3. **Technical** — scale, orientation, pivot, transforms, triangle count vs budget, normals,
   UVs, texture sizes, material remap, collision type, rig/animations present, import
   settings applied.
4. **Godot integration** — right root node type for the gameplay, wrapper structure,
   collision matches use (convex on rigid bodies), physics behaviour, shader/material setup,
   replication where specced, naming, placement, test scene, dependencies recorded.
5. **Performance** — against the bible's budgets: draw calls a kit piece adds, shader cost,
   particle counts, texture memory.

Blocking = fails 1, 2 on a pillar, or 3/4 in a way the game will hit (wrong scale, missing
collision, trimesh on a rigid body, no replication where specced). Polish = everything else.
Rank by threat to the game, not by how many things you noticed.

## Tools

- `python3 "$SKILL_DIR/scripts/inspect-gltf.py" <file.glb|.gltf> [--budget N] [--expect-height H]`
  — nodes with non-identity transforms, meshes with triangle counts and attribute presence
  (normals, UVs, tangents, skin), materials and textures, animations and durations, skin
  joint count, bounding box in metres, pivot offset from the floor, Godot import-hint
  suffixes, and warnings for the classic failures.
- `godot --headless --path . -s "$SKILL_DIR/scripts/inspect_scene.gd" ++ res://path/to.tscn`
  — dumps a scene's tree with node types, scripts, collision shapes and sizes, body masses,
  mesh surface counts and material types, particle counts, animation lists, synchronizers,
  and the mesh AABB. Not yet run against an engine in this repo — if your version rejects the
  invocation, copy the script into `res://tools/` and run it from there, and report what it
  printed.
- `godot --headless --path . --import && godot --headless --path . --quit` — the load check
  every integration review runs (`godot-verify` reads the output honestly).
- For images: view the file directly when the host allows; otherwise the user supplies
  screenshots — from the test scene, at gameplay distance, under the bible's lighting.

Read the `.tscn` as text when needed (`godot-scene-surgery` describes the format) — but
you are *reading*, never editing: findings go to the builder, fixes are not the reviewer's job.

## The report

```markdown
# Asset review — ENV_PROP_DINING_CHAIR_01 — 2026-09-12
**Reviewed against:** spec (registry), ART-BIBLE §Props, §Materials, §Performance; DD-004, DD-007
**Evidence:** inspected in file (inspect-gltf, .tscn read); engine load clean; not seen in-game

## Verdict: REWORK
1. **[blocking] Pivot at mesh centre, not floor** — inspect-gltf: bbox min.y = -0.45 m. Every
   placement floats or sinks; the kit convention (bible §Naming) is centre-bottom. → re-export
   with origin at the base.
2. **[blocking] Trimesh collision (`-col`) on a RigidBody3D** — moving bodies need convex
   (`-convcol`) or a primitive; this one will fall through the floor at speed. → rename the
   collision node in the source and re-import.
3. **[polish] Proportions read realistic** — legs 4 cm vs the exaggerated 7–9 cm rule
   (DD-004); at gameplay distance it reads as a different game's chair. → thicken legs, shorten
   back 10%.

## Passes
Triangle count 640 / 1,500 budget; master material remapped; CMP_GRABBABLE present with mass
6 kg; synchronizer on transform; test scene present.

## Not reviewable here
In-game feel of the throw arc — needs the user to run `props_test.tscn`.
```

Then record it:

```bash
python3 "$R" verdict ENV_PROP_DINING_CHAIR_01 fail --note "1 pivot at centre; 2 trimesh col on rigid body; 3 legs under DD-004 min"
# or
python3 "$R" verdict ENV_PROP_DINING_CHAIR_01 pass --note "inspected in file + engine load; in-game throw confirmed by user 2026-09-12"
```

Say what is genuinely right, specifically — it tells the builder what not to touch. Do not
pad a good asset with soft concerns to look thorough; if it passes, it passes.

## Taste, approvals, and the bible itself

- **Human calls stay human.** Whether the creature is *scary*, whether the chair is *funny* —
  flag as "human call", attach what to look at and at what distance, and let the user's
  `review approve` be the record. Your verdict covers the checkable rules.
- **Hero assets** get a review *and* a human approval; prepare the approval packet (test
  scene, screenshots, the spec's promises as a checklist) rather than approving on their
  behalf.
- **Batch reviews** for kit pieces and small props: one report, a table of ids with pass/fail
  and the one-line reason, then a `verdict` per id.
- **When the bible is what's wrong** — the asset obeys the rule and the rule produces a bad
  result — pass or fail the asset against the rule as written, and raise the rule as a
  separate finding routed to `art-direction` with a `DD-` entry proposed. Do not quietly
  review against the rule you wish existed.
- **Approved decisions are not re-litigated** here. A `FORCED:` gate bypass in the history is
  reviewed on its own terms: was the reason sound, did the skipped stage's checks get done
  another way?

## Where this sits

`asset-builder` → `review request` → user look where taste is involved → **asset-review**
→ `verdict pass|fail` → back to `asset-builder` for REWORK, or on to the next asset. The
reviewer never edits the asset it is judging; a fix it makes is a fix nobody reviewed.
