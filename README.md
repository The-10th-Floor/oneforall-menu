# One For All — digital menu

Live: https://the-10th-floor.github.io/oneforall-menu/

This URL is written on the NFC tag at the ordering window (and printed as `qr.svg` / `qr.png`). **Never change the URL.** Change the menu behind it instead.

## Update the menu
1. Drop the new PDF into `source/` (page 1 English, page 2 Arabic, A5).
2. `pip install pymupdf` once, then `python render.py source/<new>.pdf`.
3. Commit and push to `main`. GitHub Pages redeploys in about a minute.

## NFC burger piece
The acrylic "Tap for menu" piece for the Irbid window (files, install spec, NFC guide) lives in [`nfc-piece/`](nfc-piece/README.md). The menu page above is unaffected by it.
