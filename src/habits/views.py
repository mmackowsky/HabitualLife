import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.views.generic.edit import CreateView, DeleteView
from .models import Habit, Category
from .forms import HabitForm, CategoryForm


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
