# ONE FOR ALL — "Tap for menu" NFC point · Irbid branch (NST complex)
Built 2026-09-16 · Owner: Zaid · Status markers as in KHBRIA: `[CONFIRMED]` `[DRAFT]` `[NEEDS ZAID]` `[ASSUMPTION]`

## START HERE — the whole job in 5 moves
1. **Buy the tag.** Genuine NXP **NTAG213**, round label **30–38 mm**. Prototype today: Waslleh.com "NTAG213 White Round NFC Tag Sticker" 0.635 JOD
   (+962 7 80 83 83 00, same-day dispatch). Final/spares: a 38 mm NTAG213 pack on AliExpress (ships to Jordan, 16% tax on arrival).
   Check every tag with the free **NXP TagInfo** app. Details: `nfc/PROGRAMMING.md`.
2. **Write the tag.** NFC Tools app → Write → URL → `https://the-10th-floor.github.io/oneforall-menu/` → Write → then **Lock**.
   That is the live menu, the same URL already on the current tag. **The menu itself is not touched by this project.**
3. **Make the piece (acrylic, UV-printed).** Give the shop these three files from `holder/laser/`:
   `L0_backplate_RED_3mm.svg` (cut, engrave the Ø40 pocket) · `L1_frame_RED_3mm.svg` (cut) ·
   `L2_FACE_single_piece_CREAM_3mm_UVPRINT.svg` (cut) + `L2_FACE_artwork_UVPRINT_304dpi.png` (print on it, matte varnish).
   Cast acrylic 3 mm, red + cream. Amman: Acrylic and More (Sweifieh, @acrylic_more) or CPF Makerspace (King Hussein Business Park, walk-in).
   3D-printed alternative: `holder/stl/` (PETG, colours per part) — Jordan3DPrint +962 79 747 9825 or PRINTie 3D +962 79 101 7999.
4. **Assemble.** Weld L0+L1 → tag into the pocket → face into the frame. Test the tap through the finished piece on an iPhone and an Android.
5. **Install.** Plaster wall left of the ordering window, centre 1100 mm high, ≥150 mm from the blue frame, two screws in the keyhole
   slots or 3M VHB. Full spec and site checklist: `install/PLACEMENT.md`. Preview of the piece: `holder/preview/front_view.png`.

## What this is
A burger-shaped wall piece (130 × 104 mm, brand-red plate, cream buns, yellow cheese, dark patty) with an
NFC tag hidden behind the patty. Customers at the ordering window hold their phone to it and the bilingual
menu opens — no app, no QR hunting. Two build routes, same geometry: **3D-printed kit** (PETG, 5 parts)
or **laser-cut layered acrylic** (3 mm, flush inlay, UV-printed graphics). Preview: `holder/preview/front_view.png`.

## Folder map
| Path | What | Status |
|---|---|---|
| repo root (`../index.html`, `../qr.*`, `../source/`) | **The live menu, untouched.** This folder is the NFC piece only; the menu page stays exactly as deployed at https://the-10th-floor.github.io/oneforall-menu/ | `[CONFIRMED]` |
| `holder/ofa_burger_nfc_holder.scad` | Parametric OpenSCAD source (edit sizes/text; `part=` selector; exports STL) | `[DRAFT]` |
| `holder/build_holder.py` | Generates everything below from one geometry; `--url` adds an optional engraved QR | done |
| `holder/stl/` | `ofa_base` `ofa_bun_top` `ofa_cheese` `ofa_patty` `ofa_bun_bottom` (kit) · `ofa_one_piece_single_colour` · `ofa_assembled_preview.glb` | print-ready |
| `holder/laser/` | `L0_backplate_RED` `L1_frame_RED` `L2_inlay_bun_CREAM` `L2_inlay_cheese_YELLOW` `L2_inlay_patty_BROWN` · `ALL_LAYERS_nested_3mm.svg` (red = cut, blue = engrave/UV print; 1 unit = 1 mm; text already outlined) | cut-ready |
| `install/PLACEMENT.md` | Where it goes on the Irbid wall, height, fixing, site checklist | `[DRAFT]` measure on site |
| `nfc/PROGRAMMING.md` | Tag choice, where to buy in Jordan, URL strategy, writing + locking steps | `[CONFIRMED]` tech; prices dated |
| `research/RESEARCH.md` | Full graded research (5 dimensions, 19 skeptic verdicts) | reference |

## Design v3 (2026-09-16, locked to Zaid's three reference stickers) — change it in the .scad / .py if you disagree
- **Style:** cartoon sticker burger with a dark outline around every layer: domed sesame crown with a crescent highlight,
  irregular ruffled lettuce wider than the bun, two tomato slices, flat cheese slice (no drips — Zaid), patty at real
  burger proportions (16 mm visible; a thicker patty "is not a burger any more" — Zaid), rounded heel. Brand-red plate is the "sticker border".
