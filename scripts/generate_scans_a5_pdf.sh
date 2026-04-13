#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${REPO_ROOT}"

./gradlew :cli:installDist

./cli/build/install/img2pdf-cli/bin/img2pdf-cli ./scans \
  --output ./output/scans-a5-dpi200-q75-deskew.pdf \
  --page-size A5 \
  --dpi 200 \
  --image-compression JPEG \
  --jpeg-quality 75 \
  --deskew \
  --crop \
  --crop-to-page-size
