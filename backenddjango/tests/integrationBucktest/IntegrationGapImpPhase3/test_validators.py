import pytest
from django.core.exceptions import ValidationError
from applications.validators import validate_abn, validate_acn, validate_company_borrower


@pytest.mark.django_db
class TestABNValidator:
    """Test suite for ABN validator"""
    
    def test_valid_abn(self):
        """Test that valid ABNs pass validation"""
        valid_abns = [
            "51824753556",  # Valid ABN
            "51 824 753 556",  # Valid ABN with spaces
            "51-824-753-556",  # Valid ABN with dashes
        ]
        
        for abn in valid_abns:
            cleaned_abn = validate_abn(abn)
            assert cleaned_abn == "51824753556"
    
    def test_invalid_abn_length(self):
        """Test that ABNs with incorrect length fail validation"""
        invalid_abns = [
            "5182475355",  # Too short (10 digits)
            "518247535561",  # Too long (12 digits)
            "abcdefghijk",  # Non-numeric
        ]
        
        for abn in invalid_abns:
            with pytest.raises(ValidationError) as excinfo:
                validate_abn(abn)
            assert "ABN must be 11 digits" in str(excinfo.value)
    
    def test_invalid_abn_checksum(self):
        """Test that ABNs with invalid checksum fail validation"""
        invalid_abns = [
            "51824753557",  # Changed last digit
            "61824753556",  # Changed first digit
        ]
        
        for abn in invalid_abns:
            with pytest.raises(ValidationError) as excinfo:
                validate_abn(abn)
            assert "Invalid ABN checksum" in str(excinfo.value)


@pytest.mark.django_db
class TestACNValidator:
    """Test suite for ACN validator"""
    
    def test_valid_acn(self):
        """Test that valid ACNs pass validation"""
        valid_acns = [
            "004085616",  # Valid ACN
            "004 085 616",  # Valid ACN with spaces
            "004-085-616",  # Valid ACN with dashes
        ]
        
        for acn in valid_acns:
            cleaned_acn = validate_acn(acn)
            assert cleaned_acn == "004085616"
    
    def test_invalid_acn_length(self):
        """Test that ACNs with incorrect length fail validation"""
        invalid_acns = [
            "00408561",  # Too short (8 digits)
            "0040856161",  # Too long (10 digits)
            "abcdefghi",  # Non-numeric
        ]
        
        for acn in invalid_acns:
            with pytest.raises(ValidationError) as excinfo:
                validate_acn(acn)
            assert "ACN must be 9 digits" in str(excinfo.value)
    
    def test_invalid_acn_checksum(self):
        """Test that ACNs with invalid checksum fail validation"""
        invalid_acns = [
            "004085617",  # Changed last digit
            "104085616",  # Changed first digit
        ]
        
        for acn in invalid_acns:
            with pytest.raises(ValidationError) as excinfo:
                validate_acn(acn)
            assert "Invalid ACN checksum" in str(excinfo.value)


@pytest.mark.django_db
class TestCompanyBorrowerValidator:
    """Test suite for company borrower validator"""
    
    def test_valid_company_data(self):
        """Test that valid company data passes validation"""
        company_data = {
            'company_name': 'Test Company Pty Ltd',
            'abn': '51824753556',
            'acn': '004085616',
            'business_type': 'pty_ltd',
            'industry': 'Technology',
            'years_in_business': 5,
            'financial_info': {
                'annual_revenue': 1000000,
                'net_profit': 200000,
                'assets': 500000,
                'liabilities': 300000
            },
            'registered_address': {
                'street': '123 Test Street',
                'city': 'Sydney',
                'state': 'NSW',
                'postal_code': '2000',
                'country': 'Australia'
            },
            'directors': [
                {
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'email': 'john.doe@example.com'
                }
            ]
        }
        
        errors = validate_company_borrower(company_data)
        assert not errors, f"Unexpected errors: {errors}"
    
    def test_missing_required_fields(self):
        """Test validation of missing required fields"""
        company_data = {
            'company_name': 'Test Company',
            # Missing ABN
            # Missing ACN
            # Missing business_type
            # Missing industry
        }
        
        errors = validate_company_borrower(company_data)
        assert 'abn' in errors
        assert 'acn' in errors
        assert 'business_type' in errors
        assert 'industry' in errors
    
    def test_invalid_business_type(self):
        """Test validation of invalid business type"""
        company_data = {
            'company_name': 'Test Company',
            'abn': '51824753556',
            'acn': '004085616',
            'business_type': 'invalid_type',  # Invalid business type
            'industry': 'Technology'
        }
        
        errors = validate_company_borrower(company_data)
        assert 'business_type' in errors
        assert 'Invalid business type' in errors['business_type']
    
    def test_negative_years_in_business(self):
        """Test validation of negative years in business"""
        company_data = {
            'company_name': 'Test Company',
            'abn': '51824753556',
            'acn': '004085616',
            'business_type': 'pty_ltd',
            'industry': 'Technology',
            'years_in_business': -5  # Negative years
        }
        
        errors = validate_company_borrower(company_data)
        assert 'years_in_business' in errors
        assert 'cannot be negative' in errors['years_in_business']
    
    def test_invalid_financial_info(self):
        """Test validation of invalid financial information"""
        company_data = {
            'company_name': 'Test Company',
            'abn': '51824753556',
            'acn': '004085616',
            'business_type': 'pty_ltd',
            'industry': 'Technology',
            'financial_info': {
                'annual_revenue': -1000000,  # Negative revenue
                'net_profit': 'not_a_number',  # Not a number
                'assets': -500000,  # Negative assets
                'liabilities': 'invalid'  # Not a number
            }
        }
        
        errors = validate_company_borrower(company_data)
        assert 'financial_info.annual_revenue' in errors
        assert 'financial_info.net_profit' in errors
        assert 'financial_info.assets' in errors
        assert 'financial_info.liabilities' in errors
    
    def test_invalid_address(self):
        """Test validation of invalid address"""
        company_data = {
            'company_name': 'Test Company',
            'abn': '51824753556',
            'acn': '004085616',
            'business_type': 'pty_ltd',
            'industry': 'Technology',
            'registered_address': {
                # Missing street
                'city': 'Sydney',
                # Missing state
                'postal_code': 'invalid',  # Invalid postal code for Australia
                'country': 'Australia'
            }
        }
        
        errors = validate_company_borrower(company_data)
        assert 'registered_address.street' in errors
        assert 'registered_address.state' in errors
        assert 'registered_address.postal_code' in errors
    
    def test_invalid_directors(self):
        """Test validation of invalid directors"""
        company_data = {
            'company_name': 'Test Company',
            'abn': '51824753556',
            'acn': '004085616',
            'business_type': 'pty_ltd',
            'industry': 'Technology',
            'directors': [
                {
                    # Missing first_name
                    'last_name': 'Doe',
                    'email': 'invalid-email'  # Invalid email
                },
                {
                    'first_name': 'Jane',
                    # Missing last_name
                    'email': 'jane.doe@example.com'
                }
            ]
        }
        
        errors = validate_company_borrower(company_data)
        assert 'directors[0].first_name' in errors
        assert 'directors[0].email' in errors
        assert 'directors[1].last_name' in errors
