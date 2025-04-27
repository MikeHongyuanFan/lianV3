"""
Factories for broker models.
"""
import factory
from factory.django import DjangoModelFactory
from brokers.models import Broker, BDM, Branch
from django.utils import timezone
from .user_factories import UserFactory


class BranchFactory(DjangoModelFactory):
    """Factory for Branch model."""
    
    class Meta:
        model = Branch
    
    name = factory.Faker('company')
    address = factory.Faker('address')
    phone = factory.Faker('phone_number')
    email = factory.Faker('company_email')
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)


class BDMFactory(DjangoModelFactory):
    """Factory for BDM model."""
    
    class Meta:
        model = BDM
    
    user = factory.SubFactory(UserFactory, role='bd')
    name = factory.Faker('name')
    email = factory.Faker('email')
    phone = factory.Faker('phone_number')
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)


class BrokerFactory(DjangoModelFactory):
    """Factory for Broker model."""
    
    class Meta:
        model = Broker
    
    user = factory.SubFactory(UserFactory, role='broker')
    name = factory.Faker('name')
    company = factory.Faker('company')
    email = factory.Faker('email')
    phone = factory.Faker('phone_number')
    address = factory.Faker('address')
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)
