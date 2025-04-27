"""
Integration tests for WebSocket API.
"""
import pytest
import json
import asyncio
import uuid
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from django.urls import re_path
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from users.consumers import NotificationConsumer
from users.models import Notification
from channels.db import database_sync_to_async
from .common import APITestClient

User = get_user_model()

# Custom middleware for testing
class TokenAuthMiddleware:
    """
    Custom middleware for token authentication in WebSocket tests.
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Get token from query string
        query_string = scope.get('query_string', b'').decode()
        token = None
        if query_string:
            params = dict(param.split('=') for param in query_string.split('&') if '=' in param)
            token = params.get('token')
        
        # If token is provided, set user in scope
        if token and 'user' not in scope:
            user = await self.get_user_from_token(token)
            if user:
                scope['user'] = user
        
        return await self.app(scope, receive, send)
    
    @database_sync_to_async
    def get_user_from_token(self, token):
        """Get user from token."""
        from rest_framework_simplejwt.tokens import AccessToken
        try:
            # Validate token
            validated_token = AccessToken(token)
            user_id = validated_token['user_id']
            return User.objects.get(id=user_id)
        except Exception:
            return None

# Apply middleware
def get_application(user=None):
    """Get application with middleware."""
    application = URLRouter([
        re_path(r'ws/notifications/$', NotificationConsumer.as_asgi()),
    ])
    
    # If user is provided, set it directly in scope
    if user:
        async def app(scope, receive, send):
            scope['user'] = user
            return await application(scope, receive, send)
        return app
    
    # Otherwise, use token middleware
    return TokenAuthMiddleware(application)

@pytest.mark.django_db
@pytest.mark.asyncio
class TestWebSocketAPI:
    """Test WebSocket API for notifications."""
    
    @pytest.fixture
    def event_loop(self):
        """Create an instance of the default event loop for each test."""
        loop = asyncio.get_event_loop_policy().new_event_loop()
        yield loop
        loop.close()
    
    @database_sync_to_async
    def create_user(self):
        """Create a test user."""
        unique_id = uuid.uuid4().hex[:8]
        return User.objects.create_user(
            username=f'testuser_{unique_id}',
            email=f'test_{unique_id}@example.com',
            password='password123',
            role='client'
        )
    
    @database_sync_to_async
    def create_notifications(self, user, count=3):
        """Create test notifications for a user."""
        notifications = []
        for i in range(count):
            notification = Notification.objects.create(
                user=user,
                title=f'Test Notification {i+1}',
                message=f'This is test notification {i+1}',
                notification_type='test'
            )
            notifications.append(notification)
        return notifications
    
    async def test_websocket_connect(self):
        """Test WebSocket connection."""
        # Create a user
        user = await self.create_user()
        
        # Set up communicator with user directly in scope
        communicator = WebsocketCommunicator(
            get_application(user),
            "ws/notifications/"
        )
        
        # Connect
        connected, _ = await communicator.connect()
        
        # Assert connection
        assert connected, "WebSocket connection failed"
        
        # Disconnect
        await communicator.disconnect()
    
    async def test_websocket_receive_unread_count(self):
        """Test receiving unread notification count on connect."""
        # Create a user
        user = await self.create_user()
        
        # Create notifications
        await self.create_notifications(user, 3)
        
        # Set up communicator with user directly in scope
        communicator = WebsocketCommunicator(
            get_application(user),
            "ws/notifications/"
        )
        
        # Connect
        connected, _ = await communicator.connect()
        assert connected, "WebSocket connection failed"
        
        # Receive unread count message
        response = await communicator.receive_json_from()
        
        # Assert response
        assert response['type'] == 'unread_count', f"Expected message type 'unread_count', got {response['type']}"
        assert response['count'] == 3, f"Expected count 3, got {response['count']}"
        
        # Disconnect
        await communicator.disconnect()
    
    async def test_websocket_request_unread_count(self):
        """Test requesting unread notification count."""
        # Create a user
        user = await self.create_user()
        
        # Create notifications
        await self.create_notifications(user, 3)
        
        # Set up communicator with user directly in scope
        communicator = WebsocketCommunicator(
            get_application(user),
            "ws/notifications/"
        )
        
        # Connect
        connected, _ = await communicator.connect()
        assert connected, "WebSocket connection failed"
        
        # Receive initial unread count
        await communicator.receive_json_from()
        
        # Request unread count
        await communicator.send_json_to({'type': 'get_unread_count'})
        
        # Receive unread count message
        response = await communicator.receive_json_from()
        
        # Assert response
        assert response['type'] == 'unread_count', f"Expected message type 'unread_count', got {response['type']}"
        assert response['count'] == 3, f"Expected count 3, got {response['count']}"
        
        # Disconnect
        await communicator.disconnect()
    
    async def test_websocket_disconnect(self):
        """Test WebSocket disconnection."""
        # Create a user
        user = await self.create_user()
        
        # Set up communicator with user directly in scope
        communicator = WebsocketCommunicator(
            get_application(user),
            "ws/notifications/"
        )
        
        # Connect
        connected, _ = await communicator.connect()
        assert connected, "WebSocket connection failed"
        
        # Disconnect
        await communicator.disconnect()
    
    async def test_websocket_anonymous_user(self):
        """Test WebSocket connection with anonymous user."""
        # Import AnonymousUser
        from django.contrib.auth.models import AnonymousUser
        
        # Create anonymous user
        anonymous_user = AnonymousUser()
        
        # Set up communicator with anonymous user
        communicator = WebsocketCommunicator(
            get_application(anonymous_user),
            "ws/notifications/"
        )
        
        # Try to connect (should close connection)
        connected, _ = await communicator.connect()
        
        # Assert connection was rejected
        assert not connected, "Anonymous user should not be able to connect"
