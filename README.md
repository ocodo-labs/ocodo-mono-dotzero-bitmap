# Ocodo Mono DotZero Bitmap

Generate a Linux PSF2 bitmap console font from: `OcodoMonoDotZeroNerdFont-Light.ttf`

Initial target:

- framebuffer: 3840×2160
- rasterizer: FreeType
- output: PSF2

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

Use in tty 1 -> 6, use:

```
sudo systemctl edit getty@tty1.service
```

Add this and save.

```
[Service]
ExecStartPre=/usr/bin/setfont /usr/share/kbd/consolefonts/ocodo-mono-dotzero-23x42.psfu
```
We'll then link the override to all the ttys

```
for n in {2..6}; do
  sudo mkdir -p /etc/systemd/system/getty@tty${n}.service.d/
  sudo ln -sf /etc/systemd/system/getty@tty1.service.d/override.conf \
              /etc/systemd/system/getty@tty${n}.service.d/override.conf
done
```
