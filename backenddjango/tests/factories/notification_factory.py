"""
Factory for creating Notification objects.
"""
import factory
from factory.django import DjangoModelFactory
from users.models import Notification, NotificationPreference
from tests.factories.user_factory import UserFactory


class NotificationFactory(DjangoModelFactory):
    """Factory for creating Notification objects."""

    class Meta:
        model = Notification

    user = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence', nb_words=3)
    message = factory.Faker('paragraph', nb_sentences=2)
    notification_type = factory.Iterator(['application_status', 'document_uploaded', 'repayment_upcoming', 'system'])
    is_read = False


class ReadNotificationFactory(NotificationFactory):
    """Factory for creating read Notification objects."""

    is_read = True
    read_at = factory.Faker('date_time_this_month', tzinfo=factory.Faker('pytimezone'))


class NotificationPreferenceFactory(DjangoModelFactory):
    """Factory for creating NotificationPreference objects."""

    class Meta:
        model = NotificationPreference

    user = factory.SubFactory(UserFactory)
    application_status = True
    document_upload = True
    repayment_reminder = True
    email_notifications = True
