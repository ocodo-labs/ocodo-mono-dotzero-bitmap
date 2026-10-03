from pathlib import Path

import freetype


def fixed_width(
    font=Path.home() / ".local/share/fonts/OcodoMonoDotZero-Light.ttf",
    height=32,
):
    face = freetype.Face(str(font))
    face.set_pixel_sizes(0, height)
    face.load_char(
        "A",
        freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_MONO,
    )
    return face.glyph.advance.x / 64
