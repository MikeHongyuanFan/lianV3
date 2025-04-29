import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User, Notification
from datetime import datetime, timedelta

@pytest.mark.django_db
class TestNotificationViewSet:
    """Tests for the NotificationViewSet"""
    
    def test_list_notifications(self, api_client, user):
        """Test listing notifications"""
        # Create some notifications for the user
        Notification.objects.create(
            user=user,
            title="Test Notification 1",
            message="This is a test notification",
            notification_type="application_status"
        )
        Notification.objects.create(
            user=user,
            title="Test Notification 2",
            message="This is another test notification",
            notification_type="repayment_reminder"
        )
        
        # Authenticate the client
        api_client.force_authenticate(user=user)
        
        # Make the request
        url = reverse('notifications-list')
        response = api_client.get(url)
        
        # Check the response
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2
    
    def test_mark_notification_as_read(self, api_client, user):
        """Test marking a notification as read"""
        # Create a notification
        notification = Notification.objects.create(
            user=user,
            title="Test Notification",
            message="This is a test notification",
            notification_type="application_status",
            is_read=False
        )
        
        # Authenticate the client
        api_client.force_authenticate(user=user)
        
        # Make the request
        url = reverse('notifications-mark-as-read', args=[notification.id])
        response = api_client.post(url)
        
        # Check the response
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'notification marked as read'
        
        # Verify the notification is marked as read
        notification.refresh_from_db()
        assert notification.is_read is True
    
    def test_mark_all_as_read(self, api_client, user):
        """Test marking all notifications as read"""
        # Create some notifications
        Notification.objects.create(
            user=user,
            title="Test Notification 1",
            message="This is a test notification",
            notification_type="application_status",
            is_read=False
        )
        Notification.objects.create(
            user=user,
            title="Test Notification 2",
            message="This is another test notification",
            notification_type="repayment_reminder",
            is_read=False
        )
        
        # Authenticate the client
        api_client.force_authenticate(user=user)
        
        # Make the request
        url = reverse('notifications-mark-all-as-read')
        response = api_client.post(url)
        
        # Check the response
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'all notifications marked as read'
        
        # Verify all notifications are marked as read
        assert Notification.objects.filter(user=user, is_read=False).count() == 0
    
    def test_get_unread_count(self, api_client, user):
        """Test getting unread notification count"""
        # Create some notifications
        Notification.objects.create(
            user=user,
            title="Test Notification 1",
            message="This is a test notification",
            notification_type="application_status",
            is_read=False
        )
        Notification.objects.create(
            user=user,
            title="Test Notification 2",
            message="This is another test notification",
            notification_type="repayment_reminder",
            is_read=False
        )
        Notification.objects.create(
            user=user,
            title="Test Notification 3",
            message="This is a read notification",
            notification_type="application_status",
            is_read=True
        )
        
        # Authenticate the client
        api_client.force_authenticate(user=user)
        
        # Make the request
        url = reverse('notifications-unread-count')
        response = api_client.get(url)
        
        # Check the response
        assert response.status_code == status.HTTP_200_OK
        assert response.data['unread_count'] == 2
    
    def test_advanced_search(self, api_client, user):
        """Test advanced search for notifications"""
        # Create some notifications with different dates
        yesterday = datetime.now() - timedelta(days=1)
        Notification.objects.create(
            user=user,
            title="Old Notification",
            message="This is an old notification",
            notification_type="application_status",
            is_read=False,
            created_at=yesterday
        )
        Notification.objects.create(
            user=user,
            title="New Notification",
            message="This is a new notification",
            notification_type="repayment_reminder",
            is_read=False
        )
        
        # Authenticate the client
        api_client.force_authenticate(user=user)
        
        # Make the request with date filter
        today = datetime.now().strftime('%Y-%m-%d')
        url = reverse('notifications-advanced-search') + f'?date_from={today}'
        response = api_client.get(url)
        
        # Check the response
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == "New Notification"
