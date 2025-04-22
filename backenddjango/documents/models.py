from django.db import models
from django.conf import settings
import os
from model_utils import FieldTracker
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


def document_upload_path(instance, filename):
    """Generate path for document uploads"""
    app_ref = instance.application.reference_number if instance.application else "no_app"
    return f"documents/{app_ref}/{filename}"


def invoice_upload_path(instance, filename):
    """Generate path for invoice uploads"""
    app_ref = instance.application.reference_number if instance.application else "no_app"
    return f"invoices/{app_ref}/{filename}"


class Document(models.Model):
    """
    Model for documents
    """
    DOCUMENT_TYPE_CHOICES = [
        ('application_form', 'Application Form'),
        ('indicative_letter', 'Indicative Letter'),
        ('formal_approval', 'Formal Approval'),
        ('valuation_report', 'Valuation Report'),
        ('qs_report', 'Quantity Surveyor Report'),
        ('id_verification', 'ID Verification'),
        ('bank_statement', 'Bank Statement'),
        ('payslip', 'Payslip'),
        ('tax_return', 'Tax Return'),
        ('contract', 'Contract'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=255, null=True, blank=True, default='')
    description = models.TextField(null=True, blank=True)
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES, default='other')
    file = models.FileField(upload_to=document_upload_path)
    file_name = models.CharField(max_length=255, null=True, blank=True, default='document.pdf')
    file_size = models.PositiveIntegerField(help_text="File size in bytes", null=True, blank=True, default=0)
    file_type = models.CharField(max_length=100, help_text="MIME type", null=True, blank=True, default='application/pdf')
    
    # Versioning
    version = models.PositiveIntegerField(default=1)
    previous_version = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='next_versions')
    
    # Relationships
    application = models.ForeignKey('applications.Application', on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    borrower = models.ForeignKey('borrowers.Borrower', on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.get_document_type_display()} (v{self.version})"
    
    def save(self, *args, **kwargs):
        # Set file_name if not provided
        if not self.file_name and self.file:
            self.file_name = os.path.basename(self.file.name)
        
        # Set file_size if not provided
        if not self.file_size and self.file:
            self.file_size = self.file.size
        
        super().save(*args, **kwargs)


class Note(models.Model):
    """
    Model for notes
    """
    title = models.CharField(max_length=255, null=True, blank=True, default='Note')
    content = models.TextField(null=True, blank=True, default='')
    remind_date = models.DateTimeField(null=True, blank=True)
    
    # Relationships
    application = models.ForeignKey('applications.Application', on_delete=models.CASCADE, related_name='notes', null=True, blank=True)
    borrower = models.ForeignKey('borrowers.Borrower', on_delete=models.SET_NULL, null=True, blank=True, related_name='notes')
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Fee(models.Model):
    """
    Model for fees
    """
    FEE_TYPE_CHOICES = [
        ('application', 'Application Fee'),
        ('valuation', 'Valuation Fee'),
        ('legal', 'Legal Fee'),
        ('broker', 'Broker Fee'),
        ('settlement', 'Settlement Fee'),
        ('other', 'Other Fee'),
    ]
    
    fee_type = models.CharField(max_length=20, choices=FEE_TYPE_CHOICES)
    description = models.TextField(null=True, blank=True, default='')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField(null=True, blank=True)
    paid_date = models.DateField(null=True, blank=True)
    invoice = models.FileField(upload_to=invoice_upload_path, null=True, blank=True)
    
    # Add field tracker for paid_date
    tracker = FieldTracker(fields=['paid_date'])
    
    # Relationships
    application = models.ForeignKey('applications.Application', on_delete=models.CASCADE, related_name='fees')
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['due_date']
    
    def __str__(self):
        return f"{self.get_fee_type_display()} - ${self.amount}"


class Repayment(models.Model):
    """
    Model for repayments
    """
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField(null=True, blank=True)
    paid_date = models.DateField(null=True, blank=True)
    invoice = models.FileField(upload_to=invoice_upload_path, null=True, blank=True)
    
    # Add field tracker for paid_date
    tracker = FieldTracker(fields=['paid_date'])
    
    # Relationships
    application = models.ForeignKey('applications.Application', on_delete=models.CASCADE, related_name='repayments')
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Notification flags
    reminder_sent = models.BooleanField(default=False)
    overdue_3_day_sent = models.BooleanField(default=False)
    overdue_7_day_sent = models.BooleanField(default=False)
    overdue_10_day_sent = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['due_date']
    
    def __str__(self):
        return f"Repayment ${self.amount} due {self.due_date}"


class Ledger(models.Model):
    """
    Model for financial ledger
    """
    TRANSACTION_TYPE_CHOICES = [
        ('fee_created', 'Fee Created'),
        ('fee_paid', 'Fee Paid'),
        ('repayment_scheduled', 'Repayment Scheduled'),
        ('repayment_received', 'Repayment Received'),
        ('adjustment', 'Adjustment'),
    ]
    
    application = models.ForeignKey('applications.Application', on_delete=models.CASCADE, related_name='ledger_entries')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    transaction_date = models.DateTimeField(null=True, blank=True)
    
    # Relationships to related entities
    related_fee = models.ForeignKey(Fee, on_delete=models.SET_NULL, null=True, blank=True, related_name='ledger_entries')
    related_repayment = models.ForeignKey(Repayment, on_delete=models.SET_NULL, null=True, blank=True, related_name='ledger_entries')
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-transaction_date']
        verbose_name_plural = "ledger entries"
    
    def __str__(self):
        return f"{self.get_transaction_type_display()} - ${self.amount}"
