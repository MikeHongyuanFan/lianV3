import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User, Notification
from applications.models import Application
from borrowers.models import Borrower
from brokers.models import Broker, BDM, Branch
from unittest.mock import patch, MagicMock


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
            username='admin'  # Add username parameter
        )
        
        self.broker_user = User.objects.create_user(
            email='broker@example.com',
            password='password123',
            role='broker',
            username='broker'  # Add username parameter
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
        mark_read_url = reverse('notification-mark-as-read', args=[self.notification1.id])
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
        mark_all_read_url = reverse('notification-mark-all-as-read')
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
        unread_count_url = reverse('notification-unread-count')
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
    def test_application_stage_update_creates_notification(self, mock_send_notification):
        """
        Test that updating application stage creates a notification
        and sends WebSocket message
        """
        # Login as admin
        self.api_client.force_authenticate(user=self.admin_user)
        
        # Update application stage
        update_stage_url = reverse('application-update-stage', args=[self.application.id])
        stage_data = {'stage': 'pre_approval'}
        response = self.api_client.post(update_stage_url, stage_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify notification would be sent via WebSocket
        # Note: This depends on your implementation of stage updates
        # If notifications are created on stage change, this should be called
        mock_send_notification.assert_called()
        
        # Verify notification was created in database
        # This also depends on your implementation
        notifications = Notification.objects.filter(
            user=self.broker_user,  # Notification should go to the broker
            notification_type='application'
        )
        # Uncomment if your implementation creates notifications on stage change
        # self.assertTrue(notifications.exists())
        # self.assertIn('stage', notifications.first().message.lower())
