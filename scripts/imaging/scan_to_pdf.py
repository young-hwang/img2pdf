from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path
from typing import Sequence

from .core import (
    SUPPORTED_EXTENSIONS,
    CanvasSize,
    fit_with_padding,
    iter_image_files,
    normalize_skew_angle,
    page_size_to_pixels,
    should_rotate_for_orientation,
)


def require_pillow():
    try:
        from PIL import Image, ImageOps
    except ImportError as exc:  # pragma: no cover - exercised in runtime only
        raise RuntimeError(
            "Pillow is required. Install it with: pip install Pillow"
        ) from exc
    return Image, ImageOps

def require_cv2():
    try:
        import cv2  # type: ignore
    except ImportError as exc:  # pragma: no cover - exercised in runtime only
        raise RuntimeError(
            "Deskew requested but OpenCV is not installed. Install it with: "
            "pip install opencv-python"
        ) from exc
    return cv2


def detect_skew_angle(image: Image.Image, max_angle: float = 10.0) -> float | None:
    cv2 = require_cv2()
    import numpy as np  # type: ignore

    grayscale = np.array(image.convert("L"))
    _, binary = cv2.threshold(
        grayscale, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )
    coords = cv2.findNonZero(binary)
    if coords is None or len(coords) < 200:
        return None

    angle = cv2.minAreaRect(coords)[-1]
    angle = normalize_skew_angle(float(angle))
    if math.isnan(angle) or abs(angle) > max_angle:
        return None
    return angle


def deskew_image(image: Image.Image, max_angle: float = 10.0) -> Image.Image:
    Image, _ = require_pillow()
    angle = detect_skew_angle(image, max_angle=max_angle)
    if angle is None or abs(angle) < 0.1:
        return image
    return image.rotate(
        angle,
        resample=Image.Resampling.BICUBIC,
        expand=True,
        fillcolor="white",
    )


def normalize_page(
    image: Image.Image,
    *,
    page_size: str,
    dpi: int,
    orientation: str,
    grayscale: bool,
    deskew: bool,
) -> Image.Image:
    Image, ImageOps = require_pillow()
    normalized = ImageOps.exif_transpose(image)

    if should_rotate_for_orientation(
        normalized.width, normalized.height, orientation
    ):
        normalized = normalized.rotate(
            90, expand=True, resample=Image.Resampling.BICUBIC, fillcolor="white"
        )

    if deskew:
        normalized = deskew_image(normalized)

    if grayscale:
        normalized = normalized.convert("L")
    else:
        normalized = normalized.convert("RGB")

    canvas_size = page_size_to_pixels(page_size, dpi, orientation)
    if canvas_size is None:
        return normalized

    resized_size = fit_with_padding(normalized.size, canvas_size)
    resized = normalized.resize(resized_size, Image.Resampling.LANCZOS)

    background_color = 255 if resized.mode == "L" else (255, 255, 255)
    canvas = Image.new(resized.mode, (canvas_size.width, canvas_size.height), background_color)
    offset = (
        (canvas_size.width - resized.width) // 2,
        (canvas_size.height - resized.height) // 2,
    )
    canvas.paste(resized, offset)
    return canvas


def save_pdf(images: Sequence[Image.Image], output_path: Path, dpi: int) -> None:
    if not images:
        raise ValueError("No images were provided for PDF export.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    first, *rest = [image.convert("RGB") for image in images]
    first.save(
        output_path,
        save_all=True,
        append_images=rest,
        resolution=dpi,
    )


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normalize scanned images and export them as a single PDF."
    )
    parser.add_argument("input_dir", type=Path, help="Directory containing scanned images.")
    parser.add_argument("output_pdf", type=Path, help="Destination PDF path.")
    parser.add_argument(
        "--page-size",
        default="A4",
        choices=["A4", "A5", "LETTER", "ORIGINAL"],
        help="Output canvas preset. Defaults to A4.",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="Target DPI used for page-size presets. Defaults to 300.",
    )
    parser.add_argument(
        "--orientation",
        default="portrait",
        choices=["portrait", "landscape", "preserve"],
        help="Coarse page orientation normalization. Defaults to portrait.",
    )
    parser.add_argument(
        "--grayscale",
        action="store_true",
        help="Convert output pages to grayscale before PDF export.",
    )
    parser.add_argument(
        "--deskew",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Enable or disable OpenCV-based text skew correction.",
    )
    parser.add_argument(
        "--save-normalized-dir",
        type=Path,
        help="Optional directory to save normalized pages for inspection.",
    )
    return parser.parse_args(argv)


def validate_args(args: argparse.Namespace) -> None:
    require_pillow()
    if not args.input_dir.exists() or not args.input_dir.is_dir():
        raise SystemExit(f"Input directory does not exist: {args.input_dir}")
    if args.dpi <= 0:
        raise SystemExit("--dpi must be a positive integer.")
    if args.deskew:
        try:
            require_cv2()
        except RuntimeError as exc:
            raise SystemExit(str(exc)) from exc


def process_directory(args: argparse.Namespace) -> list[Image.Image]:
    Image, _ = require_pillow()
    files = iter_image_files(args.input_dir)
    if not files:
        raise SystemExit(
            f"No supported image files were found in {args.input_dir}. "
            f"Supported extensions: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    normalized_pages: list[Image.Image] = []
    save_dir = args.save_normalized_dir
    if save_dir:
        save_dir.mkdir(parents=True, exist_ok=True)

    for index, file_path in enumerate(files, start=1):
        with Image.open(file_path) as image:
            normalized = normalize_page(
                image,
                page_size=args.page_size,
                dpi=args.dpi,
                orientation=args.orientation,
                grayscale=args.grayscale,
                deskew=args.deskew,
            )

        normalized_pages.append(normalized)

        if save_dir:
            suffix = ".png" if normalized.mode == "RGBA" else ".jpg"
            output_name = f"{index:04d}_{file_path.stem}{suffix}"
            normalized.save(save_dir / output_name, quality=95)

    return normalized_pages


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        validate_args(args)
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from exc
    pages = process_directory(args)
    save_pdf(pages, args.output_pdf, dpi=args.dpi)
    return 0


if __name__ == "__main__":
    sys.exit(main())
