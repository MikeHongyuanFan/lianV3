"""
Factories for document models.
"""
import factory
from factory.django import DjangoModelFactory
from documents.models import Document, Note, Fee, Repayment
from django.utils import timezone
from .user_factories import UserFactory


class DocumentFactory(DjangoModelFactory):
    """Factory for Document model."""
    
    class Meta:
        model = Document
    
    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('paragraph')
    document_type = factory.Iterator([
        'application_form', 'loan_agreement', 'bank_statement',
        'payslip', 'tax_return', 'id_verification', 'other'
    ])
    file_name = factory.Sequence(lambda n: f'document_{n}.pdf')
    file_size = factory.Faker('random_int', min=1000, max=10000000)
    file_type = 'application/pdf'
    version = 1
    created_by = factory.SubFactory(UserFactory)
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)


class NoteFactory(DjangoModelFactory):
    """Factory for Note model."""
    
    class Meta:
        model = Note
    
    title = factory.Faker('sentence', nb_words=4)
    content = factory.Faker('paragraph')
    created_by = factory.SubFactory(UserFactory)
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)
    remind_date = None
    
    @factory.post_generation
    def borrower(self, create, extracted, **kwargs):
        """Add a borrower to the note if provided."""
        if not create:
            return
        
        if extracted:
            self.borrower = extracted


class FeeFactory(DjangoModelFactory):
    """Factory for Fee model."""
    
    class Meta:
        model = Fee
    
    fee_type = factory.Iterator(['application', 'valuation', 'legal', 'settlement', 'broker', 'other'])
    description = factory.Faker('sentence')
    amount = factory.Faker('random_int', min=100, max=10000)
    due_date = factory.LazyFunction(lambda: timezone.now().date() + timezone.timedelta(days=30))
    paid_date = None
    created_by = factory.SubFactory(UserFactory)
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)


class RepaymentFactory(DjangoModelFactory):
    """Factory for Repayment model."""
    
    class Meta:
        model = Repayment
    
    amount = factory.Faker('random_int', min=500, max=5000)
    due_date = factory.LazyFunction(lambda: timezone.now().date() + timezone.timedelta(days=30))
    paid_date = None
    reminder_sent = False
    overdue_3_day_sent = False
    overdue_7_day_sent = False
    overdue_10_day_sent = False
    created_by = factory.SubFactory(UserFactory)
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)
