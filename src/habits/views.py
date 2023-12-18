import logging
from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import CategoryForm, HabitForm
from .models import Category, Habit


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "habits/categories.html"
    context_object_name = "categories"

    def get_queryset(self) -> QuerySet[Category]:
        queryset = Category.objects.filter(user=self.request.user.profile)
        return queryset


class CategoryAddView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ["name"]
    template_name = "habits/categories.html"
    success_url = reverse_lazy("categories")

    # Add category "folder" for habits.
    def form_valid(self, form: CategoryForm) -> HttpResponseRedirect:
        try:
            form.instance.user = self.request.user.profile
            result = super().form_valid(form)
            messages.success(self.request, "Category added successfully.")
            return result
        except IntegrityError:
            messages.error(self.request, "Category already exists.")
            return HttpResponseRedirect(reverse_lazy("categories"))


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = "habits/delete_category.html"
    success_url = reverse_lazy("categories")

    # Delete added category within all habits.
    def get_queryset(self) -> Any:
        return super().get_queryset().filter(user=self.request.user.profile)

    def form_valid(self, form) -> HttpResponseRedirect:
        messages.success(self.request, "Category deleted successfully!")
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    success_url = reverse_lazy("categories")
    form_class = CategoryForm

    # Provide change name of category functionality
    def form_valid(self, form: CategoryForm) -> HttpResponseRedirect:
        form.instance.user = self.request.user.profile
        return super().form_valid(form)


class HabitListView(LoginRequiredMixin, ListView):
    model = Habit

    # Display habits for exact user.


class HabitAddView(LoginRequiredMixin, CreateView):
    model = Habit
    form_class = HabitForm
    template_name = "habits/add_habit.html"

    success_url = reverse_lazy("add-habit")

    def get_form_kwargs(self):
        kwargs = super(HabitAddView, self).get_form_kwargs()
        kwargs["user"] = self.request.user.profile
        return kwargs

    def form_valid(self, form: HabitForm) -> HttpResponseRedirect:
        messages.success(self.request, "Habit added.")
        return super().form_valid(form)

    def form_invalid(self, form) -> HttpResponseRedirect:
        messages.error(self.request, "Form invalid.")
        logging.error(form.errors)
        return super().form_invalid(form)


class HabitDeleteView(DeleteView):
    model = Habit
    form_class = HabitForm
    success_url = "main/"

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user.profile)

    def form_valid(self, form: HabitForm) -> HttpResponseRedirect:
        self.object.delete()
        messages.success(self.request, "Habit deleted.")
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        logging.error(form.errors)
        super().form_invalid(form)


class HabitUpdateView(LoginRequiredMixin, UpdateView):
    model = Habit
    form_class = HabitForm

    # Provide update option for object of Habit model.
