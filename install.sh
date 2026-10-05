#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

source "${PROJECT_DIR}/install.conf"

if [[ -z "${FONT_VERSION:-}" ]]; then
    echo "FONT_VERSION is not set"
    exit 1
fi

FONT_URL="https://cdn.jsdelivr.net/npm/${FONT_PACKAGE}@${FONT_VERSION}/${FONT_FILE}"

FONT_TTF_ABS="${PROJECT_DIR}/${FONT_TTF}"
OUT_DIR_ABS="${PROJECT_DIR}/${OUT_DIR}"

cd "${PROJECT_DIR}"

mkdir -p "$(dirname -- "${FONT_TTF_ABS}")" "${OUT_DIR_ABS}"

if [[ ! -f "${FONT_TTF_ABS}" ]]; then
    echo "==> Downloading ${FONT_URL}"
    curl --fail --silent --show-error --location \
        --output "${FONT_TTF_ABS}" \
        "${FONT_URL}"
fi

if [[ $# -gt 0 ]]; then
    heights=("$@")
else
    read -r -a heights <<< "${HEIGHTS}"
fi

for height in "${heights[@]}"; do
    echo "==> Generating ${FONT_NAME} at ${height}px"
    uv run --with "ocodo-font-bitmap @ git+https://github.com/ocodo-labs/ocodo-font-bitmap@${LIB_VERSION}" \
        ocodo-bitmap "${height}" \
        --font "${FONT_TTF_ABS}" \
        --slug "${FONT_NAME}" \
        --out "${OUT_DIR_ABS}"
done
