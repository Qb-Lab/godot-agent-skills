# Discovery map

The rungs of the dependency spine, top to bottom. Each rung says what is being decided, why it
matters to a game, the realistic options with what they buy and cost, and — most importantly —
**when to ask it and when to skip it**. This is a map for the art director to navigate, not a
questionnaire to administer. Visit only the rungs this game puts weight on; at each rung, ask
only if the answer changes what gets built.

A recommendation is always derived from the concept: read `GAME.md`, then ask of every option
"how does this support the game?" — comedy wants readable exaggeration; horror wants
controlled information; competitive play wants instant read of state; cozy wants softness and
low tension. The concept decides; the options are just the menu.

---

## 0. Game identity (read, rarely ask)

Inputs, not decisions: core fantasy, the loop in one line, emotional target (tension / chaos /
dread / comfort / mastery / laughter), tone (serious ↔ comedic), player count and perspective,
target player and comparables, platform. All of it should be in `GAME.md`; if it is not, get
it in one paragraph and offer to write `GAME.md` via `design-record`. Deep game-design forks
(economy, loop, hook) belong to `grill-me` + `loop-and-economy` + `concept-eval`, not here.

The two identity facts that drive everything below: **what the player must read instantly
during play** (threat, state, affordance, teammates) and **what the game wants the player to
feel**. Write both down before rung 1.

## 1. Dimensionality & camera

**Decide:** 2D, 2.5D (3D world with 2D-style constraints or 2D art in 3D space), or 3D; and
the camera — first-person, third-person, top-down, isometric, side-scrolling, fixed.
**Why it matters:** it sets the entire production pipeline (sprites vs meshes vs both), the
animation method, what the player can see of characters (first-person rarely sees its own
face — spend on hands and body), lighting, and half the performance budget.
**Options:** 2D — cheapest per asset for a solo dev with drawing tools, expensive per
*animation* (every angle hand-drawn), camera options are limited, readability is excellent.
2.5D — 3D lighting and camera freedom with 2D-like control; import pipeline is 3D. 3D — physics,
dynamic camera, one model animates from every angle; needs modelling/rigging pipeline; first
30% of the pipeline is expensive, everything after is cheaper than 2D.
**Ask when:** the concept does not already imply it. **Skip when:** the project already has a
`project.godot` with 2D/3D nodes or `GAME.md` states it. Physics-driven interaction, ragdolls,
free camera, and body comedy push to 3D; hand-crafted feel, tiny team, pixel nostalgia push to 2D.

## 2. Fidelity & style family

**Decide:** the family the look belongs to, and how far along realism it sits.
**Why it matters:** determines asset complexity, animation requirements, how forgiving the
style is of inconsistency (critical with generated assets), lighting model, and recognisability.
**Families (3D):** stylised low-poly (flat or gradient shading, chunky forms — cheapest to
produce and iterate, exaggeration is natural, very consistent); PSX/retro (affine wobble,
vertex lighting, 240p textures — very cheap, strong horror register, deliberately limits
expressiveness); hand-painted/stylised PBR (painted texture detail, moderate cost, needs a
consistent painter — hard with generated textures); toon/cel (outlines and stepped shading —
readable, animation-friendly, needs a shader pass and careful normals); semi-realistic PBR
(strong atmosphere, 3–5× cost, consistency is the daily fight); realistic (inappropriate for
a small team unless the game is *about* realism).
**Families (2D):** pixel art (resolution and palette become hard rules — choose them now);
vector/flat; hand-painted; paper/cutout; mixed 2D-on-3D.
**Ask when:** always — this is the single most consequential art call. Give three options
tied to the concept, recommend one, and expect the user to want to see it: offer a reference
board as the next artifact. **Lock level:** PROVISIONAL until a visual prototype exists.

## 3. Scale, readability & silhouette philosophy

**Decide:** player height and the unit scale (1 unit = 1 m in 3D by default; tile size and
sprite pixel height in 2D), proportion family (realistic 7.5-head, heroic 8-head, stylised 5–6,
chibi 2–3), how strongly silhouettes must differ between factions/roles, and how exaggeration
is used.
**Why it matters:** every environment measurement, door, stair, and camera distance derives
from player scale; silhouette is how players read a threat in 200 ms; proportions decide
whether faces or bodies carry emotion.
**Options:** short/stocky exaggerated proportions — comic, extremely readable in groups,
cheap facial detail because faces are big; realistic — flexible but bland in silhouette, and
realistic humans are the most expensive thing to make convincing; tall/thin — elegant, readable
against stocky enemies, hard to animate well.
**Ask when:** the game has characters the player watches (third-person, multiplayer, any
enemy). **Skip when:** first-person single-player with no visible allies — then decide only
the *enemy* silhouette rule. Multiplayer: silhouettes must differ between players at a glance;
decide whether by shape, colour, or accessory.

