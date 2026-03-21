#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pypdfium2 as pdfium


DEFAULT_INPUT_DIR = Path("temp_pdfs")
DEFAULT_OUTPUT_DIR = Path("output/temp_pdfs_b5_ocr")
DEFAULT_DPI = 200
DEFAULT_TESSERACT_CMD = "/opt/homebrew/bin/tesseract"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rebuild each PDF in temp_pdfs via scan2pdf with OCR."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help="Directory containing source PDFs. Defaults to temp_pdfs.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for rebuilt PDFs. Defaults to output/temp_pdfs_b5_ocr.",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=DEFAULT_DPI,
        help="Render DPI for PDF page extraction. Defaults to 200.",
    )
    parser.add_argument(
        "--tesseract-cmd",
        default=DEFAULT_TESSERACT_CMD,
        help="Tesseract executable path. Defaults to /opt/homebrew/bin/tesseract.",
    )
    return parser.parse_args()


def iter_pdfs(input_dir: Path) -> list[Path]:
    return sorted(path for path in input_dir.iterdir() if path.suffix.lower() == ".pdf")


def render_pdf_to_images(pdf_path: Path, images_dir: Path, dpi: int) -> None:
    pdf = pdfium.PdfDocument(str(pdf_path))
    scale = dpi / 72

    try:
        for index in range(len(pdf)):
            page = pdf[index]
            image = page.render(scale=scale).to_pil()
            output_path = images_dir / f"{index + 1:04d}.png"
            image.save(output_path, dpi=(dpi, dpi))
            image.close()
            page.close()
    finally:
        pdf.close()


def rebuild_pdf(pdf_path: Path, output_dir: Path, dpi: int, tesseract_cmd: str) -> Path:
    output_path = output_dir / pdf_path.name

    with tempfile.TemporaryDirectory(prefix=f"scan2pdf-{pdf_path.stem}-") as tmp:
        images_dir = Path(tmp) / "images"
        images_dir.mkdir(parents=True, exist_ok=True)
        render_pdf_to_images(pdf_path, images_dir, dpi)

        command = [
            sys.executable,
            "-m",
            "scan2pdf",
            str(images_dir),
            str(output_path),
            "--trim-margins",
            "--background-threshold",
            "245",
            "--page-size",
            "B5",
            "--dpi",
            str(dpi),
            "--jpeg-quality",
            "65",
            "--ocr",
            "--ocr-lang",
            "kor+eng",
            "--tesseract-cmd",
            tesseract_cmd,
        ]
        subprocess.run(command, check=True)

    return output_path


def main() -> int:
    args = parse_args()

    if not args.input_dir.exists() or not args.input_dir.is_dir():
        raise SystemExit(f"Input directory does not exist: {args.input_dir}")
    if shutil.which(args.tesseract_cmd) is None and not Path(args.tesseract_cmd).exists():
        raise SystemExit(f"Tesseract not found: {args.tesseract_cmd}")
    if args.dpi <= 0:
        raise SystemExit("--dpi must be a positive integer.")

    pdf_files = iter_pdfs(args.input_dir)
    if not pdf_files:
        raise SystemExit(f"No PDF files found in {args.input_dir}")

    args.output_dir.mkdir(parents=True, exist_ok=True)

    for pdf_path in pdf_files:
        output_path = args.output_dir / pdf_path.name
        if output_path.exists():
            print(f"[skip]  {output_path}", flush=True)
            continue

        print(f"[start] {pdf_path}", flush=True)
        output_path = rebuild_pdf(
            pdf_path=pdf_path,
            output_dir=args.output_dir,
            dpi=args.dpi,
            tesseract_cmd=args.tesseract_cmd,
        )
        print(f"[done]  {output_path}", flush=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
