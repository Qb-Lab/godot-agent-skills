# Store copy — method per field

Everything on this page is tier **BEST PRACTICE** unless a line is marked otherwise. These are
conversion recommendations, not Valve rules; the official half is in
`steam-requirements.md`. Say which is which in the output.

## Short description

The field is plain text with no formatting `[OFFICIAL]`, it is the first text most people
read, and Steam reuses it in places you do not control. It has to do four things at once:

```
GENRE  +  PLAYER GOAL / FANTASY  +  WHAT THE PLAYER DOES  +  THE DISTINCTIVE HOOK
```

**Lead with verbs.** The reader is deciding whether they want to *do* this, and a verb is the
fastest way to tell them: mine, build, fight, escape, trade, explore, manipulate, steal,
survive, manage, cooperate, betray, smuggle, rewire, repair, hunt, hide, automate, sabotage.

The failure is lore in the slot where the verb belongs:

> ✗ "The Prince Cyrule has taken control of the kingdom, and the old orders have fallen…"

A reader finishing that sentence knows the fiction and still cannot say what they would do
with their hands. Compare:

> ✓ "Build a resistance, recruit fighters and battle an alien occupation…"

Same setting, but the verbs arrive first. The exact writing has to come from this game — these
are patterns to aim at, never templates to fill.

### Generate and score, do not write and defend

Produce **five or more candidates** deliberately spread across different angles — the verb,
the fantasy, the hook, the tension, the comparison — then score each 1–5:

| Axis | What a 5 looks like |
|---|---|
| **Clarity** | A stranger understands it once, at speed, without re-reading |
| **Specificity** | Names this game's actual nouns and verbs, not any game's |
| **Genre communication** | The reader can place it on a shelf immediately |
| **Hook** | Contains the one thing no competitor's description contains |
| **Player action** | States what the player does, in verbs, in the first clause |
| **Differentiation** | Would not fit the three nearest competitors from the market brief |

Total them, show the table, recommend one, and say what the runner-up does better — that is
usually the sentence worth splicing in. Then let the user pick; this is their game's voice.

Read the field's own character counter in Steamworks rather than trusting a remembered
limit, and check that the sentence survives truncation — the first clause has to work alone,
because somewhere it will appear alone.

Avoid time-based copy such as "Now Available" `[OFFICIAL — Valve advises against it]`.

## Long description

The About section's enemy is the wall of text. A reader who has already clicked is skimming
for confirmation, so give them a rhythm of claim and proof rather than paragraphs:

```
SHORT INTRO (1–2 sentences that still work when surfaced elsewhere)
GAMEPLAY VISUAL
CORE IDEA
GAMEPLAY VISUAL
KEY SYSTEM
GAMEPLAY VISUAL
FEATURES
```

Open with one or two sentences strong enough to stand alone, because they get quoted, scraped,
and surfaced out of context. Then alternate: every claim is followed by the visual that proves
it. Two to four high-quality gameplay demonstrations is usually the right amount — beyond
that, the page gets heavy and you hit the 15 MB total `[OFFICIAL]`.

Keep images textless where you can; text in an image must be remade for every language
`[OFFICIAL — Valve recommends textless images]`. No links out, no fake Steam UI, no promoting
other games `[OFFICIAL]`.

Fifteen paragraphs of lore is not a long description, it is a design document nobody asked
for. If a section does not earn a skim-stop, cut it.

## Features

Close the About section with a compact features block of concrete, player-facing capabilities.
The test is whether a sentence could appear on a different game's page. If it could, it is
noise:

> ✗ "Immersive gameplay" · "Stunning graphics" · "Epic adventure" · "Unforgettable journey"

Those cost trust, because every page the reader has ever bounced off said them too. Replace
each with the thing it was gesturing at:

> ✓ "Mine destructible crystal formations with physics-driven tools."
> ✓ "Build automated transport routes between underground outposts."
> ✓ "Four players, one oxygen supply, and no way to tell who vented it."

Six to ten lines, each a capability or a situation. Bold the first few words so the block
skims. Do not restate what the short description already said.

## Tags

Tags are traffic routing, not decoration. **Wrong tags are worse than missing tags** — they
buy impressions from people who bounce, and bouncing teaches Steam to show the game to more
people like them. Accuracy beats popularity every time.

Cover the dimensions the store actually filters on: genre, gameplay, mechanics, theme,
perspective, player count and multiplayer mode, atmosphere. Then **rank by relevance, because
rank is weight** `[OFFICIAL — the first 15 are prioritized by some store filters]`.

Method:

1. Pull the tag sets of the five nearest comparables from the market brief — those are the
   tags your audience already browses.
2. Draft 15–20 `[BEST PRACTICE — Valve requires 5 and recommends up to 20]`.
3. Delete every tag you could not defend to a player who bought because of it.
4. Rank: the tags that describe what the game *is* above the ones that describe what it
   *contains*.
5. Record the ranked list in `STORE.md` so a later session does not quietly reshuffle it.

A tag you want but do not deserve ("Souls-like", "Roguelike") is an EXPERIMENT at best and a
refund generator at worst. Say so.

## Localization

Distinguish two different things that get conflated, with real consequences:

- **Store page localization** — the page's text in another language. Cheap, low-risk, and it
  only claims that the *page* is translated.
- **Game localization** — the game's own text. Expensive, and the store's language table is a
  promise. **Never list a game language the game does not genuinely support**; players buy on
  that table and refund on it, and the reviews stay.

The commonly recommended starting set is English, German, Brazilian Portuguese, Spanish and
Latin American Spanish, Russian, Simplified Chinese, Japanese, Korean. **Do not adopt that set
because it is on a list.** Choose from evidence:

- the genre — strategy, management, and anime-adjacent games have very different maps;
- where comparable games' reviews and wishlists actually come from;
- the budget, and whether a bad translation is worse than none for this audience;
- the game's own text volume — a text-light game localizes almost for free, a narrative game
  does not;
- whether the game already supports the language.

Recommend a first wave of two or three beyond English with the reason per language, and a
second wave gated on wishlist geography. That is a plan; the nine-language list is a wish.

## Presentation quality

A page that looks automatically generated is distrusted before it is read, and the tells are
specific:

- emoji in headers, or emoji as bullet points;
- buzzword stacking — "immersive", "epic", "stunning", "unforgettable" in one block;
- feature lists that restate each other in different words;
- headings on sections that are one sentence long;
- perfectly symmetrical generated key art with nonsensical detail;
- the same three-beat sentence rhythm for every bullet;
- copy that would fit any game in the genre.

The page should read as though someone who cares about *this* game wrote it, because the
reader is deciding whether anyone does. Where the user's own voice exists — a devlog, a Discord
post, the way they describe the game out loud — borrow it rather than smoothing it out.
