# Ocodo Mono DotZero Bitmap

Linux PSF2 bitmap console fonts generated from `OcodoMonoDotZero-Light.ttf`.

## Generate

```bash
FONT_VERSION=1.0.2 ./install.sh
```

Generates all heights defined in `install.conf` into `dist/`.

Single height:

```bash
FONT_VERSION=1.0.2 ./install.sh 48
```

## Install

Copy the generated font to your console font directory and load it. This is distro-specific.

Example (systemd + kbd):

```bash
sudo install -Dm644 \
  dist/ocodo-mono-dotzero-26x48.psfu \
  /usr/share/kbd/consolefonts/ocodo-mono-dotzero-26x48.psfu

sudo setfont /usr/share/kbd/consolefonts/ocodo-mono-dotzero-26x48.psfu
```

Making it persistent across reboots is distro-specific. Consult your distribution's documentation.

## Releases

Tagged releases publish the generated `.psfu` files as GitHub release assets.

## Configuration

`install.conf` holds the source package, font file, output directory, library version, and default heights.

## Requirements

- `uv`
- `curl`
- `bash`

## Development

Generation tooling: [ocodo-font-bitmap](https://github.com/ocodo-labs/ocodo-font-bitmap)
