"""
ONE FOR ALL — "Tap for menu" burger NFC holder · build script
Generates, from one geometry definition (mm, front view, Y up):
  stl/*.stl                      printable parts (face-down orientation) + assembled preview
  laser/*.svg                    laser-cut / UV-print files (1 user unit = 1 mm), text as paths
  preview/front_view.svg         coloured front view for approval
Run:  python build_holder.py [--url https://short.link/for/qr]
Deps: trimesh shapely manifold3d mapbox_earcut fonttools uharfbuzz  (qrcode optional)
"""
import sys, os, math, argparse
import numpy as np
from shapely.geometry import Polygon, MultiPolygon, Point, LineString, box
from shapely.ops import unary_union
from shapely import affinity
import trimesh
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
import uharfbuzz as hb

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_STL = os.path.join(HERE, "stl"); OUT_LASER = os.path.join(HERE, "laser"); OUT_PREV = os.path.join(HERE, "preview")
for d in (OUT_STL, OUT_LASER, OUT_PREV): os.makedirs(d, exist_ok=True)

# ----------------------------------------------------------------------------- parameters (mirror the .scad)
W = 120.0; HALO = 6.0
BASE_T = 7.0; RECESS_D = 1.6; INLAY_T = 3.5; RELIEF_H = 0.6; TOL = 0.15
NFC_D = 40.0; NFC_DEPTH = 1.2; NFC_C = (0.0, -4.0)   # front pocket under the inlays: fits up to a 38 mm NTAG213 label (research: >=30 mm antenna)
KEYHOLES = [(-36.0, 26.0), (36.0, 26.0)]   # hidden wall fixing: screw head Ø7 / shank Ø4, slot 8 mm down, 3.2 mm deep from the back
KH_HEAD_D = 7.4; KH_SHANK_D = 4.4; KH_SLOT = 8.0; KH_DEPTH = 3.2
ACRYLIC_T = 3.0
EN_TEXT = "TAP FOR MENU"; AR_TEXT = "قرّب تلفونك"
EN_SIZE = 10.2; AR_SIZE = 10.5
LILITA = os.path.join(HERE, "fonts", "LilitaOne-Regular.ttf")     # Latin: Lilita One (Google Fonts, OFL)
LALEZAR = os.path.join(HERE, "fonts", "Lalezar-Regular.ttf")      # Arabic: Lalezar (Google Fonts, OFL)
BALOO = os.path.join(HERE, "fonts", "BalooBhaijaan2-ExtraBold.ttf")   # the menu's family — identity
FONTS = {"en": [BALOO, "seguibl.ttf"], "ar": [BALOO, "segoeuib.ttf"]}
FONT_DIR = r"C:\Windows\Fonts"
OUTLINE = 1.1   # black sticker outline around every layer, mm
WORDMARK = os.path.join(HERE, "fonts", "MENU_wordmark.json")   # the real MENU lettering, harvested from the menu PDF
MENU_H = 7.6     # wordmark height on the patty, mm (Baloo caps at EN_SIZE are ~6.6)
EN_TAP = "TAP FOR"
COL = {"red": "#EF3D3D", "bun": "#E4A34D", "cheese": "#FFCC49", "patty": "#4A2314", "text": "#FFF6EE", "cut": "#FF0000", "engrave": "#0000FF"}
MENU_RED, CARD_RED, CREAM, YELLOW, BROWN = "#EF3D3D", "#D82827", "#FFF6EE", "#FFCC49", "#4A2314"
ART = {  # every colour is the menu's or a tint/shade of it, so the piece sits with the menu like the menu sits with itself
    "plate": MENU_RED, "outline": BROWN,
    "bun_top": ("#F9CF7E", "#E4A34D"), "bun_top_hi": CREAM, "rim": "#C9873A", "sesame": CREAM,
    "lettuce": ("#7CC468", "#4E9E45"), "lettuce_rim": "#3F8538",
    "tomato": (CARD_RED, "#B91F1F"), "tomato_rim": "#9A1919",
    "cheese": (YELLOW, "#F0B22D"),
    "patty": ("#6B3A2A", BROWN),
    "bun_bottom": ("#F3C273", "#DB9A43"),
    "text": CREAM, "menu": YELLOW, "ar": BROWN}

# ----------------------------------------------------------------------------- 2D primitives
def rrect(w, h, r, cx=0.0, cy=0.0):
    return box(cx - w/2, cy - h/2, cx + w/2, cy + h/2).buffer(-r, join_style=1).buffer(r, join_style=1, resolution=24)

