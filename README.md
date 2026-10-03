# Ocodo Mono DotZero Bitmap

Linux PSF2 bitmap console font generated from `OcodoMonoDotZeroNerdFont-Light.ttf`.

The font is rasterized with FreeType and converted to PSF2 for use on Linux virtual consoles (TTYs).

The primary target is a 3840×2160 framebuffer, with **48px recommended for use on a 4K TV**.

## Generate

Generate the bitmap font with:

```bash
uv run python -m ocodo_bitmap.generate <height px>
```

For 4K TV use, 48px is recommended:

```bash
uv run python -m ocodo_bitmap.generate 48
```

This generates the bitmap font in `dist/`.

The 48px target produces:

```text
dist/ocodo-mono-dotzero-26x48.psfu
```

The default font cell is 26×48 pixels.

## Install

The project includes `install.sh`, which generates and installs the default 48px font and configures TTY 1 through 6.

Run:

```bash
sudo ./install.sh
```

The installer:

- generates the 48px bitmap font
- installs `ocodo-mono-dotzero-26x48.psfu` to `/usr/share/kbd/consolefonts/`
- configures `getty@tty1.service` to load the font
- applies the same configuration to TTY 2 through 6
- reloads the systemd configuration

## Using the font

After installation, switch to a virtual console with:

- `Ctrl+Alt+F1`
- `Ctrl+Alt+F2`
- `Ctrl+Alt+F3`
- `Ctrl+Alt+F4`
- `Ctrl+Alt+F5`
- `Ctrl+Alt+F6`

The font will be loaded automatically by `getty`.

To apply the font immediately to the current console:

```bash
sudo setfont /usr/share/kbd/consolefonts/ocodo-mono-dotzero-26x48.psfu
```

## Why 48px?

The initial target is a 3840×2160 framebuffer, with the font intended for use on a 4K TV.

A 48px character height provides a large, readable console font at typical TV viewing distances while retaining the fixed-width bitmap character of the original font.

The default font cell is:

```text
26 × 48 pixels
```

## Manual installation

To install an already-generated font without running `install.sh`:

```bash
sudo install -Dm644 \
  dist/ocodo-mono-dotzero-26x48.psfu \
  /usr/share/kbd/consolefonts/ocodo-mono-dotzero-26x48.psfu
```

Then load it manually:

```bash
sudo setfont \
  /usr/share/kbd/consolefonts/ocodo-mono-dotzero-26x48.psfu
```

## Requirements

- Linux
- systemd
- `kbd` / `setfont`
- `uv`
- FreeType

## Development

Generate a bitmap font directly:

```bash
uv run python -m ocodo_bitmap.generate 48
```

Generated fonts are placed in `dist/`.
