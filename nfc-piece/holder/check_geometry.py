"""Measure the checked-in prototype; does not certify fabrication or NFC performance."""
from pathlib import Path
import hashlib
import json
import math
import re
import struct
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent


def spans(points):
    return [max(p[i] for p in points) - min(p[i] for p in points) for i in range(3)]


def svg_bounds(path):
    root = ET.parse(path).getroot()
    assert root.get('width', '').endswith('mm') and root.get('height', '').endswith('mm'), path
    view = [float(v) for v in root.get('viewBox', '').split()]
    assert len(view) == 4 and all(math.isfinite(v) for v in view), 'Invalid viewBox'
    assert all(abs(float(root.get(k)[:-2]) - view[i]) < .002 for k, i in [('width', 2), ('height', 3)]), 'Expected 1 SVG unit = 1 mm'
    assert not any('transform' in e.attrib or 'style' in e.attrib for e in root.iter()), 'Transforms/styles need a geometry reader'
    assert all(e.tag.rsplit('}', 1)[-1] in {'svg', 'title', 'path'} for e in root.iter()), 'Unsupported SVG geometry'
    points = []
    for element in root.findall('{http://www.w3.org/2000/svg}path'):
        if element.get('stroke') != '#FF0000':
            continue
        data = element.get('d', '')
        assert re.fullmatch(r'(?:[ML]-?\d+(?:\.\d+)?,[-]?\d+(?:\.\d+)?\s*|Z\s*)+', data), 'Only absolute M/L/Z prototype paths are supported'
        points += [(float(x), float(y), 0) for x, y in re.findall(r'[ML](-?[\d.]+),(-?[\d.]+)', data)]
    assert points, 'No cut paths'
    return spans(points)[:2]


def stl_bounds(path):
    data = path.read_bytes()
    assert len(data) >= 84, 'Truncated STL'
    count = struct.unpack_from('<I', data, 80)[0]
    assert count and len(data) == 84 + 50 * count, 'Expected a complete binary STL'
    points = [struct.unpack_from('<3f', data, 84 + i * 50 + 12 + j * 12) for i in range(count) for j in range(3)]
    assert all(math.isfinite(v) for p in points for v in p), 'Nonfinite vertex'
    return spans(points)


if __name__ == '__main__':
    # Rejected engraving must stop before optional geometry imports or output writes.
    rejected = subprocess.run([sys.executable, str(ROOT / 'build_holder.py'), '--url', 'https://the-10th-floor.github.io/oneforall-menu/'], capture_output=True, text=True)
    assert rejected.returncode == 2 and 'missing quiet zone' in rejected.stderr, rejected.stderr
    files = {
        'laser/L0_backplate_RED_3mm.svg': [143.799, 111.200],
        'laser/L1_frame_RED_3mm.svg': [143.799, 111.200],
        'laser/L2_FACE_single_piece_CREAM_3mm_UVPRINT.svg': [131.499, 98.900],
        'stl/ofa_base.stl': [143.799, 111.200, 7.000],
        'stl/ofa_one_piece_single_colour.stl': [143.799, 111.200, 9.500],
    }
    result = {}
    for name, expected in files.items():
        path = ROOT / name
        actual = svg_bounds(path) if path.suffix == '.svg' else stl_bounds(path)
        assert all(abs(a - b) < .002 for a, b in zip(actual, expected)), f'{name}: geometry changed; review dimensions and handoff'
        result[name] = {'millimetres': [round(v, 3) for v in actual], 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    # A changed physical scale or hidden extra cut shape must not pass this narrow reader.
    original = (ROOT / 'laser/L0_backplate_RED_3mm.svg').read_text()
    with tempfile.TemporaryDirectory() as directory:
        probe = Path(directory) / 'probe.svg'
        for invalid in [re.sub(r'width="[^"]+mm"', 'width="300mm"', original, count=1), original.replace('</svg>', '<rect width="400" height="400"/></svg>')]:
            probe.write_text(invalid)
            try:
                svg_bounds(probe)
            except AssertionError:
                pass
            else:
                raise AssertionError('Invalid scaled/extra geometry was accepted')
    print(json.dumps({'status': 'prototype dimensions verified; not the requested 350 mm sign', 'files': result}, indent=2))
