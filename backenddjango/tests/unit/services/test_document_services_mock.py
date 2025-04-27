"""
Tests for document services using mocks to bypass external dependencies.
"""
import pytest
import os
from unittest.mock import patch, MagicMock, mock_open
from django.utils import timezone
from documents.services_mock import (
    generate_document_from_template,
    generate_guarantor_letter,
    generate_company_borrower_documents
)
from documents.models import Document
from tests.factories import (
    ApplicationFactory, BorrowerFactory, GuarantorFactory, 
    AdminUserFactory, DocumentFactory
)

pytestmark = pytest.mark.django_db


@pytest.mark.service
def test_generate_document_from_template_mock(tmp_path, settings):
    """Test generating a document from a template using mocks."""
    # Set up test environment
    settings.MEDIA_ROOT = tmp_path
    
    # Create test data
    application = ApplicationFactory()
    user = AdminUserFactory()
    template_name = "test_template.html"
    context = {"test": "data"}
    output_filename = "Test_Document"
    document_type = "test_document"
    
    # Call the function
    document = generate_document_from_template(
        template_name=template_name,
        context=context,
        output_filename=output_filename,
        document_type=document_type,
        application=application,
        user=user
    )
    
    # Check that the document was created with correct attributes
    assert document is not None
    assert document.title == output_filename
    assert document.document_type == document_type
    assert document.application == application
    assert document.created_by == user
    assert document.file_size == 1024  # Mock file size
    assert document.file_type == 'application/pdf'
    assert f"{output_filename}_" in document.file_name
    assert ".pdf" in document.file_name


@pytest.mark.service
def test_generate_guarantor_letter_mock():
    """Test generating a guarantor letter using mocks."""
    # Create test data
    application = ApplicationFactory()
    borrower = BorrowerFactory()
    guarantor = GuarantorFactory(application=application, borrower=borrower)
    user = AdminUserFactory()
    
    # Call the function
    document = generate_guarantor_letter(guarantor.id, user)
    
    # Check that the document was created with correct attributes
    assert document is not None
    assert document.title == f"Guarantor_Letter_{guarantor.id}"
    assert document.document_type == 'guarantor_letter'
    assert document.application == application
    assert document.created_by == user


@pytest.mark.service
def test_generate_guarantor_letter_nonexistent_guarantor_mock():
    """Test generating a guarantor letter for a nonexistent guarantor."""
    # Call the function with a nonexistent guarantor ID
    document = generate_guarantor_letter(999, AdminUserFactory())
    
    # Check that no document was created
    assert document is None


@pytest.mark.service
def test_generate_company_borrower_documents_mock():
    """Test generating company borrower documents using mocks."""
    # Create test data
    application = ApplicationFactory()
    borrower = BorrowerFactory(is_company=True)
    application.borrowers.add(borrower)
    user = AdminUserFactory()
    
    # Call the function
    documents = generate_company_borrower_documents(borrower.id, user)
    
    # Check that both documents were created
    assert len(documents) == 2
    
    # Check company declaration document
    declaration = documents[0]
    assert declaration.title == f"Company_Declaration_{borrower.id}"
    assert declaration.document_type == 'company_declaration'
    assert declaration.application == application
    assert declaration.created_by == user
    
    # Check director guarantee document
    guarantee = documents[1]
    assert guarantee.title == f"Director_Guarantee_{borrower.id}"
    assert guarantee.document_type == 'director_guarantee'
    assert guarantee.application == application
    assert guarantee.created_by == user


@pytest.mark.service
def test_generate_company_borrower_documents_nonexistent_borrower_mock():
    """Test generating company borrower documents for a nonexistent borrower."""
    # Call the function with a nonexistent borrower ID
    documents = generate_company_borrower_documents(999, AdminUserFactory())
    
    # Check that no documents were created
    assert len(documents) == 0


@pytest.mark.service
def test_generate_company_borrower_documents_individual_borrower_mock():
    """Test generating company borrower documents for an individual borrower."""
    # Create an individual borrower
    borrower = BorrowerFactory(is_company=False)
    
    # Call the function
    documents = generate_company_borrower_documents(borrower.id, AdminUserFactory())
    
    # Check that no documents were created
    assert len(documents) == 0


@pytest.mark.service
def test_generate_company_borrower_documents_no_application_mock():
    """Test generating company borrower documents for a borrower with no application."""
    # Create a company borrower with no application
    borrower = BorrowerFactory(is_company=True)
    
    # Call the function
    documents = generate_company_borrower_documents(borrower.id, AdminUserFactory())
    
    # Check that no documents were created
    assert len(documents) == 0
