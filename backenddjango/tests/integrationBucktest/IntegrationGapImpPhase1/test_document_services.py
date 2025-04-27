"""
Integration tests for document services.
"""
import pytest
from django.contrib.auth import get_user_model
from unittest.mock import patch, MagicMock
import sys
import os

# Mock the weasyprint module
sys.modules['weasyprint'] = MagicMock()
mock_html = MagicMock()
sys.modules['weasyprint'].HTML = mock_html

# Now import the models
from documents.models import Document
from applications.models import Application
from borrowers.models import Borrower, Guarantor

User = get_user_model()

class TestDocumentServices:
    @pytest.fixture
    def admin_user(self):
        """Create an admin user for testing."""
        return User.objects.create_user(
            username="admin",  # Username is required by Django's default User model
            email="admin@example.com",
            password="password123",
            first_name="Admin",
            last_name="User",
            role="admin"
        )

    @pytest.fixture
    def application(self, admin_user):
        """Create a test application."""
        return Application.objects.create(
            reference_number="APP-TEST-001",
            application_type="residential",
            purpose="Home purchase",
            loan_amount=500000.00,
            loan_term=360,
            interest_rate=3.50,
            repayment_frequency="monthly",
            stage="draft",
            created_by=admin_user
        )

    @pytest.fixture
    def borrower(self, admin_user, application):
        """Create a test borrower."""
        borrower = Borrower.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            date_of_birth="1980-01-01",
            created_by=admin_user
        )
        application.borrowers.add(borrower)
        return borrower

    @pytest.fixture
    def guarantor(self, admin_user, borrower, application):
        """Create a test guarantor."""
        return Guarantor.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            phone="0987654321",
            relationship="spouse",
            borrower=borrower,
            application=application,
            created_by=admin_user
        )

    @pytest.fixture
    def company_borrower(self, admin_user, application):
        """Create a test company borrower."""
        borrower = Borrower.objects.create(
            company_name="Acme Corporation",
            is_company=True,
            email="info@acme.com",
            phone="1234567890",
            created_by=admin_user
        )
        application.borrowers.add(borrower)
        return borrower

    @pytest.mark.django_db
    def test_document_creation(self, application, admin_user):
        """Test basic document creation."""
        document = Document.objects.create(
            title="Test Document",
            document_type="test_document",
            file="test_file.pdf",
            file_name="test_file.pdf",
            file_size=1024,
            file_type="application/pdf",
            application=application,
            created_by=admin_user
        )
        
        # Verify document was created
        assert document is not None
        assert document.title == "Test Document"
        assert document.document_type == "test_document"
        assert document.application == application
        assert document.created_by == admin_user
        
        # Verify document in database
        db_document = Document.objects.get(id=document.id)
        assert db_document.title == "Test Document"
        assert db_document.application == application
