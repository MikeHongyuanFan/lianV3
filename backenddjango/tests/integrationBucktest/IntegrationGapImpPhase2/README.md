# Integration Gap Implementation Phase 2: Background Tasks and Async Operations

## Objective
Increase task coverage from 0% to at least 80% and improve async operation testing.

## Current Coverage Status
- `applications/tasks.py`: 0%
- WebSocket integration tests: Failing due to database locking issues

## Implementation Strategy

### 1. Background Task Testing

#### Target Files:
- `applications/tasks.py`

#### Test Cases to Implement:
1. Application status notification tasks
2. Document generation tasks
3. Email notification tasks
4. Scheduled reminder tasks
5. Data processing tasks

#### Example Implementation:
```python
@pytest.mark.django_db
def test_send_application_status_notification(application_instance, admin_user):
    from applications.tasks import send_application_status_notification
    from unittest.mock import patch
    
    # Mock the actual email sending
    with patch('applications.tasks.send_email') as mock_send_email:
        # Execute the task synchronously for testing
        send_application_status_notification(application_instance.id, 'approved')
        
        # Verify email was sent
        mock_send_email.assert_called_once()
    
    # Verify notification was created
    from users.models import Notification
    notification = Notification.objects.filter(
        user=application_instance.broker.user,
        notification_type='application_status'
    ).first()
    
    assert notification is not None
    assert 'approved' in notification.message.lower()
```

### 2. Celery Task Testing Framework

#### Implementation Steps:
1. Set up Celery test configuration
2. Create task testing utilities
3. Implement task result verification

#### Example Implementation:
```python
# conftest.py
import pytest
from celery.contrib.testing.worker import start_worker
from crm_backend.celery import app as celery_app

@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'memory://',
        'result_backend': 'rpc',
        'task_always_eager': True,  # Execute tasks synchronously for testing
    }

@pytest.fixture(scope='session')
def celery_worker():
    with start_worker(celery_app, perform_ping_check=False) as worker:
        yield worker
```

### 3. Periodic Task Testing

#### Test Cases to Implement:
1. Daily reminder tasks
2. Weekly report generation
3. Monthly compliance checks

#### Example Implementation:
```python
@pytest.mark.django_db
def test_send_repayment_reminders(repayment_instance):
    from applications.tasks import send_repayment_reminders
    from unittest.mock import patch
    from freezegun import freeze_time
    
    # Set the date to one day before repayment is due
    due_date = repayment_instance.due_date
    with freeze_time(due_date - timezone.timedelta(days=1)):
        with patch('applications.tasks.send_email') as mock_send_email:
            # Run the periodic task
            send_repayment_reminders()
            
            # Verify email was sent
            mock_send_email.assert_called_once()
```

### 4. WebSocket Testing with PostgreSQL

#### Implementation Steps:
1. Configure PostgreSQL for WebSocket tests
2. Create isolated database for async tests
3. Implement proper cleanup for WebSocket tests

#### Example Configuration:
```python
# conftest.py for WebSocket tests
import pytest
import os

@pytest.fixture(scope="session")
def django_db_setup():
    from django.conf import settings
    
    # Use PostgreSQL for WebSocket tests if available
    if os.environ.get('POSTGRES_TEST_DB'):
        settings.DATABASES["default"] = {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get('POSTGRES_TEST_DB', 'test_db'),
            "USER": os.environ.get('POSTGRES_TEST_USER', 'postgres'),
            "PASSWORD": os.environ.get('POSTGRES_TEST_PASSWORD', 'postgres'),
            "HOST": os.environ.get('POSTGRES_TEST_HOST', 'localhost'),
            "PORT": os.environ.get('POSTGRES_TEST_PORT', '5432'),
        }
```

### 5. Mock-based WebSocket Testing

#### Implementation Approach:
If PostgreSQL is not available, use mocking to test WebSocket functionality without database operations.

#### Example Implementation:
```python
@pytest.mark.asyncio
async def test_notification_websocket_with_mocks(admin_user):
    from channels.testing import WebsocketCommunicator
    from channels.routing import URLRouter
    import users.routing
    from unittest.mock import patch, MagicMock
    
    # Mock database operations
    with patch('users.consumers.NotificationConsumer.get_unread_count') as mock_get_count:
        # Set up mock return value
        mock_get_count.return_value = 5
        
        # Connect to WebSocket
        application = URLRouter(users.routing.websocket_urlpatterns)
        communicator = WebsocketCommunicator(application, "ws/notifications/")
        
        # Set user in scope directly (bypass auth)
        communicator.scope["user"] = admin_user
        
        connected, _ = await communicator.connect()
        assert connected
        
        # Verify initial count message
        response = await communicator.receive_json_from()
        assert response["type"] == "unread_count"
        assert response["count"] == 5
        
        await communicator.disconnect()
```

## Expected Outcomes
1. Increased task coverage from 0% to at least 80%
2. Working WebSocket integration tests
3. Better understanding of async behavior
4. Improved reliability of background processing

## Dependencies
- Celery test configuration
- PostgreSQL database (optional)
- Mock objects for external services
- Test fixtures for required entities

## Timeline
- Estimated completion time: 2 weeks
- Priority: High
