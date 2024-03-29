from http import HTTPStatus

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import Profile
from .views import ActivateView
from .factories import UserFactory, ProfileFactory


class UsersViewsTest(TestCase):
    def setUp(self):
        self.user = UserFactory(
            username="testuser", email="test@example.com", password="testpassword"
        )
        self.profile = ProfileFactory(user=self.user)

    def test_signup_view(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response = self.client.post(
            reverse("signup"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "newpassword123",
                "password2": "newpassword123",
            },
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(User.objects.count(), 1)

    def test_login_view(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_logout_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_profile_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_reset_password_view(self):
        response = self.client.get(reverse("password-reset"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response = self.client.post(
            reverse("password-reset"), {"email": "test@example.com"}
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_activate_view(self):
        # Create a user to activate
        user = User.objects.create_user(
            username="newuser", email="newuser@example.com", password="newpassword123"
        )

        # Generate an activation token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        response = self.client.get(reverse("activate", args=[uid, token]))
        self.assertEqual(response.status_code, 302)
        user.refresh_from_db()
        self.assertTrue(user.is_active)

    def test_get_user_by_uid(self):
        user = User.objects.create_user(
            username="newuser", email="newuser@example.com", password="newpassword123"
        )

        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Test with valid UID
        result = ActivateView.get_user_by_uid(uidb64=uid)
        self.assertEqual(result, user)

        # Test with invalid UID
        result = ActivateView.get_user_by_uid(uidb64="invalid_uid")
        self.assertIsNone(result)

    def test_reset_password_view_template_used(self):
        response = self.client.get(reverse("password-reset"))
        self.assertTemplateUsed(response, "users/password_reset.html")
