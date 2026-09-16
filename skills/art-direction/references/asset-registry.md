# Asset registry — format, lifecycle, gates

`docs/design/asset-registry.json` is the persistent answer to "what exists, what is approved,
what was rejected, what is authoritative, what is next". Claude never relies on conversation
memory for any of those; it runs `registry.py` and reads the answer.

The script lives at `scripts/registry.py` beside the `art-direction` skill. From another skill
resolve it as `$SKILL_DIR/../art-direction/scripts/registry.py` — the skills are siblings in
both the repo layout and every installed layout. If the script is genuinely absent, the file
is plain JSON in the format below and can be edited directly; keep the invariants by hand
(append to `history`, never delete, VALIDATED only from a review).

## Lifecycle

```
PLANNED ─→ CONCEPT ─→ BLOCKOUT ─→ PRODUCTION ─→ INTEGRATED ─→ VALIDATED
                │           │           ▲             │
                │           │           └── REWORK ◄──┘   (review verdict fail → fix → back)
                └───────────┴──→ REJECTED / SUPERSEDED   (terminal; kept forever)
```

| Status | Meaning | Who sets it |
|---|---|---|
| `PLANNED` | specced, nothing built | art-direction (`add`) |
| `CONCEPT` | exploration exists — sketches, board, proportion study, 2–3 alternatives | asset-builder |
| `BLOCKOUT` | placeholder at real scale in the game; validating scale/collision/nav/reach/camera | asset-builder |
| `PRODUCTION` | the real asset is being made — source files, textures, rig, shader | asset-builder |
| `INTEGRATED` | game-ready in Godot: imported, wrapped, collision/physics/material/script wired, test scene | asset-builder |
| `VALIDATED` | passed review against spec, bible, budgets, Godot practice | **asset-review only** (`verdict pass`) |
| `REWORK` | review failed or user sent it back; latest note says what to change | asset-review / user |
| `REJECTED` | killed with a reason; stays so the idea stays rejected | user via any skill |
| `SUPERSEDED` | replaced; `superseded_by` names the authoritative entry | `supersede` |

Not every asset visits every stage: a shader has no blockout; a decorative prop may go
PLANNED → PRODUCTION → INTEGRATED. Skipping is fine; the gates only bite where a flag says
the stage matters.

## The `review` field and the two flags

`review` ∈ `none | pending | approved` is the human's sign-off on **the current status's
output**. It resets to `none` on every status change, because a new stage has new output.
`review request` is the builder saying "look at this"; `review approve` is the user's call
recorded; `review rework --note` sends it back.

- `hero: true` — the user must approve the CONCEPT before PRODUCTION. Main character,
  each primary creature, the representative environment, anything on the store page.
- `blockout: true` — gameplay-heavy; the asset must pass through an **approved** BLOCKOUT
  before PRODUCTION. Rooms, buildings, doors, stairs, carried furniture, interactive
  machines, vehicles, large enemies, gameplay props.

Both gates can be bypassed with `set … --force --note "why"`, which records `FORCED:` in the
history — visible to every later review. `set … VALIDATED` is never allowed; only `verdict`
reaches it, so "a file exists" can never become "done" by accident.

## Entry shape

```json
"ENV_PROP_DINING_CHAIR_01": {
  "id": "ENV_PROP_DINING_CHAIR_01",
  "name": "Dining chair",
  "type": "interactive-prop",
  "phase": 1,
  "status": "INTEGRATED",
  "review": "pending",
  "hero": false,
  "blockout": true,
  "purpose": "Physics-enabled mansion furniture the players fight with",
  "spec": {
    "gameplay": "pick up, carry, drop, throw; breaks after 3 hard impacts",
    "visual": "Victorian mansion kit; exaggerated proportions per DD-004; wood master material",
    "requirements": ["single mesh", "pivot centre-bottom", "convex collision", "mass 6 kg", "MAT_MASTER_WOOD_01"],
    "lod": "none initially",
    "animation": "none",
    "networking": "transform replicated while held or moving (CMP_GRABBABLE)"
  },
  "spec_file": null,
  "kit": "KIT_MANSION_MODULAR",
  "decisions": ["DD-004", "DD-007"],
  "depends_on": ["MAT_MASTER_WOOD_01", "CMP_GRABBABLE"],
  "variants": ["ENV_PROP_DINING_CHAIR_01_BROKEN"],
  "files": [
    {"path": "art/source/props/dining_chair.blend", "kind": "source", "added": "2026-09-10"},
    {"path": "res://assets/props/dining_chair.glb", "kind": "output", "added": "2026-09-10"},
    {"path": "res://assets/props/dining_chair.tscn", "kind": "godot", "added": "2026-09-11"},
    {"path": "art/concepts/dining_chair_v2.png", "kind": "concept", "added": "2026-09-08",
     "generation": {"tool": "<image tool>", "model": "<model>", "prompt": "…", "negative_prompt": "…", "seed": "184223", "ref": "art/reference/mansion_board.png", "date": "2026-09-08"}}
  ],
  "godot": {"scene": "res://assets/props/dining_chair.tscn", "resources": []},
  "supersedes": null,
  "superseded_by": null,
  "validation": {"result": null, "date": null, "findings": null},
  "notes": [],
  "history": [{"date": "2026-09-08", "from": null, "to": "PLANNED", "note": "created"}, "…"],
  "created": "2026-09-08",
  "updated": "2026-09-11"
}
```

