"""
Mock implementations of document services to bypass external dependencies.
"""
import os
import uuid
from datetime import datetime
from django.conf import settings
from .models import Document


def generate_document_from_template(template_name, context, output_filename, document_type, application, user):
    """
    Generate a document from a template (mock implementation)
    
    Args:
        template_name: Name of the template file
        context: Context data for the template
        output_filename: Name for the output file
        document_type: Type of document being generated
        application: Application object
        user: User generating the document
        
    Returns:
        Document object if successful, None otherwise
    """
    # In the mock implementation, we skip actual PDF generation
    # but still create a Document record
    
    # Generate a unique filename
    filename = f"{output_filename}_{uuid.uuid4().hex}.pdf"
    
    # Create a relative path for the document
    relative_path = os.path.join('generated_documents', str(application.id), filename)
    
    # Create document record
    document = Document.objects.create(
        title=output_filename,
        document_type=document_type,
        file=relative_path,
        file_name=filename,
        file_size=1024,  # Mock file size
        file_type='application/pdf',
        application=application,
        created_by=user
    )
    
    return document


def generate_guarantor_letter(guarantor_id, user):
    """
    Generate a guarantor letter (mock implementation)
    
    Args:
        guarantor_id: ID of the guarantor
        user: User generating the document
        
    Returns:
        Document object if successful, None otherwise
    """
    from borrowers.models import Guarantor
    
    try:
        guarantor = Guarantor.objects.get(id=guarantor_id)
    except Guarantor.DoesNotExist:
        return None
    
    application = guarantor.application
    
    # Generate context
    context = {
        'guarantor': guarantor,
        'application': application,
        'borrower': guarantor.borrower,
        'generated_date': datetime.now().strftime('%d/%m/%Y'),
    }
    
    # Generate document
    template_name = 'documents/guarantor_letter.html'
    output_filename = f"Guarantor_Letter_{guarantor.id}"
    
    return generate_document_from_template(
        template_name=template_name,
        context=context,
        output_filename=output_filename,
        document_type='guarantor_letter',
        application=application,
        user=user
    )


def generate_company_borrower_documents(borrower_id, user):
    """
    Generate company borrower specific documents (mock implementation)
    
    Args:
        borrower_id: ID of the company borrower
        user: User generating the document
        
    Returns:
        List of Document objects if successful, empty list otherwise
    """
    from borrowers.models import Borrower
    
    try:
        borrower = Borrower.objects.get(id=borrower_id, is_company=True)
    except Borrower.DoesNotExist:
        return []
    
    # Get the first application for this borrower
    applications = borrower.borrower_applications.all()
    application = applications.first() if applications.exists() else None
    if not application:
        return []
    
    documents = []
    
    # Generate company declaration
    context = {
        'borrower': borrower,
        'application': application,
        'generated_date': datetime.now().strftime('%d/%m/%Y'),
    }
    
    company_declaration = generate_document_from_template(
        template_name='documents/company_declaration.html',
        context=context,
        output_filename=f"Company_Declaration_{borrower.id}",
        document_type='company_declaration',
        application=application,
        user=user
    )
    
    if company_declaration:
        documents.append(company_declaration)
    
    # Generate director's guarantee
    director_guarantee = generate_document_from_template(
        template_name='documents/director_guarantee.html',
        context=context,
        output_filename=f"Director_Guarantee_{borrower.id}",
        document_type='director_guarantee',
        application=application,
        user=user
    )
    
    if director_guarantee:
        documents.append(director_guarantee)
    
    return documents
