#!/usr/bin/env bash
# Check every SKILL.md has the required frontmatter and a unique name, and that the
# control layer is wired to files that exist and actually parse.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fail=0
names=""

while IFS= read -r f; do
  rel="${f#"$ROOT"/}"

  head -n1 "$f" | grep -q '^---$' || { echo "FAIL $rel: no frontmatter"; fail=1; continue; }

  name="$(sed -n '2,10p' "$f" | grep -m1 '^name:' | sed 's/^name:[[:space:]]*//')"
  desc="$(sed -n '2,10p' "$f" | grep -m1 '^description:' | sed 's/^description:[[:space:]]*//')"
  cat_="$(sed -n '2,10p' "$f" | grep -m1 '^category:' | sed 's/^category:[[:space:]]*//')"
  dir="$(basename "$(dirname "$f")")"

  [ -n "$name" ] || { echo "FAIL $rel: missing name"; fail=1; }
  [ -n "$desc" ] || { echo "FAIL $rel: missing description"; fail=1; }
  case "$cat_" in
    engineering|productivity|design|strategy|production|router) ;;
    "") echo "FAIL $rel: missing category"; fail=1;;
    *) echo "FAIL $rel: unknown category '$cat_'"; fail=1;;
  esac
  [ "$name" = "$dir" ] || { echo "FAIL $rel: name '$name' != folder '$dir'"; fail=1; }
  [ "${#desc}" -ge 60 ] || { echo "WARN $rel: description is short; triggering may suffer"; }

  case " $names " in *" $name "*) echo "FAIL $rel: duplicate name '$name'"; fail=1;; esac
  names="$names $name"
done < <(find "$ROOT/skills" -name SKILL.md -type f | sort)

# --- bundled skill scripts -----------------------------------------------------------
# Same bar as the hooks: executable, and it parses. A helper another skill resolves as a
# sibling must exist where the SKILL.md says it does.
while IFS= read -r sc; do
  rel="${sc#"$ROOT"/}"
  [ -x "$sc" ] || { echo "FAIL $rel: not executable (chmod +x)"; fail=1; }
  case "$sc" in
    *.sh) bash -n "$sc" 2>/dev/null || { echo "FAIL $rel: bash syntax error"; fail=1; };;
    *.py) python3 -c 'import py_compile,sys; py_compile.compile(sys.argv[1], doraise=True)' "$sc" >/dev/null 2>&1 \
            || { echo "FAIL $rel: python syntax error"; fail=1; };;
  esac
done < <(find "$ROOT/skills" -path '*/scripts/*' -type f \( -name '*.sh' -o -name '*.py' \) | sort)

# Cross-skill references: a SKILL.md that names ../<skill>/scripts/<file> must point at a real file.
while IFS= read -r line; do
  f="${line%%:*}"; ref="${line#*:}"
  skilldir="$(dirname "$f")"; [ "$(basename "$skilldir")" = references ] && skilldir="$(dirname "$skilldir")"
  target="$skilldir/$ref"
  [ -f "$target" ] || { echo "FAIL ${f#"$ROOT"/}: references missing $ref"; fail=1; }
done < <(grep -oH '\.\./[a-z0-9-]*/scripts/[A-Za-z0-9_.-]*' "$ROOT"/skills/*/SKILL.md "$ROOT"/skills/*/references/*.md 2>/dev/null | sort -u)

# --- control layer -----------------------------------------------------------------
HOOKS="$ROOT/hooks/hooks.json"
if [ -f "$HOOKS" ]; then
  if ! python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$HOOKS" 2>/dev/null; then
    echo "FAIL hooks/hooks.json: not valid JSON"; fail=1
  else
    while IFS= read -r cmd; do
      p="${cmd/\$\{CLAUDE_PLUGIN_ROOT\}/$ROOT}"
      rel="${p#"$ROOT"/}"
      [ -f "$p" ] || { echo "FAIL hooks.json: command not found: $rel"; fail=1; continue; }
      [ -x "$p" ] || { echo "FAIL $rel: not executable (chmod +x)"; fail=1; }
      case "$p" in
        *.sh) bash -n "$p" 2>/dev/null || { echo "FAIL $rel: bash syntax error"; fail=1; };;
        *.py) python3 -c 'import py_compile,sys; py_compile.compile(sys.argv[1], doraise=True)' "$p" >/dev/null 2>&1 \
                || { echo "FAIL $rel: python syntax error"; fail=1; };;
      esac
    done < <(python3 - "$HOOKS" <<'PY'
import json, sys
for groups in json.load(open(sys.argv[1]))["hooks"].values():
    for g in groups:
        for h in g.get("hooks", []):
            if h.get("command"):
                print(h["command"])
PY
    )
  fi
fi

# Skill names this pack must NOT ship, because they collide with other Godot packs
# installed into the same flat skills directory (install.sh would silently clobber one).
for taken in gdscript-patterns godot-export; do
  case " $names " in *" $taken "*)
    echo "FAIL: '$taken' collides with another Godot pack; rename or remove"; fail=1;;
  esac
done

[ "$fail" -eq 0 ] && echo "all skills valid; control layer wired"
exit "$fail"
