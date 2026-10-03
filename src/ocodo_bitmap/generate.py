from __future__ import annotations

import argparse
import struct
from pathlib import Path

import freetype

from ocodo_bitmap.width import fixed_width


FONT = Path.home() / ".local/share/fonts/OcodoMonoDotZero-Light.ttf"
GLYPH_COUNT = 512


def glyphs(face: freetype.Face):
    charcode, glyph_index = face.get_first_char()

    while glyph_index:
        yield charcode, glyph_index
        charcode, glyph_index = face.get_next_char(
            charcode,
            glyph_index,
        )


def rasterize(
    face: freetype.Face,
    glyph_index: int,
    width: int,
    height: int,
) -> bytes:
    face.load_glyph(
        glyph_index,
        freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_MONO,
    )

    glyph = face.glyph
    bitmap = glyph.bitmap

    bearing_x = glyph.metrics.horiBearingX // 64
    bearing_y = glyph.metrics.horiBearingY // 64
    advance = glyph.advance.x // 64
    baseline = face.size.ascender // 64

    x = (width - advance) // 2 + bearing_x
    y = baseline - bearing_y

    pixels = bytearray(width * height)

    for row in range(bitmap.rows):
        py = y + row

        if not 0 <= py < height:
            continue

        for col in range(bitmap.width):
            px = x + col

            if not 0 <= px < width:
                continue

            source_byte = row * bitmap.pitch + col // 8
            source_bit = 7 - col % 8

            if bitmap.buffer[source_byte] & (1 << source_bit):
                pixels[py * width + px] = 1

    return bytes(pixels)


def psf2(
    bitmaps: list[bytes],
    codepoints: list[int | None],
    width: int,
    height: int,
) -> bytes:
    bytes_per_row = (width + 7) // 8
    bytes_per_glyph = bytes_per_row * height

    header = struct.pack(
        "<8I",
        0x864AB572,
        0,
        32,
        0x01,
        GLYPH_COUNT,
        bytes_per_glyph,
        height,
        width,
    )

    bitmap_data = bytearray()

    for bitmap in bitmaps:
        for y in range(height):
            row = bitmap[y * width:(y + 1) * width]

            for start in range(0, width, 8):
                value = 0

                for bit in range(8):
                    x = start + bit

                    if x >= width:
                        break

                    if row[x]:
                        value |= 1 << (7 - bit)

                bitmap_data.append(value)

    unicode_data = bytearray()

    for codepoint in codepoints:
        if codepoint is not None:
            unicode_data.extend(
                chr(codepoint).encode("utf-8")
            )

        unicode_data.append(0xFF)

    return (
        header
        + bytes(bitmap_data)
        + bytes(unicode_data)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("height", type=int)
    args = parser.parse_args()

    height = args.height
    width = int(fixed_width(height=height))

    output = Path(
        f"dist/ocodo-mono-dotzero-{width}x{height}.psfu"
    )
    output.parent.mkdir(parents=True, exist_ok=True)

    face = freetype.Face(str(FONT))
    face.set_pixel_sizes(0, height)

    mapping = dict(glyphs(face))

    blank = bytes(width * height)

    bitmaps: list[bytes] = []
    codepoints: list[int | None] = []

    for slot in range(GLYPH_COUNT):
        codepoint = slot if slot < 256 else None
        glyph_index = mapping.get(codepoint) if codepoint is not None else None

        if glyph_index is None:
            bitmaps.append(blank)
            codepoints.append(codepoint)
        else:
            bitmaps.append(
                rasterize(
                    face,
                    glyph_index,
                    width,
                    height,
                )
            )
            codepoints.append(codepoint)

    output.write_bytes(
        psf2(
            bitmaps,
            codepoints,
            width,
            height,
        )
    )

    print(f"{width}x{height}")
    print(f"glyphs: {GLYPH_COUNT}")
    print(f"output: {output}")


if __name__ == "__main__":
    main()
