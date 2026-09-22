# PLACEMENT — One For All, Irbid branch (NST complex)

Source: Zaid's three photos of the unit (2026-09-16). The green circle marks the LEFT window,
the one customers stand at. Everything below is read from those photos; measure on site before drilling.

## What the facade gives us
- Ground-floor unit of a curved glass building, shared frontage with "قهوة BLK" on the left.
- One For All frontage, left → right: **corner column → plaster wall → ordering window (blue steel frame,
  4-pane, red brick visible inside) → plaster wall → blue-framed glass door → second blue window → plaster**.
- Red band along the top with the illuminated ONE FOR ALL stamp sign; white slatted soffit/awning above;
  concrete floor plinth with an amber LED strip.
- Wall finish: smooth grey-beige render/paint. Not tile. → Brand-red base plate on grey reads loud and clean.
- The blue window frame is steel/aluminium → NFC tag must NOT sit on or within ~40 mm of it.

## Where the holder goes  `[measured off the 2026-09-21 footage; tape it before drilling]`
**On the wall to the RIGHT of the ordering window, between that window and the blue door.**

The founder settled the size and the side on 2026-09-22: *"the nfc is bigger than that and it goes next
right to the window"*, then *"the nfc tag is 35 cm by 35 i think or sth like that which gives the shape,
so basicly its to the right and bigger"*.

| Item | Value | Why |
|---|---|---|
| **Size** | **~350 mm across** (the laser files are drawn at 154 x 121 mm — that is a plaque, this is a sign) | His call. At 350 mm it is found from the queue, not discovered by accident. The artwork is 1.27 : 1, so 350 across gives **~275 tall** and the burger keeps its shape; a true 350 x 350 means squaring up the backplate in `build_holder.py` |
| **Side** | **RIGHT of the ordering window**, centred in the wall panel between the window and the door | His call. Measured on the 2026-09-21 frame: the window frame ends and the door frame starts **610 mm** apart, so a 350 mm piece centres with **130 mm** clear each side — far past the 40 mm an NFC tag needs from metal |
| Vertical | Centre **1100 mm** above finished floor (range 1000–1200) | Research (NFC UX + ADA reach band 380–1220 mm); the iPhone antenna is at the top-back edge, so slightly lower is easier than higher |
| Orientation | Face vertical, parallel to the wall | Phones tap flat against it |
| Sight line | Visible from the queue position ~1.5 m back | People discover it while waiting, not after ordering |
| **The tag itself does not change** | 30–38 mm NTAG213, antenna ≥25 mm | A bigger holder does not read further. It only makes the piece easier to find |

Do **not** put it on the glass: the glass is fine for NFC, but the frame around it is metal and the pane
gets cleaned with solvents; the plaster wall is the durable position.

## Fixing
1. **Preferred — 2 screws, hidden.** Back of the base has two keyhole slots (centres 72 mm apart, 26 mm above
   the burger centre). Drill Ø6 into the render, insert two 6 mm nylon plugs, drive two 4 × 30 mm pan-head
   screws leaving the heads **3 mm proud**, then slide the holder down onto them. Level the two screws with
   a spirit level first (the slots are vertical, so any tilt shows).
2. **No-drill option.** 3M VHB 5952 or 4910 (clear) tape, 4 strips of 20 × 60 mm on the flat back areas
   around the NFC pocket, on clean dust-free paint. Press hard for 60 s; full bond after 72 h.
   Painted render is the weak link, not the tape — if the paint is chalky, use screws.

## NFC placement inside the holder
- Kit version: the tag pocket (Ø40 × 1.2 mm) opens to the FRONT of the red base, under the patty/cheese
  inlays. Stick the tag in, then glue the inlays over it. Only 3.5 mm of plastic sits in front of the antenna.
- One-piece version: pocket from the back, tape over it. Nothing metallic behind it either way.
- Use a 30–38 mm NTAG213 label (antenna ≥25 mm). Research: a 38 mm tag reads at 5–6 cm on a good Android,
  anything over 30 mm gives a good phone experience, discs under 25 mm do not. Through 3–4 mm of PETG or
  3 mm acrylic expect a comfortable 20–40 mm tap distance.

## Sign language on the holder (v3, locked)
- Patty: **TAP FOR MENU** (cream, dark outline, Baloo Bhaijaan 2 — the menu's family)
- Bottom bun: **قرّب تلفونك** (dark, cream outline, same family)
- Nothing else on the piece. Instagram handle, hours, order links all live on the menu page.
- Optional QR on the bottom bun right side for phones without NFC (generate with `build_holder.py --url …`
  once the short link exists). Recommended: yes for Irbid — mid-range Androids without NFC are common.

## Site checklist before fabrication
- [ ] Measure the plaster wall width left of the window (need ≥ 330 mm for holder + gaps).
- [ ] Confirm the soffit protects the spot from direct rain (it looks like it does).
- [ ] Confirm nothing metallic is embedded behind the plaster at the spot (conduit, frame stiffener) —
      hold a phone with NFC Tools running against the wall with a bare tag taped there; if it reads, the wall is fine.
- [ ] Take one straight-on daylight photo of the wall + window for the final mock-up and for the installer.
