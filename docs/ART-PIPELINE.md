# The art pipeline

How the three production skills — `art-direction`, `asset-builder`, `asset-review` — turn a
game concept into game-ready Godot assets without ever depending on conversation memory.

```
CONCEPT → QUESTIONS → DECISIONS → PLAN → BLOCKOUT → VALIDATE → BUILD → REVIEW → INTEGRATE → RECORD → ITERATE
```

Not: prompt → generate a random asset → hope it fits.

## The files

All in the game project, beside `design-record`'s files:

| File | Owner | Holds |
|---|---|---|
| `docs/design/GAME.md` | `design-record` | vision, pillars, mechanics, MVP scope — the concept every visual decision serves |
| `docs/design/DECISIONS.md` | `design-record` | why things are the way they are; `DD-NNN` ids that specs and the bible cite |
| `docs/design/ART-BIBLE.md` | `art-direction` | the visual source of truth — one section per direction area, each with a lock level |
| `docs/design/PRODUCTION.md` | `art-direction` | phases with checkpoints, reusable systems, production method per category (write-plan skeleton) |
| `docs/design/asset-registry.json` | all three, via `registry.py` | every asset's status, review state, spec, files, generation metadata, dependencies, history |
| `docs/design/specs/<ID>.md` | `art-direction` | optional design page for hero assets |
| `HANDOFF.md` | `session-handoff` | unchanged — the session snapshot |

`skills/art-direction/scripts/registry.py` is the one tool. `status` orients a session in
fifteen lines; `list`, `show`, `deps` answer "what still needs building / what exists / what is
approved / what was rejected / which version is authoritative / which files belong to it / what
depends on it / which phase is incomplete". Every change appends to history; nothing is deleted.

## The lifecycle

```
PLANNED → CONCEPT → BLOCKOUT → PRODUCTION → INTEGRATED → VALIDATED
                                    ▲              │
                                    └── REWORK ◄───┘
          any stage ──→ REJECTED / SUPERSEDED   (kept; superseded_by names the live one)
```

`review: none | pending | approved` is the human's sign-off on the *current* stage's output.
Three gates are enforced by the tool, not by prose:

- a `hero` asset does not enter PRODUCTION until its CONCEPT is approved;
- a `blockout` asset does not enter PRODUCTION until its BLOCKOUT is approved (walked in-game);
- `VALIDATED` is set only by `asset-review`'s `verdict pass` — never by the builder.

`--force --note "why"` bypasses a gate and stamps `FORCED:` in the history for the reviewer.

## Nine worked examples

### 1. Starting design discovery for a brand-new game

> "I have a concept for a 4-player co-op horror-comedy in a mansion. Let's design how it looks."

`art-direction` reads `GAME.md` (or asks for the concept paragraph and offers to write it via
`design-record`), finds no bible or registry, and starts at the top of the spine:

> **Decision — visual production direction.** We need this first because it determines asset
> complexity, animation cost, lighting, and how recognisable the game is.
> **A. Full 3D (recommended)** — you have physics props, first-person interaction, and
> ragdoll comedy; all three want a 3D world … **B. 2.5D** … **C. 2D** …
> Pick one, change one, or say "let's talk".

One decision per turn: 3D → stylised low-poly → short exaggerated proportions → value-first
palette with a warm "grabbable" accent → … When the bar for a *reference board* is reached it
says so and offers to produce it instead of asking the next question. It writes
`ART-BIBLE.md` (sections at PROVISIONAL/EXPLORING/UNKNOWN), `PRODUCTION.md` with phases shaped
to this game, `DD-001…` in `DECISIONS.md`, and `registry.py init` + the Phase 0/1 entries.

### 2. Continuing an existing game's art production

> "Let's keep going on the mansion art."

Any of the three skills runs `registry.py status` first:

```
Registry docs/design/asset-registry.json — 23 assets (Manor Mayhem)
Docs: GAME.md ✓ · DECISIONS.md ✓ · ART-BIBLE.md ✓ · PRODUCTION.md ✓
PRODUCTION.md says current phase: 1
Phase 0 — 4/4 validated: 4 VALIDATED
Phase 1 — 3/9 validated: 2 PLANNED, 3 BLOCKOUT, 1 REWORK, 3 VALIDATED  <- lowest incomplete phase
Awaiting your review (2): ENV_ROOM_DINING_01 [BLOCKOUT], CREATURE_STALKER_01 [CONCEPT]
Rework (1): ENV_PROP_DINING_CHAIR_01 — 1 pivot at centre; 2 trimesh col on rigid body
```

The recommendation follows from the output: walk the two blockouts awaiting approval, then
fix the chair. No question already answered gets asked again.

### 3. Requesting one custom asset

> "Make a grandfather clock for the hallway."

`asset-builder`: no entry exists; it is a small prop implied by the plan's prop family, so it
adds `ENV_PROP_GRANDFATHER_CLOCK_01` inheriting the mansion props' spec (kit, master wood
material, exaggerated proportions per DD-004), asks the one thing it cannot infer — decorative
or physics-enabled? — and, because "the players fight with furniture" is a pillar, recommends
physics with `blockout: true`. It builds the blockout by script, requests the walk-through,
and stops there: PRODUCTION is gated on the approval.

