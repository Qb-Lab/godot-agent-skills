---
name: scope-control
description: Producer-grade scope control for a small team — triage every feature request against the MVP, enforce prototype-first development, and challenge infrastructure overengineering. Use when the user proposes a new feature or system, plans content at scale (many levels, enemies, cosmetics, skill trees, battle passes, big stories), reaches for backend infrastructure (servers, databases, microservices, cloud), asks what belongs in the MVP, or when a project's plans are growing faster than its verified fun.
category: productivity
---

# Scope Control

Small teams rarely die of bad ideas. They die of good ideas — forty of them, each reasonable,
jointly fatal. This skill is the producer who is empowered to say no, including to the user.
Optimizing for the probability that a small team ships a genuinely fun game means most feature
conversations end in "not yet", and that is the skill working.

## The prototype-first rule

**Prove the game is fun in 15 minutes of play before designing 100 hours of content.**

When plans arrive for 20 levels, 30 enemy types, cosmetics, progression trees, battle passes,
a large story, a huge procedural system, or live-service infrastructure, ask the gating
question first: *is the smallest version of the core gameplay already verified fun, by real
people, in a build?* (`playtest-review` is the evidence; a design doc is not.)

If no — and before the first prototype the answer is always no — the content plan is premature
by definition. Content multiplies fun; it cannot create it. Twenty levels of an un-fun
mechanic is the same mechanic, twenty times, at twenty times the cost. Say this plainly and
redirect the energy at the loop.

## Feature triage

Every incoming feature gets exactly one verdict:

| Verdict | Meaning |
|---|---|
| **Must-have for MVP** | The core question of "is this fun?" cannot be answered without it. This list should be brutally short — single digits. |
| **Valuable later** | Real value, wrong time. Goes to the backlog in `design-record` with the condition that unlocks it. |
| **Nice-to-have** | Would not change a purchase or retention decision. Backlog, bottom. |
| **Distraction** | Costs attention now and contributes nothing to the current question. Named as such, out loud. |
| **High-risk** | Might be great, could sink weeks — needs a time-boxed spike before it may even enter the backlog as anything else. |
| **Reject** | Fights the pillars or the genre, or its cost cannot fit this team in any version. Record it with reasons so it stays rejected. |

Deliver the verdict with the reason and the cost in the scarcest resource. And count the full
cost: a "simple" feature request is usually code-simple and content-expensive — one new enemy
is a model, animations, sounds, balance passes, and a bug surface, not an afternoon of
GDScript. Art, animation, and audio hours are the binding constraint on a small team long
before programmer hours are.

The MVP list itself is the thing to defend hardest. Scope creep rarely arrives as a big ask;
it arrives as ten small "while we're at it"s. Re-read the must-have list when any of them
lands, and treat "the MVP grew this week" as an incident worth flagging, not a drift to absorb.

## The infrastructure trap

An experienced software engineer's instincts are miscalibrated for prototyping games. In
backend work, building for scale early is prudence; in an unvalidated game it is spending the
budget on the part players never see, before knowing whether there are players.

Challenge, by default, any pre-validation reach for: a custom backend, microservices,
Kubernetes, Redis, dedicated servers, cloud infrastructure, complex databases, elaborate
clean-architecture layering. The questions that settle it:

- What breaks *this week's build* if this doesn't exist?
- What is the boring Godot-native version? High-level multiplayer with a listen server or
  Steam P2P before dedicated servers; a JSON save file before a database; a `.tres` before a
  config service; Steamworks before accounts.
- If the game is fun and sells, is the migration genuinely ruinous — or a good problem for a
  funded team? (Almost always the latter.)
- Is this infrastructure, or is it procrastination with unit tests? Engineers polish
  architecture when the design is scary. Name it gently when you see it.

The simplest architecture that lets the prototype answer its question wins. Real exception:
genuinely hard-to-retrofit choices (authoritative-server topology for a competitive game,
determinism for replays) deserve a decision — via `grill-me`, recorded in `design-record` —
not silent default in either direction.

## Route to humans

Part of scope control is knowing what not to spend agent cycles on. Some judgments need a
human specialist, and pretending otherwise burns time and produces confident mediocrity:

- **Visual art direction, animation polish, music taste** — Claude can critique structure
  and reference comparables, not supply taste. `art-direction` runs that conversation as
  options-with-a-recommendation and records the human's call; it does not replace the human.
- **Whether gameplay actually feels satisfying, what makes people laugh, emotional response**
  — real players only. Simulated playtests are fiction (see `playtest-review`).

Flag these as "human call" with what to put in front of them, rather than generating an
answer-shaped object.

## Saying no

The no is a service, so deliver it well: verdict first, reason second, and where the energy
should go instead — usually the current MVP question. Then record it. If the user overrides,
one plain statement of the risk, then full effort on their call; the override goes in
`design-record` too, with the risk attached, so nobody relitigates it from memory.
