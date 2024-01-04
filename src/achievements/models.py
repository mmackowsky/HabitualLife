from django.db import models

from users.models import Profile


class Achievement(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    user = models.ManyToManyField(Profile)
