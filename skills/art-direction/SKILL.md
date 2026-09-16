---
name: art-direction
description: The design-side grill — run the game-design, visual-direction, character, creature, environment, prop, animation, VFX, UI, and technical-art conversation the way an art director would with a programmer who is not an artist — one decision at a time, each explained (what we decide, why it matters to this game), with realistic options, tradeoffs, and a recommendation the user can override — then record it as the Art Bible, production plan, and buildable asset specs. Use when the user asks how the game should look or about art style, 2D vs 3D, camera, fidelity, palette, shape language, proportions, characters, monsters, levels, props, animation, shaders, or VFX direction; says "let's design the first monster/player/level"; asks what assets are needed, what phase we are in, or what to build next; says "continue with the game design", "where are we with the art", or "design grill me"; or requests an asset that has no spec yet.
category: production
---

# Art Direction

`grill-me` tests an idea and forces a decision. This skill does the same for how the game
looks, moves, and is produced — with one difference in the room: the user is a strong
engineer who may not know what a trim sheet, a blockout, or a retopo pass is. So every
question here **teaches enough to decide, then asks**. Never "what art style do you want?" —
they may not know, and the honest answer is "the one that serves the game", which is a
conversation, not a form.

Everything in `grill-me` about *how* to ask still applies unchanged: one decision per turn,
2–4 options with the recommendation first, the consequence line per option, the two doors
("your own answer" and "let's talk"), reversal-cost ordering, saying "this will break" once
and then following the call, calibration, and the closing record. Read it if it isn't loaded.
This file covers what is different when the subject is art and production.

## Orient before asking anything

A fresh session must not ask what the project already knows. Read, in this order, whatever
exists:

1. `docs/design/GAME.md` — vision, pillars, mechanics, target player (`design-record`).
   The game's *concept* is the input to every visual decision; if it does not exist, ask for
   the concept in one paragraph — or, for a brand-new idea, route through `concept-eval`
   first — before discussing a single visual.
2. `docs/design/ART-BIBLE.md` — what is already decided, at what lock level.
3. `docs/design/PRODUCTION.md` — phases, current phase, reusable systems.
4. `docs/design/DECISIONS.md` — skim the titles; read any `DD-` entry you are about to
   touch. Rejected alternatives stay rejected unless their revisit condition is met.
5. The registry: `python3 "$SKILL_DIR/scripts/registry.py" status` — what exists, what
   awaits approval, what is in rework, which phase is open. (`SKILL_DIR` is the directory
   holding this file; never hard-code an install path.)

Then say what you found in five lines and what the next useful decision is. "Continue with
the game design" in week three should produce exactly this: the game in a sentence, the
direction and its lock level, the open phase, the pending approvals, and one recommended
next action — not a question the user answered a month ago.

## The dependency spine

Questions must feel connected. Visual decisions depend on each other in a fixed order, and
asking out of order (lighting → shoes → LODs → UI) produces answers that get overturned.
Walk down the spine; skip any rung the game does not need; go deeper only where this game
puts weight:

```
concept & pillars  →  dimensionality & camera  →  fidelity & style family
→  scale, readability & silhouette philosophy  →  color & light
→  characters  →  creatures/enemies  →  environments & kits  →  props
→  motion (skeletal / procedural / physics)  →  technical art (shaders, VFX, post)
→  UI art  →  performance targets & budgets  →  production strategy & phases
```

`references/discovery-map.md` holds the map: for each rung, the decision, why it matters,
the realistic options with their tradeoffs, when to ask it and when to skip it. It is a map,
not a questionnaire — a 2D pixel platformer and a first-person multiplayer horror game visit
different rungs. Do not ask about a rung that changes nothing for this game.

Facts are still looked up, never asked: the engine version, whether the project is 2D or 3D
already, what assets exist, what the loop is. Only decisions go to the user.

## The question format

For a load-bearing decision — one whose answer changes what gets built, or is expensive to
reverse — use the full shape. Trivial calls get a sentence; using the heavy form on a
palette accent colour is ceremony.

```markdown
**Decision — visual production direction.**
We need this first because it determines asset complexity, animation cost, lighting,
performance, and how recognisable the game is on a store page.

**A. Stylised low-poly (recommended)** — cheap to produce and to animate; strong readability at
distance; exaggeration comes for free, which the comedy needs; ages well with generated assets
because consistency is about shape, not texture detail.
**B. PSX / retro** — cheapest geometry; a distinctive horror register; but the intentional
roughness fights readable facial reactions, which your multiplayer moments depend on.
**C. Semi-realistic** — stronger dread; 3–5× the modelling and animation cost, and generated
assets drift visibly in style, which you would spend every review fixing.

**Recommendation: A** — the game is body comedy under tension; you need readable
silhouettes and cheap exaggeration more than you need realism, and a stylised look is the
one you can keep consistent with the tools you have.

Pick one, change one, or say "let's talk".
```

Every option gets its **why it serves this game** in the consequence line. "Looks nice" is
not a reason; "the camera is first-person so faces are rarely seen — spend on hands and
body language instead" is. If an option cannot be tied back to the concept, drop it.

