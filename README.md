# Image To PDF

Reusable Python CLI for normalizing scanned page images and exporting a single PDF.

## Features

- natural filename ordering
- EXIF-aware rotation handling
- portrait or landscape coarse orientation normalization
- optional OpenCV-based deskew
- optional white-margin trimming after rotation correction
- shared scaling across trimmed pages for stable content size
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

Trim scan margins while keeping a shared content scale across all pages:

```bash
python -m scripts.imaging.scan_to_pdf ./scans ./output/book.pdf \
  --trim-margins \
  --background-threshold 245 \
  --global-scale
```

Disable deskew when OpenCV is unavailable:

```bash
python -m scripts.imaging.scan_to_pdf ./scans ./output/book.pdf --no-deskew
```

## Configuration

Application settings are provided through CLI arguments.

- `input_dir`: Source directory that contains scanned page images. Files are loaded in natural filename order.
- `output_pdf`: Destination path for the generated PDF file.
- `--page-size`: Output canvas preset. Use `A4`, `A5`, or `LETTER` for a fixed paper size, or `ORIGINAL` to keep each page at its processed image size.
- `--dpi`: DPI used when converting paper-size presets into pixel dimensions. Higher values create larger output pages and usually increase PDF size.
- `--orientation`: Coarse page orientation target. Use `portrait` or `landscape` to normalize all pages to one direction, or `preserve` to keep the source orientation.
- `--grayscale`: Converts output pages to grayscale before writing the PDF. This is useful for reducing size on text-heavy scans.
- `--deskew` and `--no-deskew`: Enables or disables OpenCV-based skew correction for slightly rotated text lines.
- `--trim-margins`: Removes outer white scan margins after EXIF correction, coarse rotation, and deskew.
- `--background-threshold`: Threshold used when detecting white background for margin trimming. Lower values are more conservative; higher values remove more light background areas.
- `--global-scale` and `--no-global-scale`: When trimming margins, keeps one shared scale factor across all pages so the visible content stays at a consistent size.
- `--save-normalized-dir`: Optional directory where normalized page images are written for inspection before or alongside the PDF result.

Recommended starting point for scanned documents:

```bash
python -m scripts.imaging.scan_to_pdf ./scans ./output/book.pdf \
  --page-size A4 \
  --dpi 300 \
  --orientation portrait \
  --trim-margins \
  --background-threshold 245 \
  --global-scale
```

## Tests

```bash
python -m unittest discover -s tests
```
