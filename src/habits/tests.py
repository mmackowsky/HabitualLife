from http import HTTPStatus

from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from habits.models import Category, Habit
from users.factories import ProfileFactory, UserFactory

from .factories import CategoryFactory, HabitFactory


class CategoryListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory(username="testuser", password="testpassword")
        self.profile = ProfileFactory(user=self.user)
        self.client.login(username="testuser", password="testpassword")
        self.category1 = CategoryFactory(name="Category 1", user=self.user.profile)
        self.category2 = CategoryFactory(name="Category 2", user=self.user.profile)
        self.response = self.client.get(reverse("categories"))

    def test_categories_template(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response, "habits/categories.html")

    def test_category_get_context_data(self):
        self.assertIn("categories", self.response.context)
        categories_in_context = self.response.context["categories"]
        self.assertEqual(list(categories_in_context), [self.category1, self.category2])

    def test_category_get_queryset(self):
        self.assertContains(self.response, "Category 1")
        self.assertContains(self.response, "Category 2")


class CategoryAddViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory(username="testuser", password="testpassword")
        self.profile = ProfileFactory(user=self.user)
        self.client.login(username="testuser", password="testpassword")
        self.category = CategoryFactory(
            name="TestCategory", user=self.user.profile, color="#39FF00"
        )

    def test_category_add_view_success(self):
        data = {"name": "TestCategory", "color": "blue"}
        response = self.client.post(reverse("add-category"), data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(Category.objects.filter(name="TestCategory").exists())


class CategoryDeleteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory(username="testuser", password="testpassword")
        self.profile = ProfileFactory(user=self.user)
        self.client.login(username="testuser", password="testpassword")
        self.category = CategoryFactory(name="TestCategory", user=self.user.profile)
        self.response = self.client.post(
            reverse("delete-category", args=[self.category.id])
        )

    def test_category_delete_view_success(self):
        self.assertEqual(self.response.status_code, HTTPStatus.FOUND)
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())


class CategoryUpdateViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.profile = ProfileFactory(user=self.user)
        self.category = CategoryFactory(user=self.profile)
        self.client.login(username=self.user.username, password="testpassword")
        self.url = reverse("edit-category", kwargs={"pk": self.category.id})

    def test_category_update_view_success(self):
        new_name = "Updated Category"
        new_color = "#000000"
        data = {"name": new_name, "color": new_color}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        updated_category = Category.objects.get(id=self.category.id)
        self.assertEqual(updated_category.name, new_name)
        self.assertEqual(updated_category.color, new_color)

        # Check redirection
        self.assertRedirects(response, reverse("categories"))


class HabitListViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.profile = ProfileFactory(user=self.user)
        self.habit1 = HabitFactory(user=self.profile)
        self.habit2 = HabitFactory(user=self.profile)

        self.client.login(username=self.user.username, password="testpassword")
        self.url = reverse("habits")
        self.response = self.client.get(reverse("habits"))

    def test_habit_list_view(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response, "main.html")

        habits_in_context = self.response.context_data["habits"]
        self.assertEqual(list(habits_in_context), [self.habit1, self.habit2])


class HabitAddViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.profile = ProfileFactory(user=self.user)
        self.client.login(username=self.user.username, password="testpassword")
        self.url = reverse("add-habit")
        self.habit = HabitFactory(user=self.profile)

    def test_habit_add_view_success(self):
        form_data = {
            "name": HabitFactory.name,
            "category": HabitFactory.category,
            "frequency": HabitFactory.frequency,
            "interval_value": HabitFactory.interval_value,
            "is_positive": HabitFactory.is_positive,
            "status": HabitFactory.status,
        }

        response = self.client.post(self.url, form_data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        # self.assertRedirects(response, reverse_lazy('habits'))

        self.assertEqual(Habit.objects.count(), 1)

        self.assertTrue(Habit.objects.filter(user=self.user.profile).exists())

    def test_habit_add_view_form_invalid(self):
        habit_count_before = Habit.objects.count()

        invalid_form_data = {}

        response = self.client.post(self.url, invalid_form_data)

        self.assertEqual(response.status_code, HTTPStatus.OK)

        self.assertEqual(Habit.objects.count(), habit_count_before)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Form invalid.")


class HabitUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.profile = ProfileFactory(user=self.user)
        self.habit = HabitFactory(user=self.profile)
        self.url = reverse("update-habit", kwargs={"pk": self.habit.pk})

    def test_update_habit_success(self):
        self.client.force_login(self.user)

        response = self.client.post(self.url, {"status": "SUCCESS"})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("habits"))
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.status, "SUCCESS")

    def test_update_habit_failure(self):
        self.client.force_login(self.user)

        response = self.client.post(self.url, {"status": "FAILED"})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("habits"))
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.status, "FAILED")

    def test_update_habit_skipped(self):
        self.client.force_login(self.user)

        response = self.client.post(self.url, {"status": "SKIPPED"})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("habits"))
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.status, "SKIPPED")

    def test_update_habit_invalid_status(self):
        self.client.force_login(self.user)

        response = self.client.post(self.url, {"status": "INVALID_STATUS"})

        self.assertEqual(response.status_code, 200)
        self.habit.refresh_from_db()
        self.assertNotEqual(self.habit.status, "INVALID_STATUS")
