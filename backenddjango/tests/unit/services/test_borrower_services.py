"""
Tests for borrower services.
"""
import pytest
from decimal import Decimal
from unittest.mock import patch
from django.utils import timezone
from borrowers.services import (
    create_borrower_with_financials,
    create_guarantor_for_application,
    get_borrower_financial_summary
)
from borrowers.models import Borrower, Guarantor, Asset, Liability
from tests.factories import (
    ApplicationFactory, BorrowerFactory, GuarantorFactory, 
    AssetFactory, LiabilityFactory, AdminUserFactory
)

pytestmark = pytest.mark.django_db


@pytest.mark.service
def test_create_borrower_with_financials():
    """Test creating a borrower with financial information."""
    # Create test data
    user = AdminUserFactory()
    borrower_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'phone': '1234567890',
        'date_of_birth': '1980-01-01',
        'annual_income': 120000,
        'monthly_expenses': 3000
    }
    
    assets_data = [
        {
            'asset_type': 'property',
            'value': 500000,
            'description': 'Primary residence'
        },
        {
            'asset_type': 'vehicle',
            'value': 30000,
            'description': 'Car'
        }
    ]
    
    liabilities_data = [
        {
            'liability_type': 'mortgage',
            'amount': 400000,
            'monthly_payment': 2000,
            'description': 'Home loan'
        },
        {
            'liability_type': 'car_loan',
            'amount': 20000,
            'monthly_payment': 500,
            'description': 'Car loan'
        }
    ]
    
    # Call the function
    borrower = create_borrower_with_financials(
        borrower_data=borrower_data,
        assets_data=assets_data,
        liabilities_data=liabilities_data,
        user=user
    )
    
    # Check that the borrower was created with correct attributes
    assert borrower is not None
    assert borrower.first_name == 'John'
    assert borrower.last_name == 'Doe'
    assert borrower.email == 'john.doe@example.com'
    assert borrower.annual_income == 120000
    assert borrower.monthly_expenses == 3000
    assert borrower.created_by == user
    
    # Check that assets were created
    assets = Asset.objects.filter(borrower=borrower)
    assert assets.count() == 2
    
    property_asset = assets.get(asset_type='property')
    assert property_asset.value == 500000
    assert property_asset.description == 'Primary residence'
    assert property_asset.created_by == user
    
    vehicle_asset = assets.get(asset_type='vehicle')
    assert vehicle_asset.value == 30000
    assert vehicle_asset.description == 'Car'
    assert vehicle_asset.created_by == user
    
    # Check that liabilities were created
    liabilities = Liability.objects.filter(borrower=borrower)
    assert liabilities.count() == 2
    
    mortgage = liabilities.get(liability_type='mortgage')
    assert mortgage.amount == 400000
    assert mortgage.monthly_payment == 2000
    assert mortgage.description == 'Home loan'
    assert mortgage.created_by == user
    
    car_loan = liabilities.get(liability_type='car_loan')
    assert car_loan.amount == 20000
    assert car_loan.monthly_payment == 500
    assert car_loan.description == 'Car loan'
    assert car_loan.created_by == user


@pytest.mark.service
def test_create_borrower_without_financials():
    """Test creating a borrower without financial information."""
    # Create test data
    borrower_data = {
        'first_name': 'Jane',
        'last_name': 'Smith',
        'email': 'jane.smith@example.com',
        'phone': '0987654321',
        'date_of_birth': '1985-05-15'
    }
    
    # Call the function
    borrower = create_borrower_with_financials(borrower_data=borrower_data)
    
    # Check that the borrower was created with correct attributes
    assert borrower is not None
    assert borrower.first_name == 'Jane'
    assert borrower.last_name == 'Smith'
    assert borrower.email == 'jane.smith@example.com'
    
    # Check that no assets or liabilities were created
    assert Asset.objects.filter(borrower=borrower).count() == 0
    assert Liability.objects.filter(borrower=borrower).count() == 0


@pytest.mark.service
def test_create_guarantor_for_application():
    """Test creating a guarantor for an application."""
    # Create test data
    application = ApplicationFactory()
    borrower = BorrowerFactory()
    user = AdminUserFactory()
    
    guarantor_data = {
        'first_name': 'Michael',
        'last_name': 'Johnson',
        'email': 'michael.johnson@example.com',
        'phone': '5551234567',
        'date_of_birth': '1975-03-20',
        'guarantor_type': 'individual'
    }
    
    # Call the function
    guarantor = create_guarantor_for_application(
        guarantor_data=guarantor_data,
        borrower_id=borrower.id,
        application_id=application.id,
        user=user
    )
    
    # Check that the guarantor was created with correct attributes
    assert guarantor is not None
    assert guarantor.first_name == 'Michael'
    assert guarantor.last_name == 'Johnson'
    assert guarantor.email == 'michael.johnson@example.com'
    assert guarantor.guarantor_type == 'individual'
    assert guarantor.borrower == borrower
    assert guarantor.application == application
    assert guarantor.created_by == user
    assert guarantor.guarantor_type == 'individual'
    assert guarantor.borrower == borrower
    assert guarantor.application == application
    assert guarantor.created_by == user


