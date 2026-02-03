from django.test import TestCase, Client
from django.urls import reverse
from core.models import GalleryItem


class GalleryViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.item_2d = GalleryItem.objects.create(
            title="Painting", description="A 2D painting",
            category="2D", media_type="image",
            image="https://r2.example.com/painting.jpg", sort_order=1,
        )
        self.item_3d = GalleryItem.objects.create(
            title="Sculpture", description="A 3D model",
            category="3D", media_type="image",
            image="https://r2.example.com/sculpture.jpg", sort_order=2,
        )
        self.item_yt = GalleryItem.objects.create(
            title="Timelapse", description="Speed sculpt",
            category="3D", media_type="youtube",
            youtube_url="https://www.youtube.com/watch?v=abc123", sort_order=3,
        )

    def test_gallery_returns_200(self):
        response = self.client.get(reverse("core:gallery"))
        self.assertEqual(response.status_code, 200)

    def test_gallery_shows_all_items(self):
        response = self.client.get(reverse("core:gallery"))
        self.assertContains(response, "Painting")
        self.assertContains(response, "Sculpture")
        self.assertContains(response, "Timelapse")

    def test_gallery_filter_2d(self):
        response = self.client.get(reverse("core:gallery") + "?category=2D")
        self.assertContains(response, "Painting")
        self.assertNotContains(response, "Sculpture")

    def test_gallery_filter_3d(self):
        response = self.client.get(reverse("core:gallery") + "?category=3D")
        self.assertNotContains(response, "Painting")
        self.assertContains(response, "Sculpture")

    def test_gallery_htmx_returns_partial(self):
        response = self.client.get(
            reverse("core:gallery"), HTTP_HX_REQUEST="true",
        )
        self.assertNotContains(response, "<!DOCTYPE html>")
