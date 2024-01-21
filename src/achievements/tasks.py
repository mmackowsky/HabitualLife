import datetime
from typing import Union

from celery import shared_task
from celery.utils.log import get_task_logger

from habits.models import Habit
from notifications.models import Notification
from users.models import Profile

from .models import Achievement

logger = get_task_logger(__name__)


def save_achievement(achievement_name: str, user: Profile, log_text: str) -> None:
    achievement = Achievement.objects.get(name=achievement_name)
    achievement.user.add(user)
    logger.info(log_text)


def send_notification(recipient: Union[Profile, int]) -> None:
    notification_text = "Achievement get!! Congratulations, you can check your achievement in Achievement card."

    if isinstance(recipient, int):
        recipient = Profile.objects.get(pk=recipient)

    Notification.objects.create(user=recipient, message=notification_text)


@shared_task
def set_first_habit_achievement(user: Profile) -> str | None:
    if Habit.objects.filter(user=user).count() == 1:
        save_achievement(
            achievement_name="Hello there", user=user, log_text="Hello there - admit"
        )
        send_notification(recipient=user)
        return "Admitted"


@shared_task
def set_daily_streak_achievement(user: Profile) -> str | None:
    habits = Habit.objects.filter(user=user)
    for habit in habits:
        if habit.streak_count == 100:
            save_achievement(
                achievement_name="Centurion", user=user, log_text="Centurion - admit"
            )
            send_notification(recipient=user)
            return "Admitted"
        if habit.streak_count == 50:
            save_achievement(
                achievement_name="Unstoppable for 50 Days",
                user=user,
                log_text="Unstoppable for 50 Days - admit",
            )
            send_notification(recipient=user)
            return "Admitted"
        if habit.streak_count == 10:
            save_achievement(
                achievement_name="Shot at 10!",
                user=user,
                log_text="Shot at 10! - admit",
            )
            send_notification(recipient=user)
            return "Admitted"


@shared_task
def set_all_habits_for_day_done_achievement(user: Profile) -> str | None:
    habits = Habit.objects.filter(user=user).exclude(
        execution_date=datetime.date.today(), active=True
    )
    if not habits.exists():
        save_achievement(
            achievement_name="Disciplined", user=user, log_text="Disciplined - admit"
        )
        send_notification(recipient=user)
        return "Admitted"


@shared_task
def set_skip_first_habit_achievement(user: Profile) -> str | None:
    habits = Habit.objects.filter(user=user)
    for habit in habits:
        if habit.skipped_count == 1:
            save_achievement(
                achievement_name="Sloth", user=user, log_text="Sloth - admit"
            )
            send_notification(recipient=user)
            return "Admitted"


@shared_task()
def set_fail_first_habit_achievement(user: Profile) -> str | None:
    habits = Habit.objects.filter(user=user)
    for habit in habits:
        if habit.failed_count == 1:
            save_achievement(
                achievement_name="First defeat",
                user=user,
                log_text="First defeat - admit",
            )
            send_notification(recipient=user)
            return "Admitted"
