from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import ContextMixin

from .models import Notification


class NotificationsListMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["notifications"] = Notification.objects.filter(
            user=self.request.user.profile
        )
        return context


class NotificationsListView(NotificationsListMixin, ListView):
    model = Notification
    template_name = "notifications/notifications.html"
