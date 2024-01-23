from django.views.generic.base import ContextMixin

from .models import Notification


class NotificationsListMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["notifications"] = Notification.objects.filter(
            user=self.request.user.profile
        )
        context["notifications_number"] = Notification.objects.filter(
            user=self.request.user.profile
        ).count()
        return context
