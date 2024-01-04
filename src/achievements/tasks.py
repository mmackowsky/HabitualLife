import datetime

from celery import Task, shared_task

from habits.models import Habit

from .models import Achievement


class AdmitAchievementsTask(Task):
    name = "achievements_task"

    @shared_task
    def first_habit(self, user):
        if Habit.objects.filter(user=user).count() == 1:
            first_habit_achievement = Achievement.objects.get(name="Hello there.")
            first_habit_achievement.user.add(user)

    @shared_task
    def daily_streak(self, user):
        habits = Habit.objects.filter(user=user)
        for habit in habits:
            if habit.streak_count == 100:
                achievement = Achievement.objects.get(name="Centurion")
                achievement.user.add(user)
            if habit.streak_count == 50:
                achievement = Achievement.objects.get(name="Unstoppable for 50 Days")
                achievement.user.add(user)
            if habit.streak_count == 10:
                achievement = Achievement.objects.get(name="Shot at 10!")
                achievement.user.add(user)

    @shared_task
    def all_habits_for_day_done(self, user):
        habits = Habit.objects.filter(user=user).exclude(
            execution_date=datetime.date.today(), active=True
        )
        if not habits.exists():
            achievement = Achievement.objects.get(name="Disciplined")
            achievement.user.add(user)

    @shared_task
    def skip_habit(self, user):
        habits = Habit.objects.filter(user=user)
        for habit in habits:
            if habit.skipped_count == 1:
                achievement = Achievement.objects.get(name="Sloth")
                achievement.user.add(user)

    @shared_task()
    def fail_habit(self, user):
        habits = Habit.objects.filter(user=user)
        for habit in habits:
            if habit.failed_count == 1:
                achievement = Achievement.objects.get(name="First defeat")
                achievement.user.add(user)
