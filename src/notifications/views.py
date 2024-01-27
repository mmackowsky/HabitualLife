from typing import Any, Dict

from django.http import JsonResponse
from django.views.generic import UpdateView

from .models import Notification


def notification_list(request) -> Dict[str, Any]:
    if request.user.is_authenticated:
        context = {
            "notifications": Notification.objects.filter(
                user=request.user.profile
            ).order_by("-create_date"),
            "notifications_number": Notification.objects.filter(
                user=request.user.profile, status="UNSEEN"
            ).count(),
        }
        return context
    return {}


class NotificationUpdateView(UpdateView):
    model = Notification

    def get(self, request, *args, **kwargs):
        Notification.objects.filter(status="UNSEEN").update(status="SEEN")
        return JsonResponse({"message": "Status updated successfully"})
