"""
Simplified tests for Celery task execution.
"""
import pytest
from unittest.mock import patch, MagicMock
from django.utils import timezone
from datetime import timedelta
from applications.tasks import (
    check_stale_applications,
    check_note_reminders,
    check_repayment_reminders
)
from tests.factories import (
    ApplicationFactory, NoteFactory, RepaymentFactory, 
    BorrowerFactory, BDMFactory, UserFactory
)

pytestmark = pytest.mark.django_db


@pytest.mark.task
def test_stale_applications_task():
    """Test check_stale_applications task."""
    # Create a BD user
    bd_user = UserFactory(email='bd@example.com')
    bd = BDMFactory(user=bd_user)
    
    # Create a stale application
    threshold_days = 14
    stale_date = timezone.now() - timedelta(days=threshold_days + 1)
    
    # Force the updated_at field to be in the past
    with patch('django.utils.timezone.now') as mock_now:
        mock_now.return_value = stale_date
        stale_app = ApplicationFactory(
            stage='assessment',
            bd=bd
        )
    
    # Mock send_mail
    with patch('django.core.mail.send_mail') as mock_send_mail:
        # Execute the task
        check_stale_applications()
        
        # Verify send_mail was called
        assert mock_send_mail.called
        
        # Get the call arguments
        call_args = mock_send_mail.call_args_list
        
        # Check that at least one call was made with the correct parameters
        found_call = False
        for args, kwargs in call_args:
            if (
                'Stale Application Alert' in args[0] and
                stale_app.reference_number in args[1] and
                bd_user.email in args[3]
            ):
                found_call = True
                break
        
        assert found_call, "No call to send_mail with the expected parameters was found"


@pytest.mark.task
def test_note_reminders_task():
    """Test check_note_reminders task."""
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
    
    # Mock send_mail
    with patch('django.core.mail.send_mail') as mock_send_mail:
        # Execute the task
        check_note_reminders()
        
        # Verify send_mail was called
        assert mock_send_mail.called
        
        # Get the call arguments
        call_args = mock_send_mail.call_args_list
        
        # Check that at least one call was made with the correct parameters
        found_call = False
        for args, kwargs in call_args:
            if (
                'Note Reminder' in args[0] and
                'Important Note' in args[1] and
                user.email in args[3]
            ):
                found_call = True
                break
        
        assert found_call, "No call to send_mail with the expected parameters was found"


@pytest.mark.task
def test_repayment_reminders_task():
    """Test check_repayment_reminders task."""
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
    
    # Mock send_mail
    with patch('django.core.mail.send_mail') as mock_send_mail:
        # Execute the task
        check_repayment_reminders()
        
        # Verify send_mail was called
        assert mock_send_mail.called
        
        # Get the call arguments
        call_args = mock_send_mail.call_args_list
        
        # Check that at least one call was made with the correct parameters
        found_call = False
        for args, kwargs in call_args:
            if (
                'Upcoming Repayment Reminder' in args[0] and
                str(repayment.amount) in args[1] and
                borrower_user.email in args[3]
            ):
                found_call = True
                break
        
        assert found_call, "No call to send_mail with the expected parameters was found"
        
        # Verify the repayment was marked as reminded
        repayment.refresh_from_db()
        assert repayment.reminder_sent is True
