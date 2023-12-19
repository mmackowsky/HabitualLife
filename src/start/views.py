from django.shortcuts import redirect, render
from django.views.generic import FormView, TemplateView

from habits.forms import HabitForm


def main_view(request):
    if request.user.is_authenticated:
        return redirect("habits")
    else:
        return render(request, "start.html")
