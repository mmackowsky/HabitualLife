from django.urls import path

from .views import NotificationUpdateView

urlpatterns = [
    path(
        "notifications_status_update/",
        NotificationUpdateView.as_view(),
        name="notifications_status_update",
    )
]
