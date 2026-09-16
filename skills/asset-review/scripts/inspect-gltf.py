#!/usr/bin/env python3
"""Inspect a glTF / GLB file for the things a game-asset review checks: transforms, triangle
counts, vertex attributes, materials and textures, animations, skins, bounding box, pivot,
and Godot import-hint suffixes. Prints warnings for the classic failures.

Usage: inspect-gltf.py FILE [--budget TRIS] [--expect-height METRES] [--tolerance FRACTION] [--json]
Stdlib only; reads the JSON chunk and accessor bounds, not the full geometry.
"""
import argparse
import json
import os
import struct
import sys

GODOT_SUFFIXES = ("-col", "-convcol", "-colonly", "-rigid", "-navmesh", "-noimp", "-occ", "-vehicle", "-wheel")
COMPONENT_SIZE = {5120: 1, 5121: 1, 5122: 2, 5123: 2, 5125: 4, 5126: 4}
TYPE_COUNT = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT2": 4, "MAT3": 9, "MAT4": 16}


def load(path):
    with open(path, "rb") as fh:
        data = fh.read()
    if data[:4] == b"glTF":
        magic, version, length = struct.unpack_from("<4sII", data, 0)
        offset = 12
        gltf, bins = None, []
        while offset < length:
            chunk_len, chunk_type = struct.unpack_from("<II", data, offset)
            offset += 8
            chunk = data[offset:offset + chunk_len]
            offset += chunk_len
            if chunk_type == 0x4E4F534A:  # JSON
                gltf = json.loads(chunk.decode("utf-8").rstrip(" \x00\r\n\t"))  # spec pads with spaces; some exporters use NULs
            elif chunk_type == 0x004E4942:  # BIN
                bins.append(chunk)
        return gltf, bins, os.path.dirname(path)
    gltf = json.loads(data.decode("utf-8"))
    return gltf, [], os.path.dirname(path)


def accessor_minmax(gltf, idx):
    acc = gltf["accessors"][idx]
    return acc.get("min"), acc.get("max"), acc.get("count", 0)


def tri_count(gltf, prim):
    mode = prim.get("mode", 4)
    if "indices" in prim:
        n = gltf["accessors"][prim["indices"]]["count"]
    else:
        n = gltf["accessors"][prim["attributes"]["POSITION"]]["count"]
    if mode == 4:
        return n // 3
    if mode in (5, 6):
        return max(n - 2, 0)
    return 0  # points / lines


def near(a, b, eps=1e-4):
    return all(abs(x - y) <= eps for x, y in zip(a, b))


