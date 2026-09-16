#!/usr/bin/env python3
"""Asset registry for the art pipeline — the persistent state behind art-direction,
asset-builder, and asset-review.

The registry is a plain JSON file in the game project (default
docs/design/asset-registry.json). This script is the safe way to read and change it:
every change appends to the entry's history, nothing is ever deleted, and the gates
that make the pipeline honest are enforced here rather than in prose:

  - VALIDATED can only be reached through `verdict` (a review), never through `set`
  - a hero asset cannot leave CONCEPT for PRODUCTION until its concept was approved
  - an asset flagged blockout:true cannot enter PRODUCTION until its blockout was approved
  - a REJECTED or SUPERSEDED asset stays that way unless --force says why

Run `registry.py --help` and `registry.py schema` for the format. Python 3.8+, stdlib only.
"""
import argparse
import datetime as _dt
import json
import os
import re
import sys

STATUSES = [
    "PLANNED", "CONCEPT", "BLOCKOUT", "PRODUCTION", "INTEGRATED", "VALIDATED",
    "REWORK", "REJECTED", "SUPERSEDED",
]
TERMINAL = {"REJECTED", "SUPERSEDED"}
REVIEWS = ["none", "pending", "approved"]
TYPES = [
    "character", "creature", "architecture", "environment", "prop", "interactive-prop",
    "weapon", "vehicle", "ui", "texture", "material", "shader", "animation", "vfx",
    "decal", "icon", "concept", "reference", "audio-hook", "kit",
]
FILE_KINDS = ["source", "output", "godot", "concept", "reference", "spec"]
ID_RE = re.compile(r"^[A-Z][A-Z0-9]*(_[A-Z0-9]+)+$")

STATUS_HELP = {
    "PLANNED": "specced, nothing built yet",
    "CONCEPT": "exploration exists (sketch, reference board, proportion study) — hero assets need approval here",
    "BLOCKOUT": "placeholder geometry in the game, validating scale/collision/nav/reach — approve before production",
    "PRODUCTION": "the real asset is being made (source files, textures, rig, shader)",
    "INTEGRATED": "in Godot: imported, wrapped, collision/physics/material/script wired, test scene exists",
    "VALIDATED": "asset-review passed it against spec, Art Bible, budgets — only `verdict pass` sets this",
    "REWORK": "review failed; the latest note says what to fix",
    "REJECTED": "killed; the note says why. Kept so it stays rejected",
    "SUPERSEDED": "replaced by a newer entry; `superseded_by` names the authoritative one",
}


# ----------------------------------------------------------------------------- io

def today():
    return _dt.date.today().isoformat()


def find_project_root(start=None):
    d = os.path.abspath(start or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())
    for _ in range(6):
        if os.path.isfile(os.path.join(d, "project.godot")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return os.path.abspath(start or os.getcwd())


def registry_path(args):
    if args.registry:
        return os.path.abspath(args.registry)
    env = os.environ.get("ASSET_REGISTRY")
    if env:
        return os.path.abspath(env)
    return os.path.join(find_project_root(), "docs", "design", "asset-registry.json")


def load(path):
    if not os.path.isfile(path):
        die("no registry at %s — run `registry.py init` (from art-direction) first" % rel(path))
    with open(path, "r", encoding="utf-8") as fh:
        try:
            data = json.load(fh)
        except json.JSONDecodeError as exc:
            die("registry is not valid JSON: %s" % exc)
    data.setdefault("meta", {})
    data.setdefault("assets", {})
    return data


def save(path, data):
    data["meta"]["updated"] = today()
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False, sort_keys=False)
        fh.write("\n")
    os.replace(tmp, path)


def rel(path):
    try:
        return os.path.relpath(path)
    except ValueError:
        return path


def die(msg, code=1):
    print("registry: " + msg, file=sys.stderr)
    sys.exit(code)


def get(data, asset_id):
    a = data["assets"].get(asset_id)
    if a is None:
        close = [k for k in data["assets"] if asset_id.upper() in k]
        hint = (" — did you mean: " + ", ".join(close[:5])) if close else ""
        die("unknown asset %s%s" % (asset_id, hint))
    return a


