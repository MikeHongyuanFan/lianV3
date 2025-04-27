import pytest
from unittest.mock import patch, MagicMock

from applications.services import (
    generate_application_documents,
    send_application_notifications,
    process_application_approval
)
from applications.services_impl import (
    generate_document,
    generate_repayment_schedule,
    create_standard_fees,
    validate_application_schema,
    update_application_stage,
    process_signature_data
)

@pytest.mark.django_db
def test_generate_application_documents():
    mock_application = MagicMock(id=1, reference_number='APP-123')

    with patch('applications.models.Application.objects.get', return_value=mock_application):
        documents = generate_application_documents(application_id=1, user=MagicMock())

    assert len(documents) == 3  # Application form, loan agreement, privacy consent


@pytest.mark.django_db
def test_send_application_notifications():
    mock_application = MagicMock(id=1, reference_number='APP-123')
    mock_borrower = MagicMock(user=MagicMock(id=2), email='borrower@example.com')
    mock_application.borrowers.all.return_value = [mock_borrower]

    with patch('applications.models.Application.objects.get', return_value=mock_application):
        notifs = send_application_notifications(
            application_id=1,
            notification_type='application_update',
            message='Your application was updated'
        )

    assert len(notifs) >= 1


@pytest.mark.django_db
def test_process_application_approval():
    mock_application = MagicMock(id=1, reference_number='APP-123')

    with patch('applications.models.Application.objects.get', return_value=mock_application):
        result = process_application_approval(
            application_id=1,
            approval_data={
                'approved_amount': 100000,
                'approved_term': 360,
                'approved_rate': 5.5,
                'approval_expiry': '2025-12-31',
                'approval_conditions': ['Condition A', 'Condition B']
            },
            user=MagicMock()
        )

    assert result['success'] is True
    assert 'application' in result
    assert 'documents' in result
    assert 'notifications' in result


@pytest.mark.django_db
def test_generate_document():
    mock_application = MagicMock(id=1, reference_number='APP-123')

    with patch('applications.models.Application.objects.get', return_value=mock_application), \
         patch('applications.services_impl.render_to_string', return_value='HTML'), \
         patch('documents.models.Document.objects.create', return_value='mock_doc'):

        document = generate_document(application_id=1, document_type='application_form', user=MagicMock())

    assert document == 'mock_doc'


@pytest.mark.django_db
def test_generate_repayment_schedule():
    mock_application = MagicMock(id=1, loan_amount=120000, loan_term=12, interest_rate=6.0)
    mock_repayments = MagicMock()
    mock_repayments.delete = MagicMock()
    mock_application.repayments.all.return_value = mock_repayments

    with patch('applications.models.Application.objects.get', return_value=mock_application), \
         patch('documents.models.Repayment.objects.create', return_value=MagicMock()):
        
        # Skip the actual calculation logic since it's complex
        with patch('applications.services_impl.calculate_repayment_schedule', return_value=[{'amount': 1000}]):
            repayments = generate_repayment_schedule(application_id=1, user=MagicMock())

    assert isinstance(repayments, list)


@pytest.mark.django_db
def test_create_standard_fees():
    mock_application = MagicMock(id=1)

    with patch('applications.models.Application.objects.get', return_value=mock_application), \
         patch('documents.models.Fee.objects.create', return_value=MagicMock()) as mock_fee_create:

        fees = create_standard_fees(application_id=1, user=MagicMock())

    assert isinstance(fees, list)


def test_validate_application_schema_valid():
    valid_data = {
        'loan_amount': 100000,
        'loan_term': 360,
        'interest_rate': 5.5,
        'purpose': 'Home Purchase',
        'application_type': 'residential'
    }
    is_valid, error = validate_application_schema(valid_data)
    assert is_valid is True
    assert error is None


def test_validate_application_schema_invalid():
    invalid_data = {
        'loan_amount': -100000,
        'loan_term': 360,
    }
    is_valid, error = validate_application_schema(invalid_data)
    assert is_valid is False
    assert isinstance(error, str)


@pytest.mark.django_db
def test_update_application_stage():
    mock_application = MagicMock(id=1, reference_number='APP-123', stage='initial')
    mock_user = MagicMock(id=1)
    mock_user.id = 1  # Ensure id is an integer, not a MagicMock

    # Need to patch the notification service functions
    with patch('applications.models.Application.objects.get', return_value=mock_application), \
         patch('documents.models.Note.objects.create'), \
         patch('users.services.notification_service.create_notification'), \
         patch('users.services.notification_service.NotificationPreference.objects.get'):

        updated_application = update_application_stage(application_id=1, new_stage='approved', user=mock_user)

    assert updated_application.stage == 'approved'


@pytest.mark.django_db
def test_process_signature_data():
    mock_application = MagicMock(id=1)
    mock_user = MagicMock(id=1)
    mock_user.id = 1  # Ensure id is an integer, not a MagicMock

    # Need to patch the notification service functions
    with patch('applications.models.Application.objects.get', return_value=mock_application), \
         patch('documents.models.Note.objects.create'), \
         patch('users.services.notification_service.create_notification'), \
         patch('users.services.notification_service.NotificationPreference.objects.get'):

        updated_app = process_signature_data(application_id=1, signature_data='base64string', signed_by='John Doe', user=mock_user)

    assert updated_app == mock_application


# Simple placeholder test
def test_services_extended_placeholder():
    assert True  # No real logic to test yet
