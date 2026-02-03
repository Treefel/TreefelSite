from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import FeedbackMessage, SiteSetting


class AdminFeedbackViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="treefel", password="testpass123")

    def test_admin_feedback_requires_login(self):
        response = self.client.get(reverse("core:admin_feedback"))
        self.assertEqual(response.status_code, 302)

    def test_admin_feedback_returns_200(self):
        self.client.login(username="treefel", password="testpass123")
        response = self.client.get(reverse("core:admin_feedback"))
        self.assertEqual(response.status_code, 200)

    def test_admin_feedback_shows_messages(self):
        self.client.login(username="treefel", password="testpass123")
        FeedbackMessage.objects.create(subject="Test Msg", body="Hello")
        response = self.client.get(reverse("core:admin_feedback"))
        self.assertContains(response, "Test Msg")

    def test_toggle_feedback_completed(self):
        self.client.login(username="treefel", password="testpass123")
        msg = FeedbackMessage.objects.create(subject="Toggle", body="body")
        self.assertFalse(msg.is_completed)
        self.client.post(reverse("core:admin_feedback_toggle", kwargs={"pk": msg.pk}))
        msg.refresh_from_db()
        self.assertTrue(msg.is_completed)
        self.client.post(reverse("core:admin_feedback_toggle", kwargs={"pk": msg.pk}))
        msg.refresh_from_db()
        self.assertFalse(msg.is_completed)

    def test_filter_completed(self):
        self.client.login(username="treefel", password="testpass123")
        FeedbackMessage.objects.create(subject="Done", body="b", is_completed=True)
        FeedbackMessage.objects.create(subject="New", body="b", is_completed=False)
        response = self.client.get(reverse("core:admin_feedback") + "?filter=completed")
        self.assertContains(response, "Done")
        self.assertNotContains(response, "New")

    def test_filter_new(self):
        self.client.login(username="treefel", password="testpass123")
        FeedbackMessage.objects.create(subject="Done", body="b", is_completed=True)
        FeedbackMessage.objects.create(subject="New", body="b", is_completed=False)
        response = self.client.get(reverse("core:admin_feedback") + "?filter=new")
        self.assertNotContains(response, "Done")
        self.assertContains(response, "New")

    def test_update_welcome_message(self):
        self.client.login(username="treefel", password="testpass123")
        SiteSetting.objects.create(key="feedback_welcome", value="Old message")
        self.client.post(reverse("core:admin_feedback_welcome"), {
            "welcome_message": "New welcome message!",
        })
        setting = SiteSetting.objects.get(key="feedback_welcome")
        self.assertEqual(setting.value, "New welcome message!")
