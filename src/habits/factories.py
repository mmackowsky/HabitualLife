import factory
from faker import Faker

from habits.models import Category, Habit
from users.factories import ProfileFactory

fake = Faker()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")
    user = factory.SubFactory(ProfileFactory)


class HabitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Habit

    user = factory.SubFactory(ProfileFactory)
    name = fake.word()
    category = factory.SubFactory(CategoryFactory)
    active = fake.boolean()
    frequency = fake.random_element(
        elements=[choice[0] for choice in Habit.FREQUENCY_CHOICES]
    )
    interval_value = fake.random_int(min=2, max=30)
    execution_date = fake.date_this_decade()
    is_positive = fake.boolean()
    status = fake.random_element(
        elements=[choice[0] for choice in Habit.STATUS_CHOICES]
    )
    success_count = fake.random_int(min=0, max=10)
    failed_count = fake.random_int(min=0, max=5)
    skipped_count = fake.random_int(min=0, max=5)
    streak_count = fake.random_int(min=0, max=10)