def touch(a, note=None, frm=None, to=None):
    a["updated"] = today()
    entry = {"date": today()}
    if frm is not None or to is not None:
        entry["from"] = frm
        entry["to"] = to
    if note:
        entry["note"] = note
    a.setdefault("history", []).append(entry)


# ------------------------------------------------------------------------ commands

def cmd_init(args, path):
    if os.path.exists(path) and not args.force:
        die("%s already exists (use --force to overwrite an EMPTY registry only)" % rel(path))
    if os.path.exists(path):
        existing = load(path)
        if existing["assets"]:
            die("refusing to overwrite a registry with %d assets" % len(existing["assets"]))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = {
        "meta": {
            "format": 1,
            "game": args.game or "",
            "created": today(),
            "updated": today(),
            "art_bible": "docs/design/ART-BIBLE.md",
            "production_plan": "docs/design/PRODUCTION.md",
            "decisions": "docs/design/DECISIONS.md",
        },
        "assets": {},
    }
    save(path, data)
    print("created %s" % rel(path))


def cmd_add(args, path):
    data = load(path)
    aid = args.id
    if not ID_RE.match(aid):
        die("id must look like CATEGORY_NAME_01 (upper-case, underscores): %s" % aid)
    if aid in data["assets"]:
        die("%s already exists — use `set`, `note`, or `supersede`" % aid)
    if args.type not in TYPES:
        die("type must be one of: %s" % ", ".join(TYPES))
    spec = {}
    if args.spec:
        try:
            spec = json.loads(args.spec)
        except json.JSONDecodeError as exc:
            die("--spec must be a JSON object: %s" % exc)
    for kv in args.spec_field or []:
        if "=" not in kv:
            die("--spec-field wants key=value, got %s" % kv)
        k, v = kv.split("=", 1)
        spec[k.strip()] = v.strip()
    a = {
        "id": aid,
        "name": args.name or aid.replace("_", " ").title(),
        "type": args.type,
        "phase": args.phase,
        "status": "PLANNED",
        "review": "none",
        "hero": bool(args.hero),
        "blockout": bool(args.blockout),
        "purpose": args.purpose or "",
        "spec": spec,
        "spec_file": args.spec_file,
        "kit": args.kit,
        "decisions": args.decision or [],
        "depends_on": args.depends_on or [],
        "variants": [],
        "files": [],
        "godot": {"scene": None, "resources": []},
        "supersedes": None,
        "superseded_by": None,
        "validation": {"result": None, "date": None, "findings": None},
        "notes": [],
        "history": [],
        "created": today(),
        "updated": today(),
    }
    for dep in a["depends_on"]:
        if dep not in data["assets"]:
            print("warning: dependency %s is not in the registry yet" % dep, file=sys.stderr)
    touch(a, note=args.note or "created", frm=None, to="PLANNED")
    data["assets"][aid] = a
    save(path, data)
    print("added %s [%s] phase %s%s%s" % (
        aid, a["type"], a["phase"],
        " hero" if a["hero"] else "", " blockout-first" if a["blockout"] else ""))


def _gate(a, target, force):
    """Return an error string when the transition is not allowed without --force."""
    cur = a["status"]
    if force:
        return None
    if cur in TERMINAL:
        return "%s is %s; leaving that state needs --force with a reason" % (a["id"], cur)
    if target == "VALIDATED":
        return "VALIDATED is set by `verdict %s pass` after a review, not by `set`" % a["id"]
    if target == "PRODUCTION":
        if a.get("blockout"):
            been_blockout = any(h.get("to") == "BLOCKOUT" for h in a.get("history", []))
            if cur != "BLOCKOUT" or not been_blockout:
                return ("%s is blockout-first: set BLOCKOUT, validate it in-game, `review approve`, "
                        "then PRODUCTION (or --force with the reason)" % a["id"])
            if a.get("review") != "approved":
                return "%s blockout has not been approved (`review %s approve`)" % (a["id"], a["id"])
        if a.get("hero") and cur == "CONCEPT" and a.get("review") != "approved":
            return ("%s is a hero asset: its concept needs `review %s approve` before production "
                    "(or --force with the reason)" % (a["id"], a["id"]))
        if a.get("hero") and cur == "PLANNED":
            return ("%s is a hero asset: go through CONCEPT and get it approved before production "
                    "(or --force with the reason)" % a["id"])
    return None


