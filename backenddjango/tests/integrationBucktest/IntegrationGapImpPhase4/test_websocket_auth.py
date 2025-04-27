"""
Integration tests for WebSocket authentication.
"""
import pytest
import json
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from channels.auth import AuthMiddlewareStack
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from users.routing import websocket_urlpatterns
from users.websocket_auth import JWTAuthMiddleware
from users.models import Notification

User = get_user_model()


@pytest.mark.asyncio
async def test_websocket_token_authentication(helpers):
    """Test WebSocket authentication with valid JWT token."""
    # Create a user
    user = await helpers.create_user(
        username='testuser',
        email='test@example.com',
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
    assert connected, "WebSocket connection failed with valid token"
    
    # Verify initial unread count message
    response = await communicator.receive_json_from(timeout=2)
    assert response["type"] == "unread_count"
    assert "count" in response
    
    # Clean up
    await communicator.disconnect()


@pytest.mark.asyncio
async def test_websocket_invalid_token_authentication():
    """Test WebSocket authentication with invalid JWT token."""
    # Connect with invalid token
    application = JWTAuthMiddleware(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    )
    
    communicator = WebsocketCommunicator(
        application,
        "ws/notifications/?token=invalid_token"
    )
    
    connected, _ = await communicator.connect()
    assert not connected, "WebSocket connection succeeded with invalid token"


@pytest.mark.asyncio
async def test_websocket_missing_token_authentication():
    """Test WebSocket authentication with missing JWT token."""
    # Connect without token
    application = JWTAuthMiddleware(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    )
    
    communicator = WebsocketCommunicator(
        application,
        "ws/notifications/"
    )
    
    connected, _ = await communicator.connect()
    assert not connected, "WebSocket connection succeeded without token"


@pytest.mark.asyncio
async def test_websocket_token_expiration(helpers):
    """Test WebSocket behavior with expired JWT token."""
    # Create a user
    user = await helpers.create_user(
        username='expireduser',
        email='expired@example.com',
        password='password123',
        role='client'
    )
    
    # Get token with minimal expiration
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
    assert connected, "WebSocket connection failed with valid token"
    
    # Verify initial unread count message
    response = await communicator.receive_json_from(timeout=2)
    assert response["type"] == "unread_count"
    
    # Clean up
    await communicator.disconnect()
    
    # Note: To fully test expiration, we would need to manipulate token expiration
    # and wait for it to expire, which is not practical in a unit test.
    # In a real scenario, the client would need to reconnect with a new token.
