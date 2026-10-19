# Screenshots and clips — staging and capture in Godot

Tier **BEST PRACTICE** for the method; the official minimums (5 screenshots, 1920x1080, 16:9,
gameplay only, four marked all-ages) are in
`steam-store-page/references/steam-requirements.md`.

## Every screenshot has a job

Write the narrative before capturing. A set of nine images where three show the same thing is
a set of seven. Give each slot a job, then capture to the job:

```
01 — Core gameplay          the main thing the player does, unmistakable at a glance
02 — Signature mechanic     the one thing no competitor has
03 — Threat / challenge      what can go wrong — stakes
04 — Player interaction      the social or systemic moment
05 — Environment variety     proof the game is not one room
06 — Progression / depth     proof there is a reason to keep playing
07 — High-intensity moment   the one the player imagines themselves in
```

Adapt to the game. Then check the set as a set: the palettes, environments, and compositions
must differ. Seven images of the same corridor in the same light read as one image, however
good each is.

Rules that come from the medium:

- **Real gameplay, from the player's camera.** Not a posed render, not a cinematic frame.
- **Representative UI stays in.** A HUD-less screenshot sells a game that does not exist, and
  Valve notes HUD elements are often beneficial.
- **No menus** `[OFFICIAL]` unless a menu is genuinely a distinctive component of the game.
- **Accurate, not flattering.** Every screenshot is a promise that gets checked against the
  build.

## The staging sheet

One per screenshot, in the registry entry's spec or alongside `STORE.md`. Specific enough that
a different session reproduces the shot without the conversation:

```markdown
### STORE_SHOT_03 — Threat
Purpose:              Show that the stalker hunts by sound, so the quiet moments read as tense
Feature demonstrated: Creature AI awareness state + the audio-visual tell
Location:             res://levels/mansion/ground_floor.tscn, dining room doorway
Required setup:       Player at marker SHOT_03_PLAYER; stalker spawned at SHOT_03_STALKER in
                      ALERT; one dropped prop mid-roll; lights at night preset
Camera:               Player camera, FOV 70, eye height 1.6 m, yaw 212 deg
UI:                   HUD on; debug overlays off; subtitle off
Lighting:             Night preset, moon only, no flashlight
Capture notes:        Frame so the creature occupies the right third in silhouette; capture on
                      the second frame after the lamp flicker so the rim light is present
```

The sheet is the deliverable that makes a capture session repeatable. A screenshot nobody can
re-take is a screenshot you cannot improve.

## Capture in Godot 4

**`--headless` cannot take screenshots.** It uses the dummy display and rendering drivers, so
there is no rendered frame to read. Capture needs a real windowed run on a machine with a
display. Say this rather than producing an empty PNG and calling it done.

Verify the flags and API names against the project's own Godot version before relying on them
(`godot --version`); these are current for Godot 4.x and the hook injects the project's actual
version every prompt.

**Capture script** — attach to a capture scene, or run as an autoload in a capture build:

```gdscript
extends Node

@export var out_dir: String = "res://art/store/shots"

func capture(shot_id: String) -> void:
    # The frame must be drawn before the texture can be read.
    await RenderingServer.frame_post_draw
    var img: Image = get_viewport().get_texture().get_image()
    img.save_png("%s/%s.png" % [out_dir, shot_id])
```

**Force the output resolution** so the capture is 1920x1080 regardless of the window the
machine can show. Either set it on the command line:

```bash
godot --path . --resolution 1920x1080 res://tools/capture_shots.tscn
```

or render through a `SubViewport` sized 1920x1080 and read *its* texture — which is the
reliable route when the display cannot show 1080p, and the only route for capturing above the
screen's resolution.

**Make it deterministic.** A shot you cannot reproduce is a shot you cannot fix:

- seed the RNG (`seed(12345)`) in the capture scene's `_ready`;
- place the player and the actors from named markers, never by playing to the moment;
- freeze or step time deliberately — `Engine.time_scale`, or `--fixed-fps` with a fixed number
  of ticks before the capture — so particles and animations land on the same frame every run;
- hide debug overlays explicitly rather than hoping they are off: keep them on one
  `CanvasLayer` and set `visible = false` in the capture setup;
- record the scene, markers, and seed on the registry entry.

**Batch the set.** One capture scene that walks the staging sheets, captures each, and writes
`STORE_SHOT_01.png` … is worth the hour it costs: the whole set gets re-captured consistently
after any art change, instead of drifting into a mix of old and new builds. A mixed-build
screenshot set is a common and very visible way for a page to look careless.

## Animated showcases for the About section

Same staging method, shorter, and one gate before anything is produced:

> **What is this proving?**

Write the answer down. Core mechanic, movement, combat, physics, multiplayer interaction,
building, destruction, progression, enemy behaviour — one per showcase. "Movement looks nice"
is not an answer; "the grapple cancels fall damage, which is the whole traversal skill
ceiling" is.

- Keep each loop short and looping cleanly — the viewer sees it two or three times.
- `[OFFICIAL]` under 5 MB each, and all screenshots and GIFs together under 15 MB. That budget
  is the real limit on how many you get, so spend it on the two or three that prove the most.
- Keep them textless so localization does not mean re-rendering
  `[OFFICIAL — Valve's recommendation]`.
- The display width that fits the description column is not documented — render at a sensible
  width and check it in the store preview rather than trusting a remembered number.

For longer captures, **Godot 4's Movie Maker mode** writes frames deterministically rather
than recording the screen, which is what makes a clean loop possible:

```bash
godot --path . --write-movie out.avi res://tools/showcase_grapple.tscn
```

It writes MJPEG AVI, or a PNG sequence if the path ends in `.png`; frame rate and quality come
from the `editor/movie_writer/` project settings. Check the flags against your version, then
cut and encode with `ffmpeg`. Because it is frame-locked rather than real-time, the result has
no stutter and the same run produces the same frames — the opposite of a screen recorder.
