---
name: design-record
description: Maintain the project's durable design memory — vision, pillars, MVP scope, and a decision log with reasons and evidence — so settled calls stay settled and rejected ideas stay rejected across sessions. Use when a design or scope decision gets made or overridden, when an idea is rejected or killed, when the user asks "didn't we already decide this", when starting work that should be checked against prior decisions, or when setting up a new game project's vision and pillars.
category: productivity
---

# Design Record

The most expensive conversation in a long project is the one you are having for the third
time. Sessions forget; a fresh agent cheerfully re-proposes the mechanic that was killed a
month ago, and the user either wastes a cycle re-litigating or — worse — doesn't remember
either and re-approves it. Durable memory is what turns a series of sessions into a studio.

`HANDOFF.md` (`session-handoff`) is the *session* snapshot: what works right now, what's next.
This skill owns the *project* truth: two files that outlive any session. The art pipeline adds
three siblings in the same folder — `ART-BIBLE.md`, `PRODUCTION.md`, `asset-registry.json` —
owned by `art-direction`; they cite decisions from here rather than restating them.

## The two files

**`docs/design/GAME.md`** — the current state of design truth. A snapshot, overwritten as
things change, never a log. Short enough to be read at the start of any design conversation:

```markdown
# <Game> — design record

## Vision
One paragraph. The game in a sentence, and the experience it exists to deliver.

## Pillars
2–4 bullets. The things every feature must serve. If a feature serves none, it's cut.

## Target player & comparables
Who this is for; the 3–5 games they already play (with what we take and what we reject
from each).

## Approved mechanics
The mechanics that are in, one line each, with status: verified fun / prototyped / designed.

## Current MVP scope
The must-have list from scope-control. Anything not on it is not in the MVP.

## Rejected ideas
- <idea> — <why> — revisit if: <condition>. (This section is why the file exists.)

## Known risks
Technical, market, and design risks currently accepted, one line each.

## Art direction / audio direction
Current intent and references — and which calls are reserved for a human specialist. Once
`ART-BIBLE.md` exists (`art-direction`), this section is one line pointing at it.

## Backlog
"Valuable later" items, with the condition that unlocks each.

## Open questions
Undecided forks, each naming what evidence would settle it.
```

**`docs/design/DECISIONS.md`** — append-only log, newest first. One entry per decision that
shaped the game, each with a stable id (`DD-001`, `DD-002`, … — never reused, never renumbered)
so specs, plans, the Art Bible, and asset registry entries can cite it:

```markdown
## DD-014 — <decision title> — <YYYY-MM-DD>
Decision:
Reason:
Evidence: (market brief, playtest finding, prototype result — or honestly "judgment call")
Alternatives considered: (and why each lost)
Risks: (accepted knowingly, including any recorded disagreement)
Can revisit when: (the concrete trigger — new evidence, a date, a milestone)
```

`GAME.md` says what is true; `DECISIONS.md` says why it became true. When a decision is
superseded, the old entry stays — history is the point — and `GAME.md` changes.

## What gets recorded

A decision earns an entry when reversing it later would be expensive or when someone might
plausibly re-propose the alternative: concept verdicts from `concept-eval`, MVP cuts and
overrides from `scope-control`, forks settled through `grill-me`, mechanics killed by
`playtest-review` findings, architecture choices with migration cost, and art-direction calls
from `art-direction` — style family, proportions, kit grid, palette strategy, anything an
asset's spec will cite. When a decision is cited by an id, the id is what other files use;
the title can be edited, the id cannot. Tiny freely-reversible calls don't get entries; a log
with two hundred entries is a log nobody reads. Convert relative dates ("next month") to
absolute ones — the reader has no idea when "now" was.

Record overrides with special care. When the user overrides a KILL or a producer's no, the
entry states the recommendation, the override, and the accepted risk — one plain line, no
editorializing. That entry is what lets every future session respect the call instead of
re-arguing it.

## The check-before-proposing rule

Before proposing a mechanic, feature, or architecture in a project that has these files:
**read the rejected list and the decision log first.** Proposing something on the rejected
list is only legitimate when its "revisit if" condition has actually been met — in which case
name the condition and the new evidence explicitly ("we rejected local co-op for scope; the
loop is now verified fun and two testers asked for it — the revisit condition is met").
Reintroducing it without that is the exact failure this skill exists to prevent.

The same rule binds the record's author: never silently edit a decision entry to match what
you now wish had been decided. New evidence gets a new entry.

## Keeping it alive

A record only works if it is short enough to read and current enough to trust. If `GAME.md`
exceeds a couple of pages, it is accumulating prose that belongs in design docs — cut it back
to statements of truth. If the last decision entry is a month old in an active project, the
project is making undocumented decisions — say so, and offer to backfill the ones still
recoverable from `HANDOFF.md` and recent plans.
