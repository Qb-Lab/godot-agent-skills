# `docs/design/STORE.md` — skeleton

The store page's source of truth. One section per decision area, each with a lock level and
the `DD-` ids behind it, so a session three weeks later knows what is settled and what is
still open without re-asking.

Lock levels, same meaning as the Art Bible's: `UNKNOWN` (not discussed) · `EXPLORING`
(options on the table) · `PROVISIONAL` (chosen, may move) · `APPROVED` (the user signed off on
real output) · `LOCKED` (published — changing it edits a live page, so it needs a `DD-` entry).

Shape the sections to the game. Delete what does not apply rather than leaving `UNKNOWN`
headings that look like unfinished work.

```markdown
# Store page — <Game Name>
Last updated: <date> · Steam app id: <id or "not yet created">
Page status: <not started | drafting | ready for review | submitted | live>

## Positioning line — LOCK: <level>
One sentence, internal, not page copy: who this is for and why they would pick it over the
nearest thing. Every field below is judged against this line.
Decisions: DD-0NN

## Funnel status
| Step | State | Weakest thing about it |
|---|---|---|
| Capsule | | |
| Title / logo | | |
| Short description | | |
| Trailer | | |
| First screenshots | | |
| Below the fold | | |

## Short description — LOCK: <level>
> <the current text, verbatim>

Character count: <n> (counter read in Steamworks on <date>)
Candidates considered and scores: <link or inline table>
Decisions: DD-0NN

## Long description — LOCK: <level>
Structure: <the claim/proof rhythm actually used>
Current text: <inline, or the path to the file holding it>
Embedded demos: <registry ids>, total size <n> MB of the 15 MB budget

## Features — LOCK: <level>
- <concrete capability>
- <concrete capability>

## Tags — LOCK: <level>
In weight order. Rank is weight; the first 15 are prioritized by some store filters.
1. <tag> — <why it is accurate>
2. …
Rejected: <tag> — <why we do not deserve it>

## Store assets — LOCK: <level>
| Slot | Required size | Registry id | Status |
|---|---|---|---|
| Main capsule | 1232x706 | STORE_CAPSULE_MAIN_01 | |
| Header capsule | 920x430 | | |
| Small capsule | 462x174 | | |
| Vertical capsule | 748x896 | | |
| Library capsule / hero / logo | | | |
| Trailer | | STORE_TRAILER_01 | |
| Screenshots (min 5) | 1920x1080 | STORE_SHOT_01 … | |

## Localization — LOCK: <level>
Store page: <languages, and why each>
Game: <languages the game genuinely supports — this is a promise>
Second wave gated on: <signal>

## Release date — LOCK: <level>
Public presentation: <exact | month | quarter | year | Coming Soon>
Internal target: <date>
Why this granularity: <what production can honestly support>
Frozen from: <date minus two weeks>

## Links and developer presence — LOCK: <level>
Website / Discord / YouTube / X: <url or "deliberately none, because …">
Developer and publisher homepages configured: <yes/no>
Community plan: <what will actually be posted, and how often>

## Compliance
| Requirement | Source | Read on | PASS / FAIL / NEEDS VERIFICATION |
|---|---|---|---|

## Review history
| Date | Verdict | Biggest weakness identified | Highest-leverage fix | Done? |
|---|---|---|---|---|

## Open questions
- <the next decision, and what it is blocked on>
```

## Rules for keeping it honest

- **Verbatim text, not summaries.** "Short description is punchy and clear" is worthless to a
  later session; the actual sentence is the artifact.
- **Nothing is `APPROVED` without the user approving output.** A section the model likes is
  `PROVISIONAL`.
- **Compliance lines carry their read date.** A `PASS` without a date is a `NEEDS
  VERIFICATION` wearing a disguise.
- **Rejected options stay written down** with the reason, so they stay rejected.
- Per-asset state belongs in the registry, not here — this file links to ids.
