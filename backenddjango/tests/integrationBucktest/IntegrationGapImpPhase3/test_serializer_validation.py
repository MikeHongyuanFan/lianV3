import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from applications.serializers import (
    AddressSerializer, 
    EmploymentInfoSerializer, 
    BorrowerSerializer
)
from borrowers.models import Borrower
from brokers.models import Broker

User = get_user_model()


@pytest.mark.django_db
class TestAddressSerializer:
    """Test suite for AddressSerializer validation"""
    
    def test_valid_address(self):
        """Test that valid address data passes validation"""
        data = {
            'street': '123 Test Street',
            'city': 'Sydney',
            'state': 'NSW',
            'postal_code': '2000',
            'country': 'Australia'
        }
        
        serializer = AddressSerializer(data=data)
        assert serializer.is_valid(), f"Validation errors: {serializer.errors}"
    
    def test_missing_required_fields(self):
        """Test validation of missing required fields"""
        data = {
            'street': '123 Test Street',
            # Missing city
            'state': 'NSW',
            # Missing postal_code
            'country': 'Australia'
        }
        
        serializer = AddressSerializer(data=data)
        assert not serializer.is_valid()
        assert 'city' in serializer.errors
        assert 'postal_code' in serializer.errors
    
    def test_field_max_length(self):
        """Test validation of field max length"""
        # Create a string that exceeds the max length
        long_string = 'a' * 300
        
        data = {
            'street': long_string,  # Exceeds max_length=255
            'city': 'Sydney',
            'state': 'NSW',
            'postal_code': '2000',
            'country': 'Australia'
        }
        
        serializer = AddressSerializer(data=data)
        assert not serializer.is_valid()
        assert 'street' in serializer.errors
        # The actual error message is "Ensure this field has no more than 255 characters."
        assert '255 characters' in str(serializer.errors['street'][0])


@pytest.mark.django_db
class TestEmploymentInfoSerializer:
    """Test suite for EmploymentInfoSerializer validation"""
    
    def test_valid_employment_info(self):
        """Test that valid employment info passes validation"""
        data = {
            'employer': 'Test Company',
            'position': 'Software Engineer',
            'income': '120000.00',
            'years_employed': '3.5'
        }
        
        serializer = EmploymentInfoSerializer(data=data)
        assert serializer.is_valid(), f"Validation errors: {serializer.errors}"
    
    def test_missing_required_fields(self):
        """Test validation of missing required fields"""
        data = {
            'employer': 'Test Company',
            # Missing position
            'income': '120000.00',
            # Missing years_employed
        }
        
        serializer = EmploymentInfoSerializer(data=data)
        assert not serializer.is_valid()
        assert 'position' in serializer.errors
        assert 'years_employed' in serializer.errors
    
    def test_invalid_decimal_fields(self):
        """Test validation of invalid decimal fields"""
        data = {
            'employer': 'Test Company',
            'position': 'Software Engineer',
            'income': 'not-a-number',  # Invalid decimal
            'years_employed': '3.5'
        }
        
        serializer = EmploymentInfoSerializer(data=data)
        assert not serializer.is_valid()
        assert 'income' in serializer.errors
        # The actual error message is "A valid number is required."
        assert 'valid number' in str(serializer.errors['income'][0]).lower()
    
    def test_decimal_precision(self):
        """Test validation of decimal precision"""
        data = {
            'employer': 'Test Company',
            'position': 'Software Engineer',
            'income': '120000.00',
            'years_employed': '3.555'  # Too many decimal places (max 2)
        }
        
        serializer = EmploymentInfoSerializer(data=data)
        assert not serializer.is_valid()
        assert 'years_employed' in serializer.errors
        assert 'decimal places' in str(serializer.errors['years_employed'][0]).lower()


@pytest.mark.django_db
class TestBorrowerSerializer:
    """Test suite for BorrowerSerializer validation"""
    
    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
            role='borrower'
        )
    
    @pytest.fixture
    def broker_user(self):
        user = User.objects.create_user(
            username='brokeruser',
            email='broker@example.com',
            password='password123',
            role='broker'
        )
        Broker.objects.create(user=user, name='Test Broker')
        return user
    
    def test_valid_borrower(self, user):
        """Test that valid borrower data passes validation"""
        borrower = Borrower.objects.create(
            user=user,
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='0412345678',
            date_of_birth='1990-01-01',
            residential_address='123 Test Street',
            employer_name='Test Company',
            job_title='Software Engineer',
            annual_income=120000.00,
            employment_duration=3.5,
            tax_id='12345678',
            marital_status='single',
            residency_status='citizen',
            referral_source='website'
        )
        
        serializer = BorrowerSerializer(borrower)
        data = serializer.data
        
        # Verify serialized data
        assert data['first_name'] == 'John'
        assert data['last_name'] == 'Doe'
        assert data['email'] == 'john.doe@example.com'
        assert data['address']['street'] == '123 Test Street'
        assert data['employment_info']['employer'] == 'Test Company'
        assert float(data['employment_info']['income']) == 120000.00
    
    def test_serializer_method_fields(self, user):
        """Test that serializer method fields work correctly"""
        # Create borrower with minimal data
        borrower = Borrower.objects.create(
            user=user,
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@example.com'
        )
        
        serializer = BorrowerSerializer(borrower)
        data = serializer.data
        
        # Verify serializer method fields handle missing data gracefully
        assert data['address']['street'] == ''
        assert data['employment_info']['employer'] == ''
        assert float(data['employment_info']['income']) == 0
