import logging
from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import (
    CreateView,
    DeleteView,
    FormMixin,
    FormView,
    UpdateView,
)

from .forms import CategoryForm, HabitForm
from .models import Category, Habit


class AddHabitMixin(FormMixin):
    model = Habit
    form_class = HabitForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user.profile
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["frequencies"] = Habit.FREQUENCY_CHOICES
        return context


class CategoryListView(LoginRequiredMixin, ListView, AddHabitMixin):
    model = Category
    template_name = "habits/categories.html"

    def get_queryset(self) -> QuerySet[Category]:
        queryset = Category.objects.filter(user=self.request.user.profile)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["categories"] = self.get_queryset()
        return context


class CategoryAddView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ["name", "color"]
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
    template_name = "habits/categories.html"
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
    fields = ["name"]
    template_name = "habits/categories.html"

    # Provide change name of category functionality
    def form_valid(self, form: CategoryForm) -> HttpResponseRedirect:
        form.save()
        messages.success(self.request, "Category edited.")
        return super().form_valid(form)


class HabitListView(LoginRequiredMixin, ListView, AddHabitMixin):
    model = Habit
    template_name = "main.html"
    form_class = HabitForm

    # Display habits for exact user.
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user.profile
        return kwargs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["habits"] = Habit.objects.filter(user=self.request.user.profile)
        return context


class HabitAddView(LoginRequiredMixin, CreateView):
    model = Habit
    template_name = "main.html"
    success_url = reverse_lazy("habits")
    form_class = HabitForm

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs["user"] = self.request.user.profile
    #     return kwargs

    def form_valid(self, form: HabitForm) -> HttpResponseRedirect:
        form.instance.user = self.request.user.profile
        messages.success(self.request, "Habit added.")
        return super().form_valid(form)

    def form_invalid(self, form) -> HttpResponseRedirect:
        messages.error(self.request, "Form invalid.")
        logging.error(form.errors)
        return super().form_invalid(form)


class HabitDeleteView(DeleteView):
    model = Habit
    form_class = HabitForm
    success_url = reverse_lazy("habits")

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
    fields = ["status"]
    template_name = "habits/habits_list.html"
    success_url = reverse_lazy("habits")

    # Provide update option for object of Habit model.
    def form_valid(self, form):
        habit = form.save(commit=False)
        new_status = form.cleaned_data.get("status")

        self.increase_status_value(habit=habit, status=new_status)

        habit.status = new_status
        habit.save()
        messages.success(self.request, "Habit updated.")
        return super().form_valid(form)

    @staticmethod
    def increase_status_value(habit: Habit, status: str) -> None:
        status_to_field = {
            "SUCCESS": "success_count",
            "FAILED": "failed_count",
            "SKIPPED": "skipped_count",
        }
        field_name = status_to_field.get(status)

        if field_name:
            setattr(habit, field_name, getattr(habit, field_name) + 1)
