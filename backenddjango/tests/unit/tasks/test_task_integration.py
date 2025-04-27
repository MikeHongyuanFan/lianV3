"""
Integration tests for Celery tasks.
"""
import pytest
from unittest.mock import patch
from django.utils import timezone
from datetime import timedelta
from applications.tasks import (
    check_stale_applications,
    check_note_reminders,
    check_repayment_reminders
)
from applications.models import Application
from documents.models import Note, Repayment
from tests.factories import (
    ApplicationFactory, NoteFactory, RepaymentFactory, 
    BorrowerFactory, BDMFactory, UserFactory
)
from tests.unit.tasks.test_celery_base import CeleryTestCase

pytestmark = pytest.mark.django_db


class TestTaskIntegration(CeleryTestCase):
    """Test task integration with Django models."""
    
    @pytest.mark.task
    @patch('applications.tasks.send_mail')
    def test_stale_applications_integration(self, mock_send_mail):
        """Test check_stale_applications integration with Application model."""
        # Create a BD user
        bd_user = UserFactory(email='bd@example.com')
        bd = BDMFactory(user=bd_user)
        
        # Create a stale application (older than threshold)
        threshold_days = 14
        stale_date = timezone.now() - timedelta(days=threshold_days + 1)
        stale_app = ApplicationFactory(
            stage='assessment',
            updated_at=stale_date,
            bd=bd
        )
        
        # Execute the task
        check_stale_applications()
        
        # Verify that send_mail was called
        assert mock_send_mail.called
        
        # Verify the email contains the correct application reference
        args, kwargs = mock_send_mail.call_args
        assert stale_app.reference_number in args[1]
    
    @pytest.mark.task
    @patch('applications.tasks.send_mail')
    def test_note_reminders_integration(self, mock_send_mail):
        """Test check_note_reminders integration with Note model."""
        # Create a user
        user = UserFactory(email='user@example.com')
        
        # Create an application with a BD
        bd_user = UserFactory(email='bd@example.com')
        bd = BDMFactory(user=bd_user)
        application = ApplicationFactory(bd=bd)
        
        # Create a note with today's remind date
        today = timezone.now().date()
        note = NoteFactory(
            application=application,
            created_by=user,
            remind_date=today,
            title='Important Note',
            content='This is an important reminder'
        )
        
        # Execute the task
        check_note_reminders()
        
        # Verify that send_mail was called
        assert mock_send_mail.called
        
        # Verify the email contains the note title and content
        args, kwargs = mock_send_mail.call_args
        assert note.title in args[1]
        assert note.content in args[1]
    
    @pytest.mark.task
    @patch('applications.tasks.send_mail')
    def test_repayment_reminders_integration(self, mock_send_mail):
        """Test check_repayment_reminders integration with Repayment model."""
        # Create a borrower with user
        borrower_user = UserFactory(email='borrower@example.com')
        borrower = BorrowerFactory(user=borrower_user)
        
        # Create an application with the borrower
        application = ApplicationFactory()
        application.borrowers.add(borrower)
        
        # Create a repayment due in 7 days
        today = timezone.now().date()
        upcoming_date = today + timedelta(days=7)
        repayment = RepaymentFactory(
            application=application,
            due_date=upcoming_date,
            amount=1000,
            paid_date=None,
            reminder_sent=False
        )
        
        # Execute the task
        check_repayment_reminders()
        
        # Verify that send_mail was called
        assert mock_send_mail.called
        
        # Verify the repayment was marked as reminded
        repayment.refresh_from_db()
        assert repayment.reminder_sent is True
        
        # Verify the email contains the repayment amount
        args, kwargs = mock_send_mail.call_args
        assert str(repayment.amount) in args[1]
    
    @pytest.mark.task
    @patch('applications.tasks.send_mail')
    def test_multiple_tasks_integration(self, mock_send_mail):
        """Test multiple tasks running together."""
        # Create test data for all tasks
        
        # 1. Stale application
        bd_user = UserFactory(email='bd@example.com')
        bd = BDMFactory(user=bd_user)
        threshold_days = 14
        stale_date = timezone.now() - timedelta(days=threshold_days + 1)
        stale_app = ApplicationFactory(
            stage='assessment',
            updated_at=stale_date,
            bd=bd
        )
        
        # 2. Note reminder
        user = UserFactory(email='user@example.com')
        today = timezone.now().date()
        note = NoteFactory(
            application=stale_app,  # Use the same application
            created_by=user,
            remind_date=today,
            title='Important Note',
            content='This is an important reminder'
        )
        
        # 3. Repayment reminder
        borrower_user = UserFactory(email='borrower@example.com')
        borrower = BorrowerFactory(user=borrower_user)
        stale_app.borrowers.add(borrower)  # Add borrower to the same application
        
        upcoming_date = today + timedelta(days=7)
        repayment = RepaymentFactory(
            application=stale_app,  # Use the same application
            due_date=upcoming_date,
            amount=1000,
            paid_date=None,
            reminder_sent=False
        )
        
        # Execute all tasks
        check_stale_applications()
        check_note_reminders()
        check_repayment_reminders()
        
        # Verify that send_mail was called multiple times
        assert mock_send_mail.call_count == 3
        
        # Verify the repayment was marked as reminded
        repayment.refresh_from_db()
        assert repayment.reminder_sent is True
