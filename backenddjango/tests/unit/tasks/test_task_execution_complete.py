"""
Complete tests for Celery task execution with 100% coverage.
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
    now = timezone.now()
    stale_app = ApplicationFactory(
        stage='assessment',
        bd=bd,
    )
    
    # Force update timestamps with .update() to bypass auto_now
    fifteen_days_ago = now - timedelta(days=15)
    from applications.models import Application
    Application.objects.filter(id=stale_app.id).update(
        created_at=fifteen_days_ago,
        updated_at=fifteen_days_ago
    )
    
    # Refresh from DB to get updated values
    stale_app.refresh_from_db()
    
    # Patch the send_mail function where it's imported in the tasks module
    with patch('applications.tasks.send_mail') as mock_send_mail:
        # Make the mock callable and return a success value
        mock_send_mail.return_value = 1
        
        # Execute the task
        check_stale_applications()
        
        # Verify send_mail was called
        mock_send_mail.assert_called()
        
        # Check that the email was sent with the correct parameters
        call_args_list = mock_send_mail.call_args_list
        
        # Find a call that matches our expected parameters
        found_call = False
        for call in call_args_list:
            args = call.args
            kwargs = call.kwargs
            
            if (
                'subject' in kwargs and 'Stale Application Alert' in kwargs['subject'] and
                'message' in kwargs and stale_app.reference_number in kwargs['message'] and
                'recipient_list' in kwargs and bd_user.email in kwargs['recipient_list'][0]
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
    
    # Patch the send_mail function where it's imported in the tasks module
    with patch('applications.tasks.send_mail') as mock_send_mail:
        # Make the mock callable and return a success value
        mock_send_mail.return_value = 1
        
        # Execute the task
        check_note_reminders()
        
        # Verify send_mail was called
        mock_send_mail.assert_called()
        
        # Check that the email was sent with the correct parameters
        call_args_list = mock_send_mail.call_args_list
        
        # Find a call that matches our expected parameters
        found_call = False
        for call in call_args_list:
            args = call.args
            kwargs = call.kwargs
            
            if (
                'subject' in kwargs and 'Note Reminder' in kwargs['subject'] and
                'message' in kwargs and 'Important Note' in kwargs['message'] and
                'recipient_list' in kwargs and user.email in kwargs['recipient_list']
            ):
                found_call = True
                break
        
        assert found_call, "No call to send_mail with the expected parameters was found"


@pytest.mark.task
def test_repayment_reminders_upcoming():
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
    
    # Patch the send_mail function where it's imported in the tasks module
    with patch('applications.tasks.send_mail') as mock_send_mail:
        # Make the mock callable and return a success value
        mock_send_mail.return_value = 1
        
        # Execute the task
        check_repayment_reminders()
        
        # Verify send_mail was called
        mock_send_mail.assert_called()
        
        # Check that the email was sent with the correct parameters
        call_args_list = mock_send_mail.call_args_list
        
        # Find a call that matches our expected parameters
        found_call = False
        for call in call_args_list:
            args = call.args
            kwargs = call.kwargs
            
            if (
                'subject' in kwargs and 'Upcoming Repayment Reminder' in kwargs['subject'] and
                'message' in kwargs and str(repayment.amount) in kwargs['message'] and
                'recipient_list' in kwargs and borrower_user.email in kwargs['recipient_list']
            ):
                found_call = True
                break
        
        assert found_call, "No call to send_mail with the expected parameters was found"
        
        # Verify the repayment was marked as reminded
        repayment.refresh_from_db()
        assert repayment.reminder_sent is True


@pytest.mark.task
def test_repayment_reminders_overdue_3_days():
    """Test check_repayment_reminders task for 3 days overdue repayments."""
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
    
    # Patch the send_mail function where it's imported in the tasks module
    with patch('applications.tasks.send_mail') as mock_send_mail:
        # Make the mock callable and return a success value
        mock_send_mail.return_value = 1
        
        # Execute the task
        check_repayment_reminders()
        
        # Verify send_mail was called
        mock_send_mail.assert_called()
        
        # Check that the email was sent with the correct parameters
        call_args_list = mock_send_mail.call_args_list
        
        # Find a call that matches our expected parameters
        found_call = False
        for call in call_args_list:
            args = call.args
            kwargs = call.kwargs
            
            if (
                'subject' in kwargs and 'OVERDUE Repayment Notice' in kwargs['subject'] and
                'message' in kwargs and str(repayment.amount) in kwargs['message'] and
                'recipient_list' in kwargs and borrower_user.email in kwargs['recipient_list']
            ):
                found_call = True
                break
        
        assert found_call, "No call to send_mail with the expected parameters was found"
        
        # Verify the repayment was marked as notified
        repayment.refresh_from_db()
        assert repayment.overdue_3_day_sent is True


@pytest.mark.task
def test_repayment_reminders_overdue_7_days():
    """Test check_repayment_reminders task for 7 days overdue repayments."""
    # Create a borrower with user
    borrower_user = UserFactory(email='borrower@example.com')
    borrower = BorrowerFactory(user=borrower_user)
    
    # Create an application with the borrower
    application = ApplicationFactory()
    application.borrowers.add(borrower)
    
    # Create a repayment that's 7 days overdue
    today = timezone.now().date()
    overdue_date = today - timedelta(days=7)
    repayment = RepaymentFactory(
        application=application,
        due_date=overdue_date,
        amount=1000,
        paid_date=None,
        overdue_7_day_sent=False
    )
    
    # Patch the send_mail function where it's imported in the tasks module
    with patch('applications.tasks.send_mail') as mock_send_mail:
        # Make the mock callable and return a success value
        mock_send_mail.return_value = 1
        
        # Execute the task
        check_repayment_reminders()
        
        # Verify send_mail was called
        mock_send_mail.assert_called()
        
        # Check that the email was sent with the correct parameters
        call_args_list = mock_send_mail.call_args_list
        
        # Find a call that matches our expected parameters
        found_call = False
        for call in call_args_list:
            args = call.args
            kwargs = call.kwargs
            
            if (
                'subject' in kwargs and 'URGENT: 7 Days OVERDUE Repayment' in kwargs['subject'] and
                'message' in kwargs and str(repayment.amount) in kwargs['message'] and
                'recipient_list' in kwargs and borrower_user.email in kwargs['recipient_list']
            ):
                found_call = True
                break
        
        assert found_call, "No call to send_mail with the expected parameters was found"
        
        # Verify the repayment was marked as notified
        repayment.refresh_from_db()
        assert repayment.overdue_7_day_sent is True


@pytest.mark.task
def test_repayment_reminders_overdue_10_days():
    """Test check_repayment_reminders task for 10 days overdue repayments."""
    # Create a BD user
    bd_user = UserFactory(email='bd@example.com')
    bd = BDMFactory(user=bd_user)
    
    # Create an application with the BD
    application = ApplicationFactory(bd=bd)
    
    # Create a borrower
    borrower = BorrowerFactory()
    application.borrowers.add(borrower)
    
    # Create a repayment that's 10 days overdue
    today = timezone.now().date()
    overdue_date = today - timedelta(days=10)
    repayment = RepaymentFactory(
        application=application,
        due_date=overdue_date,
        amount=1000,
        paid_date=None,
        overdue_10_day_sent=False
    )
    
    # Patch the send_mail function where it's imported in the tasks module
    with patch('applications.tasks.send_mail') as mock_send_mail:
        # Make the mock callable and return a success value
        mock_send_mail.return_value = 1
        
        # Execute the task
        check_repayment_reminders()
        
        # Verify send_mail was called
        mock_send_mail.assert_called()
        
        # Check that the email was sent with the correct parameters
        call_args_list = mock_send_mail.call_args_list
        
        # Find a call that matches our expected parameters
        found_call = False
        for call in call_args_list:
            args = call.args
            kwargs = call.kwargs
            
            if (
                'subject' in kwargs and 'ESCALATION: 10 Days Overdue Repayment' in kwargs['subject'] and
                'message' in kwargs and str(repayment.amount) in kwargs['message'] and
                'recipient_list' in kwargs and bd_user.email in kwargs['recipient_list']
            ):
                found_call = True
                break
        
        assert found_call, "No call to send_mail with the expected parameters was found"
        
        # Verify the repayment was marked as notified
        repayment.refresh_from_db()
        assert repayment.overdue_10_day_sent is True
