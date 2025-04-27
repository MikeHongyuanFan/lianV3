"""
Integration tests for WebSocket connection management.
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

User = get_user_model()


@pytest.mark.asyncio
async def test_websocket_connection_lifecycle(helpers):
    """Test the full WebSocket connection lifecycle."""
    # Create a user
    user = await helpers.create_user(
        username='lifecycleuser',
        email='lifecycle@example.com',
        password='password123',
        role='client'
    )
    
    # Get token
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)
    
    # Create application
    application = JWTAuthMiddleware(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    )
    
    # Test connection
    communicator = WebsocketCommunicator(
        application,
        f"ws/notifications/?token={token}"
    )
    
    connected, _ = await communicator.connect()
    assert connected, "WebSocket connection failed"
    
    # Test receiving initial unread count
    response = await communicator.receive_json_from(timeout=2)
    assert response["type"] == "unread_count"
    
    # Test sending a message
    await communicator.send_json_to({"type": "get_unread_count"})
    
    # Test receiving response
    response = await communicator.receive_json_from(timeout=2)
    assert response["type"] == "unread_count"
    
    # Test disconnection
    await communicator.disconnect()
    
    # Test reconnection
    communicator = WebsocketCommunicator(
        application,
        f"ws/notifications/?token={token}"
    )
    
    connected, _ = await communicator.connect()
    assert connected, "WebSocket reconnection failed"
    
    # Verify we receive the initial unread count again
    response = await communicator.receive_json_from(timeout=2)
    assert response["type"] == "unread_count"
    
    # Clean up
    await communicator.disconnect()


@pytest.mark.asyncio
async def test_websocket_connection_rejection():
    """Test WebSocket connection rejection scenarios."""
    # Test connection with invalid path
    application = JWTAuthMiddleware(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    )
    
    # Invalid path
    communicator = WebsocketCommunicator(
        application,
        "ws/invalid_path/"
    )
    
    connected, _ = await communicator.connect()
    assert not connected, "WebSocket connection succeeded with invalid path"


@pytest.mark.asyncio
async def test_websocket_message_handling(helpers):
    """Test WebSocket message handling."""
    # Create a user
    user = await helpers.create_user(
        username='messageuser',
        email='message@example.com',
        password='password123',
        role='client'
    )
    
    # Get token
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)
    
    # Create application
    application = JWTAuthMiddleware(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    )
    
    # Connect
    communicator = WebsocketCommunicator(
        application,
        f"ws/notifications/?token={token}"
    )
    
    connected, _ = await communicator.connect()
    assert connected, "WebSocket connection failed"
    
    # Receive initial unread count
    await communicator.receive_json_from(timeout=2)
    
    # Test sending a valid message
    await communicator.send_json_to({"type": "get_unread_count"})
    
    # Test receiving response
    response = await communicator.receive_json_from(timeout=2)
    assert response["type"] == "unread_count"
    
    # Test sending an invalid message
    await communicator.send_json_to({"type": "invalid_message_type"})
    
    # No response expected for invalid message type
    with pytest.raises(asyncio.TimeoutError):
        await communicator.receive_json_from(timeout=1)
    
    # Clean up
    await communicator.disconnect()


@pytest.mark.asyncio
async def test_websocket_connection_limit(helpers):
    """Test WebSocket connection limits and behavior with multiple connections."""
    # Create a user
    user = await helpers.create_user(
        username='multiconnectuser',
        email='multiconnect@example.com',
        password='password123',
        role='client'
    )
    
    # Get token
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)
    
    # Create application
    application = JWTAuthMiddleware(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    )
    
    # Create multiple connections for the same user
    communicator1 = WebsocketCommunicator(
        application,
        f"ws/notifications/?token={token}"
    )
    
    communicator2 = WebsocketCommunicator(
        application,
        f"ws/notifications/?token={token}"
    )
    
    # Connect both
    connected1, _ = await communicator1.connect()
    assert connected1, "First WebSocket connection failed"
    
    connected2, _ = await communicator2.connect()
    assert connected2, "Second WebSocket connection failed"
    
    # Receive initial unread counts on both connections
    await communicator1.receive_json_from(timeout=2)
    await communicator2.receive_json_from(timeout=2)
    
    # Create a notification
    notification_id = await helpers.create_notification(
        user=user,
        title="Multi-connection Test",
        message="Testing multiple connections",
        notification_type="system"
    )
    
    # Both connections should receive the notification
    response1 = await communicator1.receive_json_from(timeout=2)
    assert response1["type"] == "notification"
    
    response2 = await communicator2.receive_json_from(timeout=2)
    assert response2["type"] == "notification"
    
    # Both connections should receive the unread count update
    response1 = await communicator1.receive_json_from(timeout=2)
    assert response1["type"] == "unread_count"
    
    response2 = await communicator2.receive_json_from(timeout=2)
    assert response2["type"] == "unread_count"
    
    # Clean up
    await communicator1.disconnect()
    await communicator2.disconnect()
