# Trailer construction

Tier **BEST PRACTICE** unless marked. Official encode specs, ordering, and conversion rules
are in `steam-store-page/references/steam-requirements.md`.

## Write the timeline first

A trailer assembled from good clips becomes a tour. A trailer built to a beat sheet becomes an
argument. Write the sheet before capturing anything — what each beat is *proving*, not what it
shows:

```
0:00–0:03   HOOK                 the single most interesting second of the game, cold
0:03–0:08   SIGNATURE MECHANIC   the thing no competitor has, demonstrated not described
0:08–0:13   SECOND HIGHLIGHT     a different verb, so the game reads as deep
0:13–0:18   CHAOS / THREAT       what can go wrong — stakes, or the social moment
0:18–0:28   VARIETY              two or three fast cuts proving breadth
0:28–0:35   PEAK                 the clip a streamer would clip
0:35–end    TITLE + CTA          logo, wishlist / demo, store beat
```

**Do not apply those timings as written.** They are a starting shape; the real duration comes
from how much genuinely compelling material exists. A game with 25 seconds of real hook makes
a better 25-second trailer than a padded 50-second one, and padding is visible — it shows up
as shots held two beats too long. `[OFFICIAL]` Valve sets no length limit and no trailer count
limit, so every number here is a choice, not a constraint.

Four or five gameplay highlights inside the first fifteen seconds is the load-bearing part of
the recommendation. Attention is lost early or not at all.

## The opening

The first three seconds answer one question: **what is interesting about this game?** Anything
that delays the answer is cut, however much work it was:

- long studio or publisher logos — put them at the end, or at most one second at the start;
- slow fades from black;
- text-heavy lore introductions;
- establishing shots of an environment where nothing happens;
- a menu, a loading screen, or a character creator.

Cold open on motion. If the game's hook is slow by nature — a management game, a horror game
built on dread — the opening still has to *show* that in a way that is interesting at speed,
usually by showing its consequence rather than its build-up.

## Shot discipline

- **Short shots.** If a shot has made its point, it is over. Most first-time trailer cuts hold
  every shot about a second too long; try cutting a third off and see what breaks.
- **One idea per shot.** A shot proving two things proves neither at this speed.
- **Gameplay over cinematics.** `[OFFICIAL — Valve's recommendation]` the first trailer should
  be primarily gameplay, and in-game HUD elements "are often beneficial". A cinematic the game
  does not contain is a promise it cannot keep.
- **It must work muted.** Most first views are silent. Mute your own cut and watch it: if the
  hook lands only with the music, the picture is not carrying it yet. Captions carry
  information that audio would otherwise own — sparingly, and they cost a re-render per
  language.
- **End with one clear action.** Title, then wishlist, demo, or release date — one of them,
  not all three. `[OFFICIAL]` Keep "available on" date claims out of capsules; in a trailer
  they are fine but they date the asset.

## Capture

Capture in-engine and deterministically, so the cut can be revised:

- stage the scene the way `references/screenshots.md` describes — fixed setup, known lighting,
  debug UI off, a repeatable camera path;
- record at the target resolution or above, at a constant frame rate, with v-sync behaviour
  settled — a trailer cut from stutter cannot be fixed in the edit;
- keep the project state that produced each clip (scene, seed, save) recorded on the registry
  entry, so a re-capture six weeks later matches;
- capture more than the beat sheet needs for the beats you are least sure about, and nothing
  for the beats you are sure about. Shooting everything is how a trailer takes three days.

## Export and upload

`[OFFICIAL]` 1920x1080 or 1280x720, 30/29.97 or 60/59.94 fps, 5,000+ Kbps, .mp4 / .mov /
.wmv, H.264 + AAC, 16:9, 44 or 48 kHz audio. The first two trailers appear before the
screenshots; the rest after. A custom poster frame must be a real frame from the video at
1920x1080 — pick one with unique content and no text.

**A game cannot be released while a trailer is still converting.** Upload with slack before
any date that matters.

Produce the YouTube-ready version in the same session — same cut, different encode target and
a thumbnail — because the distribution copy is what the Discord post, the press email, and the
creator pitch all link to.

## Record it

One registry entry per trailer (`--type trailer --hero`), with the beat sheet as the spec, the
source project file and the export recorded as files, and the user's approval of the cut as
the `review approve`. Rejected cuts keep their note: "too slow to the mechanic" is information
the next cut needs.
