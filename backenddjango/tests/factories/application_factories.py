"""
Factories for application models.
"""
import factory
from factory.django import DjangoModelFactory
from applications.models import Application
from django.utils import timezone
from datetime import timedelta
from .user_factories import UserFactory
from .broker_factories import BrokerFactory, BDMFactory


class ApplicationFactory(DjangoModelFactory):
    """Factory for Application model."""
    
    class Meta:
        model = Application
    
    reference_number = factory.Sequence(lambda n: f'APP-{n:06d}')
    application_type = factory.Iterator(['residential', 'commercial', 'personal', 'asset_finance'])
    purpose = factory.Faker('sentence')
    loan_amount = factory.Faker('random_int', min=50000, max=2000000)
    loan_term = factory.Faker('random_int', min=1, max=30)
    interest_rate = factory.Faker('pyfloat', left_digits=2, right_digits=2, positive=True, max_value=10)
    repayment_frequency = factory.Iterator(['weekly', 'fortnightly', 'monthly'])
    stage = factory.Iterator(['inquiry', 'assessment', 'approved', 'settlement', 'funded'])
    broker = factory.SubFactory(BrokerFactory)
    bd = factory.SubFactory(BDMFactory)
    created_by = factory.SubFactory(UserFactory)
    
    class Params:
        """Parameters for customizing the factory."""
        days_old = 0  # Default to current date
    
    @factory.lazy_attribute
    def created_at(self):
        """Generate a created_at date based on days_old parameter."""
        if self.days_old > 0:
            return timezone.now() - timedelta(days=self.days_old)
        return timezone.now()
    
    @factory.lazy_attribute
    def updated_at(self):
        """Generate an updated_at date based on days_old parameter."""
        if self.days_old > 0:
            return timezone.now() - timedelta(days=self.days_old)
        return timezone.now()
    
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the _create method to handle days_old parameter."""
        days_old = kwargs.pop('days_old', 0)
        
        if days_old > 0:
            past_date = timezone.now() - timedelta(days=days_old)
            kwargs['created_at'] = past_date
            kwargs['updated_at'] = past_date
        
        return super()._create(model_class, *args, **kwargs)


class StaleApplicationFactory(ApplicationFactory):
    """Factory for creating stale applications (older than 14 days)."""
    days_old = 15  # Default to 15 days old (stale)
    stage = 'assessment'  # Default to assessment stage
