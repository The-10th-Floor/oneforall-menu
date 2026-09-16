// ============================================================================
//  ONE FOR ALL — "Tap for menu" burger NFC holder
//  Parametric OpenSCAD source · units = mm · front view, Y up, Z toward viewer
//  Sept 2026 · Irbid branch (NST complex) walk-up window · plaster wall · keyhole screws or 3M VHB
//
//  HOW TO USE
//    part = "assembly"   → coloured preview of the whole thing (F5)
//    part = "base"       → red back plate with burger-shaped recess + NFC pocket
//    part = "bun_top" | "cheese" | "patty" | "bun_bottom" → inlay pieces
//    part = "one_piece"  → single-body version for single-colour printing
//    part = "plate"      → all printable parts laid flat for one print bed
//  Render (F6) then File → Export → STL.
//
//  PRINT NOTES
//    • All parts print FACE DOWN (front face on the bed) — the raised 0.6 mm
//      text/symbols are the first layers. On a single-extruder printer use
//      "pause at layer" at 0.6 mm to swap filament: letters colour first,
//      then body colour. Multi-material printers: assign by part.
//    • Material: PETG or ASA (Irbid sun + winter). Not PLA outdoors.
//    • NFC tag: genuine NXP NTAG213, 30–38 mm round label (antenna ≥25 mm).
//      Kit: stick it in the front pocket of the base, then glue the inlays over it.
//      One-piece: it goes in the back pocket; tape over it.
// ============================================================================

part = "assembly";   // ["assembly","base","bun_top","lettuce","tomato","cheese","patty","bun_bottom","one_piece","plate"]

/* ---------- dimensions ---------- */
W            = 120;    // burger width
halo         = 6;      // red "stamp" border around the burger (visible frame)
outline      = 1.1;    // black sticker outline width (UV print); layers grow by this
base_t       = 7;      // base plate thickness
recess_d     = 1.6;    // depth of the burger-shaped recess in the base (inlays sit here)
inlay_t      = 3.5;    // inlay piece thickness (sits recess_d deep → 1.9 mm proud)
relief_h     = 0.6;    // raised text / symbol height on the inlay faces
tol          = 0.15;   // per-side clearance between inlays and recess
nfc_d        = 40;     // NFC pocket diameter — fits up to a 38 mm NTAG213 label (use ≥30 mm tags)
nfc_depth    = 1.2;    // kit: pocket opens to the FRONT inside the recess (tag sits under the inlays)
nfc_center   = [0, -4];// pocket centre (patty/cheese = middle of the tap target)
keyholes     = [[-36, 26], [36, 26]];  // hidden wall fixing (2 screws + plugs). Set keyholes = [] for a flat back (VHB tape)
kh_head_d    = 7.4;    // screw head pocket Ø
kh_shank_d   = 4.4;    // screw shank slot width
kh_slot      = 8;      // slot length downward (holder slides down onto the screws)
kh_depth     = 3.2;    // head pocket depth from the back
$fn          = 96;

/* ---------- text ---------- */
en_text      = "TAP FOR MENU";
ar_text      = "قرّب تلفونك";          // "bring your phone close" (Jordanian) — Zaid's pick
en_font      = "Baloo Bhaijaan 2:style=ExtraBold";   // the menu's family; install holder/fonts/BalooBhaijaan2-ExtraBold.ttf
ar_font      = "Baloo Bhaijaan 2:style=ExtraBold";
en_size      = 10.2;
ar_size      = 10.5;

/* ---------- colours (preview only) ---------- */
C_RED   = "#EF3D3D";   // menu page red
C_BUN   = "#F4DEB2";
C_CHEESE= "#F6C21B";
C_PATTY = "#4A2A1E";
C_LETTUCE = "#5FB23A";
C_TOMATO = "#E24B3A";
C_TEXT  = "#FFCC49";   // menu yellow (MENU wordmark)

/* ============================================================================
   2D SILHOUETTES  (front view; origin = burger centre)
   Y ranges: top bun 12..52 · cheese 2..12 (+drips) · patty -20..2 · bottom bun -42..-20
   ========================================================================== */
