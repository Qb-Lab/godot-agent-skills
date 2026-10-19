---
name: steam-store-assets
description: Produce the Steam store assets — capsule art in every required size, the logo treatment, the trailer, the screenshot set, and the embedded gameplay GIFs — from briefs, testing each one at the size players actually see it rather than at full resolution. Use when the user asks to make, fix, or export a capsule, header, library asset, game logo or logotype, store trailer, store screenshots, or an animated gameplay showcase; asks how to stage or capture a screenshot or clip in Godot for the store; says "make the capsule", "cut the trailer", "take the store screenshots", or "this capsule looks AI-generated"; or when the registry holds store assets still to build.
category: production
---

# Steam Store Assets

`asset-builder` makes the things the game is made of. This skill makes the five or six images
and one video that decide whether anyone ever sees them. Same discipline, different failure
mode: an in-game asset fails when it is wrong, a store asset fails when it is *invisible* —
and it fails at 184x69 pixels, in a grid of twelve competitors, on a dark background, three
rows down a page the player is scrolling past.

So the rule that organises everything here: **nothing is judged at the size it was made.**

## Before building anything

```bash
SKILL_DIR="$(cd "$(dirname "<path of this SKILL.md>")" && pwd)"
R="$SKILL_DIR/../art-direction/scripts/registry.py"
python3 "$R" status && python3 "$R" show <ID>
```

Then read `docs/design/STORE.md` (the brief, the funnel status, the asset table),
`docs/design/ART-BIBLE.md` (the capsule has to look like the game — the bible says what the
game looks like), and the `DD-` entries the brief cites. If there is no brief, stop and route
to `steam-store-page`: an asset built without one is a guess that someone will have to
re-make, and capsules are expensive to re-make because the logo is usually baked in.

Confirm the required dimensions against
`$SKILL_DIR/../steam-store-page/references/steam-requirements.md` **and re-read the Steamworks
page it links** before exporting — or, if that sibling skill is not installed, read
<https://partner.steamgames.com/doc/store/assets/standard> directly, which is what the
reference tells you to do anyway. Shipping a 1232x706 crop of something composed for 920x430
is the most common wasted day in this whole pipeline.

## Capsule and logo

The capsule is the whole funnel's gate. `references/capsule.md` holds the craft: composition
for the thumbnail rather than the poster, safe areas and Steam's own overlays, the logo
treatment, the AI-tell checklist, the text rules, and the border experiment.

Three things belong in the SKILL.md because they are decisions, not craft:

**Produce candidates, not a capsule.** Five directions for the same game, the way
`art-direction` runs visual concept exploration — vary the focal subject, the composition, the
colour strategy, the logo placement and the amount of scene; keep the game's actual look fixed.
One should be the brief's recommendation and one should push past it. Say what the five are and
why each is worth testing before generating anything. Each candidate is a registry entry of
type `capsule` with its tool, model, prompt, and seed recorded, so the winner and the losers
both survive the conversation.

**Test the ladder before showing anyone.** Every serious candidate gets rendered at full size,
listing size, 184x69, on dark, blurred, in greyscale, and dropped into a real competitor grid.
`scripts/capsule-check.py` does the mechanical half — dimension and slot check, and it builds
the ladder files for you to actually look at. Judgement on what comes out is still yours and
the user's; the point is that the judgement happens on the right images.

**It has to still be the game.** A capsule that out-promises the screenshots converts into
refunds and "nothing like the trailer" reviews. If the best capsule is better than the game
currently looks, that is a finding for `art-direction`, not a licence to ship it.

`[OFFICIAL]` Base capsules carry game artwork, the game name, and an official subtitle —
nothing else. No review scores, awards, sale copy, calls to action, or other text. Check the
rules page before adding anything clever.

## Trailer

`references/trailer.md` holds the construction method. The shape that matters:

- **Build the timeline before capturing a frame.** A written beat sheet — what each second is
  proving — is what stops a trailer becoming a tour. Thirty to fifty seconds with a cold open,
  four or five gameplay highlights in the first fifteen, short shots, and a wishlist CTA is a
  strong default `[BEST PRACTICE — Valve sets no length limit]`, but the real duration comes
  from how much genuinely compelling material exists. Padding a 25-second game to 50 seconds
  makes a worse trailer, not a longer one.
- **Gameplay over logos, lore, and cinematics.** No long studio logo, no slow fade-in, no
  text-heavy lore intro, no establishing shot before anything happens. The opening has one
  job: answer "what is interesting about this game?" while the viewer's hand is still on the
  mouse.
- **It must work muted.** Most first views have no sound. If the hook needs audio to land,
  the hook is not in the picture yet.
- **Capture in-engine, deterministically.** `references/screenshots.md`'s staging method
  applies to video too — the same setup, the same lighting, a known camera path, debug UI off.
  A trailer cut from clips nobody can re-capture cannot be fixed later.
- `[OFFICIAL]` Export to the documented specs (1080p or 720p, 30/60 fps, 5,000+ Kbps, H.264 +
  AAC, 44/48 kHz), remember the first two trailers appear *before* the screenshots, and budget
  for conversion time — a game cannot release while a trailer is still converting.

