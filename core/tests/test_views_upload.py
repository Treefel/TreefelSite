from unittest.mock import patch
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO


class TinyMCEUploadTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="treefel", password="testpass123")

    def _create_test_image(self):
        img = Image.new("RGB", (100, 100), color="red")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return SimpleUploadedFile("test.png", buffer.read(), content_type="image/png")

    def test_upload_requires_login(self):
        response = self.client.post(reverse("core:tinymce_upload"))
        self.assertEqual(response.status_code, 302)

    @patch("core.views.upload_image")
    def test_upload_returns_url(self, mock_upload):
        mock_upload.return_value = "https://r2.example.com/blog/abc123.jpg"
        self.client.login(username="treefel", password="testpass123")
        image = self._create_test_image()
        response = self.client.post(
            reverse("core:tinymce_upload"),
            {"file": image},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("location", data)
