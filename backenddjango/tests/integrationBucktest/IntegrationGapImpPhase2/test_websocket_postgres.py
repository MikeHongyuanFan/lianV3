"""
Integration tests for WebSocket functionality using PostgreSQL.
These tests are skipped if PostgreSQL is not available.
"""
import pytest
import os
import json
import asyncio
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from django.urls import re_path
from users.consumers import NotificationConsumer
from users.models import Notification
from channels.db import database_sync_to_async
from django.conf import settings
from django.test import override_settings

# Set up PostgreSQL test database configuration
POSTGRES_TEST_CONFIG = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get('POSTGRES_TEST_DB', 'test_db'),
        "USER": os.environ.get('POSTGRES_TEST_USER', 'postgres'),
        "PASSWORD": os.environ.get('POSTGRES_TEST_PASSWORD', 'postgres'),
        "HOST": os.environ.get('POSTGRES_TEST_HOST', 'localhost'),
        "PORT": os.environ.get('POSTGRES_TEST_PORT', '5433'),
        "TEST": {
            "NAME": os.environ.get('POSTGRES_TEST_DB', 'test_db'),
        }
    }
}

# Set up in-memory channel layer for testing
IN_MEMORY_CHANNEL_LAYER = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}

# Skip all tests in this module if PostgreSQL is not available
pytestmark = pytest.mark.skipif(
    not os.environ.get('POSTGRES_TEST_DB'),
    reason="PostgreSQL test database not available"
)

# Use asyncio marker with scope parameter instead of redefining event_loop
pytestmark = [
    pytestmark,
    pytest.mark.asyncio(scope="function")
]

@pytest.mark.django_db(transaction=True)
@override_settings(DATABASES=POSTGRES_TEST_CONFIG, CHANNEL_LAYERS=IN_MEMORY_CHANNEL_LAYER)
async def test_notification_consumer_connect_postgres(admin_user):
    """Test that a user can connect to the notification WebSocket with PostgreSQL"""
    # Create application with just our test consumer
    application = URLRouter([
        re_path(r"ws/notifications/$", NotificationConsumer.as_asgi()),
    ])
    
    # Create a communicator
    communicator = WebsocketCommunicator(application, "ws/notifications/")
    
    # Set user in scope (bypassing auth)
    communicator.scope["user"] = admin_user
    
    # Connect to the WebSocket
    connected, _ = await communicator.connect()
    assert connected
    
    # Verify initial unread count message
    response = await communicator.receive_json_from()
    assert response["type"] == "unread_count"
    assert "count" in response
    
    # Disconnect
    await communicator.disconnect()

@pytest.mark.django_db(transaction=True)
@override_settings(DATABASES=POSTGRES_TEST_CONFIG, CHANNEL_LAYERS=IN_MEMORY_CHANNEL_LAYER)
async def test_notification_consumer_receive_notification_postgres(admin_user):
    """Test that a user receives notifications through the WebSocket with PostgreSQL"""
    # Create application with just our test consumer
    application = URLRouter([
        re_path(r"ws/notifications/$", NotificationConsumer.as_asgi()),
    ])
    
    # Create a communicator
    communicator = WebsocketCommunicator(application, "ws/notifications/")
    
    # Set user in scope (bypassing auth)
    communicator.scope["user"] = admin_user
    
    # Connect to the WebSocket
    connected, _ = await communicator.connect()
    assert connected
    
    # Skip the initial unread count message
    await communicator.receive_json_from()
    
    # Create a notification for the user
    notification = await database_sync_to_async(create_notification)(admin_user)
    
    # Send notification through the channel layer
    from channels.layers import get_channel_layer
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        f"user_{admin_user.id}_notifications",
        {
            "type": "notification_message",
            "notification": {
                "id": notification.id,
                "message": notification.message,
                "notification_type": notification.notification_type,
                "created_at": notification.created_at.isoformat(),
                "is_read": notification.is_read
            }
        }
    )
    
    # Receive the notification
    response = await communicator.receive_json_from()
    assert response["type"] == "notification"
    assert response["notification"]["message"] == "Test notification"
    assert response["notification"]["notification_type"] == "test"
    
    # Disconnect
    await communicator.disconnect()

@pytest.mark.django_db(transaction=True)
@override_settings(DATABASES=POSTGRES_TEST_CONFIG, CHANNEL_LAYERS=IN_MEMORY_CHANNEL_LAYER)
async def test_notification_consumer_mark_read_postgres(admin_user):
    """Test marking notifications as read through WebSocket with PostgreSQL"""
    # Create application with just our test consumer
    application = URLRouter([
        re_path(r"ws/notifications/$", NotificationConsumer.as_asgi()),
    ])
    
    # Create a communicator
    communicator = WebsocketCommunicator(application, "ws/notifications/")
    
    # Set user in scope (bypassing auth)
    communicator.scope["user"] = admin_user
    
    # Connect to the WebSocket
    connected, _ = await communicator.connect()
    assert connected
    
    # Skip the initial unread count message
    await communicator.receive_json_from()
    
    # Create some unread notifications
    for i in range(3):
        await database_sync_to_async(create_notification)(admin_user, f"Test notification {i}")
    
    # Mark one notification as read
    notification = await database_sync_to_async(get_first_notification)(admin_user)
    await database_sync_to_async(mark_notification_read)(notification)
    
    # Send unread count update through the channel layer
    from channels.layers import get_channel_layer
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        f"user_{admin_user.id}_notifications",
        {
            "type": "notification_count",
            "count": 2  # 3 created, 1 marked as read
        }
    )
    
    # Receive the count update
    response = await communicator.receive_json_from()
    assert response["type"] == "unread_count"
    assert response["count"] == 2
    
    # Disconnect
    await communicator.disconnect()

@pytest.mark.django_db(transaction=True)
@override_settings(DATABASES=POSTGRES_TEST_CONFIG, CHANNEL_LAYERS=IN_MEMORY_CHANNEL_LAYER)
async def test_notification_consumer_get_unread_count_postgres(admin_user):
    """Test that a user can request the unread count through the WebSocket with PostgreSQL"""
    # Create application with just our test consumer
    application = URLRouter([
        re_path(r"ws/notifications/$", NotificationConsumer.as_asgi()),
    ])
    
    # Create a communicator
    communicator = WebsocketCommunicator(application, "ws/notifications/")
    
    # Set user in scope (bypassing auth)
    communicator.scope["user"] = admin_user
    
    # Connect to the WebSocket
    connected, _ = await communicator.connect()
    assert connected
    
    # Skip the initial unread count message
    await communicator.receive_json_from()
    
    # Create some unread notifications
    for i in range(3):
        await database_sync_to_async(create_notification)(
            admin_user, 
            message=f"Test notification {i}"
        )
    
    # Request unread count
    await communicator.send_json_to({"type": "get_unread_count"})
    
    # Receive the count update
    response = await communicator.receive_json_from()
    assert response["type"] == "unread_count"
    assert response["count"] == 3
    
    # Disconnect
    await communicator.disconnect()

# Helper functions for database operations
def create_notification(user, message="Test notification"):
    """Create a notification for a user"""
    return Notification.objects.create(
        user=user,
        message=message,
        notification_type="test"
    )

def get_first_notification(user):
    """Get the first notification for a user"""
    return Notification.objects.filter(user=user).first()

def mark_notification_read(notification):
    """Mark a notification as read"""
    notification.is_read = True
    notification.save()
    return notification
