# Frontend Error Fixes

## Issue 1: WebSocket Connection Failures

The frontend is trying to connect to WebSocket endpoints that are not properly implemented or configured in the backend.

### Fix Steps:

1. **Update WebSocket URL in routing.py**:
   - The WebSocket URL in the routing.py file needs to include the token parameter
   - Updated the routing.py file to handle token authentication

2. **Refactor WebSocket Services**:
   - Created a dedicated `send_notification_via_websocket` function in users/services.py
   - Updated the create_notification function to use this new service
   - This makes the code more maintainable and easier to test

3. **Implement Comprehensive WebSocket Tests**:
   - Created a comprehensive test suite for WebSocket functionality
   - Tests cover notification delivery, reconnection handling, and error cases
   - Tests verify that notifications are properly filtered by user preferences

## Issue 2: Missing API Endpoints

The frontend is trying to access API endpoints that don't exist or aren't properly implemented.

### Fix Steps:

1. **Fix Notification Unread Count Endpoint**:
   - Ensure the endpoint at `/api/notifications/unread_count/` is properly implemented
   - Verify the URL configuration in users/urls.py

2. **Fix Application API Endpoints**:
   - Ensure all application-related endpoints are properly implemented
   - Verify URL configurations in applications/urls.py

## Issue 3: Router Navigation Issues

The Vue Router is trying to navigate to routes that don't exist in the router configuration.

### Fix Steps:

1. **Add Missing Routes**:
   - Add routes for "/applications" and "/borrowers" in the Vue Router configuration
   - Update the router/index.js file to include these routes

2. **Fix Navigation Components**:
   - Ensure navigation components are using the correct route names
   - Update any hardcoded URLs to use router links

## Implementation Details

### 1. WebSocket Service Refactoring

Created a new function `send_notification_via_websocket` in users/services.py:

```python
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
```

### 2. Comprehensive WebSocket Tests

Created a comprehensive test suite in test_websocket_api.py that tests:

1. Notification creation and delivery
2. WebSocket message sending
3. Notification preferences filtering
4. Error handling and reconnection
5. Multiple user notification delivery
6. Application event notifications

### 3. Next Steps

1. Fix the Vue Router configuration to include missing routes
2. Update the NotificationCenter component to handle WebSocket errors gracefully
3. Implement proper error handling in the WebSocket service
4. Add logging for WebSocket errors to help with debugging