def ellipse(cx, cy, rx, ry, res=96):
    return affinity.scale(Point(cx, cy).buffer(1.0, resolution=res), rx, ry, origin=(cx, cy))

def bun_top():
    dome = ellipse(0, 20, 62, 38).intersection(box(-70, 16, 70, 60))          # 16..58, ~123 wide at the base
    return dome.buffer(-5, join_style=1).buffer(5, join_style=1, resolution=32)  # rounds the two lower corners

def lettuce():
    R = ((4.6, -1.2), (6.3, 1.4), (5.2, 0.2), (6.8, 1.0), (4.9, -0.8), (5.8, 1.6))
    blobs = [Point(x, 13 + R[i % 6][1]).buffer(R[i % 6][0], resolution=20) for i, x in enumerate(range(-62, 63, 7))]
    return unary_union(blobs + [box(-60, 11, 60, 17)])                         # ~7..20, irregular ruffles past the bun

def tomato():     return unary_union([rrect(54, 8, 3.8, -29, 7.0), rrect(54, 8, 3.8, 29, 7.0)])     # 3..11

def cheese():
    return rrect(118, 6, 2.5, 0, 2)                                            # -1..5, flat slice, no drips (Zaid)

def patty():      return rrect(126, 20, 8, 0, -7)                              # -17..3 (16 mm visible under the cheese) — burger proportions
def bun_bottom(): return rrect(122, 22, 9, 0, -28)                             # -39..-17

FULL_ORDER = ["bun_bottom", "patty", "cheese", "tomato", "lettuce", "bun_top"]  # back → front
def full_layers(): return dict(bun_top=bun_top(), lettuce=lettuce(), tomato=tomato(), cheese=cheese(), patty=patty(), bun_bottom=bun_bottom())
def disjoint_layers():
    """Non-overlapping pieces for solid-colour inlays / STL parts: each layer (incl. its outline ring) minus everything in front."""
    F = {k: v.buffer(OUTLINE, join_style=1) for k, v in full_layers().items()}
    out, front = {}, None
    for name in reversed(FULL_ORDER):
        out[name] = F[name] if front is None else F[name].difference(front)
        front = F[name] if front is None else front.union(F[name])
    return out
def burger():     return unary_union([v.buffer(OUTLINE, join_style=1) for v in full_layers().values()])
def halo():       return burger().buffer(HALO, join_style=1, resolution=32)

def nfc_symbol(cx, cy, s=1.15, stroke=1.6):
    arcs = []
    for r in (3.2, 6.2, 9.2, 12.2):
        pts = [(cx + s*r*math.cos(a), cy + s*r*math.sin(a)) for a in np.linspace(-math.pi/4, math.pi/4, 40)]
        arcs.append(LineString(pts).buffer(s*stroke/2, resolution=12))
    return unary_union(arcs)

def sesame():
    seeds = []
    for x, y, ang in ((-40, 33, 25), (-26, 44, 10), (-8, 51, -15), (12, 49, 20), (30, 42, -10), (46, 31, 30), (-18, 30, -25), (20, 30, 15), (2, 38, 5)):
        e = affinity.scale(Point(0, 0).buffer(2.2, resolution=16), 1, 0.55)
        seeds.append(affinity.translate(affinity.rotate(e, ang), x, y))
    return unary_union(seeds)

# ----------------------------------------------------------------------------- text → polygons (HarfBuzz shaping + fontTools outlines)
def _pick_font(lang, sample):
    for name in FONTS[lang]:
        p = name if os.path.isabs(name) else os.path.join(FONT_DIR, name)
        if not os.path.exists(p): continue
        cmap = TTFont(p).getBestCmap()
        if all(ord(ch) in cmap for ch in sample if not ch.isspace() and ord(ch) not in (0x651,)):  # shadda may be combining
            return p
    raise SystemExit(f"No font with glyphs for {lang!r} text found in {FONT_DIR}")

