from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=100)


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits")
    name = models.CharField(max_length=250, help_text="name of the habit to perform")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="habits"
    )
    active = models.BooleanField(default=False)
    is_positive = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)
