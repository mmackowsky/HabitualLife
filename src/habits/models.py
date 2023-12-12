from django.contrib.auth.models import User
from django.db import models

from users.models import Profile


class Category(models.Model):
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="categories"
    )
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ["user", "name"]


class Habit(models.Model):
    FREQUENCY_CHOICES = [
        ("DAILY", "Daily"),
        ("WEEKLY", "Weekly"),
        ("MONTHLY", "Monthly"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits")
    name = models.CharField(
        max_length=250, help_text="name of the habit to perform", default=None
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="habits"
    )
    active = models.BooleanField(default=False)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default=None)
    is_positive = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)
