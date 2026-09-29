# PLACEMENT — One For All, Irbid branch (NST complex)

Source: Zaid's three photos of the unit (2026-09-16). The green circle marks the LEFT window,
the one customers stand at. Photo observations are not site dimensions; measure on site before drilling. The later right-side direction below supersedes the initial left-side suggestion.

## What the facade gives us
- Ground-floor unit of a curved glass building, shared frontage with "قهوة BLK" on the left.
- One For All frontage, left → right: **corner column → plaster wall → ordering window (blue steel frame,
  4-pane, red brick visible inside) → plaster wall → blue-framed glass door → second blue window → plaster**.
- Red band along the top with the illuminated ONE FOR ALL stamp sign; white slatted soffit/awning above;
  concrete floor plinth with an amber LED strip.
- Wall finish: smooth grey-beige render/paint. Not tile. → Brand-red base plate on grey reads loud and clean.
- The blue window frame is steel/aluminium → NFC tag must NOT sit on or within ~40 mm of it.

## Where the holder goes  `[founder direction; site measurement and taped proof pending]`
**On the wall to the RIGHT of the ordering window, between that window and the blue door.**

The founder settled the size and the side on 2026-09-22: *"the nfc is bigger than that and it goes next
right to the window"*, then *"the nfc tag is 35 cm by 35 i think or sth like that which gives the shape,
so basicly its to the right and bigger"*.

| Item | Value | Why |
|---|---|---|
| **Size** | **~350 mm across** (current cut outline is 143.799 × 111.200 mm; the larger SVG sheet includes margins) | His call. At 350 mm it is found from the queue, not discovered by accident. The measured outline is about 1.293 : 1, so 350 across gives **~271 tall** and the burger keeps its shape; a true 350 x 350 means squaring up the backplate in `build_holder.py` |
| **Side** | **RIGHT of the ordering window**, centred in the wall panel between the window and the door | His call. Earlier footage estimate was 610 mm between frames; confirm with a tape measure. A 350 mm sign would leave 130 mm each side only if that estimate holds. Test the actual tag at the selected location; a numerical gap alone does not establish read performance |
| Vertical | Centre **1100 mm** above finished floor (range 1000–1200) | Research (NFC UX + ADA reach band 380–1220 mm); the iPhone antenna is at the top-back edge, so slightly lower is easier than higher |
| Orientation | Face vertical, parallel to the wall | Phones tap flat against it |
| Sight line | Visible from the queue position ~1.5 m back | People discover it while waiting, not after ordering |
| **The tag itself does not change** | 30–38 mm NTAG213, antenna ≥25 mm | A bigger holder does not read further. It only makes the piece easier to find |

Do **not** put it on the glass: the glass is fine for NFC, but the frame around it is metal and the pane
gets cleaned with solvents; the plaster wall is the durable position.

## Fixing — choose for the final size and actual wall

The small STL prototype includes keyholes with centres 72 mm apart. The acrylic SVG backplate has no keyholes or screw holes. Do not use the STL mounting instruction as an acrylic drilling template.

Have the fabricator provide the final sign's fixing positions, substrate-compatible anchors or adhesive system and installation drawing. Verify the wall condition and concealed services before drilling; prototype the mounting and tag together. Uniformly scaling the existing file would also scale the tag pocket, fixing features and material thickness, which is not a valid final-sign design.

## NFC placement inside the holder
- Kit version: the tag pocket (Ø40 × 1.2 mm) opens to the FRONT of the red base, under the patty/cheese
  inlays. Stick the tag in, then glue the inlays over it. Measure the actual assembled material over the tag; test it with both phones.
- One-piece version: pocket from the back, tape over it. Nothing metallic behind it either way.
- Use the selected tag's actual dimensions for the pocket. Keep the test tag removable until the assembled and mounted read tests pass. No guaranteed read distance is established by the exported geometry.

## Sign language on the holder (v3, locked)
- Patty: **TAP FOR MENU** (cream, dark outline, Baloo Bhaijaan 2 — the menu's family)
- Bottom bun: **قرّب تلفونك** (dark, cream outline, same family)
- Nothing else on the piece. Instagram handle, hours, order links all live on the menu page.
- The optional engraved QR is not accepted: its generator uses zero quiet-zone modules. Do not fabricate that optional layer. Use the separately checked root `qr.svg`/`qr.png` with their complete white margin if a QR alternative is needed; inspect and scan a physical proof at the intended size.

## Site checklist before fabrication
- [ ] Measure the wall panel RIGHT of the ordering window; tape out the proposed 350 mm outline, confirm door/window clearance and comfortable reach.
- [ ] Confirm the soffit protects the spot from direct rain (it looks like it does).
- [ ] Have the installer check concealed services and substrate suitability before drilling. A bare-tag read cannot establish that the wall is clear of metal or services; test the mounted assembly separately for NFC operation.
- [ ] Take one straight-on daylight photo of the wall + window for the final mock-up and for the installer.

- [ ] Supplier confirms final dimensions, fixing drawing, material and UV-print registration.
- [ ] Read back the exact menu URL; test the assembled piece on iPhone and Android at the site before owner-approved write protection.
