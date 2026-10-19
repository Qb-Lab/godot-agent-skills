#!/usr/bin/env python3
"""Check a store image against Steam's asset slots, and build the thumbnail ladder.

A capsule is judged at the size players see it, not at the size it was made. This script
does the mechanical half of that: it reads the image's real dimensions without any
third-party library, matches them against every official Steam slot, reports the mismatches
that waste an export, and with --ladder writes the small, tiny, greyscale and blurred
versions so the judgement happens on the right images.

Downscaling needs a tool. It uses whichever of sips (macOS), ImageMagick, or ffmpeg is on
PATH; with none of them it prints the exact commands instead of pretending it worked.

The slot sizes below were read from Steamworks on 2026-10-19. Steam changes them. Re-read
https://partner.steamgames.com/doc/store/assets/standard before any export.

Python 3.8+, standard library only.
"""
import argparse
import os
import shutil
import struct
import subprocess
import sys

CHECKED = "2026-10-19"
DOC = "https://partner.steamgames.com/doc/store/assets/standard"

# name -> (width, height, required, note)
SLOTS = {
    "main":            (1232, 706, True,  "Main capsule"),
    "header":          (920, 430,  True,  "Header capsule — smaller versions generated from it"),
    "small":           (462, 174,  True,  "Small capsule — 184x69 and 120x45 generated from it"),
    "vertical":        (748, 896,  True,  "Vertical capsule"),
    "screenshot":      (1920, 1080, True, "Screenshot — this is the MINIMUM; 16:9, larger is fine"),
    "page-background": (1438, 810, False, "Page background — ambient; Steam overlays a template"),
    "bundle-header":   (707, 232,  False, "Bundle header — required for bundles only"),
    "library-capsule": (600, 900,  True,  "Library capsule — logo plus optional subtitle only"),
    "library-header":  (920, 430,  True,  "Library header — falls back to the store header"),
    "library-hero":    (3840, 1240, True, "Library hero — safe area 860x380 centred, no text at all"),
    "library-logo":    (1280, 720, True,  "Library logo — 1280 wide and/or 720 tall, transparent PNG"),
    "trailer-poster":  (1920, 1080, False, "Custom trailer poster — must be a real frame of the video"),
}

# Steam generates these from the small capsule; everything eventually shows up tiny.
GENERATED = [(184, 69), (120, 45)]

# Two slots are not exact-size rules, so they get their own predicates rather than ==.
#   screenshot   — 1920x1080 is a documented MINIMUM at 16:9; larger is accepted
#   library-logo — "either 1280px wide and/or 720px tall", transparent PNG
FLEXIBLE = {
    "screenshot": (
        lambda w, h: w >= 1920 and h >= 1080 and abs(aspect(w, h) - 16 / 9) < 0.01,
        "at least 1920x1080 and 16:9",
    ),
    "library-logo": (
        lambda w, h: w == 1280 or h == 720,
        "1280px wide and/or 720px tall",
    ),
}

# Documented only for images embedded in the store description.
DESC_IMAGE_MAX_BYTES = 5 * 1024 * 1024


# ------------------------------------------------------------------ image dimensions

def png_size(fh):
    fh.seek(0)
    if fh.read(8) != b"\x89PNG\r\n\x1a\n":
        return None
    length, kind = struct.unpack(">I4s", fh.read(8))
    if kind != b"IHDR":
        return None
    w, h = struct.unpack(">II", fh.read(8))
    bit_depth, colour_type = struct.unpack(">BB", fh.read(2))
    # colour types 4 and 6 carry an alpha channel; 3 may via tRNS, which we do not scan for.
    return w, h, "PNG", colour_type in (4, 6)


def jpeg_size(fh):
    fh.seek(0)
    if fh.read(2) != b"\xff\xd8":
        return None
    sof = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
    while True:
        byte = fh.read(1)
        if not byte:
            return None
        if byte != b"\xff":
            continue
        marker = fh.read(1)
        while marker == b"\xff":          # fill bytes are legal
            marker = fh.read(1)
        if not marker:
            return None
        code = marker[0]
        if code in (0xD8, 0x01) or 0xD0 <= code <= 0xD7:
            continue                       # no payload
        payload = fh.read(2)
        if len(payload) < 2:
            return None
        (seg_len,) = struct.unpack(">H", payload)
        if code in sof:
            data = fh.read(min(seg_len - 2, 5))
            if len(data) < 5:
                return None
            h, w = struct.unpack(">HH", data[1:5])
            return w, h, "JPEG", False
        fh.seek(seg_len - 2, os.SEEK_CUR)


