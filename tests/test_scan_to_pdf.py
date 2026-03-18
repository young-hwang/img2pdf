from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.imaging.core import (
    CanvasSize,
    fit_with_padding,
    iter_image_files,
    natural_sort_key,
    normalize_skew_angle,
    page_size_to_pixels,
    should_rotate_for_orientation,
)


class NaturalSortTests(unittest.TestCase):
    def test_natural_sort_key_orders_numeric_suffixes(self) -> None:
        values = ["page10.png", "page2.png", "page1.png"]
        self.assertEqual(sorted(values, key=natural_sort_key), ["page1.png", "page2.png", "page10.png"])

    def test_iter_image_files_filters_and_sorts_supported_files(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ["page10.jpg", "page2.jpg", "notes.txt", "page1.png"]:
                (root / name).write_bytes(b"sample")

            ordered = [path.name for path in iter_image_files(root)]
            self.assertEqual(ordered, ["page1.png", "page2.jpg", "page10.jpg"])


class GeometryTests(unittest.TestCase):
    def test_normalize_skew_angle_flattens_min_area_rect_values(self) -> None:
        self.assertAlmostEqual(normalize_skew_angle(-88.0), 2.0)
        self.assertAlmostEqual(normalize_skew_angle(87.0), -3.0)
        self.assertAlmostEqual(normalize_skew_angle(-7.5), -7.5)

    def test_orientation_rotation_rule(self) -> None:
        self.assertTrue(should_rotate_for_orientation(1600, 1200, "portrait"))
        self.assertTrue(should_rotate_for_orientation(1200, 1600, "landscape"))
        self.assertFalse(should_rotate_for_orientation(1200, 1600, "portrait"))
        self.assertFalse(should_rotate_for_orientation(1200, 1200, "portrait"))
        self.assertFalse(should_rotate_for_orientation(1600, 1200, "preserve"))

    def test_fit_with_padding_preserves_aspect_ratio(self) -> None:
        fitted = fit_with_padding((3000, 2000), CanvasSize(width=1000, height=1000))
        self.assertEqual(fitted, (1000, 667))

    def test_page_size_to_pixels_respects_orientation(self) -> None:
        portrait = page_size_to_pixels("A4", dpi=300, orientation="portrait")
        landscape = page_size_to_pixels("A4", dpi=300, orientation="landscape")

        self.assertEqual(portrait, CanvasSize(width=2481, height=3507))
        self.assertEqual(landscape, CanvasSize(width=3507, height=2481))

    def test_original_page_size_returns_none(self) -> None:
        self.assertIsNone(page_size_to_pixels("ORIGINAL", dpi=300, orientation="portrait"))


if __name__ == "__main__":
    unittest.main()
