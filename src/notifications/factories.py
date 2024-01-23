import factory
from faker import Faker

from notifications.models import Notification
from users.factories import ProfileFactory

fake = Faker()


class NotificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notification

    user = factory.SubFactory(ProfileFactory)
    message = fake.text()
    status = fake.random_element(
        elements=[choice[0] for choice in Notification.STATUS_CHOICES]
    )
