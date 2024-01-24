from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from habits.models import Habit
from users.factories import ProfileFactory, UserFactory
from habits.factories import HabitFactory


class HabitStatisticsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = UserFactory(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.profile = ProfileFactory(user=self.user)
        self.habit = HabitFactory()
        self.url = reverse('stats')
        self.response = self.client.get(self.url)

    def test_get_habit_statistics(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'stats/stats.html')
        self.assertIn('plot_div', self.response.context)

    def test_get_habit_statistics_with_no_habits(self):
        Habit.objects.all().delete()

        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'stats/stats.html')
        self.assertIn('plot_div', self.response.context)

    def test_get_habit_statistics_with_notification(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'stats/stats.html')
        self.assertIn('notifications', self.response.context)
        self.assertIn('notifications_number', self.response.context)
