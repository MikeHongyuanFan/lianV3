import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from brokers.models import Broker, BDM
from borrowers.models import Borrower
from applications.models import Application
from documents.models import Document, Note, Fee, Repayment
from users.models import Notification, NotificationPreference
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user():
    return User.objects.create_user(
        username='admin',
        email='admin@example.com',
        password='password123',
        role='admin',
        is_staff=True,
        is_superuser=True,
        first_name='Admin',
        last_name='User'
    )

@pytest.fixture
def broker_user():
    return User.objects.create_user(
        username='broker',
        email='broker@example.com',
        password='password123',
        role='broker',
        first_name='Broker',
        last_name='User'
    )

@pytest.fixture
def bd_user():
    return User.objects.create_user(
        username='bd',
        email='bd@example.com',
        password='password123',
        role='bd',
        first_name='BD',
        last_name='User'
    )

@pytest.fixture
def client_user():
    return User.objects.create_user(
        username='client',
        email='client@example.com',
        password='password123',
        role='client',
        first_name='Client',
        last_name='User'
    )

@pytest.fixture
def broker(broker_user):
    return Broker.objects.create(
        user=broker_user,
        name="Test Broker",
        company="Test Broker Company"
    )

@pytest.fixture
def bdm(bd_user):
    return BDM.objects.create(
        user=bd_user,
        name="Test BDM",
        email="bd@example.com"
    )

@pytest.fixture
def borrower(client_user):
    return Borrower.objects.create(
        user=client_user,
        first_name="Test",
        last_name="Borrower",
        email="client@example.com"
    )

@pytest.fixture
def application(broker, bdm):
    app = Application.objects.create(
        reference_number="APP-001",
        application_type="residential",
        purpose="Purchase",
        loan_amount=500000,
        loan_term=30,
        repayment_frequency="monthly",
        broker=broker,
        bd=bdm,
        stage="application_received"
    )
    return app

@pytest.fixture
def document(application, admin_user):
    # Create a simple PDF file
    file_content = b'%PDF-1.4\n1 0 obj\n<</Type/Catalog/Pages 2 0 R>>\nendobj\n2 0 obj\n<</Type/Pages/Kids[3 0 R]/Count 1>>\nendobj\n3 0 obj\n<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<<>>>>\nendobj\nxref\n0 4\n0000000000 65535 f\n0000000010 00000 n\n0000000053 00000 n\n0000000102 00000 n\ntrailer\n<</Size 4/Root 1 0 R>>\nstartxref\n178\n%%EOF\n'
    pdf_file = SimpleUploadedFile("test_document.pdf", file_content, content_type="application/pdf")
    
    doc = Document.objects.create(
        title="Test Document",
        description="This is a test document",
        document_type="application_form",
        file=pdf_file,
        file_name="test_document.pdf",
        file_size=len(file_content),
        file_type="application/pdf",
        application=application,
        created_by=admin_user
    )
    return doc

@pytest.fixture
def note(application, admin_user):
    return Note.objects.create(
        content="This is a test note",
        application=application,
        created_by=admin_user
    )

@pytest.fixture
def fee(application, admin_user):
    return Fee.objects.create(
        fee_type="application_fee",
        amount=1500,
        application=application,
        created_by=admin_user
    )

@pytest.fixture
def repayment(application, admin_user):
    return Repayment.objects.create(
        amount=2000,
        due_date='2025-05-15',
        application=application,
        created_by=admin_user
    )

@pytest.fixture
def notification(client_user):
    return Notification.objects.create(
        user=client_user,
        title="Test Notification",
        message="This is a test notification",
        notification_type="application_status",
        related_object_id=1,
        related_object_type="application"
    )

@pytest.fixture
def notification_preference(client_user):
    return NotificationPreference.objects.create(
        user=client_user,
        email_notifications=True,
        application_status=True,
        document_uploaded=True,
        payment_received=True,
        payment_due=True
    )
