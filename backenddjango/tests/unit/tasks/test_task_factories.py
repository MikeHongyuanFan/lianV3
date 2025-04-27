"""
Test factories for Celery tasks.
"""
import pytest
from django.utils import timezone
from datetime import timedelta
from tests.factories import (
    ApplicationFactory, NoteFactory, RepaymentFactory, 
    BorrowerFactory, BDMFactory, UserFactory
)

pytestmark = pytest.mark.django_db


class TaskTestFactories:
    """Factory methods for creating test data for task tests."""
    
    @staticmethod
    def create_stale_application_data():
        """Create test data for stale application tests."""
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
        
        return {
            'bd_user': bd_user,
            'bd': bd,
            'stale_app': stale_app,
            'recent_app': recent_app,
            'completed_app': completed_app
        }
    
    @staticmethod
    def create_note_reminder_data():
        """Create test data for note reminder tests."""
        # Create a user
        user = UserFactory(email='user@example.com')
        
        # Create an application with a BD
        bd_user = UserFactory(email='bd@example.com')
        bd = BDMFactory(user=bd_user)
        application = ApplicationFactory(bd=bd)
        
        # Create a note with today's remind date
        today = timezone.now().date()
        note_today = NoteFactory(
            application=application,
            created_by=user,
            remind_date=today,
            title='Important Note',
            content='This is an important reminder'
        )
        
        # Create a note with tomorrow's remind date (should not trigger)
        tomorrow = today + timedelta(days=1)
        note_tomorrow = NoteFactory(
            application=application,
            created_by=user,
            remind_date=tomorrow
        )
        
        return {
            'user': user,
            'bd_user': bd_user,
            'bd': bd,
            'application': application,
            'note_today': note_today,
            'note_tomorrow': note_tomorrow
        }
    
    @staticmethod
    def create_repayment_reminder_data():
        """Create test data for repayment reminder tests."""
        # Create a borrower with user
        borrower_user = UserFactory(email='borrower@example.com')
        borrower = BorrowerFactory(user=borrower_user)
        
        # Create an application with the borrower
        application = ApplicationFactory()
        application.borrowers.add(borrower)
        
        today = timezone.now().date()
        
        # Create a repayment due in 7 days (upcoming)
        upcoming_date = today + timedelta(days=7)
        upcoming_repayment = RepaymentFactory(
            application=application,
            due_date=upcoming_date,
            amount=1000,
            paid_date=None,
            reminder_sent=False
        )
        
        # Create a repayment that's 3 days overdue
        overdue_3_date = today - timedelta(days=3)
        overdue_3_repayment = RepaymentFactory(
            application=application,
            due_date=overdue_3_date,
            amount=1500,
            paid_date=None,
            overdue_3_day_sent=False
        )
        
        # Create a repayment that's 7 days overdue
        overdue_7_date = today - timedelta(days=7)
        overdue_7_repayment = RepaymentFactory(
            application=application,
            due_date=overdue_7_date,
            amount=2000,
            paid_date=None,
            overdue_7_day_sent=False
        )
        
        # Create a repayment that's 10 days overdue
        overdue_10_date = today - timedelta(days=10)
        overdue_10_repayment = RepaymentFactory(
            application=application,
            due_date=overdue_10_date,
            amount=2500,
            paid_date=None,
            overdue_10_day_sent=False
        )
        
        return {
            'borrower_user': borrower_user,
            'borrower': borrower,
            'application': application,
            'upcoming_repayment': upcoming_repayment,
            'overdue_3_repayment': overdue_3_repayment,
            'overdue_7_repayment': overdue_7_repayment,
            'overdue_10_repayment': overdue_10_repayment
        }
