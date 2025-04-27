import pytest
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from crm_backend.asgi import application
import json

User = get_user_model()

@pytest.mark.asyncio
async def test_websocket_auth_middleware():
    """Test that the WebSocket authentication middleware works correctly"""
    # Create a user
    user = User.objects.create_user(
        username='authuser',
        email='authuser@example.com',
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
    
    # Send a message to check if the user is authenticated
    await communicator.send_json_to({
        'type': 'get_user_info'
    })
    
    # Receive the response
    response = await communicator.receive_json_from()
    
    # Check that the user info is correct
    assert response['user_id'] == user.id
    assert response['email'] == user.email
    
    # Close the connection
    await communicator.disconnect()

@pytest.mark.asyncio
async def test_websocket_token_expiration():
    """Test that an expired token is rejected"""
    # Create a user
    user = User.objects.create_user(
        username='expireduser',
        email='expireduser@example.com',
        password='password123',
        role='client'
    )
    
    # Generate a token for the user with a very short lifetime
    from datetime import timedelta
    
    # Create a token that expires immediately
    refresh = RefreshToken.for_user(user)
    refresh.access_token.set_exp(lifetime=timedelta(seconds=0))
    token = str(refresh.access_token)
    
    # Connect to the WebSocket with the expired token
    communicator = WebsocketCommunicator(
        application=application,
        path=f'/ws/notifications/?token={token}'
    )
    connected, _ = await communicator.connect()
    
    # Check that the connection was rejected
    assert not connected

@pytest.mark.asyncio
async def test_websocket_user_specific_groups():
    """Test that users are added to their specific notification groups"""
    # Create two users
    user1 = User.objects.create_user(
        username='user1',
        email='user1@example.com',
        password='password123',
        role='client'
    )
    
    user2 = User.objects.create_user(
        username='user2',
        email='user2@example.com',
        password='password123',
        role='client'
    )
    
    # Generate tokens for both users
    token1 = str(RefreshToken.for_user(user1).access_token)
    token2 = str(RefreshToken.for_user(user2).access_token)
    
    # Connect both users to the WebSocket
    communicator1 = WebsocketCommunicator(
        application=application,
        path=f'/ws/notifications/?token={token1}'
    )
    connected1, _ = await communicator1.connect()
    assert connected1
    
    communicator2 = WebsocketCommunicator(
        application=application,
        path=f'/ws/notifications/?token={token2}'
    )
    connected2, _ = await communicator2.connect()
    assert connected2
    
    # Send a notification to user1's group
    from channels.layers import get_channel_layer
    
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        f"user_{user1.id}_notifications",
        {
            'type': 'notification_message',
            'message': {
                'title': 'User1 Notification',
                'message': 'This is for user1 only',
                'notification_type': 'test'
            }
        }
    )
    
    # User1 should receive the notification
    response1 = await communicator1.receive_json_from()
    assert response1['title'] == 'User1 Notification'
    
    # User2 should not receive any message (would timeout)
    import asyncio
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(communicator2.receive_json_from(), timeout=0.5)
    
    # Close the connections
    await communicator1.disconnect()
    await communicator2.disconnect()
