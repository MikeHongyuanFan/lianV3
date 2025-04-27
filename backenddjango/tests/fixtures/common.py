"""
Common test fixtures for both unit and integration tests.
"""
import pytest
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """Return an authenticated API client."""
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, admin_user):
    """Return an authenticated API client."""
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def broker_client(api_client, broker_user):
    """Return an API client authenticated as a broker."""
    api_client.force_authenticate(user=broker_user)
    return api_client


@pytest.fixture
def staff_client(api_client, staff_user):
    """Return an API client authenticated as a staff member."""
    api_client.force_authenticate(user=staff_user)
    return api_client


@pytest.fixture
def client_client(api_client, client_user):
    """Return an API client authenticated as a client."""
    api_client.force_authenticate(user=client_user)
    return api_client


@pytest.fixture
def sample_pdf():
    """Return a sample PDF file."""
    with tempfile.NamedTemporaryFile(suffix='.pdf') as temp_file:
        temp_file.write(b'Test PDF content')
        temp_file.seek(0)
        return SimpleUploadedFile(
            'test.pdf',
            temp_file.read(),
            content_type='application/pdf'
        )


@pytest.fixture
def sample_image():
    """Return a sample image file."""
    with tempfile.NamedTemporaryFile(suffix='.jpg') as temp_file:
        temp_file.write(b'Test image content')
        temp_file.seek(0)
        return SimpleUploadedFile(
            'test.jpg',
            temp_file.read(),
            content_type='image/jpeg'
        )


@pytest.fixture
def future_date():
    """Return a date in the future."""
    return timezone.now().date() + timedelta(days=30)


@pytest.fixture
def past_date():
    """Return a date in the past."""
    return timezone.now().date() - timedelta(days=30)


@pytest.fixture
def sample_application_data():
    """Return sample data for creating an application."""
    return {
        'reference_number': 'APP-TEST-002',
        'stage': 'assessment',
        'loan_amount': 500000,
        'loan_term': 360,
        'interest_rate': 4.5,
        'purpose': 'Home purchase',
        'application_type': 'residential',
    }


@pytest.fixture
def sample_borrower_data():
    """Return sample data for creating a borrower."""
    return {
        'first_name': 'Jane',
        'last_name': 'Smith',
        'email': 'jane@example.com',
        'phone': '0987654321',
        'residential_address': '456 Other St',
        'is_company': False,
    }


@pytest.fixture
def sample_company_borrower_data():
    """Return sample data for creating a company borrower."""
    return {
        'first_name': 'Company',
        'last_name': 'Ltd',
        'email': 'company@example.com',
        'phone': '0987654321',
        'residential_address': '456 Company St',
        'is_company': True,
        'company_name': 'Test Company Ltd',
        'company_abn': '98765432109',
        'company_acn': '987654321',
        'company_address': '456 Company St',
    }


@pytest.fixture
def sample_document_data():
    """Return sample data for creating a document."""
    return {
        'title': 'Test Document',
        'description': 'Test description',
        'document_type': 'application_form',
    }


@pytest.fixture
def sample_fee_data():
    """Return sample data for creating a fee."""
    return {
        'fee_type': 'application',
        'description': 'Application Fee',
        'amount': 500.00,
        'due_date': timezone.now().date(),
    }


@pytest.fixture
def sample_notification_data():
    """Return sample data for creating a notification."""
    return {
        'title': 'Test Notification',
        'message': 'This is a test notification',
        'notification_type': 'application_status',
    }
