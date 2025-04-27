"""
Tests for notification filtering functionality
"""
from django.test import TestCase
from users.models import User, Notification
from users.filters import NotificationFilter
from django.utils import timezone
from datetime import timedelta


class NotificationFilterTests(TestCase):
    """
    Test cases for notification filter functionality
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
        
        # Create test notifications with different dates
        now = timezone.now()
        yesterday = now - timedelta(days=1)
        last_week = now - timedelta(days=7)
        
        # Create notifications
        self.notifications = [
            # Application notification
            Notification.objects.create(
                user=self.user,
                title='Application Status Update',
                message='Your application #12345 has been approved',
                notification_type='application_status',
                is_read=False,
                created_at=now
            ),
            # Repayment notification
            Notification.objects.create(
                user=self.user,
                title='Repayment Reminder',
                message='Your repayment of $500 is due tomorrow',
                notification_type='repayment_upcoming',
                is_read=False,
                created_at=yesterday
            ),
            # Document notification
            Notification.objects.create(
                user=self.user,
                title='Document Required',
                message='Please upload your bank statements',
                notification_type='document_uploaded',
                is_read=True,
                created_at=last_week
            )
        ]
    
    def test_filter_by_search_term(self):
        """
        Test filtering by search term
        """
        # Create filter instance
        f = NotificationFilter({'search': 'application'}, queryset=Notification.objects.all())
        results = f.qs
        
        # Should find one notification with 'application' in title or message
        self.assertEqual(results.count(), 1)
        self.assertEqual(results[0].title, 'Application Status Update')
        
        # Test multiple terms
        f = NotificationFilter({'search': 'repayment due'}, queryset=Notification.objects.all())
        results = f.qs
        
        # Should find one notification with both terms
        self.assertEqual(results.count(), 1)
        self.assertEqual(results[0].title, 'Repayment Reminder')
    
    def test_filter_by_notification_type(self):
        """
        Test filtering by notification type
        """
        # Filter by application_status
        f = NotificationFilter({'notification_type': 'application_status'}, queryset=Notification.objects.all())
        results = f.qs
        
        # Should get only application notifications
        self.assertEqual(results.count(), 1)
        self.assertEqual(results[0].notification_type, 'application_status')
    
    def test_filter_by_read_status(self):
        """
        Test filtering by read status
        """
        # Filter by unread
        f = NotificationFilter({'is_read': False}, queryset=Notification.objects.all())
        results = f.qs
        
        # Should get only unread notifications
        self.assertEqual(results.count(), 2)
        for notification in results:
            self.assertFalse(notification.is_read)
        
        # Filter by read
        f = NotificationFilter({'is_read': True}, queryset=Notification.objects.all())
        results = f.qs
        
        # Should get only read notifications
        self.assertEqual(results.count(), 1)
        self.assertTrue(results[0].is_read)
    
    def test_combined_filters(self):
        """
        Test combining multiple filters
        """
        # Combine notification type and read status
        f = NotificationFilter({
            'notification_type': 'document_uploaded',
            'is_read': True
        }, queryset=Notification.objects.all())
        results = f.qs
        
        # Should get only the document notification
        self.assertEqual(results.count(), 1)
        self.assertEqual(results[0].title, 'Document Required')
        self.assertTrue(results[0].is_read)
