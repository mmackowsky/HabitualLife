from django.urls import path

from .views import HabitStatisticsView

urlpatterns = [
    path("stats/", HabitStatisticsView.as_view(), name="stats"),
]
