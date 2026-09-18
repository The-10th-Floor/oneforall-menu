"""Re-render the menu pages from the source PDF (page 1 = English, page 2 = Arabic).
Writes menu-<lang>.svg (what the page shows) and menu-<lang>.png (og:image + no-JS fallback).
Usage: python render.py source/<menu>.pdf
"""
import base64, re, sys, pymupdf

doc = pymupdf.open(sys.argv[1])
for page, name in zip(doc, ["en", "ar"]):
    z = 1300 / page.rect.width
    page.get_pixmap(matrix=pymupdf.Matrix(z, z), alpha=False).save(f"menu-{name}.png")
    svg = page.get_svg_image()
    # Browsers paint a print (CMYK) JPEG black. Swap each one for an RGB PNG taken from the PDF itself -
    # decoding the JPEG bytes on their own loses Adobe's inverted-CMYK flag and comes out black too.
    for xref, w, h in [(i[0], i[2], i[3]) for i in page.get_images(full=True) if i[5] == "DeviceCMYK"]:
        png = pymupdf.Pixmap(pymupdf.csRGB, pymupdf.Pixmap(doc, xref)).tobytes("png")
        svg, n = re.subn(r'(<image [^>]*width="%d" height="%d" xlink:href=")data:image/jpeg;base64,[A-Za-z0-9+/=\s]+?"' % (w, h),
                         lambda m: m.group(1) + "data:image/png;base64," + base64.b64encode(png).decode() + '"', svg, count=1)
        assert n == 1, f"CMYK image {xref} ({w}x{h}) not found in the {name} SVG"
    open(f"menu-{name}.svg", "w", encoding="utf-8", newline="\n").write(svg)