@pytest.mark.service
def test_create_guarantor_nonexistent_borrower():
    """Test creating a guarantor with a nonexistent borrower."""
    # Create test data
    application = ApplicationFactory()
    
    guarantor_data = {
        'first_name': 'Michael',
        'last_name': 'Johnson',
        'email': 'michael.johnson@example.com',
        'guarantor_type': 'individual'
    }
    
    # Call the function with a nonexistent borrower ID
    guarantor = create_guarantor_for_application(
        guarantor_data=guarantor_data,
        borrower_id=999,
        application_id=application.id
    )
    
    # Check that no guarantor was created
    assert guarantor is None


@pytest.mark.service
def test_create_guarantor_nonexistent_application():
    """Test creating a guarantor with a nonexistent application."""
    # Create test data
    borrower = BorrowerFactory()
    
    guarantor_data = {
        'first_name': 'Michael',
        'last_name': 'Johnson',
        'email': 'michael.johnson@example.com',
        'guarantor_type': 'individual'
    }
    
    # Call the function with a nonexistent application ID
    guarantor = create_guarantor_for_application(
        guarantor_data=guarantor_data,
        borrower_id=borrower.id,
        application_id=999
    )
    
    # Check that no guarantor was created
    assert guarantor is None


@pytest.mark.service
def test_get_borrower_financial_summary():
    """Test getting a borrower's financial summary."""
    # Create test data
    borrower = BorrowerFactory(
        annual_income=120000,
        other_income=1000,
        monthly_expenses=3000
    )
    
    # Create assets
    property_asset = AssetFactory(
        borrower=borrower,
        asset_type='property',
        value=500000
    )
    
    vehicle_asset = AssetFactory(
        borrower=borrower,
        asset_type='vehicle',
        value=30000
    )
    
    # Create liabilities
    mortgage = LiabilityFactory(
        borrower=borrower,
        liability_type='mortgage',
        amount=400000,
        monthly_payment=2000
    )
    
    car_loan = LiabilityFactory(
        borrower=borrower,
        liability_type='car_loan',
        amount=20000,
        monthly_payment=500
    )
    
    # Call the function
    summary = get_borrower_financial_summary(borrower.id)
    
    # Check the summary
    assert summary is not None
    assert summary['total_assets'] == 530000  # 500000 + 30000
    assert summary['total_liabilities'] == 420000  # 400000 + 20000
    assert summary['net_worth'] == 110000  # 530000 - 420000
    assert summary['monthly_income'] == 11000  # (120000 / 12) + 1000
    assert summary['monthly_expenses'] == 5500  # 3000 + 2000 + 500
    assert summary['disposable_income'] == 5500  # 11000 - 5500
    
    # Check asset breakdown
    assert len(summary['asset_breakdown']) == 2
    
    property_breakdown = next(a for a in summary['asset_breakdown'] if a['type'] == 'Property')
    assert property_breakdown['value'] == 500000
    
    vehicle_breakdown = next(a for a in summary['asset_breakdown'] if a['type'] == 'Vehicle')
    assert vehicle_breakdown['value'] == 30000
    
    # Check liability breakdown
    assert len(summary['liability_breakdown']) == 2
    
    mortgage_breakdown = next(l for l in summary['liability_breakdown'] if l['type'] == 'Mortgage')
    assert mortgage_breakdown['amount'] == 400000
    assert mortgage_breakdown['monthly_payment'] == 2000
    
    car_loan_breakdown = next(l for l in summary['liability_breakdown'] if l['type'] == 'Car Loan')
    assert car_loan_breakdown['amount'] == 20000
    assert car_loan_breakdown['monthly_payment'] == 500


@pytest.mark.service
def test_get_borrower_financial_summary_no_financials():
    """Test getting a financial summary for a borrower with no financial information."""
    # Create a borrower with no financial information
    borrower = BorrowerFactory(annual_income=None, other_income=None, monthly_expenses=None)
    
    # Call the function
    summary = get_borrower_financial_summary(borrower.id)
    
    # Check the summary
    assert summary is not None
    assert summary['total_assets'] == 0
    assert summary['total_liabilities'] == 0
    assert summary['net_worth'] == 0
    assert summary['monthly_income'] == 0
    assert summary['monthly_expenses'] == 0
    assert summary['disposable_income'] == 0
    assert len(summary['asset_breakdown']) == 0
    assert len(summary['liability_breakdown']) == 0


@pytest.mark.service
def test_get_borrower_financial_summary_nonexistent_borrower():
    """Test getting a financial summary for a nonexistent borrower."""
    # Call the function with a nonexistent borrower ID
    summary = get_borrower_financial_summary(999)
    
    # Check that no summary was returned
    assert summary is None
