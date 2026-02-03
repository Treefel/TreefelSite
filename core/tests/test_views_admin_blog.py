from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import BlogCategory, BlogPost


class AdminBlogViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="treefel", password="testpass123")
        self.category = BlogCategory.objects.create(name="Dev Log")

    def test_admin_blog_requires_login(self):
        response = self.client.get(reverse("core:admin_blog"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_admin_blog_returns_200_when_logged_in(self):
        self.client.login(username="treefel", password="testpass123")
        response = self.client.get(reverse("core:admin_blog"))
        self.assertEqual(response.status_code, 200)

    def test_create_blog_post(self):
        self.client.login(username="treefel", password="testpass123")
        response = self.client.post(reverse("core:admin_blog_create"), {
            "title": "New Post",
            "body": "<p>Content</p>",
            "category": self.category.pk,
            "tags": "test,blog",
            "published": True,
        })
        self.assertEqual(BlogPost.objects.count(), 1)
        post = BlogPost.objects.first()
        self.assertEqual(post.title, "New Post")

    def test_edit_blog_post(self):
        self.client.login(username="treefel", password="testpass123")
        post = BlogPost.objects.create(
            title="Old Title", body="body", category=self.category
        )
        self.client.post(reverse("core:admin_blog_edit", kwargs={"pk": post.pk}), {
            "title": "Updated Title",
            "body": "<p>Updated</p>",
            "category": self.category.pk,
            "tags": "",
            "published": False,
        })
        post.refresh_from_db()
        self.assertEqual(post.title, "Updated Title")

    def test_delete_blog_post(self):
        self.client.login(username="treefel", password="testpass123")
        post = BlogPost.objects.create(
            title="Delete Me", body="body", category=self.category
        )
        self.client.post(reverse("core:admin_blog_delete", kwargs={"pk": post.pk}))
        self.assertEqual(BlogPost.objects.count(), 0)


class AdminBlogCategoryTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="treefel", password="testpass123")
        self.client.login(username="treefel", password="testpass123")

    def test_create_category(self):
        self.client.post(reverse("core:admin_blog_category_create"), {
            "name": "New Category",
        })
        self.assertEqual(BlogCategory.objects.filter(name="New Category").count(), 1)

    def test_delete_category(self):
        cat = BlogCategory.objects.create(name="To Delete")
        self.client.post(reverse("core:admin_blog_category_delete", kwargs={"pk": cat.pk}))
        self.assertEqual(BlogCategory.objects.filter(name="To Delete").count(), 0)
