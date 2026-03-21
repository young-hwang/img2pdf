#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${REPO_ROOT}"

python3 -m scan2pdf ./scans ./output/book.pdf \
  --trim-margins \
  --background-threshold 245 \
  --page-size B5 \
  --dpi 200 \
  --jpeg-quality 65 \
  --save-normalized-dir ./output/normalized \
  --ocr \
  --ocr-lang kor+eng
