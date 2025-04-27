"""
Tests for application services.
"""
import pytest
import os
from unittest.mock import patch, MagicMock
from django.utils import timezone
from applications.services_impl import (
    generate_document, generate_repayment_schedule, create_standard_fees,
    validate_application_schema, update_application_stage, process_signature_data
)
from applications.models import Application
from documents.models import Document, Fee, Repayment, Note
from tests.factories import ApplicationFactory, AdminUserFactory

pytestmark = pytest.mark.django_db


@pytest.mark.service
def test_generate_document_success(admin_user, tmp_path, settings):
    """Test generating a document successfully."""
    # Set up test environment
    settings.MEDIA_ROOT = tmp_path
    
    # Create an application
    application = ApplicationFactory()
    
    # Generate document
    document = generate_document(application.id, 'application_form', admin_user)
    
    # Check that the document was created
    assert document is not None
    assert document.title == f'Application Form - {application.reference_number}'
    assert document.document_type == 'application_form'
    assert document.application == application
    assert document.created_by == admin_user
    
    # Check that the file was created
    assert os.path.exists(os.path.join(tmp_path, document.file.name))


@pytest.mark.service
def test_generate_document_invalid_type(admin_user):
    """Test generating a document with an invalid type."""
    # Create an application
    application = ApplicationFactory()
    
    # Generate document with invalid type
    document = generate_document(application.id, 'invalid_type', admin_user)
    
    # Check that no document was created
    assert document is None


@pytest.mark.service
def test_generate_document_nonexistent_application(admin_user):
    """Test generating a document for a nonexistent application."""
    # Generate document for nonexistent application
    document = generate_document(999, 'application_form', admin_user)
    
    # Check that no document was created
    assert document is None


@pytest.mark.service
def test_generate_repayment_schedule_monthly(admin_user):
    """Test generating a monthly repayment schedule."""
    # Create an application with known values
    application = ApplicationFactory(
        loan_amount=100000,
        loan_term=12,  # 1 year
        interest_rate=5.0,  # 5%
        repayment_frequency='monthly',
        estimated_settlement_date=timezone.now().date()
    )
    
    # Generate repayment schedule
    repayments = generate_repayment_schedule(application.id, admin_user)
    
    # Check that repayments were created
    assert len(repayments) == 12  # 12 monthly payments for 1 year
    
    # Check that all repayments have the correct properties
    for repayment in repayments:
        assert repayment.application == application
        assert repayment.created_by == admin_user
        assert repayment.status == 'pending'
        assert repayment.amount > 0


@pytest.mark.service
def test_generate_repayment_schedule_no_interest(admin_user):
    """Test generating a repayment schedule with no interest."""
    # Create an application with no interest
    application = ApplicationFactory(
        loan_amount=12000,
        loan_term=12,
        interest_rate=0,
        repayment_frequency='monthly',
        estimated_settlement_date=timezone.now().date()
    )
    
    # Generate repayment schedule
    repayments = generate_repayment_schedule(application.id, admin_user)
    
    # Check that repayments were created
    assert len(repayments) == 12
    
    # Check that all repayments have the correct amount (equal payments)
    for repayment in repayments:
        assert repayment.amount == 1000.0  # 12000 / 12 = 1000


@pytest.mark.service
def test_generate_repayment_schedule_nonexistent_application(admin_user):
    """Test generating a repayment schedule for a nonexistent application."""
    # Generate repayment schedule for nonexistent application
    repayments = generate_repayment_schedule(999, admin_user)
    
    # Check that no repayments were created
    assert len(repayments) == 0


@pytest.mark.service
def test_create_standard_fees(admin_user):
    """Test creating standard fees for an application."""
    # Create an application
    application = ApplicationFactory()
    
    # Create standard fees
    fees = create_standard_fees(application.id, admin_user)
    
    # Check that fees were created
    assert len(fees) == 4  # 4 standard fees
    
    # Check that all fees have the correct properties
    fee_types = set()
    for fee in fees:
        assert fee.application == application
        assert fee.created_by == admin_user
        assert fee.amount > 0
        assert not fee.is_paid
        fee_types.add(fee.fee_type)
    
    # Check that all expected fee types were created
    assert fee_types == {'application', 'valuation', 'legal', 'settlement'}


