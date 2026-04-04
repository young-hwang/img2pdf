#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${REPO_ROOT}"

./gradlew :cli:run --args="./images --output ./output/book.pdf \
  --page-size A5 \
  --dpi 200 \
  --jpeg-quality 65 \
  --deskew \
  --crop \
  --deskew-temp-dir ./.img2pdf-temp \
  --ocr \
  --lang kor+eng"
