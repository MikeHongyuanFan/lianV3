"""
Tests for notification filters.
"""
import pytest
from django.utils import timezone
from datetime import timedelta
from users.filters import NotificationFilter
from users.models import Notification
from tests.factories.notification_factory import NotificationFactory, ReadNotificationFactory

pytestmark = pytest.mark.django_db


@pytest.mark.filter
def test_notification_filter_is_read(admin_user):
    """Test filtering notifications by is_read."""
    # Create unread notifications
    unread1 = NotificationFactory(user=admin_user)
    unread2 = NotificationFactory(user=admin_user)
    
    # Create read notifications
    read1 = ReadNotificationFactory(user=admin_user)
    read2 = ReadNotificationFactory(user=admin_user)
    
    # Get all notifications for the user
    queryset = Notification.objects.filter(user=admin_user)
    
    # Filter for unread notifications
    filterset = NotificationFilter({'is_read': 'False'}, queryset=queryset)
    filtered_queryset = filterset.qs
    
    # Check that only unread notifications are returned
    assert filtered_queryset.count() == 2
    assert unread1 in filtered_queryset
    assert unread2 in filtered_queryset
    assert read1 not in filtered_queryset
    assert read2 not in filtered_queryset
    
    # Filter for read notifications
    filterset = NotificationFilter({'is_read': 'True'}, queryset=queryset)
    filtered_queryset = filterset.qs
    
    # Check that only read notifications are returned
    assert filtered_queryset.count() == 2
    assert unread1 not in filtered_queryset
    assert unread2 not in filtered_queryset
    assert read1 in filtered_queryset
    assert read2 in filtered_queryset


@pytest.mark.filter
def test_notification_filter_notification_type(admin_user):
    """Test filtering notifications by notification_type."""
    # Create notifications with different types
    status1 = NotificationFactory(user=admin_user, notification_type='application_status')
    status2 = NotificationFactory(user=admin_user, notification_type='application_status')
    document = NotificationFactory(user=admin_user, notification_type='document_uploaded')
    repayment = NotificationFactory(user=admin_user, notification_type='repayment_upcoming')
    
    # Get all notifications for the user
    queryset = Notification.objects.filter(user=admin_user)
    
    # Filter for application_status notifications
    filterset = NotificationFilter({'notification_type': 'application_status'}, queryset=queryset)
    filtered_queryset = filterset.qs
    
    # Check that only application_status notifications are returned
    assert filtered_queryset.count() == 2
    assert status1 in filtered_queryset
    assert status2 in filtered_queryset
    assert document not in filtered_queryset
    assert repayment not in filtered_queryset
    
    # Filter for document_uploaded notifications
    filterset = NotificationFilter({'notification_type': 'document_uploaded'}, queryset=queryset)
    filtered_queryset = filterset.qs
    
    # Check that only document_uploaded notifications are returned
    assert filtered_queryset.count() == 1
    assert status1 not in filtered_queryset
    assert status2 not in filtered_queryset
    assert document in filtered_queryset
    assert repayment not in filtered_queryset


@pytest.mark.filter
def test_notification_filter_date_range(admin_user):
    """Test filtering notifications by date range."""
    # Create notifications with different dates
    today = timezone.now()
    yesterday = today - timedelta(days=1)
    last_week = today - timedelta(days=7)
    last_month = today - timedelta(days=30)
    
    # Create notifications with specific dates
    notification_today = NotificationFactory(user=admin_user)
    notification_today.created_at = today
    notification_today.save()
    
    notification_yesterday = NotificationFactory(user=admin_user)
    notification_yesterday.created_at = yesterday
    notification_yesterday.save()
    
    notification_last_week = NotificationFactory(user=admin_user)
    notification_last_week.created_at = last_week
    notification_last_week.save()
    
    notification_last_month = NotificationFactory(user=admin_user)
    notification_last_month.created_at = last_month
    notification_last_month.save()
    
    # Get all notifications for the user
    queryset = Notification.objects.filter(user=admin_user)
    
    # Filter for notifications from the last 2 days
    two_days_ago = (today - timedelta(days=2)).date().isoformat()
    filterset = NotificationFilter({'date_from': two_days_ago}, queryset=queryset)
    filtered_queryset = filterset.qs
    
    # Check that only recent notifications are returned
    assert filtered_queryset.count() == 2
    assert notification_today in filtered_queryset
    assert notification_yesterday in filtered_queryset
    assert notification_last_week not in filtered_queryset
    assert notification_last_month not in filtered_queryset
    
    # Filter for notifications from the last week to yesterday
    week_ago = (today - timedelta(days=7)).date().isoformat()
    yesterday_date = yesterday.date().isoformat()
    filterset = NotificationFilter({
        'date_from': week_ago,
        'date_to': yesterday_date
    }, queryset=queryset)
    filtered_queryset = filterset.qs
    
    # Check that only notifications from the last week to yesterday are returned
    assert notification_today not in filtered_queryset
    assert notification_yesterday in filtered_queryset
    assert notification_last_week in filtered_queryset
    assert notification_last_month not in filtered_queryset


