from django.urls import path

from .views import (
    CategoryAddView,
    CategoryDeleteView,
    CategoryListView,
    CategoryUpdateView,
    HabitAddView,
    HabitListView,
    HabitUpdateView,
)

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="categories"),
    path("categories/add/", CategoryAddView.as_view(), name="add-category"),
    path(
        "categories/<int:pk>/edit", CategoryUpdateView.as_view(), name="edit-category"
    ),
    path(
        "categories/<int:pk>/delete",
        CategoryDeleteView.as_view(),
        name="delete-category",
    ),
    path("habits/", HabitListView.as_view(), name="habits"),
    path("habits/add/", HabitAddView.as_view(), name="add-habit"),
    path("habits/<int:pk>/edit", HabitUpdateView.as_view(), name="update-habit"),
]
