import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User, Notification, NotificationPreference
from users.serializers import NotificationSerializer, NotificationListSerializer
from django.utils import timezone
import json

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user():
    return User.objects.create_user(
        username='admin',
        email='admin@example.com',
        password='password123',
        role='admin',
        is_staff=True,
        is_superuser=True,
        first_name='Admin',
        last_name='User'
    )

@pytest.fixture
def regular_user():
    return User.objects.create_user(
        username='user',
        email='user@example.com',
        password='password123',
        role='client',
        first_name='Regular',
        last_name='User'
    )

@pytest.fixture
def notification(regular_user):
    return Notification.objects.create(
        user=regular_user,
        title="Test Notification",
        message="This is a test notification",
        notification_type="application_status",
        related_object_id=1,
        related_object_type="application"
    )

@pytest.fixture
def notification_preference(regular_user):
    return NotificationPreference.objects.create(
        user=regular_user,
        application_status_in_app=True,
        document_uploaded_in_app=True,
        application_status_email=True,
        document_uploaded_email=True,
        repayment_upcoming_in_app=True,
        repayment_overdue_in_app=True
    )

@pytest.mark.django_db
class TestLoginView:
    """Tests for the LoginView"""
    
    def test_login_success(self, api_client, regular_user):
        """Should be able to login with valid credentials"""
        url = reverse('login')
        data = {
            'email': 'user@example.com',
            'password': 'password123'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert response.data['email'] == regular_user.email
        assert response.data['role'] == regular_user.role
    
    def test_login_invalid_credentials(self, api_client):
        """Should not be able to login with invalid credentials"""
        url = reverse('login')
        data = {
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'error' in response.data


@pytest.mark.django_db
class TestRegisterView:
    """Tests for the RegisterView"""
    
    def test_register_success(self, api_client):
        """Should be able to register a new user"""
        url = reverse('register')
        data = {
            'email': 'newuser@example.com',
            'password': 'securepassword123',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'client'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert response.data['email'] == data['email']
        assert response.data['role'] == data['role']
        
        # Verify user was created in database
        assert User.objects.filter(email='newuser@example.com').exists()
    
    def test_register_duplicate_email(self, api_client, regular_user):
        """Should not be able to register with an existing email"""
        url = reverse('register')
        data = {
            'email': 'user@example.com',  # Same as regular_user
            'password': 'securepassword123',
            'first_name': 'Duplicate',
            'last_name': 'User',
            'role': 'client'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data  # Should contain error about duplicate email


@pytest.mark.django_db
class TestUserProfileView:
    """Tests for the UserProfileView"""
    
    def test_get_profile(self, api_client, regular_user):
        """Should be able to get own profile"""
        api_client.force_authenticate(user=regular_user)
        url = reverse('user-profile')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == regular_user.email
        assert response.data['first_name'] == regular_user.first_name
        assert response.data['last_name'] == regular_user.last_name
    
    def test_get_profile_unauthenticated(self, api_client):
        """Should not be able to get profile when unauthenticated"""
        url = reverse('user-profile')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUserProfileUpdateView:
    """Tests for the UserProfileUpdateView"""
    
    def test_update_profile(self, api_client, regular_user):
        """Should be able to update own profile"""
        api_client.force_authenticate(user=regular_user)
        url = reverse('user-profile-update')
        
        data = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        
        response = api_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == 'Updated'
        assert response.data['last_name'] == 'Name'
        
        # Verify changes in database
        regular_user.refresh_from_db()
        assert regular_user.first_name == 'Updated'
        assert regular_user.last_name == 'Name'


@pytest.mark.django_db
class TestNotificationListView:
    """Tests for the NotificationListView"""
    
    def test_list_notifications(self, api_client, regular_user, notification):
        """Should be able to list own notifications"""
        api_client.force_authenticate(user=regular_user)
        url = reverse('notification-list')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == notification.title
        assert response.data['results'][0]['message'] == notification.message
    
    def test_filter_notifications_by_type(self, api_client, regular_user, notification):
        """Should be able to filter notifications by type"""
        # Create another notification with different type
        Notification.objects.create(
            user=regular_user,
            title="Payment Notification",
            message="Payment received",
            notification_type="payment_received",
            related_object_id=1,
            related_object_type="payment"
        )
        
        api_client.force_authenticate(user=regular_user)
        url = reverse('notification-list') + '?notification_type=application_status'
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == notification.title
    
    def test_filter_notifications_by_read_status(self, api_client, regular_user, notification):
        """Should be able to filter notifications by read status"""
        # Mark the notification as read
        notification.is_read = True
        notification.save()
        
        # Create another unread notification
        Notification.objects.create(
            user=regular_user,
            title="Unread Notification",
            message="This is unread",
            notification_type="application_status",
            related_object_id=2,
            related_object_type="application"
        )
        
        api_client.force_authenticate(user=regular_user)
        url = reverse('notification-list') + '?is_read=true'
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == notification.title
    
    def test_search_notifications(self, api_client, regular_user, notification):
        """Should be able to search notifications"""
        # Create another notification with different content
        Notification.objects.create(
            user=regular_user,
            title="Document Upload",
            message="A document has been uploaded",
            notification_type="document_uploaded",
            related_object_id=1,
            related_object_type="document"
        )
        
        api_client.force_authenticate(user=regular_user)
        url = reverse('notification-list') + '?search=document'
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == "Document Upload"


@pytest.mark.django_db
class TestNotificationMarkReadView:
    """Tests for the NotificationMarkReadView"""
    
    def test_mark_notification_as_read(self, api_client, regular_user, notification):
        """Should be able to mark a notification as read"""
        api_client.force_authenticate(user=regular_user)
        url = reverse('notification-mark-read')
        
        data = {
            'notification_id': notification.id
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'notification marked as read'
        
        # Verify notification is marked as read in database
        notification.refresh_from_db()
        assert notification.is_read is True
    
    def test_mark_all_notifications_as_read(self, api_client, regular_user, notification):
        """Should be able to mark all notifications as read"""
        # Create another notification
        Notification.objects.create(
            user=regular_user,
            title="Another Notification",
            message="This is another notification",
            notification_type="application_status",
            related_object_id=2,
            related_object_type="application"
        )
        
        api_client.force_authenticate(user=regular_user)
        url = reverse('notification-mark-read')
        
        response = api_client.post(url, {}, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'all notifications marked as read'
        
        # Verify all notifications are marked as read in database
        assert Notification.objects.filter(user=regular_user, is_read=False).count() == 0


@pytest.mark.django_db
class TestNotificationCountView:
    """Tests for the NotificationCountView"""
    
    def test_get_unread_count(self, api_client, regular_user, notification):
        """Should be able to get unread notification count"""
        api_client.force_authenticate(user=regular_user)
        url = reverse('notification-count')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['unread_count'] == 1
        
        # Mark notification as read
        notification.is_read = True
        notification.save()
        
        # Count should now be 0
        response = api_client.get(url)
        assert response.data['unread_count'] == 0


@pytest.mark.django_db
class TestNotificationPreferenceView:
    """Tests for the NotificationPreferenceView"""
    
    def test_get_preferences(self, api_client, regular_user, notification_preference):
        """Should be able to get notification preferences"""
        api_client.force_authenticate(user=regular_user)
        url = reverse('notification-preferences')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['application_status_in_app'] is True
        assert response.data['document_uploaded_in_app'] is True
    
    def test_update_preferences(self, api_client, regular_user, notification_preference):
        """Should be able to update notification preferences"""
        api_client.force_authenticate(user=regular_user)
        url = reverse('notification-preferences')
        
        data = {
            'application_status_email': False,
            'application_status_in_app': True,
            'document_uploaded_in_app': False
        }
        
        response = api_client.put(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['application_status_email'] is False
        assert response.data['application_status_in_app'] is True
        assert response.data['document_uploaded_in_app'] is False
        
        # Verify changes in database
        notification_preference.refresh_from_db()
        assert notification_preference.application_status_email is False
        assert notification_preference.application_status_in_app is True
        assert notification_preference.document_uploaded_in_app is False


@pytest.mark.django_db
class TestNotificationViewSet:
    """Tests for the NotificationViewSet"""
    
    def test_list_notifications(self, api_client, regular_user, notification):
        """Should be able to list notifications"""
        api_client.force_authenticate(user=regular_user)
        url = reverse('notification-list')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == notification.title
    
    def test_retrieve_notification(self, api_client, regular_user, notification):
        """Should be able to retrieve a specific notification"""
        api_client.force_authenticate(user=regular_user)
        url = reverse('notifications-detail', kwargs={'pk': notification.id})
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == notification.title
        assert response.data['message'] == notification.message
    
    def test_mark_notification_as_read(self, api_client, regular_user, notification):
        """Should be able to mark a notification as read"""
        api_client.force_authenticate(user=regular_user)
        url = reverse('notification-mark-read')
        
        data = {
            'notification_id': notification.id
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'notification marked as read'
        
        # Verify notification is marked as read in database
        notification.refresh_from_db()
        assert notification.is_read is True
    
    def test_mark_all_notifications_as_read(self, api_client, regular_user, notification):
        """Should be able to mark all notifications as read"""
        # Create another notification
        Notification.objects.create(
            user=regular_user,
            title="Another Notification",
            message="This is another notification",
            notification_type="application_status",
            related_object_id=2,
            related_object_type="application"
        )
        
        api_client.force_authenticate(user=regular_user)
        url = reverse('notification-mark-read')
        
        response = api_client.post(url, {}, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'all notifications marked as read'
        
        # Verify all notifications are marked as read in database
        assert Notification.objects.filter(user=regular_user, is_read=False).count() == 0
    
    def test_advanced_search(self, api_client, regular_user, notification):
        """Should be able to use advanced search for notifications"""
        # Create notifications with different dates
        yesterday = timezone.now() - timezone.timedelta(days=1)
        tomorrow = timezone.now() + timezone.timedelta(days=1)
        
        Notification.objects.create(
            user=regular_user,
            title="Old Notification",
            message="This is an old notification",
            notification_type="application_status",
            related_object_id=2,
            related_object_type="application",
            created_at=yesterday
        )
        
        future_notification = Notification.objects.create(
            user=regular_user,
            title="Future Notification",
            message="This is a future notification",
            notification_type="document_uploaded",
            related_object_id=3,
            related_object_type="document",
            created_at=tomorrow
        )
        
        api_client.force_authenticate(user=regular_user)
        
        # Test notification type filtering
        url = reverse('notification-search') + f'?notification_type=document_uploaded'
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == "Future Notification"
    
    def test_unread_count(self, api_client, regular_user, notification):
        """Should be able to get unread notification count"""
        api_client.force_authenticate(user=regular_user)
        url = reverse('notification-count')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['unread_count'] == 1
