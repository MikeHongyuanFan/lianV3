"""
Factories for notification models.
"""
import factory
from factory.django import DjangoModelFactory
from users.models import Notification, NotificationPreference
from django.utils import timezone
from .user_factories import UserFactory


class NotificationFactory(DjangoModelFactory):
    """Factory for Notification model."""
    
    class Meta:
        model = Notification
    
    user = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence', nb_words=4)
    message = factory.Faker('paragraph')
    notification_type = factory.Iterator([
        'application_status', 'repayment_upcoming', 'repayment_overdue',
        'note_reminder', 'document_uploaded', 'signature_required', 'system'
    ])
    related_object_id = factory.Sequence(lambda n: n)
    related_object_type = factory.Iterator(['application', 'document', 'repayment'])
    is_read = False
    created_at = factory.LazyFunction(timezone.now)
    read_at = None


class NotificationPreferenceFactory(DjangoModelFactory):
    """Factory for NotificationPreference model."""
    
    class Meta:
        model = NotificationPreference
    
    user = factory.SubFactory(UserFactory)
    
    # In-app notification preferences
    application_status_in_app = True
    repayment_upcoming_in_app = True
    repayment_overdue_in_app = True
    note_reminder_in_app = True
    document_uploaded_in_app = True
    signature_required_in_app = True
    system_in_app = True
    
    # Email notification preferences
    application_status_email = True
    repayment_upcoming_email = True
    repayment_overdue_email = True
    note_reminder_email = True
    document_uploaded_email = False
    signature_required_email = True
    system_email = False
    
    # Digest preferences
    daily_digest = False
    weekly_digest = False
    
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)
