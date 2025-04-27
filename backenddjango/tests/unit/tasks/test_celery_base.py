"""
Base test class for Celery task testing.
"""
import pytest
from unittest.mock import patch
from celery import current_app
from django.test import override_settings
from tests.celery_test_config import app as test_app

class CeleryTestCase:
    """Base class for Celery task tests."""
    
    @pytest.fixture(autouse=True)
    def setup_celery(self):
        """Set up Celery for testing."""
        # Store the original app
        self.original_app = current_app._get_current_object()
        
        # Replace with the test app
        current_app.conf = test_app.conf
        
        # Ensure tasks are executed locally
        with override_settings(CELERY_TASK_ALWAYS_EAGER=True, CELERY_TASK_EAGER_PROPAGATES=True):
            yield
        
        # Restore the original app
        current_app.conf = self.original_app.conf
    
    @pytest.fixture
    def mock_email(self):
        """Mock Django's send_mail function."""
        with patch('django.core.mail.send_mail') as mock:
            yield mock
    
    @pytest.fixture
    def mock_task_delay(self):
        """Mock the delay method of a task."""
        def _mock_task_delay(task_path):
            with patch(f'{task_path}.delay') as mock:
                yield mock
        
        return _mock_task_delay