## 4. Colour & light

**Decide:** the palette strategy (limited palette with role-coded accents; naturalistic;
monochrome-plus-accent), the lighting philosophy (baked vs realtime, key-light drama vs flat
ambient, how dark is too dark for readability), and contrast rules (gameplay-critical objects
always above N% luminance contrast against their background).
**Why it matters:** colour is the cheapest readability tool — interactive = one hue, danger =
another — and the fastest way to look consistent. Lighting is where horror and mood actually
live, and where performance is lost.
**Options:** value-first palette (decide light/dark first, hue second — robust, reads at any
size); role-coded accents (a hue per gameplay meaning — excellent for multiplayer chaos);
naturalistic (needs strong lighting to read; expensive). Lighting: fully baked (fast, static,
no destruction); realtime with few shadowed lights (flexible, budget the light count);
stylised unlit/flat (cheap, needs the shapes to carry everything).
**Ask when:** always for palette strategy (one question); lighting when the game is 3D or
mood-heavy. Pin exact hex values later — the *rule* is the decision, the values are tuning.

## 5. Characters

**Decide:** proportions (rung 3 applies), what carries emotion (face, body, both), clothing
complexity and silhouette variety, customisation (none / palette swap / modular parts —
modular multiplies rig and clothing work), and the animation approach (rung 9).
**Why it matters:** the player character is the most-seen asset in the game and the one
whose animation set is largest; a decision here fans out into rig, IK, cloth, and every
outfit.
**Options for customisation:** none (cheapest); material/palette swap (near free, enough for
player distinction in co-op); modular attachments — hats, accessories on bone attachment
points (moderate, great for comedy and identity); modular bodies/clothing (rig-heavy,
avoid pre-validation).
**Ask when:** the player is visible or there are NPCs. Multiplayer: how players tell each
other apart is a required decision.

## 6. Creatures & enemies

**Decide:** per creature — its gameplay role and what the player must read (threat level,
state, attack windup, vulnerability), silhouette relative to the player, locomotion (biped,
quadruped, flying, crawling, amorphous — each is a rig and animation family), the state list
and what each state communicates, hit/death reactions (animation, ragdoll, dissolve, VFX),
and whether it interacts with physics objects.
**Why it matters:** enemies are the most expensive content category (model + rig + animation
set + VFX + audio + balancing) and the one players stare at most. A creature whose attack
isn't readable is a design failure no texture can fix.
**Options for hit/death:** ragdoll (physics, cheap once the rig exists, comic or grim
depending on tuning, non-deterministic in multiplayer without care); authored animation
(controlled, expensive per variant); dissolve/VFX (cheap, stylised, hides rig quality).
**Ask when:** designing each creature. **Skip:** never ask about a creature that isn't in the
MVP — `scope-control` cuts it first.

## 7. Environments & kits

**Decide:** modular kit vs unique set pieces (or a kit plus a few hero pieces), indoor vs
outdoor mix, architecture language, grid size and pivot convention for the kit, prop density
targets, environmental storytelling intent, destruction and physics (none / props only /
structural), navigation needs (NavigationMesh? climbing? vertical play?), and the player-scale
rules (door, corridor, ceiling, step heights).
**Why it matters:** a modular kit is the single biggest production multiplier — ten pieces
build a hundred rooms — but only if the grid, pivots, and material sharing are decided before
the first piece. Player scale rules are the blockout's checklist.
**Options:** modular kit (grid-snapped walls/floors/doors/trim — cheap per room, repetitive
without dressing, needs a trim sheet or shared material); unique set pieces (bespoke, memorable,
non-reusable — right for 2–3 signature spaces only); hybrid (kit for 80%, hero pieces where
players linger). Grid: 1 m (flexible, more pieces per room) vs 2 m / 4 m (fast, chunkier, fewer
draw calls). Pivot: back-bottom-left corner for walls (snaps cleanly), centre-bottom for props.
**Ask when:** the game has levels. **Skip:** outdoor-only games skip architecture; a single
arena skips modular.

## 8. Props

**Decide:** the categories that exist (decorative, interactive, pick-up, physics, breakable,
animated, network-replicated, gameplay-critical), the physics rules (mass ranges, what can be
carried, thrown, stacked), the breakable strategy (swap-to-pieces, shader dissolve, none), and
the reuse plan (prop families sharing one material).
**Why it matters:** in a physics or comedy game props *are* the gameplay; in others they are
dressing. The category determines what "done" means — a decorative barrel is a mesh; a
throwable barrel is a mesh, collision, RigidBody3D, mass, material, replication, and a sound.
**Ask when:** the game has interaction with objects. **Skip:** ask about categories, not
individual props — individual props are registry entries later.

