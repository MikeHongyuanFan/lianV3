"""
Integration tests for application services implementation.
"""
import pytest
from django.contrib.auth import get_user_model
from applications.services_impl import (
    generate_document, 
    generate_repayment_schedule, 
    create_standard_fees,
    validate_application_schema,
    update_application_stage,
    process_signature_data,
    calculate_repayment_schedule
)
from applications.models import Application
from documents.models import Document, Fee, Repayment, Note
from users.models import Notification
from django.utils import timezone
import os
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

User = get_user_model()

@pytest.fixture
def admin_user():
    """Create an admin user for testing."""
    return User.objects.create_user(
        username="admin",
        email="admin@example.com",
        password="password123",
        first_name="Admin",
        last_name="User",
        role="admin"
    )

@pytest.fixture
def application(admin_user):
    """Create a test application."""
    return Application.objects.create(
        reference_number="APP-TEST-001",
        application_type="residential",
        purpose="Home purchase",
        loan_amount=500000.00,
        loan_term=360,
        interest_rate=3.50,
        repayment_frequency="monthly",
        stage="draft",
        created_by=admin_user,
        estimated_settlement_date=datetime.now().date()
    )

@pytest.mark.django_db
def test_generate_document(application, admin_user):
    """Test generating a document for an application."""
    # Mock the render_to_string function to avoid template not found error
    with patch('applications.services_impl.render_to_string', return_value="<html>Test</html>"):
        with patch('os.makedirs'):  # Mock directory creation
            with patch('builtins.open', MagicMock()):  # Mock file opening
                with patch('os.path.getsize', return_value=1024):  # Mock file size
                    document = generate_document(
                        application_id=application.id,
                        document_type="application_form",
                        user=admin_user
                    )
    
    # Verify document was created
    assert document is not None
    assert document.document_type == "application_form"
    assert document.application == application
    assert document.created_by == admin_user
    
    # Verify document in database
    db_document = Document.objects.get(id=document.id)
    assert db_document.document_type == "application_form"
    assert db_document.application == application

@pytest.mark.django_db
def test_generate_document_invalid_id(admin_user):
    """Test generating a document with invalid application ID."""
    document = generate_document(
        application_id=999,
        document_type="application_form",
        user=admin_user
    )
    
    assert document is None

@pytest.mark.django_db
def test_generate_document_invalid_type(application, admin_user):
    """Test generating a document with invalid document type."""
    document = generate_document(
        application_id=application.id,
        document_type="invalid_type",
        user=admin_user
    )
    
    assert document is None

@pytest.mark.django_db
def test_generate_repayment_schedule(application, admin_user):
    """Test generating a repayment schedule for an application."""
    repayments = generate_repayment_schedule(
        application_id=application.id,
        user=admin_user
    )
    
    # Verify repayments were created
    assert len(repayments) > 0
    assert len(repayments) == application.loan_term
    
    # Verify first repayment
    first_repayment = repayments[0]
    assert first_repayment.application == application
    assert first_repayment.created_by == admin_user
    assert first_repayment.amount > 0
    
    # Verify repayments in database
    db_repayments = Repayment.objects.filter(application=application)
    assert db_repayments.count() == application.loan_term

@pytest.mark.django_db
def test_generate_repayment_schedule_invalid_id(admin_user):
    """Test generating a repayment schedule with invalid application ID."""
    repayments = generate_repayment_schedule(
        application_id=999,
        user=admin_user
    )
    
    assert len(repayments) == 0

@pytest.mark.django_db
def test_create_standard_fees(application, admin_user):
    """Test creating standard fees for an application."""
    fees = create_standard_fees(
        application_id=application.id,
        user=admin_user
    )
    
    # Verify fees were created
    assert len(fees) == 4  # Should create 4 standard fees
    
    # Verify fee types
    fee_types = [fee.fee_type for fee in fees]
    assert "application" in fee_types
    assert "valuation" in fee_types
    assert "legal" in fee_types
    assert "settlement" in fee_types
    
    # Verify fees in database
    db_fees = Fee.objects.filter(application=application)
    assert db_fees.count() == 4

@pytest.mark.django_db
def test_create_standard_fees_invalid_id(admin_user):
    """Test creating standard fees with invalid application ID."""
    fees = create_standard_fees(
        application_id=999,
        user=admin_user
    )
    
    assert len(fees) == 0

@pytest.mark.django_db
def test_validate_application_schema_valid():
    """Test validating a valid application schema."""
    application_data = {
        "loan_amount": 500000.00,
        "loan_term": 360,
        "interest_rate": 3.50,
        "purpose": "Home purchase",
        "application_type": "residential",
        "repayment_frequency": "monthly"
    }
    
    is_valid, errors = validate_application_schema(application_data)
    
    assert is_valid is True
    assert errors is None

@pytest.mark.django_db
def test_validate_application_schema_invalid():
    """Test validating an invalid application schema."""
    # Missing required fields
    application_data = {
        "loan_amount": 500000.00,
        "loan_term": 360,
        # Missing interest_rate
        # Missing purpose
        "application_type": "residential"
    }
    
    is_valid, errors = validate_application_schema(application_data)
    
    assert is_valid is False
    assert errors is not None
    assert "interest_rate" in errors or "purpose" in errors

@pytest.mark.django_db
def test_update_application_stage_impl(application, admin_user):
    """Test updating an application stage using the implementation service."""
    # Initial state
    assert application.stage == "draft"
    
    # Update stage
    updated_app = update_application_stage(
        application_id=application.id,
        new_stage="submitted",
        user=admin_user
    )
    
    # Verify application was updated
    assert updated_app.stage == "submitted"
    
    # Verify application in database was updated
    refreshed_app = Application.objects.get(id=application.id)
    assert refreshed_app.stage == "submitted"
    
    # Verify a note was created
    notes = refreshed_app.notes.all()
    assert notes.count() == 1
    assert "Application stage changed from" in notes.first().content
    
    # Verify notifications were created
    notifications = Notification.objects.filter(
        notification_type="application_status",
        related_object_id=application.id
    )
    assert notifications.exists()

@pytest.mark.django_db
def test_process_signature_data_impl(application, admin_user):
    """Test processing signature data using the implementation service."""
    # Initial state
    assert application.signed_by is None
    assert application.signature_date is None
    
    # Process signature
    signature_data = "data:image/png;base64,test_signature_data"
    signed_by = "John Doe"
    
    updated_app = process_signature_data(
        application_id=application.id,
        signature_data=signature_data,
        signed_by=signed_by,
        user=admin_user
    )
    
    # Verify application was updated
    assert updated_app.signed_by == signed_by
    assert updated_app.signature_date is not None
    
    # Verify application in database was updated
    refreshed_app = Application.objects.get(id=application.id)
    assert refreshed_app.signed_by == signed_by
    assert refreshed_app.signature_date is not None
    
    # Verify a note was created
    notes = refreshed_app.notes.all()
    assert notes.count() == 1
    assert "Application signed by" in notes.first().content
    
    # Verify notifications were created
    notifications = Notification.objects.filter(
        notification_type="signature_required",
        related_object_id=application.id
    )
    assert notifications.exists()

@pytest.mark.django_db
def test_calculate_repayment_schedule():
    """Test calculating a repayment schedule."""
    loan_amount = 500000.00
    loan_term = 360
    interest_rate = 3.50
    
    schedule = calculate_repayment_schedule(loan_amount, loan_term, interest_rate)
    
    # Verify schedule was created
    assert len(schedule) == loan_term
    
    # Verify each repayment has an amount
    for repayment in schedule:
        assert "amount" in repayment
        assert repayment["amount"] > 0
