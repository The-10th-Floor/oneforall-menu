# ONE FOR ALL — "Tap for menu" NFC point · Irbid branch (NST complex)
Built 2026-09-16 · Owner: Zaid · Status markers as in KHBRIA: `[CONFIRMED]` `[DRAFT]` `[NEEDS ZAID]` `[ASSUMPTION]`

## Current handoff — 30 September 2026

**Use the existing files for prototype review only.** The founder's later placement direction is roughly **350 mm across, RIGHT of the ordering window**, between the window and door; final size follows a measured site fit. The checked-in files are a smaller prototype. Do not send them to a shop as the final sign or enlarge every dimension uniformly.

1. Read `install/PLACEMENT.md` and measure the right-hand wall panel; the earlier left-side instruction is superseded.
2. Run `python3 holder/check_geometry.py` from this folder. It measures the actual cut paths and binary STL vertices, not the SVG page margin.
3. Select the fabrication route and prepare the larger geometry with the supplier. Preserve the real tag size, material thickness and mounting clearances; agree fixing and print registration on a proof.
4. Write the exact existing menu URL to an unlocked test tag and read it back. Test both phones through the finished prototype at the intended wall position. Follow `nfc/PROGRAMMING.md`.
5. Record acceptance before authorizing production or irreversible locking. No tag programming, purchase, fabrication or installation is authorized by this document.

### Measured files, not final sign dimensions

| Existing output | Actual geometry (mm) | What it establishes |
|---|---|---|
| L0 backplate / L1 frame | 143.799 × 111.200 | Outer cut bounds; SVG sheet adds 5 mm margin on each side |
| L2 UV-print face | 131.499 × 98.900 | Cut face bounds inside frame |
| STL base | 143.799 × 111.200 × 7.000 | Base extents only |
| One-piece STL | 143.799 × 111.200 × 9.500 | Overall relief-model extents |
| Acrylic assembly | Nominal 6 mm | L0 3 mm + L1 3 mm; L2 fills the frame, not a third stacked sheet |

These files do not implement the requested 350 mm sign. Current 3D-print files include keyholes; the acrylic backplate does **not** include corresponding mounting holes. Supplier fixing design and site proof remain necessary. Existing SVG preview still contains a historical size label; measured geometry above takes precedence.

## What this is
A burger-shaped prototype (143.799 × 111.200 mm outline, brand-red plate, cream buns, yellow cheese, dark patty) with an
NFC tag hidden behind the patty. Customers at the ordering window hold their phone to it and the bilingual
menu opens — no app, no QR hunting. Two build routes, same geometry: **3D-printed kit** (PETG, base + six inlays)
or **laser-cut layered acrylic** (3 mm, flush inlay, UV-printed graphics). Preview: `holder/preview/front_view.png`.

## Folder map
| Path | What | Status |
|---|---|---|
| repo root (`../index.html`, `../qr.*`, `../source/`) | **The live menu, untouched.** This folder is the NFC piece only; the menu page stays exactly as deployed at https://the-10th-floor.github.io/oneforall-menu/ | `[CONFIRMED]` |
| `holder/ofa_burger_nfc_holder.scad` | Parametric OpenSCAD source (edit sizes/text; `part=` selector; exports STL) | `[DRAFT]` |
| `holder/build_holder.py` | Generates the small prototype; optional `--url` engraving is disabled pending QR proof | done |
| `holder/stl/` | `ofa_base` `ofa_bun_top` `ofa_cheese` `ofa_patty` `ofa_bun_bottom` (kit) · `ofa_one_piece_single_colour` · `ofa_assembled_preview.glb` | prototype export; measure/test before fabrication |
| `holder/laser/` | `L0_backplate_RED` `L1_frame_RED` `L2_inlay_bun_CREAM` `L2_inlay_cheese_YELLOW` `L2_inlay_patty_BROWN` · `ALL_LAYERS_nested_3mm.svg` (red = cut, blue = engrave/UV print; 1 unit = 1 mm; text already outlined) | prototype export; supplier review required |
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
- **Size:** measured outline 143.799 × 111.200 mm; STL one-piece depth 9.500 mm. These are the smaller prototype files, not the later 350 mm sign.
- **Tag:** genuine NXP NTAG213, 30–38 mm round label, pocket Ø40 mm under the inlays (kit) / from the back (one-piece).
- **Fixing:** STL base has two keyhole slots. Acrylic cut files have no equivalent mounting holes; supplier must design and proof the fixing for the actual substrate and final size.
- **Materials:** PETG or ASA for print (no PLA outside); cast acrylic for the laser version (extruded yellows fade).
- **Menu language:** Arabic default; switches by phone language, `?lang=en` forces English; choice remembered.

