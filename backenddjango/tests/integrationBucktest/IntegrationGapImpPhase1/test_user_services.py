"""
Integration tests for user services.
"""
import pytest
from django.contrib.auth import get_user_model
from users.services import (
    create_notification,
    create_application_notification,
    send_email_notification,
    get_or_create_notification_preferences
)
from users.models import Notification, NotificationPreference
from applications.models import Application
from borrowers.models import Borrower
from brokers.models import Broker, BDM
from django.utils import timezone
from unittest.mock import patch, MagicMock

User = get_user_model()

@pytest.fixture
def admin_user():
    """Create an admin user for testing."""
    return User.objects.create_user(
        username="admin",
        email="admin@example.com",
        password="password123",
        first_name="Admin",
        last_name="User",
        role="admin"
    )

@pytest.fixture
def borrower_user():
    """Create a borrower user for testing."""
    return User.objects.create_user(
        username="borrower",
        email="borrower@example.com",
        password="password123",
        first_name="Borrower",
        last_name="User",
        role="borrower"
    )

@pytest.fixture
def broker_user():
    """Create a broker user for testing."""
    return User.objects.create_user(
        username="broker",
        email="broker@example.com",
        password="password123",
        first_name="Broker",
        last_name="User",
        role="broker"
    )

@pytest.fixture
def application(admin_user, borrower_user, broker_user):
    """Create a test application with borrower and broker."""
    application = Application.objects.create(
        reference_number="APP-TEST-001",
        application_type="residential",
        purpose="Home purchase",
        loan_amount=500000.00,
        loan_term=360,
        interest_rate=3.50,
        repayment_frequency="monthly",
        stage="draft",
        created_by=admin_user
    )
    
    # Create borrower
    borrower = Borrower.objects.create(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        user=borrower_user,
        created_by=admin_user
    )
    application.borrowers.add(borrower)
    
    # Create proper Broker instance
    broker = Broker.objects.create(
        name="Broker User",
        email="broker@example.com",
        user=broker_user,
        created_by=admin_user
    )
    application.broker = broker
    
    application.save()
    
    return application

@pytest.mark.django_db
def test_create_notification(admin_user):
    """Test creating a notification."""
    notification = create_notification(
        user=admin_user,
        title="Test Notification",
        message="This is a test notification",
        notification_type="system",
        related_object_id=1,
        related_object_type="application"
    )
    
    # Verify notification was created
    assert notification is not None
    assert notification.user == admin_user
    assert notification.title == "Test Notification"
    assert notification.message == "This is a test notification"
    assert notification.notification_type == "system"
    assert notification.related_object_id == 1
    assert notification.related_object_type == "application"
    assert notification.is_read is False
    
    # Verify notification in database
    db_notification = Notification.objects.get(id=notification.id)
    assert db_notification.title == "Test Notification"

@pytest.mark.django_db
def test_create_notification_with_preferences(admin_user):
    """Test creating a notification with notification preferences."""
    # Create notification preferences that disable in-app notifications for system type
    preferences = NotificationPreference.objects.create(
        user=admin_user,
        system_in_app=False,
        system_email=False
    )
    
    notification = create_notification(
        user=admin_user,
        title="Test Notification",
        message="This is a test notification",
        notification_type="system"
    )
    
    # Verify notification was not created due to preferences
    assert notification is None
    
    # Verify no notification in database
    db_notifications = Notification.objects.filter(
        user=admin_user,
        title="Test Notification"
    )
    assert not db_notifications.exists()
    
    # Now test with a notification type that is enabled
    preferences.application_status_in_app = True
    preferences.save()
    
    notification = create_notification(
        user=admin_user,
        title="Test Notification",
        message="This is a test notification",
        notification_type="application_status"
    )
    
    # Verify notification was created
    assert notification is not None
    assert notification.notification_type == "application_status"

@pytest.mark.django_db
def test_create_application_notification(application, admin_user, borrower_user, broker_user):
    """Test creating application notifications."""
    notifications = create_application_notification(
        application=application,
        notification_type="application_status",
        title="Application Status Update",
        message="The application status has been updated"
    )
    
    # Verify notifications were created
    assert len(notifications) > 0
    
    # Verify notifications in database
    db_notifications = Notification.objects.filter(
        notification_type="application_status",
        related_object_id=application.id
    )
    assert db_notifications.count() > 0
    
    # Verify notifications for different user types
    user_ids = [notification.user.id for notification in db_notifications]
    assert borrower_user.id in user_ids  # Borrower should get notification
    assert broker_user.id in user_ids  # Broker should get notification
    assert admin_user.id in user_ids  # Admin should get notification

@pytest.mark.django_db
def test_send_email_notification(admin_user):
    """Test sending an email notification."""
    # We'll just test the function returns True when a user has an email
    result = send_email_notification(
        user=admin_user,
        subject="Test Email",
        message="This is a test email"
    )
    
    # Verify email was sent (or at least the function returned True)
    assert result is True
    
    # Test with user without email
    user_without_email = User.objects.create_user(
        username="no_email",
        email="",
        password="password123",
        first_name="No",
        last_name="Email"
    )
    
    result = send_email_notification(
        user=user_without_email,
        subject="Test Email",
        message="This is a test email"
    )
    
    # Verify email was not sent
    assert result is False

@pytest.mark.django_db
def test_get_or_create_notification_preferences(admin_user):
    """Test getting or creating notification preferences."""
    # Initially, no preferences exist
    assert NotificationPreference.objects.filter(user=admin_user).count() == 0
    
    # Get or create preferences
    preferences = get_or_create_notification_preferences(admin_user)
    
    # Verify preferences were created
    assert preferences is not None
    assert preferences.user == admin_user
    
    # Verify preferences in database
    db_preferences = NotificationPreference.objects.get(user=admin_user)
    assert db_preferences == preferences
    
    # Call again to test getting existing preferences
    preferences_again = get_or_create_notification_preferences(admin_user)
    
    # Verify same preferences were returned
    assert preferences_again == preferences
    
    # Verify no new preferences were created
    assert NotificationPreference.objects.filter(user=admin_user).count() == 1