module rrect(w, h, r, cy=0, cx=0) { translate([cx, cy]) offset(r) offset(-r) square([w, h], center=true); }
module ellipse(cx, cy, rx, ry) { translate([cx, cy]) scale([rx, ry]) circle(1); }

// Layers OVERLAP like the reference sticker (front covers back). Each *_2d is the full shape.
module bun_top_2d()    { offset(5) offset(-5) intersection() { ellipse(0, 20, 62, 38); translate([-70, 16]) square([140, 44]); } }   // 16..58
R_LET = [[4.6, -1.2], [6.3, 1.4], [5.2, 0.2], [6.8, 1.0], [4.9, -0.8], [5.8, 1.6]];
module lettuce_2d()    { union() { translate([0, 14]) square([120, 6], center=true);
                                   for (i = [0:17]) translate([-62 + 7*i, 13 + R_LET[i % 6][1]]) circle(R_LET[i % 6][0]); } }
module tomato_2d()     { union() { rrect(54, 8, 3.8, 7.0, -29); rrect(54, 8, 3.8, 7.0, 29); } }                    // 3..11
module cheese_2d()     { rrect(118, 6, 2.5, 2); }                                                                  // -1..5, flat slice
module patty_2d()      { rrect(126, 20, 8, -7); }                                                                  // -17..3
module bun_bottom_2d() { rrect(122, 22, 9, -28); }                                                                 // -39..-17

// Disjoint pieces for inlays: layer (+outline ring) minus everything in front of it
module bun_top_cut()    { offset(outline) bun_top_2d(); }
module lettuce_cut()    { difference() { offset(outline) lettuce_2d(); bun_top_cut(); } }
module tomato_cut()     { difference() { offset(outline) tomato_2d(); bun_top_cut(); offset(outline) lettuce_2d(); } }
module cheese_cut()     { difference() { offset(outline) cheese_2d(); bun_top_cut(); offset(outline) lettuce_2d(); offset(outline) tomato_2d(); } }
module patty_cut()      { difference() { offset(outline) patty_2d(); bun_top_cut(); offset(outline) lettuce_2d(); offset(outline) tomato_2d(); offset(outline) cheese_2d(); } }
module bun_bottom_cut() { difference() { offset(outline) bun_bottom_2d(); offset(outline) patty_2d(); offset(outline) cheese_2d(); } }
module burger_2d()  { offset(outline) union() { bun_top_2d(); lettuce_2d(); tomato_2d(); cheese_2d(); patty_2d(); bun_bottom_2d(); } }
module halo_2d()    { offset(r = halo) burger_2d(); }

/* ---------- graphics ---------- */
module nfc_symbol_2d(s = 1) {
    // contactless "waves" mark: 4 concentric arcs, 90° span, stroke 1.6 mm
    for (r = [3.2, 6.2, 9.2, 12.2])
        scale(s) intersection() {
            difference() { circle(r + 0.8); circle(r - 0.8); }
            rotate(-45) square([r + 2, r + 2]);   // first quadrant, rotated so the arcs open to the right
        }
}
module sesame_2d() {
    for (p = [[-40, 33, 25], [-26, 44, 10], [-8, 51, -15], [12, 49, 20], [30, 42, -10], [46, 31, 30], [-18, 30, -25], [20, 30, 15], [2, 38, 5]])
        translate([p[0], p[1]]) rotate(p[2]) scale([1, 0.55]) circle(2.2);
}
module en_text_2d()  { text(en_text, size = en_size, font = en_font, halign = "center", valign = "center", spacing = 1.08); }
module ar_text_2d()  { text(ar_text, size = ar_size, font = ar_font, halign = "center", valign = "center", direction = "rtl", language = "ar", script = "arabic"); }

/* ============================================================================
   3D PARTS — each modelled with its FRONT face at z = 0 and body toward -z,
   so exporting a part and printing it "as is" puts the face on the bed.
   ========================================================================== */
module inlay(color_body, color_relief) {
    // children(0) = silhouette, children(1) = relief graphics (optional)
    color(color_body) translate([0, 0, -inlay_t]) linear_extrude(inlay_t) offset(-tol) children(0);
    if ($children > 1) color(color_relief) translate([0, 0, -0.01]) linear_extrude(relief_h + 0.01) children(1);
}

