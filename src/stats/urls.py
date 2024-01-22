from django.urls import path

from .views import habit_statistics

urlpatterns = [path("statistics/", habit_statistics, name="statistics")]
