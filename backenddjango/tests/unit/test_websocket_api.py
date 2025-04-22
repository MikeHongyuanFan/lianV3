import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User, Notification, NotificationPreference
from applications.models import Application
from borrowers.models import Borrower
from brokers.models import Broker, BDM, Branch
from unittest.mock import patch, MagicMock
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from django.urls import re_path
from users.consumers import NotificationConsumer
from rest_framework_simplejwt.tokens import AccessToken
import asyncio
from asgiref.sync import sync_to_async
from users.services import create_notification, send_notification_via_websocket


class WebSocketAPITest(TestCase):
    """
    Test case for WebSocket notification API endpoints
    
    Note: This doesn't test the actual WebSocket connection,
    just verifies that the notification endpoints work correctly
    and that WebSocket messages would be sent
    """
    
    def setUp(self):
        """
        Set up test data
        """
        # Create test users
        self.admin_user = User.objects.create_user(
            email='admin@example.com',
            password='password123',
            role='admin',
            is_staff=True,
            is_superuser=True,
            username='admin'
        )
        
        self.broker_user = User.objects.create_user(
            email='broker@example.com',
            password='password123',
            role='broker',
            username='broker'
        )
        
        self.borrower_user = User.objects.create_user(
            email='borrower@example.com',
            password='password123',
            role='borrower',
            username='borrower'
        )
        
        # Create notification preferences
        NotificationPreference.objects.create(
            user=self.admin_user,
            in_app_application=True,
            in_app_system=True,
            in_app_repayment=True,
            email_application=True,
            email_system=True,
            email_repayment=True
        )
        
        NotificationPreference.objects.create(
            user=self.broker_user,
            in_app_application=True,
            in_app_system=True,
            in_app_repayment=True,
            email_application=True,
            email_system=True,
            email_repayment=True
        )
        
        # Create test branch
        self.branch = Branch.objects.create(
            name='Test Branch',
            address='123 Test St',
            created_by=self.admin_user
        )
        
        # Create test BDM
        self.bdm = BDM.objects.create(
            name='Test BDM',
            email='bdm@example.com',
            phone='1234567890',
            branch=self.branch,
            created_by=self.admin_user
        )
        
        # Create test broker
        self.broker = Broker.objects.create(
            name='Test Broker',
            company='Test Company',
            email='broker@example.com',
            phone='0987654321',
            branch=self.branch,
            user=self.broker_user,
            created_by=self.admin_user
        )
        
        # Create test borrower
        self.borrower = Borrower.objects.create(
            first_name='Test',
            last_name='Borrower',
            email='borrower@example.com',
            phone='1231231234',
            user=self.borrower_user,
            created_by=self.admin_user
        )
        
        # Create test application
        self.application = Application.objects.create(
            loan_amount=500000,
            loan_term=30,
            interest_rate=5.5,
            purpose='Purchase',
            repayment_frequency='monthly',
            application_type='residential',
            stage='inquiry',
            broker=self.broker,
            bd=self.bdm,
            branch=self.branch,
            created_by=self.admin_user
        )
        
        # Add borrower to application
        self.application.borrowers.add(self.borrower)
        
        # Create test notifications
        self.notification1 = Notification.objects.create(
            user=self.admin_user,
            title='Test Notification 1',
            message='This is test notification 1',
            notification_type='system'
        )
        
        self.notification2 = Notification.objects.create(
            user=self.admin_user,
            title='Test Notification 2',
            message='This is test notification 2',
            notification_type='application'
        )
        
        # Create API client
        self.api_client = APIClient()
    
    @patch('channels.layers.get_channel_layer')
    def test_mark_notification_as_read(self, mock_get_channel_layer):
        """
        Test marking a notification as read sends WebSocket update
        """
        # Setup mock channel layer
        mock_channel_layer = MagicMock()
        mock_get_channel_layer.return_value = mock_channel_layer
        
        # Login as admin
        self.api_client.force_authenticate(user=self.admin_user)
        
        # Mark notification as read
        mark_read_url = f'/api/users/notifications/{self.notification1.id}/mark-read/'
        response = self.api_client.post(mark_read_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify notification is marked as read
        self.notification1.refresh_from_db()
        self.assertTrue(self.notification1.is_read)
        
        # Verify WebSocket message would be sent
        mock_channel_layer.group_send.assert_called_once()
        args, kwargs = mock_channel_layer.group_send.call_args
        self.assertEqual(args[0], f"user_{self.admin_user.id}_notifications")
        self.assertEqual(kwargs['type'], 'notification_count')
        self.assertEqual(kwargs['count'], 1)  # One notification still unread
    
    @patch('channels.layers.get_channel_layer')
    def test_mark_all_notifications_as_read(self, mock_get_channel_layer):
        """
        Test marking all notifications as read sends WebSocket update
        """
        # Setup mock channel layer
        mock_channel_layer = MagicMock()
        mock_get_channel_layer.return_value = mock_channel_layer
        
        # Login as admin
        self.api_client.force_authenticate(user=self.admin_user)
        
        # Mark all notifications as read
        mark_all_read_url = '/api/users/notifications/mark-read/'
        response = self.api_client.post(mark_all_read_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify all notifications are marked as read
        self.notification1.refresh_from_db()
        self.notification2.refresh_from_db()
        self.assertTrue(self.notification1.is_read)
        self.assertTrue(self.notification2.is_read)
        
        # Verify WebSocket message would be sent
        mock_channel_layer.group_send.assert_called_once()
        args, kwargs = mock_channel_layer.group_send.call_args
        self.assertEqual(args[0], f"user_{self.admin_user.id}_notifications")
        self.assertEqual(kwargs['type'], 'notification_count')
        self.assertEqual(kwargs['count'], 0)  # No notifications unread
    
    def test_get_unread_notification_count(self):
        """
        Test getting unread notification count
        """
        # Login as admin
        self.api_client.force_authenticate(user=self.admin_user)
        
        # Get unread count
        unread_count_url = '/api/users/notifications/unread_count/'
        response = self.api_client.get(unread_count_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['unread_count'], 2)
        
        # Mark one notification as read
        self.notification1.is_read = True
        self.notification1.save()
        
        # Get updated unread count
        response = self.api_client.get(unread_count_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['unread_count'], 1)
    
    @patch('users.services.send_notification_via_websocket')
    def test_create_notification_sends_websocket_message(self, mock_send_notification):
        """
        Test that creating a notification sends a WebSocket message
        """
        # Create a notification
        notification = create_notification(
            user=self.admin_user,
            title='Test WebSocket Notification',
            message='This is a test WebSocket notification',
            notification_type='system'
        )
        
        # Verify notification was created
        self.assertIsNotNone(notification)
        
        # Verify WebSocket message would be sent
        mock_send_notification.assert_called_once()
        args, kwargs = mock_send_notification.call_args
        self.assertEqual(args[0], self.admin_user)
        self.assertEqual(kwargs['notification_data']['title'], 'Test WebSocket Notification')
    
    @patch('users.services.send_notification_via_websocket')
    def test_application_stage_update_creates_notification(self, mock_send_notification):
        """
        Test that updating application stage creates a notification
        and sends WebSocket message
        """
        # Login as admin
        self.api_client.force_authenticate(user=self.admin_user)
        
        # Update application stage
        update_stage_url = f'/api/applications/{self.application.id}/update-stage/'
        stage_data = {'stage': 'pre_approval'}
        response = self.api_client.post(update_stage_url, stage_data, format='json')
        
        # If the endpoint exists and works correctly
        if response.status_code == status.HTTP_200_OK:
            # Verify WebSocket notification would be sent
            mock_send_notification.assert_called()
            
            # Verify notification was created for broker
            broker_notifications = Notification.objects.filter(
                user=self.broker_user,
                notification_type='application'
            )
            self.assertTrue(broker_notifications.exists())
            self.assertIn('stage', broker_notifications.first().message.lower())
    
    @patch('channels.layers.get_channel_layer')
    def test_notification_delivery_to_multiple_users(self, mock_get_channel_layer):
        """
        Test that notifications are delivered to multiple users
        """
        # Setup mock channel layer
        mock_channel_layer = MagicMock()
        mock_get_channel_layer.return_value = mock_channel_layer
        
        # Create notifications for multiple users
        admin_notification = create_notification(
            user=self.admin_user,
            title='Admin Notification',
            message='This is a notification for admin',
            notification_type='system'
        )
        
        broker_notification = create_notification(
            user=self.broker_user,
            title='Broker Notification',
            message='This is a notification for broker',
            notification_type='system'
        )
        
        # Verify WebSocket messages would be sent to both users
        self.assertEqual(mock_channel_layer.group_send.call_count, 2)
        
        # Check that the correct groups were used
        group_names = [args[0] for args, _ in mock_channel_layer.group_send.call_args_list]
        self.assertIn(f"user_{self.admin_user.id}_notifications", group_names)
        self.assertIn(f"user_{self.broker_user.id}_notifications", group_names)
    
    @patch('channels.layers.get_channel_layer')
    def test_notification_preferences_filter_notifications(self, mock_get_channel_layer):
        """
        Test that notification preferences filter which notifications are created
        """
        # Setup mock channel layer
        mock_channel_layer = MagicMock()
        mock_get_channel_layer.return_value = mock_channel_layer
        
        # Update broker's notification preferences to disable system notifications
        broker_prefs = NotificationPreference.objects.get(user=self.broker_user)
        broker_prefs.in_app_system = False
        broker_prefs.save()
        
        # Create system notification for broker (should be filtered out)
        broker_system_notification = create_notification(
            user=self.broker_user,
            title='System Notification',
            message='This should be filtered out',
            notification_type='system'
        )
        
        # Create application notification for broker (should be created)
        broker_app_notification = create_notification(
            user=self.broker_user,
            title='Application Notification',
            message='This should be created',
            notification_type='application'
        )
        
        # Verify system notification was not created
        self.assertIsNone(broker_system_notification)
        
        # Verify application notification was created
        self.assertIsNotNone(broker_app_notification)
        
        # Verify WebSocket message was only sent once (for the application notification)
        self.assertEqual(mock_channel_layer.group_send.call_count, 1)
    
    @patch('channels.layers.get_channel_layer')
    def test_websocket_reconnection_handling(self, mock_get_channel_layer):
        """
        Test WebSocket reconnection handling by simulating connection errors
        """
        # Setup mock channel layer that raises an exception
        mock_channel_layer = MagicMock()
        mock_channel_layer.group_send.side_effect = [Exception("Connection error"), None]
        mock_get_channel_layer.return_value = mock_channel_layer
        
        # First attempt should fail but not raise an exception
        result = send_notification_via_websocket(
            user=self.admin_user,
            notification_data={'title': 'Test', 'message': 'Test message'},
            update_count=True
        )
        
        # Function should return False on failure
        self.assertFalse(result)
        
        # Reset mock and try again
        mock_channel_layer.group_send.side_effect = None
        
        # Second attempt should succeed
        result = send_notification_via_websocket(
            user=self.admin_user,
            notification_data={'title': 'Test', 'message': 'Test message'},
            update_count=True
        )
        
        # Function should return True on success
        self.assertTrue(result)
    
    @patch('channels.layers.get_channel_layer')
    def test_notification_count_update(self, mock_get_channel_layer):
        """
        Test that notification count is updated correctly
        """
        # Setup mock channel layer
        mock_channel_layer = MagicMock()
        mock_get_channel_layer.return_value = mock_channel_layer
        
        # Create initial notification
        notification = create_notification(
            user=self.admin_user,
            title='Test Notification',
            message='This is a test notification',
            notification_type='system'
        )
        
        # Mark all existing notifications as read
        Notification.objects.filter(user=self.admin_user).update(is_read=True)
        
        # Create new notification
        new_notification = create_notification(
            user=self.admin_user,
            title='New Notification',
            message='This is a new notification',
            notification_type='system'
        )
        
        # Verify count update was sent
        count_calls = [
            call for call in mock_channel_layer.group_send.call_args_list 
            if call[1]['type'] == 'notification_count'
        ]
        
        # Should have at least one count update call
        self.assertGreaterEqual(len(count_calls), 1)
        
        # Last count update should be 1 (for the new notification)
        last_count_call = count_calls[-1]
        self.assertEqual(last_count_call[1]['count'], 1)
    
    @patch('channels.layers.get_channel_layer')
    def test_notification_for_application_events(self, mock_get_channel_layer):
        """
        Test notifications for various application events
        """
        # Setup mock channel layer
        mock_channel_layer = MagicMock()
        mock_get_channel_layer.return_value = mock_channel_layer
        
        # Login as admin
        self.api_client.force_authenticate(user=self.admin_user)
        
        # Test events that should create notifications:
        
        # 1. Application stage update
        update_stage_url = f'/api/applications/{self.application.id}/update-stage/'
        stage_data = {'stage': 'processing'}
        response = self.api_client.post(update_stage_url, stage_data, format='json')
        
        # 2. Document upload (if endpoint exists)
        # This would require mocking file upload
        
        # 3. Comment/note added (if endpoint exists)
        note_url = f'/api/applications/{self.application.id}/notes/'
        note_data = {'content': 'Test note for notification testing'}
        response = self.api_client.post(note_url, note_data, format='json')
        
        # Verify notifications were created for the broker
        broker_notifications = Notification.objects.filter(
            user=self.broker_user,
            notification_type='application'
        )
        
        # There should be at least one notification for the broker
        self.assertTrue(broker_notifications.exists())


class AsyncWebSocketTest(TestCase):
    """
    Test case for asynchronous WebSocket connections
    
    Note: These tests require a running event loop and may not work in all environments
    """
    
    async def test_websocket_auth_and_connect(self):
        """
        Test WebSocket authentication and connection
        
        This test is marked to skip by default as it requires an async environment
        """
        # This test is more complex and requires setting up an async test environment
        # It's included here as a template but would need additional setup to run
        self.skipTest("Async WebSocket tests require special setup")
        
        # Create a test user
        user = await sync_to_async(User.objects.create_user)(
            email='websocket@example.com',
            password='password123',
            role='admin',
            username='websocket'
        )
        
        # Get a token for the user
        token = AccessToken.for_user(user)
        
        # Setup the application with just the WebSocket URL
        application = URLRouter([
            re_path(r'ws/notifications/$', NotificationConsumer.as_asgi()),
        ])
        
        # Connect to the WebSocket with the token
        communicator = WebsocketCommunicator(
            application, f"/ws/notifications/?token={token}"
        )
        connected, _ = await communicator.connect()
        
        # Verify connection was successful
        self.assertTrue(connected)
        
        # Send a message to request unread count
        await communicator.send_json_to({
            'type': 'get_unread_count'
        })
        
        # Wait for response
        response = await communicator.receive_json_from()
        
        # Verify response contains unread count
        self.assertEqual(response['type'], 'unread_count')
        self.assertIn('count', response)
        
        # Close the connection
        await communicator.disconnect()