**Ids** are `CATEGORY_NAME_NN`, upper-case with underscores, stable forever. Prefixes in use
are the team's convention — the registry only checks the shape. Common: `CHAR_`, `CREATURE_`,
`ENV_` (`ENV_PROP_`, `ENV_ROOM_`), `KIT_`, `MAT_`, `SHADER_`, `VFX_`, `ANIM_`, `UI_`, `ICON_`,
`DECAL_`, `CONCEPT_`, `REF_`, `CMP_` (a reusable component), `WEAPON_`, `VEHICLE_`.

**Types:** character, creature, architecture, environment, prop, interactive-prop, weapon,
vehicle, ui, texture, material, shader, animation, vfx, decal, icon, concept, reference,
audio-hook, kit. A `kit` entry represents the family (grid, pivot, piece list); its pieces
set `kit` and `depends_on` it.

**Spec** is free-form keys, but a fresh session must be able to build from it: purpose,
gameplay role, the visual rules it inherits (cite bible sections and `DD-` ids rather than
restating), concrete requirements, LOD/animation/networking needs. Long design pages go in
`docs/design/specs/<ID>.md` as `spec_file`; keep the JSON spec to the buildable summary.

**Files** carry `kind`: `source` (blend/psd/kra — not imported by Godot), `output` (glb/png
the engine imports), `godot` (the `.tscn`/`.tres` the game uses; a `.tscn` also sets
`godot.scene`), `concept`, `reference`, `spec`. **Generation metadata** attaches to the file
it produced — tool, model, prompt, negative prompt, seed, reference input, date — so the
result can be reproduced or iterated. Record it for every generated concept and texture; skip
it for hand-authored files.

## Replacing and rejecting

Never delete. `supersede OLD NEW` marks OLD `SUPERSEDED`, sets `superseded_by`, creates NEW
from OLD's spec (files and state start empty) with `supersedes` set, and lists everything
that depended on OLD so the dependency can be repointed deliberately. `set ID REJECTED
--note "why"` keeps the entry and its reason; `list --all` / `list --status REJECTED` shows
them; `status` counts them. A rejected concept's prompt and seed stay in its files so the
same thing is not generated again next month.

## Commands

```bash
R="$SKILL_DIR/scripts/registry.py"            # or ../art-direction/scripts/registry.py
python3 "$R" status                            # orientation — always first
python3 "$R" list [--phase 1] [--status BLOCKOUT] [--type prop] [--kit KIT_X] [--needs-review] [--all] [--json --ids]
python3 "$R" show ID [--json] [--history N]
python3 "$R" deps ID
python3 "$R" add ID --type T --phase N [--name] [--purpose] [--hero] [--blockout] \
        [--spec '{"gameplay":"…"}' | --spec-field key=value …] [--spec-file P] [--kit K] [--decision DD-004]… [--depends-on ID]…
python3 "$R" set ID STATUS [--note "…"] [--force]
python3 "$R" review ID request|approve|rework [--note "…"]
python3 "$R" verdict ID pass|fail [--note "ranked findings"]      # asset-review only
python3 "$R" file ID PATH --kind source|output|godot|concept|reference|spec \
        [--tool T --model M --prompt "…" --negative-prompt "…" --seed S --ref P]
python3 "$R" edit ID field value                 # name purpose phase hero blockout kit spec.<key>; append to decisions/depends_on/variants
python3 "$R" note ID "text"
python3 "$R" supersede OLD NEW [--name] [--note]
python3 "$R" validate                            # consistency + files on disk; exit 1 on FAIL
python3 "$R" schema
```

`--registry PATH` or `$ASSET_REGISTRY` overrides the default location; the default is found
by walking up to `project.godot`.
