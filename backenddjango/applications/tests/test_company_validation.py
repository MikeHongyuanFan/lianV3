from django.test import TestCase
from applications.validators import validate_abn, validate_acn, validate_company_borrower
from django.core.exceptions import ValidationError
import pytest

class CompanyValidationTests(TestCase):
    
    def test_valid_abn(self):
        # Valid ABN examples
        valid_abns = [
            '51824753556',  # Properly formatted ABN
            '51 824 753 556',  # With spaces
            '51-824-753-556',  # With hyphens
        ]
        
        for abn in valid_abns:
            try:
                cleaned_abn = validate_abn(abn)
                self.assertEqual(cleaned_abn, '51824753556')
            except ValidationError:
                self.fail(f"validate_abn raised ValidationError unexpectedly for {abn}")
    
    def test_invalid_abn(self):
        # Invalid ABN examples
        invalid_abns = [
            '1234567890',  # Too short
            '123456789012',  # Too long
            '51824753557',  # Invalid checksum
            'ABCDEFGHIJK',  # Non-numeric
        ]
        
        for abn in invalid_abns:
            with self.assertRaises(ValidationError):
                validate_abn(abn)
    
    def test_valid_acn(self):
        # Valid ACN examples
        valid_acns = [
            '004085616',  # Properly formatted ACN
            '004 085 616',  # With spaces
            '004-085-616',  # With hyphens
        ]
        
        for acn in valid_acns:
            try:
                cleaned_acn = validate_acn(acn)
                self.assertEqual(cleaned_acn, '004085616')
            except ValidationError:
                self.fail(f"validate_acn raised ValidationError unexpectedly for {acn}")
    
    def test_invalid_acn(self):
        # Invalid ACN examples
        invalid_acns = [
            '12345678',  # Too short
            '1234567890',  # Too long
            '004085617',  # Invalid checksum
            'ABCDEFGHI',  # Non-numeric
        ]
        
        for acn in invalid_acns:
            with self.assertRaises(ValidationError):
                validate_acn(acn)
    
    def test_company_borrower_validation_valid(self):
        # Valid company borrower data
        valid_company = {
            'company_name': 'Test Company Pty Ltd',
            'abn': '51824753556',
            'acn': '004085616',
            'business_type': 'pty_ltd',
            'years_in_business': '5.5',
            'industry': 'Technology',
            'registered_address': {
                'street': '123 Main St',
                'city': 'Sydney',
                'state': 'NSW',
                'postal_code': '2000',
                'country': 'Australia'
            },
            'directors': [
                {
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'email': 'john@example.com',
                    'phone': '0412345678'
                }
            ],
            'financial_info': {
                'annual_revenue': '1000000',
                'net_profit': '200000',
                'assets': '2000000',
                'liabilities': '800000'
            }
        }
        
        errors = validate_company_borrower(valid_company)
        self.assertEqual(errors, {})
    
    def test_company_borrower_validation_invalid(self):
        # Invalid company borrower data
        invalid_company = {
            'company_name': '',  # Missing company name
            'abn': '1234',  # Invalid ABN
            'acn': '1234',  # Invalid ACN
            'business_type': 'invalid_type',  # Invalid business type
            'years_in_business': 'abc',  # Non-numeric
            'industry': 'Technology',
            'registered_address': {
                'street': '123 Main St',
                'city': 'Sydney',
                'state': 'NSW',
                'postal_code': 'ABC',  # Invalid postal code
                'country': 'Australia'
            },
            'directors': [
                {
                    'first_name': '',  # Missing first name
                    'last_name': 'Doe',
                    'email': 'invalid-email',  # Invalid email
                    'phone': '0412345678'
                }
            ],
            'financial_info': {
                'annual_revenue': '-1000',  # Negative revenue
                'net_profit': 'abc',  # Non-numeric
                'assets': '2000000',
                'liabilities': '800000'
            }
        }
        
        errors = validate_company_borrower(invalid_company)
        
        # Check that we have the expected errors
        self.assertIn('company_name', errors)
        self.assertIn('abn', errors)
        self.assertIn('acn', errors)
        self.assertIn('business_type', errors)
        self.assertIn('years_in_business', errors)
        self.assertIn('registered_address.postal_code', errors)
        self.assertIn('directors[0].first_name', errors)
        self.assertIn('directors[0].email', errors)
        self.assertIn('financial_info.annual_revenue', errors)
        self.assertIn('financial_info.net_profit', errors)
