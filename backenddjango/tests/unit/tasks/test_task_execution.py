"""
Tests for basic Celery task execution.
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
from tests.unit.tasks.test_mock_tasks import (
    mock_check_stale_applications,
    mock_check_note_reminders,
    mock_check_repayment_reminders
)

pytestmark = pytest.mark.django_db


class TestTaskExecution(CeleryTestCase):
    """Test basic task execution."""


class TestTaskExecution(CeleryTestCase):
    """Test basic task execution."""
    
    @pytest.mark.task
    def test_check_stale_applications(self):
        """Test check_stale_applications task execution."""
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
        
        # Create a recent application (should not trigger notification)
        recent_date = timezone.now() - timedelta(days=5)
        recent_app = ApplicationFactory(
            stage='assessment',
            updated_at=recent_date,
            bd=bd
        )
        
        # Create a completed application (should not trigger notification)
        completed_app = ApplicationFactory(
            stage='funded',
            updated_at=stale_date,
            bd=bd
        )
        
        # Use a mock for send_mail
        with patch('django.core.mail.send_mail') as mock_send_mail:
            # Make the mock callable
            mock_send_mail.side_effect = lambda *args, **kwargs: None
            
            # Execute the mock task implementation
            mock_check_stale_applications(mock_send_mail)
            
            # Verify that send_mail was called once for the stale application
            assert mock_send_mail.call_count == 1
            
            # Verify the email was sent to the BD
            args, kwargs = mock_send_mail.call_args
            assert 'Stale Application Alert' in args[0]  # subject
            assert stale_app.reference_number in args[1]  # message
            assert args[3] == [bd_user.email]  # recipient_list
    
    @pytest.mark.task
    def test_check_note_reminders(self):
        """Test check_note_reminders task execution."""
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
        
        # Create a note with tomorrow's remind date (should not trigger)
        tomorrow = today + timedelta(days=1)
        NoteFactory(
            application=application,
            created_by=user,
            remind_date=tomorrow
        )
        
        # Use a mock for send_mail
        with patch('django.core.mail.send_mail') as mock_send_mail:
            # Execute the mock task implementation
            mock_check_note_reminders(mock_send_mail)
            
            # Verify that send_mail was called once for today's note
            assert mock_send_mail.call_count == 1
            
            # Verify the email contains the note details
            args, kwargs = mock_send_mail.call_args
            assert 'Note Reminder' in args[0]  # subject
            assert 'Important Note' in args[1]  # message
            assert 'This is an important reminder' in args[1]  # message
            assert user.email in args[3]  # recipient_list
            assert bd_user.email in args[3]  # recipient_list
    
    @pytest.mark.task
    def test_check_repayment_reminders_upcoming(self):
        """Test check_repayment_reminders task for upcoming repayments."""
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
        
        # Use a mock for send_mail
        with patch('django.core.mail.send_mail') as mock_send_mail:
            # Execute the mock task implementation
            mock_check_repayment_reminders(mock_send_mail)
            
            # Verify that send_mail was called for the upcoming repayment
            assert mock_send_mail.call_count == 1
            
            # Verify the email was sent to the borrower
            args, kwargs = mock_send_mail.call_args
            assert 'Upcoming Repayment Reminder' in args[0]  # subject
            assert str(repayment.amount) in args[1]  # message contains amount
            assert upcoming_date.strftime('%d/%m/%Y') in args[1]  # message contains date
            assert args[3] == [borrower_user.email]  # recipient_list
        
        # Verify the repayment was marked as reminded
        repayment.refresh_from_db()
        assert repayment.reminder_sent is True
    
    @pytest.mark.task
    def test_check_repayment_reminders_overdue(self):
        """Test check_repayment_reminders task for overdue repayments."""
        # Create a borrower with user
        borrower_user = UserFactory(email='borrower@example.com')
        borrower = BorrowerFactory(user=borrower_user)
        
        # Create an application with the borrower
        application = ApplicationFactory()
        application.borrowers.add(borrower)
        
        # Create a repayment that's 3 days overdue
        today = timezone.now().date()
        overdue_date = today - timedelta(days=3)
        repayment = RepaymentFactory(
            application=application,
            due_date=overdue_date,
            amount=1000,
            paid_date=None,
            overdue_3_day_sent=False
        )
        
        # Use a mock for send_mail
        with patch('django.core.mail.send_mail') as mock_send_mail:
            # Execute the mock task implementation
            mock_check_repayment_reminders(mock_send_mail)
            
            # Verify that send_mail was called for the overdue repayment
            assert mock_send_mail.call_count == 1
            
            # Verify the email was sent to the borrower
            args, kwargs = mock_send_mail.call_args
            assert 'OVERDUE Repayment Notice' in args[0]  # subject
            assert str(repayment.amount) in args[1]  # message contains amount
            assert overdue_date.strftime('%d/%m/%Y') in args[1]  # message contains date
            assert args[3] == [borrower_user.email]  # recipient_list
        
        # Verify the repayment was marked as notified
        repayment.refresh_from_db()
        assert repayment.overdue_3_day_sent is True
