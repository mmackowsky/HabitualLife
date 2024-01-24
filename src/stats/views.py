import plotly.graph_objs as go
from django.db.models import Sum
from django.shortcuts import render
from django.views import View
from plotly.offline import plot

from habits.models import Habit
from notifications.views import NotificationsListMixin


class HabitStatisticsView(View, NotificationsListMixin):
    def get(self, request):
        notification_context = self.get_context_data()

        habits = Habit.objects.filter(user=request.user.profile)

        success_count = habits.aggregate(success_count=Sum("success_count"))[
            "success_count"
        ]
        failed_count = habits.aggregate(failed_count=Sum("failed_count"))[
            "failed_count"
        ]
        skipped_count = habits.aggregate(skipped_count=Sum("skipped_count"))[
            "skipped_count"
        ]

        labels = ["SUCCESS", "FAILED", "SKIPPED"]
        values = [success_count, failed_count, skipped_count]

        # Tworzenie wykresu słupkowego
        trace = go.Bar(x=labels, y=values)
        layout = go.Layout(
            title="Status Statistics",
            xaxis=dict(title="Status"),
            yaxis=dict(title="Count"),
        )
        fig = go.Figure(data=[trace], layout=layout)
        plot_div = plot(fig, output_type="div")

        context = {"plot_div": plot_div}
        context.update(notification_context)

        return render(request, "stats/stats.html", context)
