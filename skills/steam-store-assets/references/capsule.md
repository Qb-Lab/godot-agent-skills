# Capsule and logo craft

Tier **BEST PRACTICE** unless marked. The official half — sizes, and what text is allowed —
is in `steam-store-page/references/steam-requirements.md`; re-read the Steamworks page before
exporting.

## Compose for the thumbnail, not the poster

The capsule is seen small, briefly, beside competitors, on a dark background, by someone who
is not looking for it. That inverts normal composition instincts:

- **One focal point.** Two competing subjects become mush at 184x69. Decide what the eye lands
  on and subordinate everything else.
- **Silhouette over detail.** A shape readable at thumbnail size survives; rendered detail
  does not — it averages into noise. Let a character, a tool, an effect, or a landmark create
  a strong outline, and allow it to break out of a rigid box if that strengthens the shape.
  **Safe areas and Steam's overlays take priority over any composition idea** — Steam draws
  its own UI over parts of some capsule placements, so check current templates and keep the
  logo and the focal point clear of them.
- **Value separation.** Squint at it: if the subject and background collapse into one tone,
  nothing will read. Fix with value, not with more detail.
- **Dark-background awareness.** Steam's UI is dark. A capsule with dark edges bleeds into the
  page and loses its boundary; a bright rim or a lighter background separates it.

## The logo

A game needs an intentional logotype, not a font choice. Evaluate a treatment on:

- **Silhouette** — the shape of the whole word, which is what gets recognised before any
  letter is read;
- **Custom type treatment** — a modification that ties the type to the game (a cut, a weight,
  a mark, a texture), not a decorative display font applied as-is;
- **Readability** — at 184x69, in greyscale, blurred;
- **Relationship to the game** — the type says something true about the genre and tone;
- **Recognition when small** — would the user spot it in a Twitch thumbnail?

**Simple is usually stronger.** Do not generate an elaborate logo because elaborate looks like
effort; an ornate logo is the first thing to turn to mud at thumbnail size. A clean weight
with one deliberate modification beats five effects.

`[OFFICIAL]` The small capsule should contain a readable logo at the smallest size and the
logo "should nearly fill the small capsule" — so the small capsule is usually a different
composition, not a crop. Treat it as its own design.

**Contrast between logo and art is a hard test, not a taste call.** Put the logo on the art,
export at 184x69, and read it. If it needs a drop shadow to survive, the art behind it is too
busy — fix the art, not the shadow.

## The AI-tell checklist

Generated imagery is a legitimate part of the workflow, and the Art Bible governs it the same
way it governs everything else. What is not acceptable is a capsule that **looks** generated,
because that reads as "nobody cared" to exactly the audience being asked to care. Check for:

- malformed geometry — hands, weapons, architecture that cannot exist;
- nonsensical details that do not survive a second look;
- lighting that disagrees with itself across the image;
- generic composition — centred subject, symmetrical framing, radial glow behind the head;
- over-detailed backgrounds competing with the subject (the classic tell at thumbnail size);
- fake typography — letterforms that are nearly letters;
- a rendering style that does not match the game's actual look;
- the familiar composition patterns of whichever generator made it.

The fix is work, not a re-roll: manual cleanup, compositing the subject onto a simplified
background, repainting the focal area, setting real type, and a human look at full and
thumbnail size. If the image needs more cleanup than a repaint can carry, it is the wrong base
image — generate again with a composition brief rather than rescuing this one.

**The deciding question is not "was this generated?" but "does this look art-directed?"** —
deliberate, consistent with the bible, and like the same hand made the screenshots.

## Text on the capsule

`[OFFICIAL]` Base capsules: game artwork, game name, official subtitle. No review scores, no
awards, no sale copy, no calls to action, no promoting another product, "no other
miscellaneous text". Text-bearing variants exist only as artwork overrides, time-limited and
tied to real new content.

So the capsule communicates with **game art + logo**, and any idea that needs a caption needs
a different idea. Verify the rules page before export — this is the restriction that changed
most recently.

## The border experiment

A subtle border or rim can separate a capsule from its neighbours in a grid of near-identical
dark thumbnails. It can also look like a template. **This is an EXPERIMENT, not a
requirement** — nothing in Valve's rules asks for one.

Run it properly: export the chosen capsule with no border and with a subtle border, drop both
into a real competitor grid screenshot at listing size, and look. Keep the one that holds its
edge. Record the comparison in `STORE.md` so it is not re-argued from taste later.

## The testing ladder

No capsule is approved from its full-size appearance. Render every serious candidate at:

| View | Why |
|---|---|
| Full resolution | craft check only — never the deciding view |
| Normal listing size | how most people meet it |
| ~184x69 | the smallest generated size `[OFFICIAL]`; the honest test |
| On Steam's dark background | boundary and bleed |
| Blurred / squinted | focal hierarchy, with detail removed |
| Greyscale | value structure, independent of colour |
| In a real competitor grid | the only test of standing out |

`scripts/capsule-check.py --ladder` writes these files. Then answer, per candidate:

1. Can I read the title?
2. Is there an obvious focal point?
3. Can I infer the genre and tone?
4. Does it stand out in the grid?
5. Does it still look like the actual game?
6. Does it look professional beside established titles?
7. Does it become visual noise when tiny?

Score them side by side and bring the user the comparison, not a winner. Question 5 is the one
a builder is least able to answer about its own work — flag it for `steam-store-review`.