def cmd_set(args, path):
    data = load(path)
    a = get(data, args.id)
    target = args.status.upper()
    if target not in STATUSES:
        die("status must be one of: %s" % ", ".join(STATUSES))
    err = _gate(a, target, args.force)
    if err:
        die(err)
    if args.force and not args.note:
        die("--force needs --note explaining why the gate is being bypassed")
    frm = a["status"]
    a["status"] = target
    # review always refers to the current stage's output; a new stage starts unreviewed
    a["review"] = "none"
    note = args.note or ""
    if args.force:
        note = "FORCED: " + note
    touch(a, note=note or None, frm=frm, to=target)
    save(path, data)
    print("%s: %s -> %s%s" % (a["id"], frm, target, (" — " + note) if note else ""))


def cmd_review(args, path):
    data = load(path)
    a = get(data, args.id)
    action = args.action
    if action == "request":
        a["review"] = "pending"
        touch(a, note="review requested: " + (args.note or "awaiting human look at %s output" % a["status"]))
    elif action == "approve":
        a["review"] = "approved"
        touch(a, note="APPROVED at %s%s" % (a["status"], (": " + args.note) if args.note else ""))
    elif action == "rework":
        frm = a["status"]
        a["status"] = "REWORK"
        a["review"] = "none"
        if not args.note:
            die("rework needs --note saying what to change")
        touch(a, note="rework: " + args.note, frm=frm, to="REWORK")
    save(path, data)
    print("%s: review %s (status %s)" % (a["id"], a["review"] if action != "rework" else "rework", a["status"]))


def cmd_verdict(args, path):
    data = load(path)
    a = get(data, args.id)
    if a["status"] in TERMINAL and not args.force:
        die("%s is %s" % (a["id"], a["status"]))
    result = args.result
    a["validation"] = {"result": result, "date": today(), "findings": args.note or None}
    frm = a["status"]
    if result == "pass":
        a["status"] = "VALIDATED"
        a["review"] = "approved"
    else:
        if not args.note:
            die("a failing verdict needs --note with the ranked findings (or a path to them)")
        a["status"] = "REWORK"
        a["review"] = "none"
    touch(a, note="review verdict %s%s" % (result, (": " + args.note) if args.note else ""), frm=frm, to=a["status"])
    save(path, data)
    print("%s: %s -> %s" % (a["id"], frm, a["status"]))


def cmd_file(args, path):
    data = load(path)
    a = get(data, args.id)
    if args.kind not in FILE_KINDS:
        die("kind must be one of: %s" % ", ".join(FILE_KINDS))
    entry = {"path": args.path, "kind": args.kind, "added": today()}
    if args.note:
        entry["note"] = args.note
    gen = {}
    for key in ("tool", "prompt", "negative_prompt", "seed", "model", "ref"):
        val = getattr(args, key, None)
        if val:
            gen[key] = val
    if gen:
        gen["date"] = today()
        entry["generation"] = gen
    a["files"] = [f for f in a["files"] if f["path"] != args.path] + [entry]
    if args.kind == "godot" and args.path.endswith(".tscn"):
        a["godot"]["scene"] = args.path
    elif args.kind == "godot":
        if args.path not in a["godot"]["resources"]:
            a["godot"]["resources"].append(args.path)
    if args.kind == "spec":
        a["spec_file"] = args.path
    touch(a, note="file %s: %s" % (args.kind, args.path))
    save(path, data)
    root = find_project_root()
    disk = args.path
    if disk.startswith("res://"):
        disk = os.path.join(root, disk[len("res://"):])
    elif not os.path.isabs(disk):
        disk = os.path.join(root, disk)
    if not os.path.exists(disk):
        print("warning: %s does not exist on disk yet" % args.path, file=sys.stderr)
    print("%s: recorded %s %s" % (a["id"], args.kind, args.path))