- **Copy (locked):** patty **TAP FOR MENU** (cream, dark outline, 3 mm clear of cheese and heel); heel **قرّب تلفونك** (dark, cream outline).
  Nothing else on the piece. The Instagram handle and everything else live on the menu page, not on the acrylic.
- **Type:** the word **MENU** is the menu's own hand-lettered wordmark, harvested as vectors from the outlined menu PDF
  (`holder/fonts/MENU_wordmark.json`, page 1 yellow MENU) — not a font, the real lettering, in the menu's yellow #FFCC49.
  **TAP FOR** and **قرّب تلفونك** are set in the menu's heading family (Baloo Bhaijaan 2 ExtraBold), cream and dark, flat, no outlines.
  The OpenSCAD file cannot load the wordmark; use the Python build (`build_holder.py`) for the real files.
- **Palette (synced to the menu)** in `ART` in `build_holder.py`: plate = menu page red #EF3D3D; tomato = menu card red #D82827;
  cheese = menu yellow #FFCC49; sesame + crown highlight = menu cream #FFF6EE; buns = tints of the yellow (#F9CF7E→#E4A34D);
  patty and every outline = one brown #4A2314; lettuce a muted green #7CC468→#4E9E45 (the only colour not in the menu — a burger needs it).
- **Lettering:** MENU = the real wordmark; TAP FOR and قرّب تلفونك get the same hand-lettered treatment (per-letter / per-word bounce,
  wobbled edges, marker-soft corners) so all three lines read as one hand.
- **Build:** UV-printed face on cream acrylic inside the red frame (Route A) is the intended build — outlines and gradients
  print as-is. Solid-colour inlay files (Route B) and STL parts are generated from the same shapes without gradients.
- **Size:** 145 × 113 mm, 8.9 mm deep (kit).
- **Tag:** genuine NXP NTAG213, 30–38 mm round label, pocket Ø40 mm under the inlays (kit) / from the back (one-piece).
- **Fixing:** two hidden keyhole slots on the back (4 mm screws + plugs into the plaster) or 3M VHB tape. Nothing visible.
- **Materials:** PETG or ASA for print (no PLA outside); cast acrylic for the laser version (extruded yellows fade).
- **Menu language:** Arabic default; switches by phone language, `?lang=en` forces English; choice remembered.

## Bill of materials (one unit)
| Item | Qty | Source | Cost |
|---|---|---|---|
| NTAG213 round label 30–38 mm | 1 (+ spares) | Waslleh 0.635 JOD (prototype) / AliExpress 38 mm pack | < 1 JOD |
| 3D-print kit, PETG (≈70 cm³ base + ≈35 cm³ inlays; ≈90–130 g at real infill) | 1 set | Jordan3DPrint 0.12 JD/g · PRINTie 3D 0.15 JD/g | ≈ 11–20 JOD |
| — or — layered cast acrylic 3 mm, 5 colours, laser-cut + UV print | 1 set | Acrylic and More (Sweifieh) · Printman · CPF Makerspace | quote (small job, expect 15–35 JOD) |
| 2× 4 × 30 mm pan-head screws + 6 mm plugs, or 4 strips 3M VHB 5952 | 1 | any hardware shop | ≈ 1–3 JOD |
| Short.io Free + Cloudflare Pages (hosting) | — | online | 0 JOD (+50 JOD/yr if you buy oneforall.jo) |
**Total per unit ≈ 15–40 JOD.** Second unit for the other window or another branch = same files.

## Fabrication contacts (Amman — research graded HIGH from first-party pages; a second verification pass did not run)
- **Jordan3DPrint** · +962 79 747 9825 · PETG 0.12 JD/g, 1–3 business days, upload STL, quotes per gram.
- **PRINTie 3D** · Queen Rania St · +962 79 101 7999 · Bambu Lab dealer · PETG 0.15 JOD/g · rush 24 h +50%.
- **CPF Makerspace** (ex-TechWorks) · King Hussein Business Park Bldg 23 · walk-in Sat–Thu 9–5 · +962 79 100 0110 ·
  laser cutter + UV flatbed + Prusa XL (ASA-capable) — one visit covers BOTH versions and a prototype.
- **Acrylic and More** · Sweifieh · Instagram @acrylic_more · laser + CNC + direct UV print on acrylic, claims 3-yr outdoor colour.
- **Printman** · Al-Shahid St · acrylic laser department + UV stickers — backup.
- `[NEEDS ZAID]` Irbid-local printers were not researched (the brief said Amman before the branch correction). Yarmouk/JUST
  university labs and Irbid sign shops likely exist; Amman vendors ship or the piece rides with anyone driving up.

