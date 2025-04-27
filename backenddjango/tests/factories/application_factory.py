"""
Factory for creating Application objects.
"""
import factory
from factory.django import DjangoModelFactory
from applications.models import Application
from tests.factories.user_factory import AdminUserFactory
from tests.factories.broker_factory import BrokerFactory, BranchFactory, BDMFactory
from tests.factories.borrower_factory import BorrowerFactory


class ApplicationFactory(DjangoModelFactory):
    """Factory for creating Application objects."""

    class Meta:
        model = Application
        django_get_or_create = ('reference_number',)

    reference_number = factory.Sequence(lambda n: f'APP-TEST-{n:05d}')
    stage = 'assessment'
    loan_amount = factory.Faker('pydecimal', left_digits=6, right_digits=2, positive=True)
    loan_term = factory.Faker('random_int', min=12, max=360)
    interest_rate = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True)
    purpose = factory.Faker('sentence', nb_words=4)
    application_type = factory.Iterator(['residential', 'commercial', 'personal'])
    broker = factory.SubFactory(BrokerFactory)
    branch = factory.SubFactory(BranchFactory)
    bd = factory.SubFactory(BDMFactory)
    created_by = factory.SubFactory(AdminUserFactory)
    signed_by = factory.SelfAttribute('created_by.username')  # Store username as string


class ResidentialApplicationFactory(ApplicationFactory):
    """Factory for creating residential Application objects."""

    application_type = 'residential'
    property_address = factory.Faker('address')
    property_value = factory.Faker('pydecimal', left_digits=6, right_digits=2, positive=True)


class CommercialApplicationFactory(ApplicationFactory):
    """Factory for creating commercial Application objects."""

    application_type = 'commercial'
    business_name = factory.Faker('company')
    business_abn = factory.Sequence(lambda n: f'{n:011d}')
    business_address = factory.Faker('address')


class PersonalApplicationFactory(ApplicationFactory):
    """Factory for creating personal Application objects."""

    application_type = 'personal'
    purpose_details = factory.Faker('paragraph')


class ApplicationWithBorrowerFactory(ApplicationFactory):
    """Factory for creating Application objects with a borrower."""

    @factory.post_generation
    def borrowers(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for borrower in extracted:
                self.borrowers.add(borrower)
        else:
            borrower = BorrowerFactory()
            self.borrowers.add(borrower)
