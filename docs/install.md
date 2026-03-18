# scan2pdf Install Guide

## Requirements

- Python 3.9+
- `pip`

## Install From Source

```bash
git clone <REPOSITORY_URL>
cd image-to-pdf
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install .
```

After installation, run:

```bash
scan2pdf ./scans ./output/book.pdf
```

## Install With Deskew Support

If you want `--deskew`, install the optional OpenCV dependency:

```bash
python -m pip install ".[deskew]"
```

## Install As a Standalone CLI

If you prefer an isolated tool install:

```bash
pipx install .
```
