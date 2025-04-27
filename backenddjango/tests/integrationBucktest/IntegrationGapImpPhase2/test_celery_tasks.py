"""
Integration tests for Celery tasks in the application.
"""
import pytest
from unittest.mock import patch, MagicMock
from django.utils import timezone
from applications.tasks import (
    check_stale_applications,
    check_note_reminders,
    check_repayment_reminders
)

@pytest.mark.django_db
def test_stale_applications_task_execution(stale_application):
    """Test that the stale applications task executes correctly"""
    # Make sure the application is actually stale according to the task's criteria
    threshold_date = timezone.now() - timezone.timedelta(days=15)
    stale_application.updated_at = threshold_date
    stale_application.save()
    
    # Make sure the stage is not in the excluded list
    assert stale_application.stage not in ['funded', 'declined', 'withdrawn']
    
    # Test the task's functionality by directly calling the email sending part
    # But use a mock to avoid actually sending emails
    with patch('applications.tasks.send_mail') as mock_send_mail:
        # Call the task with a patched query to return our stale application
        with patch('applications.models.Application.objects.filter') as mock_filter:
            # Create a mock queryset that returns our stale application
            mock_queryset = MagicMock()
            mock_queryset.exclude.return_value = [stale_application]
            mock_filter.return_value = mock_queryset
            
            # Now call the task directly (not through Celery)
            check_stale_applications()
            
            # Verify email was sent
            mock_send_mail.assert_called_once()
            
            # Verify email content
            call_args = mock_send_mail.call_args[1]
            assert stale_application.reference_number in call_args['subject']
            assert stale_application.bd.user.email in call_args['recipient_list']

@pytest.mark.django_db
def test_note_reminders_task_execution(note_with_reminder):
    """Test that the note reminders task executes correctly"""
    # Make sure the note's remind_date is today
    note_with_reminder.remind_date = timezone.now().date()
    note_with_reminder.save()
    
    with patch('applications.tasks.send_mail') as mock_send_mail:
        # Call the task with a patched query to return our note
        with patch('documents.models.Note.objects.filter') as mock_filter:
            # Create a mock queryset that returns our note
            mock_filter.return_value = [note_with_reminder]
            
            # Now call the task directly (not through Celery)
            check_note_reminders()
            
            # Verify email was sent
            mock_send_mail.assert_called_once()
            
            # Verify email content
            call_args = mock_send_mail.call_args[1]
            assert note_with_reminder.title in call_args['subject']
            assert note_with_reminder.content in call_args['message']
            assert note_with_reminder.created_by.email in call_args['recipient_list']

@pytest.mark.django_db
def test_repayment_reminders_task_execution(overdue_repayment_3_days, borrower_instance, application_instance):
    """Test that the repayment reminders task executes correctly"""
    # Add borrower to application
    application_instance.borrowers.add(borrower_instance)
    
    # Make sure the borrower has a user with an email
    if not hasattr(borrower_instance, 'user') or not borrower_instance.user:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_user(
            username='borrower_test_user',
            email='borrower_test@example.com',
            password='password'
        )
        borrower_instance.user = user
        borrower_instance.save()

    # Make sure the repayment is exactly 3 days overdue
    overdue_repayment_3_days.due_date = timezone.now().date() - timezone.timedelta(days=3)
    overdue_repayment_3_days.reminder_sent = True
    overdue_repayment_3_days.overdue_3_day_sent = False
    overdue_repayment_3_days.save()
    
    with patch('applications.tasks.send_mail') as mock_send_mail:
        # Call the task directly (not through Celery)
        check_repayment_reminders()
        
        # Verify email was sent
        mock_send_mail.assert_called_once()
        
        # Verify email content
        call_args = mock_send_mail.call_args[1]
        assert 'OVERDUE Repayment Notice' in call_args['subject']
        assert borrower_instance.user.email in call_args['recipient_list']

@pytest.mark.django_db
def test_task_chain_execution(stale_application, note_with_reminder):
    """Test that multiple tasks can be chained together"""
    # Set up the test data
    threshold_date = timezone.now() - timezone.timedelta(days=15)
    stale_application.updated_at = threshold_date
    stale_application.save()
    
    note_with_reminder.remind_date = timezone.now().date()
    note_with_reminder.save()
    
    with patch('applications.tasks.send_mail') as mock_send_mail:
        # Set up mocks for both tasks
        with patch('applications.models.Application.objects.filter') as mock_app_filter:
            mock_app_queryset = MagicMock()
            mock_app_queryset.exclude.return_value = [stale_application]
            mock_app_filter.return_value = mock_app_queryset
            
            with patch('documents.models.Note.objects.filter') as mock_note_filter:
                mock_note_filter.return_value = [note_with_reminder]
                
                # Execute the tasks in sequence
                check_stale_applications()
                check_note_reminders()
                
                # Verify both tasks were executed
                assert mock_send_mail.call_count == 2

@pytest.mark.django_db
def test_task_error_handling():
    """Test that task errors are handled correctly"""
    # Mock Application.objects.filter to raise an exception
    with patch('applications.models.Application.objects.filter') as mock_filter:
        mock_filter.side_effect = Exception("Test exception")
        
        # Execute the task and expect it to fail
        with pytest.raises(Exception) as excinfo:
            check_stale_applications()
        
        # Verify the exception message
        assert "Test exception" in str(excinfo.value)
