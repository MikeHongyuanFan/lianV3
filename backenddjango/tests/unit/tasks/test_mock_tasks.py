"""
Mock implementations of tasks for testing.
"""
from unittest.mock import patch
from django.utils import timezone
from datetime import timedelta
from applications.models import Application
from documents.models import Note, Repayment


def mock_check_stale_applications(mock_send_mail):
    """Mock implementation of check_stale_applications for testing."""
    # Define the threshold for stale applications
    threshold_days = 14
    threshold_date = timezone.now() - timedelta(days=threshold_days)
    
    # Find applications that haven't been updated in threshold_days
    stale_applications = Application.objects.filter(
        updated_at__lt=threshold_date
    ).exclude(
        stage__in=['funded', 'declined', 'withdrawn']
    )
    
    for application in stale_applications:
        if application.bd and application.bd.user and application.bd.user.email:
            # Use the mock to "send" email
            mock_send_mail(
                subject=f'Stale Application Alert: {application.reference_number}',
                message=f'''
                Application {application.reference_number} has been in the {application.get_stage_display()} stage for over {threshold_days} days.
                
                Please review this application and update its status or contact the broker.
                
                Application Details:
                - Reference: {application.reference_number}
                - Stage: {application.get_stage_display()}
                - Loan Amount: ${application.loan_amount}
                - Broker: {application.broker.name if application.broker else 'N/A'}
                - Last Updated: {application.updated_at.strftime('%d/%m/%Y')}
                ''',
                from_email='test@example.com',
                recipient_list=[application.bd.user.email],
            )


def mock_check_note_reminders(mock_send_mail):
    """Mock implementation of check_note_reminders for testing."""
    today = timezone.now().date()
    
    # Find notes with remind_date today
    reminder_notes = Note.objects.filter(
        remind_date__date=today
    )
    
    for note in reminder_notes:
        # Determine recipients
        recipients = []
        
        # Add note creator
        if note.created_by and note.created_by.email:
            recipients.append(note.created_by.email)
        
        # Add application BD if exists
        if note.application and note.application.bd and note.application.bd.user and note.application.bd.user.email:
            recipients.append(note.application.bd.user.email)
        
        # Send email if we have recipients
        if recipients:
            mock_send_mail(
                subject=f'Note Reminder: {note.title}',
                message=f'''
                This is a reminder for the note: {note.title}
                
                Content: {note.content}
                
                Related to Application: {note.application.reference_number if note.application else 'N/A'}
                Related to Borrower: {note.borrower if note.borrower else 'N/A'}
                
                Created on: {note.created_at.strftime('%d/%m/%Y')}
                ''',
                from_email='test@example.com',
                recipient_list=recipients,
            )


def mock_check_repayment_reminders(mock_send_mail):
    """Mock implementation of check_repayment_reminders for testing."""
    today = timezone.now().date()
    
    # Upcoming repayments (7 days before due date)
    upcoming_date = today + timedelta(days=7)
    upcoming_repayments = Repayment.objects.filter(
        due_date=upcoming_date,
        paid_date__isnull=True,
        reminder_sent=False
    )
    
    for repayment in upcoming_repayments:
        # Notify borrowers
        borrowers = repayment.application.borrowers.all()
        for borrower in borrowers:
            if hasattr(borrower, 'user') and borrower.user and borrower.user.email:
                mock_send_mail(
                    subject=f'Upcoming Repayment Reminder',
                    message=f'''
                    This is a reminder that you have a repayment of ${repayment.amount} due on {repayment.due_date.strftime('%d/%m/%Y')}.
                    
                    Application Reference: {repayment.application.reference_number}
                    
                    Please ensure funds are available in your account for this repayment.
                    ''',
                    from_email='test@example.com',
                    recipient_list=[borrower.user.email],
                )
        
        # Mark as reminded
        repayment.reminder_sent = True
        repayment.save()
    
    # 3 days overdue - notify borrowers
    overdue_3_date = today - timedelta(days=3)
    overdue_3_repayments = Repayment.objects.filter(
        due_date=overdue_3_date,
        paid_date__isnull=True,
        overdue_3_day_sent=False
    )
    
    for repayment in overdue_3_repayments:
        # Notify borrowers
        borrowers = repayment.application.borrowers.all()
        for borrower in borrowers:
            if hasattr(borrower, 'user') and borrower.user and borrower.user.email:
                mock_send_mail(
                    subject=f'OVERDUE Repayment Notice',
                    message=f'''
                    IMPORTANT: Your repayment of ${repayment.amount} was due on {repayment.due_date.strftime('%d/%m/%Y')} and is now 3 days overdue.
                    
                    Application Reference: {repayment.application.reference_number}
                    
                    Please make this payment immediately to avoid additional fees and penalties.
                    ''',
                    from_email='test@example.com',
                    recipient_list=[borrower.user.email],
                )
        
        # Mark as notified
        repayment.overdue_3_day_sent = True
        repayment.save()
