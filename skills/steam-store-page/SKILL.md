---
name: steam-store-page
description: Plan, write, and gate a Steam store page the way the funnel actually works — capsule, logo, short description, trailer, first screenshots before anything further down the page — labelling every claim as an official Valve requirement, a conversion best practice, or an experiment, and re-reading the official half from Steamworks instead of recalling it. Use when the user asks about their Steam page or Steamworks store presence, store copy, the short or long description, the About section, features list, store tags, store localization, release-date presentation, wishlists, a Coming Soon page, or announcing the game; or says "help me set up my Steam page", "write my short description", "what tags should I use", or "what do I need before I can publish the page".
category: strategy
---

# Steam Store Page

A store page is not a feature list. It is a funnel with one job at each step, and almost all
of the leverage sits in the first four seconds. This skill runs the page the way an art
director runs the Art Bible: one decision at a time, taught before asked, options with
tradeoffs and a recommendation — then written into a file so a later session continues from
the record instead of the chat.

`grill-me` describes *how* to ask: one decision per turn, 2–4 options with the recommendation
first, a consequence line per option, the two doors ("your own answer" / "let's talk"),
reversal-cost ordering, saying "this will break" once and then following the call. All of it
applies here unchanged. Read it if it is not loaded. This file covers what is different when
the subject is a storefront.

## Three tiers, never blurred

Every recommendation about a Steam page is one of three things, and collapsing them is the
most expensive mistake this skill can make.

| Tier | What it is | How to write it |
|---|---|---|
| **OFFICIAL** | Documented by Valve in Steamworks, and you read the doc in this session | Paraphrase with the doc URL and the date you read it |
| **BEST PRACTICE** | A conversion recommendation from people who sell games — not from Valve | Name it as practice and say what it is meant to improve |
| **EXPERIMENT** | Plausible for *this* game, unproven; worth testing | State the comparison you would run and what would settle it |

**Never present a third-party recommendation as an official Valve requirement.** The cost is
concrete and recurring: a team that believes "at least 7 screenshots" is a rule burns a day
chasing a number Valve never asked for (it requires 5), and a team that believes a capsule
border is required ships one it never compared against no border. Both lose the information
they would have had from treating it as an experiment.

Label inline, every time, in the tier's own words — `[OFFICIAL]`, `[BEST PRACTICE]`,
`[EXPERIMENT]` — not in a legend at the bottom that nobody reads.

## Verify, never recall

`market-scan`'s rule applies to Steam's own rules too: **asset dimensions, field limits,
required items, review lead times, and tag mechanics change, and model memory of them is
stale on arrival.** Before you state an OFFICIAL requirement, read the current page.

`references/steam-requirements.md` holds what was read from Steamworks on 2026-10-19, with
the URL beside each fact. Treat it as a starting point and a list of things to re-check, not
as authority: re-read any requirement you are about to have someone act on, and update the
reference's date line when you do. If you cannot browse in this session, say so, mark every
official claim `NEEDS VERIFICATION`, and do not let an export happen on an unverified
dimension.

## Orient before writing anything

A store page is downstream of the whole project. Read, in this order, whatever exists:

1. `docs/design/GAME.md` — vision, pillars, mechanics, target player (`design-record`). The
   short description is a compression of the pillars; if there are no pillars, the page has
   nothing to compress and the conversation belongs in `concept-eval` first.
2. `docs/design/STORE.md` — what is already decided here, at what lock level.
3. `docs/design/ART-BIBLE.md` — the capsule and screenshots must look like the game, which
   means they obey the bible. `art-direction` owns that document; this skill consumes it.
4. `docs/design/DECISIONS.md` — skim titles, read any `DD-` you are about to touch.
5. The registry — `python3 "$SKILL_DIR/../art-direction/scripts/registry.py" status` — what
   store assets exist, what awaits approval, what was rejected. (`SKILL_DIR` is the directory
   holding this file; never hard-code an install path.)
6. The most recent market brief, if there is one. Differentiation, tags, and pricing all
   depend on who else is in the grid; if the brief is older than about a month, re-run
   `market-scan` before claiming the page stands out.

Then say what you found in five lines and what the next useful decision is.

## Is a store page the right work right now?

Two true things pull in opposite directions, and the honest answer is a judgment call rather
than a rule:

- Wishlists accumulate over months and a Coming Soon page must be live for at least two weeks
  before release `[OFFICIAL]`, so waiting until the game is finished wastes the only free
  discovery Steam gives you. Start talking about the game early.
- A page needs footage that honestly represents the game. If every screenshot would be a
  blockout and the trailer would be a logo, the page is marketing fiction and the review
  scores it would earn are noise.

The gate: **one honest vertical slice.** Does something exist that a stranger could watch for
twenty seconds and want? If yes, build the page now — early is correct. If no, say that
plainly, name what is missing, and route back to the prototype (`scope-control`,
`playtest-review`). Writing excellent copy for an unvalidated loop is the most pleasant way
to avoid making the game.

## The funnel decides the order

```
STEAM IMPRESSION → CAPSULE → CLICK → ABOVE-THE-FOLD UNDERSTANDING → INTEREST → WISHLIST
```

Work the funnel in order and stop polishing anything below the step that is currently losing
people:

1. **Capsule** — wins or loses the click. Nothing below it matters until it works.
2. **Title and logo** — must be readable at the smallest capsule size.
3. **Short description** — the first text anyone reads, and the one Steam reuses elsewhere.
4. **Trailer** — the first autoplay-adjacent thing above the fold.
5. **First screenshots** — the fallback for everyone who does not play the trailer.
6. Everything else: long description, features, tags, localization, links, release date.