def _flatten(pen_value, upem):
    """RecordingPen ops → list of shapely Polygons (one per contour), scaled to font units 1.0 = 1 em."""
    contours, cur = [], []
    def add(p): cur.append((p[0]/upem, p[1]/upem))
    def quad(p0, p1, p2, n=10):
        for t in np.linspace(0, 1, n+1)[1:]:
            add(((1-t)**2*p0[0] + 2*(1-t)*t*p1[0] + t**2*p2[0], (1-t)**2*p0[1] + 2*(1-t)*t*p1[1] + t**2*p2[1]))
    def cubic(p0, p1, p2, p3, n=12):
        for t in np.linspace(0, 1, n+1)[1:]:
            add(((1-t)**3*p0[0] + 3*(1-t)**2*t*p1[0] + 3*(1-t)*t**2*p2[0] + t**3*p3[0],
                 (1-t)**3*p0[1] + 3*(1-t)**2*t*p1[1] + 3*(1-t)*t**2*p2[1] + t**3*p3[1]))
    last = None
    for op, args in pen_value:
        if op == "moveTo": cur = []; add(args[0]); last = args[0]
        elif op == "lineTo": add(args[0]); last = args[0]
        elif op == "qCurveTo":
            pts = list(args)
            if pts[-1] is None:                       # closed contour made only of off-curve points (TrueType)
                pts = pts[:-1]
                start = ((pts[-1][0] + pts[0][0]) / 2, (pts[-1][1] + pts[0][1]) / 2)
                cur = []; add(start); last = start
                pts = pts + [start]
            # implied on-curve points between consecutive off-curve points
            p0 = last
            for i in range(len(pts) - 1):
                c = pts[i]; nxt = pts[i+1]
                end = ((c[0]+nxt[0])/2, (c[1]+nxt[1])/2) if i < len(pts) - 2 else nxt
                quad(p0, c, end); p0 = end
            last = pts[-1]
        elif op == "curveTo":
            pts = list(args); p0 = last
            for i in range(0, len(pts) - 2, 3):
                cubic(p0, pts[i], pts[i+1], pts[i+2]); p0 = pts[i+2]
            last = pts[-1]
        elif op in ("closePath", "endPath"):
            if len(cur) >= 3: contours.append(Polygon(cur))
            cur = []
    return contours

def _shape(txt, size_mm, lang):
    """HarfBuzz-shaped glyph polygons, one entry per glyph, in mm, left-to-right visual order, pen at x=0."""
    path = _pick_font(lang, txt)
    tt = TTFont(path); upem = tt["head"].unitsPerEm; gs = tt.getGlyphSet(); order = tt.getGlyphOrder()
    blob = hb.Blob.from_file_path(path); face = hb.Face(blob); font = hb.Font(face); font.scale = (upem, upem)
    buf = hb.Buffer(); buf.add_str(txt); buf.guess_segment_properties()
    if lang == "ar": buf.direction, buf.script, buf.language = "rtl", "Arab", "ar"
    hb.shape(font, buf, {"kern": True, "liga": True})
    x = 0.0; glyphs = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        gname = order[info.codepoint]
        pen = DecomposingRecordingPen(gs); gs[gname].draw(pen)
        conts = _flatten(pen.value, upem)
        if conts:
            outers = [c.buffer(0) for c in conts if not c.exterior.is_ccw]
            inners = [c.buffer(0) for c in conts if c.exterior.is_ccw]
            if not outers and inners: outers, inners = inners, []
            poly = unary_union(outers)
            if inners: poly = poly.difference(unary_union(inners))
            if not poly.is_empty:
                glyphs.append(affinity.scale(affinity.translate(poly, (x + pos.x_offset)/upem, pos.y_offset/upem), size_mm, size_mm, origin=(0, 0)))
        x += pos.x_advance
    return glyphs

def text_polys(txt, size_mm, lang):
    g = unary_union(_shape(txt, size_mm, lang)); minx, miny, maxx, maxy = g.bounds
    return affinity.translate(g, -(minx+maxx)/2, -(miny+maxy)/2)

def _wobble(poly, amp=0.11, wl=5.5, seed=1):
    """Hand-drawn edge: densify the outline and push each point along its normal by smooth low-frequency noise."""
    rng = np.random.default_rng(seed)
    def ring(coords):
        pts = np.array(coords[:-1], dtype=float)
        if len(pts) < 4: return pts
        seg = np.linalg.norm(np.diff(np.vstack([pts, pts[:1]]), axis=0), axis=1)
        t = np.concatenate([[0], np.cumsum(seg)[:-1]])
        ph = rng.uniform(0, 2*np.pi, 3)
        d = amp * (np.sin(2*np.pi*t/wl + ph[0]) + 0.6*np.sin(2*np.pi*t/(wl*0.47) + ph[1]) + 0.3*np.sin(2*np.pi*t/(wl*2.3) + ph[2]))
        nxt = np.roll(pts, -1, axis=0); prv = np.roll(pts, 1, axis=0)
        tang = nxt - prv; tang /= (np.linalg.norm(tang, axis=1, keepdims=True) + 1e-9)
        normal = np.stack([tang[:, 1], -tang[:, 0]], axis=1)
        return pts + normal * d[:, None]
    if isinstance(poly, MultiPolygon):                                   # dots, split glyphs: treat each part on its own
        return unary_union([_wobble(q, amp, wl, seed + k) for k, q in enumerate(poly.geoms)])
    dense = poly.segmentize(0.35)
    out = Polygon(ring(dense.exterior.coords), [ring(i.coords) for i in dense.interiors]).buffer(0)
    return out.buffer(0.22, join_style=1).buffer(-0.22, join_style=1)   # soften corners like a marker stroke

