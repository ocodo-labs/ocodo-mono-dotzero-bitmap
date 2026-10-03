#!/usr/bin/env bash
set -euo pipefail

FONT_NAME="ocodo-mono-dotzero"
FONT_SIZE="26x48"
FONT_FILE="${FONT_NAME}-${FONT_SIZE}.psfu"

PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
FONT_SOURCE="${PROJECT_DIR}/dist/${FONT_FILE}"
FONT_DEST="/usr/share/kbd/consolefonts/${FONT_FILE}"

OVERRIDE_DIR="/etc/systemd/system/getty@tty1.service.d"
OVERRIDE_FILE="${OVERRIDE_DIR}/override.conf"

if [[ "${EUID}" -ne 0 ]]; then
    echo "Run this script with sudo:"
    echo "  sudo ./install.sh"
    exit 1
fi

if [[ "$(uname -s)" != "Linux" ]]; then
    echo "This installer requires Linux."
    exit 1
fi

if ! command -v systemctl >/dev/null 2>&1; then
    echo "systemd is required."
    exit 1
fi

if ! command -v uv >/dev/null 2>&1; then
    echo "uv is required to generate the font."
    exit 1
fi

cd "${PROJECT_DIR}"

echo "==> Generating ${FONT_FILE}"
uv run python -m ocodo_bitmap.generate 42

if [[ ! -f "${FONT_SOURCE}" ]]; then
    echo "Generated font not found:"
    echo "  ${FONT_SOURCE}"
    exit 1
fi

echo "==> Installing ${FONT_FILE}"
install -Dm644 \
    "${FONT_SOURCE}" \
    "${FONT_DEST}"

echo "==> Configuring tty1"
mkdir -p "${OVERRIDE_DIR}"

cat > "${OVERRIDE_FILE}" <<EOF
[Service]
ExecStartPre=/usr/bin/setfont ${FONT_DEST}
EOF

echo "==> Applying configuration to tty2-tty6"

for n in {2..6}; do
    TTY_DIR="/etc/systemd/system/getty@tty${n}.service.d"

    mkdir -p "${TTY_DIR}"

    ln -sfn \
        "${OVERRIDE_FILE}" \
        "${TTY_DIR}/override.conf"
done

echo "==> Reloading systemd"
systemctl daemon-reload

echo
echo "Installed ${FONT_FILE} for tty1-tty6."
echo
echo "To apply it immediately to the current console:"
echo "  sudo setfont ${FONT_DEST}"
echo
echo "Done."

