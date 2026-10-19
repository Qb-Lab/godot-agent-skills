# Official Steam requirements — what Valve actually asks for

**Everything on this page is tier OFFICIAL and was read from Steamworks documentation on
2026-10-19.** It is a starting point and a re-check list, not authority. Steam changes asset
slots, limits, and review timings without announcement, so **re-read the linked page before
anyone exports a file or commits to a date**, and update the date line above when you do.
If you cannot browse in this session, mark every line below `NEEDS VERIFICATION` and say so in
the output — do not let a 1232x706 export happen on the strength of this file alone.

Anything *not* on this page is not an official requirement. Screenshot counts above five,
trailer lengths, capsule borders, and tag counts above the minimum are best practice or
experiment. Keep them labelled that way.

## Store graphical assets

<https://partner.steamgames.com/doc/store/assets/standard>

| Asset | Status | Size | Notes |
|---|---|---|---|
| Header capsule | Required | 920 x 430 | Smaller versions are generated from it |
| Small capsule | Required | 462 x 174 | **120 x 45 and 184 x 69 are generated automatically** — the logo must stay readable at the smallest |
| Main capsule | Required | 1232 x 706 | |
| Vertical capsule | Required | 748 x 896 | |
| Screenshots | Required, **minimum 5** | 1920 x 1080 minimum, 16:9 | |
| Page background | Optional | 1438 x 810 | Should be ambient; Steam applies a template over it |
| Bundle header | Required for bundles | 707 x 232 | Branding-focused; logo legible |

Valve's own wording on the capsules: "Do not include quotes or other strings of text beyond
the title of your game", and "The game's logotype should be easily legible against the
background". For the small capsule: it "should contain readable logo, even at smallest size"
and "your logo should nearly fill the small capsule".

On screenshots: "Screenshots should exclusively show the gameplay of your game" and "Menu
screens should only be included if they are a unique component of your game". At least four
must be marked suitable for all ages — suitable ones "should not contain gore, violence, or
suggestive themes".

Note what this means for the common advice: the 7-screenshot guidance is **best practice**;
five is the requirement. The "no menu screenshots" guidance is **official**.

## Graphical asset rules — what may appear on a capsule

<https://partner.steamgames.com/doc/store/assets/rules> (in effect since 2022-09-01)

Base capsules are limited to "game artwork, the game name, and any official subtitle".
Specifically prohibited:

- review scores of any kind, including Steam's own;
- award names, symbols, or logos;
- discount or sale copy ("On Sale Now", "Up to 90% off");
- calls to action ("Prepurchase Now", "Wishlisting now available");
- text or imagery promoting a different product, including sequels and other titles in the
  same franchise;
- "no other miscellaneous text".

Capsules must carry a readable product logo/name, have accurate dimensions, and be PG-13
appropriate. Non-compliant games "may have limits to visibility within the Steam store" and
are ineligible for featuring in official sales and events.

Text-bearing capsules exist but only as **artwork overrides**, limited to one month, only for
content currently available (a major update, seasonal event, battle pass, DLC), localized into
at least the languages the game supports — and still never for "Wishlist now!" or a date.

Review quotes, scores, and awards have their own place: store page accolades, not the capsule.

## Library assets

<https://partner.steamgames.com/doc/store/assets/libraryassets>

Only visible once the store page is published, but required for release.

| Asset | Size | Rule |
|---|---|---|
| Library capsule | 600 x 900 | Logo plus optional subtitle; "no other text should be present" |
| Library header | 920 x 430 | Falls back to the store header capsule if unset |
| Library hero | 3840 x 1240 | Safe area 860 x 380 centred; "this image cannot include any text" |
| Library logo | 1280 wide and/or 720 tall, transparent PNG | Logotype plus optional logomark only; positionable left-bottom, centre-top, centre-middle, centre-bottom |

## Trailers

<https://partner.steamgames.com/doc/store/trailer>

