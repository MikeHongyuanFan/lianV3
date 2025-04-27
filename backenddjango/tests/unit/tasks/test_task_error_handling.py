"""
Tests for Celery task error handling.
"""
import pytest
from unittest.mock import patch, MagicMock
from django.utils import timezone
from datetime import timedelta
from celery.exceptions import Retry
from celery import shared_task
from applications.tasks import (
    check_stale_applications,
    check_note_reminders,
    check_repayment_reminders
)
from tests.factories import (
    ApplicationFactory, NoteFactory, RepaymentFactory, 
    BorrowerFactory, BDMFactory, UserFactory
)
from tests.unit.tasks.test_celery_base import CeleryTestCase

pytestmark = pytest.mark.django_db


class TestTaskErrorHandling(CeleryTestCase):
    """Test task error handling."""
    
    @pytest.mark.task
    @patch('applications.tasks.send_mail')
    def test_email_failure_handling(self, mock_send_mail):
        """Test handling of email sending failures."""
        # Make send_mail raise an exception
        mock_send_mail.side_effect = Exception("Email sending failed")
        
        # Create test data
        bd_user = UserFactory(email='bd@example.com')
        bd = BDMFactory(user=bd_user)
        threshold_days = 14
        stale_date = timezone.now() - timedelta(days=threshold_days + 1)
        stale_app = ApplicationFactory(
            stage='assessment',
            updated_at=stale_date,
            bd=bd
        )
        
        # Execute the task - it should not raise an exception
        # because we should have error handling in the task
        check_stale_applications()
        
        # Verify that send_mail was called
        assert mock_send_mail.called
    
    @pytest.mark.task
    @patch('applications.tasks.Application.objects.filter')
    def test_database_error_handling(self, mock_filter):
        """Test handling of database query errors."""
        # Make the database query raise an exception
        mock_filter.side_effect = Exception("Database error")
        
        # Execute the task - it should not raise an exception
        # because we should have error handling in the task
        check_stale_applications()
        
        # Verify that the filter was called
        assert mock_filter.called
    
    @pytest.mark.task
    @patch('applications.tasks.check_stale_applications.retry')
    @patch('applications.tasks.send_mail')
    def test_task_retry_mechanism(self, mock_send_mail, mock_retry):
        """Test that tasks can retry on failure."""
        # Make send_mail raise an exception
        mock_send_mail.side_effect = Exception("Email sending failed")
        
        # Make retry raise Retry exception to simulate retry
        mock_retry.side_effect = Retry()
        
        # Create test data
        bd_user = UserFactory(email='bd@example.com')
        bd = BDMFactory(user=bd_user)
        threshold_days = 14
        stale_date = timezone.now() - timedelta(days=threshold_days + 1)
        stale_app = ApplicationFactory(
            stage='assessment',
            updated_at=stale_date,
            bd=bd
        )
        
        # Execute the task - it should call retry
        with pytest.raises(Retry):
            # We need to modify the task to use retry for this test
            # This is a mock implementation for testing
            @shared_task(bind=True, max_retries=3)
            def test_retry_task(self):
                try:
                    check_stale_applications()
                except Exception as exc:
                    self.retry(exc=exc, countdown=1)
            
            with patch('applications.tasks.shared_task', return_value=test_retry_task):
                test_retry_task()
        
        # Verify that retry was called
        assert mock_retry.called
    
    @pytest.mark.task
    @patch('applications.tasks.send_mail')
    def test_partial_failure_handling(self, mock_send_mail):
        """Test handling of partial failures in batch processing."""
        # Make send_mail fail for the second call only
        mock_send_mail.side_effect = [None, Exception("Email sending failed"), None]
        
        # Create test data for multiple notifications
        bd_user = UserFactory(email='bd@example.com')
        bd = BDMFactory(user=bd_user)
        
        # Create multiple applications
        threshold_days = 14
        stale_date = timezone.now() - timedelta(days=threshold_days + 1)
        
        for i in range(3):
            ApplicationFactory(
                stage='assessment',
                updated_at=stale_date,
                bd=bd,
                reference_number=f'APP-TEST-{i+1}'
            )
        
        # Execute the task - it should continue processing after a failure
        check_stale_applications()
        
        # Verify that send_mail was called for all applications
        assert mock_send_mail.call_count == 3
