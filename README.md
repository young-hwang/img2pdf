# Image To PDF

Reusable Python CLI for normalizing scanned page images and exporting a single PDF.

## Features

- natural filename ordering
- EXIF-aware rotation handling
- portrait or landscape coarse orientation normalization
- optional OpenCV-based deskew
- fixed page-size canvas with centered white padding
- grayscale export option
- deterministic multi-page PDF output

## Requirements

- Python 3.9+
- `Pillow`
- `opencv-python` for deskew support

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install Pillow opencv-python
```

## Usage

```bash
python -m scripts.imaging.scan_to_pdf ./scans ./output/book.pdf
```

Common options:

```bash
python -m scripts.imaging.scan_to_pdf ./scans ./output/book.pdf \
  --page-size LETTER \
  --dpi 300 \
  --orientation portrait \
  --grayscale \
  --deskew \
  --save-normalized-dir ./output/normalized
```

Disable deskew when OpenCV is unavailable:

```bash
python -m scripts.imaging.scan_to_pdf ./scans ./output/book.pdf --no-deskew
```

## Tests

```bash
python -m unittest discover -s tests
```
