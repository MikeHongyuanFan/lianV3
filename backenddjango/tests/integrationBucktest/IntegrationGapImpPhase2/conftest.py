"""
Pytest configuration for Phase 2 integration tests focusing on background tasks and async operations.
"""
import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from applications.models import Application
from borrowers.models import Borrower
from brokers.models import Broker
from documents.models import Note, Repayment
from celery.contrib.testing.worker import start_worker
from crm_backend.celery import app as celery_app
from datetime import timedelta

User = get_user_model()

@pytest.fixture(scope='session')
def celery_config():
    """Configure Celery for testing"""
    return {
        'broker_url': 'memory://',
        'result_backend': 'cache',
        'cache_backend': 'memory',
        'task_always_eager': True,  # Execute tasks synchronously for testing
    }

@pytest.fixture(scope='session')
def celery_worker():
    """Mock Celery worker for testing"""
    # Instead of starting an actual worker, we'll just use eager mode
    # This avoids the need for Redis connection
    yield None

@pytest.fixture
def admin_user(db):
    """Create an admin user for testing"""
    user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpassword'
    )
    return user

@pytest.fixture
def broker_user(db):
    """Create a broker user for testing"""
    user = User.objects.create_user(
        username='broker',
        email='broker@example.com',
        password='brokerpassword'
    )
    user.role = 'broker'
    user.save()
    return user

@pytest.fixture
def bd_user(db):
    """Create a business development user for testing"""
    user = User.objects.create_user(
        username='bd',
        email='bd@example.com',
        password='bdpassword'
    )
    user.role = 'bd'
    user.save()
    return user

@pytest.fixture
def borrower_user(db):
    """Create a borrower user for testing"""
    user = User.objects.create_user(
        username='borrower',
        email='borrower@example.com',
        password='borrowerpassword'
    )
    user.role = 'borrower'
    user.save()
    return user

@pytest.fixture
def broker_instance(broker_user):
    """Create a broker instance for testing"""
    broker = Broker.objects.create(
        name='Test Broker',
        company='Test Broker Company',
        phone='1234567890',
        user=broker_user
    )
    return broker

@pytest.fixture
def bd_instance(bd_user):
    """Create a BD instance for testing"""
    from brokers.models import BDM
    bd = BDM.objects.create(
        name='Test BD',
        phone='0987654321',
        user=bd_user
    )
    return bd

@pytest.fixture
def borrower_instance(borrower_user):
    """Create a borrower instance for testing"""
    borrower = Borrower.objects.create(
        first_name='Test',
        last_name='Borrower',
        email='borrower@example.com',
        phone='1234567890',
        user=borrower_user
    )
    return borrower

@pytest.fixture
def application_instance(broker_instance, bd_instance):
    """Create an application instance for testing"""
    application = Application.objects.create(
        reference_number='TEST-APP-001',
        loan_amount=100000,
        loan_term=12,
        interest_rate=5.5,
        stage='inquiry',  # Using a valid stage from the model
        broker=broker_instance,
        bd=bd_instance
    )
    return application

@pytest.fixture
def stale_application(broker_instance, bd_instance):
    """Create a stale application for testing"""
    application = Application.objects.create(
        reference_number='STALE-APP-001',
        loan_amount=200000,
        loan_term=24,
        interest_rate=6.0,
        stage='inquiry',  # Using a valid stage that's not in the excluded list
        broker=broker_instance,
        bd=bd_instance,
        created_at=timezone.now() - timedelta(days=30),
        updated_at=timezone.now() - timedelta(days=20)
    )
    return application

@pytest.fixture
def note_with_reminder(application_instance, admin_user):
    """Create a note with a reminder for testing"""
    note = Note.objects.create(
        title='Test Note with Reminder',
        content='This is a test note with a reminder',
        application=application_instance,
        created_by=admin_user,
        remind_date=timezone.now().date()
    )
    return note

@pytest.fixture
def repayment_instance(application_instance):
    """Create a repayment instance for testing"""
    repayment = Repayment.objects.create(
        application=application_instance,
        amount=10000,
        due_date=timezone.now().date() + timedelta(days=7),
        reminder_sent=False
    )
    return repayment

@pytest.fixture
def overdue_repayment_3_days(application_instance):
    """Create a repayment that is 3 days overdue"""
    repayment = Repayment.objects.create(
        application=application_instance,
        amount=10000,
        due_date=timezone.now().date() - timedelta(days=3),
        reminder_sent=True,
        overdue_3_day_sent=False
    )
    return repayment

@pytest.fixture
def overdue_repayment_7_days(application_instance):
    """Create a repayment that is 7 days overdue"""
    repayment = Repayment.objects.create(
        application=application_instance,
        amount=10000,
        due_date=timezone.now().date() - timedelta(days=7),
        reminder_sent=True,
        overdue_3_day_sent=True,
        overdue_7_day_sent=False
    )
    return repayment

@pytest.fixture
def overdue_repayment_10_days(application_instance):
    """Create a repayment that is 10 days overdue"""
    repayment = Repayment.objects.create(
        application=application_instance,
        amount=10000,
        due_date=timezone.now().date() - timedelta(days=10),
        reminder_sent=True,
        overdue_3_day_sent=True,
        overdue_7_day_sent=True,
        overdue_10_day_sent=False
    )
    return repayment
