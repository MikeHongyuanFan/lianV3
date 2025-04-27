from .models import Application
from django.utils import timezone
from users.models import Notification
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

def update_application_stage(application_id, new_stage, user):
    """
    Update the stage of an application and create notifications
    """
    try:
        application = Application.objects.get(pk=application_id)
    except Application.DoesNotExist:
        raise ValueError(f"Application with ID {application_id} not found")
    
    # Check if the stage is valid
    if new_stage not in dict(Application.STAGE_CHOICES):
        raise ValueError(f"Invalid stage: {new_stage}")
    
    # Update the stage
    old_stage = application.stage
    application.stage = new_stage
    application.updated_at = timezone.now()
    application.save()
    
    # Create a note about the stage change
    from documents.models import Note
    Note.objects.create(
        application=application,
        content=f"Application stage changed from {old_stage} to {new_stage}",
        created_by=user
    )
    
    # Create notifications for relevant users
    _create_stage_change_notifications(application, old_stage, new_stage)
    
    return application

def _create_stage_change_notifications(application, old_stage, new_stage):
    """
    Create notifications for stage changes
    """
    # Notify broker
    if application.broker and application.broker.user:
        Notification.objects.create(
            user=application.broker.user,
            title=f"Application Status Update: {application.reference_number}",
            message=f"Application status changed from {old_stage} to {new_stage}",
            notification_type="application_status",
            related_object_id=application.id,
            related_object_type="application"
        )
    
    # Notify BD
    if application.bd and application.bd.user:
        Notification.objects.create(
            user=application.bd.user,
            title=f"Application Status Update: {application.reference_number}",
            message=f"Application status changed from {old_stage} to {new_stage}",
            notification_type="application_status",
            related_object_id=application.id,
            related_object_type="application"
        )
    
    # Notify borrowers
    for borrower in application.borrowers.all():
        if borrower.user:
            Notification.objects.create(
                user=borrower.user,
                title=f"Application Status Update: {application.reference_number}",
                message=f"Your application status has changed from {old_stage} to {new_stage}",
                notification_type="application_status",
                related_object_id=application.id,
                related_object_type="application"
            )

def process_signature_data(application_id, signature_data, signed_by, user):
    """
    Process signature data for an application
    """
    try:
        application = Application.objects.get(pk=application_id)
    except Application.DoesNotExist:
        logger.error(f"Application with ID {application_id} not found")
        return None
    
    try:
        with transaction.atomic():
            # Update application with signature data
            application.signed_by = signed_by
            application.signature_date = timezone.now().date()
            
            # In a real app, we would save the signature image
            # For now, just simulate PDF generation
            application.uploaded_pdf_path = f"signatures/application_{application.id}_signed.pdf"
            application.save()
            
            # Create notifications for relevant users
            _create_signature_notifications(application, signed_by)
            
            return application
    except Exception as e:
        logger.error(f"Error processing signature: {str(e)}")
        return None

def _create_signature_notifications(application, signed_by):
    """
    Create notifications for signature events
    """
    # Notify broker
    if application.broker and application.broker.user:
        Notification.objects.create(
            user=application.broker.user,
            title=f"Application Signed: {application.reference_number}",
            message=f"Application has been signed by {signed_by}",
            notification_type="document_signed",
            related_object_id=application.id,
            related_object_type="application"
        )
    
    # Notify BD
    if application.bd and application.bd.user:
        Notification.objects.create(
            user=application.bd.user,
            title=f"Application Signed: {application.reference_number}",
            message=f"Application has been signed by {signed_by}",
            notification_type="document_signed",
            related_object_id=application.id,
            related_object_type="application"
        )