def cmd_note(args, path):
    data = load(path)
    a = get(data, args.id)
    a["notes"].append({"date": today(), "text": args.text})
    touch(a, note=args.text)
    save(path, data)
    print("%s: noted" % a["id"])


def cmd_edit(args, path):
    """Change a scalar field or a spec field without touching status."""
    data = load(path)
    a = get(data, args.id)
    field, value = args.field, args.value
    if field.startswith("spec."):
        a.setdefault("spec", {})[field[5:]] = value
    elif field in ("name", "purpose", "spec_file", "kit"):
        a[field] = value
    elif field == "phase":
        a["phase"] = int(value)
    elif field in ("hero", "blockout"):
        a[field] = value.lower() in ("1", "true", "yes")
    elif field in ("decisions", "depends_on", "variants"):
        if value not in a[field]:
            a[field].append(value)
    else:
        die("editable fields: name purpose spec_file kit phase hero blockout decisions depends_on variants spec.<key>")
    touch(a, note="edit %s" % field)
    save(path, data)
    print("%s: %s updated" % (a["id"], field))


def cmd_supersede(args, path):
    data = load(path)
    old = get(data, args.old)
    new_id = args.new
    if not ID_RE.match(new_id):
        die("new id must look like CATEGORY_NAME_02: %s" % new_id)
    if new_id in data["assets"]:
        new = data["assets"][new_id]
    else:
        new = json.loads(json.dumps(old))  # deep copy of the spec, not of the state
        auto_old = old["id"].replace("_", " ").title()
        new.update({
            "id": new_id,
            "name": args.name or (new_id.replace("_", " ").title() if old["name"] == auto_old else old["name"]),
            "status": "PLANNED",
            "review": "none",
            "files": [],
            "godot": {"scene": None, "resources": []},
            "validation": {"result": None, "date": None, "findings": None},
            "notes": [],
            "history": [],
            "supersedes": None,
            "superseded_by": None,
            "created": today(),
            "updated": today(),
        })
        touch(new, note="created as replacement for %s: %s" % (old["id"], args.note or ""), to="PLANNED")
        data["assets"][new_id] = new
    frm = old["status"]
    old["status"] = "SUPERSEDED"
    old["review"] = "none"
    old["superseded_by"] = new_id
    new["supersedes"] = old["id"]
    touch(old, note="superseded by %s: %s" % (new_id, args.note or ""), frm=frm, to="SUPERSEDED")
    # anything that depended on the old id should now point at the new one — flag, don't rewrite
    dependents = [k for k, v in data["assets"].items() if old["id"] in v.get("depends_on", []) and k != new_id]
    save(path, data)
    print("%s: %s -> SUPERSEDED, authoritative is now %s" % (old["id"], frm, new_id))
    if dependents:
        print("note: these depend on %s and may need repointing: %s" % (old["id"], ", ".join(dependents)))


