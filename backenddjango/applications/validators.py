from django.core.exceptions import ValidationError
import re

def validate_abn(abn):
    """
    Validate Australian Business Number (ABN)
    
    ABN must be 11 digits with no spaces or special characters
    """
    # Remove any spaces or special characters
    abn_cleaned = re.sub(r'[^0-9]', '', abn)
    
    if len(abn_cleaned) != 11:
        raise ValidationError('ABN must be 11 digits')
    
    # ABN validation algorithm
    # Weights for each digit
    weights = [10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    
    # Subtract 1 from the first digit
    digits = [int(d) for d in abn_cleaned]
    digits[0] -= 1
    
    # Calculate the weighted sum
    total = sum(w * d for w, d in zip(weights, digits))
    
    # Valid ABN should be divisible by 89
    if total % 89 != 0:
        raise ValidationError('Invalid ABN checksum')
    
    return abn_cleaned

def validate_acn(acn):
    """
    Validate Australian Company Number (ACN)
    
    ACN must be 9 digits with no spaces or special characters
    """
    # Remove any spaces or special characters
    acn_cleaned = re.sub(r'[^0-9]', '', acn)
    
    if len(acn_cleaned) != 9:
        raise ValidationError('ACN must be 9 digits')
    
    # ACN validation algorithm
    # Weights for each digit
    weights = [8, 7, 6, 5, 4, 3, 2, 1]
    
    # Calculate the weighted sum
    digits = [int(d) for d in acn_cleaned[:-1]]  # Exclude the check digit
    total = sum(w * d for w, d in zip(weights, digits))
    
    # Calculate the check digit
    remainder = total % 10
    check_digit = (10 - remainder) % 10
    
    # Verify the check digit
    if check_digit != int(acn_cleaned[-1]):
        raise ValidationError('Invalid ACN checksum')
    
    return acn_cleaned

def validate_company_borrower(company_data):
    """
    Validate company borrower information
    """
    errors = {}
    
    # Validate required fields and identifiers
    errors.update(_validate_required_fields(company_data))
    errors.update(_validate_identifiers(company_data))
    
    # Validate business type and years
    errors.update(_validate_business_details(company_data))
    
    # Validate financial information
    errors.update(_validate_financial_info(company_data))
    
    # Validate address information
    errors.update(_validate_address(company_data))
    
    # Validate directors information
    errors.update(_validate_directors(company_data))
    
    return errors

def _validate_required_fields(company_data):
    """Validate required company fields"""
    errors = {}
    required_fields = ['company_name', 'abn', 'acn', 'business_type', 'industry']
    for field in required_fields:
        if not company_data.get(field):
            errors[field] = f'{field.replace("_", " ").title()} is required'
    return errors

def _validate_identifiers(company_data):
    """Validate ABN and ACN"""
    errors = {}
    
    # ABN validation
    if company_data.get('abn'):
        try:
            validate_abn(company_data['abn'])
        except ValidationError as e:
            errors['abn'] = str(e)
    
    # ACN validation
    if company_data.get('acn'):
        try:
            validate_acn(company_data['acn'])
        except ValidationError as e:
            errors['acn'] = str(e)
            
    return errors

def _validate_business_details(company_data):
    """Validate business type and years in business"""
    errors = {}
    
    # Business type validation
    valid_business_types = [
        'sole_proprietorship', 'partnership', 'pty_ltd', 
        'public_company', 'trust', 'non_profit'
    ]
    if company_data.get('business_type') and company_data['business_type'] not in valid_business_types:
        errors['business_type'] = 'Invalid business type'
    
    # Years in business validation
    if company_data.get('years_in_business'):
        try:
            years = float(company_data['years_in_business'])
            if years < 0:
                errors['years_in_business'] = 'Years in business cannot be negative'
        except (ValueError, TypeError):
            errors['years_in_business'] = 'Years in business must be a number'
            
    return errors

def _validate_financial_info(company_data):
    """Validate financial information"""
    errors = {}
    
    financial_fields = ['annual_revenue', 'net_profit', 'assets', 'liabilities']
    if 'financial_info' in company_data:
        for field in financial_fields:
            if field in company_data['financial_info'] and company_data['financial_info'][field]:
                try:
                    amount = float(company_data['financial_info'][field])
                    if field != 'net_profit' and amount < 0:
                        errors[f'financial_info.{field}'] = f'{field.replace("_", " ").title()} cannot be negative'
                except (ValueError, TypeError):
                    errors[f'financial_info.{field}'] = f'{field.replace("_", " ").title()} must be a number'
                    
    return errors

def _validate_address(company_data):
    """Validate company address"""
    errors = {}
    
    if 'registered_address' in company_data:
        address = company_data['registered_address']
        address_fields = ['street', 'city', 'state', 'postal_code', 'country']
        for field in address_fields:
            if not address.get(field):
                errors[f'registered_address.{field}'] = f'{field.replace("_", " ").title()} is required'
        
        # Postal code validation for Australia
        if address.get('country', '').lower() == 'australia' and address.get('postal_code'):
            if not re.match(r'^\d{4}$', str(address['postal_code'])):
                errors['registered_address.postal_code'] = 'Australian postal code must be 4 digits'
                
    return errors

def _validate_directors(company_data):
    """Validate company directors"""
    errors = {}
    
    if 'directors' in company_data and company_data['directors']:
        for i, director in enumerate(company_data['directors']):
            if not director.get('first_name'):
                errors[f'directors[{i}].first_name'] = 'Director first name is required'
            if not director.get('last_name'):
                errors[f'directors[{i}].last_name'] = 'Director last name is required'
            
            # Email validation
            if director.get('email') and not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', director['email']):
                errors[f'directors[{i}].email'] = 'Invalid email format'
                
    return errors
