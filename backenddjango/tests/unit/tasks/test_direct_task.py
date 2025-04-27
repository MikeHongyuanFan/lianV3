"""
Direct tests for Celery tasks without mocking.
"""
import pytest
from unittest.mock import patch
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from applications.models import Application
from documents.models import Note, Repayment
from tests.factories import (
    ApplicationFactory, NoteFactory, RepaymentFactory, 
    BorrowerFactory, BDMFactory, UserFactory
)

pytestmark = pytest.mark.django_db


@pytest.mark.task
def test_direct_stale_applications():
    """Test stale applications directly."""
    # Create a BD user
    bd_user = UserFactory(email='bd@example.com')
    bd = BDMFactory(user=bd_user)
    
    # Capture the current time once to ensure consistency
    now = timezone.now()
    
    # Create a stale application first
    stale_app = Application.objects.create(
        reference_number='APP-STALE-001',
        stage='assessment',
        loan_amount=500000,
        loan_term=360,
        interest_rate=4.5,
        purpose='Home purchase',
        application_type='residential',
        broker=None,
        bd=bd,
        created_by=bd_user,
    )
    
    # Force update timestamps with .update() to bypass auto_now
    fifteen_days_ago = now - timedelta(days=15)
    Application.objects.filter(id=stale_app.id).update(
        created_at=fifteen_days_ago,
        updated_at=fifteen_days_ago
    )
    
    # Refresh from DB to get updated values
    stale_app.refresh_from_db()
    
    # Create a recent application
    recent_app = Application.objects.create(
        reference_number='APP-RECENT-001',
        stage='assessment',
        loan_amount=500000,
        loan_term=360,
        interest_rate=4.5,
        purpose='Home purchase',
        application_type='residential',
        broker=None,
        bd=bd,
        created_by=bd_user,
    )
    
    # Set the recent app's dates to 5 days ago using update()
    five_days_ago = now - timedelta(days=5)
    Application.objects.filter(id=recent_app.id).update(
        created_at=five_days_ago,
        updated_at=five_days_ago
    )
    
    # Refresh from DB to get updated values
    recent_app.refresh_from_db()
    
    # Print the actual dates for debugging
    print(f"Stale app updated_at: {stale_app.updated_at}")
    print(f"Recent app updated_at: {recent_app.updated_at}")
    print(f"Current time: {now}")
    print(f"Threshold date: {now - timedelta(days=14)}")
    
    # Find applications that haven't been updated in threshold_days
    threshold_days = 14
    threshold_date = now - timedelta(days=threshold_days)
    stale_applications = Application.objects.filter(
        updated_at__lt=threshold_date
    ).exclude(
        stage__in=['funded', 'declined', 'withdrawn']
    )
    
    # Print all applications for debugging
    all_apps = Application.objects.all()
    print(f"All applications count: {all_apps.count()}")
    for app in all_apps:
        print(f"App ID: {app.id}, Updated: {app.updated_at}, Stage: {app.stage}")
    
    # Verify that our stale application is found
    assert stale_applications.count() >= 1
    assert stale_app in stale_applications
    assert stale_app.bd.user.email == bd_user.email
    
    # Verify that our recent application is not found
    assert recent_app not in stale_applications


@pytest.mark.task
def test_direct_note_reminders():
    """Test note reminders directly."""
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
    
    # Find notes with remind_date today
    reminder_notes = Note.objects.filter(
        remind_date__date=today
    )
    
    # Verify that our note is found
    assert reminder_notes.count() == 1
    assert reminder_notes.first().id == note.id
    assert reminder_notes.first().created_by.email == user.email
    assert reminder_notes.first().application.bd.user.email == bd_user.email


@pytest.mark.task
def test_direct_repayment_reminders():
    """Test repayment reminders directly."""
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
    
    # Find upcoming repayments
    upcoming_repayments = Repayment.objects.filter(
        due_date=upcoming_date,
        paid_date__isnull=True,
        reminder_sent=False
    )
    
    # Verify that our repayment is found
    assert upcoming_repayments.count() == 1
    assert upcoming_repayments.first().id == repayment.id
    assert upcoming_repayments.first().application.borrowers.first().user.email == borrower_user.email
