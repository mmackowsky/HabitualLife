from django.db import IntegrityError
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Category
from .views import CategoryListView
from users.models import Profile
from http import HTTPStatus


class CategoryListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user)
        self.client.login(username='testuser', password='testpassword')
        self.category1 = Category.objects.create(name='Category 1', user=self.user.profile)
        self.category2 = Category.objects.create(name='Category 2', user=self.user.profile)
        self.response = self.client.get(reverse('categories'))

    def test_categories_template(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response, 'habits/categories.html')

    def test_category_get_context_data(self):
        self.assertIn('categories', self.response.context)
        categories_in_context = self.response.context['categories']
        self.assertEqual(list(categories_in_context), [self.category1, self.category2])

    def test_category_get_queryset(self):
        self.assertContains(self.response, 'Category 1')
        self.assertContains(self.response, 'Category 2')

    def tearDown(self):
        self.client.logout()
        self.user.delete()


class CategoryAddViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user)
        self.client.login(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='TestCategory', user=self.user.profile, color="#39FF00")

    def test_category_add_view_success(self):
        data = {'name': 'TestCategory', 'color': 'blue'}
        response = self.client.post(reverse('add-category'), data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(Category.objects.filter(name='TestCategory').exists())

    def tearDown(self):
        self.client.logout()
        self.user.delete()


class CategoryDeleteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user)
        self.client.login(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='TestCategory', user=self.user.profile)
        self.response = self.client.post(reverse('delete-category', args=[self.category.id]))

    def test_category_delete_view_success(self):
        self.assertEqual(self.response.status_code, HTTPStatus.FOUND)
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())

    def tearDown(self):
        self.client.logout()
        self.user.delete()
