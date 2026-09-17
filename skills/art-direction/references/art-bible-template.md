# Art Bible — template and guidance

`docs/design/ART-BIBLE.md` is the visual source of truth. Rules, not prose: a builder or a
reviewer must be able to check an asset against a section in under a minute. Every section
carries a lock level and cites the `DD-` entries behind it. Sections the game does not need
are deleted, not left as "N/A". Keep it under about three pages; when it grows past that,
detail belongs in a hero asset's `specs/<ID>.md`, not here.

Lock levels: `UNKNOWN` · `EXPLORING` · `PROVISIONAL` · `APPROVED` · `LOCKED`. Promote on
approved *output* (a board, a blockout walked in-game, a visual prototype), never on talk.
Changing an APPROVED or LOCKED section needs a new `DD-` entry and a note of which assets
it reopens.

```markdown
# <Game> — Art Bible

Read `GAME.md` first: every rule here exists to serve the concept there.
Lock levels: UNKNOWN · EXPLORING · PROVISIONAL · APPROVED · LOCKED — promoted on approved output only.
Last reviewed: YYYY-MM-DD

## Visual direction  [PROVISIONAL · DD-001, DD-002]
One paragraph: the look in a sentence, the three references it takes from (and what it
rejects from each), and the one-line answer to "how does this support the game".

## Visual concept exploration  [APPROVED · DD-005]
Approved target: `CONCEPT_VISUAL_R2_A` — `art/concepts/visual-target/r2_a_lowpoly-moonlit.png`
(R1 B lighting + R1 D character proportions on the R1 A environment). Rounds: 2 (5 + 3 images).
Rejected: R1 C (PSX — killed facial reads), R1 E (semi-realistic — cost, generated-asset drift);
reasons on the registry entries. Status: approved 2026-09-02; revisit if the visual prototype
fails in-game. The image is the reference every visual-prototype asset is judged against.
While exploring: list the round, the candidates, and what is still undecided — then delete
this note when a target is approved. Delete the section if the direction was approved
without an exploration.

## Visual pillars  [PROVISIONAL]
2–4 rules every asset must obey. "Readable at 20 m under one key light." "Everything the
player can grab has a warm accent." "Nothing is straight — every edge leans." If an asset
serves none of these, it is off-style regardless of quality.

## Dimensionality, camera & scale  [APPROVED · DD-003]
- 3D, first-person, 1 unit = 1 m. Player capsule 1.4 m × 0.5 m (short proportions, DD-004).
- Door 2.0 × 0.9 m · corridor ≥ 1.4 m · ceiling 2.8–3.6 m · step 0.17 m · counter height 0.85 m
- Camera: FOV 80°, eye height 1.25 m, bob amplitude ≤ 2 cm (motion-sickness option to disable)

## Shape language & proportions  [PROVISIONAL]
Player/NPC: heads, silhouette rule, what carries emotion (face / body / hands).
Creatures: how they contrast the player in silhouette. Exaggeration rules and limits.

## Colour  [PROVISIONAL]
Palette strategy (value-first / role-coded / naturalistic), the role hues if any
(interactive, danger, ally, neutral), saturation limits, and the contrast rule for
gameplay-critical objects. Exact values live in `res://art/palette.tres` or a swatch image
once tuned — link, don't paste dozens of hexes.

## Lighting  [EXPLORING]
Baked / realtime / hybrid; light count per scene; how dark is allowed (min luminance of
walkable floor); the mood recipe (key, fill, rim, fog); what lighting must never hide.

## Materials & textures  [EXPLORING]
Master materials and their parameters; trim sheet(s) and atlas plan; texture sizes per
category; roughness/metallic conventions; how wear and damage are expressed (material
parameter / decal / variant mesh).

## Characters  [EXPLORING]
Rules the player and NPCs obey: proportions, face rules, clothing complexity, how players
tell each other apart, customisation scope. Point at `specs/CHAR_PLAYER_01.md` for detail.

## Creatures & enemies  [UNKNOWN]
Readability rules: threat by silhouette, state by pose/colour/emission, attack windup
visibility. Locomotion families in use. Hit/death treatment (ragdoll / authored / dissolve).

## Environments  [EXPLORING]
Kit or unique; grid and pivot conventions; architecture language; prop density targets
(props per m² or per room); environmental storytelling rules; destruction and physics
scope; navigation constraints (what NavigationMesh must reach).

## Props  [EXPLORING]
Categories in use (decorative / interactive / pick-up / physics / breakable / animated /
replicated) and what each requires; mass ranges; what can be carried, thrown, stacked;
the breakable strategy.

## Motion  [EXPLORING]
Skeletal / procedural / physics mix; the authored animation set per character class;
IK needs; ragdoll rules; secondary motion in scope; camera motion rules; environmental
motion (all shader-driven unless stated).

## Technical art & VFX  [EXPLORING]
Shader-owned effects (water, fire, fog, dissolve, outlines…); particle budget per effect
class; post-processing stack; the "VFX not geometry / shader not texture" calls.

## UI  [UNKNOWN]
Diegetic / screen-space; HUD information budget; typography and minimum sizes; icon
language; how menus relate to the world's materials.

## Performance targets  [PROVISIONAL]
Platform floor and frame rate; tri budgets per category; texture sizes and count; draw-call
ceiling; LOD policy; shader and particle ceilings; max instances of the most repeated asset.

## Naming & files  [APPROVED]
Registry ids: `CATEGORY_NAME_NN`. Source art in `art/source/<category>/` (with `.gdignore`);
game-ready in `res://assets/<category>/`; scene wrappers beside their meshes; materials in
`res://assets/materials/`; shaders in `res://assets/shaders/`. Node and file names snake_case
or PascalCase per the project's existing convention — say which.

## Human calls
Which decisions are reserved for the user's taste (main character face, palette accents,
final creature look) and which are batch-approved.
```

## Writing guidance

- Start the file at the first PROVISIONAL decision, not when everything is known. An Art
  Bible with six UNKNOWN sections is honest; no Art Bible is how assets drift.
- The visual concept exploration (`concept-exploration.md`) is what promotes *Visual
  direction*, *Visual pillars*, *Colour*, *Lighting*, *Shape language*, and *Materials* from
  PROVISIONAL to APPROVED — as far as the approved image actually shows them. The section
  above stays short: ids, paths, borrowed traits, status. Reasons and rejected alternatives
  live in the `DD-` entry and on the registry entries, not here.
- A rule is checkable: "warm accent on grabbable props" can be reviewed; "cohesive" cannot.
- Every section answers "how does this support the game" in one clause. If it can't, the
  rule is taste, and taste goes in *Human calls*.
- When a rule changes, change it here and add the `DD-` entry with what it reopens. Never
  let a spec or a builder's note carry a rule the bible contradicts.