## Print instructions (give this to the shop with the STLs)
- Print every part **as exported**: front face already on the bed. 0.2 mm layers, 4 walls, 20% infill (base), 100% (inlays).
- Colours: base **red**; bun_top + bun_bottom **cream**; cheese **yellow**; patty **dark brown**.
- Two-tone text on a single-extruder printer: the letters/symbol are the first 0.6 mm. Pause at 0.6 mm and swap
  filament (patty: start **cream** → swap to **brown**; buns: start **brown** → swap to **cream**). Multi-material printers: just assign.
- Assembly: stick the NFC tag in the base's front pocket → drop the four inlays into the recess (0.15 mm clearance, they self-align) →
  thin CA glue on the recess floor, not on the edges → done.
- Single-colour fallback: `ofa_one_piece_single_colour.stl` (relief only, paint the face if wanted; tag goes in the back pocket).

## Laser instructions (acrylic version) — the recommended build
**Route A, UV-printed face (looks like the preview):** 3 mm cast acrylic, three sheets.
- L0 back plate (red): cut `L0_backplate_RED_3mm.svg`; engrave the Ø40 circle 0.5–1 mm for the tag.
- L1 frame (red): cut `L1_frame_RED_3mm.svg`; UV-print or engrave-and-fill the handle on the tab (blue paths).
- L2 face (cream or white): cut `L2_FACE_single_piece_CREAM_3mm_UVPRINT.svg`, then UV-print `L2_FACE_artwork_UVPRINT_304dpi.png`
  on it (1 px = 1/12 mm, artwork is already cropped to the cut outline; ask for a matte/satin varnish — no glare under the soffit LEDs).
- Stack: L0 + L1 solvent-welded → tag in the pocket → face dropped into the frame, flush → 6 mm total, hairline seam only around the burger.
**Route B, solid colour inlays (no UV printer):** the `L2_inlay_*` files, one sheet per colour, text engraved-and-filled. Flatter look.
**Edge-lit option (night variant):** make L0 from 5 mm clear acrylic instead of red, sand the back matte, run a 12 V warm-white
LED strip in a 4 mm channel routed along the back edge (or a slim LED tray behind the plate), red L1 frame on top hides the strip.
The plate glows amber at night in the same tone as the plinth LED on the facade. Needs a 12 V feed from the shop.
- Ask for 0.1 mm kerf compensation (face cut inside the line, frame outside) or accept a hairline gap — both look fine.

## URL decision (resolved)
The tag URL is **https://the-10th-floor.github.io/oneforall-menu/** — already written on the window tag and printed as QR
per the earlier repo. Everything here targets it: `site/qr.svg`, the optional QR engrave layer
(`holder/laser/OPTIONAL_qr_on_bun_bottom_engrave.svg`), and the placement/programming docs.
Caveat from research: GitHub Pages' terms discourage commercial sites; if that ever bites, move the files to Cloudflare Pages
and leave a redirect at the old URL — no tag needs rewriting as long as the old URL still answers.

## What is still open  `[NEEDS ZAID]`
1. **Push `site/` to the repo** (replaces `index.html`, adds `print.html`, `logo.png`, new `qr.*`). Not pushed — say the word.
2. ~~**Irbid branch maps link** for the Directions button.~~ Done 2026-09-24: the listing is live (CID `2649453184101416150`) and Directions start navigation to it by place ID.
3. **Acrylic or print?** Print kit is cheaper and faster; acrylic looks more premium under the soffit lights at night (they run to 1 AM).
4. Site measurements per `install/PLACEMENT.md` before drilling.
5. Optional: Cloudflare Web Analytics snippet on `index.html` for tap counts (free, no cookies).

## Brand facts picked up on the way (research, HIGH unless marked)
- Company "Food For All Foods", est. 2023, Amman; branches Abdoun (Fawzi Al-Qawuqji St) + Khalda (app) + Irbid (Zaid's photos, new).
- No website (ofafoods.com is dead); the brand lives on Instagram and its "One For All JO" app (Bites n' Bags white label).
- Lines: "Deliciously Affordable", "1 JOD and change", Arabic **"كلشي عنا بدينار وشوي"** — worth echoing on the menu page.
- Verified mark: heavy white groovy "ONE / FOR ALL" on a wobbly tomato-red blob (~#C03830) with mustard-yellow strokes.
- Hours run to midnight / 1 AM → matte finish (no glare under the soffit LEDs), high contrast — both already in the design.
