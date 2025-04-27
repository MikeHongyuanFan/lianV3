"""
Integration tests for WebSocket functionality in the application.
"""
import pytest
import json
import asyncio
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from django.urls import re_path
from users.consumers import NotificationConsumer
from users.models import Notification
from unittest.mock import patch, MagicMock
from channels.db import database_sync_to_async

@pytest.mark.asyncio
async def test_notification_consumer_connect(admin_user):
    """Test that a user can connect to the notification WebSocket"""
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

@pytest.mark.asyncio
async def test_notification_consumer_anonymous_user():
    """Test that anonymous users cannot connect to the notification WebSocket"""
    # Create application with just our test consumer
    application = URLRouter([
        re_path(r"ws/notifications/$", NotificationConsumer.as_asgi()),
    ])
    
    # Create a communicator
    communicator = WebsocketCommunicator(application, "ws/notifications/")
    
    # Set anonymous user in scope
    communicator.scope["user"] = MagicMock(is_anonymous=True)
    
    # Try to connect to the WebSocket
    connected, _ = await communicator.connect()
    assert not connected

@pytest.mark.asyncio
@pytest.mark.django_db
async def test_notification_consumer_with_mocks():
    """Test WebSocket functionality using mocks to avoid database operations"""
    # Create application with just our test consumer
    application = URLRouter([
        re_path(r"ws/notifications/$", NotificationConsumer.as_asgi()),
    ])
    
    # Create a mock user
    mock_user = MagicMock()
    mock_user.is_anonymous = False
    mock_user.id = 999
    
    # Mock the get_unread_count method
    with patch('users.consumers.NotificationConsumer.get_unread_count') as mock_get_count:
        # Set up mock return value
        mock_get_count.return_value = 5
        
        # Create a communicator
        communicator = WebsocketCommunicator(application, "ws/notifications/")
        
        # Set user in scope
        communicator.scope["user"] = mock_user
        
        # Connect to the WebSocket
        connected, _ = await communicator.connect()
        assert connected
        
        # Verify initial count message
        response = await communicator.receive_json_from()
        assert response["type"] == "unread_count"
        assert response["count"] == 5
        
        # Disconnect - we'll skip the actual disconnect to avoid database access
        # await communicator.disconnect()
