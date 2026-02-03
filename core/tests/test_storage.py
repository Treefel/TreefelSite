from unittest.mock import patch, MagicMock
from django.test import TestCase
from io import BytesIO
from PIL import Image
from core.storage import optimize_image


class ImageOptimizationTest(TestCase):
    def _create_test_image(self, width=2000, height=2000, format="PNG"):
        img = Image.new("RGB", (width, height), color="red")
        buffer = BytesIO()
        img.save(buffer, format=format)
        buffer.seek(0)
        return buffer

    def test_optimize_resizes_large_image(self):
        large_image = self._create_test_image(4000, 4000)
        result = optimize_image(large_image, max_dimension=1920)
        img = Image.open(result)
        self.assertLessEqual(max(img.size), 1920)

    def test_optimize_preserves_small_image_dimensions(self):
        small_image = self._create_test_image(800, 600)
        result = optimize_image(small_image, max_dimension=1920)
        img = Image.open(result)
        self.assertEqual(img.size[0], 800)

    def test_optimize_outputs_jpeg(self):
        image = self._create_test_image(1000, 1000, "PNG")
        result = optimize_image(image)
        img = Image.open(result)
        self.assertEqual(img.format, "JPEG")
