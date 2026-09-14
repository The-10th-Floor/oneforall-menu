"""Re-render the menu pages from the source PDF (page 1 = English, page 2 = Arabic).
Usage: python render.py source/<menu>.pdf
"""
import sys, pymupdf
doc = pymupdf.open(sys.argv[1])
for page, name in zip(doc, ["en", "ar"]):
    z = 1300 / page.rect.width
    page.get_pixmap(matrix=pymupdf.Matrix(z, z), alpha=False).save(f"menu-{name}.png")
