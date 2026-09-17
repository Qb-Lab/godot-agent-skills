# Visual concept exploration — procedure

Five images, one scene, five directions. The user looks at them and answers the question
the grill cannot answer in words: **"what should this game actually look like?"** This is a
design-decision tool, not decoration; every image tests a real art-direction choice, and the
outcome is recorded so no later session re-asks it.

## When to run it — and when not to

Run it when all of these are true:

- `GAME.md` exists and the emotional target and "what the player must read instantly" are
  written down (discovery map, rung 0);
- dimensionality and camera are decided (rung 1) — or perspective is *explicitly* the thing
  being explored, in which case say so and vary only that;
- the fidelity / style-family question (rung 2) has been asked, the user has approved a main
  direction at PROVISIONAL — or has said "show me" instead of choosing;
- the player scale and the proportion family are at least EXPLORING (rung 3), so every image
  can show the same character against the same door;
- `ART-BIBLE.md` exists as a draft, even with most sections UNKNOWN;
- one representative environment, one representative character or creature, and one
  gameplay moment can be named from `GAME.md`'s loop.

Do **not** run it while a question that changes what the images would show is still open —
first-person vs third-person, 2D vs 3D, whether the game is horror or comedy. Generating
polished concepts on top of an unresolved fork wastes the round and anchors the user on
images that will have to be thrown away. Ask that question first; say that is why.

Do not run it for a game whose direction is already APPROVED or LOCKED unless the user is
deliberately reopening it (`DD-` entry, and say what it reopens).

## Check the image tooling first

Image generation depends on what the host session exposes — an MCP tool, an API the user
configured, or nothing. Check the tools available; never assume, never pretend. Record the
answer in `PRODUCTION.md → Direction & constraints → Tools available`.

If no image generation is available: say so in one line and offer the two honest
substitutes — the user enables a tool and you continue; or you write the five **prompt
packages** (scene brief + direction block + negative prompt, ready to paste) and the user
generates them elsewhere, drops the results into `art/concepts/visual-target/`, and you run
the comparison on those files. A written reference board is a fallback for *exploration*,
not a replacement for this phase — the phase exists because words were not enough.

## 1. Fix the comparison scene

Before choosing directions, write the **scene brief** — the constants every image shares so
the user compares art direction, not five unrelated pictures. One short block:

- **Camera** — exactly the player's view: perspective, FOV or orthographic size, eye height
  or camera distance and angle, aspect ratio of the target display. No cinematic angles the
  game cannot produce.
- **Location** — one representative space from the loop (the dining room; the first forest
  clearing; the arena's main lane), with its key architecture.
- **Player position and action** — where the player stands and what they are doing (in
  first-person: what the hands hold).
- **The other body** — the representative character or creature, its position, and its
  state (idle, alert, mid-attack) — the state the player most needs to read.
- **Gameplay moment** — the beat that the image freezes; one sentence.
- **Interactive elements in shot** — one or two objects the gameplay hinges on (the
  grabbable chair, the door, the pickup), so readability rules get tested.
- **Light source and time** — the scene's key light, stated as *what* not *how* (moonlight
  through a window; a single overhead lamp; midday sun) — the *treatment* varies per concept.
- **HUD** — none, unless the UI direction is already decided as diegetic; the HUD is a UI
  decision and would otherwise dominate the comparison.

Per camera type the brief must produce:

| Game | The image is |
|---|---|
| 2D | a representative gameplay scene at the game's native camera framing and tile/sprite scale |
| 3D first-person | something close to an in-game screenshot: hands or held object in frame, real eye height and FOV |
| 3D third-person | the player character in the gameplay environment at the real camera distance and angle |
| Top-down / isometric | a representative gameplay area at the actual camera angle and zoom, with the player and threat in it |
| Side-scrolling / 2.5D | the play plane at gameplay zoom, with parallax depth as the game would render it |

If the concept can only be exciting from an angle the game never shows, that is a finding
about the direction, not a licence to cheat the camera.

## 2. Choose the five directions

Each concept is a **plausible production direction for this actual game** — one a small
team could actually ship in Godot with the tools recorded in `PRODUCTION.md`. Curate; do
not roll dice. Derive the five from the concept the same way the grill derives options:
"how does this serve the game?" must have an answer for each. Typical axes to draw from —
*never* the same list every time:

stylised low-poly · painterly · darker / horror-leaning · more colourful / arcade ·
grounded / semi-realistic · retro / PSX / pixel · exaggerated / cartoon · minimalist /
flat · cinematic / high-contrast · hand-painted / stylised PBR · toon / cel-shaded ·
paper / cutout · graphic / poster-flat

A good five covers the *tensions in the concept*: for a horror-comedy, how far toward
dread vs how far toward cartoon; for a competitive game, how much atmosphere before
readability suffers; for a cosy game, how much detail before production cost explodes. One
concept should be the recommendation from the grill; at least one should deliberately push
past what the user said they wanted, because seeing the edge is how people find the middle.
Two concepts that would look alike at gameplay distance are one concept — replace one.

What varies between concepts: materials, lighting treatment, palette, geometry style and
density, rendering style (shading, outlines, texture resolution), character exaggeration,
VFX style, atmosphere and post-processing.
What does not: the scene brief. Same room, same creature, same moment, same composition.

Name each concept by its direction, not a letter alone — "Concept B — Painterly Dark
Fantasy" — so the names survive into the decision log.

## 3. Announce the line-up, then generate

Before generating, one short block (not a page): for each of the five — the direction in a
phrase, and the one reason it is worth testing for *this* game — then which one you
currently recommend and why, in two sentences. Then generate one image per concept. Do not
ask for permission to generate unless the user has asked to approve line-ups first or the
session's tooling makes each image expensive.

**Prompt assembly.** Each prompt is the same scene brief with a different direction block:

```
[camera block]      first-person, eye height 1.25 m, 80° FOV, 16:9, in-game screenshot framing
[scene brief]       Victorian dining room, long table, moonlight through tall window camera-left;
                    player's hands hold a wooden chair mid-swing; a tall thin stalker creature
                    at the far door, alert pose, about to lunge; a candelabra on the table;
                    no HUD, no text
[direction block]   stylised low-poly, flat-shaded chunky forms, gradient ambient, warm accent
                    on grabbable objects, cool moonlight with a single warm fill, short-proportion
                    creature with an oversized head, soft bloom, minimal particles
[readability]       creature silhouette clearly separated from the background; the chair reads as
                    holdable; the door reads as an exit
[negative]          marketing poster, splash art, character portrait, letterbox, text, logo,
                    watermark, UI overlay, photo-realism (unless the concept is realism)
```

Quality target in words the tool understands: "gameplay concept art", "vertical slice
visual target", "in-game screenshot". Refuse the register of key art, cinematic splash, and
isolated portraits — unless the user explicitly asks for that.

**Files.** Save to `art/concepts/visual-target/r<round>_<letter>_<direction-slug>.png`. Then
record each as a registry entry (type `concept`, phase 0, status `CONCEPT`) with the file
and its generation metadata — tool, model, full prompt, negative prompt, seed, any reference
image — so any concept can be reproduced, iterated, or proven rejected next month:

```bash
R="$SKILL_DIR/scripts/registry.py"
python3 "$R" add CONCEPT_VISUAL_R1_A --type concept --phase 0 --name "R1 A — Stylised Low-Poly Horror" \
        --purpose "Visual-target candidate, round 1" --spec-field direction="stylised low-poly, …" \
        --spec-field scene="dining room / chair swing / stalker at door" --decision DD-002
python3 "$R" set CONCEPT_VISUAL_R1_A CONCEPT --note "generated"
python3 "$R" file CONCEPT_VISUAL_R1_A art/concepts/visual-target/r1_a_stylised-low-poly.png --kind concept \
        --tool "<tool>" --model "<model>" --prompt "…" --negative-prompt "…" --seed 184223
```

Show the images to the user (attach or link the paths; on a remote session send the files).

## 4. Compare — and do not choose for them

After the five exist, one structured card per concept, in the order generated:

```markdown
### Concept B — Painterly Dark Fantasy
**Strengths:** the moonlight reads as mood without hiding the creature; the brush texture
forgives geometry roughness, which suits generated and kit-built assets.
**Weaknesses:** painted textures are the hardest thing to keep consistent across a hundred
props without one painter; the chair's grabbable accent is lost in the palette.
**Production cost:** Medium–High (unique painted textures per family; master materials help less).
**Godot suitability:** good — StandardMaterial3D with painted albedo, low shader cost; needs
a texture-consistency review step in `asset-review`.
**Best for:** a game that sells on atmosphere and whose team has one strong texture painter.
```

