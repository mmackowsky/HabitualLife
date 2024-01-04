import datetime

from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import Profile


class Category(models.Model):
    DEFAULT_CATEGORIES = [
        ("HEALTH", "Health"),
        ("FINANCE", "Finance"),
        ("WORK", "Work"),
    ]

    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="categories"
    )
    name = models.CharField(max_length=100)
    color = ColorField(default="#d3d3d3")

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("name", "user")


class Habit(models.Model):
    FREQUENCY_CHOICES = [
        ("DAILY", "Daily"),
        ("INTERVAL", "Interval"),
    ]
    STATUS_CHOICES = [
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
        ("SKIPPED", "Skipped"),
    ]

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="habits")
    name = models.CharField(
        max_length=250, help_text="name of the habit to perform", default=None
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="habits"
    )
    active = models.BooleanField(default=True)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default=None)
    interval_value = models.IntegerField(
        default=None,
        blank=True,
        null=True,
        validators=[MinValueValidator(2), MaxValueValidator(30)],
    )
    execution_date = models.DateField(auto_now_add=True)
    is_positive = models.BooleanField()
    status = models.CharField(
        max_length=7, choices=STATUS_CHOICES, default=None, blank=True, null=True
    )
    success_count = models.IntegerField(default=0)
    failed_count = models.IntegerField(default=0)
    skipped_count = models.IntegerField(default=0)
    streak_count = models.IntegerField(default=0)
