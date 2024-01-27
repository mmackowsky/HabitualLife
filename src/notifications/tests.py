from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from users.factories import ProfileFactory, UserFactory

from .factories import NotificationFactory


class NotificationListTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory(username="testuser", password="testpass")
        self.profile = ProfileFactory(user=self.user)
        self.client.login(username="testuser", password="testpass")
        self.notification1 = NotificationFactory(
            message="Notification message 1", user=self.profile
        )
        self.notification2 = NotificationFactory(
            message="Notification message 2", user=self.profile
        )
        self.url = reverse("habits")  # Example of url where Mixin is used
        self.response = self.client.get(self.url)

    def test_notification_template(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response, "notifications/notifications.html")

    def test_achievement_get_context_data(self):
        self.assertIn("habits", self.response.context)
        notifications_in_context = self.response.context["notifications"]
        self.assertEqual(
            list(notifications_in_context), [self.notification2, self.notification1]
        )

    def test_achievement_get_queryset(self):
        self.assertContains(self.response, "Notification message 1")
        self.assertContains(self.response, "Notification message 2")
