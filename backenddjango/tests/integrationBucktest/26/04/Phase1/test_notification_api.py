"""
Integration tests for notification API endpoints.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from users.models import Notification, NotificationPreference
from .common import APITestClient, assert_response_status, assert_response_contains

User = get_user_model()

@pytest.mark.django_db
class TestNotificationAPI:
    """Test notification API endpoints."""
    
    def setup_method(self):
        """Set up test client and data."""
        self.client = APITestClient()
        self.notifications_url = reverse('notifications-list')
        self.mark_read_url = reverse('notification-mark-read')
        self.notification_count_url = reverse('notification-count')
        self.notification_preferences_url = reverse('notification-preferences')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'role': 'client'
        }
    
    def create_notifications(self, user, count=3):
        """Create test notifications for a user."""
        notifications = []
        for i in range(count):
            notification = Notification.objects.create(
                user=user,
                title=f'Test Notification {i+1}',
                message=f'This is test notification {i+1}',
                notification_type='test',
                related_object_id=i+1,
                related_object_type='test'
            )
            notifications.append(notification)
        return notifications
    
    def test_list_notifications(self):
        """Test listing user notifications."""
        # Create a user and authenticate
        user, _ = self.client.create_and_login(**self.user_data)
        
        # Create notifications
        notifications = self.create_notifications(user)
        
        # List notifications
        response = self.client.get(self.notifications_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        data = response.json()
        assert len(data['results']) == len(notifications), f"Expected {len(notifications)} notifications, got {len(data['results'])}"
    
    def test_list_notifications_empty(self):
        """Test listing notifications when there are none."""
        # Create a user and authenticate
        user, _ = self.client.create_and_login(**self.user_data)
        
        # List notifications
        response = self.client.get(self.notifications_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        data = response.json()
        assert len(data['results']) == 0, f"Expected 0 notifications, got {len(data['results'])}"
    
    def test_mark_notification_as_read(self):
        """Test marking a notification as read."""
        # Create a user and authenticate
        user, _ = self.client.create_and_login(**self.user_data)
        
        # Create notifications
        notifications = self.create_notifications(user)
        notification_id = notifications[0].id
        
        # Mark notification as read
        response = self.client.post(
            self.mark_read_url,
            data={'notification_id': notification_id}
        )
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        
        # Verify notification is marked as read
        notification = Notification.objects.get(id=notification_id)
        assert notification.is_read, "Notification should be marked as read"
    
    def test_get_notification_count(self):
        """Test getting unread notification count."""
        # Create a user and authenticate
        user, _ = self.client.create_and_login(**self.user_data)
        
        # Create notifications
        notifications = self.create_notifications(user)
        
        # Get notification count
        response = self.client.get(self.notification_count_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        assert_response_contains(response, 'unread_count', len(notifications))
    
    def test_filter_notifications_by_type(self):
        """Test filtering notifications by type."""
        # Create a user and authenticate
        user, _ = self.client.create_and_login(**self.user_data)
        
        # Create notifications with different types
        Notification.objects.create(
            user=user,
            title='Test Notification 1',
            message='This is test notification 1',
            notification_type='type1',
            related_object_id=1,
            related_object_type='test'
        )
        Notification.objects.create(
            user=user,
            title='Test Notification 2',
            message='This is test notification 2',
            notification_type='type2',
            related_object_id=2,
            related_object_type='test'
        )
        
        # Filter notifications by type
        response = self.client.get(f"{self.notifications_url}?notification_type=type1")
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        data = response.json()
        assert len(data['results']) == 1, f"Expected 1 notification, got {len(data['results'])}"
        assert data['results'][0]['notification_type'] == 'type1', f"Expected notification_type 'type1', got {data['results'][0]['notification_type']}"
    
    def test_filter_notifications_by_read_status(self):
        """Test filtering notifications by read status."""
        # Create a user and authenticate
        user, _ = self.client.create_and_login(**self.user_data)
        
        # Create notifications
        notifications = self.create_notifications(user)
        
        # Mark one notification as read
        notification = notifications[0]
        notification.is_read = True
        notification.save()
        
        # Filter notifications by read status
        response = self.client.get(f"{self.notifications_url}?is_read=true")
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        data = response.json()
        assert len(data['results']) == 1, f"Expected 1 notification, got {len(data['results'])}"
        assert data['results'][0]['is_read'] == True, f"Expected is_read True, got {data['results'][0]['is_read']}"
    
    def test_search_notifications(self):
        """Test searching notifications."""
        # Create a user and authenticate
        user, _ = self.client.create_and_login(**self.user_data)
        
        # Create notifications with different titles
        Notification.objects.create(
            user=user,
            title='Application Status Update',
            message='Your application status has changed',
            notification_type='application_status',
            related_object_id=1,
            related_object_type='application'
        )
        Notification.objects.create(
            user=user,
            title='Document Signed',
            message='A document has been signed',
            notification_type='document_signed',
            related_object_id=2,
            related_object_type='document'
        )
        
        # Search notifications
        response = self.client.get(f"{self.notifications_url}?search=application")
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        data = response.json()
        assert len(data['results']) == 1, f"Expected 1 notification, got {len(data['results'])}"
        assert 'Application' in data['results'][0]['title'], f"Expected 'Application' in title, got {data['results'][0]['title']}"
    
    def test_get_notification_preferences(self):
        """Test getting notification preferences."""
        # Create a user and authenticate
        user, _ = self.client.create_and_login(**self.user_data)
        
        # Create notification preferences
        NotificationPreference.objects.create(user=user)
        
        # Get notification preferences
        response = self.client.get(self.notification_preferences_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        # Check that the response contains notification preference fields
        assert_response_contains(response, 'application_status_in_app')
    
    def test_update_notification_preferences(self):
        """Test updating notification preferences."""
        # Create a user and authenticate
        user, _ = self.client.create_and_login(**self.user_data)
        
        # Create notification preferences
        preferences = NotificationPreference.objects.create(user=user)
        
        # Update notification preferences
        update_data = {
            'application_status_email': False,
            'document_uploaded_email': False,
            'application_status_in_app': True,
            'document_uploaded_in_app': True
        }
        response = self.client.put(self.notification_preferences_url, data=update_data)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        
        # Verify preferences are updated
        preferences.refresh_from_db()
        assert preferences.application_status_email == update_data['application_status_email']
        assert preferences.document_uploaded_email == update_data['document_uploaded_email']
        assert preferences.application_status_in_app == update_data['application_status_in_app']
        assert preferences.document_uploaded_in_app == update_data['document_uploaded_in_app']
