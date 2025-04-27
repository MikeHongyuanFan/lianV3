"""
Tests for notification WebSocket consumer.
"""
import pytest
import json
from unittest.mock import patch, MagicMock, AsyncMock
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from users.consumers import NotificationConsumer
from users.models import Notification
from tests.factories.user_factory import UserFactory
from tests.factories.notification_factory import NotificationFactory

User = get_user_model()

pytestmark = [pytest.mark.django_db, pytest.mark.asyncio]


@pytest.fixture
def mock_auth_middleware():
    """Mock the authentication middleware."""
    with patch('users.consumers.AuthMiddlewareStack', new=MagicMock()) as mock:
        yield mock


@pytest.fixture
async def notification_communicator(admin_user):
    """Create a WebSocket communicator for testing."""
    # Create a communicator
    communicator = WebsocketCommunicator(
        NotificationConsumer.as_asgi(),
        "/ws/notifications/"
    )
    
    # Mock the scope to include the user
    communicator.scope["user"] = admin_user
    
    # Connect
    connected, _ = await communicator.connect()
    assert connected
    
    yield communicator
    
    # Disconnect
    await communicator.disconnect()


async def test_connect(notification_communicator, admin_user):
    """Test connecting to the WebSocket."""
    # Send a message to verify connection
    await notification_communicator.send_json_to({
        'type': 'ping',
        'message': 'hello'
    })
    
    # Receive the response
    response = await notification_communicator.receive_json_from()
    
    # Check the response
    assert response['type'] == 'pong'
    assert response['message'] == 'hello'


async def test_disconnect(notification_communicator):
    """Test disconnecting from the WebSocket."""
    # Disconnect
    await notification_communicator.disconnect()
    
    # Try to send a message after disconnect
    with pytest.raises(Exception):
        await notification_communicator.send_json_to({
            'type': 'ping',
            'message': 'hello'
        })


async def test_receive_json_invalid(notification_communicator):
    """Test receiving invalid JSON."""
    # Send invalid JSON
    await notification_communicator.send_json_to({
        'type': 'invalid_type',
        'message': 'hello'
    })
    
    # Receive the error response
    response = await notification_communicator.receive_json_from()
    
    # Check the response
    assert response['type'] == 'error'
    assert 'message' in response


async def test_notification_message(notification_communicator, admin_user):
    """Test sending a notification message."""
    # Create a notification
    notification = NotificationFactory(user=admin_user)
    
    # Send a notification message directly to the consumer
    await notification_communicator.send_json_to({
        'type': 'notification_message',
        'notification': {
            'id': notification.id,
            'title': notification.title,
            'message': notification.message,
            'notification_type': notification.notification_type,
            'is_read': notification.is_read,
            'created_at': notification.created_at.isoformat()
        }
    })
    
    # Receive the notification
    response = await notification_communicator.receive_json_from()
    
    # Check the response
    assert response['type'] == 'notification'
    assert response['notification']['id'] == notification.id
    assert response['notification']['title'] == notification.title


async def test_mark_read_message(notification_communicator, admin_user):
    """Test marking a notification as read."""
    # Create an unread notification
    notification = NotificationFactory(user=admin_user, is_read=False)
    
    # Send a mark_read message
    await notification_communicator.send_json_to({
        'type': 'mark_read',
        'notification_id': notification.id
    })
    
    # Receive the response
    response = await notification_communicator.receive_json_from()
    
    # Check the response
    assert response['type'] == 'notification_read'
    assert response['notification_id'] == notification.id
    
    # Check that the notification was marked as read in the database
    notification.refresh_from_db()
    assert notification.is_read is True


async def test_mark_all_read_message(notification_communicator, admin_user):
    """Test marking all notifications as read."""
    # Create multiple unread notifications
    notification1 = NotificationFactory(user=admin_user, is_read=False)
    notification2 = NotificationFactory(user=admin_user, is_read=False)
    notification3 = NotificationFactory(user=admin_user, is_read=False)
    
    # Send a mark_all_read message
    await notification_communicator.send_json_to({
        'type': 'mark_all_read'
    })
    
    # Receive the response
    response = await notification_communicator.receive_json_from()
    
    # Check the response
    assert response['type'] == 'all_notifications_read'
    
    # Check that all notifications were marked as read in the database
    notification1.refresh_from_db()
    notification2.refresh_from_db()
    notification3.refresh_from_db()
    assert notification1.is_read is True
    assert notification2.is_read is True
    assert notification3.is_read is True


async def test_get_unread_count_message(notification_communicator, admin_user):
    """Test getting the unread notification count."""
    # Create multiple notifications with different read statuses
    NotificationFactory(user=admin_user, is_read=False)
    NotificationFactory(user=admin_user, is_read=False)
    NotificationFactory(user=admin_user, is_read=True)
    
    # Send a get_unread_count message
    await notification_communicator.send_json_to({
        'type': 'get_unread_count'
    })
    
    # Receive the response
    response = await notification_communicator.receive_json_from()
    
    # Check the response
    assert response['type'] == 'unread_count'
    assert response['count'] == 2