def read_size(path):
    with open(path, "rb") as fh:
        for reader in (png_size, jpeg_size):
            try:
                got = reader(fh)
            except (struct.error, OSError):
                got = None
            if got:
                return got
    return None


# ------------------------------------------------------------------ reporting

def aspect(w, h):
    return w / h if h else 0.0


def match_slots(w, h):
    exact = []
    for name, (sw, sh, _, _) in SLOTS.items():
        if name in FLEXIBLE:
            if FLEXIBLE[name][0](w, h):
                exact.append(name)
        elif (w, h) == (sw, sh):
            exact.append(name)
    near = []
    for name, (sw, sh, _, _) in SLOTS.items():
        if name in exact or name in FLEXIBLE:
            continue
        if abs(aspect(w, h) - aspect(sw, sh)) < 0.01:
            near.append(name)
    return exact, near


def report(path, slot_hint):
    size = read_size(path)
    print("== %s" % path)
    if size is None:
        print("   ! cannot read dimensions — only PNG and JPEG are parsed here.")
        print("     Convert, or read the size with your image tool and check it by hand.")
        return 1, None
    w, h, fmt, has_alpha = size
    nbytes = os.path.getsize(path)
    print("   %s %dx%d  aspect %.3f  %.2f MB" % (fmt, w, h, aspect(w, h), nbytes / 1048576))

    problems = 0
    exact, near = match_slots(w, h)

    if slot_hint:
        if slot_hint not in SLOTS:
            print("   ! unknown slot '%s' — see --list-slots" % slot_hint)
            return 1, (w, h)
        sw, sh, _, note = SLOTS[slot_hint]
        if slot_hint in FLEXIBLE:
            predicate, rule = FLEXIBLE[slot_hint]
            if predicate(w, h):
                print("   PASS  matches %s (%s) — %s" % (slot_hint, rule, note))
            else:
                problems += 1
                print("   FAIL  %s needs %s; this is %dx%d" % (slot_hint, rule, w, h))
        elif (w, h) == (sw, sh):
            print("   PASS  matches %s (%dx%d) — %s" % (slot_hint, sw, sh, note))
        else:
            problems += 1
            same_aspect = abs(aspect(w, h) - aspect(sw, sh)) < 0.01
            print("   FAIL  %s needs exactly %dx%d; this is %dx%d" % (slot_hint, sw, sh, w, h))
            if same_aspect:
                print("         aspect is right, so a clean resample fixes it")
            else:
                print("         aspect is wrong (%.3f vs %.3f) — this needs re-composing, not"
                      " cropping: a crop moves the logo out of the composition it was made for"
                      % (aspect(w, h), aspect(sw, sh)))
    elif exact:
        for name in exact:
            print("   PASS  matches %s (%s)" % (name, SLOTS[name][3]))
    else:
        problems += 1
        print("   FAIL  matches no Steam slot exactly.")
        if near:
            print("         same aspect as: %s — resample to that slot's size" % ", ".join(sorted(near)))
        else:
            print("         no slot shares this aspect either; pick the target slot first,"
                  " then compose for it")

    if nbytes > DESC_IMAGE_MAX_BYTES:
        print("   note  over 5 MB. That is the documented limit for images embedded in the"
              " store description (15 MB for all of them together); capsule slots have no"
              " documented size limit, so this only blocks description use.")

    effective = [slot_hint] if slot_hint else exact
    if has_alpha and "library-logo" not in effective:
        print("   note  has an alpha channel. Only the library logo is meant to be"
              " transparent; a capsule with transparency composites against Steam's dark UI"
              " in ways you did not design. Flatten it.")

    if slot_hint in ("library-hero",):
        print("   note  safe area is 860x380 centred, and this asset cannot include any text")

    return problems, (w, h)


# ------------------------------------------------------------------ the ladder

def downscaler():
    for tool in ("magick", "convert", "ffmpeg", "sips"):
        if shutil.which(tool):
            return tool
    return None


def scale_cmd(tool, src, dst, w, h, grey=False, blur=False):
    if tool in ("magick", "convert"):
        cmd = [tool, src, "-resize", "%dx%d!" % (w, h)]
        if grey:
            cmd += ["-colorspace", "Gray"]
        if blur:
            cmd += ["-blur", "0x3"]
        return cmd + [dst]
    if tool == "ffmpeg":
        filters = ["scale=%d:%d" % (w, h)]
        if grey:
            filters.append("format=gray")
        if blur:
            filters.append("boxblur=2")
        return [tool, "-y", "-loglevel", "error", "-i", src, "-vf", ",".join(filters), dst]
    if tool == "sips":
        if grey or blur:
            return None       # sips cannot do either reliably
        return [tool, "-z", str(h), str(w), src, "--out", dst]
    return None


