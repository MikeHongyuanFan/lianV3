"""
Factories for borrower models.
"""
import factory
from factory.django import DjangoModelFactory
from borrowers.models import Borrower, Guarantor, Asset, Liability
from django.utils import timezone
from datetime import timedelta
from .user_factories import UserFactory


class BorrowerFactory(DjangoModelFactory):
    """Factory for Borrower model."""
    
    class Meta:
        model = Borrower
    
    user = factory.SubFactory(UserFactory, role='client')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    phone = factory.Faker('phone_number')
    date_of_birth = factory.Faker('date_of_birth', minimum_age=18, maximum_age=80)
    residential_address = factory.Faker('address')
    marital_status = factory.Iterator(['single', 'married', 'divorced', 'widowed'])
    residency_status = factory.Iterator(['citizen', 'permanent_resident', 'temporary_resident'])
    annual_income = factory.Faker('random_int', min=30000, max=300000)
    other_income = factory.Faker('random_int', min=0, max=50000)
    monthly_expenses = factory.Faker('random_int', min=1000, max=10000)
    is_company = False
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)


class GuarantorFactory(DjangoModelFactory):
    """Factory for Guarantor model."""
    
    class Meta:
        model = Guarantor
    
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    phone = factory.Faker('phone_number')
    date_of_birth = factory.Faker('date_of_birth', minimum_age=18, maximum_age=80)
    guarantor_type = factory.Iterator(['individual', 'company'])
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)


class AssetFactory(DjangoModelFactory):
    """Factory for Asset model."""
    
    class Meta:
        model = Asset
    
    asset_type = factory.Iterator(['property', 'vehicle', 'savings', 'investment', 'other'])
    value = factory.Faker('random_int', min=10000, max=1000000)
    description = factory.Faker('sentence')
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)


class LiabilityFactory(DjangoModelFactory):
    """Factory for Liability model."""
    
    class Meta:
        model = Liability
    
    liability_type = factory.Iterator(['mortgage', 'car_loan', 'personal_loan', 'credit_card', 'other'])
    amount = factory.Faker('random_int', min=5000, max=500000)
    monthly_payment = factory.Faker('random_int', min=200, max=5000)
    description = factory.Faker('sentence')
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)
