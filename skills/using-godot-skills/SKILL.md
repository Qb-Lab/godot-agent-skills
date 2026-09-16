---
name: using-godot-skills
description: Index and precedence rules for the godot-agent-skills pack, and how it composes with other installed Godot skill packs (GodotPrompter, awesome-gamedev, Randroids-Dojo). Consult when a Godot task could be served by more than one installed skill, when two packs give conflicting API advice, or when you need to know which pack owns a given concern. Use whenever a request involves Godot, GDScript, .tscn or .tres files, game feel, game balance, game concepts or market viability, scope or playtesting, art direction or asset production, or planning game development work.
category: router
---

# Using godot-agent-skills

This pack is deliberately small. It covers the things no other Godot skill pack covers, and
delegates everything else. If you are looking for GDScript idiom, node/scene structure,
physics, UI, shaders, audio, export, or optimization, those live in the other installed
packs — see the delegation table below.

## The standing rules do not live here

The rules this pack exists to enforce are injected by hooks on every prompt, not by this
skill. That is deliberate: a router skill only routes if it wins a triggering contest
against every other pack's router, and two of them advertise harder than this one does.

See `hooks/` in the pack root. What it does:

| Hook | Event | Effect |
|---|---|---|
| `godot-context.sh` | `UserPromptSubmit` | Injects the standing rules and the project's actual engine version into every prompt |
| `guard-scene-files.py` | `PreToolUse` | Denies structural `.tscn`/`.tres` edits — ids, `load_steps`, `uid://`, node blocks |
| `require-verify.sh` | `Stop` | Blocks ending the turn while Godot source changed and nothing was verified |
| `verify-baseline.sh` | `SessionStart` | Marks the verification baseline for the session |

If the hooks are not installed, this skill is the fallback and you should apply its rules
by hand. `scripts/install-hooks.sh` wires them into `settings.json`.

## What this pack owns

| The request involves | Load |
|---|---|
| Editing, repairing, or merging `.tscn` / `.tres`, or a broken `uid://` | `godot-scene-surgery` |
| Writing or reviewing GDScript that may carry Godot 3 API | `godot4-api-guard` |
| Running, testing, or claiming something works | `godot-verify` |
| A feature request touching 3+ files | `write-plan` first — a phased plan, then `build-loop` per phase |
| Multi-step implementation | `build-loop` |
| "Critique this", "poke holes in this", "which approach should I take" | `grill-me` |
| A staged changeset before commit, "review this", second opinion | `codex-review` (explicit invocation only) |
| Stopping, resuming, "where are we" | `session-handoff` |
| "Feels floaty / mushy / unresponsive" | `game-feel-review` |
| Progression, currency, upgrades, balance | `loop-and-economy` — plus `grill-me` when a design decision is on the table |
| "What's trending", "is this genre saturated", competitor or market questions | `market-scan` — never answered from internal knowledge |
| A game idea or pitch, "should I build this" | `concept-eval` — with `market-scan` for the evidence and `grill-me` for the argument |
| New feature requests, content at scale, MVP questions, backend/infra urges | `scope-control` |
| Streamer appeal, clips, virality, "does multiplayer earn its cost" | `streamability` |
| Playtest feedback, "is it actually fun", reviewing a build against intent | `playtest-review` |
| A decision made / overridden / rejected, "didn't we decide this already" | `design-record` |
| How the game should look; art style, 2D/3D, camera, characters, monsters, environments, props, animation, shaders, VFX, UI direction; "design the first monster"; "what assets do we need"; "continue with the game design" | `art-direction` — the design-side `grill-me`; writes the Art Bible, production plan, and asset specs |
| "Build it", "build phase N", "make the X", a variant, a cheaper version, any asset or placeholder to produce | `asset-builder` — reads the registry and Art Bible first; blockout before beauty |
| "Review / check / approve this asset", something "looks off" or "out of scale", before marking an asset done | `asset-review` — the separated judge; the only thing that sets VALIDATED |

Rows compose — load every skill whose trigger matches, not just the best one. The standing
combo: an economy or progression *design* still being decided loads `loop-and-economy` for the
domain critique **and** `grill-me` to force it to a decision, ideally before `write-plan`
records the outcome.

## The greenlight pipeline

