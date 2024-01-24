from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from users.factories import ProfileFactory, UserFactory


class MainViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory(username="testuser", password="testpass")
        self.profile = ProfileFactory(user=self.user)

    def test_main_page_if_user_not_logged_in(self):
        response = self.client.get(reverse("main"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "start.html")

    def test_main_page_if_user_logged_in(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("habits"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
