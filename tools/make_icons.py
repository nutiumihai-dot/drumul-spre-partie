"""Draws the app icon (dusk sky, sun, two peaks, sunrise bands) as PNGs without external libraries."""
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
    top, bottom = (46, 35, 71), (74, 47, 102)
    bands = [(122, 62, 143), (226, 84, 106), (255, 122, 69), (255, 179, 71)]
    sun, snow, peak_far = (255, 179, 71), (251, 248, 244), (92, 74, 120)
    # 100x100 space; shapes stay inside the maskable safe zone
    far_peak = [(8, 70), (36, 40), (56, 58), (92, 70)]
    near_peak = [(24, 70), (56, 26), (88, 70)]
    near_snow = [(46, 40), (56, 26), (66, 40), (61, 37), (56, 42), (51, 37)]
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
                    if y >= 70:
                        c = bands[min(3, int((y - 70) / 7.5))]
                    if (x - 30) ** 2 + (y - 30) ** 2 < 8 ** 2:
                        c = sun
                    if inside(far_peak, x, y):
                        c = peak_far
                    if inside(near_peak, x, y):
                        c = lerp(snow, (226, 214, 236), (y - 26) / 44)
                    if inside(near_snow, x, y):
                        c = (255, 255, 255)
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