Prepare the YouTube-ready version at the same time if the trailer will be distributed there;
it is the same cut with different encode targets, and doing it later means re-finding the
project file.

## Screenshots

`[OFFICIAL]` Minimum five, 1920x1080 or larger, 16:9, gameplay only — menus only if a menu is
genuinely a distinctive component. At least four must be marked suitable for all ages.
Seven-plus is `[BEST PRACTICE]`, not a rule.

The number is the least interesting part. **Every screenshot has a job**, and a set where
three images do the same job is shorter than it looks. Write the narrative first, then capture
to it:

```
01 — Core gameplay          the main thing the player does, unmistakable
02 — Signature mechanic     the one thing no competitor has
03 — Threat / challenge     what can go wrong, so there are stakes
04 — Player interaction     the social or systemic moment
05 — Environment variety    proof the game is not one room
06 — Progression / depth    proof there is a reason to keep playing
07 — High-intensity moment  the clip the player imagines themselves in
```

Adapt it — a management game's narrative is not a horror game's. The first screenshot carries
the most weight: it is the fallback for everyone who did not watch the trailer, so it shows
the core loop or the core fantasy, never a vista.

Each shot gets a staging sheet — purpose, feature demonstrated, location, required setup,
camera, UI, lighting, capture notes — specific enough that a fresh session can reproduce it in
Godot without the conversation. Format and the Godot capture recipes (viewport size overrides,
hiding debug UI, deterministic setup, headless and in-editor capture, batch capture) are in
`references/screenshots.md`.

Keep the UI in when the UI is representative. A screenshot with the HUD stripped out is a
different game than the one being sold, and Valve notes HUD elements are often beneficial.

## Embedded gameplay showcases

The About section's GIFs and clips have one rule, and it is a gate rather than a guideline:

> **What is this proving?**

Core mechanic, movement, combat, physics, multiplayer interaction, building, destruction,
progression, enemy behaviour — one answer per showcase, written down before it is made. If the
answer is "it looks cool when things move", cut it. Motion on a store page costs attention and
page weight, and `[OFFICIAL]` all screenshots and GIFs together must stay under 15 MB, each
image under 5 MB — so every showcase is competing for a real budget.

Two to four is usually right. Keep them textless so localization does not mean re-rendering
`[OFFICIAL — Valve's recommendation]`. The display width that fits the description column is
not documented; render at a sensible width, then check it in the store preview rather than
trusting a number.

## Tools

- `python3 "$SKILL_DIR/scripts/capsule-check.py" <image> [--slot main] [--ladder]` — reads
  PNG/JPEG dimensions and file size with no third-party libraries, matches the image against
  every official Steam slot, reports mismatches and aspect errors, checks the 5 MB limit, and
  with `--ladder` writes the thumbnail ladder (and the greyscale pass) using whatever
  downscaler is on PATH — `sips`, ImageMagick, or `ffmpeg`. Without one it prints the exact
  commands instead of pretending. `--help` for everything.
- `godot --headless --path . --import && godot --headless --path . --quit` — run before a
  capture session, so the scene you are staging is the scene that imports cleanly
  (`godot-verify` reads exit codes honestly).
- Viewing images: look at the files directly when the host allows. If it cannot, say so and
  ask the user to look at the ladder output — **do not describe a capsule you have not seen**,
  and do not approve one from its generation prompt.

## Registry lifecycle

Store assets use the same lifecycle as everything else, read with the same `status` command:

```bash
# --phase is the numbered phase in PRODUCTION.md that the store work sits in.
python3 "$R" add STORE_CAPSULE_MAIN_01 --type capsule --phase 4 --hero \
  --purpose "Main capsule 1232x706 — signature mechanic mid-action per DD-031"
python3 "$R" file STORE_CAPSULE_MAIN_01 art/store/capsule_cand_a.png --kind concept \
  --tool <tool> --model <model> --prompt "<prompt>" --seed <seed>
python3 "$R" set STORE_CAPSULE_MAIN_01 CONCEPT
python3 "$R" review STORE_CAPSULE_MAIN_01 request   # the user picks among the candidates
python3 "$R" set STORE_CAPSULE_MAIN_01 PRODUCTION   # gated on that approval, because --hero
```

Capsules and trailers are `--hero`: they need the user's approval at concept before
production, because they are the most expensive thing here to redo and the most public.
Rejected candidates get `REJECTED` with the user's reason in the note — a later session must
know which capsule lost and why, or it will propose it again.

Never set `VALIDATED` here. That belongs to `steam-store-review`, which is a different session
on purpose: the one that composed the capsule cannot see it the way a stranger will.

## Where this sits

```
steam-store-page (brief)  →  steam-store-assets (candidates → ladder test → user picks → export)
                          →  steam-store-review (compliance + conversion verdict)  →  iterate
```

Taste is the user's: whether the capsule is *striking*, whether the trailer is *exciting*.
Prepare the comparison honestly — same scene, same sizes, side by side — and let them choose.