def image_dims(gltf, bins, base, img):
    """Width/height for PNG or JPEG images, embedded or external, when cheaply readable."""
    blob = None
    if "bufferView" in img:
        bv = gltf["bufferViews"][img["bufferView"]]
        if bins and bv.get("buffer", 0) == 0:
            start = bv.get("byteOffset", 0)
            blob = bins[0][start:start + bv["byteLength"]]
    elif "uri" in img and not img["uri"].startswith("data:"):
        p = os.path.join(base, img["uri"])
        if os.path.isfile(p):
            with open(p, "rb") as fh:
                blob = fh.read(65536)
    if not blob:
        return None
    if blob[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", blob[16:24])
        return w, h
    if blob[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(blob):
            if blob[i] != 0xFF:
                i += 1
                continue
            marker = blob[i + 1]
            if marker in (0xC0, 0xC1, 0xC2):
                h, w = struct.unpack(">HH", blob[i + 5:i + 9])
                return w, h
            seg_len = struct.unpack(">H", blob[i + 2:i + 4])[0]
            i += 2 + seg_len
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--budget", type=int, help="triangle budget for the whole file")
    ap.add_argument("--expect-height", type=float, help="expected height in metres (Y extent)")
    ap.add_argument("--tolerance", type=float, default=0.15, help="fraction of expected height allowed (default 0.15)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    gltf, bins, base = load(args.file)
    if gltf is None:
        print("not a glTF/GLB file", file=sys.stderr)
        return 2
    warnings = []
    report = {"file": args.file, "generator": gltf.get("asset", {}).get("generator"), "nodes": [], "meshes": [], "materials": [], "textures": [], "animations": [], "skins": []}

    # nodes
    for i, n in enumerate(gltf.get("nodes", [])):
        name = n.get("name", "node%d" % i)
        entry = {"name": name, "mesh": n.get("mesh"), "skin": n.get("skin"), "children": len(n.get("children", []))}
        t, r, s = n.get("translation"), n.get("rotation"), n.get("scale")
        if "matrix" in n:
            entry["matrix"] = True
            warnings.append("node %s uses a matrix transform — apply transforms on export so scale/rotation are explicit" % name)
        if t and not near(t, [0, 0, 0]):
            entry["translation"] = t
        if r and not near(r, [0, 0, 0, 1]):
            entry["rotation"] = r
        if s and not near(s, [1, 1, 1]):
            entry["scale"] = s
            if "mesh" in n or n.get("children"):
                warnings.append("node %s has scale %s — Godot imports it scaled; apply scale in the source (should be 1,1,1)" % (name, s))
        hints = [suf for suf in GODOT_SUFFIXES if name.endswith(suf)]
        if hints:
            entry["godot_hint"] = hints[0]
        report["nodes"].append(entry)

    # meshes
    total_tris = 0
    bbox_min, bbox_max = None, None
    has_skin_nodes = any(n.get("skin") is not None for n in gltf.get("nodes", []))
    for i, m in enumerate(gltf.get("meshes", [])):
        me = {"name": m.get("name", "mesh%d" % i), "primitives": []}
        for p in m.get("primitives", []):
            attrs = p.get("attributes", {})
            tris = tri_count(gltf, p)
            total_tris += tris
            pe = {"triangles": tris, "attributes": sorted(attrs.keys()), "material": p.get("material")}
            if "POSITION" in attrs:
                mn, mx, _ = accessor_minmax(gltf, attrs["POSITION"])
                if mn and mx:
                    pe["min"], pe["max"] = mn, mx
                    bbox_min = mn if bbox_min is None else [min(a, b) for a, b in zip(bbox_min, mn)]
                    bbox_max = mx if bbox_max is None else [max(a, b) for a, b in zip(bbox_max, mx)]
            if "NORMAL" not in attrs:
                warnings.append("mesh %s: primitive has no NORMAL — Godot will generate flat normals; export normals" % me["name"])
            if "TEXCOORD_0" not in attrs and p.get("material") is not None and gltf["materials"][p["material"]].get("pbrMetallicRoughness", {}).get("baseColorTexture"):
                warnings.append("mesh %s: textured material but no TEXCOORD_0 (UVs)" % me["name"])
            if "JOINTS_0" in attrs and not has_skin_nodes:
                warnings.append("mesh %s: has skin weights but no node references a skin" % me["name"])
            me["primitives"].append(pe)
        if len(m.get("primitives", [])) > 4:
            warnings.append("mesh %s: %d primitives (= %d surfaces / draw calls) — merge materials if possible" % (me["name"], len(m["primitives"]), len(m["primitives"])))
        report["meshes"].append(me)
    report["triangles_total"] = total_tris
    if args.budget and total_tris > args.budget:
        warnings.append("triangle count %d exceeds budget %d" % (total_tris, args.budget))

    # bbox / pivot
    if bbox_min and bbox_max:
        size = [b - a for a, b in zip(bbox_min, bbox_max)]
        report["bbox"] = {"min": bbox_min, "max": bbox_max, "size_m": size}
        if size[1] > 0 and abs(bbox_min[1]) > 0.02 and abs(bbox_min[1]) > 0.05 * size[1]:
            warnings.append("pivot: bbox min.y = %.3f m — for a floor-standing asset the base should sit at y=0 (centre-bottom pivot)" % bbox_min[1])
        if max(size) > 50:
            warnings.append("bbox extent %.1f — is this in centimetres? Godot expects metres" % max(size))
        if max(size) < 0.01:
            warnings.append("bbox extent %.4f — asset is tiny; check unit scale" % max(size))
        if args.expect_height:
            lo, hi = args.expect_height * (1 - args.tolerance), args.expect_height * (1 + args.tolerance)
            if not (lo <= size[1] <= hi):
                warnings.append("height %.3f m outside expected %.2f ± %.0f%%" % (size[1], args.expect_height, args.tolerance * 100))

    # materials / textures
    for i, mat in enumerate(gltf.get("materials", [])):
        pbr = mat.get("pbrMetallicRoughness", {})
        report["materials"].append({
            "name": mat.get("name", "material%d" % i),
            "baseColorTexture": "baseColorTexture" in pbr,
            "metallicRoughnessTexture": "metallicRoughnessTexture" in pbr,
            "normalTexture": "normalTexture" in mat,
            "emissive": "emissiveTexture" in mat or any(mat.get("emissiveFactor", [0, 0, 0])),
            "alphaMode": mat.get("alphaMode", "OPAQUE"),
            "doubleSided": mat.get("doubleSided", False),
        })
    for i, img in enumerate(gltf.get("images", [])):
        dims = image_dims(gltf, bins, base, img)
        te = {"name": img.get("name", img.get("uri", "image%d" % i)), "embedded": "bufferView" in img or str(img.get("uri", "")).startswith("data:"), "dims": dims}
        if dims:
            w, h = dims
            if (w & (w - 1)) or (h & (h - 1)):
                warnings.append("texture %s is %dx%d — not power of two; some compression modes and mipmaps need it" % (te["name"], w, h))
            if max(w, h) > 2048:
                warnings.append("texture %s is %dx%d — above 2k; check the bible's texture budget" % (te["name"], w, h))
        report["textures"].append(te)

    # animations / skins
    for a in gltf.get("animations", []):
        dur = 0.0
        for s in a.get("samplers", []):
            _, mx, _ = accessor_minmax(gltf, s["input"])
            if mx:
                dur = max(dur, mx[0])
        report["animations"].append({"name": a.get("name"), "channels": len(a.get("channels", [])), "duration_s": round(dur, 3)})
    for s in gltf.get("skins", []):
        report["skins"].append({"name": s.get("name"), "joints": len(s.get("joints", []))})
        if len(s.get("joints", [])) > 120:
            warnings.append("skin %s has %d joints — heavy; check the rig family budget" % (s.get("name"), len(s["joints"])))

    report["warnings"] = warnings
    if args.json:
        print(json.dumps(report, indent=2))
        return 0

    print("%s  (generator: %s)" % (args.file, report["generator"] or "unknown"))
    print("triangles: %d%s" % (total_tris, ("  / budget %d" % args.budget) if args.budget else ""))
    if "bbox" in report:
        sz = report["bbox"]["size_m"]
        print("bbox size (m): %.3f x %.3f x %.3f   min: %s" % (sz[0], sz[1], sz[2], ["%.3f" % v for v in report["bbox"]["min"]]))
    print("nodes (%d):" % len(report["nodes"]))
    for n in report["nodes"]:
        extra = []
        for k in ("translation", "rotation", "scale"):
            if k in n:
                extra.append("%s=%s" % (k, ["%.3f" % v for v in n[k]]))
        if n.get("godot_hint"):
            extra.append("godot:%s" % n["godot_hint"])
        if n.get("mesh") is not None:
            extra.append("mesh#%s" % n["mesh"])
        if n.get("skin") is not None:
            extra.append("skin#%s" % n["skin"])
        print("  %-30s %s" % (n["name"], " ".join(extra)))
    print("meshes (%d):" % len(report["meshes"]))
    for m in report["meshes"]:
        for p in m["primitives"]:
            print("  %-30s %6d tris  attrs=%s  mat#%s" % (m["name"], p["triangles"], ",".join(p["attributes"]), p["material"]))
    if report["materials"]:
        print("materials (%d):" % len(report["materials"]))
        for m in report["materials"]:
            flags = [k for k in ("baseColorTexture", "metallicRoughnessTexture", "normalTexture", "emissive", "doubleSided") if m[k]]
            print("  %-30s %s %s" % (m["name"], m["alphaMode"], ",".join(flags)))
    if report["textures"]:
        print("textures (%d):" % len(report["textures"]))
        for t in report["textures"]:
            print("  %-30s %s%s" % (t["name"], ("%dx%d" % t["dims"]) if t["dims"] else "?", " embedded" if t["embedded"] else ""))
    if report["animations"]:
        print("animations (%d):" % len(report["animations"]))
        for a in report["animations"]:
            print("  %-30s %d channels  %.2fs" % (a["name"], a["channels"], a["duration_s"]))
    if report["skins"]:
        print("skins: " + ", ".join("%s (%d joints)" % (s["name"], s["joints"]) for s in report["skins"]))
    if warnings:
        print("\nWARNINGS (%d):" % len(warnings))
        for w in warnings:
            print("  ! " + w)
    else:
        print("\nno warnings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
