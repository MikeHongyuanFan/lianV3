"""
Integration tests for real-time notifications.
"""
import pytest
import json
import asyncio
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from channels.auth import AuthMiddlewareStack
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from users.routing import websocket_urlpatterns
from users.websocket_auth import JWTAuthMiddleware
from users.models import Notification
from users.services import create_notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

User = get_user_model()


@pytest.mark.asyncio
async def test_realtime_notification_delivery(helpers):
    """Test real-time notification delivery via WebSocket."""
    # Create a user
    user = await helpers.create_user(
        username='notifyuser',
        email='notify@example.com',
        password='password123',
        role='client'
    )
    
    # Get token
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)
    
    # Connect with token
    application = JWTAuthMiddleware(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    )
    
    communicator = WebsocketCommunicator(
        application,
        f"ws/notifications/?token={token}"
    )
    
    connected, _ = await communicator.connect()
    assert connected, "WebSocket connection failed"
    
    # Receive initial unread count
    await communicator.receive_json_from(timeout=2)
    
    # Create a notification
    notification_id = await helpers.create_notification(
        user=user,
        title="Test Notification",
        message="This is a test notification",
        notification_type="system"
    )
    
    # Wait for WebSocket notification
    response = await communicator.receive_json_from(timeout=2)
    
    # Verify notification data
    assert response["type"] == "notification"
    assert response["notification"]["title"] == "Test Notification"
    assert response["notification"]["message"] == "This is a test notification"
    assert response["notification"]["notification_type"] == "system"
    assert not response["notification"]["is_read"]
    
    # Verify unread count update
    response = await communicator.receive_json_from(timeout=2)
    assert response["type"] == "unread_count"
    assert response["count"] == 1
    
    # Clean up
    await communicator.disconnect()


@pytest.mark.asyncio
async def test_notification_read_status_update(helpers):
    """Test notification read status updates via WebSocket."""
    # Create a user
    user = await helpers.create_user(
        username='readuser',
        email='read@example.com',
        password='password123',
        role='client'
    )
    
    # Create notifications
    notification1_id = await helpers.create_notification(
        user=user,
        title="Notification 1",
        message="This is notification 1",
        notification_type="system"
    )
    
    notification2_id = await helpers.create_notification(
        user=user,
        title="Notification 2",
        message="This is notification 2",
        notification_type="system"
    )
    
    # Get token
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)
    
    # Connect with token
    application = JWTAuthMiddleware(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    )
    
    communicator = WebsocketCommunicator(
        application,
        f"ws/notifications/?token={token}"
    )
    
    connected, _ = await communicator.connect()
    assert connected, "WebSocket connection failed"
    
    # Receive initial unread count (should be 2)
    response = await communicator.receive_json_from(timeout=2)
    assert response["type"] == "unread_count"
    assert response["count"] == 2
    
    # Mark one notification as read
    await helpers.mark_notification_as_read(notification1_id)
    
    # Wait for WebSocket unread count update
    response = await communicator.receive_json_from(timeout=2)
    assert response["type"] == "unread_count"
    assert response["count"] == 1
    
    # Mark all notifications as read
    await helpers.mark_all_notifications_as_read(user.id)
    
    # Wait for WebSocket unread count update
    response = await communicator.receive_json_from(timeout=2)
    assert response["type"] == "unread_count"
    assert response["count"] == 0
    
    # Clean up
    await communicator.disconnect()


@pytest.mark.asyncio
async def test_notification_filtering(helpers):
    """Test notification filtering by type."""
    # Create a user
    user = await helpers.create_user(
        username='filteruser',
        email='filter@example.com',
        password='password123',
        role='client'
    )
    
    # Create notifications of different types
    await helpers.create_notification(
        user=user,
        title="System Notification",
        message="This is a system notification",
        notification_type="system"
    )
    
    await helpers.create_notification(
        user=user,
        title="Application Status",
        message="Your application status has changed",
        notification_type="application_status"
    )
    
    # Get token
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)
    
    # Connect with token
    application = JWTAuthMiddleware(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    )
    
    communicator = WebsocketCommunicator(
        application,
        f"ws/notifications/?token={token}"
    )
    
    connected, _ = await communicator.connect()
    assert connected, "WebSocket connection failed"
    
    # Receive initial unread count (should be 2)
    response = await communicator.receive_json_from(timeout=2)
    assert response["type"] == "unread_count"
    assert response["count"] == 2
    
    # Create a new notification of a specific type
    await helpers.create_notification(
        user=user,
        title="Document Uploaded",
        message="A new document has been uploaded",
        notification_type="document_uploaded"
    )
    
    # Wait for WebSocket notification
    response = await communicator.receive_json_from(timeout=2)
    assert response["type"] == "notification"
    assert response["notification"]["notification_type"] == "document_uploaded"
    
    # Wait for WebSocket unread count update
    response = await communicator.receive_json_from(timeout=2)
    assert response["type"] == "unread_count"
    assert response["count"] == 3
    
    # Clean up
    await communicator.disconnect()


@pytest.mark.asyncio
async def test_multiple_clients(helpers):
    """Test notifications with multiple connected clients."""
    # Create two users
    user1 = await helpers.create_user(
        username='user1',
        email='user1@example.com',
        password='password123',
        role='client'
    )
    
    user2 = await helpers.create_user(
        username='user2',
        email='user2@example.com',
        password='password123',
        role='client'
    )
    
    # Get tokens
    refresh1 = RefreshToken.for_user(user1)
    token1 = str(refresh1.access_token)
    
    refresh2 = RefreshToken.for_user(user2)
    token2 = str(refresh2.access_token)
    
    # Create application
    application = JWTAuthMiddleware(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    )
    
    # Connect both users
    communicator1 = WebsocketCommunicator(
        application,
        f"ws/notifications/?token={token1}"
    )
    
    communicator2 = WebsocketCommunicator(
        application,
        f"ws/notifications/?token={token2}"
    )
    
    connected1, _ = await communicator1.connect()
    assert connected1, "WebSocket connection failed for user1"
    
    connected2, _ = await communicator2.connect()
    assert connected2, "WebSocket connection failed for user2"
    
    # Receive initial unread counts
    await communicator1.receive_json_from(timeout=2)
    await communicator2.receive_json_from(timeout=2)
    
    # Create a notification for user1 only
    await helpers.create_notification(
        user=user1,
        title="User1 Notification",
        message="This is for user1 only",
        notification_type="system"
    )
    
    # User1 should receive the notification
    response1 = await communicator1.receive_json_from(timeout=2)
    assert response1["type"] == "notification"
    assert response1["notification"]["title"] == "User1 Notification"
    
    # User1 should receive the unread count update
    response1 = await communicator1.receive_json_from(timeout=2)
    assert response1["type"] == "unread_count"
    assert response1["count"] == 1
    
    # User2 should not receive anything (would timeout)
    with pytest.raises(asyncio.TimeoutError):
        await communicator2.receive_json_from(timeout=1)
    
    # Clean up
    await communicator1.disconnect()
    await communicator2.disconnect()