def cmd_show(args, path):
    data = load(path)
    a = get(data, args.id)
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
        return
    print("%s — %s" % (a["id"], a["name"]))
    print("  type %s · phase %s · status %s · review %s%s%s" % (
        a["type"], a["phase"], a["status"], a["review"],
        " · HERO" if a["hero"] else "", " · blockout-first" if a.get("blockout") else ""))
    if a["purpose"]:
        print("  purpose: %s" % a["purpose"])
    for k, v in (a.get("spec") or {}).items():
        print("  spec.%s: %s" % (k, v if not isinstance(v, list) else ", ".join(map(str, v))))
    if a.get("spec_file"):
        print("  spec file: %s" % a["spec_file"])
    if a.get("kit"):
        print("  kit: %s" % a["kit"])
    if a["decisions"]:
        print("  decisions: %s" % ", ".join(a["decisions"]))
    if a["depends_on"]:
        print("  depends on: %s" % ", ".join(a["depends_on"]))
    if a["supersedes"]:
        print("  supersedes: %s" % a["supersedes"])
    if a["superseded_by"]:
        print("  SUPERSEDED BY: %s  <- use that one" % a["superseded_by"])
    if a["godot"]["scene"]:
        print("  godot scene: %s" % a["godot"]["scene"])
    for f in a["files"]:
        gen = f.get("generation")
        print("  file [%s] %s%s" % (f["kind"], f["path"],
                                    ("  (gen: %s%s)" % (gen.get("tool", "?"), (" seed " + str(gen["seed"])) if gen.get("seed") else "")) if gen else ""))
    if a["validation"]["result"]:
        print("  validation: %s (%s) %s" % (a["validation"]["result"], a["validation"]["date"], a["validation"]["findings"] or ""))
    for n in a["notes"][-3:]:
        print("  note %s: %s" % (n["date"], n["text"]))
    hist = a["history"][-(args.history or 4):]
    for h in hist:
        arrow = ("%s -> %s " % (h.get("from"), h.get("to"))) if "to" in h else ""
        print("  %s %s%s" % (h["date"], arrow, h.get("note", "")))


def _filtered(data, args):
    out = []
    for a in data["assets"].values():
        if args.status and a["status"] != args.status.upper():
            continue
        if args.phase is not None and a["phase"] != args.phase:
            continue
        if args.type and a["type"] != args.type:
            continue
        if args.needs_review and a["review"] != "pending":
            continue
        if args.kit and a.get("kit") != args.kit:
            continue
        if not args.all and a["status"] in TERMINAL and not args.status:
            continue
        out.append(a)
    out.sort(key=lambda x: (x["phase"], STATUSES.index(x["status"]), x["id"]))
    return out


def cmd_list(args, path):
    data = load(path)
    rows = _filtered(data, args)
    if args.json:
        print(json.dumps([a["id"] for a in rows] if args.ids else rows, indent=2))
        return
    if not rows:
        print("no assets match")
        return
    for a in rows:
        flags = ("H" if a["hero"] else "-") + ("B" if a.get("blockout") else "-")
        rv = {"none": "", "pending": " ⏳review", "approved": " ✓approved"}[a["review"]]
        print("P%-2s %-11s %s %-32s %-16s %s%s" % (
            a["phase"], a["status"], flags, a["id"], a["type"], a["name"], rv))


def _read_current_phase(root):
    plan = os.path.join(root, "docs", "design", "PRODUCTION.md")
    if not os.path.isfile(plan):
        return None, False
    with open(plan, "r", encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r"\s*Current phase:\s*(\S+)", line)
            if m:
                return m.group(1).rstrip(".,;"), True
    return None, True


