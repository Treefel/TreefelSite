from django.test import TestCase, Client
from django.urls import reverse
from core.models import BlogCategory, BlogPost, GalleryItem


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = BlogCategory.objects.create(name="Dev Log")

    def test_home_returns_200(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)

    def test_home_shows_latest_post(self):
        BlogPost.objects.create(
            title="Latest Post", body="body", category=self.category, published=True
        )
        response = self.client.get(reverse("core:home"))
        self.assertContains(response, "Latest Post")

    def test_home_shows_featured_gallery_item(self):
        GalleryItem.objects.create(
            title="Featured Art", description="desc",
            category="3D", media_type="image",
            image="https://r2.example.com/art.jpg", sort_order=1,
        )
        response = self.client.get(reverse("core:home"))
        self.assertContains(response, "Featured Art")
