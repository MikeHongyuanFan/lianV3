import pytest
from django.contrib.auth import get_user_model
from applications.models import Application
from brokers.models import Broker, Branch, BDM
from borrowers.models import Borrower, Guarantor

User = get_user_model()


@pytest.fixture
def admin_user():
    """Create an admin user for testing"""
    return User.objects.create_user(
        username='adminuser',
        email='admin@example.com',
        password='password123',
        role='admin',
        is_staff=True,
        is_superuser=True
    )


@pytest.fixture
def broker_user():
    """Create a broker user for testing"""
    user = User.objects.create_user(
        username='brokeruser',
        email='broker@example.com',
        password='password123',
        role='broker'
    )
    broker = Broker.objects.create(user=user, name='Test Broker')
    # Refresh the user to ensure the broker relationship is loaded
    user.refresh_from_db()
    return user


@pytest.fixture
def borrower_user():
    """Create a borrower user for testing"""
    user = User.objects.create_user(
        username='borroweruser',
        email='borrower@example.com',
        password='password123',
        role='client'  # Changed from 'borrower' to 'client' to match ROLE_CHOICES
    )
    borrower = Borrower.objects.create(
        user=user,
        first_name='John',
        last_name='Doe',
        email='john.doe@example.com',
        phone='0412345678',
        date_of_birth='1990-01-01',
        residential_address='123 Test Street',
        employer_name='Test Company',
        job_title='Software Engineer',
        annual_income=120000.00,
        employment_duration=3.5
    )
    # Refresh the user to ensure the borrower relationship is loaded
    user.refresh_from_db()
    return user


@pytest.fixture
def application(broker_user, borrower_user):
    """Create a test application"""
    broker = broker_user.broker_profile  # Changed from broker_user.broker to broker_user.broker_profile
    borrower = borrower_user.borrower  # This might need to be adjusted based on the actual relationship
    return Application.objects.create(
        application_type='residential',
        purpose='Home purchase',
        loan_amount=500000.00,
        loan_term=360,
        interest_rate=3.50,
        repayment_frequency='monthly',
        broker=broker,
        borrower=borrower,
        stage='inquiry'
    )


@pytest.fixture
def guarantor(borrower_user):
    """Create a test guarantor"""
    borrower = borrower_user.borrower  # This might need to be adjusted based on the actual relationship
    return Guarantor.objects.create(
        borrower=borrower,
        first_name='Jane',
        last_name='Smith',
        email='jane.smith@example.com',
        phone='0498765432',
        date_of_birth='1985-05-15',
        relationship='spouse',
        residential_address='123 Test Street',
        employer_name='Another Company',
        job_title='Manager',
        annual_income=150000.00,
        employment_duration=5.0
    )


@pytest.fixture
def branch(broker_user):
    """Create a test branch"""
    broker = broker_user.broker_profile  # Changed from broker_user.broker to broker_user.broker_profile
    return Branch.objects.create(
        name='Test Branch',
        address='456 Branch Street',
        phone='0287654321',
        email='branch@example.com'
    )


@pytest.fixture
def bdm():
    """Create a test BDM (Business Development Manager)"""
    user = User.objects.create_user(
        username='bdmuser',
        email='bdm@example.com',
        password='password123',
        role='bd'  # Changed from 'bdm' to 'bd' to match ROLE_CHOICES
    )
    return BDM.objects.create(
        user=user,
        name='Test BDM',
        phone='0412345678',
        email='bdm@example.com'
    )
