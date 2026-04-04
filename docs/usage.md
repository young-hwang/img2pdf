# img2pdf Usage Guide

## Overview

`img2pdf` is a Java CLI for turning image files or directories into a PDF.
It can optionally deskew scans, crop empty margins, and run Tesseract OCR.

## Install

See [Install Guide](install.md).

## Basic Usage

```bash
./cli/build/install/cli/bin/img2pdf-cli ./images --output ./output/book.pdf
```

By default this produces an image-only PDF.

## OCR

```bash
./cli/build/install/cli/bin/img2pdf-cli ./images \
  --output ./output/book.pdf \
  --ocr \
  --lang kor+eng
```

If your trained data is stored outside the default location:

```bash
./cli/build/install/cli/bin/img2pdf-cli ./images \
  --output ./output/book.pdf \
  --ocr \
  --lang kor+eng \
  --tessdata /opt/homebrew/share/tessdata
```

Write recognized text to a file as well:

```bash
./cli/build/install/cli/bin/img2pdf-cli ./images \
  --output ./output/book.pdf \
  --ocr \
  --ocr-text-out ./output/book.txt
```

## Deskew and Crop

```bash
./cli/build/install/cli/bin/img2pdf-cli ./images \
  --output ./output/book.pdf \
  --deskew \
  --crop
```

Use a stable temporary directory for intermediate deskew files:

```bash
./cli/build/install/cli/bin/img2pdf-cli ./images \
  --output ./output/book.pdf \
  --deskew \
  --deskew-temp-dir ./.img2pdf-temp
```

## Page Sizing

Keep each source image at its processed size:

```bash
./cli/build/install/cli/bin/img2pdf-cli ./images \
  --output ./output/book.pdf \
  --page-size ORIGINAL
```

Render onto a fixed paper size:

```bash
./cli/build/install/cli/bin/img2pdf-cli ./images \
  --output ./output/book.pdf \
  --page-size LETTER \
  --dpi 300
```

Disable aspect-ratio preservation if you explicitly want stretch-to-page behavior:

```bash
./cli/build/install/cli/bin/img2pdf-cli ./images \
  --output ./output/book.pdf \
  --page-size A4 \
  --stretch
```

## PDF Image Compression

JPEG with lower quality for smaller files:

```bash
./cli/build/install/cli/bin/img2pdf-cli ./images \
  --output ./output/book.pdf \
  --image-compression JPEG \
  --jpeg-quality 60
```

Lossless embedding:

```bash
./cli/build/install/cli/bin/img2pdf-cli ./images \
  --output ./output/book.pdf \
  --image-compression LOSSLESS
```

## Configuration

See [Options Reference](options.md).

## Tests

```bash
./gradlew test
```
