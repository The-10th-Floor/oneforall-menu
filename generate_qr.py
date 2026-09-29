"""Generate the fixed menu QR. Install: pip install 'qrcode[pil]==8.2'.
Run: python generate_qr.py [--check]
"""
import argparse
from io import BytesIO
from pathlib import Path

import qrcode
from PIL import Image, ImageChops
from qrcode.image.svg import SvgPathFillImage

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--check", action="store_true", help="verify committed files without writing")
args = parser.parse_args()
root = Path(__file__).resolve().parent
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=24, border=4)
qr.add_data("https://the-10th-floor.github.io/oneforall-menu/")
qr.make(fit=True)
png = qr.make_image().convert("RGB")
svg = BytesIO()
qr.make_image(image_factory=SvgPathFillImage).save(svg)

# Keep the entire four-module quiet zone white, including all corners.
margin = 4 * qr.box_size
size = png.width
for bounds in [(0, 0, size, margin), (0, size-margin, size, size),
               (0, 0, margin, size), (size-margin, 0, size, size)]:
    assert png.crop(bounds).getextrema() == ((255, 255),) * 3

if args.check:
    with Image.open(root / "qr.png") as saved:
        assert saved.size == png.size, "QR dimensions changed"
        assert saved.convert("RGBA").getchannel("A").getextrema() == (255, 255), "QR must be opaque"
        assert ImageChops.difference(saved.convert("RGB"), png).getbbox() is None, "QR pixels changed"
    assert (root / "qr.svg").read_bytes() == svg.getvalue(), "QR SVG changed"
    print("PASS: both QR files match the fixed URL and four-module quiet zone")
else:
    png.save(root / "qr.png", optimize=True)
    (root / "qr.svg").write_bytes(svg.getvalue())
    print(f"Generated qr.png ({size}×{size}) and qr.svg with a four-module white quiet zone")
