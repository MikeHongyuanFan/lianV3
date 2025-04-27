# Integration Gap Implementation Phase 3: Validation and Edge Cases

## Objective
Increase validator coverage from 6% to at least 85% and improve edge case testing.

## Current Coverage Status
- `applications/validators.py`: 6%
- Edge case coverage across the system: Limited

## Implementation Strategy

### 1. Validator Testing

#### Target Files:
- `applications/validators.py`
- Other validation logic in serializers and models

#### Test Cases to Implement:
1. Input validation for all forms
2. Business rule validation
3. Data integrity validation
4. Cross-field validation
5. Custom validator functions

#### Example Implementation:
```python
@pytest.mark.django_db
def test_loan_amount_validator():
    from applications.validators import validate_loan_amount
    from django.core.exceptions import ValidationError
    
    # Test valid loan amount
    validate_loan_amount(500000)  # Should not raise exception
    
    # Test invalid loan amount (negative)
    with pytest.raises(ValidationError) as excinfo:
        validate_loan_amount(-1000)
    assert "Loan amount cannot be negative" in str(excinfo.value)
    
    # Test invalid loan amount (zero)
    with pytest.raises(ValidationError) as excinfo:
        validate_loan_amount(0)
    assert "Loan amount must be greater than zero" in str(excinfo.value)
    
    # Test invalid loan amount (too large)
    with pytest.raises(ValidationError) as excinfo:
        validate_loan_amount(1000000000)
    assert "Loan amount exceeds maximum allowed" in str(excinfo.value)
```

### 2. Serializer Validation Testing

#### Target Files:
- `applications/serializers.py`
- `borrowers/serializers.py`
- `documents/serializers.py`
- `users/serializers.py`

#### Test Cases to Implement:
1. Required field validation
2. Field type validation
3. Field format validation
4. Custom validation methods
5. Nested serializer validation

#### Example Implementation:
```python
@pytest.mark.django_db
def test_application_serializer_validation():
    from applications.serializers import ApplicationSerializer
    
    # Test missing required fields
    serializer = ApplicationSerializer(data={})
    assert not serializer.is_valid()
    assert 'application_type' in serializer.errors
    assert 'loan_amount' in serializer.errors
    
    # Test invalid field types
    serializer = ApplicationSerializer(data={
        'application_type': 'residential',
        'purpose': 'Home purchase',
        'loan_amount': 'not-a-number',  # Invalid type
        'loan_term': 360,
        'interest_rate': 3.50,
        'repayment_frequency': 'monthly',
    })
    assert not serializer.is_valid()
    assert 'loan_amount' in serializer.errors
    
    # Test valid data
    serializer = ApplicationSerializer(data={
        'application_type': 'residential',
        'purpose': 'Home purchase',
        'loan_amount': 500000.00,
        'loan_term': 360,
        'interest_rate': 3.50,
        'repayment_frequency': 'monthly',
    })
    assert serializer.is_valid()
```

### 3. Edge Case Testing

#### Areas to Focus:
1. Boundary conditions
2. Error handling
3. Resource limitations
4. Concurrent operations
5. Data migration scenarios

#### Example Implementation:
```python
@pytest.mark.django_db
def test_application_status_transition_edge_cases(application_instance):
    from applications.services import ApplicationService
    from django.core.exceptions import ValidationError
    
    # Test invalid transition (skipping stages)
    with pytest.raises(ValidationError) as excinfo:
        ApplicationService.update_application_status(application_instance, 'closed')
    assert "Invalid status transition" in str(excinfo.value)
    
    # Test valid transition sequence
    ApplicationService.update_application_status(application_instance, 'processing')
    assert application_instance.stage == 'processing'
    
    ApplicationService.update_application_status(application_instance, 'approved')
    assert application_instance.stage == 'approved'
    
    # Test idempotent operation (setting same status)
    ApplicationService.update_application_status(application_instance, 'approved')
    assert application_instance.stage == 'approved'
    
    # Test transition after final state
    ApplicationService.update_application_status(application_instance, 'closed')
    assert application_instance.stage == 'closed'
    
    with pytest.raises(ValidationError) as excinfo:
        ApplicationService.update_application_status(application_instance, 'processing')
    assert "Cannot transition from closed state" in str(excinfo.value)
```

### 4. Security Validation Testing

#### Areas to Focus:
1. Permission validation
2. Authentication validation
3. Authorization validation
4. Data access validation

#### Example Implementation:
```python
@pytest.mark.django_db
def test_application_permission_validation(admin_user, broker_user, client_user, application_instance):
    from applications.services import ApplicationService
    from django.core.exceptions import PermissionDenied
    
    # Test admin can access any application
    assert ApplicationService.can_access_application(admin_user, application_instance)
    
    # Test broker can access own applications
    application_instance.broker = broker_user.broker
    application_instance.save()
    assert ApplicationService.can_access_application(broker_user, application_instance)
    
    # Test broker cannot access other broker's applications
    other_broker_user = User.objects.create_user(
        username='otherbroker',
        email='other@example.com',
        password='password',
        role='broker'
    )
    other_broker = Broker.objects.create(user=other_broker_user, name='Other Broker')
    
    with pytest.raises(PermissionDenied):
        ApplicationService.can_access_application(other_broker_user, application_instance)
    
    # Test client can access applications they're associated with
    application_instance.borrower = client_user.borrower
    application_instance.save()
    assert ApplicationService.can_access_application(client_user, application_instance)
```

### 5. Data Integrity Validation

#### Areas to Focus:
1. Database constraints
2. Unique constraints
3. Foreign key constraints
4. Check constraints

#### Example Implementation:
```python
@pytest.mark.django_db
def test_application_data_integrity(application_instance):
    from applications.models import Application
    from django.db.utils import IntegrityError
    
    # Test duplicate application number
    with pytest.raises(IntegrityError):
        Application.objects.create(
            application_number=application_instance.application_number,
            application_type='residential',
            purpose='Home purchase',
            loan_amount=500000.00,
            loan_term=360,
            interest_rate=3.50,
            repayment_frequency='monthly',
            broker=application_instance.broker,
            stage='inquiry'
        )
    
    # Test invalid foreign key
    with pytest.raises(IntegrityError):
        Application.objects.create(
            application_type='residential',
            purpose='Home purchase',
            loan_amount=500000.00,
            loan_term=360,
            interest_rate=3.50,
            repayment_frequency='monthly',
            broker_id=99999,  # Non-existent broker ID
            stage='inquiry'
        )
```

## Expected Outcomes
1. Increased validator coverage from 6% to at least 85%
2. Improved edge case handling
3. Better data integrity validation
4. Enhanced security validation
5. More robust error handling

## Dependencies
- Properly configured test database
- Test fixtures for required entities
- Mock objects for external services

## Timeline
- Estimated completion time: 2 weeks
- Priority: Medium
