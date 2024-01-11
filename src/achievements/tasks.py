import datetime

from celery import shared_task
from celery.utils.log import get_task_logger

from habits.models import Habit
from users.models import Profile

from .models import Achievement

logger = get_task_logger(__name__)


@shared_task
def set_first_habit_achievement(user: Profile) -> str | None:
    if Habit.objects.filter(user=user).count() == 1:
        first_habit_achievement = Achievement.objects.get(name="Hello there")
        first_habit_achievement.user.add(user)
        logger.info("Hello there - admit")
        return "Admitted"


@shared_task
def set_daily_streak_achievement(user: Profile) -> str | None:
    habits = Habit.objects.filter(user=user)
    for habit in habits:
        if habit.streak_count == 100:
            achievement = Achievement.objects.get(name="Centurion")
            achievement.user.add(user)
            logger.info("Centurion - admit")
            return "Admitted"
        if habit.streak_count == 50:
            achievement = Achievement.objects.get(name="Unstoppable for 50 Days")
            achievement.user.add(user)
            logger.info("Unstoppable for 50 Days - admit")
            return "Admitted"
        if habit.streak_count == 10:
            achievement = Achievement.objects.get(name="Shot at 10!")
            achievement.user.add(user)
            logger.info("Shot at 10! - admit")
            return "Admitted"


@shared_task
def set_all_habits_for_day_done_achievement(user: Profile) -> str | None:
    habits = Habit.objects.filter(user=user).exclude(
        execution_date=datetime.date.today(), active=True
    )
    if not habits.exists():
        achievement = Achievement.objects.get(name="Disciplined")
        achievement.user.add(user)
        logger.info("Disciplined - admit")
        return "Admitted"


@shared_task
def set_skip_first_habit_achievement(user: Profile) -> str | None:
    habits = Habit.objects.filter(user=user)
    for habit in habits:
        if habit.skipped_count == 1:
            achievement = Achievement.objects.get(name="Sloth")
            achievement.user.add(user)
            logger.info("Sloth - admit")
            return "Admitted"


@shared_task()
def set_fail_first_habit_achievement(user: Profile) -> str | None:
    habits = Habit.objects.filter(user=user)
    for habit in habits:
        if habit.failed_count == 1:
            achievement = Achievement.objects.get(name="First defeat")
            achievement.user.add(user)
            logger.info("First defeat - admit")
            return "Admitted"