@pytest.mark.filter
def test_notification_filter_search(admin_user):
    """Test searching notifications."""
    # Create notifications with different content
    notification1 = NotificationFactory(
        user=admin_user,
        title='Application Status Update',
        message='Your application has been approved'
    )
    notification2 = NotificationFactory(
        user=admin_user,
        title='Document Required',
        message='Please upload your identification documents'
    )
    notification3 = NotificationFactory(
        user=admin_user,
        title='Repayment Reminder',
        message='Your loan repayment is due tomorrow'
    )
    notification4 = NotificationFactory(
        user=admin_user,
        title='System Notification',
        message='The system will be down for maintenance'
    )
    
    # Get all notifications for the user
    queryset = Notification.objects.filter(user=admin_user)
    
    # Search for 'application'
    filterset = NotificationFilter({'search': 'application'}, queryset=queryset)
    filtered_queryset = filterset.qs
    
    # Check that only notifications with 'application' are returned
    assert filtered_queryset.count() == 1
    assert notification1 in filtered_queryset
    assert notification2 not in filtered_queryset
    assert notification3 not in filtered_queryset
    assert notification4 not in filtered_queryset
    
    # Search for 'document upload'
    filterset = NotificationFilter({'search': 'document upload'}, queryset=queryset)
    filtered_queryset = filterset.qs
    
    # Check that only notifications with 'document' or 'upload' are returned
    assert notification1 not in filtered_queryset
    assert notification2 in filtered_queryset
    assert notification3 not in filtered_queryset
    assert notification4 not in filtered_queryset
    
    # Search for 'system maintenance'
    filterset = NotificationFilter({'search': 'system maintenance'}, queryset=queryset)
    filtered_queryset = filterset.qs
    
    # Check that only notifications with 'system' or 'maintenance' are returned
    assert notification1 not in filtered_queryset
    assert notification2 not in filtered_queryset
    assert notification3 not in filtered_queryset
    assert notification4 in filtered_queryset


@pytest.mark.filter
def test_notification_filter_combined(admin_user):
    """Test combining multiple filters."""
    # Create notifications with different properties
    notification1 = NotificationFactory(
        user=admin_user,
        title='Application Status Update',
        message='Your application has been approved',
        notification_type='application_status',
        is_read=False
    )
    notification2 = ReadNotificationFactory(
        user=admin_user,
        title='Document Required',
        message='Please upload your identification documents',
        notification_type='document_uploaded',
        is_read=True
    )
    notification3 = NotificationFactory(
        user=admin_user,
        title='Repayment Reminder',
        message='Your loan repayment is due tomorrow',
        notification_type='repayment_upcoming',
        is_read=False
    )
    
    # Set specific dates
    today = timezone.now()
    yesterday = today - timedelta(days=1)
    
    notification1.created_at = today
    notification1.save()
    
    notification2.created_at = yesterday
    notification2.save()
    
    notification3.created_at = yesterday
    notification3.save()
    
    # Get all notifications for the user
    queryset = Notification.objects.filter(user=admin_user)
    
    # Combine filters: unread + yesterday + search for 'repayment'
    yesterday_date = yesterday.date().isoformat()
    filterset = NotificationFilter({
        'is_read': 'False',
        'date_from': yesterday_date,
        'date_to': yesterday_date,
        'search': 'repayment'
    }, queryset=queryset)
    filtered_queryset = filterset.qs
    
    # Check that only the matching notification is returned
    assert filtered_queryset.count() == 1
    assert notification1 not in filtered_queryset
    assert notification2 not in filtered_queryset
    assert notification3 in filtered_queryset
