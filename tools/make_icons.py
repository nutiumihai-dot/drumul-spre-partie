"""Draws the app icon (night sky, orange sun, two peaks with snow caps) as PNGs without external libraries."""
import struct
import sys
import zlib
from pathlib import Path


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def inside(poly, x, y):
    hit = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            hit = not hit
        j = i
    return hit


def draw(size):
    top, bottom = (12, 26, 48), (29, 53, 87)
    sun, far, near, snow = (255, 90, 31), (43, 74, 116), (240, 244, 250), (255, 255, 255)
    # shapes in a 100x100 space; peaks stay inside the maskable safe zone
    far_peak = [(10, 82), (40, 40), (62, 66), (90, 82)]
    near_peak = [(28, 82), (58, 30), (88, 82)]
    near_snow = [(48, 44), (58, 30), (68, 44), (62, 41), (58, 46), (54, 41)]
    far_snow = [(34, 48), (40, 40), (46, 48), (40, 46)]
    rows = []
    ss = 3  # supersampling
    for py in range(size):
        row = bytearray([0])
        for px in range(size):
            acc = [0, 0, 0]
            for sy in range(ss):
                for sx in range(ss):
                    x = (px + (sx + .5) / ss) * 100 / size
                    y = (py + (sy + .5) / ss) * 100 / size
                    c = lerp(top, bottom, y / 100)
                    if (x - 30) ** 2 + (y - 32) ** 2 < 9 ** 2:
                        c = sun
                    if inside(far_peak, x, y):
                        c = far
                    if inside(far_snow, x, y):
                        c = (200, 214, 232)
                    if inside(near_peak, x, y):
                        c = lerp(near, (196, 210, 228), (y - 30) / 52)
                    if inside(near_snow, x, y):
                        c = snow
                    if y > 82:
                        c = sun if 82 < y < 86 and 22 < x < 78 else c
                    for i in range(3):
                        acc[i] += c[i]
            row += bytes(round(v / ss / ss) for v in acc)
        rows.append(bytes(row))
    raw = b"".join(rows)

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


out = Path(sys.argv[1])
for s in (192, 512):
    (out / f"icon-{s}.png").write_bytes(draw(s))
print("ok")
