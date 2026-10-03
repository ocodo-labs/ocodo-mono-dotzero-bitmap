# Ocodo Mono DotZero Bitmap

Generate a Linux PSF2 bitmap console font from: `OcodoMonoDotZeroNerdFont-Light.ttf`

Initial target:

- framebuffer: 3840×2160
- rasterizer: FreeType
- output: PSF2
- glyphs: full Unicode coverage from source font

```
uv run python -m ocodo_bitmap.generate <height px>
```

Generates the bitmap font in dist.

# Install bitmap fonts

From the project folder after generate e.g. height 42 will generate 23x42:

```
sudo install -Dm644 \
  dist/ocodo-mono-dotzero-23x42.psfu \
  /usr/share/kbd/consolefonts/ocodo-mono-dotzero-23x42.psfu

```

Setting for use in `/etc/vconsole.conf`

```
FONT=ocodo-mono-dotzero-23x42.psfu
```
