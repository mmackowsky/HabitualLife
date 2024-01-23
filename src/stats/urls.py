from django.urls import path

from .views import habit_statistics

urlpatterns = [path("stats/", habit_statistics, name="stats")]
