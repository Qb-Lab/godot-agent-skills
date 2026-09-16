# Contributing

## Adding a skill

0. **Check it isn't already covered.** GodotPrompter ships 55 Godot skills and
   awesome-gamedev ships 68. If one of them owns the topic, add a row to the *delegation*
   table in the router instead of writing a skill. Duplicating them costs context and
   creates version-skew disagreements the model has to arbitrate.
1. Create `skills/<skill-name>/SKILL.md` (flat — the `category:` field is the grouping)
2. Frontmatter needs `name`, `description`, and `category` (one of `engineering`,
   `productivity`, `design`, `strategy`, `production`, `router` — see the router's
   *Categories* section for what each says about how fast the contents rot)
3. Check the name against the other packs — a directory-name collision makes `install.sh`
   silently clobber one of them. `validate.sh` blocks the two known ones.
4. Add it to the "what this pack owns" table in `skills/using-godot-skills/SKILL.md`
5. Add it to the README table
6. Run `./scripts/validate.sh`

## Writing the description

The description is the entire triggering mechanism. Claude decides whether to load a skill from `name` + `description` alone, and the common failure is under-triggering — a good skill that never loads.

Write it as *when to use*, with concrete trigger phrases, not as a summary of contents:

- Weak: "Guidance on Godot scene files."
- Strong: "Safely read, edit, and repair Godot .tscn and .tres files by hand. Use whenever you are about to open, diff, patch, merge, or generate a scene file — including fixing a broken uid:// error or resolving a git merge conflict in a scene."

Include the error messages and user phrasings that should pull the skill in.

## Writing the body

- Imperative voice
- Explain *why* something matters rather than stacking MUSTs — a model that understands the reason generalizes to cases you did not list
- Under ~500 lines; past that, split into `references/` and point at them from SKILL.md.
  Domain knowledge the model needs only sometimes (checklists, maps, glossaries) belongs in
  `references/` from the start — the SKILL.md carries the method, the references carry the
  material.
- Executable helpers go in `scripts/`, stdlib-only, with a `--help`; resolve them from the
  loaded SKILL.md's directory, never from a hard-coded install path. A helper shared by
  several skills lives in exactly one of them and the others resolve it as a sibling
  (`$SKILL_DIR/../<owner>/scripts/…`) with a stated fallback. `validate.sh` lints them.
- State a skill keeps between sessions lives in the *game project* (`docs/design/`,
  `HANDOFF.md`, a registry file), never in the skill directory, and is machine-readable when
  another skill has to act on it.
- Concrete examples over abstract rules
- Version-specific claims need a version attached

## Changing the hooks

The hooks see every prompt and can block tool calls, so they get a higher bar than a skill:

- **Fail open.** Not a Godot project, no engine binary, malformed stdin — exit 0 silently.
  A hook that blocks work it cannot justify will be uninstalled, and then nothing is enforced.
- **Never loop.** The `Stop` hook must honour `stop_hook_active` and nudge at most once.
- **Say why, and say what to do instead.** A denial the model cannot act on just wastes a turn.
- **Keep `UserPromptSubmit` cheap.** It runs on every prompt; full rules once per session.
- Add a case to the test payloads before changing behaviour, and run `./scripts/validate.sh`.

## Scope

In scope: Godot 4.x engineering that no other pack covers, game-dev workflow, game design
judgment, and the control layer.

Out of scope: general programming advice with no game or Godot angle, Godot 3.x (the API guard
covers translation, but the pack targets 4.x), other engines, and anything GodotPrompter or
awesome-gamedev already covers — delegate to them from the router instead.
