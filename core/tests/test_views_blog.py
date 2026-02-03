from django.test import TestCase, Client
from django.urls import reverse
from core.models import BlogCategory, BlogPost


class BlogListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = BlogCategory.objects.create(name="Dev Log")
        self.published_post = BlogPost.objects.create(
            title="Published Post",
            body="<p>Content</p>",
            category=self.category,
            published=True,
        )
        self.draft_post = BlogPost.objects.create(
            title="Draft Post",
            body="<p>Draft</p>",
            category=self.category,
            published=False,
        )

    def test_blog_list_returns_200(self):
        response = self.client.get(reverse("core:blog_list"))
        self.assertEqual(response.status_code, 200)

    def test_blog_list_shows_published_only(self):
        response = self.client.get(reverse("core:blog_list"))
        self.assertContains(response, "Published Post")
        self.assertNotContains(response, "Draft Post")

    def test_blog_list_filter_by_category(self):
        other_cat = BlogCategory.objects.create(name="Personal")
        BlogPost.objects.create(
            title="Other Post", body="body", category=other_cat, published=True
        )
        response = self.client.get(
            reverse("core:blog_list") + f"?category={self.category.slug}"
        )
        self.assertContains(response, "Published Post")
        self.assertNotContains(response, "Other Post")

    def test_blog_list_htmx_returns_partial(self):
        response = self.client.get(
            reverse("core:blog_list"),
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "<!DOCTYPE html>")


class BlogDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = BlogCategory.objects.create(name="Dev Log")
        self.post = BlogPost.objects.create(
            title="Test Post",
            body="<p>Full content here</p>",
            category=self.category,
            published=True,
            tags="django,web",
        )

    def test_blog_detail_returns_200(self):
        response = self.client.get(
            reverse("core:blog_detail", kwargs={"slug": self.post.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_blog_detail_shows_content(self):
        response = self.client.get(
            reverse("core:blog_detail", kwargs={"slug": self.post.slug})
        )
        self.assertContains(response, "Test Post")
        self.assertContains(response, "Full content here")

    def test_unpublished_post_returns_404(self):
        draft = BlogPost.objects.create(
            title="Draft", body="body", category=self.category, published=False
        )
        response = self.client.get(
            reverse("core:blog_detail", kwargs={"slug": draft.slug})
        )
        self.assertEqual(response.status_code, 404)