def cmd_status(args, path):
    root = find_project_root()
    if not os.path.isfile(path):
        print("No asset registry at %s." % rel(path))
        print("This project has no art pipeline state yet — art-direction starts discovery and runs `registry.py init`.")
        for name in ("GAME.md", "DECISIONS.md", "ART-BIBLE.md", "PRODUCTION.md"):
            p = os.path.join(root, "docs", "design", name)
            print("  %-14s %s" % (name, "present" if os.path.isfile(p) else "missing"))
        return
    data = load(path)
    assets = data["assets"]
    phase_from_plan, plan_exists = _read_current_phase(root)
    docs = {}
    for name in ("GAME.md", "DECISIONS.md", "ART-BIBLE.md", "PRODUCTION.md"):
        docs[name] = os.path.isfile(os.path.join(root, "docs", "design", name))
    print("Registry %s — %d assets (%s)" % (rel(path), len(assets), data["meta"].get("game") or "unnamed game"))
    print("Docs: " + " · ".join("%s %s" % (k, "✓" if v else "MISSING") for k, v in docs.items()))
    if plan_exists and phase_from_plan:
        print("PRODUCTION.md says current phase: %s" % phase_from_plan)

    by_phase = {}
    for a in assets.values():
        by_phase.setdefault(a["phase"], []).append(a)
    lowest_open = None
    for ph in sorted(by_phase):
        rows = by_phase[ph]
        counts = {}
        for a in rows:
            counts[a["status"]] = counts.get(a["status"], 0) + 1
        live = [a for a in rows if a["status"] not in TERMINAL]
        done = sum(1 for a in live if a["status"] == "VALIDATED")
        summary = ", ".join("%d %s" % (counts[s], s) for s in STATUSES if s in counts)
        marker = ""
        if live and done < len(live) and lowest_open is None:
            lowest_open = ph
            marker = "  <- lowest incomplete phase"
        print("Phase %s — %d/%d validated: %s%s" % (ph, done, len(live), summary, marker))

    pending = [a for a in assets.values() if a["review"] == "pending"]
    rework = [a for a in assets.values() if a["status"] == "REWORK"]
    heroes_unapproved = [a for a in assets.values() if a["hero"] and a["status"] in ("PLANNED", "CONCEPT") and a["review"] != "approved"]
    blocked = []
    for a in assets.values():
        if a["status"] in TERMINAL:
            continue
        for dep in a.get("depends_on", []):
            d = assets.get(dep)
            if d is None or d["status"] not in ("INTEGRATED", "VALIDATED"):
                blocked.append((a["id"], dep, d["status"] if d else "missing"))
    if pending:
        print("Awaiting your review (%d): %s" % (len(pending), ", ".join("%s [%s]" % (a["id"], a["status"]) for a in pending)))
    if rework:
        print("Rework (%d):" % len(rework))
        for a in rework:
            print("  %s — %s" % (a["id"], (a["validation"].get("findings") or (a["history"][-1].get("note") if a["history"] else "") or "")[:110]))
    if heroes_unapproved:
        print("Hero assets not yet approved (%d): %s" % (len(heroes_unapproved), ", ".join(a["id"] for a in heroes_unapproved)))
    if blocked:
        print("Blocked on dependencies (%d): %s" % (len(blocked), "; ".join("%s needs %s (%s)" % b for b in blocked[:6])))
    term = [a for a in assets.values() if a["status"] in TERMINAL]
    if term:
        print("Rejected/superseded: %d (kept for history — `list --all` or `list --status REJECTED`)" % len(term))
    if lowest_open is None and assets:
        print("Every live asset is VALIDATED. Next: the next phase in PRODUCTION.md, or art-direction for new work.")


def cmd_deps(args, path):
    data = load(path)
    a = get(data, args.id)
    dependents = [k for k, v in data["assets"].items() if a["id"] in v.get("depends_on", [])]
    kitmates = [k for k, v in data["assets"].items() if a.get("kit") and v.get("kit") == a["kit"] and k != a["id"]]
    print("%s depends on: %s" % (a["id"], ", ".join(a["depends_on"]) or "nothing"))
    print("depended on by: %s" % (", ".join(dependents) or "nothing"))
    if kitmates:
        print("same kit (%s): %s" % (a["kit"], ", ".join(kitmates)))
    if a["variants"]:
        print("variants: %s" % ", ".join(a["variants"]))


