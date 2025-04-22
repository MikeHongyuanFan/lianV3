from .models import Notification, User, NotificationPreference
from django.core.mail import send_mail
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


def send_notification_via_websocket(user, notification_data=None, update_count=True):
    """
    Send a notification via WebSocket to a user
    
    Args:
        user: User to send notification to
        notification_data: Notification data to send (optional)
        update_count: Whether to update the unread count (default: True)
        
    Returns:
        Boolean indicating success or failure
    """
    try:
        channel_layer = get_channel_layer()
        
        # Send notification data if provided
        if notification_data:
            async_to_sync(channel_layer.group_send)(
                f"user_{user.id}_notifications",
                {
                    'type': 'notification_message',
                    'notification': notification_data
                }
            )
        
        # Update unread count if requested
        if update_count:
            unread_count = Notification.objects.filter(user=user, is_read=False).count()
            async_to_sync(channel_layer.group_send)(
                f"user_{user.id}_notifications",
                {
                    'type': 'notification_count',
                    'count': unread_count
                }
            )
        
        return True
    except Exception as e:
        print(f"Error sending WebSocket notification: {str(e)}")
        return False


def create_notification(user, title, message, notification_type, related_object_id=None, related_object_type=None):
    """
    Create a notification for a user
    
    Args:
        user: User to create notification for
        title: Notification title
        message: Notification message
        notification_type: Type of notification
        related_object_id: ID of related object (optional)
        related_object_type: Type of related object (optional)
        
    Returns:
        Created Notification object or None if notification preferences prevent creation
    """
    # Check if user has notification preferences
    try:
        preferences = NotificationPreference.objects.get(user=user)
        
        # Check if user wants in-app notifications for this type
        if not preferences.get_in_app_preference(notification_type):
            return None
    except NotificationPreference.DoesNotExist:
        # If no preferences exist, create default preferences
        preferences = NotificationPreference.objects.create(user=user)
    
    # Create the notification
    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type,
        related_object_id=related_object_id,
        related_object_type=related_object_type
    )
    
    # Send real-time notification via WebSocket
    try:
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
        
        # Send notification via WebSocket
        send_notification_via_websocket(user, notification_data)
    except Exception as e:
        # Log the error but don't fail the notification creation
        print(f"Error sending WebSocket notification: {str(e)}")
    
    # Check if user wants email notifications for this type
    try:
        if preferences.get_email_preference(notification_type):
            send_email_notification(
                user=user,
                subject=title,
                message=message
            )
    except Exception as e:
        # Log the error but don't fail the notification creation
        print(f"Error sending email notification: {str(e)}")
    
    return notification


def create_application_notification(application, notification_type, title, message):
    """
    Create notifications for users related to an application
    
    Args:
        application: Application object
        notification_type: Type of notification
        title: Notification title
        message: Notification message
        
    Returns:
        List of created Notification objects
    """
    notifications = []
    
    # Notify broker
    if application.broker and application.broker.user:
        broker_notification = create_notification(
            user=application.broker.user,
            title=title,
            message=message,
            notification_type=notification_type,
            related_object_id=application.id,
            related_object_type='application'
        )
        if broker_notification:
            notifications.append(broker_notification)
    
    # Notify BD
    if application.bd and application.bd.user:
        bd_notification = create_notification(
            user=application.bd.user,
            title=title,
            message=message,
            notification_type=notification_type,
            related_object_id=application.id,
            related_object_type='application'
        )
        if bd_notification:
            notifications.append(bd_notification)
    
    # Notify borrowers who have user accounts
    for borrower in application.borrowers.all():
        if borrower.user:
            borrower_notification = create_notification(
                user=borrower.user,
                title=title,
                message=message,
                notification_type=notification_type,
                related_object_id=application.id,
                related_object_type='application'
            )
            if borrower_notification:
                notifications.append(borrower_notification)
    
    # Notify admin users
    admin_users = User.objects.filter(role='admin')
    for admin in admin_users:
        admin_notification = create_notification(
            user=admin,
            title=title,
            message=message,
            notification_type=notification_type,
            related_object_id=application.id,
            related_object_type='application'
        )
        if admin_notification:
            notifications.append(admin_notification)
    
    return notifications


def send_email_notification(user, subject, message):
    """
    Send an email notification to a user
    
    Args:
        user: User to send email to
        subject: Email subject
        message: Email message
        
    Returns:
        Boolean indicating success or failure
    """
    if not user.email:
        return False
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return True
    except Exception:
        return False


def get_or_create_notification_preferences(user):
    """
    Get or create notification preferences for a user
    
    Args:
        user: User to get or create preferences for
        
    Returns:
        NotificationPreference object
    """
    preferences, created = NotificationPreference.objects.get_or_create(user=user)
    return preferences
