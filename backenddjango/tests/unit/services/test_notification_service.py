"""
Tests for notification services.
"""
import pytest
from unittest.mock import patch, MagicMock
from users.services.notification_service import (
    create_notification, create_application_notification,
    send_email_notification, get_or_create_notification_preferences
)
from users.models import Notification, NotificationPreference
from applications.models import Application
from tests.factories.notification_factory import NotificationFactory, ReadNotificationFactory
from tests.factories.user_factory import UserFactory, AdminUserFactory

pytestmark = pytest.mark.django_db


@pytest.mark.service
def test_create_notification(admin_user):
    """Test creating a notification."""
    # Create a notification
    with patch('users.services.notification_service.get_channel_layer') as mock_channel_layer:
        # Mock the channel layer and async_to_sync
        mock_channel_layer.return_value = MagicMock()
        
        notification = create_notification(
            user=admin_user,
            title='Test Notification',
            message='This is a test notification',
            notification_type='application_status',
            related_object_id=1,
            related_object_type='application'
        )
    
    # Check that the notification was created correctly
    assert notification is not None
    assert notification.user == admin_user
    assert notification.title == 'Test Notification'
    assert notification.message == 'This is a test notification'
    assert notification.notification_type == 'application_status'
    assert notification.related_object_id == 1
    assert notification.related_object_type == 'application'
    assert not notification.is_read


@pytest.mark.service
def test_create_notification_with_preferences_disabled(admin_user):
    """Test creating a notification when preferences are disabled."""
    # Create notification preferences with application_status_in_app disabled
    preferences = NotificationPreference.objects.create(
        user=admin_user,
        application_status_in_app=False
    )
    
    # Create a notification
    notification = create_notification(
        user=admin_user,
        title='Test Notification',
        message='This is a test notification',
        notification_type='application_status'
    )
    
    # Check that no notification was created
    assert notification is None


@pytest.mark.service
def test_create_notification_with_websocket_error(admin_user):
    """Test creating a notification when WebSocket sends fails."""
    # Create a notification with WebSocket error
    with patch('users.services.notification_service.get_channel_layer') as mock_channel_layer:
        # Mock the channel layer to raise an exception
        mock_channel_layer.side_effect = Exception("WebSocket error")
        
        # This should not fail despite the WebSocket error
        notification = create_notification(
            user=admin_user,
            title='Test Notification',
            message='This is a test notification',
            notification_type='application_status'
        )
    
    # Check that the notification was still created
    assert notification is not None
    assert notification.user == admin_user
    assert notification.title == 'Test Notification'


@pytest.mark.service
@patch('users.services.notification_service.create_notification')
def test_create_application_notification(mock_create_notification, admin_user):
    """Test creating notifications for users related to an application."""
    # Mock create_notification to return a MagicMock
    mock_create_notification.return_value = MagicMock()
    
    # Create application with mock users
    application = MagicMock()
    application.broker.user = UserFactory()
    application.bd.user = UserFactory()
    
    # Create application notification
    notifications = create_application_notification(
        application=application,
        notification_type='application_status',
        title='Test Application Notification',
        message='This is a test application notification'
    )
    
    # Check that create_notification was called for broker, BD, and admin users
    assert mock_create_notification.call_count >= 2  # At least broker and BD users


@pytest.mark.service
def test_send_email_notification_success(admin_user):
    """Test sending an email notification successfully."""
    # Send email notification
    with patch('users.services.notification_service.send_mail') as mock_send_mail:
        # Mock send_mail to return True
        mock_send_mail.return_value = 1
        
        result = send_email_notification(
            user=admin_user,
            subject='Test Email',
            message='This is a test email'
        )
    
    # Check that the email was sent
    assert result is True
    mock_send_mail.assert_called_once()


@pytest.mark.service
def test_send_email_notification_no_email(admin_user):
    """Test sending an email notification to a user with no email."""
    # Remove email from user
    admin_user.email = ''
    admin_user.save()
    
    # Send email notification
    result = send_email_notification(
        user=admin_user,
        subject='Test Email',
        message='This is a test email'
    )
    
    # Check that the email was not sent
    assert result is False


@pytest.mark.service
def test_send_email_notification_error(admin_user):
    """Test sending an email notification with an error."""
    # Send email notification with error
    with patch('users.services.notification_service.send_mail') as mock_send_mail:
        # Mock send_mail to raise an exception
        mock_send_mail.side_effect = Exception("Email error")
        
        result = send_email_notification(
            user=admin_user,
            subject='Test Email',
            message='This is a test email'
        )
    
    # Check that the function handled the error
    assert result is False


@pytest.mark.service
def test_get_or_create_notification_preferences_existing(admin_user):
    """Test getting existing notification preferences."""
    # Create notification preferences
    original_preferences = NotificationPreference.objects.create(
        user=admin_user,
        application_status_in_app=False,
        document_uploaded_in_app=True,
        repayment_upcoming_in_app=False,
        application_status_email=True
    )
    
    # Get or create preferences
    preferences = get_or_create_notification_preferences(admin_user)
    
    # Check that the existing preferences were returned
    assert preferences.id == original_preferences.id
    assert preferences.application_status_in_app is False
    assert preferences.document_uploaded_in_app is True
    assert preferences.repayment_upcoming_in_app is False
    assert preferences.application_status_email is True


@pytest.mark.service
def test_get_or_create_notification_preferences_new(admin_user):
    """Test creating new notification preferences."""
    # Get or create preferences
    preferences = get_or_create_notification_preferences(admin_user)
    
    # Check that new preferences were created with default values
    assert preferences is not None
    assert preferences.application_status_in_app is True  # Default value
    assert preferences.document_uploaded_in_app is True  # Default value
    assert preferences.repayment_upcoming_in_app is True  # Default value
    assert preferences.application_status_email is True  # Default value