def ladder_steps(w, h):
    """(label, width, height, grey, blur) — the sizes a capsule is actually judged at."""
    steps = [("listing", max(1, w // 2), max(1, h // 2), False, False)]
    sw, sh = SLOTS["small"][0], SLOTS["small"][1]
    if abs(aspect(w, h) - aspect(sw, sh)) < 0.01:
        # The small capsule's own generated sizes, exactly as Steam makes them.
        for gw, gh in GENERATED:
            steps.append(("tiny-%dx%d" % (gw, gh), gw, gh, False, False))
    else:
        tiny_w = GENERATED[0][0]
        steps.append(("tiny-%dw" % tiny_w, tiny_w, max(1, int(round(tiny_w * h / w))),
                      False, False))
    small_w = steps[-1][1]
    small_h = steps[-1][2]
    steps.append(("grey", small_w, small_h, True, False))
    steps.append(("squint", max(1, w // 4), max(1, h // 4), False, True))
    return steps


def build_ladder(path, w, h, out_dir):
    tool = downscaler()
    base = os.path.splitext(os.path.basename(path))[0]
    ext = os.path.splitext(path)[1] or ".png"
    os.makedirs(out_dir, exist_ok=True)
    print("   ladder -> %s" % out_dir)
    if tool is None:
        print("   ! no downscaler on PATH (looked for magick, convert, ffmpeg, sips).")
        print("     Install one, or run these by hand:")
    for label, lw, lh, grey, blur in ladder_steps(w, h):
        dst = os.path.join(out_dir, "%s__%s%s" % (base, label, ext))
        cmd = scale_cmd(tool or "magick", path, dst, lw, lh, grey, blur)
        if cmd is None:
            print("     %-16s skipped — %s cannot do this pass; use magick or ffmpeg"
                  % (label, tool))
            continue
        if tool is None:
            print("     " + " ".join(cmd))
            continue
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            print("     %-16s %dx%d  %s" % (label, lw, lh, dst))
        except subprocess.CalledProcessError as exc:
            print("     %-16s FAILED: %s" % (label, exc.stderr.decode("utf-8", "replace").strip()))
    print("   Now look at them. Can you read the title? Is there one focal point? Can you")
    print("   infer the genre? Does it stand out? Does it still look like the actual game?")


# ------------------------------------------------------------------ cli

def main(argv=None):
    p = argparse.ArgumentParser(
        description=__doc__.split("\n\n")[0],
        epilog="Slot sizes read from Steamworks on %s. Re-read %s before exporting."
               % (CHECKED, DOC),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("images", nargs="*", help="PNG or JPEG files to check")
    p.add_argument("--slot", help="check against one named slot (see --list-slots)")
    p.add_argument("--ladder", action="store_true",
                   help="also write the thumbnail ladder: listing, tiny, greyscale, squint")
    p.add_argument("--out", default=None,
                   help="directory for ladder output (default: <image dir>/ladder)")
    p.add_argument("--list-slots", action="store_true", help="print every slot and its size")
    args = p.parse_args(argv)

    if args.list_slots:
        print("Steam asset slots as read from Steamworks on %s — re-read %s\n" % (CHECKED, DOC))
        for name in sorted(SLOTS):
            w, h, required, note = SLOTS[name]
            size = FLEXIBLE[name][1] if name in FLEXIBLE else "%dx%d" % (w, h)
            print("  %-16s %-28s %-9s %s"
                  % (name, size, "required" if required else "optional", note))
        return 0
    if not args.images:
        p.error("give at least one image, or --list-slots")

    problems = 0
    for path in args.images:
        if not os.path.isfile(path):
            print("== %s\n   ! not a file" % path)
            problems += 1
            continue
        bad, size = report(path, args.slot)
        problems += bad
        if args.ladder and size:
            out = args.out or os.path.join(os.path.dirname(os.path.abspath(path)), "ladder")
            build_ladder(path, size[0], size[1], out)
        print("")

    print("Slot sizes were read from Steamworks on %s. They change; re-read %s before you"
          " export anything." % (CHECKED, DOC))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
