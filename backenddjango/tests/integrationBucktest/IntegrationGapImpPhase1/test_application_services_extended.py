"""
Integration tests for extended application services.
"""
import pytest
from django.contrib.auth import get_user_model
from applications.services_extended import (
    calculate_loan_metrics,
    validate_borrower_eligibility,
    generate_application_documents,
    send_application_notifications,
    process_application_approval
)
from applications.models import Application
from borrowers.models import Borrower, Asset, Liability
from documents.models import Document
from users.models import Notification
from django.utils import timezone
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
def borrower_user():
    """Create a borrower user for testing."""
    return User.objects.create_user(
        username="borrower",
        email="borrower@example.com",
        password="password123",
        first_name="Borrower",
        last_name="User",
        role="borrower"
    )

@pytest.fixture
def broker_user():
    """Create a broker user for testing."""
    return User.objects.create_user(
        username="broker",
        email="broker@example.com",
        password="password123",
        first_name="Broker",
        last_name="User",
        role="broker"
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
        security_value=625000.00  # 80% LTV
    )

@pytest.fixture
def borrower(application, borrower_user):
    """Create a test borrower with financial information."""
    borrower = Borrower.objects.create(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="1234567890",
        date_of_birth="1980-01-01",
        annual_income=120000.00,
        monthly_expenses=3000.00,
        user=borrower_user,
        created_by=application.created_by
    )
    
    # Add borrower to application
    application.borrowers.add(borrower)
    
    # Create assets
    Asset.objects.create(
        borrower=borrower,
        asset_type="property",
        description="Primary Residence",
        value=600000.00,
        created_by=application.created_by
    )
    
    Asset.objects.create(
        borrower=borrower,
        asset_type="savings",
        description="Savings Account",
        value=50000.00,
        created_by=application.created_by
    )
    
    # Create liabilities
    Liability.objects.create(
        borrower=borrower,
        liability_type="mortgage",
        description="Existing Mortgage",
        amount=400000.00,
        monthly_payment=2000.00,
        created_by=application.created_by
    )
    
    return borrower

@pytest.mark.django_db
def test_calculate_loan_metrics(application):
    """Test calculating loan metrics for an application."""
    metrics = calculate_loan_metrics(application.id)
    
    # Verify metrics were calculated
    assert metrics is not None
    assert "monthly_repayment" in metrics
    assert "total_repayment" in metrics
    assert "total_interest" in metrics
    assert "loan_to_value_ratio" in metrics
    
    # Verify specific metrics
    assert metrics["monthly_repayment"] > 0
    assert metrics["total_repayment"] > application.loan_amount
    assert metrics["total_interest"] > 0
    assert metrics["loan_to_value_ratio"] == 80.0  # 500000/625000 * 100

@pytest.mark.django_db
def test_calculate_loan_metrics_invalid_id():
    """Test calculating loan metrics with invalid application ID."""
    metrics = calculate_loan_metrics(999)
    
    assert metrics is None

@pytest.mark.django_db
def test_validate_borrower_eligibility(application, borrower):
    """Test validating borrower eligibility for a loan."""
    eligibility = validate_borrower_eligibility(application.id)
    
    # Verify eligibility was calculated
    assert eligibility is not None
    assert "is_eligible" in eligibility
    assert "debt_to_income_ratio" in eligibility
    assert "serviceability_ratio" in eligibility
    assert "reasons" in eligibility
    
    # Verify specific eligibility metrics
    assert isinstance(eligibility["is_eligible"], bool)
    assert eligibility["debt_to_income_ratio"] > 0
    assert eligibility["serviceability_ratio"] > 0

@pytest.mark.django_db
def test_validate_borrower_eligibility_invalid_id():
    """Test validating borrower eligibility with invalid application ID."""
    eligibility = validate_borrower_eligibility(999)
    
    assert eligibility is not None
    assert eligibility["is_eligible"] is False
    assert "Application not found" in eligibility["reasons"]

