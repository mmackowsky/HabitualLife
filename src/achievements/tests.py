from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from users.factories import ProfileFactory, UserFactory

from .factories import AchievementFactory


class AchievementsListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory(username="testuser", password="testpassword")
        self.profile = ProfileFactory(user=self.user)
        self.client.login(username="testuser", password="testpassword")

        self.achievement1 = AchievementFactory(name="Achievement 1", user=self.profile)
        self.achievement2 = AchievementFactory(name="Achievement 2", user=self.profile)

        self.url = reverse("achievements")
        self.response = self.client.get(self.url)

    def test_achievement_template(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response, "achievements/achievements.html")

    def test_achievement_get_context_data(self):
        self.assertIn("achievements", self.response.context)
        achievements_in_context = self.response.context["achievements"]
        self.assertEqual(
            list(achievements_in_context), [self.achievement1, self.achievement2]
        )

    def test_achievement_get_queryset(self):
        self.assertContains(self.response, "Achievement 1")
        self.assertContains(self.response, "Achievement 2")