@pytest.mark.service
def test_create_standard_fees_nonexistent_application(admin_user):
    """Test creating standard fees for a nonexistent application."""
    # Create standard fees for nonexistent application
    fees = create_standard_fees(999, admin_user)
    
    # Check that no fees were created
    assert len(fees) == 0


@pytest.mark.service
def test_validate_application_schema_valid():
    """Test validating a valid application schema."""
    # Create valid application data
    application_data = {
        'loan_amount': 100000,
        'loan_term': 12,
        'interest_rate': 5.0,
        'purpose': 'Home purchase',
        'application_type': 'residential',
        'repayment_frequency': 'monthly'
    }
    
    # Validate schema
    is_valid, errors = validate_application_schema(application_data)
    
    # Check that validation passed
    assert is_valid
    assert errors is None


@pytest.mark.service
def test_validate_application_schema_invalid():
    """Test validating an invalid application schema."""
    # Create invalid application data (missing required fields)
    application_data = {
        'loan_amount': 100000,
        'loan_term': 12,
        # Missing interest_rate
        # Missing purpose
        'application_type': 'residential'
    }
    
    # Validate schema
    is_valid, errors = validate_application_schema(application_data)
    
    # Check that validation failed
    assert not is_valid
    assert errors is not None
    assert 'interest_rate' in errors or 'purpose' in errors


@pytest.mark.service
def test_validate_application_schema_invalid_values():
    """Test validating an application schema with invalid values."""
    # Create application data with invalid values
    application_data = {
        'loan_amount': -100,  # Negative loan amount
        'loan_term': 0,  # Zero loan term
        'interest_rate': 50.0,  # Interest rate too high
        'purpose': 'Home',
        'application_type': 'residential',
        'repayment_frequency': 'invalid'  # Invalid frequency
    }
    
    # Validate schema
    is_valid, errors = validate_application_schema(application_data)
    
    # Check that validation failed
    assert not is_valid
    assert errors is not None


@pytest.mark.service
def test_update_application_stage(admin_user):
    """Test updating an application stage."""
    # Create an application
    application = ApplicationFactory(stage='assessment')
    
    # Update stage
    updated_application = update_application_stage(application.id, 'approved', admin_user)
    
    # Check that the stage was updated
    assert updated_application.stage == 'approved'
    
    # Check that a note was created
    note = Note.objects.filter(application=application).first()
    assert note is not None
    assert "stage changed from 'assessment' to 'approved'" in note.content
    
    # Check that notifications were created
    # This would require mocking the create_application_notification function
    # or checking the database for created notifications


@pytest.mark.service
def test_update_application_stage_nonexistent():
    """Test updating the stage of a nonexistent application."""
    # Update stage of nonexistent application
    with pytest.raises(ValueError) as excinfo:
        update_application_stage(999, 'approved', AdminUserFactory())
    
    # Check that the correct error was raised
    assert "Application with ID 999 not found" in str(excinfo.value)


@pytest.mark.service
def test_process_signature_data(admin_user):
    """Test processing signature data for an application."""
    # Create an application
    application = ApplicationFactory()
    
    # Process signature data
    updated_application = process_signature_data(
        application_id=application.id,
        signature_data="test_signature_data",
        signed_by="John Doe",
        user=admin_user
    )
    
    # Check that the signature data was updated
    assert updated_application.signature_data == "test_signature_data"
    assert updated_application.signed_by == "John Doe"
    assert updated_application.signature_date is not None
    
    # Check that a note was created
    note = Note.objects.filter(application=application).first()
    assert note is not None
    assert "signed by John Doe" in note.content
    
    # Check that notifications were created
    # This would require mocking the create_application_notification function
    # or checking the database for created notifications


@pytest.mark.service
def test_process_signature_data_nonexistent():
    """Test processing signature data for a nonexistent application."""
    # Process signature data for nonexistent application
    with pytest.raises(ValueError) as excinfo:
        process_signature_data(
            application_id=999,
            signature_data="test_signature_data",
            signed_by="John Doe",
            user=AdminUserFactory()
        )
    
    # Check that the correct error was raised
    assert "Application with ID 999 not found" in str(excinfo.value)