For a new game idea the strategy and design skills run as a pipeline, each gate feeding the
next. Enter wherever the project actually is; never skip forward past an unanswered gate:

```
idea → market-scan → concept-eval (+grill-me) → scope-control (MVP cut)
     → loop-and-economy + streamability (design the loop and the clip engine)
     → write-plan → build-loop + godot-verify (prototype)
     → playtest-review → iterate, or re-enter concept-eval → GO / PIVOT / KILL
```

`design-record` runs alongside the whole pipeline: every verdict, cut, and override lands in
`docs/design/`, and every skill checks the rejected list before proposing. Judging is kept
separate from building on purpose — the session that implemented a build does not also declare
it fun; that call belongs to `playtest-review` with real players.

## The art pipeline

Once a concept has a `GAME.md`, the art and asset skills run their own loop beside the
engineering one, sharing `docs/design/` and the same decision log:

```
GAME.md → art-direction (discovery → decisions → ART-BIBLE.md + PRODUCTION.md + asset specs)
        → asset-builder (CONCEPT → BLOCKOUT → user walks it → PRODUCTION → INTEGRATED)
        → asset-review (VALIDATED | REWORK) → design-record for every call → iterate
```

State lives in the project, not the conversation: `ART-BIBLE.md` (direction, with lock
levels), `PRODUCTION.md` (phases and reusable systems), `asset-registry.json` (per-asset
status, files, approvals, history — read with `art-direction/scripts/registry.py status`),
`DECISIONS.md` (`DD-` ids). A fresh session saying "continue with the game design" orients
from those five files and recommends the next action. Blockouts are the prototype
`scope-control` asks for; nothing past a blockout is polished before the loop is verified fun,
unless the concept is art-led and the plan says so.

The first two rows of the ownership table are the reason this pack exists: across the ~140
skills in the other Godot packs, none covers scene-file surgery and none covers Godot 3 → 4
translation.

## What this pack delegates

| Concern | Owner |
|---|---|
| GDScript idiom, typing, lifecycle, signals | `godot-gdscript` (awesome-gamedev), `gdscript-patterns` / `gdscript-advanced` (GodotPrompter) |
| Scene tree structure, composition, autoloads | `godot-nodes-scenes`, `scene-organization`, `component-system` |
| Physics, UI, animation, audio, shaders, tilemaps, 3D, multiplayer | the per-topic skills in either pack |
| Shader syntax, particle properties, import-dock options, `AnimationTree` API — the *how* behind an asset the art pipeline specced | the per-topic skills in either pack; `asset-builder` names the *what* and the checklist |
| Performance and profiling | `performance-optimization`, `godot-optimization` |
| Export, CI, distribution | `godot-export` (awesome-gamedev), `export-pipeline` (GodotPrompter) |
| Actually running tests — GdUnit4, PlayGodot, E2E | the `godot` skill (Randroids-Dojo) |

`godot-verify` states the rule; the Randroids skill supplies the machinery. Prefer its
`run_tests.py` / `validate_project.py` over hand-rolled scripts when it is installed.

## Precedence when packs disagree

1. **Engine version wins.** Read `config/features` in `project.godot` before trusting any
   API detail. awesome-gamedev pins Godot 4.7; GodotPrompter targets 4.3+. A skill written
   for a different minor version is advisory, not authoritative, and its API names need
   checking against the project's version.
2. **Scene files and Godot 3 → 4 translation are this pack's call**, because nothing else
   covers them.
3. **Everything technical otherwise defers to the specialist skill**, which is version-pinned
   and more detailed than anything here.
4. **Never resolve a disagreement by picking the more confident-sounding answer.** Check it:
   `godot --version`, or the class reference for the project's exact minor version.

## Categories

Each skill carries a `category:` field. What it tells you is how fast the contents rot:

- **engineering** — engine-specific. Goes stale with releases; check against the project.
- **productivity** — workflow discipline. Engine-agnostic, ages well.
- **design** — game design judgment. Not Godot-specific and largely version-proof.
- **strategy** — market-facing judgment. The *method* ages well; any market *claim* is stale
  in weeks, which is why these skills require fresh research instead of recall.
- **production** — art direction and asset production. The interview method and the state
  format age well; the Godot integration checklists and tool notes rot with engine and tool
  releases — check them against the project's version like any engineering claim.
