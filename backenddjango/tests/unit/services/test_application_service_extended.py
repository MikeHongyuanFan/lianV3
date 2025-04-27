"""
Extended tests for application services.
"""
import pytest
from decimal import Decimal
from unittest.mock import patch, MagicMock
from django.utils import timezone
from applications.services_extended import (
    calculate_loan_metrics,
    validate_borrower_eligibility,
    generate_application_documents,
    send_application_notifications,
    process_application_approval
)
from applications.models import Application
from documents.models import Document, Fee, Repayment, Note
from users.models import Notification
from tests.factories import (
    ApplicationFactory, BorrowerFactory, GuarantorFactory, 
    AdminUserFactory, BrokerFactory, BDMFactory
)

pytestmark = pytest.mark.django_db


@pytest.mark.service
def test_calculate_loan_metrics():
    """Test calculating loan metrics."""
    # Create test data
    application = ApplicationFactory(
        loan_amount=500000,
        loan_term=360,  # 30 years in months
        interest_rate=4.5,  # 4.5%
        repayment_frequency='monthly'
    )
    
    # Call the function
    metrics = calculate_loan_metrics(application.id)
    
    # Check the metrics
    assert metrics is not None
    assert 'monthly_repayment' in metrics
    assert 'total_repayment' in metrics
    assert 'total_interest' in metrics
    assert 'loan_to_value_ratio' in metrics
    
    # Check that the monthly repayment is calculated correctly
    # For a $500,000 loan at 4.5% over 30 years, monthly payment should be around $2,533
    assert 2500 < metrics['monthly_repayment'] < 2600
    
    # Check that the total repayment is calculated correctly
    # Total repayment should be monthly payment * term * 12
    assert metrics['total_repayment'] == pytest.approx(metrics['monthly_repayment'] * 30 * 12, rel=0.01)
    
    # Check that the total interest is calculated correctly
    # Total interest should be total repayment - loan amount
    assert metrics['total_interest'] == pytest.approx(metrics['total_repayment'] - application.loan_amount, rel=0.01)


@pytest.mark.service
def test_calculate_loan_metrics_nonexistent_application():
    """Test calculating loan metrics for a nonexistent application."""
    # Call the function with a nonexistent application ID
    metrics = calculate_loan_metrics(999)
    
    # Check that no metrics were returned
    assert metrics is None


@pytest.mark.service
def test_calculate_loan_metrics_zero_interest():
    """Test calculating loan metrics with zero interest."""
    # Create test data
    application = ApplicationFactory(
        loan_amount=100000,
        loan_term=120,  # 10 years in months
        interest_rate=0,  # 0% interest
        repayment_frequency='monthly'
    )
    
    # Call the function
    metrics = calculate_loan_metrics(application.id)
    
    # Check the metrics
    assert metrics is not None
    assert metrics['monthly_repayment'] == pytest.approx(100000 / 120, rel=0.01)  # Simple division
    assert metrics['total_repayment'] == pytest.approx(100000, rel=0.01)  # No interest
    assert metrics['total_interest'] == pytest.approx(0, rel=0.01)  # No interest


@pytest.mark.service
def test_validate_borrower_eligibility():
    """Test validating borrower eligibility."""
    # Create test data
    application = ApplicationFactory(
        loan_amount=500000,
        loan_term=360,  # 30 years in months
        interest_rate=4.5,  # 4.5%
        security_value=625000  # 80% LTV
    )
    
    borrower = BorrowerFactory(
        annual_income=120000,  # $120,000 per year
        monthly_expenses=3000,  # $3,000 per month
    )
    application.borrowers.add(borrower)
    
    # Create some liabilities
    from borrowers.models import Liability
    Liability.objects.create(
        borrower=borrower,
        liability_type='credit_card',
        amount=10000,
        monthly_payment=300
    )
    
    # Call the function
    result = validate_borrower_eligibility(application.id)
    
    # Check the result
    assert result is not None
    assert 'is_eligible' in result
    assert 'debt_to_income_ratio' in result
    assert 'serviceability_ratio' in result
    assert 'reasons' in result
    
    # For this example, the borrower should be eligible
    assert result['is_eligible'] is True
    
    # Debt to income ratio should be calculated correctly
    # Monthly debt payments: $300 (credit card)
    # Monthly income: $120,000 / 12 = $10,000
    # Debt to income ratio: $300 / $10,000 = 0.03 (3%)
    assert result['debt_to_income_ratio'] == pytest.approx(0.03, rel=0.01)
    
    # Serviceability ratio should be calculated correctly
    # Monthly income: $10,000
    # Monthly expenses: $3,000 + $300 = $3,300
    # Serviceability ratio: ($10,000 - $3,300) / estimated monthly loan payment
    assert result['serviceability_ratio'] > 1.0  # Should be able to service the loan


