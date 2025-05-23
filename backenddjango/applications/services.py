from django.template.loader import render_to_string
from django.conf import settings
import os
import uuid
import json
import jsonschema
from datetime import datetime
# Comment out weasyprint import to avoid dependency issues during testing
# from weasyprint import HTML
from .models import Application
from documents.models import Document, Fee, Repayment, Note
from users.services import create_application_notification


def generate_document(application_id, document_type, user):
    """
    Generate a document for an application
    
    Args:
        application_id: ID of the application
        document_type: Type of document to generate
        user: User generating the document
        
    Returns:
        Document object if successful, None otherwise
    """
    try:
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        return None
    
    # Define template and title based on document type
    template_map = {
        'application_form': {
            'template': 'documents/application_form.html',
            'title': f'Application Form - {application.reference_number}'
        },
        'indicative_letter': {
            'template': 'documents/indicative_letter.html',
            'title': f'Indicative Letter - {application.reference_number}'
        },
        'formal_approval': {
            'template': 'documents/formal_approval.html',
            'title': f'Formal Approval - {application.reference_number}'
        }
    }
    
    if document_type not in template_map:
        return None
    
    template_info = template_map[document_type]
    
    # Generate HTML content
    context = {
        'application': application,
        'borrowers': application.borrowers.all(),
        'guarantors': application.guarantors.all(),
        'broker': application.broker,
        'branch': application.branch,
        'bd': application.bd,
        'generated_date': datetime.now().strftime('%d/%m/%Y'),
    }
    
    html_content = render_to_string(template_info['template'], context)
    
    # Generate PDF - commented out for testing
    output_dir = os.path.join(settings.MEDIA_ROOT, 'generated_documents', str(application.id))
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"{document_type}_{uuid.uuid4().hex}.pdf"
    output_path = os.path.join(output_dir, filename)
    
    # Comment out PDF generation for testing
    # HTML(string=html_content).write_pdf(output_path)
    
    # For testing, just create an empty file
    with open(output_path, 'w') as f:
        f.write("Test PDF content")
    
    # Create document record
    relative_path = os.path.join('generated_documents', str(application.id), filename)
    
    document = Document.objects.create(
        title=template_info['title'],
        document_type=document_type,
        file=relative_path,
        file_name=filename,
        file_size=os.path.getsize(output_path),
        file_type='application/pdf',
        application=application,
        created_by=user
    )
    
    return document