- Up to 1920 x 1080; 1280 x 720 is called out as avoiding processing problems.
- 30/29.97 or 60/59.94 fps; 5,000+ Kbps; .mov, .wmv, or .mp4; H.264 video with AAC audio
  preferred; 16:9 preferred, 4:3 accepted; 44 or 48 kHz audio (other rates cause errors).
- **No length limit and no maximum trailer count** — every length recommendation is best
  practice, not a rule.
- The first two valid trailers appear *before* the screenshots; the rest appear after. Order
  is drag-and-drop. Deleting and resubmitting sends a trailer to the back of the queue.
- Steam generates a 600 x 380 poster and a 232 x 130 thumbnail; a custom poster must be a
  frame from the video itself, 1920 x 1080, .jpg or .png.
- Gameplay is **not required**, but Valve recommends the first trailer be primarily gameplay
  and notes in-game HUD elements are often beneficial.
- **You cannot release while a trailer is still converting.** Budget for this.

## Written description fields

<https://partner.steamgames.com/doc/store/page/description>

- **Short description:** plain text only, no formatting, "limited to a few hundred
  characters". Steamworks shows the field's own live counter — read that counter rather than
  trusting any number from memory. Valve advises against time-based text such as "Now
  Available" or "Prepurchase now".
- **About This Game:** longer, with formatting, and can embed images.
- Images must be under 5 MB each, and all screenshots and GIFs together under 15 MB. Valve
  recommends textless images because text in an image has to be re-made per language.
- **No links out** — not in text, not via embedded images, QR codes, or implied URLs. Website
  and social links go in the link fields under Basic Info.
- **No mimicking the Steam UI** — no fake wishlist or buy buttons, mock capsules, or faux
  pricing overlays.
- **No advertising other games** in the description. Related products belong in the DLC or
  "More From" sections.

The embedded-image width that fits the description column is **not specified in the docs** —
treat any specific pixel width as best practice and check how it renders in preview.

## Tags

<https://partner.steamgames.com/doc/store/tags>

- **At least 5 tags are required before launch**; Valve recommends up to 20. Only the top 20
  are visible and used for store visibility.
- Order is weight: "the tags given the most weight govern your visibility more than those
  given less", and "some store filters prioritize the first 15 tags", so rank deliberately.
- Player tags combine with the developer's and shift the order over time; developers can
  remove tags that do not fit the game.
- The Tag Wizard's "Suggest Prioritization" is explicitly "not guaranteed to be accurate
  because it has no knowledge of what your game is actually like".

## Release date and the Coming Soon page

<https://partner.steamgames.com/doc/store/coming_soon> ·
<https://partner.steamgames.com/doc/store/release_dates>

- **A Coming Soon page must be live for at least two weeks before release.**
- The page needs Valve's approval first: mark it ready for review and submit **at least 7
  business days** before you want it live. Everything in the "Your Store Presence" section is
  required before posting.
- Branding images and a written description are needed; a gameplay trailer is recommended.
- Public date granularity: exact date, month and year, quarter, year, or no date ("Coming
  Soon"). An exact internal date is required regardless, and is not shown to players.
- **The date can be changed up to two weeks before it.** Inside that window the game starts
  appearing in upcoming lists and the date is frozen.
- Upcoming lists sort a game at the **last possible date of its display range** — "August
  2026" sorts as 31 August, a quarter as its final day, and no date sorts behind everything
  specific. Vagueness has a real placement cost, which is the argument for the most precise
  granularity production can honestly support.
- The date picker hides weekends; weekend releases are allowed but discouraged because Valve
  support may be unavailable.

## Re-check protocol

Before an export or a commitment, re-read the page that covers it and record the date:

```markdown
| Requirement | Source | Read on | Status |
|---|---|---|---|
| Main capsule 1232x706 | partner.steamgames.com/doc/store/assets/standard | 2026-10-19 | PASS |
| Coming Soon live 2 weeks before release | .../doc/store/coming_soon | 2026-10-19 | NEEDS VERIFICATION |
```

`NEEDS VERIFICATION` is the honest default for anything you did not read today. It is not a
failure state — it is the difference between a compliance table and a guess.