A beautiful features list under a capsule nobody clicks is wasted work. If the user wants to
start at the bottom, say once why the order matters, then follow their call — and record the
override.

`steam-store-assets` produces 1, 2, 4, 5 from briefs this skill writes. This skill owns 3 and
6, and owns the brief for all of them.

## The grill

Walk the decisions in funnel order, skipping anything already settled in `STORE.md`. For each
load-bearing call — one that changes what gets produced, or is expensive to reverse — use the
full `grill-me` shape, with the tier labelled on any factual claim inside it:

```markdown
**Decision — what the capsule has to say in one glance.**
This comes first because it determines the capsule brief, and the capsule decides whether
anyone sees the rest of the page at all.

**A. The signature mechanic, mid-action (recommended)** — a stranger infers genre and verb
without reading; survives the 184x69 thumbnail `[OFFICIAL: small capsule generates down to
184x69]` because one shape dominates. Costs the most art direction.
**B. The player character, hero pose** — cheapest to produce and most familiar; but in a
grid of twelve crafting games it reads as "another one", and your wedge is the mechanic.
**C. The environment as the hook** — right if atmosphere *is* the product; yours is a
systems game, so it undersells the thing people would wishlist for.

**Recommendation: A** — your differentiator is a verb, not a face or a place, and the
competitor grid from the market brief is full of faces.

Pick one, change one, or say "let's talk".
```

Teach in passing when a term first becomes load-bearing — capsule slot, safe area, tag
weighting, artwork override, wishlist conversion — one line, right there, tied to the decision
in front of them. Do not lecture.

Facts are looked up, never asked: what Valve requires, what the field limits are, what the
competitors' capsules look like, what assets the registry already holds. Only decisions go to
the user.

## Challenge

The user asked for a page that converts, not agreement. Say so, once and plainly, with the
better option and its cost, when a request:

- buries the verb under lore, so a reader still cannot say what they would *do*;
- puts text on a base capsule beyond the title and subtitle, which Valve's asset rules
  prohibit `[OFFICIAL]`;
- picks tags for popularity rather than accuracy — wrong tags buy wrong traffic, and traffic
  that bounces is worse than no traffic because it teaches Steam the wrong audience;
- claims game languages the game does not have, which converts into refunds and bad reviews;
- commits to a release date the production plan does not support;
- or reads as machine-made: emoji headers, buzzword stacks, redundant feature lists,
  templated marketing phrases. `references/copy.md` has the full anti-pattern list and why
  each one costs trust.

Then take their call and record it as an override with its risk.

## The page itself

| Field | Where the method lives |
|---|---|
| Short description — candidates, scoring, verbs | `references/copy.md` §Short description |
| Long description — structure, rhythm, embedded demos | `references/copy.md` §Long description |
| Features — concrete capability phrasing | `references/copy.md` §Features |
| Tags — accuracy, ranking, weighting | `references/copy.md` §Tags |
| Localization — store page vs game, which languages | `references/copy.md` §Localization |
| Presentation quality — what makes a page look generated | `references/copy.md` §Presentation |
| Release date, developer presence, links, Coming Soon | `references/steam-requirements.md` |
| Announcement and press package | `references/launch-package.md` |
| Capsule, logo, trailer, screenshots, GIFs | `steam-store-assets` — brief it from here |

Generate **multiple candidates and score them** for the short description and the capsule
concept rather than producing one and defending it; a single candidate is an opinion, five
scored candidates are a decision the user can actually make.

## What this skill writes

Direction lives in `STORE.md`; per-asset state lives in the registry; reasons live in the
decision log. Never duplicate one into another — link.

- **`docs/design/STORE.md`** — the store page source of truth: positioning line, the funnel
  status, every field's current text, the tag list in weight order, localization plan, release
  date presentation, asset briefs, and the compliance table. Skeleton in
  `references/store-page-template.md`. Each section carries a lock level the same way the Art
  Bible does: `UNKNOWN`, `EXPLORING`, `PROVISIONAL`, `APPROVED` (the user signed off on real
  output), `LOCKED` (published; changing it is a visible edit to a live page).
- **The asset registry** — one entry per store asset to produce, via
  `registry.py add --type capsule|logo|trailer|screenshot|showcase`, each with a brief a fresh
  session could build from. `art-direction/references/asset-registry.md` has the format and
  the gates.
- **`docs/design/DECISIONS.md`** — every call someone could re-propose (the capsule concept,
  the positioning line, the tag set, the date granularity, each override), as a
  `design-record` entry with a `DD-NNN` id, the alternatives, and the revisit condition.

## Human checkpoints

Claude proposes; the storefront is the user's name on a public page. Ask for explicit approval
on: the positioning line, the final short description, the capsule concept and the winning
capsule, the trailer cut, the screenshot set, the tag list, the release-date presentation, and
anything that goes live. Record each with `registry.py review <ID> approve` where an asset is
involved. Never mark a page section `LOCKED` on your own recommendation.

## Ending

Close as `grill-me` does — **Decided / Parked / Where I still disagree** — plus three lines
this skill owns: which files changed, which funnel step is currently the weakest, and the
single next action with its kickoff prompt. For example:

```
Brief STORE_CAPSULE_MAIN_01 from STORE.md and produce five capsule candidates.
```

Before anyone calls the page finished, hand it to `steam-store-review`. The session that wrote
the copy is the worst judge of whether it lands.
