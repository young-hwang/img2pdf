# scan2pdf

Turn a folder of scanned images into a cleaned, consistently sized PDF.

## Quick Start

Clone the repository, install it, and run the CLI:

```bash
git clone <REPOSITORY_URL>
cd image-to-pdf
python3 -m pip install .
scan2pdf ./scans ./output/book.pdf
```

If you want deskew support, install the optional OpenCV dependency:

```bash
python3 -m pip install ".[deskew]"
```

You can also install the tool in an isolated CLI environment:

```bash
pipx install .
```

## What You Get

- natural filename ordering
- EXIF-aware rotation handling
- portrait or landscape coarse orientation normalization
- optional OpenCV-based deskew
- optional white-margin trimming after rotation correction
- shared scaling across trimmed pages for stable content size
- fixed page-size canvas with centered white padding
- grayscale export option
- deterministic multi-page PDF output

## Basic Usage

```bash
scan2pdf ./scans ./output/book.pdf
```

Input:

- `./scans`: directory containing page images

Output:

- `./output/book.pdf`: generated multi-page PDF

## Common Commands

Basic conversion:

```bash
scan2pdf ./scans ./output/book.pdf
```

Letter-sized grayscale output:

```bash
scan2pdf ./scans ./output/book.pdf \
  --page-size LETTER \
  --dpi 300 \
  --orientation portrait \
  --grayscale
```

Trim white borders and keep a shared scale across pages:

```bash
scan2pdf ./scans ./output/book.pdf \
  --trim-margins \
  --background-threshold 245 \
  --global-scale
```

Save normalized page images for inspection:

```bash
scan2pdf ./scans ./output/book.pdf \
  --save-normalized-dir ./output/normalized
```

## Development

Run tests:

```bash
python3 -m unittest discover -s tests
```

Check the installed CLI version:

```bash
scan2pdf --version
```

## Documentation

- [Install Guide](docs/install.md)
- [Usage Guide](docs/usage.md)
- [Options Reference](docs/options.md)
