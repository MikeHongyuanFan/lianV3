"""
Tests for WebSocket consumers.
"""
import pytest
import json
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from users.consumers import NotificationConsumer
from crm_backend.asgi import application
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()

@pytest.mark.asyncio
@pytest.mark.websocket
async def test_notification_consumer_connect_with_valid_token(admin_user):
    """Test that a user can connect to the notification consumer with a valid token."""
    # Create a valid token for the user
    token = AccessToken.for_user(admin_user)
    
    # Connect to the websocket with the token
    communicator = WebsocketCommunicator(
        application=application,
        path=f"/ws/notifications/?token={token}"
    )
    connected, _ = await communicator.connect()
    
    # Check that the connection was accepted
    assert connected
    
    # Close the connection
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.websocket
async def test_notification_consumer_connect_without_token():
    """Test that a user cannot connect to the notification consumer without a token."""
    # Connect to the websocket without a token
    communicator = WebsocketCommunicator(
        application=application,
        path="/ws/notifications/"
    )
    connected, _ = await communicator.connect()
    
    # Check that the connection was rejected
    assert not connected


@pytest.mark.asyncio
@pytest.mark.websocket
async def test_notification_consumer_connect_with_invalid_token():
    """Test that a user cannot connect to the notification consumer with an invalid token."""
    # Connect to the websocket with an invalid token
    communicator = WebsocketCommunicator(
        application=application,
        path="/ws/notifications/?token=invalid_token"
    )
    connected, _ = await communicator.connect()
    
    # Check that the connection was rejected
    assert not connected


@pytest.mark.asyncio
@pytest.mark.websocket
async def test_notification_consumer_receive_notification(admin_user):
    """Test that a user can receive a notification through the websocket."""
    # Create a valid token for the user
    token = AccessToken.for_user(admin_user)
    
    # Connect to the websocket with the token
    communicator = WebsocketCommunicator(
        application=application,
        path=f"/ws/notifications/?token={token}"
    )
    connected, _ = await communicator.connect()
    assert connected
    
    # Send a notification to the user
    notification_data = {
        "type": "notification.message",
        "message": {
            "id": 1,
            "title": "Test Notification",
            "message": "This is a test notification",
            "notification_type": "application_status",
            "is_read": False,
            "created_at": "2023-01-01T00:00:00Z"
        }
    }
    
    # Use the consumer's group_send method to send the notification
    await NotificationConsumer.group_send(
        f"notifications_{admin_user.id}",
        notification_data
    )
    
    # Receive the notification from the websocket
    response = await communicator.receive_json_from()
    
    # Check that the notification was received correctly
    assert response["title"] == "Test Notification"
    assert response["message"] == "This is a test notification"
    assert response["notification_type"] == "application_status"
    assert not response["is_read"]
    
    # Close the connection
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.websocket
async def test_notification_consumer_receive_unread_count(admin_user):
    """Test that a user can receive an unread count update through the websocket."""
    # Create a valid token for the user
    token = AccessToken.for_user(admin_user)
    
    # Connect to the websocket with the token
    communicator = WebsocketCommunicator(
        application=application,
        path=f"/ws/notifications/?token={token}"
    )
    connected, _ = await communicator.connect()
    assert connected
    
    # Send an unread count update to the user
    unread_count_data = {
        "type": "unread_count",
        "count": 5
    }
    
    # Use the consumer's group_send method to send the unread count
    await NotificationConsumer.group_send(
        f"notifications_{admin_user.id}",
        unread_count_data
    )
    
    # Receive the unread count from the websocket
    response = await communicator.receive_json_from()
    
    # Check that the unread count was received correctly
    assert response["type"] == "unread_count"
    assert response["count"] == 5
    
    # Close the connection
    await communicator.disconnect()
