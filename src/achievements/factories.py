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

    @factory.post_generation
    def user(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.user.set([extracted])
