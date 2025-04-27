"""
Integration tests for WebSocket API functionality.
"""
import pytest
import json
import asyncio
from channels.testing import WebsocketCommunicator
from django.urls import reverse
from rest_framework import status
from users.models import Notification
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter
import users.routing
from users.websocket_auth import JWTAuthMiddleware

# Create a direct application for WebSocket testing
websocket_application = JWTAuthMiddleware(
    AuthMiddlewareStack(
        URLRouter(users.routing.websocket_urlpatterns)
    )
)

@pytest.mark.asyncio
class TestWebSocketAPI:
    """Test suite for WebSocket API functionality."""

    async def test_websocket_connection_authentication(self, admin_user, broker_user, client_user):
        """Test WebSocket connection authentication."""
        # Get tokens for each user
        admin_token = str(RefreshToken.for_user(admin_user).access_token)
        broker_token = str(RefreshToken.for_user(broker_user).access_token)
        client_token = str(RefreshToken.for_user(client_user).access_token)
        
        # Test valid connection with admin token
        admin_communicator = WebsocketCommunicator(
            websocket_application,
            f"ws/notifications/?token={admin_token}"
        )
        connected, _ = await admin_communicator.connect()
        assert connected
        await admin_communicator.disconnect()
        
        # Test valid connection with broker token
        broker_communicator = WebsocketCommunicator(
            websocket_application,
            f"ws/notifications/?token={broker_token}"
        )
        connected, _ = await broker_communicator.connect()
        assert connected
        await broker_communicator.disconnect()
        
        # Test valid connection with client token
        client_communicator = WebsocketCommunicator(
            websocket_application,
            f"ws/notifications/?token={client_token}"
        )
        connected, _ = await client_communicator.connect()
        assert connected
        await client_communicator.disconnect()
        
        # Test invalid connection with invalid token
        invalid_communicator = WebsocketCommunicator(
            websocket_application,
            "ws/notifications/?token=invalid_token"
        )
        connected, _ = await invalid_communicator.connect()
        assert not connected

    async def test_websocket_connection_without_token(self):
        """Test WebSocket connection without token."""
        communicator = WebsocketCommunicator(
            websocket_application,
            "ws/notifications/"
        )
        connected, _ = await communicator.connect()
        assert not connected

    async def test_notification_delivery(self, admin_user):
        """Test notification delivery via WebSocket."""
        # Create a WebSocket connection
        admin_token = str(RefreshToken.for_user(admin_user).access_token)
        communicator = WebsocketCommunicator(
            websocket_application,
            f"ws/notifications/?token={admin_token}"
        )
        connected, _ = await communicator.connect()
        assert connected
        
        # Receive initial unread count
        initial_response = await communicator.receive_json_from(timeout=2)
        
        # Create a notification directly in the database
        @database_sync_to_async
        def create_notification():
            notification = Notification.objects.create(
                user=admin_user,
                title='Test Notification',
                message='This is a test notification',
                notification_type='system',
                is_read=False
            )
            
            # Manually trigger the WebSocket notification
            from channels.layers import get_channel_layer
            from asgiref.sync import async_to_sync
            
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{admin_user.id}_notifications",
                {
                    'type': 'notification_message',
                    'notification': {
                        'id': notification.id,
                        'title': notification.title,
                        'message': notification.message,
                        'notification_type': notification.notification_type,
                        'is_read': notification.is_read,
                        'created_at': notification.created_at.isoformat()
                    }
                }
            )
            
            return notification.id
        
        # Create notification
        notification_id = await create_notification()
        
        # Wait for WebSocket message
        response = await communicator.receive_json_from(timeout=2)
        
        # Verify notification data
        assert 'type' in response
        assert response['type'] == 'notification'
        assert 'notification' in response
        assert response['notification']['title'] == 'Test Notification'
        assert response['notification']['message'] == 'This is a test notification'
        assert response['notification']['notification_type'] == 'system'
        
        await communicator.disconnect()

    async def test_websocket_token_expiry(self, admin_user):
        """Test WebSocket connection with expired token."""
        # Create an expired token (this is a simplified simulation)
        from rest_framework_simplejwt.tokens import RefreshToken
        import datetime
        
        refresh = RefreshToken.for_user(admin_user)
        access_token = refresh.access_token
        access_token.set_exp(lifetime=datetime.timedelta(seconds=0))
        expired_token = str(access_token)
        
        # Try to connect with expired token
        await asyncio.sleep(1)  # Ensure token is expired
        communicator = WebsocketCommunicator(
            websocket_application,
            f"ws/notifications/?token={expired_token}"
        )
        connected, _ = await communicator.connect()
        assert not connected
