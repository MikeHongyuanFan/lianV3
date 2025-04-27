"""
Factory for creating Broker objects.
"""
import factory
from factory.django import DjangoModelFactory
from brokers.models import Broker, Branch, BDM
from tests.factories.user_factory import BrokerUserFactory, BDMUserFactory


class BrokerFactory(DjangoModelFactory):
    """Factory for creating Broker objects."""

    class Meta:
        model = Broker
        django_get_or_create = ('email',)

    name = factory.Faker('company')
    user = factory.SubFactory(BrokerUserFactory)
    email = factory.SelfAttribute('user.email')
    phone = factory.Faker('phone_number')
    address = factory.Faker('address')
    accreditation_number = factory.Sequence(lambda n: f'ACC{n:05d}')
    is_active = True


class SeniorBrokerFactory(BrokerFactory):
    """Factory for creating senior Broker objects."""

    is_senior = True


class BranchFactory(DjangoModelFactory):
    """Factory for creating Branch objects."""

    class Meta:
        model = Branch
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: f'Branch {n}')
    address = factory.Faker('address')
    phone = factory.Faker('phone_number')
    email = factory.Faker('company_email')
    is_active = True


class BDMFactory(DjangoModelFactory):
    """Factory for creating BDM objects."""

    class Meta:
        model = BDM
        django_get_or_create = ('email',)

    user = factory.SubFactory(BDMUserFactory)
    name = factory.Faker('name')
    email = factory.SelfAttribute('user.email')
    phone = factory.Faker('phone_number')
    is_active = True
