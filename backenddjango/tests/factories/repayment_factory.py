"""
Factory for creating Repayment objects.
"""
import factory
from factory.django import DjangoModelFactory
from documents.models import Repayment
from tests.factories.user_factory import AdminUserFactory
from tests.factories.application_factory import ApplicationFactory


class RepaymentFactory(DjangoModelFactory):
    """Factory for creating Repayment objects."""

    class Meta:
        model = Repayment

    application = factory.SubFactory(ApplicationFactory)
    amount = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    due_date = factory.Faker('date_this_month')
    created_by = factory.SubFactory(AdminUserFactory)
    status = 'pending'


class PaidRepaymentFactory(RepaymentFactory):
    """Factory for creating paid Repayment objects."""

    status = 'paid'
    paid_date = factory.Faker('date_this_month')
    payment_reference = factory.Sequence(lambda n: f'PAY-{n:05d}')


class PartialRepaymentFactory(RepaymentFactory):
    """Factory for creating partially paid Repayment objects."""

    status = 'partial'
    paid_amount = factory.LazyAttribute(lambda o: o.amount / 2)
    paid_date = factory.Faker('date_this_month')
    payment_reference = factory.Sequence(lambda n: f'PAY-{n:05d}')


class PendingRepaymentFactory(RepaymentFactory):
    """Factory for creating pending Repayment objects."""

    status = 'pending'
    paid_amount = 0
    paid_date = None
    payment_reference = None


class OverdueRepaymentFactory(RepaymentFactory):
    """Factory for creating overdue Repayment objects."""

    status = 'overdue'
    due_date = factory.Faker('date_this_year', before_today=True)
    paid_amount = 0
    paid_date = None
    payment_reference = None
