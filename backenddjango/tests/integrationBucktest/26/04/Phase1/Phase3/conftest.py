import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from borrowers.models import Borrower, Guarantor
from brokers.models import Broker, Branch, BDM
from applications.models import Application, Document, Fee, Repayment
from documents.models import Document as DocumentModel
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

User = get_user_model()

@pytest.fixture
def admin_user(db):
    """Create an admin user for testing"""
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpassword',
        first_name='Admin',
        last_name='User',
        role='admin'
    )

@pytest.fixture
def broker_user(db):
    """Create a broker user for testing"""
    return User.objects.create_user(
        username='broker',
        email='broker@example.com',
        password='brokerpassword',
        first_name='Broker',
        last_name='User',
        role='broker'
    )

@pytest.fixture
def client_user(db):
    """Create a client user for testing"""
    return User.objects.create_user(
        username='client',
        email='client@example.com',
        password='clientpassword',
        first_name='Client',
        last_name='User',
        role='client'
    )

@pytest.fixture
def admin_client(admin_user):
    """Create an authenticated admin client"""
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client

@pytest.fixture
def broker_client(broker_user):
    """Create an authenticated broker client"""
    client = APIClient()
    client.force_authenticate(user=broker_user)
    return client

@pytest.fixture
def client_client(client_user):
    """Create an authenticated client client"""
    client = APIClient()
    client.force_authenticate(user=client_user)
    return client

@pytest.fixture
def broker_instance(db, broker_user):
    """Create a broker instance for testing"""
    return Broker.objects.create(
        user=broker_user,
        name='Test Broker',
        company='Test Broker Company',
        phone='1234567890',
        email='broker@example.com'
    )

@pytest.fixture
def branch_instance(db, broker_instance):
    """Create a branch instance for testing"""
    return Branch.objects.create(
        name='Test Branch',
        address='123 Branch St',
        phone='1234567890',
        email='branch@example.com',
        broker=broker_instance
    )

@pytest.fixture
def borrower_instance(db, client_user):
    """Create a borrower instance for testing"""
    return Borrower.objects.create(
        user=client_user,
        first_name='John',
        last_name='Doe',
        email='john.doe@example.com',
        phone='1234567890',
        date_of_birth='1980-01-01',
        residential_address='123 Main St'
    )

@pytest.fixture
def guarantor_instance(db):
    """Create a guarantor instance for testing"""
    return Guarantor.objects.create(
        first_name='Jane',
        last_name='Smith',
        email='jane.smith@example.com',
        phone='0987654321',
        date_of_birth='1985-05-05',
        address='456 Oak St',
        guarantor_type='individual'
    )

@pytest.fixture
def application_instance(db, broker_instance):
    """Create an application instance for testing"""
    return Application.objects.create(
        application_type='residential',
        purpose='Home purchase',
        loan_amount=500000.00,
        loan_term=360,
        interest_rate=3.50,
        repayment_frequency='monthly',
        broker=broker_instance,
        stage='inquiry'
    )

@pytest.fixture
def application_instance_for_broker(db, broker_instance):
    """Create an application instance assigned to the broker for testing"""
    return Application.objects.create(
        application_type='commercial',
        purpose='Business expansion',
        loan_amount=750000.00,
        loan_term=240,
        interest_rate=4.25,
        repayment_frequency='monthly',
        broker=broker_instance,
        stage='inquiry'
    )

@pytest.fixture
def document_instance(db, application_instance):
    """Create a document instance for testing"""
    # Create a simple text file for testing
    test_file = SimpleUploadedFile("test_document.txt", b"Test document content", content_type="text/plain")
    
    return DocumentModel.objects.create(
        title='Test Document',
        description='This is a test document',
        document_type='application_form',
        file=test_file,
        file_name='test_document.txt',
        file_size=len(b"Test document content"),
        file_type='text/plain',
        application=application_instance
    )

@pytest.fixture
def fee_instance(db, application_instance, admin_user):
    """Create a fee instance for testing"""
    return Fee.objects.create(
        fee_type='application',
        description='Application fee',
        amount=1500.00,
        due_date=timezone.now().date(),
        application=application_instance,
        created_by=admin_user
    )

@pytest.fixture
def repayment_instance(db, application_instance, admin_user):
    """Create a repayment instance for testing"""
    return Repayment.objects.create(
        amount=2500.00,
        due_date=timezone.now().date(),
        application=application_instance,
        created_by=admin_user
    )
