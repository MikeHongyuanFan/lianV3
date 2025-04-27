"""
User services package.
"""
from .notification_service import (
    create_notification, create_application_notification,
    send_email_notification, get_or_create_notification_preferences
)
from .auth_service import AuthService
