"""
Factory for creating Note instances for testing.
"""
import factory
from django.utils import timezone
from documents.models import Note
from tests.factories.user_factory import UserFactory
from tests.factories.application_factory import ApplicationFactory


class NoteFactory(factory.django.DjangoModelFactory):
    """Factory for creating Note instances."""
    
    class Meta:
        model = Note
    
    title = factory.Sequence(lambda n: f"Test Note {n}")
    content = factory.Sequence(lambda n: f"This is test note content {n}")
    created_by = factory.SubFactory(UserFactory)
    application = factory.SubFactory(ApplicationFactory)
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
