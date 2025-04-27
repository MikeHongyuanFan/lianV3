"""
Tests for user notification services.
"""
import pytest
from unittest.mock import patch, MagicMock
from users.services.notification_service import (
    create_notification, create_application_notification,
    send_email_notification, get_or_create_notification_preferences
)
from users.models import Notification, NotificationPreference
from applications.models import Application
from tests.factories import (
    ApplicationFactory, AdminUserFactory, BrokerUserFactory,
    BrokerFactory, BDMFactory, UserFactory
)

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
    # Create notification preferences with application_status disabled
    preferences = NotificationPreference.objects.create(
        user=admin_user,
        application_status=False
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
def test_create_application_notification(admin_user):
    """Test creating notifications for users related to an application."""
    # Create broker and BD users
    broker_user = BrokerUserFactory()
    bd_user = UserFactory(role='bd')
    
    # Create broker and BD
    broker = BrokerFactory(user=broker_user)
    bd = BDMFactory(user=bd_user)
    
    # Create an application with broker and BD
    application = ApplicationFactory(broker=broker, bd=bd)
    
    # Create admin user
    admin = admin_user
    
    # Create application notification
    with patch('users.services.notification_service.create_notification') as mock_create_notification:
        # Mock create_notification to return a MagicMock
        mock_create_notification.return_value = MagicMock()
        
        notifications = create_application_notification(
            application=application,
            notification_type='application_status',
            title='Test Application Notification',
            message='This is a test application notification'
        )
    
    # Check that create_notification was called for broker, BD, and admin
    assert mock_create_notification.call_count >= 3
    
    # Check that the calls included the broker, BD, and admin users
    user_args = [call_args[1]['user'] for call_args in mock_create_notification.call_args_list]
    assert broker_user in user_args
    assert bd_user in user_args
    assert admin in user_args


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
        application_status=False,
        document_upload=True,
        repayment_reminder=False,
        email_notifications=True
    )
    
    # Get or create preferences
    preferences = get_or_create_notification_preferences(admin_user)
    
    # Check that the existing preferences were returned
    assert preferences.id == original_preferences.id
    assert preferences.application_status is False
    assert preferences.document_upload is True
    assert preferences.repayment_reminder is False
    assert preferences.email_notifications is True


@pytest.mark.service
def test_get_or_create_notification_preferences_new(admin_user):
    """Test creating new notification preferences."""
    # Get or create preferences
    preferences = get_or_create_notification_preferences(admin_user)
    
    # Check that new preferences were created with default values
    assert preferences is not None
    assert preferences.application_status is True  # Default value
    assert preferences.document_upload is True  # Default value
    assert preferences.repayment_reminder is True  # Default value
    assert preferences.email_notifications is True  # Default value