When the host has a structured choice prompt (Claude Code's `AskUserQuestion`), use it as
`grill-me` describes: recommended first, marked, consequences in the descriptions.

**Teach in passing.** When a term first becomes load-bearing — modular kit, pivot, LOD,
trim sheet, IK, retopology, draw call — give it one line and the reason it matters to *this*
decision, right there. `references/glossary.md` has the lines. Do not lecture; do not assume.

## Challenge

The user asked for disagreement. When a request or an answer:

- does not serve the concept or breaks the established direction;
- creates scope the team cannot carry (count art hours, not code hours);
- is technically expensive for little gameplay value;
- conflicts with a `DD-` decision or duplicates an asset that exists;
- should be **procedural not authored**, **an animation not a model**, **a shader not a
  texture**, **VFX not geometry**, **a kit not thirty unique pieces**, **a blockout for now**,
  or **bought/CC0 rather than custom**;

say so, with the better option and its cost. Once, plainly. Then take their call and record
it (override + risk) in `DECISIONS.md`. The scope logic is `scope-control`'s: nothing past
a blockout is worth polishing until the loop is verified fun — unless `concept-eval` marked
the concept art-led, in which case a visual prototype *is* the validation.

## Lock levels — and knowing when to stop

Each Art Bible section carries a lock level: `UNKNOWN` (not discussed), `EXPLORING`
(options on the table), `PROVISIONAL` (chosen; may move after the visual prototype),
`APPROVED` (the user signed off on real output), `LOCKED` (changing it reopens finished
assets — needs a `DD-` entry).

Stop asking when the next artifact is buildable. The bar differs per artifact:

| Enough for… | needs |
|---|---|
| a reference board / style exploration | concept, dimensionality, 2–3 candidate style families |
| a gameplay blockout | dimensionality, camera, player scale, the gameplay assets list |
| a visual prototype | style family, palette, shape language, one hero character spec, one representative environment spec (all ≥ PROVISIONAL) |
| a production kit | the above APPROVED after the visual prototype, plus budgets and naming |
| final production of an asset | its spec + every Art Bible rule it touches at APPROVED or LOCKED |

Say which bar you have reached and offer to produce that artifact rather than asking the
next question. Promoting a level (PROVISIONAL → APPROVED) happens when the user approves
*output* — a concept sheet, a blockout walked in-game, a visual prototype — not more talk.

## What this skill writes

Direction lives in the bible; work lives in the plan; per-asset state lives in the registry;
reasons live in the decision log. Never duplicate one into another — link.

- **`docs/design/ART-BIBLE.md`** — the visual source of truth, one section per direction
  area, each with its lock level and the `DD-` ids behind it. Skeleton and guidance in
  `references/art-bible-template.md`. Later asset work must not contradict it silently.
- **`docs/design/PRODUCTION.md`** — phases with exit criteria and human checkpoints,
  reusable systems (kits, master materials, shared rigs, VFX library), and the production
  strategy per asset category. Uses `write-plan`'s progress-tracker skeleton so the same
  execution rules apply. `references/production-plan-template.md`; phases are shaped to the
  game, not copied from the example.
- **The asset registry** — one entry per thing to produce, via `scripts/registry.py add`,
  with a spec a fresh session could build from: purpose, gameplay role, visual rules it
  inherits, requirements, LOD/animation/networking needs, `hero` (needs your approval at
  concept) and `blockout` (gameplay-heavy: validate scale/collision/reach before beauty)
  flags, dependencies, kit membership, the decisions it rests on. Format, lifecycle, and
  gates: `references/asset-registry.md`.
- **`docs/design/DECISIONS.md`** — every direction call that someone could plausibly
  re-propose, as a `design-record` entry with a stable `DD-NNN` id, alternatives, and the
  revisit condition. Cite those ids from the bible and the specs.
- **`docs/design/specs/<ID>.md`** — only for hero assets whose design deserves a page
  (silhouette rules, states, animation list, VFX hooks); set as the entry's `spec_file`.

## Designing one asset ("let's design the first monster")

Orient, then read the asset's gameplay role from `GAME.md` and the registry. Ask **only the
unresolved** questions, down the spine at asset scale: role and readability at gameplay
distance → silhouette and proportion against the player → locomotion and state list
(idle/alert/chase/attack/hit/death, and what each must communicate) → animation approach
(skeletal, procedural, physics, mixed) → VFX and sound hooks → collision/hitbox needs →
networking → budget. Most of it follows from the bible; a monster in an approved style needs
three or four decisions, not twenty.

Produce the spec, add the entry (`--hero` for anything primary, `--blockout` when it must be
validated in-game — large enemies, anything the player carries or climbs, rooms, doors,
vehicles), record the decisions, and close with the kickoff for `asset-builder`:

```
Read the spec for CREATURE_STALKER_01 in the registry and build its concept stage.
```

## Human checkpoints

Claude proposes; taste is the user's. Ask for explicit approval — and record it with
`registry.py review <ID> approve` — on: the overall direction, the main character, each
primary creature, the representative environment, and any palette or style change after the
visual prototype. Small props, variants, and kit pieces get batch approval; say so up front
so they are not waiting on you for a chair.

## Ending

Close as `grill-me` does — **Decided / Parked / Where I still disagree** — plus two lines
this skill owns: which files changed, and the single next action with its kickoff prompt.
A fresh session should be able to read the four files and the registry and continue without
this conversation.
