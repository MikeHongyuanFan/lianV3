"""
Integration tests for borrower services.
"""
import pytest
from django.contrib.auth import get_user_model
from borrowers.services import (
    create_borrower_with_financials,
    create_guarantor_for_application,
    get_borrower_financial_summary
)
from borrowers.models import Borrower, Guarantor, Asset, Liability
from applications.models import Application
from django.utils import timezone

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
        created_by=admin_user
    )

@pytest.mark.django_db
def test_create_borrower_with_financials(admin_user):
    """Test creating a borrower with financial information."""
    borrower_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890",
        "date_of_birth": "1980-01-01",
        "annual_income": 120000.00,
        "monthly_expenses": 3000.00
    }
    
    assets_data = [
        {
            "asset_type": "property",
            "description": "Primary Residence",
            "value": 600000.00
        },
        {
            "asset_type": "savings",
            "description": "Savings Account",
            "value": 50000.00
        }
    ]
    
    liabilities_data = [
        {
            "liability_type": "mortgage",
            "description": "Existing Mortgage",
            "amount": 400000.00,
            "monthly_payment": 2000.00
        },
        {
            "liability_type": "credit_card",
            "description": "Credit Card",
            "amount": 5000.00,
            "monthly_payment": 200.00
        }
    ]
    
    borrower = create_borrower_with_financials(
        borrower_data=borrower_data,
        assets_data=assets_data,
        liabilities_data=liabilities_data,
        user=admin_user
    )
    
    # Verify borrower was created
    assert borrower is not None
    assert borrower.first_name == "John"
    assert borrower.last_name == "Doe"
    assert borrower.email == "john.doe@example.com"
    assert borrower.annual_income == 120000.00
    assert borrower.created_by == admin_user
    
    # Verify assets were created
    assets = borrower.assets.all()
    assert assets.count() == 2
    
    property_asset = assets.filter(asset_type="property").first()
    assert property_asset is not None
    assert property_asset.value == 600000.00
    assert property_asset.created_by == admin_user
    
    # Verify liabilities were created
    liabilities = borrower.liabilities.all()
    assert liabilities.count() == 2
    
    mortgage = liabilities.filter(liability_type="mortgage").first()
    assert mortgage is not None
    assert mortgage.amount == 400000.00
    assert mortgage.monthly_payment == 2000.00
    assert mortgage.created_by == admin_user

@pytest.mark.django_db
def test_create_guarantor_for_application(admin_user, application):
    """Test creating a guarantor for an application."""
    # Create a borrower first
    borrower = Borrower.objects.create(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="1234567890",
        date_of_birth="1980-01-01",
        created_by=admin_user
    )
    
    guarantor_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "phone": "0987654321",
        "date_of_birth": "1982-05-15",
        # Remove fields that aren't in the Guarantor model
        # "relationship": "spouse",
        # "annual_income": 80000.00
    }
    
    guarantor = create_guarantor_for_application(
        guarantor_data=guarantor_data,
        borrower_id=borrower.id,
        application_id=application.id,
        user=admin_user
    )
    
    # Verify guarantor was created
    assert guarantor is not None
    assert guarantor.first_name == "Jane"
    assert guarantor.last_name == "Smith"
    assert guarantor.email == "jane.smith@example.com"
    # assert guarantor.relationship == "spouse"  # Field doesn't exist
    # assert guarantor.annual_income == 80000.00  # Field doesn't exist
    assert guarantor.borrower == borrower
    assert guarantor.application == application
    assert guarantor.created_by == admin_user
    
    # Verify guarantor in database
    db_guarantor = Guarantor.objects.get(id=guarantor.id)
    assert db_guarantor.first_name == "Jane"
    assert db_guarantor.borrower == borrower
    assert db_guarantor.application == application

@pytest.mark.django_db
def test_create_guarantor_for_application_invalid_ids(admin_user):
    """Test creating a guarantor with invalid borrower or application ID."""
    guarantor_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "phone": "0987654321",
        "relationship": "spouse"
    }
    
    # Invalid borrower ID
    guarantor = create_guarantor_for_application(
        guarantor_data=guarantor_data,
        borrower_id=999,
        application_id=1,
        user=admin_user
    )
    
    assert guarantor is None
    
    # Create a borrower but use invalid application ID
    borrower = Borrower.objects.create(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        created_by=admin_user
    )
    
    guarantor = create_guarantor_for_application(
        guarantor_data=guarantor_data,
        borrower_id=borrower.id,
        application_id=999,
        user=admin_user
    )
    
    assert guarantor is None

@pytest.mark.django_db
def test_get_borrower_financial_summary(admin_user):
    """Test getting a borrower's financial summary."""
    # Create a borrower with financial information
    borrower = Borrower.objects.create(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="1234567890",
        date_of_birth="1980-01-01",
        annual_income=120000.00,
        monthly_expenses=3000.00,
        created_by=admin_user
    )
    
    # Create assets
    Asset.objects.create(
        borrower=borrower,
        asset_type="property",
        description="Primary Residence",
        value=600000.00,
        created_by=admin_user
    )
    
    Asset.objects.create(
        borrower=borrower,
        asset_type="savings",
        description="Savings Account",
        value=50000.00,
        created_by=admin_user
    )
    
    # Create liabilities
    Liability.objects.create(
        borrower=borrower,
        liability_type="mortgage",
        description="Existing Mortgage",
        amount=400000.00,
        monthly_payment=2000.00,
        created_by=admin_user
    )
    
    Liability.objects.create(
        borrower=borrower,
        liability_type="credit_card",
        description="Credit Card",
        amount=5000.00,
        monthly_payment=200.00,
        created_by=admin_user
    )
    
    summary = get_borrower_financial_summary(borrower.id)
    
    # Verify summary was calculated
    assert summary is not None
    assert "total_assets" in summary
    assert "total_liabilities" in summary
    assert "net_worth" in summary
    assert "monthly_income" in summary
    assert "monthly_expenses" in summary
    assert "disposable_income" in summary
    assert "asset_breakdown" in summary
    assert "liability_breakdown" in summary
    
    # Verify specific summary values
    assert summary["total_assets"] == 650000.00  # 600000 + 50000
    assert summary["total_liabilities"] == 405000.00  # 400000 + 5000
    assert summary["net_worth"] == 245000.00  # 650000 - 405000
    assert summary["monthly_income"] == 10000.00  # 120000 / 12
    assert summary["monthly_expenses"] == 5200.00  # 3000 + 2000 + 200
    assert summary["disposable_income"] == 4800.00  # 10000 - 5200
    
    # Verify asset breakdown
    assert len(summary["asset_breakdown"]) == 2
    
    # Verify liability breakdown
    assert len(summary["liability_breakdown"]) == 2

@pytest.mark.django_db
def test_get_borrower_financial_summary_invalid_id():
    """Test getting a financial summary with invalid borrower ID."""
    summary = get_borrower_financial_summary(999)
    
    assert summary is None
