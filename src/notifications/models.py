from django.db import models

from users.models import Profile


class Notification(models.Model):
    STATUS_CHOICES = (("SEEN", "Seen"), ("UNSEEN", "Unseen"))

    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.CharField(max_length=250)
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default="UNSEEN")
    create_date = models.DateTimeField(auto_now_add=True)