## Historical prototype estimates — 16 September 2026, obtain a current quote
| Item | Qty | Source | Cost |
|---|---|---|---|
| NTAG213 round label 30–38 mm | 1 (+ spares) | Waslleh 0.635 JOD (prototype) / AliExpress 38 mm pack | < 1 JOD |
| 3D-print kit, PETG (≈70 cm³ base + ≈35 cm³ inlays; ≈90–130 g at real infill) | 1 set | Jordan3DPrint 0.12 JD/g · PRINTie 3D 0.15 JD/g | ≈ 11–20 JOD |
| — or — layered cast acrylic 3 mm, 5 colours, laser-cut + UV print | 1 set | Acrylic and More (Sweifieh) · Printman · CPF Makerspace | quote (small job, expect 15–35 JOD) |
| 2× 4 × 30 mm pan-head screws + 6 mm plugs, or 4 strips 3M VHB 5952 | 1 | any hardware shop | ≈ 1–3 JOD |
| Short.io Free + Cloudflare Pages (hosting) | — | online | 0 JOD (+50 JOD/yr if you buy oneforall.jo) |
Historical prototype estimate only; not a quote for the larger sign. Do not order from these figures.

## Fabrication contacts (Amman — research graded HIGH from first-party pages; a second verification pass did not run)
- **Jordan3DPrint** · +962 79 747 9825 · PETG 0.12 JD/g, 1–3 business days, upload STL, quotes per gram.
- **PRINTie 3D** · Queen Rania St · +962 79 101 7999 · Bambu Lab dealer · PETG 0.15 JOD/g · rush 24 h +50%.
- **CPF Makerspace** (ex-TechWorks) · King Hussein Business Park Bldg 23 · walk-in Sat–Thu 9–5 · +962 79 100 0110 ·
  laser cutter + UV flatbed + Prusa XL (ASA-capable) — one visit covers BOTH versions and a prototype.
- **Acrylic and More** · Sweifieh · Instagram @acrylic_more · laser + CNC + direct UV print on acrylic, claims 3-yr outdoor colour.
- **Printman** · Al-Shahid St · acrylic laser department + UV stickers — backup.
- `[NEEDS ZAID]` Irbid-local printers were not researched (the brief said Amman before the branch correction). Yarmouk/JUST
  university labs and Irbid sign shops likely exist; Amman vendors ship or the piece rides with anyone driving up.

## Existing small-prototype print notes (not a final-sign work order)
- Print every part **as exported**: front face already on the bed. 0.2 mm layers, 4 walls, 20% infill (base), 100% (inlays).
- Colours: base **red**; bun_top + bun_bottom **cream**; cheese **yellow**; patty **dark brown**.
- Two-tone text on a single-extruder printer: the letters/symbol are the first 0.6 mm. Pause at 0.6 mm and swap
  filament (patty: start **cream** → swap to **brown**; buns: start **brown** → swap to **cream**). Multi-material printers: just assign.
- Assembly: stick the NFC tag in the base's front pocket → drop the six inlays into the recess (0.15 mm clearance, they self-align) →
  thin CA glue on the recess floor, not on the edges → done.
- Single-colour prototype: `ofa_one_piece_single_colour.stl` (tag goes in the back pocket). Its cover is thicker than the earlier target; NFC performance is unaccepted until tested through this exact piece. Do not select it as a proven fallback.

## Existing small-prototype laser notes — supplier proof required
**Route A, UV-printed face (looks like the preview):** 3 mm cast acrylic, three sheets.
- L0 back plate (red): cut `L0_backplate_RED_3mm.svg`; engrave the Ø40 circle 0.5–1 mm for the tag.
- L1 frame (red): cut `L1_frame_RED_3mm.svg`; it contains cut paths only, with no tab/handle engraving.
- L2 face (cream or white): cut `L2_FACE_single_piece_CREAM_3mm_UVPRINT.svg`, then UV-print `L2_FACE_artwork_UVPRINT_304dpi.png`
  on it at the original physical scale (12 px/mm, 304.8 dpi). The 1586 × 1195 px canvas is about 132.167 × 99.583 mm and includes transparent margin around the smaller face cut; do not stretch the canvas to the cut bounds or use fit-to-page. Ask the shop to register artwork to the contour and proof the finish under the actual lights.
- Stack: L0 + L1 solvent-welded → tag in the pocket → face dropped into the frame, flush → 6 mm total, hairline seam only around the burger.
**Route B, solid colour inlays (no UV printer):** the `L2_inlay_*` files, one sheet per colour, text engraved-and-filled. Flatter look.
**Edge-lit option (night variant):** make L0 from 5 mm clear acrylic instead of red, sand the back matte, run a 12 V warm-white
LED strip in a 4 mm channel routed along the back edge (or a slim LED tray behind the plate), red L1 frame on top hides the strip.
The plate glows amber at night in the same tone as the plinth LED on the facade. Needs a 12 V feed from the shop.
- Ask for 0.1 mm kerf compensation (face cut inside the line, frame outside) or accept a hairline gap — both look fine.

## URL decision (resolved)
The tag URL is **https://the-10th-floor.github.io/oneforall-menu/** — already written on the window tag and printed as QR
per the earlier repo. The current root `qr.svg` / `qr.png` and programming docs target it. The historical `site/` outputs and optional engraved QR layer are not approved production inputs. The generator now rejects `--url`; use the corrected root QR files with their full white margin and a physical proof.
Caveat from research: GitHub Pages' terms discourage commercial sites; if that ever bites, move the files to Cloudflare Pages
and leave a redirect at the old URL — no tag needs rewriting as long as the old URL still answers.

## What is still open  `[NEEDS ZAID]`
1. **Create and test the final-size sign.** Preserve the live root menu; `site/` is historical and must not replace it.
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
