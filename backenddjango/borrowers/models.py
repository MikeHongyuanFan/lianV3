from django.db import models
from django.conf import settings


class Borrower(models.Model):
    """
    Model for borrowers
    """
    RESIDENCY_STATUS_CHOICES = [
        ('citizen', 'Citizen'),
        ('permanent_resident', 'Permanent Resident'),
        ('temporary_resident', 'Temporary Resident'),
        ('foreign_investor', 'Foreign Investor'),
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('de_facto', 'De Facto'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]
    
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('casual', 'Casual'),
        ('self_employed', 'Self Employed'),
        ('contractor', 'Contractor'),
        ('unemployed', 'Unemployed'),
        ('retired', 'Retired'),
    ]
    
    # Personal information
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    
    # Address information
    residential_address = models.TextField(null=True, blank=True)
    mailing_address = models.TextField(null=True, blank=True)
    
    # Identity information
    tax_id = models.CharField(max_length=50, null=True, blank=True, help_text="Tax File Number or equivalent")
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, null=True, blank=True)
    residency_status = models.CharField(max_length=20, choices=RESIDENCY_STATUS_CHOICES, null=True, blank=True)
    
    # Employment information
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, null=True, blank=True, default='full_time')
    employer_name = models.CharField(max_length=255, null=True, blank=True)
    employer_address = models.TextField(null=True, blank=True)
    job_title = models.CharField(max_length=100, null=True, blank=True)
    employment_duration = models.PositiveIntegerField(null=True, blank=True, help_text="Duration in months")
    
    # Financial information
    annual_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    other_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    monthly_expenses = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Bank account information
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    bank_account_name = models.CharField(max_length=100, null=True, blank=True)
    bank_account_number = models.CharField(max_length=30, null=True, blank=True)
    bank_bsb = models.CharField(max_length=10, null=True, blank=True)
    
    # Additional information
    referral_source = models.CharField(max_length=100, null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True)
    notes_text = models.TextField(null=True, blank=True)
    
    # Company information (for company borrowers)
    is_company = models.BooleanField(default=False)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    company_abn = models.CharField(max_length=20, null=True, blank=True)
    company_acn = models.CharField(max_length=20, null=True, blank=True)
    company_address = models.TextField(null=True, blank=True)
    
    # Relationships
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='borrower_profile')
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_borrowers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        if self.is_company:
            return f"{self.company_name}"
        return f"{self.first_name} {self.last_name}"


class Asset(models.Model):
    """
    Model for borrower assets
    """
    ASSET_TYPE_CHOICES = [
        ('property', 'Property'),
        ('vehicle', 'Vehicle'),
        ('savings', 'Savings'),
        ('investment', 'Investment'),
        ('superannuation', 'Superannuation'),
        ('other', 'Other'),
    ]
    
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE, related_name='assets')
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPE_CHOICES, default='other')
    description = models.TextField(null=True, blank=True, default='')
    value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    address = models.TextField(null=True, blank=True, help_text="For property assets")
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_asset_type_display()} - {self.value}"


class Liability(models.Model):
    """
    Model for borrower liabilities
    """
    LIABILITY_TYPE_CHOICES = [
        ('mortgage', 'Mortgage'),
        ('personal_loan', 'Personal Loan'),
        ('car_loan', 'Car Loan'),
        ('credit_card', 'Credit Card'),
        ('tax_debt', 'Tax Debt'),
        ('other', 'Other'),
    ]
    
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE, related_name='liabilities')
    liability_type = models.CharField(max_length=20, choices=LIABILITY_TYPE_CHOICES)
    description = models.TextField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    lender = models.CharField(max_length=100, null=True, blank=True)
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_liability_type_display()} - {self.amount}"


class Guarantor(models.Model):
    """
    Model for guarantors
    """
    GUARANTOR_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('company', 'Company'),
    ]
    
    RELATIONSHIP_CHOICES = [
        ('spouse', 'Spouse'),
        ('parent', 'Parent'),
        ('child', 'Child'),
        ('sibling', 'Sibling'),
        ('business_partner', 'Business Partner'),
        ('friend', 'Friend'),
        ('other', 'Other'),
    ]
    
    # Basic information
    guarantor_type = models.CharField(max_length=20, choices=GUARANTOR_TYPE_CHOICES, default='individual')
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    
    # Relationship to borrower
    relationship_to_borrower = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES, null=True, blank=True)
    
    # Company information (for company guarantors)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    company_abn = models.CharField(max_length=20, null=True, blank=True)
    company_acn = models.CharField(max_length=20, null=True, blank=True)
    
    # Relationships
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE, related_name='borrower_guarantors', null=True, blank=True)
    application = models.ForeignKey('applications.Application', on_delete=models.CASCADE, related_name='application_guarantors', null=True, blank=True)
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['guarantor_type', 'last_name', 'first_name', 'company_name']
    
    def __str__(self):
        if self.guarantor_type == 'company':
            return f"{self.company_name} (Company Guarantor)"
        return f"{self.first_name} {self.last_name} (Individual Guarantor)"
