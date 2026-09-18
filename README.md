# One For All — digital menu

Live: https://the-10th-floor.github.io/oneforall-menu/

This URL is written on the NFC tag at the ordering window (and printed as `qr.svg` / `qr.png`). **Never change the URL.** Change the menu behind it instead.

## Update the menu
1. Drop the new PDF into `source/` (page 1 English, page 2 Arabic, A5).
2. `pip install pymupdf` once, then `python render.py source/<new>.pdf`. It writes `menu-en.svg` / `menu-ar.svg` (what the page shows) and the two PNGs (link preview + no-JavaScript fallback).
3. Open the page and watch it load. The card lands in six panels, cut at fixed places (`PIECES` in `index.html`: bands at 8.08 / 54.85 / 69.27 / 87.59 % of the height, column at 72.96 % of the width, stamp box 42–58 % × 88.35–97.56 %). A new card with the same layout needs nothing. If a panel moved, a cut will slice through it — re-measure those numbers.
4. If prices or items changed, change them in the text menu and the JSON-LD in `index.html` too, and in `nst-irbid-geo/templates/oneforall-index.html` (the template that page is generated from).
5. Commit and push to `main`. GitHub Pages redeploys in about a minute.

## NFC burger piece
The acrylic "Tap for menu" piece for the Irbid window (files, install spec, NFC guide) lives in [`nfc-piece/`](nfc-piece/README.md). The menu page above is unaffected by it.
