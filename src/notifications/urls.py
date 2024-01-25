from django.urls import path

from .views import NotificationsUpdateView

urlpatterns = [
    path(
        "notifications_status_update/",
        NotificationsUpdateView.as_view(),
        name="notifications_status_update",
    )
]
