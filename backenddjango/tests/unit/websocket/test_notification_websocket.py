import pytest
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from crm_backend.asgi import application
import json
from users.models import Notification

User = get_user_model()

@pytest.mark.asyncio
async def test_notification_creation_triggers_websocket():
    """Test that creating a notification sends a WebSocket message"""
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
    
    # Create a notification for the user
    notification = Notification.objects.create(
        user=user,
        title="Test Notification",
        message="This is a test notification",
        notification_type="application_status",
        related_object_id=1,
        related_object_type="application"
    )
    
    # Receive the notification through WebSocket
    response = await communicator.receive_json_from()
    
    # Check the notification content
    assert 'notification' in response
    assert response['notification']['title'] == "Test Notification"
    assert response['notification']['message'] == "This is a test notification"
    
    # Close the connection
    await communicator.disconnect()

@pytest.mark.asyncio
async def test_mark_notification_as_read_updates_count():
    """Test that marking a notification as read updates the unread count via WebSocket"""
    # Create a user
    user = User.objects.create_user(
        username='readuser',
        email='readuser@example.com',
        password='password123',
        role='client'
    )
    
    # Create some notifications for the user
    notification1 = Notification.objects.create(
        user=user,
        title="Notification 1",
        message="This is notification 1",
        notification_type="application_status",
        related_object_id=1,
        related_object_type="application"
    )
    
    notification2 = Notification.objects.create(
        user=user,
        title="Notification 2",
        message="This is notification 2",
        notification_type="document_uploaded",
        related_object_id=2,
        related_object_type="document"
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
    
    # Mark one notification as read
    notification1.is_read = True
    notification1.save()
    
    # Receive the unread count update
    response = await communicator.receive_json_from()
    
    # Check the unread count
    assert 'unread_count' in response
    assert response['unread_count'] == 1
    
    # Close the connection
    await communicator.disconnect()

@pytest.mark.asyncio
async def test_notification_filtering_by_type():
    """Test that notifications can be filtered by type"""
    # Create a user
    user = User.objects.create_user(
        username='filteruser',
        email='filteruser@example.com',
        password='password123',
        role='client'
    )
    
    # Create notifications of different types
    notification1 = Notification.objects.create(
        user=user,
        title="Application Status",
        message="Application status changed",
        notification_type="application_status",
        related_object_id=1,
        related_object_type="application"
    )
    
    notification2 = Notification.objects.create(
        user=user,
        title="Document Uploaded",
        message="A document was uploaded",
        notification_type="document_uploaded",
        related_object_id=2,
        related_object_type="document"
    )
    
    # Generate a token for the user
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)
    
    # Connect to the WebSocket with the token
    communicator = WebsocketCommunicator(
        application=application,
        path=f'/ws/notifications/?token={token}&notification_type=application_status'
    )
    connected, _ = await communicator.connect()
    assert connected
    
    # Create another application status notification
    notification3 = Notification.objects.create(
        user=user,
        title="Another Status Change",
        message="Application status changed again",
        notification_type="application_status",
        related_object_id=3,
        related_object_type="application"
    )
    
    # Receive the notification through WebSocket
    response = await communicator.receive_json_from()
    
    # Check that we received only the application status notification
    assert 'notification' in response
    assert response['notification']['title'] == "Another Status Change"
    assert response['notification']['notification_type'] == "application_status"
    
    # Close the connection
    await communicator.disconnect()
