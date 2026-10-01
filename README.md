# One For All — digital menu

Live: https://the-10th-floor.github.io/oneforall-menu/

This URL is written on the NFC tag at the ordering window (and printed as `qr.svg` / `qr.png`). **Never change the URL.** Change the menu behind it instead.

**Print QR:** use the root `qr.svg` (vector) or `qr.png`. Both include an opaque white, four-module quiet zone on every side; keep that space clear and do not crop it, overlay artwork or stretch the code. Regenerate with `pip install 'qrcode[pil]==8.2'` then `python generate_qr.py`; verify with `python generate_qr.py --check`. Scan a physical proof at the intended size/material before production. These files do not validate or replace the optional engraved QR inside the NFC holder prototype.

**Public address: https://oneforalljo.com/** (since 2026-10-01). DNS is on Cloudflare (Zaid's account), with no mail on the domain (null MX, SPF `-all`, DMARC `reject`). The domain (and `www`) is a custom domain of the Cloudflare Pages project `oneforall-jo`; its `pages-dev/_worker.js` serves this repo from GitHub Pages:
- `/` is a 301 to `/irbid/`, the main page.
- `/menu/` is the tap page (this repo's root): the menu card. `/menu/x` is the root's `x`.
- every other path is the same file from GitHub Pages. Push to `main` and the domain follows; nothing to deploy.
- `www` and `oneforall-jo.pages.dev` 301 to the same path on oneforalljo.com.

**The repo has no custom domain, and must never get one again** (removed 2026-10-01; there is no `CNAME` file). GitHub serves the tag URL at github.io itself, so a tap opens the menu with no redirect. With a custom domain, GitHub 301s the tag to that domain's `/`, which is the main page, not the menu. The pages' canonical, `og:url` and schema name oneforalljo.com; the tag and the QR keep the github.io address. The loyalty card lives at `https://card.oneforalljo.com` (repo `oneforall-loyalty`).

**Old interim address https://oneforall-jo.pages.dev/** (2026-09-24 to 2026-10-01): the same worker 301s every path to oneforalljo.com, except the Search Console and IndexNow files, which stay 200. Test the worker with `node pages-dev/test.mjs`, then redeploy it only when `_worker.js` changes: `npx wrangler pages deploy pages-dev --project-name oneforall-jo --branch main`.

**Search files (2026-09-24):** `sitemap.xml` lists the one canonical page (`/irbid/`); `robots.txt` points to it; `d590794667958097a6f50493ef61101a.txt` is the IndexNow key that lets us tell Bing (and the engines that share IndexNow) about a changed page — do not delete it. Both name https://oneforalljo.com since 2026-10-01. `google85fa2133dd80e4b3.html` proves ownership of https://oneforall-jo.pages.dev/ in Google Search Console (property on zaidgharaibeh17@gmail.com, verified 2026-09-24) — removing it unverifies the property. It keeps that old property alive for the change of address; the new domain gets its own Domain property (DNS TXT). **Bing (2026-10-01):** the `msvalidate.01` meta tag in `index.html` and `/irbid/` proves ownership of https://oneforalljo.com/ in Bing Webmaster Tools; removing it unverifies the site. **Cloudflare Web Analytics (2026-10-01):** the beacon snippet before `</body>` in `index.html` and `/irbid/` (from the template in `nst-irbid-geo`) counts page views, cookieless; the site is DNS-only on Cloudflare, so the snippet is the only way it counts. The token in it is public by design.

**IndexNow workflow (`.github/workflows/indexnow.yml`, 2026-09-24), two jobs:**
- `ping` runs on a push to `main` that changes `irbid/index.html`. It asks GitHub for a Pages build if none starts within 3 min, waits (up to 20 min) until the live `/irbid/` matches the commit byte for byte, checks the key file, then tells IndexNow about `/irbid/`. A 403 means the key is no longer valid: add a new key file and change `KEY` in the workflow.
- `reach` runs every day at about 09:17 Amman (GitHub may start it late). It is the daily check that the NFC tap page (the github.io address on the tag) still answers 200 with the menu and no redirect, and it also checks the domain's redirects (`/` to `/irbid/`, `/menu` to `/menu/`, `www`), `/menu/` and its menu image, `/irbid/` (canonical kept, no `noindex`), the sitemap, robots, the key file, the Google file, the old pages.dev address (301 to the new host, its two proof files 200) and the loyalty card at card.oneforalljo.com.
- Run either job by hand: Actions → IndexNow → Run workflow, pick `ping` or `reach`.
- **Trap:** after 60 days with no repo activity, GitHub turns off the whole IndexNow workflow (this repo is public), so `reach` and `ping` both stop, silently. A later push does not turn it back on. To turn it on again: Actions → IndexNow → Enable workflow (or push a commit that changes the `cron` line). Before the 60 days pass, any commit resets the clock.

## Two pages, two jobs
| Page | For | What is on it |
|---|---|---|
| `/` on github.io (the tag), `/menu/` on oneforalljo.com — **the tap page** (`index.html`, kept by hand) | the customer at the window | the menu card, which lands in six panels, and the language switch — **nothing else shows**. The link to the landing page is in the page for screen readers and keyboards only (founder, 2026-09-19: the NFC menu is the menu, no extra line). A visitor who opens the card **from the landing page** (`?from=site`) also gets a "← One For All" button back to it; a tap on the NFC piece never does. The **My card** button appears once loyalty is live |
| `/irbid/` — **the landing page** (`irbid/index.html`, **generated**) | Google, Maps, anyone arriving from Instagram | the menu as real text with prices, set as their printed card; the `Restaurant` + `Menu` schema, Directions, Instagram. It opens with burger-range imagery and the entry sandwich price (from 1.98 JD), pans to the milkshake, then brings both images together beside the menu action. The burger photograph does not establish one exact patty configuration, so it is not labelled as a single triple-patty OFA or used to calculate a pictured combo bill. Existing images remain in `irbid/scene/`; the milkshake composition uses the branch phone photo on the same backdrop (2026-09-24). Then the menu as the card, then Find us. The top bar carries the way around: the badge (top), **Menu** and **Find us** (jump to their sections), and the language switch. The motion runs on CSS scroll timelines with no scroll script, so it stays smooth on slow machines; browsers without them get each beat as a still, finished screen. This is the Website and Menu link for the Google Business Profile, and the canonical URL of both pages |

## How the pages link
`/irbid/` is the main page (oneforalljo.com/ opens it); everything else is one step from it and one step back.

| From | To | How |
|---|---|---|
| `/irbid/` | its own menu and Find us sections | Menu / Find us in the top bar; Directions + The whole menu in the final scene |
| `/irbid/` | `/menu/` (the printed card) | "The printed menu card" in Find us, with `?from=site` |
| `/menu/` from the site | `/irbid/` | the "← One For All" button (only with `?from=site`) |
| the github.io page from the NFC tag | — | the card only, by the founder's call |
| `/irbid/world/` (retired 2026-09-24) | `/irbid/` | an instant redirect; old links keep working |

`/plan/` is the owner's planner: unlisted, `noindex`, linked from nowhere.

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

## Home Screen and loyalty (2026-10-01)

`native.js`, `manifest.webmanifest` and `sw.js` provide translated Home Screen help and native Chrome install prompts; notifications open the stamp card at `card.oneforalljo.com`, where consent is recorded. Menus remain network-first with an offline explanation; no stale prices are cached. The authoritative landing template is `nst-irbid-geo/templates/oneforall-index.html`; regenerate and copy it here after edits. The remaining `feat/landing-real` lane footage is incorporated with native, user-controlled video; its older layout/scroll scripting is superseded by the current template. `feat/my-card` links are incorporated at the current host. The returning-vehicle plan content already existed on main with newer domain/footer fixes. Those old branch pointers are preserved and reconciled into main, without restoring stale hosts/layouts.
