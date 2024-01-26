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


def send_achievement_notification(
    recipient: Union[Profile, int], achievement_name: str
) -> None:
    notification_text = f'Achievement "{achievement_name}" get!!'

    if isinstance(recipient, int):
        recipient = Profile.objects.get(pk=recipient)

    Notification.objects.create(user=recipient, message=notification_text)


@shared_task
def set_first_habit_achievement(user: Profile) -> str | None:
    if Habit.objects.filter(user=user).count() == 1:
        save_achievement(
            achievement_name="Hello there", user=user, log_text="Hello there - admit"
        )
        send_achievement_notification(recipient=user, achievement_name="Hello there")
        return "Admitted"


@shared_task
def set_daily_streak_achievement(user: Profile) -> str | None:
    habits = Habit.objects.filter(user=user)
    for habit in habits:
        if habit.streak_count == 100:
            save_achievement(
                achievement_name="Centurion", user=user, log_text="Centurion - admit"
            )
            send_achievement_notification(recipient=user, achievement_name="Centurion")
            return "Admitted"
        if habit.streak_count == 50:
            save_achievement(
                achievement_name="Unstoppable for 50 Days",
                user=user,
                log_text="Unstoppable for 50 Days - admit",
            )
            send_achievement_notification(
                recipient=user, achievement_name="Unstoppable for 50 days"
            )
            return "Admitted"
        if habit.streak_count == 10:
            save_achievement(
                achievement_name="Shot at 10!",
                user=user,
                log_text="Shot at 10! - admit",
            )
            send_achievement_notification(
                recipient=user, achievement_name="Shot at 10!"
            )
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
        send_achievement_notification(recipient=user, achievement_name="Disciplined")
        return "Admitted"


@shared_task
def set_skip_first_habit_achievement(user: Profile) -> str | None:
    habits = Habit.objects.filter(user=user)
    if Achievement.objects.filter(user=user, name="Sloth").exists():
        return "Already awarded"
    for habit in habits:
        if habit.skipped_count == 1:
            save_achievement(
                achievement_name="Sloth", user=user, log_text="Sloth - admit"
            )
            send_achievement_notification(recipient=user, achievement_name="Sloth")
            return "Admitted"


@shared_task()
def set_fail_first_habit_achievement(user: Profile) -> str | None:
    habits = Habit.objects.filter(user=user)
    if Achievement.objects.filter(user=user, name="First defeat").exists():
        return "Already awarded"
    for habit in habits:
        if habit.failed_count == 1:
            save_achievement(
                achievement_name="First defeat",
                user=user,
                log_text="First defeat - admit",
            )
            send_achievement_notification(
                recipient=user, achievement_name="First defeat"
            )
            return "Admitted"