@pytest.mark.service
def test_validate_borrower_eligibility_ineligible():
    """Test validating borrower eligibility for an ineligible borrower."""
    # Create test data
    application = ApplicationFactory(
        loan_amount=1000000,  # $1M loan
        loan_term=360,  # 30 years in months
        interest_rate=4.5,  # 4.5%
        security_value=1100000  # High LTV
    )
    
    borrower = BorrowerFactory(
        annual_income=50000,  # $50,000 per year (too low for the loan)
        monthly_expenses=3000,  # $3,000 per month
    )
    application.borrowers.add(borrower)
    
    # Create some liabilities
    from borrowers.models import Liability
    Liability.objects.create(
        borrower=borrower,
        liability_type='credit_card',
        amount=20000,
        monthly_payment=600
    )
    
    # Call the function
    result = validate_borrower_eligibility(application.id)
    
    # Check the result
    assert result is not None
    assert result['is_eligible'] is False
    assert len(result['reasons']) > 0  # Should have reasons for ineligibility


@pytest.mark.service
@patch('documents.services_mock.generate_document_from_template')
def test_generate_application_documents(mock_generate_document):
    """Test generating application documents."""
    # Create test data
    application = ApplicationFactory()
    user = AdminUserFactory()
    
    # Mock document generation
    mock_documents = [
        MagicMock(id=1, document_type='application_form'),
        MagicMock(id=2, document_type='loan_agreement'),
        MagicMock(id=3, document_type='privacy_consent')
    ]
    mock_generate_document.side_effect = mock_documents
    
    # Call the function
    documents = generate_application_documents(application.id, user)
    
    # Check that generate_document_from_template was called for each document type
    assert mock_generate_document.call_count == 3
    
    # Check the document types that were generated
    document_types = [call_args[1]['document_type'] for call_args in mock_generate_document.call_args_list]
    assert 'application_form' in document_types
    assert 'loan_agreement' in document_types
    assert 'privacy_consent' in document_types
    
    # Check that all documents were returned
    assert len(documents) == 3


@pytest.mark.service
@patch('applications.services_extended.send_email_notification')
@patch('applications.services_extended.send_websocket_notification')
def test_send_application_notifications(mock_websocket, mock_email):
    """Test sending application notifications."""
    # Create test data
    application = ApplicationFactory(stage='approved')
    
    # Create a borrower with a user
    borrower_user = AdminUserFactory(role='client')
    borrower = BorrowerFactory(user=borrower_user, email=borrower_user.email)
    application.borrowers.add(borrower)
    
    # Create a broker with a user
    broker_user = AdminUserFactory(role='broker')
    broker = BrokerFactory(user=broker_user, email=broker_user.email)
    application.broker = broker
    application.save()
    
    # Create a BD with a user
    bd_user = AdminUserFactory(role='bd')
    bd = BDMFactory(user=bd_user, email=bd_user.email)
    application.bd = bd
    application.save()
    
    # Call the function
    notifications = send_application_notifications(
        application_id=application.id,
        notification_type='application_status',
        message='Application has been approved',
        include_borrowers=True,
        include_broker=True,
        include_bd=True
    )
    
    # Check that notifications were created for all parties
    assert len(notifications) == 3  # Borrower, broker, and BD
    
    # Check that email notifications were sent
    assert mock_email.call_count == 3
    
    # Check that websocket notifications were sent
    assert mock_websocket.call_count == 3
    
    # Check that the notifications were saved to the database
    db_notifications = Notification.objects.filter(related_object_id=application.id)
    assert db_notifications.count() == 3


@pytest.mark.service
@patch('applications.services_impl.update_application_stage')
@patch('applications.services_extended.generate_application_documents')
@patch('applications.services_extended.send_application_notifications')
def test_process_application_approval(mock_send_notifications, mock_generate_documents, mock_update_stage):
    """Test processing application approval."""
    # Create test data
    application = ApplicationFactory(stage='assessment')
    user = AdminUserFactory()
    
    # Mock function returns
    mock_update_stage.return_value = application
    mock_generate_documents.return_value = [MagicMock(), MagicMock()]
    mock_send_notifications.return_value = [MagicMock(), MagicMock()]
    
    # Call the function
    result = process_application_approval(
        application_id=application.id,
        approval_data={
            'approved_amount': 500000,
            'approved_term': 30,
            'approved_rate': 4.5,
            'approval_expiry': '2025-06-30',
            'approval_conditions': ['Condition 1', 'Condition 2']
        },
        user=user
    )
    
    # Check that the stage was updated
    mock_update_stage.assert_called_once_with(application.id, 'approved', user)
    
    # Check that documents were generated
    mock_generate_documents.assert_called_once_with(application.id, user)
    
    # Check that notifications were sent
    mock_send_notifications.assert_called_once()
    
    # Check the result
    assert result['success'] is True
    assert 'application' in result
    assert 'documents' in result
    assert 'notifications' in result
    
    # Check that a note was created with the conditions
    note = Note.objects.filter(application=application, title="Approval Conditions").first()
    assert note is not None
    assert "Condition 1" in note.content
    assert "Condition 2" in note.content
