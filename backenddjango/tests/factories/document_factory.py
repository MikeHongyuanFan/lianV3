"""
Factory for creating Document objects.
"""
import factory
import tempfile
from factory.django import DjangoModelFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from documents.models import Document, Fee
from tests.factories.user_factory import AdminUserFactory
from tests.factories.application_factory import ApplicationFactory


class DocumentFactory(DjangoModelFactory):
    """Factory for creating Document objects."""

    class Meta:
        model = Document

    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('paragraph', nb_sentences=2)
    document_type = factory.Iterator(['application_form', 'id_verification', 'income_proof', 'property_valuation', 'other'])
    application = factory.SubFactory(ApplicationFactory)
    created_by = factory.SubFactory(AdminUserFactory)
    file_name = factory.Sequence(lambda n: f'document_{n}.pdf')
    file_size = factory.Faker('random_int', min=1000, max=10000000)
    file_type = 'application/pdf'

    @factory.lazy_attribute
    def file(self):
        """Create a temporary file for the document."""
        temp_file = tempfile.NamedTemporaryFile(suffix='.pdf')
        temp_file.write(b'Test file content')
        temp_file.seek(0)
        return SimpleUploadedFile(
            self.file_name,
            temp_file.read(),
            content_type=self.file_type
        )


class FeeFactory(DjangoModelFactory):
    """Factory for creating Fee objects."""

    class Meta:
        model = Fee

    fee_type = factory.Iterator(['application', 'valuation', 'legal', 'broker', 'other'])
    description = factory.Faker('sentence', nb_words=3)
    amount = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    due_date = factory.Faker('date_this_month')
    application = factory.SubFactory(ApplicationFactory)
    created_by = factory.SubFactory(AdminUserFactory)
    is_paid = False


class PaidFeeFactory(FeeFactory):
    """Factory for creating paid Fee objects."""

    is_paid = True
    paid_date = factory.Faker('date_this_month')
    payment_reference = factory.Sequence(lambda n: f'PAY-{n:05d}')
