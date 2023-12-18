from django.urls import path

from .views import (
    CategoryAddView,
    CategoryDeleteView,
    CategoryListView,
    CategoryUpdateView,
    HabitAddView,
)

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="categories"),
    path("categories/add/", CategoryAddView.as_view(), name="add-category"),
    path("categories/edit/", CategoryUpdateView.as_view(), name="edit-category"),
    path(
        "categories/delete/<int:pk>",
        CategoryDeleteView.as_view(),
        name="delete-category",
    ),
    path("add_habit/", HabitAddView.as_view(), name="add-habit"),
]
