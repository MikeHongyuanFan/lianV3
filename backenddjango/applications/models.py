from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string
from brokers.models import Broker, Branch, BDM


def generate_reference_number():
    """Generate a unique reference number for applications"""
    prefix = "APP"
    random_suffix = get_random_string(length=8, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    return f"{prefix}-{random_suffix}"


class Application(models.Model):
    """
    Model for loan applications
    """
    STAGE_CHOICES = [
        ('inquiry', 'Inquiry'),
        ('pre_approval', 'Pre-Approval'),
        ('valuation', 'Valuation'),
        ('formal_approval', 'Formal Approval'),
        ('settlement', 'Settlement'),
        ('funded', 'Funded'),
        ('declined', 'Declined'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    APPLICATION_TYPE_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('construction', 'Construction'),
        ('refinance', 'Refinance'),
        ('investment', 'Investment'),
        ('smsf', 'SMSF'),
    ]
    
    REPAYMENT_FREQUENCY_CHOICES = [
        ('weekly', 'Weekly'),
        ('fortnightly', 'Fortnightly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually'),
    ]
    
    # Basic application details
    reference_number = models.CharField(max_length=20, unique=True, default=generate_reference_number)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='inquiry')
    application_type = models.CharField(max_length=20, choices=APPLICATION_TYPE_CHOICES, null=True, blank=True)
    purpose = models.TextField(null=True, blank=True, default='')
    
    # Loan details
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    loan_term = models.PositiveIntegerField(help_text="Loan term in months", null=True, blank=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    repayment_frequency = models.CharField(max_length=20, choices=REPAYMENT_FREQUENCY_CHOICES, default='monthly')
    product_id = models.CharField(max_length=50, null=True, blank=True)
    estimated_settlement_date = models.DateField(null=True, blank=True)
    
    # Relationships
    broker = models.ForeignKey(Broker, on_delete=models.SET_NULL, null=True, related_name='broker_applications')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, related_name='branch_applications')
    bd = models.ForeignKey(BDM, on_delete=models.SET_NULL, null=True, related_name='bdm_applications')
    borrowers = models.ManyToManyField('borrowers.Borrower', related_name='borrower_applications')
    guarantors = models.ManyToManyField('borrowers.Guarantor', related_name='guaranteed_applications', blank=True)
    
    # Signature and document info
    signed_by = models.CharField(max_length=255, null=True, blank=True)
    signature_date = models.DateField(null=True, blank=True)
    uploaded_pdf_path = models.FileField(upload_to='applications/signed_forms/', null=True, blank=True)
    
    # Valuer information (flat fields)
    valuer_company_name = models.CharField(max_length=255, null=True, blank=True)
    valuer_contact_name = models.CharField(max_length=255, null=True, blank=True)
    valuer_phone = models.CharField(max_length=20, null=True, blank=True)
    valuer_email = models.EmailField(null=True, blank=True)
    valuation_date = models.DateField(null=True, blank=True)
    valuation_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Quantity Surveyor information (flat fields)
    qs_company_name = models.CharField(max_length=255, null=True, blank=True)
    qs_contact_name = models.CharField(max_length=255, null=True, blank=True)
    qs_phone = models.CharField(max_length=20, null=True, blank=True)
    qs_email = models.EmailField(null=True, blank=True)
    qs_report_date = models.DateField(null=True, blank=True)
    
    # Security property details
    security_address = models.TextField(null=True, blank=True)
    security_type = models.CharField(max_length=50, null=True, blank=True)
    security_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_applications')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.reference_number} - {self.get_stage_display()}"
    
    def save(self, *args, **kwargs):
        # Generate reference number if not provided
        if not self.reference_number:
            self.reference_number = generate_reference_number()
        super().save(*args, **kwargs)

class Document(models.Model):
    """
    Model for application documents
    """
    DOCUMENT_TYPE_CHOICES = [
        ('id', 'Identification'),
        ('income', 'Income Verification'),
        ('bank_statement', 'Bank Statement'),
        ('property', 'Property Document'),
        ('application', 'Application Form'),
        ('contract', 'Contract'),
        ('valuation', 'Valuation Report'),
        ('other', 'Other'),
    ]
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='app_documents', null=True, blank=True)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES, default='other')
    file = models.FileField(upload_to='documents/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='uploaded_documents')
    
    def __str__(self):
        if self.application:
            return f"{self.get_document_type_display()} - {self.application.reference_number}"
        return f"{self.get_document_type_display()} - No Application"


class Fee(models.Model):
    """
    Model for application fees
    """
    FEE_TYPE_CHOICES = [
        ('application', 'Application Fee'),
        ('valuation', 'Valuation Fee'),
        ('legal', 'Legal Fee'),
        ('broker', 'Broker Commission'),
        ('settlement', 'Settlement Fee'),
        ('other', 'Other Fee'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('waived', 'Waived'),
        ('refunded', 'Refunded'),
    ]
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='app_fees', null=True, blank=True)
    fee_type = models.CharField(max_length=20, choices=FEE_TYPE_CHOICES, default='other')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    invoice = models.FileField(upload_to='invoices/', null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        fee_type = self.get_fee_type_display() if self.fee_type else "Fee"
        amount = self.amount if self.amount else 0
        return f"{fee_type} - {amount}"


class Repayment(models.Model):
    """
    Model for loan repayments
    """
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('paid', 'Paid'),
        ('missed', 'Missed'),
        ('partial', 'Partial Payment'),
    ]
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='app_repayments', null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')
    paid_date = models.DateField(null=True, blank=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    invoice = models.FileField(upload_to='repayment_invoices/', null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        due_date = self.due_date if self.due_date else "No date"
        amount = self.amount if self.amount else 0
        return f"Repayment {due_date} - {amount}"