def cmd_validate(args, path):
    data = load(path)
    root = find_project_root()
    problems, warnings = [], []
    for aid, a in data["assets"].items():
        if a.get("id") != aid:
            problems.append("%s: id field mismatch" % aid)
        if not ID_RE.match(aid):
            problems.append("%s: id does not match CATEGORY_NAME_01" % aid)
        if a.get("status") not in STATUSES:
            problems.append("%s: unknown status %s" % (aid, a.get("status")))
        if a.get("review") not in REVIEWS:
            problems.append("%s: unknown review %s" % (aid, a.get("review")))
        if a.get("type") not in TYPES:
            problems.append("%s: unknown type %s" % (aid, a.get("type")))
        if a.get("status") == "VALIDATED" and (a.get("validation") or {}).get("result") != "pass":
            problems.append("%s: VALIDATED without a passing verdict" % aid)
        if a.get("status") == "SUPERSEDED" and not a.get("superseded_by"):
            problems.append("%s: SUPERSEDED but superseded_by is empty" % aid)
        if a.get("superseded_by") and a["superseded_by"] not in data["assets"]:
            problems.append("%s: superseded_by %s does not exist" % (aid, a["superseded_by"]))
        for dep in a.get("depends_on", []):
            d = data["assets"].get(dep)
            if d is None:
                problems.append("%s: depends on missing %s" % (aid, dep))
            elif d["status"] in TERMINAL and a["status"] not in TERMINAL:
                warnings.append("%s: depends on %s which is %s%s" % (
                    aid, dep, d["status"], (" (use %s)" % d["superseded_by"]) if d.get("superseded_by") else ""))
        if a.get("kit") and a["kit"] not in data["assets"]:
            warnings.append("%s: kit %s has no registry entry" % (aid, a["kit"]))
        if a.get("status") in ("PRODUCTION", "INTEGRATED", "VALIDATED") and not a.get("files"):
            warnings.append("%s: %s but no files recorded" % (aid, a["status"]))
        if a.get("status") in ("INTEGRATED", "VALIDATED") and not a["godot"].get("scene") and a["type"] not in ("concept", "reference", "texture", "material", "shader", "animation", "audio-hook", "icon", "decal", "kit", "ui"):
            warnings.append("%s: %s but no Godot scene recorded" % (aid, a["status"]))
        for f in a.get("files", []):
            p = f["path"]
            disk = os.path.join(root, p[len("res://"):]) if p.startswith("res://") else (p if os.path.isabs(p) else os.path.join(root, p))
            if not os.path.exists(disk):
                warnings.append("%s: file missing on disk: %s" % (aid, p))
            if f.get("kind") == "output" and not f.get("generation") and a["type"] in ("concept", "texture"):
                warnings.append("%s: generated %s has no generation metadata" % (aid, p))
    for p in problems:
        print("FAIL " + p)
    for w in warnings:
        print("WARN " + w)
    if not problems:
        print("registry consistent: %d assets%s" % (len(data["assets"]), (", %d warnings" % len(warnings)) if warnings else ""))
    sys.exit(1 if problems else 0)


def cmd_schema(args, path):
    print("Asset registry format 1 — one JSON object: {\"meta\": {...}, \"assets\": {\"<ID>\": {...}}}\n")
    print("Statuses (lifecycle):")
    for s in STATUSES:
        print("  %-11s %s" % (s, STATUS_HELP[s]))
    print("\nreview: none | pending | approved — human sign-off on the CURRENT status's output; resets on every status change")
    print("hero: true  — needs concept approval before PRODUCTION (main character, primary creatures, representative environment)")
    print("blockout: true — gameplay-heavy; needs an approved BLOCKOUT before PRODUCTION")
    print("\nTypes: " + ", ".join(TYPES))
    print("File kinds: " + ", ".join(FILE_KINDS) + "  (generation metadata attaches to a file: --tool --prompt --seed --model --ref)")
    print("\nEntry fields: id name type phase status review hero blockout purpose spec{} spec_file kit decisions[] depends_on[]")
    print("              variants[] files[] godot{scene,resources[]} supersedes superseded_by validation{} notes[] history[] created updated")
    print("\nIds: CATEGORY_NAME_NN e.g. CHAR_PLAYER_01, CREATURE_STALKER_01, ENV_PROP_DINING_CHAIR_01, KIT_MANSION_MODULAR, SHADER_WATER_01, VFX_BLOOD_HIT_01")


# ----------------------------------------------------------------------------- main