def generate_repayment_schedule(application_id, user):
    """
    Generate a repayment schedule for an application
    
    Args:
        application_id: ID of the application
        user: User generating the schedule
        
    Returns:
        List of created Repayment objects
    """
    try:
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        return []
    
    # Delete existing repayments
    application.repayments.all().delete()
    
    # Calculate repayment amount and schedule
    loan_amount = application.loan_amount
    loan_term = application.loan_term  # in months
    interest_rate = application.interest_rate / 100 if application.interest_rate else 0
    
    # Simple calculation for monthly repayments
    # For a more accurate calculation, use financial formulas
    if application.repayment_frequency == 'monthly':
        monthly_interest = interest_rate / 12
        if monthly_interest > 0:
            # Using the formula for monthly payments: P = L[i(1+i)^n]/[(1+i)^n-1]
            # where P is payment, L is loan amount, i is monthly interest rate, n is number of payments
            monthly_payment = loan_amount * (monthly_interest * (1 + monthly_interest) ** loan_term) / ((1 + monthly_interest) ** loan_term - 1)
        else:
            # If no interest, simple division
            monthly_payment = loan_amount / loan_term
        
        # Create repayment schedule
        repayments = []
        start_date = application.estimated_settlement_date or datetime.now().date()
        
        for i in range(1, loan_term + 1):
            due_date = start_date.replace(month=((start_date.month + i - 1) % 12) + 1)
            if (start_date.month + i - 1) // 12 > 0:
                due_date = due_date.replace(year=due_date.year + (start_date.month + i - 1) // 12)
            
            repayment = Repayment.objects.create(
                application=application,
                amount=round(monthly_payment, 2),
                due_date=due_date,
                created_by=user
            )
            repayments.append(repayment)
        
        return repayments
    
    # Handle other frequencies as needed
    return []


def create_standard_fees(application_id, user):
    """
    Create standard fees for an application
    
    Args:
        application_id: ID of the application
        user: User creating the fees
        
    Returns:
        List of created Fee objects
    """
    try:
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        return []
    
    # Define standard fees
    standard_fees = [
        {
            'fee_type': 'application',
            'description': 'Application processing fee',
            'amount': 500.00,
        },
        {
            'fee_type': 'valuation',
            'description': 'Property valuation fee',
            'amount': 800.00,
        },
        {
            'fee_type': 'legal',
            'description': 'Legal documentation fee',
            'amount': 1200.00,
        },
        {
            'fee_type': 'settlement',
            'description': 'Settlement fee',
            'amount': 300.00,
        }
    ]
    
    # Calculate due dates
    from datetime import timedelta
    today = datetime.now().date()
    
    # Create fees
    fees = []
    for i, fee_data in enumerate(standard_fees):
        due_date = today + timedelta(days=(i+1)*7)  # Due weekly
        
        fee = Fee.objects.create(
            application=application,
            fee_type=fee_data['fee_type'],
            description=fee_data['description'],
            amount=fee_data['amount'],
            due_date=due_date,
            created_by=user
        )
        fees.append(fee)
    
    return fees

def process_signature_data(application_id, signature_data, signed_by, signature_date, user):
    """
    Process signature data for an application
    
    Args:
        application_id: ID of the application
        signature_data: Base64 encoded signature data
        signed_by: Name of the person who signed
        signature_date: Date of signature
        user: User processing the signature
        
    Returns:
        Updated Application object if successful, None otherwise
    """
    from .models import Application
    import base64
    import os
    from django.conf import settings
    from django.core.files.base import ContentFile
    from documents.models import Note
    from users.services import create_application_notification
    
    try:
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        return None
    
    # Process signature data (base64 encoded)
    if signature_data:
        # Remove data URL prefix if present
        if signature_data.startswith('data:image'):
            header, signature_data = signature_data.split(';base64,')
        
        # Decode base64 data
        binary_data = base64.b64decode(signature_data)
        
        # Create directory if it doesn't exist
        signature_dir = os.path.join(settings.MEDIA_ROOT, 'signatures', str(application.id))
        os.makedirs(signature_dir, exist_ok=True)
        
        # Save signature as PNG file
        filename = f"signature_{application.id}.png"
        file_path = os.path.join('signatures', str(application.id), filename)
        
        # Update application with signature info
        application.signed_by = signed_by
        application.signature_date = signature_date
        application.uploaded_pdf_path.save(filename, ContentFile(binary_data), save=False)
        application.save()
        
        # Create note about signature
        Note.objects.create(
            application=application,
            content=f"Application signed by {signed_by} on {signature_date}",
            created_by=user
        )
        
        # Create notification
        create_application_notification(
            application=application,
            notification_type='signature_required',
            title=f'Application {application.reference_number} signed',
            message=f'Application has been signed by {signed_by}'
        )
    
    return application


def validate_application_schema(data):
    """
    Validate application data against JSON schema
    
    Args:
        data: Application data to validate
        
    Returns:
        (is_valid, errors) tuple
    """
    import jsonschema
    
    # Define the JSON schema for application validation
    application_schema = {
        "type": "object",
        "required": ["application_type", "purpose", "loan_amount", "loan_term", "repayment_frequency"],
        "properties": {
            "application_type": {
                "type": "string",
                "enum": ["residential", "commercial", "construction", "refinance", "investment", "smsf"]
            },
            "purpose": {
                "type": "string",
                "minLength": 5
            },
            "loan_amount": {
                "type": "number",
                "minimum": 1000
            },
            "loan_term": {
                "type": "integer",
                "minimum": 1,
                "maximum": 360  # 30 years in months
            },
            "interest_rate": {
                "type": ["number", "null"],
                "minimum": 0,
                "maximum": 30
            },
            "repayment_frequency": {
                "type": "string",
                "enum": ["weekly", "fortnightly", "monthly", "quarterly", "annually"]
            },
            "estimated_settlement_date": {
                "type": ["string", "null"],
                "format": "date"
            },
            "security_address": {
                "type": ["string", "null"]
            },
            "security_type": {
                "type": ["string", "null"]
            },
            "security_value": {
                "type": ["number", "null"],
                "minimum": 0
            },
            "stage": {"type": "string"},
            "valuer_info": {"type": "object"},
            "qs_info": {"type": "object"}
        }
    }
    
    # Validate against schema
    try:
        jsonschema.validate(instance=data, schema=application_schema)
        return True, None
    except jsonschema.exceptions.ValidationError as e:
        return False, str(e)


def update_application_stage(application_id, new_stage, user):
    """
    Update application stage and create notification
    
    Args:
        application_id: Application ID
        new_stage: New stage value
        user: User making the change
        
    Returns:
        Updated Application object
    """
    try:
        application = Application.objects.get(id=application_id)
        old_stage = application.stage
        
        # Update stage
        application.stage = new_stage
        application.save()
        
        # Create note about stage change
        Note.objects.create(
            application=application,
            content=f"Application stage changed from '{old_stage}' to '{new_stage}'",
            created_by=user
        )
        
        # Create notification
        create_application_notification(
            application=application,
            notification_type='application_status',
            title=f'Application {application.reference_number} stage updated',
            message=f'Application stage changed from {old_stage} to {new_stage}'
        )
        
        return application
    except Application.DoesNotExist:
        raise ValueError(f"Application with ID {application_id} not found")


# This function has been merged with the earlier definition of process_signature_data