module part_bun_top()    { inlay(C_BUN, C_PATTY) { bun_top_cut(); sesame_2d(); } }
module part_cheese()     { inlay(C_CHEESE)       { cheese_cut(); } }
module part_lettuce()    { inlay(C_LETTUCE)      { lettuce_cut(); } }
module part_tomato()     { inlay(C_TOMATO)       { tomato_cut(); } }
module part_patty()      { inlay(C_PATTY, C_TEXT){ patty_cut(); translate([0, -9]) en_text_2d(); } }
module part_bun_bottom() { inlay(C_BUN, C_PATTY) { bun_bottom_cut(); translate([0, -28]) ar_text_2d(); } }

module keyhole_cuts() {
    for (k = keyholes) translate([k[0], k[1], 0]) {
        translate([0, 0, -base_t - 0.01]) linear_extrude(kh_depth + 0.01)
            hull() { circle(d = kh_head_d); translate([0, -kh_slot]) circle(d = kh_head_d); }   // head channel
        translate([0, 0, -base_t - 0.01]) linear_extrude(kh_depth + 1.01)
            union() { circle(d = kh_head_d); hull() { circle(d = kh_shank_d); translate([0, -kh_slot]) circle(d = kh_shank_d); } } // neck + entry
    }
}

module part_base() {
    color(C_RED) difference() {
        translate([0, 0, -base_t]) linear_extrude(base_t) halo_2d();                     // plate, front at z=0
        translate([0, 0, -recess_d]) linear_extrude(recess_d + 0.01) offset(tol) burger_2d(); // front recess
        translate([nfc_center[0], nfc_center[1], -recess_d - nfc_depth]) cylinder(d = nfc_d, h = nfc_depth + 0.01); // front pocket under the inlays
        keyhole_cuts();
    }
}

module part_one_piece() {
    // Single body: base + burger relief + raised graphics, for single-colour printing.
    color(C_RED) difference() {
        union() {
            translate([0, 0, -base_t]) linear_extrude(base_t) halo_2d();
            translate([0, 0, -recess_d]) linear_extrude(recess_d + inlay_t - recess_d) burger_2d();   // burger proud by inlay_t - recess_d
            translate([0, 0, inlay_t - recess_d - 0.01]) linear_extrude(relief_h + 0.01) union() {
                translate([-6, 31]) nfc_symbol_2d(1.15); sesame_2d();
                translate([0, -9]) en_text_2d(); translate([0, -28]) ar_text_2d();
            }
        }
        translate([nfc_center[0], nfc_center[1], -base_t - 0.01]) cylinder(d = nfc_d, h = 4.01);   // one-piece: pocket from the back, 4 mm deep
        keyhole_cuts();
    }
}

/* ---------- assembly preview: inlays sit in the recess (face proud by inlay_t - recess_d) ---------- */
module assembly() {
    part_base();
    translate([0, 0, inlay_t - recess_d]) { part_bun_top(); part_lettuce(); part_tomato(); part_cheese(); part_patty(); part_bun_bottom(); }
}

/* ---------- print plate: all parts face-down (rotate 180° about X so face is at z=0 pointing down → we flip so faces touch bed) ---------- */
module face_down() { mirror([0, 0, 1]) children(); }   // face at z=0, body toward +z

module plate() {
    face_down() part_base();
    translate([0, 130, 0])  face_down() part_bun_top();
    translate([0, 200, 0])  face_down() part_cheese();
    translate([0, 300, 0])  face_down() part_lettuce();
    translate([0, 330, 0])  face_down() part_tomato();
    translate([0, 230, 0])  face_down() part_patty();
    translate([0, 265, 0])  face_down() part_bun_bottom();
}

/* ---------- dispatcher ---------- */
if (part == "assembly")        assembly();
else if (part == "base")       face_down() part_base();
else if (part == "bun_top")    face_down() part_bun_top();
else if (part == "cheese")     face_down() part_cheese();
else if (part == "lettuce")    face_down() part_lettuce();
else if (part == "tomato")     face_down() part_tomato();
else if (part == "patty")      face_down() part_patty();
else if (part == "bun_bottom") face_down() part_bun_bottom();
else if (part == "one_piece")  face_down() part_one_piece();
else if (part == "plate")      plate();