def handlettered(txt, size_mm, lang, seed=7):
    """Bounce each unit (Latin: letter, Arabic: word, so joins stay intact) with a small rotation / lift / scale, then wobble edges."""
    rng = np.random.default_rng(seed)
    if lang == "ar":
        units, x = [], 0.0
        for w in txt.split(" ")[::-1]:                     # visual order left→right for RTL words
            g = unary_union(_shape(w, size_mm, lang)); minx, miny, maxx, maxy = g.bounds
            units.append(affinity.translate(g, x - minx, 0)); x += (maxx - minx) + size_mm * 0.28
    else:
        units = [g for g in _shape(txt, size_mm, lang)]
    out = []
    for i, g in enumerate(units):
        c = g.centroid
        g = affinity.rotate(g, rng.uniform(-4.5, 4.5), origin=c)
        g = affinity.scale(g, rng.uniform(0.96, 1.05), rng.uniform(0.95, 1.06), origin=c)
        g = affinity.translate(g, 0, rng.uniform(-0.45, 0.45))
        out.append(_wobble(g, seed=seed + i))
    g = unary_union(out); minx, miny, maxx, maxy = g.bounds
    return affinity.translate(g, -(minx+maxx)/2, -(miny+maxy)/2)

# ----------------------------------------------------------------------------- 3D helpers
def extrude(poly, h, z0=0.0):
    """Extrude a shapely (Multi)Polygon by h starting at z0. Holes preserved."""
    polys = list(poly.geoms) if isinstance(poly, MultiPolygon) else [poly]
    meshes = [trimesh.creation.extrude_polygon(p, h) for p in polys if not p.is_empty and p.area > 1e-6]
    m = trimesh.util.concatenate(meshes) if len(meshes) > 1 else meshes[0]
    m.apply_translation([0, 0, z0]); return m

def union(*ms):  ms = [m for m in ms if m is not None]; return trimesh.boolean.union(ms, engine="manifold") if len(ms) > 1 else ms[0]
def diff(a, b):  return trimesh.boolean.difference([a, b], engine="manifold")
def cyl(d, h, cx, cy, z0): c = trimesh.creation.cylinder(radius=d/2, height=h, sections=96); c.apply_translation([cx, cy, z0 + h/2]); return c

def keyhole_cut_safe():
    cuts = []
    for kx, ky in KEYHOLES:
        head = Point(kx, ky).buffer(KH_HEAD_D/2, resolution=48).union(LineString([(kx, ky), (kx, ky - KH_SLOT)]).buffer(KH_HEAD_D/2, resolution=24))
        cuts.append(extrude(head, KH_DEPTH + 0.02, -BASE_T - 0.01))                 # head channel, 3.2 mm deep
        shank = LineString([(kx, ky), (kx, ky - KH_SLOT)]).buffer(KH_SHANK_D/2, resolution=24).union(Point(kx, ky).buffer(KH_HEAD_D/2, resolution=48))
        cuts.append(extrude(shank, KH_DEPTH + 1.0 + 0.02, -BASE_T - 0.01))          # shank neck 1 mm deeper → head is captured behind a lip
    return cuts

def face_down(m):
    """Parts are modelled with the front face at z=0 and the body at z<0. Mirror so the face lies on the bed (z=0) and body is +z."""
    m = m.copy(); m.apply_transform(np.diag([1, 1, -1, 1])); m.fix_normals(); return m

def inlay_part(sil, relief=None):
    body = extrude(sil.buffer(-TOL, join_style=1), INLAY_T, -INLAY_T)
    if relief is not None and not relief.is_empty:
        body = union(body, extrude(relief.intersection(sil.buffer(-TOL-0.3)), RELIEF_H + 0.02, -0.02))
    return body

# ----------------------------------------------------------------------------- SVG writer
def _ring(coords, flipy):
    pts = [(x, -y if flipy else y) for x, y in coords]
    return "M" + " L".join(f"{x:.3f},{y:.3f}" for x, y in pts) + " Z"

