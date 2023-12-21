from colorfield.fields import ColorField
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
        ("WEEKLY", "Weekly"),
        ("MONTHLY", "Monthly"),
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
    is_positive = models.BooleanField()
    execution_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=7, choices=STATUS_CHOICES, default=None, blank=True, null=True
    )
    success_count = models.IntegerField(default=0)
    failed_count = models.IntegerField(default=0)
    skipped_count = models.IntegerField(default=0)

    def increase_success(self):
        self.success_count += 1
        self.save()

    def increase_failed(self):
        self.failed_count += 1
        self.save()

    def increase_skipped(self):
        self.skipped_count += 1
        self.save()

    def reset_counts(self):
        self.success_count = 0
        self.failed_count = 0
        self.skipped_count = 0
        self.save()

    def update_execution_date(self, current_date):
        self.execution_date = current_date
        self.save()
