"""
Mock-based WebSocket tests for environments without PostgreSQL.
"""
import pytest
import json
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from django.contrib.auth import get_user_model
from unittest.mock import patch, MagicMock
from users.routing import websocket_urlpatterns
from users.consumers import NotificationConsumer

User = get_user_model()


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_websocket_with_mocks(helpers):
    """Test WebSocket functionality using mocks."""
    # Create a user
    user = await helpers.create_user(
        username='mockuser',
        email='mock@example.com',
        password='password123',
        role='client'
    )
    
    # Mock the get_unread_count method
    with patch.object(NotificationConsumer, 'get_unread_count', return_value=5):
        # Create application with direct user authentication
        application = URLRouter(websocket_urlpatterns)
        
        # Create communicator
        communicator = WebsocketCommunicator(application, "ws/notifications/")
        
        # Set user in scope directly (bypass auth)
        communicator.scope["user"] = user
        
        # Connect
        connected, _ = await communicator.connect()
        assert connected, "WebSocket connection failed with mocked auth"
        
        # Verify initial count message
        response = await communicator.receive_json_from(timeout=2)
        assert response["type"] == "unread_count"
        assert response["count"] == 5
        
        # Clean up
        await communicator.disconnect()


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_notification_message_handler_with_mocks(helpers):
    """Test notification_message handler using mocks."""
    # Create a user
    user = await helpers.create_user(
        username='mockhandleruser',
        email='mockhandler@example.com',
        password='password123',
        role='client'
    )
    
    # Create application with direct user authentication
    application = URLRouter(websocket_urlpatterns)
    
    # Create communicator
    communicator = WebsocketCommunicator(application, "ws/notifications/")
    
    # Set user in scope directly (bypass auth)
    communicator.scope["user"] = user
    
    # Connect
    connected, _ = await communicator.connect()
    assert connected, "WebSocket connection failed with mocked auth"
    
    # Receive initial unread count
    await communicator.receive_json_from(timeout=2)
    
    # Mock a notification message from the channel layer
    notification_data = {
        'id': 1,
        'title': 'Mocked Notification',
        'message': 'This is a mocked notification',
        'notification_type': 'system',
        'is_read': False,
        'created_at': '2023-01-01T12:00:00Z'
    }
    
    # Get the consumer instance
    consumer = communicator.application.consumer_instances[0]
    
    # Call the notification_message method directly
    await consumer.notification_message({
        'type': 'notification_message',
        'notification': notification_data
    })
    
    # Verify the notification was sent
    response = await communicator.receive_json_from(timeout=2)
    assert response["type"] == "notification"
    assert response["notification"]["title"] == "Mocked Notification"
    assert response["notification"]["message"] == "This is a mocked notification"
    
    # Clean up
    await communicator.disconnect()


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_notification_count_handler_with_mocks(helpers):
    """Test notification_count handler using mocks."""
    # Create a user
    user = await helpers.create_user(
        username='mockcountuser',
        email='mockcount@example.com',
        password='password123',
        role='client'
    )
    
    # Create application with direct user authentication
    application = URLRouter(websocket_urlpatterns)
    
    # Create communicator
    communicator = WebsocketCommunicator(application, "ws/notifications/")
    
    # Set user in scope directly (bypass auth)
    communicator.scope["user"] = user
    
    # Connect
    connected, _ = await communicator.connect()
    assert connected, "WebSocket connection failed with mocked auth"
    
    # Receive initial unread count
    await communicator.receive_json_from(timeout=2)
    
    # Get the consumer instance
    consumer = communicator.application.consumer_instances[0]
    
    # Call the notification_count method directly
    await consumer.notification_count({
        'type': 'notification_count',
        'count': 10
    })
    
    # Verify the count was sent
    response = await communicator.receive_json_from(timeout=2)
    assert response["type"] == "unread_count"
    assert response["count"] == 10
    
    # Clean up
    await communicator.disconnect()


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_receive_method_with_mocks(helpers):
    """Test receive method using mocks."""
    # Create a user
    user = await helpers.create_user(
        username='mockreceiveuser',
        email='mockreceive@example.com',
        password='password123',
        role='client'
    )
    
    # Mock the get_unread_count method
    with patch.object(NotificationConsumer, 'get_unread_count', return_value=7):
        # Create application with direct user authentication
        application = URLRouter(websocket_urlpatterns)
        
        # Create communicator
        communicator = WebsocketCommunicator(application, "ws/notifications/")
        
        # Set user in scope directly (bypass auth)
        communicator.scope["user"] = user
        
        # Connect
        connected, _ = await communicator.connect()
        assert connected, "WebSocket connection failed with mocked auth"
        
        # Receive initial unread count
        await communicator.receive_json_from(timeout=2)
        
        # Send a get_unread_count message
        await communicator.send_json_to({"type": "get_unread_count"})
        
        # Verify the response
        response = await communicator.receive_json_from(timeout=2)
        assert response["type"] == "unread_count"
        assert response["count"] == 7
        
        # Clean up
        await communicator.disconnect()
