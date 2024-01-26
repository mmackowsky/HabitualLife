from django.views.generic import ListView

from .models import Achievement


class AchievementListView(ListView):
    model = Achievement
    template_name = "achievements/achievements.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["achievements"] = Achievement.objects.all()
        return context
