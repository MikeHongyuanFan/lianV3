"""
Tests for document services.
"""
import pytest
import os
from unittest.mock import patch, MagicMock
from django.utils import timezone
from documents.services import (
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
@patch('documents.services.render_to_string')
@patch('documents.services.HTML')
def test_generate_document_from_template(mock_html, mock_render, tmp_path, settings):
    """Test generating a document from a template."""
    # Set up test environment
    settings.MEDIA_ROOT = tmp_path
    
    # Mock HTML rendering
    mock_html_instance = MagicMock()
    mock_html.return_value = mock_html_instance
    mock_render.return_value = "<html><body>Test Document</body></html>"
    
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
    
    # Check that the template was rendered with the correct context
    mock_render.assert_called_once_with(template_name, context)
    
    # Check that HTML was created and PDF was written
    mock_html.assert_called_once()
    mock_html_instance.write_pdf.assert_called_once()
    
    # Check that the document was created with correct attributes
    assert document is not None
    assert document.title == output_filename
    assert document.document_type == document_type
    assert document.application == application
    assert document.created_by == user


@pytest.mark.service
@patch('documents.services.generate_document_from_template')
def test_generate_guarantor_letter(mock_generate_document, tmp_path, settings):
    """Test generating a guarantor letter."""
    # Set up test environment
    settings.MEDIA_ROOT = tmp_path
    
    # Create test data
    application = ApplicationFactory()
    borrower = BorrowerFactory()
    guarantor = GuarantorFactory(application=application, borrower=borrower)
    user = AdminUserFactory()
    
    # Mock document generation
    mock_document = DocumentFactory(
        title=f"Guarantor_Letter_{guarantor.id}",
        document_type="guarantor_letter",
        application=application,
        created_by=user
    )
    mock_generate_document.return_value = mock_document
    
    # Call the function
    document = generate_guarantor_letter(guarantor.id, user)
    
    # Check that generate_document_from_template was called with correct parameters
    mock_generate_document.assert_called_once()
    args, kwargs = mock_generate_document.call_args
    assert kwargs['template_name'] == 'documents/guarantor_letter.html'
    assert kwargs['output_filename'] == f"Guarantor_Letter_{guarantor.id}"
    assert kwargs['document_type'] == 'guarantor_letter'
    assert kwargs['application'] == application
    assert kwargs['user'] == user
    
    # Check context data
    context = kwargs['context']
    assert context['guarantor'] == guarantor
    assert context['application'] == application
    assert context['borrower'] == borrower
    assert 'generated_date' in context
    
    # Check that the document was returned
    assert document == mock_document


@pytest.mark.service
def test_generate_guarantor_letter_nonexistent_guarantor():
    """Test generating a guarantor letter for a nonexistent guarantor."""
    # Call the function with a nonexistent guarantor ID
    document = generate_guarantor_letter(999, AdminUserFactory())
    
    # Check that no document was created
    assert document is None


@pytest.mark.service
@patch('documents.services.generate_document_from_template')
def test_generate_company_borrower_documents(mock_generate_document, tmp_path, settings):
    """Test generating company borrower documents."""
    # Set up test environment
    settings.MEDIA_ROOT = tmp_path
    
    # Create test data
    application = ApplicationFactory()
    borrower = BorrowerFactory(is_company=True)
    borrower.applications.add(application)
    user = AdminUserFactory()
    
    # Mock document generation
    mock_declaration = DocumentFactory(
        title=f"Company_Declaration_{borrower.id}",
        document_type="company_declaration",
        application=application,
        created_by=user
    )
    mock_guarantee = DocumentFactory(
        title=f"Director_Guarantee_{borrower.id}",
        document_type="director_guarantee",
        application=application,
        created_by=user
    )
    mock_generate_document.side_effect = [mock_declaration, mock_guarantee]
    
    # Call the function
    documents = generate_company_borrower_documents(borrower.id, user)
    
    # Check that generate_document_from_template was called twice
    assert mock_generate_document.call_count == 2
    
    # Check first call (company declaration)
    args1, kwargs1 = mock_generate_document.call_args_list[0]
    assert kwargs1['template_name'] == 'documents/company_declaration.html'
    assert kwargs1['output_filename'] == f"Company_Declaration_{borrower.id}"
    assert kwargs1['document_type'] == 'company_declaration'
    assert kwargs1['application'] == application
    assert kwargs1['user'] == user
    
    # Check second call (director guarantee)
    args2, kwargs2 = mock_generate_document.call_args_list[1]
    assert kwargs2['template_name'] == 'documents/director_guarantee.html'
    assert kwargs2['output_filename'] == f"Director_Guarantee_{borrower.id}"
    assert kwargs2['document_type'] == 'director_guarantee'
    assert kwargs2['application'] == application
    assert kwargs2['user'] == user
    
    # Check that both documents were returned
    assert len(documents) == 2
    assert documents[0] == mock_declaration
    assert documents[1] == mock_guarantee


@pytest.mark.service
def test_generate_company_borrower_documents_nonexistent_borrower():
    """Test generating company borrower documents for a nonexistent borrower."""
    # Call the function with a nonexistent borrower ID
    documents = generate_company_borrower_documents(999, AdminUserFactory())
    
    # Check that no documents were created
    assert len(documents) == 0


@pytest.mark.service
def test_generate_company_borrower_documents_individual_borrower():
    """Test generating company borrower documents for an individual borrower."""
    # Create an individual borrower
    borrower = BorrowerFactory(is_company=False)
    
    # Call the function
    documents = generate_company_borrower_documents(borrower.id, AdminUserFactory())
    
    # Check that no documents were created
    assert len(documents) == 0


@pytest.mark.service
def test_generate_company_borrower_documents_no_application():
    """Test generating company borrower documents for a borrower with no application."""
    # Create a company borrower with no application
    borrower = BorrowerFactory(is_company=True)
    
    # Call the function
    documents = generate_company_borrower_documents(borrower.id, AdminUserFactory())
    
    # Check that no documents were created
    assert len(documents) == 0