@pytest.mark.django_db
def test_validate_borrower_eligibility_no_borrowers(application):
    """Test validating borrower eligibility with no borrowers."""
    # Remove any borrowers
    application.borrowers.clear()
    
    eligibility = validate_borrower_eligibility(application.id)
    
    assert eligibility is not None
    assert eligibility["is_eligible"] is False
    assert "No borrowers associated with this application" in eligibility["reasons"]

@pytest.mark.django_db
def test_generate_application_documents(application, admin_user):
    """Test generating application documents."""
    documents = generate_application_documents(application.id, admin_user)
    
    # Verify documents were created
    assert len(documents) > 0
    
    # Verify document types
    document_types = [doc.document_type for doc in documents]
    assert "application_form" in document_types
    assert "loan_agreement" in document_types
    assert "privacy_consent" in document_types
    
    # Verify documents in database
    db_documents = Document.objects.filter(application=application)
    assert db_documents.count() >= 3

@pytest.mark.django_db
def test_generate_application_documents_invalid_id(admin_user):
    """Test generating application documents with invalid application ID."""
    documents = generate_application_documents(999, admin_user)
    
    assert len(documents) == 0

@pytest.mark.django_db
def test_send_application_notifications(application, borrower, admin_user):
    """Test sending application notifications."""
    # Mock the send_email_notification and send_websocket_notification functions
    with patch('applications.services_extended.send_email_notification') as mock_email:
        with patch('applications.services_extended.send_websocket_notification') as mock_websocket:
            # Set up the mocks
            mock_email.return_value = True
            mock_websocket.return_value = True
            
            # Call the function
            notifications = send_application_notifications(
                application_id=application.id,
                notification_type="application_status",
                message="Application status has been updated",
                include_borrowers=True,
                include_broker=False,  # Don't include broker since we don't have a proper Broker instance
                include_bd=False  # Don't include BD since we don't have a proper BD instance
            )
            
            # Verify notifications were created for borrowers
            assert len(notifications) > 0
            
            # Verify notifications in database
            db_notifications = Notification.objects.filter(
                notification_type="application_status",
                related_object_id=application.id
            )
            assert db_notifications.count() > 0

@pytest.mark.django_db
def test_send_application_notifications_invalid_id():
    """Test sending application notifications with invalid application ID."""
    notifications = send_application_notifications(
        application_id=999,
        notification_type="application_status",
        message="Application status has been updated"
    )
    
    assert len(notifications) == 0

@pytest.mark.django_db
def test_process_application_approval(application, admin_user):
    """Test processing application approval."""
    # Mock the imported update_application_stage function
    with patch('applications.services_impl.update_application_stage', return_value=application) as mock_impl_update:
        # Mock the generate_application_documents function
        with patch('applications.services_extended.generate_application_documents', return_value=[]) as mock_generate_docs:
            # Mock the send_application_notifications function
            with patch('applications.services_extended.send_application_notifications', return_value=[]) as mock_send_notifications:
                # Mock Note.objects.create
                with patch('documents.models.Note.objects.create') as mock_create_note:
                    approval_data = {
                        "approved_amount": 480000.00,
                        "approved_term": 300,
                        "approved_rate": 3.25,
                        "approval_expiry": (datetime.now() + timedelta(days=90)).date(),
                        "approval_conditions": [
                            "Proof of income required",
                            "Property valuation required",
                            "Insurance policy required"
                        ]
                    }
                    
                    result = process_application_approval(
                        application_id=application.id,
                        approval_data=approval_data,
                        user=admin_user
                    )
                    
                    # Verify result structure
                    assert "success" in result
                    assert result.get("success") is True

@pytest.mark.django_db
def test_process_application_approval_invalid_id(admin_user):
    """Test processing application approval with invalid application ID."""
    approval_data = {
        "approved_amount": 480000.00,
        "approved_term": 300,
        "approved_rate": 3.25,
        "approval_expiry": (datetime.now() + timedelta(days=90)).date()
    }
    
    result = process_application_approval(
        application_id=999,
        approval_data=approval_data,
        user=admin_user
    )
    
    assert result["success"] is False
    assert "error" in result
    assert "Application not found" in result["error"]
