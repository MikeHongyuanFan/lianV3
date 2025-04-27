"""
Tests for notification search and filtering functionality
"""
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User, Notification
import json


class NotificationSearchTests(APITestCase):
    """
    Test cases for notification search and filtering functionality
    """
    
    def setUp(self):
        """
        Set up test data
        """
        # Create test user
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword',
            username='testuser',
            first_name='Test',
            last_name='User',
            role='client'
        )
        
        # Create another user to test isolation
        self.other_user = User.objects.create_user(
            email='other@example.com',
            password='otherpassword',
            username='otheruser',
            first_name='Other',
            last_name='User',
            role='client'
        )
        
        # Create test notifications with different dates
        now = timezone.now()
        yesterday = now - timedelta(days=1)
        last_week = now - timedelta(days=7)
        last_month = now - timedelta(days=30)
        
        # Create notifications for main test user
        self.notifications = [
            # Recent notification about application
            Notification.objects.create(
                user=self.user,
                title='Application Status Update',
                message='Your application #12345 has been approved by the loan committee',
                notification_type='application_status',
                related_object_id=12345,
                related_object_type='application',
                is_read=False,
                created_at=now
            ),
            # Yesterday's notification about repayment
            Notification.objects.create(
                user=self.user,
                title='Repayment Reminder',
                message='Your repayment of $500 is due tomorrow',
                notification_type='repayment_upcoming',
                related_object_id=67890,
                related_object_type='repayment',
                is_read=False,
                created_at=yesterday
            ),
            # Last week's notification about documents
            Notification.objects.create(
                user=self.user,
                title='Document Required',
                message='Please upload your bank statements for loan processing',
                notification_type='document_uploaded',
                related_object_id=54321,
                related_object_type='document',
                is_read=True,
                created_at=last_week
            ),
            # Last month's notification about signature
            Notification.objects.create(
                user=self.user,
                title='Signature Required',
                message='Please sign the loan agreement document',
                notification_type='signature_required',
                related_object_id=98765,
                related_object_type='document',
                is_read=True,
                created_at=last_month
            ),
            # System notification
            Notification.objects.create(
                user=self.user,
                title='System Maintenance',
                message='The system will be down for maintenance on Sunday',
                notification_type='system',
                is_read=False,
                created_at=now
            )
        ]
        
        # Create notifications for other user (to test isolation)
        Notification.objects.create(
            user=self.other_user,
            title='Other User Notification',
            message='This should not appear in search results',
            notification_type='system',
            is_read=False,
            created_at=now
        )
        
        # Authenticate the client
        self.client.force_authenticate(user=self.user)
        
        # Define common URLs
        self.list_url = '/api/users/notifications/'
    
    def test_list_all_notifications(self):
        """
        Test listing all notifications for the user
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 5)  # Should see all 5 notifications
    
    def test_basic_search(self):
        """
        Test basic search functionality
        """
        # Search for 'application'
        response = self.client.get(f"{self.list_url}?search=application")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        
        # Check if any notification contains 'application' in title
        found = False
        for item in data:
            if 'application' in item['title'].lower():
                found = True
                break
        self.assertTrue(found, "Should find at least one notification with 'application'")
    
    def test_filter_by_notification_type(self):
        """
        Test filtering by notification type
        """
        # Filter by application_status
        response = self.client.get(f"{self.list_url}?notification_type=application_status")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        
        # Check if all returned notifications have the correct type
        for item in data:
            self.assertEqual(item['notification_type'], 'application_status')
    
    def test_filter_by_read_status(self):
        """
        Test filtering by read status
        """
        # Filter by unread
        response = self.client.get(f"{self.list_url}?is_read=false")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        
        # Check if all returned notifications are unread
        for item in data:
            self.assertFalse(item['is_read'])
        
        # Filter by read
        response = self.client.get(f"{self.list_url}?is_read=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        
        # Check if all returned notifications are read
        for item in data:
            self.assertTrue(item['is_read'])
    
    def test_combined_basic_filters(self):
        """
        Test combining multiple basic filters
        """
        # Combine type and read status
        response = self.client.get(f"{self.list_url}?notification_type=document_uploaded&is_read=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        
        # Check if all returned notifications match both criteria
        for item in data:
            self.assertEqual(item['notification_type'], 'document_uploaded')
            self.assertTrue(item['is_read'])
    
    def test_user_isolation(self):
        """
        Test that users can only see their own notifications
        """
        # Get all notifications for current user
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        
        # Verify no notifications from other_user are visible
        for item in data:
            self.assertNotEqual(item['title'], 'Other User Notification')
        
        # Switch to other user
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        
        # Should only see their notification
        self.assertEqual(data[0]['title'], 'Other User Notification')