### 4. Building a whole phase

> "Build Phase 1."

`asset-builder` lists phase 1, orders by dependencies (`KIT_MANSION_MODULAR` and
`CMP_GRABBABLE` first, pieces after), builds each blockout by script, verifies headless after
each, records files and statuses, and stops at the checkpoint the plan names — the user's
walk-through. The report lists what was produced, what awaits review, what could not be done
with the tools present (e.g. no Blender: the kit export is specced, entry stays PRODUCTION),
and the next action.

### 5. Replacing an existing asset

> "The stalker's arms should be longer, but keep the front silhouette."

Not an overwrite. `asset-builder` runs `supersede CREATURE_STALKER_01 CREATURE_STALKER_02
--note "longer arms; front silhouette unchanged (DD-009)"`. v1 becomes SUPERSEDED with its
files intact; v2 inherits the spec, starts PLANNED, and — being a hero — goes through CONCEPT
approval again. `registry.py deps` lists what pointed at v1 so the references get repointed
deliberately. Three weeks later, `show CREATURE_STALKER_01` says `SUPERSEDED BY:
CREATURE_STALKER_02 <- use that one`.

### 6. Rejecting a generated concept

> "No — concept B looks like a generic zombie. Kill it."

`registry.py set CONCEPT_STALKER_B REJECTED --note "generic zombie read; fails pillar
'every creature is a specific joke'"`. The prompt, model, and seed stay on its file entry, so
next month's session does not regenerate the same thing. If the rejection reveals a *rule*
("no bare humanoid creatures"), `art-direction` records it as a `DD-` entry and adds it to the
bible's creature section.

### 7. Changing a global art-direction decision

> "Actually, let's make the whole game darker and more serious."

`art-direction` treats this as reopening LOCKED/APPROVED sections and says what it costs:

> This reverses DD-002 (comedy-forward palette) and touches DD-004 (exaggerated proportions
> exist for comedy). It reopens 6 VALIDATED props and the approved player concept.
> **A. Keep the direction; darken the lighting recipe only (recommended)** — mood shifts,
> nothing reopens … **B. Change palette, keep proportions** — reopens the 6 props' materials …
> **C. Full pivot** — a new visual prototype before anything else …

Whatever is chosen becomes a new `DD-` entry with "supersedes DD-002", the bible sections
change with their lock level dropped to PROVISIONAL, and affected entries get `set … REWORK`
with the decision cited.

### 8. Reviewing an asset before Godot integration

> "Review the dining chair before we integrate it."

`asset-review` — ideally in a session that did not build it — reads the spec, the bible
sections, and DD-004; runs `inspect-gltf.py dining_chair.glb --budget 1500 --expect-height 0.9`;
reads the wrapper `.tscn`; runs the headless load. Report: ranked findings with evidence tier,
what passes, what only the user can judge in-game. Then `verdict … fail --note "…"` (→ REWORK)
or `verdict … pass` (→ VALIDATED). It does not fix anything itself.

### 9. Continuing after several days in a new Claude session

> "Continue with the game design."

A fresh session with no memory of any conversation reads the five files and runs `status`.
Its first message is the orientation, not a question:

> Manor Mayhem — 4-player co-op horror-comedy in a mansion (GAME.md). Direction: stylised
> low-poly, short exaggerated proportions, value-first palette with a warm grab accent — bible
> sections APPROVED after the visual prototype on 2026-09-14 (DD-001…DD-011). Phase 2 (visual
> prototype) is complete; Phase 3 (core production kit) is open: kit 6/9 pieces INTEGRATED,
> master materials VALIDATED, `SHADER_DISSOLVE_01` in REWORK (particle count over budget).
> Two hero concepts await your approval: `CREATURE_BUTLER_01`, `ENV_ROOM_LIBRARY_01`.
> **Recommended next:** approve or send back the two concepts (they gate Phase 4 content),
> then let the builder finish the three kit pieces. Want to start with the butler?

## The critical success test

Three prompts a fresh session must handle from state alone:

- **"Continue with the game design."** → orientation + recommended next action (example 9).
- **"Let's design the first monster."** → `art-direction` reads the game, the bible, and the
  monster's gameplay role; asks only the unresolved rungs (silhouette vs player, locomotion
  family, state list, hit/death treatment, VFX hooks); writes the spec and `DD-` entries;
  adds a `--hero` entry; hands off with `Read the spec for CREATURE_… and build its concept stage.`
- **"Build it."** → `asset-builder` resolves "it" from the session or the registry
  (approved-at-current-stage entries in the lowest open phase), reads the spec, checks the bible
  and decisions for conflicts, picks the method, builds what the tools allow, records files and
  status, verifies headless, and reports what exists and what still needs a human look.

## Honesty rules the pipeline keeps

- A file existing is not an asset existing; `INTEGRATED` requires the type's checklist.
- A written spec or a prompt package is not a concept; status says what is actually there.
- The builder never sets VALIDATED; the reviewer never edits the asset.
- Taste — funny, scary, appealing — is a human call, recorded with `review approve`.
- The user can override any gate and any recommendation; the override is recorded, once, with
  its risk, and is not re-argued next session.