def main(argv=None):
    p = argparse.ArgumentParser(prog="registry.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--registry", help="path to asset-registry.json (default: <project>/docs/design/asset-registry.json, or $ASSET_REGISTRY)")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init", help="create an empty registry"); s.add_argument("--game"); s.add_argument("--force", action="store_true"); s.set_defaults(fn=cmd_init)
    s = sub.add_parser("status", help="orientation: docs present, per-phase counts, what awaits review, what is blocked"); s.set_defaults(fn=cmd_status)
    s = sub.add_parser("schema", help="print the format, statuses, types"); s.set_defaults(fn=cmd_schema)

    s = sub.add_parser("list", help="list assets (terminal ones hidden unless --all or --status)")
    s.add_argument("--status"); s.add_argument("--phase", type=int); s.add_argument("--type"); s.add_argument("--kit")
    s.add_argument("--needs-review", action="store_true"); s.add_argument("--all", action="store_true")
    s.add_argument("--json", action="store_true"); s.add_argument("--ids", action="store_true"); s.set_defaults(fn=cmd_list)

    s = sub.add_parser("show", help="one asset in full"); s.add_argument("id"); s.add_argument("--json", action="store_true"); s.add_argument("--history", type=int); s.set_defaults(fn=cmd_show)
    s = sub.add_parser("deps", help="what an asset depends on and what depends on it"); s.add_argument("id"); s.set_defaults(fn=cmd_deps)

    s = sub.add_parser("add", help="add a PLANNED asset")
    s.add_argument("id"); s.add_argument("--type", required=True); s.add_argument("--phase", type=int, required=True)
    s.add_argument("--name"); s.add_argument("--purpose"); s.add_argument("--hero", action="store_true"); s.add_argument("--blockout", action="store_true")
    s.add_argument("--spec", help="JSON object"); s.add_argument("--spec-field", action="append", help="key=value, repeatable")
    s.add_argument("--spec-file"); s.add_argument("--kit"); s.add_argument("--decision", action="append"); s.add_argument("--depends-on", action="append")
    s.add_argument("--note"); s.set_defaults(fn=cmd_add)

    s = sub.add_parser("set", help="change status (gates apply)"); s.add_argument("id"); s.add_argument("status"); s.add_argument("--note"); s.add_argument("--force", action="store_true"); s.set_defaults(fn=cmd_set)
    s = sub.add_parser("review", help="request / approve / rework the current stage's output"); s.add_argument("id"); s.add_argument("action", choices=["request", "approve", "rework"]); s.add_argument("--note"); s.set_defaults(fn=cmd_review)
    s = sub.add_parser("verdict", help="asset-review outcome: pass -> VALIDATED, fail -> REWORK"); s.add_argument("id"); s.add_argument("result", choices=["pass", "fail"]); s.add_argument("--note"); s.add_argument("--force", action="store_true"); s.set_defaults(fn=cmd_verdict)

    s = sub.add_parser("file", help="record a file (source/output/godot/concept/reference/spec) with optional generation metadata")
    s.add_argument("id"); s.add_argument("path"); s.add_argument("--kind", required=True); s.add_argument("--note")
    s.add_argument("--tool"); s.add_argument("--prompt"); s.add_argument("--negative-prompt", dest="negative_prompt"); s.add_argument("--seed"); s.add_argument("--model"); s.add_argument("--ref", help="reference image or source used")
    s.set_defaults(fn=cmd_file)

    s = sub.add_parser("note", help="append a note"); s.add_argument("id"); s.add_argument("text"); s.set_defaults(fn=cmd_note)
    s = sub.add_parser("edit", help="change name/purpose/phase/hero/blockout/kit/spec.<key>, or append to decisions/depends_on/variants"); s.add_argument("id"); s.add_argument("field"); s.add_argument("value"); s.set_defaults(fn=cmd_edit)
    s = sub.add_parser("supersede", help="retire OLD in favour of NEW (created from OLD's spec if absent)"); s.add_argument("old"); s.add_argument("new"); s.add_argument("--name"); s.add_argument("--note"); s.set_defaults(fn=cmd_supersede)
    s = sub.add_parser("validate", help="consistency check: statuses, links, files on disk"); s.set_defaults(fn=cmd_validate)

    args = p.parse_args(argv)
    args.fn(args, registry_path(args))


if __name__ == "__main__":
    main()