Strengths and weaknesses are judged against the game's pillars, the readability list from
rung 0, the production tools and team in `PRODUCTION.md`, and the discovery map's cost notes.
"Looks nice" is not a strength; "the attack windup is readable from the far door" is.
Production cost is Low / Medium / High for *this* team; Godot suitability names the concrete
rendering path (shaders needed, lighting mode, material strategy) and any Godot-specific
cost (e.g. cel outlines need a post pass; PSX wobble is one vertex shader; painterly PBR
means large textures and a consistency problem).

Then the recommendation, once, in the grill's shape: *"Based on the game's concept,
production scope, gameplay readability, and team size, I recommend Concept C — because …"*
Then the doors, all of them open:

- choose one;
- combine aspects — "B's lighting, D's characters";
- modify one — "C but warmer";
- reject all — say what was missing so round 2 does not repeat it;
- another round — broader, or on a different scene;
- more variations of one concept.

Never promote anything on the strength of your own recommendation. Taste is the user's.

## 5. Refine — rounds, not restarts

When the user combines or modifies, **do not regenerate from scratch**. Build the refined
direction block from the named parts — Concept B's lighting treatment, Concept D's character
proportions, the approved environment direction, the existing gameplay constraints — keep
the scene brief identical, and generate the new samples. Round 2 is narrower (2–3 images),
round 3 is a final target (1–2 images, optionally a second scene to prove the direction
survives a different location).

Record the lineage in the refined entry's spec — which trait came from which parent — not
in `depends_on` (that is a *build* dependency, and a parent that is later rejected would
show the child as blocked):

```bash
python3 "$R" add CONCEPT_VISUAL_R2_A --type concept --phase 0 --name "R2 A — B lighting + D characters" \
        --spec-field borrowed="lighting: CONCEPT_VISUAL_R1_B; character proportions: CONCEPT_VISUAL_R1_D; environment: approved direction" \
        --spec-field scene="<same scene brief>"
python3 "$R" supersede CONCEPT_VISUAL_R1_B CONCEPT_VISUAL_R2_A --note "folded into R2 A (lighting)"
python3 "$R" supersede CONCEPT_VISUAL_R1_D CONCEPT_VISUAL_R2_A --note "folded into R2 A (characters)"
```

Parents the user drew from are `SUPERSEDED` by the refined entry (their `superseded_by`
points at it). Concepts the user rejects get `set … REJECTED --note "<their reason>"`; their
prompt and seed stay on the file, so the same thing is not generated again next month.

Stop at three rounds by default. If the user is still undecided after round 3, the
remaining difference is taste, not information — say so, lay the finalists side by side,
and ask them to pick one or park the choice with a named revisit condition. Do not run
round 4 to avoid a decision.

## 6. Persist the approval

When the user says "this one", record it everywhere a later session will look — and nowhere
twice:

1. **Registry** — `review CONCEPT_VISUAL_R2_A approve`; the winner is the authoritative
   visual target. Add the user's notes with `note`. Every rejected sibling is `REJECTED`
   with the reason; every superseded one points at the winner.
2. **`DECISIONS.md`** — one `DD-` entry: *Visual target: Concept … (R2 A)*, with the
   rejected concepts as the alternatives (each with the reason), the borrowed traits, the
   user's notes, and the revisit condition (normally: the visual prototype fails in-game).
3. **`ART-BIBLE.md → Visual concept exploration`** — the short section from the template:
   approved concept id and image path, the borrowed traits, rounds run, status. Then update
   the sections the image settles — *Visual direction*, *Visual pillars*, *Colour*,
   *Lighting*, *Shape language*, *Materials* as far as the image shows them — and promote
   them to `APPROVED`, citing the `DD-`. This is the "Art Bible lock" in the pipeline's
   flow: the direction is approved on real output. `LOCKED` proper still comes after the
   visual prototype, because an image is not the game in motion.
4. **`PRODUCTION.md`** — Phase 0's checkpoint line, and the visual-prototype phase now names
   the approved target as its reference.

A fresh session must be able to answer, from files alone: which concept was approved, which
were rejected and why, which traits were borrowed from which concept, where the images and
prompts are, and whether the direction is approved or still exploring.

Then hand off: the visual prototype (`asset-builder`) builds the representative
environment, character, and creature *to the approved target*, and `asset-review` judges
them against the image and the bible sections it promoted.
