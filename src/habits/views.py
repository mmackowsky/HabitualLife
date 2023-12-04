import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Habit, Category
from .forms import HabitForm, CategoryForm


class CategoryAddView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ["name"]

    # Add category "folder" for habits.
    def form_valid(self, form):
        form.instance.user = self.request.user.profile
        return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    form_class = CategoryForm

    # Delete added category within all habits.


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm

    # Provide change name of category functionality
    def form_valid(self, form):
        form.instance.user = self.request.user.profile
        return super().form_valid(form)


class HabitListView(LoginRequiredMixin, ListView):
    model = Habit

    # Display habits for exact user.


class HabitAddView(LoginRequiredMixin, CreateView):
    model = Habit
    form_class = HabitForm

    def form_valid(self, form):
        category_name = self.kwargs["category_name"]
        form.instance.user = self.request.user.profile
        category = Category.objects.get(name=category_name)
        form.instance.category = category

        messages.success(self.request, "Habit added.")
        return super().form_valid(form)

    def form_invalid(self, form):
        logging.error(form.errors)
        super().form_invalid(form)


class HabitDeleteView(DeleteView):
    model = Habit
    form_class = HabitForm
    success_url = 'main/'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user.profile)

    def form_valid(self, form):
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
