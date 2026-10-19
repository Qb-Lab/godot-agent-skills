---
name: steam-store-review
description: Judge a Steam store page before it goes live — an official compliance matrix of PASS, FAIL or NEEDS VERIFICATION against current Steamworks requirements, a scored conversion review of the capsule, logo, copy, trailer and screenshots at the sizes players actually see them, and then exactly one biggest weakness and one highest-leverage fix instead of a list nobody acts on. Use when the user asks whether their Steam page is ready, good enough, or compliant; asks for a review, audit, critique or second opinion on a store page, capsule, trailer or screenshot set; says "will this convert", "does this stand out", "why is nobody wishlisting", or "check my page before I submit it"; or before a page is marked ready for review in Steamworks.
category: strategy
---

# Steam Store Review

The session that wrote the copy and composed the capsule cannot see them the way a stranger
scrolling a tag page will. That is not a failure of effort — it is what knowing the game does
to you. This skill is the other pair of eyes: it reads the requirements, looks at the assets at
the sizes players meet them, scores the funnel, and names **one** thing to fix.

It is `asset-review` applied to a storefront, and it is the only thing that marks a page
`READY`.

## Evidence tiers — state the tier with every finding

**Seen on the live or preview page** > **seen in the exported files** (the image itself, at the
ladder sizes, the trailer played) > **read in `STORE.md`** > **argued from the brief**. Never
blur them.

If you cannot view an image in this session, say so and ask for the files or screenshots —
**do not review a capsule from its description, its prompt, or the fact that it exists.** A
review of a capsule nobody looked at is worse than no review, because it ends the
conversation that would have caught the problem.

## Before reviewing

```bash
SKILL_DIR="$(cd "$(dirname "<path of this SKILL.md>")" && pwd)"
R="$SKILL_DIR/../art-direction/scripts/registry.py"
python3 "$R" status && python3 "$R" list --needs-review
# Needs steam-store-assets installed; without it, resize by hand and still look at 184x69.
python3 "$SKILL_DIR/../steam-store-assets/scripts/capsule-check.py" <capsule> --ladder
```

Then read `docs/design/STORE.md` (positioning line, current field text, compliance table),
`docs/design/GAME.md` (the pillars the page is compressing), `docs/design/ART-BIBLE.md` (what
the game is supposed to look like), the `DD-` entries the page cites, and the most recent
market brief — **differentiation cannot be judged without the competitor grid.** If the brief
is older than about a month, say that the standing-out question is unverified rather than
guessing at it.

The review compares the page to *those*, plus current Steamworks requirements. Not to your
taste, and not to the builder's account of it.

## Official compliance

Re-read the Steamworks pages. `$SKILL_DIR/../steam-store-page/references/steam-requirements.md`
lists what to check and where, with the date it was last read — but a compliance table built
from that file alone is a guess with a table around it. If that sibling is not installed, work
from <https://partner.steamgames.com/doc/store/assets/standard>,
`/assets/rules`, `/store/trailer`, `/store/page/description`, `/store/tags`, and
`/store/coming_soon`.

Every relevant requirement gets exactly one of three verdicts:

| Verdict | Means |
|---|---|
| **PASS** | You read the current requirement and checked the artifact against it |
| **FAIL** | Same, and it does not meet it. Say what the requirement is and what the artifact is |
| **NEEDS VERIFICATION** | You could not read the requirement, or could not inspect the artifact |

`NEEDS VERIFICATION` is the honest default and not a failure state. A table of `PASS` rows
where half were never actually checked is the single most damaging output this skill can
produce, because it is the thing someone submits on.

Cover at minimum: the five required capsule sizes and the library set, the minimum five
screenshots at 1920x1080 16:9 with four marked all-ages and no menu shots, capsule text rules,
trailer encode specs and conversion status, the tag minimum, no outbound links or Steam-UI
mimicry in the description, image size budgets, and the Coming Soon lead times. Each row
carries its source URL and the date you read it.

## Conversion review

Separate from compliance, and scored, so a re-review can be compared against this one. Score
each axis 1–10 with one line of justification naming what you looked at.
`references/scorecard.md` has the anchors — what a 3, a 6 and a 9 actually look like per axis,
so the numbers mean the same thing next month.

| Axis | The question |
|---|---|
| Capsule click potential | In a real competitor grid, would a stranger stop? |
| Logo readability | Readable at 184x69, in greyscale, blurred? |
| Short-description clarity | Does one read tell you the genre and the verb? |
| Trailer hook | Is something interesting happening in the first three seconds? |
| Screenshot strength | Does each one have a distinct job, and does the first carry the loop? |
| Gameplay communication | Could a stranger explain what they would do? |
| Visual consistency | Do the capsule, trailer, and screenshots look like one game? |
| Store differentiation | Against the actual grid, not against the genre in the abstract |
| Professional polish | Does it read as authored for this game, or as generated? |
| Wishlist motivation | Is there a reason not to forget about it? |

