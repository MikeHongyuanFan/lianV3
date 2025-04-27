import pytest
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from crm_backend.asgi import application
import json

User = get_user_model()

@pytest.mark.asyncio
async def test_websocket_connect_with_valid_token():
    """Test that a user can connect to the WebSocket with a valid token"""
    # Create a user
    user = User.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='password123',
        role='client'
    )
    
    # Generate a token for the user
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)
    
    # Connect to the WebSocket with the token
    communicator = WebsocketCommunicator(
        application=application,
        path=f'/ws/notifications/?token={token}'
    )
    connected, _ = await communicator.connect()
    
    # Check that the connection was accepted
    assert connected
    
    # Close the connection
    await communicator.disconnect()

@pytest.mark.asyncio
async def test_websocket_connect_with_invalid_token():
    """Test that a user cannot connect to the WebSocket with an invalid token"""
    # Connect to the WebSocket with an invalid token
    communicator = WebsocketCommunicator(
        application=application,
        path='/ws/notifications/?token=invalid_token'
    )
    connected, _ = await communicator.connect()
    
    # Check that the connection was rejected
    assert not connected

@pytest.mark.asyncio
async def test_websocket_receive_notification():
    """Test that a user can receive a notification through the WebSocket"""
    # Create a user
    user = User.objects.create_user(
        username='notifyuser',
        email='notifyuser@example.com',
        password='password123',
        role='client'
    )
    
    # Generate a token for the user
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)
    
    # Connect to the WebSocket with the token
    communicator = WebsocketCommunicator(
        application=application,
        path=f'/ws/notifications/?token={token}'
    )
    connected, _ = await communicator.connect()
    assert connected
    
    # Send a notification to the user's group
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync
    
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        f"user_{user.id}_notifications",
        {
            'type': 'notification_message',
            'message': {
                'title': 'Test Notification',
                'message': 'This is a test notification',
                'notification_type': 'test'
            }
        }
    )
    
    # Receive the notification
    response = await communicator.receive_json_from()
    
    # Check the notification content
    assert response['title'] == 'Test Notification'
    assert response['message'] == 'This is a test notification'
    assert response['notification_type'] == 'test'
    
    # Close the connection
    await communicator.disconnect()
