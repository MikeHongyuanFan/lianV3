"""
Factory for creating Borrower objects.
"""
import factory
from factory.django import DjangoModelFactory
from borrowers.models import Borrower, Guarantor
from tests.factories.user_factory import AdminUserFactory


class BorrowerFactory(DjangoModelFactory):
    """Factory for creating Borrower objects."""

    class Meta:
        model = Borrower
        django_get_or_create = ('email',)

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    phone = factory.Faker('phone_number')
    residential_address = factory.Faker('address')
    is_company = False
    created_by = factory.SubFactory(AdminUserFactory)


class CompanyBorrowerFactory(BorrowerFactory):
    """Factory for creating company Borrower objects."""

    is_company = True
    company_name = factory.Faker('company')
    company_abn = factory.Sequence(lambda n: f'{n:011d}')
    company_acn = factory.Sequence(lambda n: f'{n:09d}')
    company_address = factory.Faker('address')


class GuarantorFactory(DjangoModelFactory):
    """Factory for creating Guarantor objects."""

    class Meta:
        model = Guarantor
        django_get_or_create = ('email',)

    guarantor_type = 'individual'
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    phone = factory.Faker('phone_number')
    address = factory.Faker('address')
    borrower = factory.SubFactory(BorrowerFactory)
    created_by = factory.SubFactory(AdminUserFactory)


class CompanyGuarantorFactory(GuarantorFactory):
    """Factory for creating company Guarantor objects."""

    guarantor_type = 'company'
    company_name = factory.Faker('company')
    company_abn = factory.Sequence(lambda n: f'{n:011d}')
    company_acn = factory.Sequence(lambda n: f'{n:09d}')