**The capsule is never scored from its full-size appearance.** Run the ladder, look at the
184x69 and the greyscale, and drop it into a real competitor grid screenshot. A capsule that
scores 9 at 1232x706 and 3 at 184x69 scores 3 — that is the size that decides.

## One weakness, one fix

The output ends with exactly two named things:

- **Biggest weakness** — the single thing most costing the page right now, with the evidence
  for why it is that one and not another.
- **Highest-leverage improvement** — the single change most likely to improve the page, with
  what it would take.

They are often, but not always, the same thing: the weakest element is sometimes also the most
expensive to fix, and the highest-leverage change is the cheap one next to it.

**Do not bury the recommendation under a list.** A page with twenty-three findings gets zero
fixed; a page with one gets one fixed, and then it can be reviewed again. Rank everything else
below those two, keep it short, and say plainly that it is secondary.

## The report

```markdown
# Store page review — <Game> — 2026-10-19
**Reviewed against:** STORE.md, GAME.md §Pillars, ART-BIBLE §Palette; DD-031, DD-034;
market brief 2026-10-02
**Evidence:** capsule seen in file at full/listing/184x69/grey + competitor grid; trailer
played; screenshots 01–07 seen in file; page not yet live, so no preview render
**Requirements re-read:** assets/standard, assets/rules, trailer (all 2026-10-19)

## Verdict: NOT READY

## Official compliance
| Requirement | Source | Read on | Verdict |
|---|---|---|---|
| Main capsule 1232x706 | .../assets/standard | 2026-10-19 | PASS |
| Small capsule logo readable at 184x69 | .../assets/standard | 2026-10-19 | FAIL — the subtitle is illegible below ~300px; Valve asks for a readable logo at the smallest size |
| Screenshots: min 5, 16:9, gameplay only | .../assets/standard | 2026-10-19 | PASS (7 shots, no menus) |
| 4+ screenshots marked all-ages | .../assets/standard | 2026-10-19 | NEEDS VERIFICATION — flags are set in Steamworks, which I cannot see |
| Trailer encode 5,000+ Kbps H.264 | .../store/trailer | 2026-10-19 | NEEDS VERIFICATION — no export file supplied |

## Conversion score
| Axis | Score | Why |
|---|---|---|
| Capsule click potential | 7 | Strong silhouette survives the grid; loses the second read to a busy background |
| Logo readability | 3 | Subtitle gone by 300px, wordmark mushy at 184x69 — see ladder/grey |
| Short-description clarity | 8 | Genre and verb in the first clause |
| … | | |

## Biggest weakness
The small capsule's logo. It is the one asset Valve generates down to 184x69, every other
score depends on the click it loses, and it is currently the lowest-scoring axis by four
points.

## Highest-leverage improvement
Design the small capsule as its own composition rather than a crop of the main one — drop the
subtitle, scale the wordmark to nearly fill the frame as Valve's guidance asks, and keep the
focal silhouette as a simplified shape behind it. One capsule, not a re-do of the set.

## Secondary, in order
1. Screenshot 04 and 05 do the same job (both show the ground floor at night) — replace 05.
2. The features block opens with "Immersive atmosphere", which reads as filler beside the
   rest of the page.

## Human calls
Whether the creature reads as frightening at thumbnail size is yours — look at
`ladder/capsule__tiny-184x69.png` beside the competitor grid.

## Not reviewable here
Trailer encode, all-ages flags, tag weight order as saved in Steamworks.
```

Then record it: append the verdict row to `STORE.md`'s review history, and for assets use the
registry so the outcome outlives the chat:

```bash
python3 "$R" verdict STORE_CAPSULE_SMALL_01 fail --note "logo illegible below ~300px; needs its own composition, not a crop of main"
```

Say what is genuinely right, specifically — it tells the builder what not to touch while
fixing the one thing. Do not pad a good page with soft concerns to look thorough. If it passes,
it passes.

## Taste, and what a verdict does not cover

- **Human calls stay human.** Whether the capsule is *striking*, whether the creature is
  *scary*, whether the voice sounds like the user — flag it as a human call, attach exactly
  what to look at and at what size, and let their approval be the record.
- **`READY` means compliance plus conversion plus the user's sign-off**, not your own
  satisfaction. Never mark a `STORE.md` section `LOCKED` or a page `READY` on your
  recommendation alone.
- **When the brief is what's wrong** — the assets obey `STORE.md` and `STORE.md` produces a bad
  page — review the assets against the brief as written, and raise the brief as a separate
  finding routed to `steam-store-page` with a `DD-` entry proposed. Do not quietly review
  against the brief you wish existed.
- **The reviewer does not fix the page.** A fix made here is a fix nobody reviewed. Findings
  go back to `steam-store-page` or `steam-store-assets`.

## What the page is for

The purpose is not to explain every feature. It is to make the right player think, in this
order:

> "I understand this." · "This looks like my kind of game." · "This looks fun." ·
> "I don't want to forget about it." → **wishlist**

Score against that, not against completeness. A page that answers all four with five
screenshots beats a complete one that answers none.
