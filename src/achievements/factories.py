import factory
from faker import Faker

from achievements.models import Achievement
from users.factories import ProfileFactory

fake = Faker()


class AchievementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Achievement

    user = factory.SubFactory(ProfileFactory)
    name = fake.word()
    description = fake.text()
