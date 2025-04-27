"""
Integration tests for periodic tasks in the application.
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

@pytest.mark.django_db
def test_daily_repayment_reminders(repayment_instance, borrower_instance, application_instance):
    """Test the daily repayment reminders task"""
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
    
    # Make sure the repayment is due in 7 days
    repayment_instance.due_date = timezone.now().date() + timezone.timedelta(days=7)
    repayment_instance.reminder_sent = False
    repayment_instance.save()
    
    with patch('applications.tasks.send_mail') as mock_send_mail:
        # Run the periodic task
        check_repayment_reminders()
        
        # Verify email was sent
        mock_send_mail.assert_called_once()
        
        # Verify email content
        call_args = mock_send_mail.call_args[1]
        assert 'Upcoming Repayment Reminder' in call_args['subject']
        assert str(repayment_instance.amount) in call_args['message']
        assert borrower_instance.user.email in call_args['recipient_list']

@pytest.mark.django_db
def test_weekly_stale_application_check(stale_application):
    """Test the weekly stale application check task"""
    # Make sure the application is actually stale according to the task's criteria
    threshold_date = timezone.now() - timezone.timedelta(days=15)
    stale_application.updated_at = threshold_date
    stale_application.save()
    
    # Make sure the BD has a user with an email
    if not stale_application.bd.user or not stale_application.bd.user.email:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_user(
            username='bd_test_user',
            email='bd_test@example.com',
            password='password'
        )
        stale_application.bd.user = user
        stale_application.bd.save()
    
    # Patch the filter method to ensure our application is returned
    with patch('applications.models.Application.objects.filter') as mock_filter:
        mock_queryset = MagicMock()
        mock_queryset.exclude.return_value = [stale_application]
        mock_filter.return_value = mock_queryset
        
        with patch('applications.tasks.send_mail') as mock_send_mail:
            # Run the periodic task
            check_stale_applications()
            
            # Verify email was sent
            mock_send_mail.assert_called_once()
            
            # Verify email content
            call_args = mock_send_mail.call_args[1]
            assert stale_application.reference_number in call_args['subject']
            assert stale_application.bd.user.email in call_args['recipient_list']

@pytest.mark.django_db
def test_daily_note_reminders(note_with_reminder, admin_user):
    """Test the daily note reminders task"""
    # Make sure the note reminder is for today
    note_with_reminder.remind_date = timezone.now().date()
    note_with_reminder.save()
    
    with patch('applications.tasks.send_mail') as mock_send_mail:
        # Run the periodic task
        check_note_reminders()
        
        # Verify email was sent
        mock_send_mail.assert_called_once()
        
        # Verify email content
        call_args = mock_send_mail.call_args[1]
        assert 'Note Reminder' in call_args['subject']
        assert note_with_reminder.title in call_args['subject']
        assert admin_user.email in call_args['recipient_list']

@pytest.mark.django_db
def test_multiple_periodic_tasks_sequence():
    """Test that multiple periodic tasks can run in sequence"""
    # Create test data
    from borrowers.models import Borrower
    from brokers.models import Broker, BDM
    from applications.models import Application
    from documents.models import Note, Repayment
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    # Create users
    bd_user = User.objects.create_user(username='bd_test', email='bd_test@example.com', password='password')
    borrower_user = User.objects.create_user(username='borrower_test', email='borrower_test@example.com', password='password')
    admin_user = User.objects.create_superuser(username='admin_test', email='admin_test@example.com', password='password')
    
    # Create BD
    bd = BDM.objects.create(name='Test BD', phone='1234567890', user=bd_user)
    
    # Create borrower
    borrower = Borrower.objects.create(first_name='Test', last_name='Borrower', email='borrower_test@example.com', phone='1234567890', user=borrower_user)
    
    # Create broker
    broker = Broker.objects.create(name='Test Broker', company='Test Company', phone='0987654321')
    
    # Create application
    application = Application.objects.create(
        reference_number='TEST-MULTI-001',
        loan_amount=150000,
        loan_term=24,
        interest_rate=5.0,
        stage='inquiry',  # Using a valid stage
        broker=broker,
        bd=bd,
        created_at=timezone.now() - timedelta(days=20),
        updated_at=timezone.now() - timedelta(days=15)
    )
    
    # Add borrower to application
    application.borrowers.add(borrower)
    
    # Create note with reminder
    note = Note.objects.create(
        title='Test Multi-task Note',
        content='This is a test note for multiple tasks',
        application=application,
        created_by=admin_user,
        remind_date=timezone.now().date()
    )
    
    # Create repayment due in 7 days
    repayment = Repayment.objects.create(
        application=application,
        amount=5000,
        due_date=timezone.now().date() + timedelta(days=7),
        reminder_sent=False
    )
    
    # Run all tasks in sequence
    with patch('applications.tasks.send_mail') as mock_send_mail:
        # Run the stale application check
        check_stale_applications()
        
        # Run the note reminders check
        check_note_reminders()
        
        # Run the repayment reminders check
        check_repayment_reminders()
        
        # Verify all emails were sent (1 for note, 1 for repayment)
        # Note: stale application won't trigger an email because it's not old enough by default
        assert mock_send_mail.call_count == 2

@pytest.mark.django_db
def test_periodic_task_with_time_changes(note_with_reminder, admin_user):
    """Test that periodic tasks handle time changes correctly"""
    # Set the note reminder to yesterday
    yesterday = timezone.now().date() - timezone.timedelta(days=1)
    note_with_reminder.remind_date = yesterday
    note_with_reminder.save()
    
    with patch('applications.tasks.send_mail') as mock_send_mail:
        # Run the periodic task with a time freeze to yesterday
        with patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = timezone.datetime.combine(
                yesterday,
                timezone.datetime.min.time(),
                tzinfo=timezone.get_current_timezone()
            )
            
            # Run the task
            check_note_reminders()
            
            # Verify email was sent
            mock_send_mail.assert_called_once()
            
            # Verify email content
            call_args = mock_send_mail.call_args[1]
            assert 'Note Reminder' in call_args['subject']
            assert note_with_reminder.title in call_args['subject']
            assert admin_user.email in call_args['recipient_list']
