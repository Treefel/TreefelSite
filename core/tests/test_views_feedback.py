from django.test import TestCase, Client
from django.urls import reverse
from core.models import FeedbackMessage, SiteSetting


class AboutViewTest(TestCase):
    def test_about_returns_200(self):
        response = self.client.get(reverse("core:about"))
        self.assertEqual(response.status_code, 200)


class FeedbackViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        SiteSetting.objects.create(
            key="feedback_welcome", value="Drop a message!"
        )

    def test_feedback_page_returns_200(self):
        response = self.client.get(reverse("core:feedback"))
        self.assertEqual(response.status_code, 200)

    def test_feedback_shows_welcome_message(self):
        response = self.client.get(reverse("core:feedback"))
        self.assertContains(response, "Drop a message!")

    def test_feedback_submit_valid(self):
        response = self.client.post(
            reverse("core:feedback"),
            {"subject": "Hello", "body": "Nice site!", "honeypot": ""},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(FeedbackMessage.objects.count(), 1)
        self.assertContains(response, "Thank you")

    def test_feedback_submit_with_email(self):
        self.client.post(
            reverse("core:feedback"),
            {"email": "user@example.com", "subject": "Hi", "body": "Great", "honeypot": ""},
        )
        msg = FeedbackMessage.objects.first()
        self.assertEqual(msg.email, "user@example.com")

    def test_feedback_honeypot_rejects_bots(self):
        response = self.client.post(
            reverse("core:feedback"),
            {"subject": "Spam", "body": "Buy stuff", "honeypot": "gotcha"},
        )
        self.assertEqual(FeedbackMessage.objects.count(), 0)

    def test_feedback_submit_invalid(self):
        response = self.client.post(
            reverse("core:feedback"),
            {"subject": "", "body": "", "honeypot": ""},
        )
        self.assertEqual(FeedbackMessage.objects.count(), 0)
