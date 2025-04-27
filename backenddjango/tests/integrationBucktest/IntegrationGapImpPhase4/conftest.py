"""
Pytest configuration and fixtures for WebSocket integration tests.
"""
import pytest
import asyncio
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from users.models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

User = get_user_model()


@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


class Helpers:
    """Helper methods for tests."""
    
    @staticmethod
    @database_sync_to_async
    def create_user(username, email, password, role):
        """Create a user for testing."""
        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )
    
    @staticmethod
    @database_sync_to_async
    def create_notification(user, title, message, notification_type, related_object_id=None, related_object_type=None):
        """Create a notification for testing."""
        notification = Notification.objects.create(
            user=user,
            title=title,
            message=message,
            notification_type=notification_type,
            related_object_id=related_object_id,
            related_object_type=related_object_type,
            is_read=False
        )
        
        # Send real-time notification via WebSocket
        try:
            channel_layer = get_channel_layer()
            notification_data = {
                'id': notification.id,
                'title': notification.title,
                'message': notification.message,
                'notification_type': notification.notification_type,
                'related_object_id': notification.related_object_id,
                'related_object_type': notification.related_object_type,
                'is_read': notification.is_read,
                'created_at': notification.created_at.isoformat()
            }
            
            # Send notification to user's group
            async_to_sync(channel_layer.group_send)(
                f"user_{user.id}_notifications",
                {
                    'type': 'notification_message',
                    'notification': notification_data
                }
            )
            
            # Update unread count
            unread_count = Notification.objects.filter(user=user, is_read=False).count()
            async_to_sync(channel_layer.group_send)(
                f"user_{user.id}_notifications",
                {
                    'type': 'notification_count',
                    'count': unread_count
                }
            )
        except Exception as e:
            print(f"Error sending WebSocket notification: {str(e)}")
        
        return notification.id
    
    @staticmethod
    @database_sync_to_async
    def mark_notification_as_read(notification_id):
        """Mark a notification as read."""
        notification = Notification.objects.get(id=notification_id)
        notification.mark_as_read()
        
        # Send unread count update
        try:
            channel_layer = get_channel_layer()
            unread_count = Notification.objects.filter(user=notification.user, is_read=False).count()
            async_to_sync(channel_layer.group_send)(
                f"user_{notification.user.id}_notifications",
                {
                    'type': 'notification_count',
                    'count': unread_count
                }
            )
        except Exception as e:
            print(f"Error sending WebSocket notification count: {str(e)}")
        
        return True
    
    @staticmethod
    @database_sync_to_async
    def mark_all_notifications_as_read(user_id):
        """Mark all notifications as read for a user."""
        user = User.objects.get(id=user_id)
        notifications = Notification.objects.filter(user=user, is_read=False)
        for notification in notifications:
            notification.mark_as_read()
        
        # Send unread count update
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{user.id}_notifications",
                {
                    'type': 'notification_count',
                    'count': 0
                }
            )
        except Exception as e:
            print(f"Error sending WebSocket notification count: {str(e)}")
        
        return True


@pytest.fixture
def helpers():
    """Provide helpers to tests."""
    return Helpers
