import datetime

from celery import Task, shared_task
from celery.utils.log import get_task_logger

from .models import Habit

logger = get_task_logger(__name__)


@shared_task()
def schedule_interval_habit_task() -> None:
    habits = Habit.objects.filter(frequency="INTERVAL")
    for habit in habits:
        next_execution_date = habit.execution_date + datetime.timedelta(
            days=habit.interval_value
        )
        reset_interval.apply_async(args=[habit.id], eta=next_execution_date)


@shared_task()
def reset_interval(habit_id: int) -> None:
    try:
        habit = Habit.objects.get(pk=habit_id)
        habit.active = True
        habit.status = None
        habit.execution_date += datetime.timedelta(days=habit.interval_value)
        habit.save()
        logger.info(f"Reset interval for Habit with ID: {habit_id}")
    except Habit.DoesNotExist:
        logger.error(f"Habit with ID {habit_id} does not exist.")


@shared_task()
def reset_daily() -> None:
    habits = Habit.objects.filter(frequency="DAILY")

    for habit in habits:
        habit.status = None
        habit.active = True
        habit.execution_date = datetime.datetime.now().date()

        habit.save()


@shared_task()
def set_status_if_none() -> None:
    habits = Habit.objects.all()

    for habit in habits:
        if habit.status is None and habit.frequency == "DAILY":
            habit.status = "SKIPPED"
            habit.save()
            reset_daily()
        if habit.status is None and habit.frequency == "INTERVAL":
            habit.status = "SKIPPED"
            habit.save()
            reset_interval()