## 9. Motion

**Decide:** skeletal animation vs procedural vs physics vs mixed; IK needs (foot placement,
hand-to-object grabbing, look-at); ragdoll and blends; secondary motion (cloth, hair, jiggle —
each a system); camera motion rules (bob, shake, FOV changes — with player-facing intensity
options); environmental motion (wind, water, foliage — shaders, not animation).
**Why it matters:** animation is the largest recurring cost after enemies, and the wrong
approach is the one that scales linearly with content. Procedural and physics motion scale
with *systems*, not assets — a big win for a small team and often funnier or more organic.
**Options:** authored skeletal only (controlled, expensive, brittle with interactions);
procedural-first with a small authored set (locomotion authored, everything reactive
procedural — cheaper, emergent, needs a technical-animation mindset); physics-driven (active
ragdolls — very funny, very emergent, hard to control and to replicate over the network).
**Ask when:** there are animated characters or creatures. Multiplayer changes the answer:
physics motion must be authoritative somewhere.

## 10. Technical art

**Decide:** what needs a shader or a system rather than an asset — water, fire, smoke, fog,
electricity, wind, foliage, dissolve, damage, outlines, screen effects, post-processing — and
the material strategy (a few master materials with parameters vs unique textures per asset;
trim sheets and texture atlases vs unique UVs).
**Why it matters:** technical art is where a small team gets a big-team look — one water
shader serves every puddle; one master wood material with a colour parameter serves every
piece of furniture; a dissolve shader replaces a death animation set. It is also where
performance is won or lost (shader complexity × pixels).
**Options for materials:** master materials + parameters (few textures, consistent, cheap —
the default for stylised); trim sheets (one texture strip shared across a kit — the standard
for modular architecture); unique PBR textures per asset (max fidelity, max cost, the
consistency problem with generated textures).
**Ask when:** the concept names an effect (water, fire, weather) or the style needs a pass
(toon outlines, PSX wobble, pixelation). **Skip:** rung-by-rung shader questions before the
style is PROVISIONAL.

## 11. UI art

**Decide:** diegetic vs screen-space (or mixed), the HUD's information budget (what must be
visible always vs on demand), typography and scale rules for readability at the target
display, icon language, and whether menus share the game's material language or contrast
with it.
**Why it matters:** UI is the asset category most often left to the end and most visible in
every screenshot. Diegetic UI is beautiful and expensive; it also fails on readability for
some players — plan the fallback.
**Ask when:** the UI is more than a health bar and a menu, or the game is horror/immersive
(diegetic is a real fork). **Skip:** detailed icon and menu decisions until the visual
prototype is approved.

## 12. Performance targets & budgets

**Decide:** target hardware and frame rate (the platform floor — Steam Deck? low-end
laptop? phone?), triangle budgets per category (hero character, enemy, prop, kit piece,
scene), texture sizes and count, draw-call ceiling per scene, LOD policy (none until profiled?
two levels for kits?), shader complexity ceiling, particle budgets, and how many instances of
the most-repeated asset appear at once.
**Why it matters:** budgets are the only thing that stops "make it look better" from being
infinite, and they are much cheaper to set before assets exist than to retrofit. They also
tell the builder when a shader must be cheaper or a mesh needs an LOD.
**Options:** conservative first (stylised low-poly on a Steam Deck floor: hero 8–15k tris,
enemy 3–8k, prop 200–1500, kit piece 50–500, 1k–2k textures, draw calls in the low hundreds —
numbers to *tune*, not gospel); generous with LODs (higher budgets, mandatory LOD1/LOD2 —
more work per asset); profile-driven (no budgets until a scene exists — honest, but assets
built before the profile get rebuilt).
**Ask when:** before the production kit phase — earlier if the platform is constrained.
**Skip:** exact numbers before a blockout scene exists to profile; decide the *policy* now.

## 13. Production strategy & phases

**Decide:** for each asset category, the production method (Godot primitives, procedural
geometry, `@tool` scripts, Blender, image generation for concepts, shaders, particles,
CC0/purchased packs, a human artist for taste-critical pieces) and the phases with their
checkpoints. `production-plan-template.md` has the shape; `asset-builder`'s
`references/production-methods.md` has the method tradeoffs.
**Why it matters:** the plan is what lets a fresh session build the right thing next without
re-deriving the conversation, and what keeps beauty after validation, not before.
**Ask:** only the forks the user must own — whether to buy a base kit, whether a human artist
is in the budget for the hero character, and which single environment and creature
represent the visual prototype. Everything else is your recommendation, written down and
overridable.
