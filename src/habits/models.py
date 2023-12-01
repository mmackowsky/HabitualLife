from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)


class Habit(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
