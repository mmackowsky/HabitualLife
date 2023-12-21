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
        "categories/edit/<int:pk>", CategoryUpdateView.as_view(), name="edit-category"
    ),
    path(
        "categories/delete/<int:pk>",
        CategoryDeleteView.as_view(),
        name="delete-category",
    ),
    path("habits/", HabitListView.as_view(), name="habits"),
    path("habits/add/", HabitAddView.as_view(), name="add-habit"),
    path("habits/edit/<int:pk>", HabitUpdateView.as_view(), name="update-habit"),
]
