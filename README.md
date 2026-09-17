# godot-agent-skills

A control layer for AI agents working in Godot 4.x, plus the few skills no other pack covers.

The skills are portable `SKILL.md` — they work with Claude Code, Codex, Cursor, OpenCode and
~70 other agents via the [`skills` CLI](https://github.com/vercel-labs/skills). The hooks are
Claude Code specific.

## Why

Generated GDScript fails in three predictable ways:

1. **Godot 3 API leaks in.** Most GDScript online is Godot 3, so `yield`, `.instance()`, and
   `export var` come out fluently and break immediately.
2. **Scene files get corrupted.** `.tscn` looks like editable INI. It is full of
   cross-references that must stay consistent.
3. **Nothing gets verified.** Code is written, declared working, and never run.

Other packs cover Godot's API surface well and in more depth than anything here would.
None of them covers these three. So this pack does these three, enforces them with hooks,
and delegates the rest.

## The control layer

Rules written in a `SKILL.md` only apply if that skill triggers — and with several packs
installed, ~140 skill descriptions compete for the same slot. Hooks do not compete. They run.

| Hook | Event | Effect |
|---|---|---|
| `godot-context.sh` | `UserPromptSubmit` | Injects the standing rules and the project's real engine version into every prompt. Full rules once per session, one line after that. Silent outside a Godot project. |
| `guard-scene-files.py` | `PreToolUse` | Denies structural `.tscn`/`.tres` edits — `uid://`, `load_steps`, `ext_resource`/`sub_resource` ids, node blocks — with the reason attached. Scalar property edits and `[connection]` lines pass through. |
| `require-verify.sh` | `Stop` | Blocks ending the turn while `.gd`/`.tscn`/`.tres` changed and nothing was verified. Nudges once per turn, never loops. |
| `verify-baseline.sh` | `SessionStart` | Marks the verification baseline for the session. |

The `PreToolUse` and `Stop` hooks are the pack's two founding rules turned from prose into
enforcement. Both degrade quietly: no Godot project, no engine binary, or malformed input and
they exit silently rather than blocking work.

## Skills

### Engineering — what nothing else covers

| Skill | Purpose |
|---|---|
| `godot-scene-surgery` | Safe `.tscn`/`.tres` editing, uid and `load_steps` rules, merge-conflict handling |
| `godot4-api-guard` | Godot 3 → 4 translation tables, plus drift inside Godot 4's own minor versions |
| `godot-verify` | The verify-before-claiming rule; headless import, parse checks, GdUnit4/GUT, honest exit-code reading |
| `codex-review` | Bounded Codex review loop over the staged changeset, tuned for Godot bug classes; engine-verified fixes |

### Productivity — workflow, engine-agnostic

| Skill | Purpose |
|---|---|
| `write-plan` | Phased, reviewable plan before non-trivial work — one phase per agent session |
| `grill-me` | Stress-test a design, then decide it — pickable options with a recommendation |
| `build-loop` | One change per verification cycle, so failures stay attributable |
| `session-handoff` | Compact state snapshot for resuming later |
| `scope-control` | The producer who says no — MVP triage, prototype-first, the infrastructure trap |
| `design-record` | Durable vision, pillars, and decision log, so rejected ideas stay rejected |

### Design — game design judgment

| Skill | Purpose |
|---|---|
| `game-feel-review` | Input buffering, coyote time, hitstop, camera, response curves |
| `loop-and-economy` | Core loop, sources/sinks, progression pacing, dominant strategies |
| `streamability` | Clip potential, unscripted stories, and whether multiplayer earns its cost |
| `playtest-review` | Feedback → ranked findings; the judge kept separate from the builder |

### Strategy — market-facing judgment

| Skill | Purpose |
|---|---|
| `market-scan` | Current-market research protocol — Steam, Twitch, reviews, saturation; never from recall |
| `concept-eval` | Scored concept gate returning BUILD / PROTOTYPE / MODIFY / RESEARCH MORE / KILL |

Skills compose — every skill whose trigger matches loads, not just one. The standing combo:
an economy or progression design still being decided loads `loop-and-economy` for the domain
critique **and** `grill-me` to force it to a decision, ideally before `write-plan` records the
outcome. No special syntax needed — "grill my upgrade economy: …" triggers both.

The strategy and design skills also chain into a greenlight pipeline for new game ideas —
`market-scan → concept-eval → scope-control → design → prototype → playtest-review`, with
`design-record` keeping every verdict on file. The router documents the full pipeline. Roles
you might expect and won't find — level design, enemy/AI design, narrative, Steam launch
strategy — are deliberately absent: they are premature before a validated prototype, and the
technical halves are covered by the larger packs this one delegates to. Art direction *is*
present (below), but built the same way: blockouts are the prototype, nothing is polished
before the loop is verified fun, and taste stays a human call.

### Production — art direction and asset production

| Skill | Purpose |
|---|---|
| `art-direction` | The design-side `grill-me`: one decision at a time, taught before asked, options with tradeoffs and a recommendation — then five curated visual-concept images of one gameplay moment to compare and refine before the Art Bible locks — producing the Art Bible, the production plan, and buildable asset specs |
| `asset-builder` | Executes approved asset work by the right method — blockout before beauty, shader not texture, kit not thirty walls — and leaves it game-ready in Godot with its state recorded |
| `asset-review` | The separated judge: inspects the real files and scenes against concept, Art Bible, spec, budgets, and Godot practice; the only thing that marks an asset VALIDATED |

State lives in the game project, not in the conversation: `docs/design/ART-BIBLE.md`,
`PRODUCTION.md`, and `asset-registry.json` beside `design-record`'s `GAME.md` and
`DECISIONS.md`. `art-direction/scripts/registry.py status` tells a fresh session what exists,
what is approved, what was rejected, and what is next — so "continue with the game design"
three weeks later starts from the record, not from questions already answered. The pipeline,
lifecycle, and nine worked examples are in [docs/ART-PIPELINE.md](docs/ART-PIPELINE.md).

### Router

`using-godot-skills` — precedence rules and the delegation map for composing with other packs.

## Composing with other packs

This pack is built to sit **on top of** the larger Godot packs, not to replace them:

| Concern | Owner |
|---|---|
| GDScript idiom, nodes, physics, UI, shaders, audio, tilemaps, 3D, multiplayer | [GodotPrompter](https://github.com/jame581/GodotPrompter) (55 skills), [awesome-gamedev-agent-skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills) (68) |
| Performance, export, CI, distribution | either of the above |
| Running tests — GdUnit4, PlayGodot, E2E | [Randroids-Dojo/Godot-Claude-Skills](https://github.com/Randroids-Dojo/Godot-Claude-Skills) |
| Scene-file surgery, Godot 3→4 guard, verification discipline, workflow, design, art direction & asset production state | this pack |

**Known name collisions** if you install more than one pack into a flat skills directory:
this pack previously shipped `gdscript-patterns` (collides with GodotPrompter) and
`godot-export` (collides with awesome-gamedev). Both were removed for exactly that reason.

**Version skew is real.** awesome-gamedev pins Godot 4.7; GodotPrompter targets 4.3+. The
`UserPromptSubmit` hook reads `config/features` from your `project.godot` and states the actual
version every prompt, so advice pinned to another version gets treated as unverified.

## Install

```bash
# Pick from a list
npx skills add Qb-Lab/godot-agent-skills

# A specific skill, globally, for Claude Code
npx skills add Qb-Lab/godot-agent-skills --skill <name> -g -a claude-code

# Everything
npx skills add Qb-Lab/godot-agent-skills --all
```

Project installs go to `./.claude/skills/` (or your agent's equivalent); `-g` installs to your
home directory instead. `--list` shows the names without installing, and `npx skills update`
pulls the latest versions.

Useful subsets:

```bash
# The Godot guardrails only
npx skills add Qb-Lab/godot-agent-skills \
  -s godot-scene-surgery -s godot4-api-guard -s godot-verify

# The workflow discipline only — engine-agnostic, useful outside Godot
npx skills add Qb-Lab/godot-agent-skills \
  -s write-plan -s grill-me -s build-loop -s session-handoff

# The studio layer — greenlight pipeline, scope control, playtesting, decision memory
npx skills add Qb-Lab/godot-agent-skills \
  -s market-scan -s concept-eval -s scope-control -s streamability \
  -s playtest-review -s design-record

# The art pipeline — direction, production, review (install all three; they share one registry tool)
npx skills add Qb-Lab/godot-agent-skills \
  -s art-direction -s asset-builder -s asset-review -s design-record
```

`using-godot-skills` references the other skills by name, so install it last or edit its tables
to match what you took.

### The control layer

The `skills` CLI installs skills, not hooks. The hooks are what make the rules stick when other
packs are installed, so install them too:

```bash
git clone https://github.com/Qb-Lab/godot-agent-skills.git
cd path/to/your-game
/path/to/godot-agent-skills/scripts/install-hooks.sh    # -> ./.claude/settings.json
```

Idempotent, and it merges alongside hooks other packs registered on the same event — it will
not clobber GodotPrompter's `SessionStart` entry. Claude Code only; `bash` and `python3`
required. Read `hooks/` first: two of them can block your work.

Or take both halves as a Claude Code plugin, which picks up skills and `hooks/hooks.json`
together:

```bash
claude plugin marketplace add Qb-Lab/godot-agent-skills
claude plugin install godot@godot-agent-skills
```

### Check it worked

Open a Godot project and send any prompt. The response should be working from an injected block
naming your engine version; `/hooks` lists what is registered. For the skills, ask something
that should trigger one:

> "I'm getting `Invalid call. Nonexistent function 'instance'` in my Godot project"

`godot4-api-guard` should load.

See [docs/INSTALLATION.md](docs/INSTALLATION.md) for the offline `scripts/install.sh` path,
per-agent directories, and exactly what each hook can do to your session.

## A note on categories

Skills live flat at `skills/<skill-name>/SKILL.md`, which is the layout every agent's discovery
expects — nesting them under category folders puts them one level too deep for some, including
Claude Code's plugin loader. The grouping survives as a `category:` field in each skill's
frontmatter, and as the headings in the table above.

## Status

Early. The hooks are tested against synthetic payloads; the skills are not yet eval-tested
against a real project. Version-specific claims are accurate to Godot 4.3 as far as they have
been checked. Verify against your engine version before relying on any specific API detail.

## Security

Read every `SKILL.md`, hook, and script before installing this or any other skill pack — this
one included, and with more care than usual, because it registers hooks that see every prompt
and can block tool calls. Agent skills are executable instructions with repository-level trust;
treat them as third-party code. Snyk's ToxicSkills research found prompt injection in a
substantial fraction of published skills across the ecosystem.

## License

MIT
