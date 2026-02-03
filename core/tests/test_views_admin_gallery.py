from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import GalleryItem
import json


class AdminGalleryViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="treefel", password="testpass123")

    def test_admin_gallery_requires_login(self):
        response = self.client.get(reverse("core:admin_gallery"))
        self.assertEqual(response.status_code, 302)

    def test_admin_gallery_returns_200(self):
        self.client.login(username="treefel", password="testpass123")
        response = self.client.get(reverse("core:admin_gallery"))
        self.assertEqual(response.status_code, 200)

    def test_create_gallery_item(self):
        self.client.login(username="treefel", password="testpass123")
        self.client.post(reverse("core:admin_gallery_create"), {
            "title": "New Art",
            "description": "Description",
            "category": "2D",
            "media_type": "image",
            "image": "https://r2.example.com/art.jpg",
            "sort_order": 1,
        })
        self.assertEqual(GalleryItem.objects.count(), 1)

    def test_edit_gallery_item(self):
        self.client.login(username="treefel", password="testpass123")
        item = GalleryItem.objects.create(
            title="Old", description="d", category="2D",
            media_type="image", sort_order=1,
        )
        self.client.post(reverse("core:admin_gallery_edit", kwargs={"pk": item.pk}), {
            "title": "Updated",
            "description": "new desc",
            "category": "3D",
            "media_type": "image",
            "image": "",
            "sort_order": 1,
        })
        item.refresh_from_db()
        self.assertEqual(item.title, "Updated")
        self.assertEqual(item.category, "3D")

    def test_delete_gallery_item(self):
        self.client.login(username="treefel", password="testpass123")
        item = GalleryItem.objects.create(
            title="Delete", description="d", category="2D",
            media_type="image", sort_order=1,
        )
        self.client.post(reverse("core:admin_gallery_delete", kwargs={"pk": item.pk}))
        self.assertEqual(GalleryItem.objects.count(), 0)

    def test_reorder_gallery_items(self):
        self.client.login(username="treefel", password="testpass123")
        i1 = GalleryItem.objects.create(
            title="A", description="d", category="2D",
            media_type="image", sort_order=1,
        )
        i2 = GalleryItem.objects.create(
            title="B", description="d", category="2D",
            media_type="image", sort_order=2,
        )
        self.client.post(
            reverse("core:admin_gallery_reorder"),
            data=json.dumps({"order": [i2.pk, i1.pk]}),
            content_type="application/json",
        )
        i1.refresh_from_db()
        i2.refresh_from_db()
        self.assertEqual(i2.sort_order, 0)
        self.assertEqual(i1.sort_order, 1)
