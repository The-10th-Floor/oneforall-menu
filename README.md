# One For All — digital menu

Live: https://the-10th-floor.github.io/oneforall-menu/

This URL is written on the NFC tag at the ordering window (and printed as `qr.svg` / `qr.png`). **Never change the URL.** Change the menu behind it instead.

## Two pages, two jobs
| Page | For | What is on it |
|---|---|---|
| `/` — **the tap page** (`index.html`, kept by hand) | the customer at the window | the menu card, which lands in six panels, and the language switch — **nothing else shows**. The link to the landing page is in the page for screen readers and keyboards only (founder, 2026-09-19: the NFC menu is the menu, no extra line). The **My card** button appears once loyalty is live |
| `/irbid/` — **the landing page** (`irbid/index.html`, **generated**) | Google, Maps, anyone arriving from Instagram | the menu as real text with prices, set as their printed card; the `Restaurant` + `Menu` schema, Directions, Instagram. The whole page is one directed scroll on professional material only, nobody in frame: the lane walked into our red screen (`irbid/film/`), a crash zoom into its red, the OFA studio photograph (`irbid/scene/`), the menu dealt as the card, Find us. The motion runs on CSS scroll timelines, so it stays smooth on slow machines; browsers without them get each scene still and finished. This is the Website and Menu link for the Google Business Profile, and the canonical URL of both pages |

One menu per page: a customer never sees the card and the text stacked. `irbid/index.html` is written by `node fill.mjs` in the `nst-irbid-geo` repo (template `templates/oneforall-index.html`, values from `DATA.json`) — do not edit it here; edit the template, run `node fill.mjs --force`, copy `out/oneforall-index.html` over it.

**Loyalty:** both pages have `const LOYALTY_URL = ''` near the top of their script. While it is empty the *My card* button does not exist. Set it to the deployed address of `oneforall-loyalty` (tap page here, landing page in the template) and the button appears.

## Update the menu
1. Drop the new PDF into `source/` (page 1 English, page 2 Arabic, A5).
2. `pip install pymupdf` once, then `python render.py source/<new>.pdf`. It writes `menu-en.svg` / `menu-ar.svg` (what the page shows) and the two PNGs (link preview + no-JavaScript fallback).
3. Open the page and watch it load. The card lands in six panels, cut at fixed places (`PIECES` in `index.html`: bands at 8.08 / 54.85 / 69.27 / 87.59 % of the height, column at 72.96 % of the width, stamp box 42–58 % × 88.35–97.56 %). A new card with the same layout needs nothing. If a panel moved, a cut will slice through it — re-measure those numbers.
4. If prices or items changed, change them in the text menu and the JSON-LD in `nst-irbid-geo/templates/oneforall-index.html`, run `node fill.mjs --force` there, and copy `out/oneforall-index.html` to `irbid/index.html` here.
5. Commit and push to `main`. GitHub Pages redeploys in about a minute.

## NFC burger piece
The acrylic "Tap for menu" piece for the Irbid window (files, install spec, NFC guide) lives in [`nfc-piece/`](nfc-piece/README.md). The menu page above is unaffected by it.
