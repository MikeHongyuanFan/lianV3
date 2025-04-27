"""
Tests for Celery task scheduling.
"""
import pytest
from unittest.mock import patch, MagicMock
from django.utils import timezone
from datetime import timedelta
from celery.schedules import crontab
from celery import shared_task
from applications.tasks import (
    check_stale_applications,
    check_note_reminders,
    check_repayment_reminders
)
from tests.unit.tasks.test_celery_base import CeleryTestCase

pytestmark = pytest.mark.django_db


class TestTaskScheduling(CeleryTestCase):
    """Test task scheduling."""
    
    @pytest.mark.task
    def test_task_registration(self):
        """Test that tasks are properly registered with Celery."""
        from celery import current_app
        
        # Get all registered task names
        task_names = list(current_app.tasks.keys())
        
        # Check that our tasks are registered
        assert 'applications.tasks.check_stale_applications' in task_names
        assert 'applications.tasks.check_note_reminders' in task_names
        assert 'applications.tasks.check_repayment_reminders' in task_names
    
    @pytest.mark.task
    @patch('applications.tasks.check_stale_applications')
    def test_stale_applications_scheduled_execution(self, mock_task):
        """Test scheduled execution of check_stale_applications task."""
        # Mock the Celery beat scheduler
        with patch('celery.app.base.Celery.send_task') as mock_send_task:
            # Simulate the scheduler calling the task
            mock_send_task.return_value = MagicMock()
            
            # Call the task directly to verify it's callable
            check_stale_applications()
            
            # Verify the task was called
            assert mock_task.called
    
    @pytest.mark.task
    @patch('applications.tasks.check_note_reminders')
    def test_note_reminders_scheduled_execution(self, mock_task):
        """Test scheduled execution of check_note_reminders task."""
        # Mock the Celery beat scheduler
        with patch('celery.app.base.Celery.send_task') as mock_send_task:
            # Simulate the scheduler calling the task
            mock_send_task.return_value = MagicMock()
            
            # Call the task directly to verify it's callable
            check_note_reminders()
            
            # Verify the task was called
            assert mock_task.called
    
    @pytest.mark.task
    @patch('applications.tasks.check_repayment_reminders')
    def test_repayment_reminders_scheduled_execution(self, mock_task):
        """Test scheduled execution of check_repayment_reminders task."""
        # Mock the Celery beat scheduler
        with patch('celery.app.base.Celery.send_task') as mock_send_task:
            # Simulate the scheduler calling the task
            mock_send_task.return_value = MagicMock()
            
            # Call the task directly to verify it's callable
            check_repayment_reminders()
            
            # Verify the task was called
            assert mock_task.called
    
    @pytest.mark.task
    def test_task_schedule_configuration(self):
        """Test that task schedules are properly configured."""
        # This test verifies that the beat_schedule is properly configured
        # in the Celery app settings
        
        from crm_backend.celery import app
        
        # Get the beat schedule
        beat_schedule = app.conf.beat_schedule
        
        # Check that our tasks are in the schedule
        assert 'check-stale-applications' in beat_schedule
        assert 'check-note-reminders' in beat_schedule
        assert 'check-repayment-reminders' in beat_schedule
        
        # Check the schedule for stale applications (should run daily)
        stale_schedule = beat_schedule['check-stale-applications']['schedule']
        assert isinstance(stale_schedule, crontab)
        
        # Check the schedule for note reminders (should run daily)
        note_schedule = beat_schedule['check-note-reminders']['schedule']
        assert isinstance(note_schedule, crontab)
        
        # Check the schedule for repayment reminders (should run daily)
        repayment_schedule = beat_schedule['check-repayment-reminders']['schedule']
        assert isinstance(repayment_schedule, crontab)
    
    @pytest.mark.task
    @patch('applications.tasks.send_mail')
    def test_task_retry_mechanism(self, mock_send_mail):
        """Test that tasks can retry on failure."""
        # Make send_mail fail the first time
        mock_send_mail.side_effect = [Exception("Connection error"), None]
        
        # Create a task that will retry
        @shared_task(bind=True, max_retries=3)
        def test_retry_task(self):
            try:
                send_mail(
                    subject="Test",
                    message="Test message",
                    from_email="test@example.com",
                    recipient_list=["recipient@example.com"]
                )
            except Exception as exc:
                # This should retry the task
                self.retry(exc=exc, countdown=1)
        
        # Execute the task
        with patch('applications.tasks.shared_task', return_value=test_retry_task):
            test_retry_task()
        
        # Verify send_mail was called twice (initial failure + retry success)
        assert mock_send_mail.call_count == 2
