from django.http import JsonResponse
from django.views.generic import UpdateView
from django.views.generic.base import ContextMixin

from .models import Notification


class NotificationsListMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["notifications"] = Notification.objects.filter(
            user=self.request.user.profile
        ).order_by("-create_date")
        context["notifications_number"] = Notification.objects.filter(
            user=self.request.user.profile, status="UNSEEN"
        ).count()
        return context


class NotificationUpdateView(NotificationsListMixin, UpdateView):
    model = Notification

    def get(self, request, *args, **kwargs):
        Notification.objects.filter(status="UNSEEN").update(status="SEEN")
        return JsonResponse({"message": "Status updated successfully"})
