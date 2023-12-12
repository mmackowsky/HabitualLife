from django.contrib.auth import views as auth_views
from django.urls import path

from .views import CategoryAddView, HabitAddView

urlpatterns = [
    path("add_category/", CategoryAddView.as_view(), name="add-category"),
    path("add_habit/", HabitAddView.as_view(), name="add-habit"),
]