def path_d(geom, flipy=True):
    polys = list(geom.geoms) if isinstance(geom, MultiPolygon) else ([geom] if not geom.is_empty else [])
    return " ".join(_ring(p.exterior.coords, flipy) + " " + " ".join(_ring(i.coords, flipy) for i in p.interiors) for p in polys)

def svg_doc(width, height, body, title, ox=0.0, oy=0.0):
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}mm" height="{height}mm" viewBox="{ox:.3f} {oy:.3f} {width:.3f} {height:.3f}">\n'
            f'<title>{title}</title>\n{body}\n</svg>\n')

def write(path, s):
    with open(path, "w", encoding="utf-8") as f: f.write(s)
    print("  wrote", os.path.relpath(path, HERE))

# ----------------------------------------------------------------------------- build
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--url", default=None, help="URL to encode as optional QR on the bottom bun (laser engrave variant)")
    a = ap.parse_args()

    print("Shaping text …")
    # "TAP FOR" in the menu's clean font + the real "MENU" wordmark, one centred group on the beef band (-2..-16)
    import json
    wm = json.load(open(WORDMARK))
    menu = unary_union([Polygon(q["exterior"], q["holes"]) for q in wm["polygons"]])
    menu = affinity.scale(menu, MENU_H, MENU_H, origin=(0, 0))                     # normalised height 1 → MENU_H mm
    tap = handlettered(EN_TAP, EN_SIZE, "en", seed=7)
    gap = 3.2; tw = tap.bounds[2] - tap.bounds[0]; mw = menu.bounds[2] - menu.bounds[0]; total = tw + gap + mw
    tap = affinity.translate(tap, -total/2 + tw/2, -9); menu = affinity.translate(menu, total/2 - mw/2, -9)
    en_tap, en_menu = tap, menu
    en = unary_union([tap, menu])
    ar = affinity.translate(handlettered(AR_TEXT, AR_SIZE, "ar", seed=11), 0, -28)
    print(f"  EN bbox {tuple(round(v,1) for v in en.bounds)}   AR bbox {tuple(round(v,1) for v in ar.bounds)}")
    assert en.bounds[2] - en.bounds[0] < 100, "EN text too wide for the patty — reduce EN_SIZE"
    assert ar.bounds[2] - ar.bounds[0] < 100, "AR text too wide for the bottom bun — reduce AR_SIZE"

    S = disjoint_layers(); FULL = full_layers()
    B, H = burger(), halo()
    gfx_top = sesame()

    # ---------------- STL parts (front face at z=0, body at -z) ----------------
    print("Building 3D parts …")
    base = extrude(H, BASE_T, -BASE_T)
    base = diff(base, extrude(B.buffer(TOL, join_style=1), RECESS_D + 0.02, -RECESS_D))
    base = diff(base, cyl(NFC_D, NFC_DEPTH + 0.02, NFC_C[0], NFC_C[1], -RECESS_D - NFC_DEPTH))   # tag pocket opens to the FRONT, inside the recess
    for kc in keyhole_cut_safe(): base = diff(base, kc)
    parts = {
        "base":       base,
        "bun_top":    inlay_part(S["bun_top"], gfx_top),
        "lettuce":    inlay_part(S["lettuce"]),
        "tomato":     inlay_part(S["tomato"]),
        "cheese":     inlay_part(S["cheese"]),
        "patty":      inlay_part(S["patty"], en),
        "bun_bottom": inlay_part(S["bun_bottom"], ar),
    }
    for name, m in parts.items():
        fd = face_down(m)
        assert fd.is_watertight, f"{name} not watertight"
        fd.export(os.path.join(OUT_STL, f"ofa_{name}.stl")); print(f"  wrote stl/ofa_{name}.stl  ({fd.extents.round(1)} mm, {fd.volume/1000:.1f} cm³)")

    # one-piece single-colour version
    one = union(extrude(H, BASE_T, -BASE_T), extrude(B, INLAY_T, -RECESS_D),
                extrude(unary_union([gfx_top, en, ar]), RELIEF_H + 0.02, INLAY_T - RECESS_D - 0.02))
    one = diff(one, cyl(NFC_D, 4.0 + 0.02, NFC_C[0], NFC_C[1], -BASE_T - 0.01))   # one-piece: pocket from the back, 4 mm deep
    for kc in keyhole_cut_safe(): one = diff(one, kc)
    fd = face_down(one); fd.export(os.path.join(OUT_STL, "ofa_one_piece_single_colour.stl")); print(f"  wrote stl/ofa_one_piece_single_colour.stl ({fd.extents.round(1)} mm)")

    # assembled preview (colours embedded) — for viewing only
    lift = INLAY_T - RECESS_D
    scene = []
    for name, colour in (("base", COL["red"]), ("bun_top", COL["bun"]), ("lettuce", "#5FB23A"), ("tomato", "#E24B3A"), ("cheese", COL["cheese"]), ("patty", COL["patty"]), ("bun_bottom", COL["bun"])):
        m = parts[name].copy()
        if name != "base": m.apply_translation([0, 0, lift])
        m.visual.face_colors = trimesh.visual.color.hex_to_rgba(colour); scene.append(m)
    trimesh.util.concatenate(scene).export(os.path.join(OUT_STL, "ofa_assembled_preview.glb")); print("  wrote stl/ofa_assembled_preview.glb")

    # ---------------- Laser files (3 mm acrylic, flush inlay build) ----------------
    print("Writing laser files …")
    kerf_note = "<!-- 1 unit = 1 mm. RED stroke = CUT through. BLUE stroke = ENGRAVE / UV-PRINT artwork. No kerf compensation applied; ask the shop to cut inlays on the inside of the line and the frame on the outside, or apply 0.1 mm offset. -->"
    def layer(name, geoms_cut, geoms_engrave=(), fill="none"):
        allg = unary_union(list(geoms_cut) + list(geoms_engrave)); minx, miny, maxx, maxy = allg.bounds; pad = 5
        body = kerf_note + "\n" + "".join(f'<path d="{path_d(g)}" fill="{fill}" stroke="{COL["cut"]}" stroke-width="0.1"/>\n' for g in geoms_cut)
        body += "".join(f'<path d="{path_d(g)}" fill="none" stroke="{COL["engrave"]}" stroke-width="0.1"/>\n' for g in geoms_engrave if not g.is_empty)
        write(os.path.join(OUT_LASER, name), svg_doc(maxx-minx+2*pad, maxy-miny+2*pad, body, name, minx-pad, -maxy-pad))

    frame = H.difference(B.buffer(TOL, join_style=1))
    nfc_pocket = Point(*NFC_C).buffer(NFC_D/2, resolution=64)                 # engrave ~1 mm deep in L0 for a coin tag (skip for stickers)
    layer("L0_backplate_RED_3mm.svg", [H], [nfc_pocket])
    layer("L1_frame_RED_3mm.svg", [frame])
    layer("L2_inlay_bun_CREAM_3mm.svg", [S["bun_top"].buffer(-TOL, join_style=1), S["bun_bottom"].buffer(-TOL, join_style=1)], [gfx_top, ar])
    layer("L2_inlay_cheese_YELLOW_3mm.svg", [S["cheese"].buffer(-TOL, join_style=1)])
    layer("L2_inlay_lettuce_GREEN_3mm.svg", [S["lettuce"].buffer(-TOL, join_style=1)])
    layer("L2_inlay_tomato_RED_3mm.svg", [S["tomato"].buffer(-TOL, join_style=1)])
    layer("L2_inlay_patty_BROWN_3mm.svg", [S["patty"].buffer(-TOL, join_style=1)], [en])

    # optional QR (engrave on bottom bun, right side) — only if a URL is given
    if a.url:
        try:
            import qrcode
            q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0); q.add_data(a.url); q.make(fit=True)
            mat = q.get_matrix(); n = len(mat); size = 18.0; mod = size/n; x0, y0 = 60 - 8 - size, -42 + 2
            cells = [box(x0 + j*mod, y0 + (n-1-i)*mod, x0 + (j+1)*mod, y0 + (n-i)*mod) for i in range(n) for j in range(n) if mat[i][j]]
            layer("OPTIONAL_qr_on_bun_bottom_engrave.svg", [S["bun_bottom"].buffer(-TOL, join_style=1)], [unary_union(cells), affinity.translate(ar, -12, 0)])
            print(f"  QR: {n}x{n} modules at {mod:.2f} mm (>= 0.4 mm/module is scannable)")
        except ImportError:
            print("  (pip install qrcode to generate the optional QR layer)")

    # nested sheet with all layers + legend
    tiles = [("L0 back plate · RED", [H], [nfc_pocket]), ("L1 frame · RED", [frame], []),
             ("L2 buns · CREAM", [S["bun_top"].buffer(-TOL), S["bun_bottom"].buffer(-TOL)], [gfx_top, ar]),
             ("L2 cheese · YELLOW", [S["cheese"].buffer(-TOL)], []), ("L2 lettuce · GREEN", [S["lettuce"].buffer(-TOL)], []),
             ("L2 tomato · RED", [S["tomato"].buffer(-TOL)], []), ("L2 patty · BROWN", [S["patty"].buffer(-TOL)], [en])]
    body, x = kerf_note + "\n", 0.0
    for label, cuts, engs in tiles:
        g = unary_union(cuts); minx, miny, maxx, maxy = g.bounds; dx = x - minx + 5
        body += f'<g transform="translate({dx:.3f},0)">' + "".join(f'<path d="{path_d(c)}" fill="none" stroke="{COL["cut"]}" stroke-width="0.1"/>' for c in cuts)
        body += "".join(f'<path d="{path_d(e)}" fill="none" stroke="{COL["engrave"]}" stroke-width="0.1"/>' for e in engs if not e.is_empty)
        body += f'<text x="{(minx+maxx)/2:.1f}" y="{-miny+8:.1f}" font-family="Arial" font-size="5" text-anchor="middle" fill="#888">{label}</text></g>\n'
        x += (maxx - minx) + 10
    write(os.path.join(OUT_LASER, "ALL_LAYERS_nested_3mm.svg"), svg_doc(x + 10, 130, body, "One For All NFC holder — all laser layers", -5, -70))

    # ---------------- Front-view preview (coloured, assembled) ----------------
    print("Writing preview …")
    body = f'<rect x="-100" y="-100" width="400" height="300" fill="#D8542E"/>'   # tile-wall orange for context
    body += f'<path d="{path_d(H)}" fill="{COL["red"]}"/>'
    body += f'<path d="{path_d(H)}" fill="none" stroke="rgba(0,0,0,.15)" stroke-width="0.6"/>'
    for name, col in (("bun_top", COL["bun"]), ("lettuce", "#5FB23A"), ("tomato", "#E24B3A"), ("cheese", COL["cheese"]), ("patty", COL["patty"]), ("bun_bottom", COL["bun"])):
        body += f'<path d="{path_d(S[name].buffer(-TOL))}" fill="{col}"/>'
    body += f'<path d="{path_d(gfx_top)}" fill="{COL["patty"]}"/><path d="{path_d(en)}" fill="{COL["text"]}"/><path d="{path_d(ar)}" fill="{COL["patty"]}"/>'
    body += f'<circle cx="{NFC_C[0]}" cy="{-NFC_C[1]}" r="{NFC_D/2}" fill="none" stroke="rgba(255,255,255,.35)" stroke-width="0.4" stroke-dasharray="1.5 1.5"/>'
    body += '<text x="0" y="66" font-family="Arial" font-size="4.2" text-anchor="middle" fill="#fff" opacity=".85">130 × 104 mm · dashed = NFC tag zone (inside, invisible)</text>'
    write(os.path.join(OUT_PREV, "front_view.svg"), svg_doc(170, 150, body, "One For All — Tap for menu holder, front view", -85, -75))

    # ---------------- Realistic raster (PIL): preview, night variant, UV-print artwork ----------------
    from PIL import Image, ImageDraw, ImageFilter
    PX = 12  # px per mm  (= 304.8 dpi, print-ready)
    w_mm, h_mm = 150, 136

    def to_px(pts): return [((x + w_mm/2)*PX, (h_mm/2 - y)*PX) for x, y in pts]
    def polys_of(g): return [q for q in (list(g.geoms) if isinstance(g, MultiPolygon) else [g]) if not q.is_empty]
    def mask_of(g, size):
        m = Image.new("L", size, 0); d = ImageDraw.Draw(m)
        for q in polys_of(g):
            d.polygon(to_px(q.exterior.coords), fill=255)
            for i in q.interiors: d.polygon(to_px(i.coords), fill=0)
        return m
    def hex2rgb(h): h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    def paint(img, g, colour):
        if isinstance(colour, tuple) and isinstance(colour[0], str):   # vertical gradient top→bottom over the shape's bbox
            minx, miny, maxx, maxy = g.bounds
            y0, y1 = (h_mm/2 - maxy)*PX, (h_mm/2 - miny)*PX
            c0, c1 = hex2rgb(colour[0]), hex2rgb(colour[1])
            grad = Image.new("RGB", img.size, c1); gd = ImageDraw.Draw(grad)
            steps = max(2, int(y1 - y0))
            for k in range(steps):
                t = k / (steps - 1); col = tuple(int(c0[j] + (c1[j] - c0[j]) * t) for j in range(3))
                gd.line([(0, y0 + k), (img.size[0], y0 + k)], fill=col)
            img.paste(grad, (0, 0), mask_of(g, img.size))
        else:
            img.paste(Image.new("RGB", img.size, hex2rgb(colour)), (0, 0), mask_of(g, img.size))

    def draw_burger(img, with_plate=True, night=False):
        A = ART; OUT = A["outline"]
        if with_plate: paint(img, H, "#B92E2E" if night else A["plate"])
        def layer(g, fill, extras=()):
            paint(img, g.buffer(OUTLINE, join_style=1), OUT)      # sticker outline
            paint(img, g, fill)
            for gg, c in extras: paint(img, gg, c)
        bb, pt, ch, tm, lt, bt = (FULL[k] for k in FULL_ORDER)
        layer(bb, A["bun_bottom"], [(bb.intersection(box(-70, -39, 70, -36.5)), A["rim"])])
        layer(pt, A["patty"], [(pt.intersection(box(-70, -17, 70, -14.5)), "#3A1B10")])
        layer(ch, A["cheese"])
        layer(tm, A["tomato"], [(tm.intersection(box(-70, 3, 70, 4.5)), A["tomato_rim"])])
        layer(lt, A["lettuce"], [(lt.intersection(box(-70, 6, 70, 10)), A["lettuce_rim"])])
        crescent = bt.intersection(ellipse(-3, 42, 46, 12)).difference(ellipse(-3, 39, 43, 10.5))
        layer(bt, A["bun_top"], [(bt.intersection(box(-70, 16, 70, 19)), A["rim"]), (crescent, A["bun_top_hi"]), (gfx_top, A["sesame"])])
        # soft shadow the crown throws on the lettuce
        sh = Image.new("L", img.size, 0); sd = ImageDraw.Draw(sh)
        for q in polys_of(bt.buffer(1.6).difference(bt).intersection(lt)): sd.polygon(to_px(q.exterior.coords), fill=110)
        img.paste(Image.new("RGB", img.size, (30, 15, 8)), (0, 0), sh.filter(ImageFilter.GaussianBlur(PX*0.7)))
        # text: cream with dark outline on the patty; dark with cream outline on the heel
        paint(img, en_tap, A["text"]); paint(img, en_menu, A["menu"]); paint(img, ar, A["ar"])   # flat type, exactly like the menu

    # preview on a plaster-grey wall
    img = Image.new("RGB", (w_mm*PX, h_mm*PX), "#B9B4AA")
    paint(img, H.buffer(1.5), "#8f8a80"); draw_burger(img)
    img.save(os.path.join(OUT_PREV, "front_view.png")); print("  wrote preview/front_view.png")

    # night / edge-lit: dark wall, warm light leaking from behind the plate
    night = Image.new("RGB", (w_mm*PX, h_mm*PX), "#2A2622")
    glow = mask_of(H.buffer(4), night.size).filter(ImageFilter.GaussianBlur(PX*3))
    night.paste(Image.new("RGB", night.size, "#FFB347"), (0, 0), glow)
    draw_burger(night, night=True)
    night.save(os.path.join(OUT_PREV, "front_view_night_edgelit.png")); print("  wrote preview/front_view_night_edgelit.png")

    # UV-print artwork for the single-piece acrylic face: burger only, transparent outside, 304.8 dpi, 1 px = 1/12 mm
    art = Image.new("RGB", (w_mm*PX, h_mm*PX), "#FFFFFF"); draw_burger(art, with_plate=False)
    rgba = art.convert("RGBA"); rgba.putalpha(mask_of(B.buffer(-TOL), art.size))
    minx, miny, maxx, maxy = B.bounds
    crop = rgba.crop((int((minx + w_mm/2)*PX) - 2, int((h_mm/2 - maxy)*PX) - 2, int((maxx + w_mm/2)*PX) + 2, int((h_mm/2 - miny)*PX) + 2))
    crop.save(os.path.join(OUT_LASER, "L2_FACE_artwork_UVPRINT_304dpi.png"), dpi=(304.8, 304.8))
    print(f"  wrote laser/L2_FACE_artwork_UVPRINT_304dpi.png  ({crop.size[0]/PX:.1f} x {crop.size[1]/PX:.1f} mm)")
    layer("L2_FACE_single_piece_CREAM_3mm_UVPRINT.svg", [B.buffer(-TOL, join_style=1)], [en, ar])
    print("Done.")

if __name__ == "__main__":
    main()
