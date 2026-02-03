from django.test import TestCase
from core.models import BlogCategory, BlogPost, GalleryItem, FeedbackMessage, SiteSetting


class BlogCategoryModelTest(TestCase):
    def test_create_category(self):
        cat = BlogCategory.objects.create(name="Dev Log")
        self.assertEqual(cat.name, "Dev Log")
        self.assertEqual(cat.slug, "dev-log")

    def test_str_representation(self):
        cat = BlogCategory.objects.create(name="Personal")
        self.assertEqual(str(cat), "Personal")

    def test_slug_auto_generated(self):
        cat = BlogCategory.objects.create(name="Interesting Finds")
        self.assertEqual(cat.slug, "interesting-finds")


class BlogPostModelTest(TestCase):
    def setUp(self):
        self.category = BlogCategory.objects.create(name="Dev Log")

    def test_create_post(self):
        post = BlogPost.objects.create(
            title="My First Post",
            body="<p>Hello world</p>",
            category=self.category,
        )
        self.assertEqual(post.title, "My First Post")
        self.assertEqual(post.slug, "my-first-post")
        self.assertFalse(post.published)

    def test_str_representation(self):
        post = BlogPost.objects.create(
            title="Test Post", body="body", category=self.category
        )
        self.assertEqual(str(post), "Test Post")

    def test_published_manager(self):
        BlogPost.objects.create(
            title="Draft", body="body", category=self.category, published=False
        )
        BlogPost.objects.create(
            title="Live", body="body", category=self.category, published=True
        )
        self.assertEqual(BlogPost.objects.filter(published=True).count(), 1)

    def test_ordering_by_created_at_desc(self):
        p1 = BlogPost.objects.create(
            title="First", body="body", category=self.category, published=True
        )
        p2 = BlogPost.objects.create(
            title="Second", body="body", category=self.category, published=True
        )
        posts = list(BlogPost.objects.all())
        self.assertEqual(posts[0], p2)


class GalleryItemModelTest(TestCase):
    def test_create_image_item(self):
        item = GalleryItem.objects.create(
            title="Landscape",
            description="A 3D landscape",
            category="3D",
            media_type="image",
            image="https://r2.example.com/landscape.jpg",
            sort_order=1,
        )
        self.assertEqual(item.title, "Landscape")
        self.assertEqual(item.category, "3D")

    def test_create_youtube_item(self):
        item = GalleryItem.objects.create(
            title="Timelapse",
            description="Speed modeling",
            category="3D",
            media_type="youtube",
            youtube_url="https://youtube.com/watch?v=abc123",
            sort_order=2,
        )
        self.assertEqual(item.media_type, "youtube")

    def test_str_representation(self):
        item = GalleryItem.objects.create(
            title="My Art", description="desc", category="2D",
            media_type="image", sort_order=1,
        )
        self.assertEqual(str(item), "My Art")

    def test_ordering_by_sort_order(self):
        i2 = GalleryItem.objects.create(
            title="Second", description="d", category="2D",
            media_type="image", sort_order=2,
        )
        i1 = GalleryItem.objects.create(
            title="First", description="d", category="2D",
            media_type="image", sort_order=1,
        )
        items = list(GalleryItem.objects.all())
        self.assertEqual(items[0], i1)


class FeedbackMessageModelTest(TestCase):
    def test_create_message(self):
        msg = FeedbackMessage.objects.create(
            subject="Hello", body="Nice work!"
        )
        self.assertEqual(msg.subject, "Hello")
        self.assertFalse(msg.is_completed)
        self.assertEqual(msg.email, "")

    def test_create_message_with_email(self):
        msg = FeedbackMessage.objects.create(
            email="test@example.com", subject="Hi", body="Great art"
        )
        self.assertEqual(msg.email, "test@example.com")

    def test_str_representation(self):
        msg = FeedbackMessage.objects.create(subject="Test", body="body")
        self.assertEqual(str(msg), "Test")


class SiteSettingModelTest(TestCase):
    def test_create_setting(self):
        setting = SiteSetting.objects.create(
            key="feedback_welcome", value="Welcome! Leave a message."
        )
        self.assertEqual(setting.key, "feedback_welcome")

    def test_str_representation(self):
        setting = SiteSetting.objects.create(key="test_key", value="val")
        self.assertEqual(str(setting), "test_key")
