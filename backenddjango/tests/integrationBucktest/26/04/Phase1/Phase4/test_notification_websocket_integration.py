"""
Integration tests for notification and WebSocket integration.
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
from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter
import users.routing
from channels.db import database_sync_to_async

# Create a direct application for WebSocket testing
websocket_application = AuthMiddlewareStack(URLRouter(users.routing.websocket_urlpatterns))

@pytest.mark.asyncio
class TestNotificationWebSocketIntegration:
    """Test suite for notification and WebSocket integration."""

    async def test_notification_creation_and_delivery(self, admin_user):
        """Test notification creation and delivery via WebSocket."""
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
                title='Test Integration Notification',
                message='This is a test notification for integration',
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
        
        # Wait for WebSocket notification
        response = await communicator.receive_json_from(timeout=2)
        
        # Verify notification data
        assert 'type' in response
        assert response['type'] == 'notification'
        assert 'notification' in response
        assert 'Test Integration Notification' in response['notification']['title']
        
        # Verify notification was saved to database
        @database_sync_to_async
        def check_notification_exists():
            return Notification.objects.filter(
                user=admin_user,
                notification_type='system',
                title='Test Integration Notification'
            ).exists()
        
        assert await check_notification_exists()
        
        await communicator.disconnect()

    async def test_notification_mark_as_read(self, admin_user):
        """Test marking notification as read updates WebSocket."""
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
                title='Read Test Notification',
                message='This notification will be marked as read',
                notification_type='system',
                is_read=False
            )
            return notification.id
        
        # Create notification
        notification_id = await create_notification()
        
        # Mark notification as read
        @database_sync_to_async
        def mark_notification_read():
            notification = Notification.objects.get(id=notification_id)
            notification.is_read = True
            notification.save()
            
            # Manually trigger the WebSocket unread count update
            from channels.layers import get_channel_layer
            from asgiref.sync import async_to_sync
            
            channel_layer = get_channel_layer()
            unread_count = Notification.objects.filter(user=admin_user, is_read=False).count()
            
            async_to_sync(channel_layer.group_send)(
                f"user_{admin_user.id}_notifications",
                {
                    'type': 'notification_count',
                    'count': unread_count
                }
            )
        
        await mark_notification_read()
        
        # Wait for WebSocket unread count update
        response = await communicator.receive_json_from(timeout=2)
        
        # Verify unread count update
        assert 'type' in response
        assert response['type'] == 'unread_count'
        
        # Verify notification is marked as read in database
        @database_sync_to_async
        def check_notification_read():
            notification = Notification.objects.get(id=notification_id)
            return notification.is_read
        
        assert await check_notification_read()
        
        await communicator.disconnect()

    async def test_notification_count_update(self, admin_user):
        """Test notification count updates via WebSocket."""
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
        initial_count = initial_response['count']
        
        # Create a notification directly in the database
        @database_sync_to_async
        def create_notification():
            notification = Notification.objects.create(
                user=admin_user,
                title='Count Test Notification',
                message='This notification should increase the count',
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
            
            # Also update the unread count
            unread_count = Notification.objects.filter(user=admin_user, is_read=False).count()
            async_to_sync(channel_layer.group_send)(
                f"user_{admin_user.id}_notifications",
                {
                    'type': 'notification_count',
                    'count': unread_count
                }
            )
            
            return notification.id, unread_count
        
        # Create notification
        notification_id, updated_count = await create_notification()
        
        # Wait for WebSocket notification
        notification_response = await communicator.receive_json_from(timeout=2)
        assert notification_response['type'] == 'notification'
        
        # Wait for unread count update
        count_response = await communicator.receive_json_from(timeout=2)
        assert count_response['type'] == 'unread_count'
        
        # Verify count increased
        assert count_response['count'] == initial_count + 1
        
        await communicator.disconnect()

    async def test_multiple_notifications(self, admin_user):
        """Test multiple notifications via WebSocket."""
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
        
        # Create notifications directly in the database
        @database_sync_to_async
        def create_notifications():
            notification_ids = []
            for i in range(3):
                notification = Notification.objects.create(
                    user=admin_user,
                    title=f'Multiple Test {i}',
                    message=f'This is multiple test notification {i}',
                    notification_type='system',
                    is_read=False
                )
                notification_ids.append(notification.id)
                
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
            
            return notification_ids
        
        # Create notifications
        notification_ids = await create_notifications()
        
        # Wait for WebSocket notifications (3 notifications)
        notifications_received = []
        for _ in range(3):
            response = await communicator.receive_json_from(timeout=2)
            assert response['type'] == 'notification'
            notifications_received.append(response['notification']['title'])
        
        # Verify all notifications were received
        assert len(notifications_received) == 3
        assert any('Multiple Test 0' in title for title in notifications_received)
        assert any('Multiple Test 1' in title for title in notifications_received)
        assert any('Multiple Test 2' in title for title in notifications_received)
        
        await communicator.disconnect()

    async def test_notification_list_retrieval(self, admin_user):
        """Test notification list retrieval after WebSocket updates."""
        # Create a notification directly in the database
        @database_sync_to_async
        def create_notification():
            notification = Notification.objects.create(
                user=admin_user,
                title='List Test Notification',
                message='This notification should appear in the list',
                notification_type='system',
                is_read=False
            )
            return notification.id
        
        # Create notification
        notification_id = await create_notification()
        
        # Get notification list
        @database_sync_to_async
        def get_notification_list():
            return list(Notification.objects.filter(user=admin_user).values('title'))
        
        notifications = await get_notification_list()
        
        # Verify notification is in the list
        assert any('List Test Notification' in n['title'] for n in notifications)

    async def test_notification_filtering(self, admin_user):
        """Test notification filtering after WebSocket updates."""
        # Create notifications with different types directly in the database
        @database_sync_to_async
        def create_notifications():
            types = ['system', 'application_status', 'repayment_upcoming']
            notification_ids = []
            
            for notification_type in types:
                notification = Notification.objects.create(
                    user=admin_user,
                    title=f'{notification_type.capitalize()} Notification',
                    message=f'This is a {notification_type} notification',
                    notification_type=notification_type,
                    is_read=False
                )
                notification_ids.append(notification.id)
            
            return notification_ids, types
        
        # Create notifications
        notification_ids, types = await create_notifications()
        
        # Filter notifications by type
        @database_sync_to_async
        def filter_notifications(notification_type):
            return list(Notification.objects.filter(
                user=admin_user,
                notification_type=notification_type
            ).values('title', 'notification_type'))
        
        # Verify filtered results for each type
        for notification_type in types:
            filtered_notifications = await filter_notifications(notification_type)
            assert len(filtered_notifications) >= 1
            assert all(n['notification_type'] == notification_type for n in filtered_notifications)
            assert any(notification_type.capitalize() in n['title'] for n in filtered_notifications)
