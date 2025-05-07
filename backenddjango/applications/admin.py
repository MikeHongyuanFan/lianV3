from django.contrib import admin
from .models import (
    Application, Document, Fee, Repayment, FundingCalculationHistory,
    SecurityProperty, LoanRequirement
)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'stage', 'application_type', 'loan_amount', 'created_at', 'stage_last_updated')
    list_filter = ('stage', 'application_type', 'created_at', 'stage_last_updated')
    search_fields = ('reference_number', 'purpose', 'additional_comments')
    raw_id_fields = ('broker', 'branch', 'bd', 'created_by')
    filter_horizontal = ('borrowers', 'guarantors')
    readonly_fields = ('reference_number', 'created_at', 'updated_at', 'stage_last_updated')
    fieldsets = (
        ('Basic Information', {
            'fields': ('reference_number', 'stage', 'application_type', 'purpose')
        }),
        ('Loan Details', {
            'fields': ('loan_amount', 'loan_term', 'interest_rate', 'repayment_frequency', 'product_id', 'estimated_settlement_date')
        }),
        ('Loan Purpose', {
            'fields': ('loan_purpose', 'additional_comments', 'prior_application', 'prior_application_details')
        }),
        ('Exit Strategy', {
            'fields': ('exit_strategy', 'exit_strategy_details')
        }),
        ('Relationships', {
            'fields': ('broker', 'branch', 'bd', 'borrowers', 'guarantors')
        }),
        ('Signature and Documents', {
            'fields': ('signed_by', 'signature_date', 'uploaded_pdf_path')
        }),
        ('Valuation Information', {
            'fields': ('valuer_company_name', 'valuer_contact_name', 'valuer_phone', 'valuer_email', 'valuation_date', 'valuation_amount')
        }),
        ('Quantity Surveyor Information', {
            'fields': ('qs_company_name', 'qs_contact_name', 'qs_phone', 'qs_email', 'qs_report_date')
        }),
        ('Security Property (Legacy)', {
            'fields': ('security_address', 'security_type', 'security_value')
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at', 'updated_at', 'stage_last_updated')
        }),
    )

@admin.register(SecurityProperty)
class SecurityPropertyAdmin(admin.ModelAdmin):
    list_display = ('get_address', 'property_type', 'estimated_value', 'purchase_price')
    list_filter = ('property_type', 'occupancy', 'created_at')
    search_fields = ('address_street_name', 'address_suburb', 'address_state', 'address_postcode')
    raw_id_fields = ('application', 'created_by')
    
    def get_address(self, obj):
        address_parts = [
            obj.address_unit,
            obj.address_street_no,
            obj.address_street_name,
            obj.address_suburb,
            obj.address_state,
            obj.address_postcode
        ]
        return ' '.join(filter(None, address_parts))
    get_address.short_description = 'Address'

@admin.register(LoanRequirement)
class LoanRequirementAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'application', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('description', 'application__reference_number')
    raw_id_fields = ('application', 'created_by')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('document_type', 'description', 'application', 'uploaded_at', 'uploaded_by')
    list_filter = ('document_type', 'uploaded_at')
    search_fields = ('description', 'application__reference_number')
    raw_id_fields = ('application', 'uploaded_by')

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('fee_type', 'amount', 'due_date', 'status', 'application')
    list_filter = ('fee_type', 'status', 'due_date', 'created_at')
    search_fields = ('notes', 'application__reference_number')
    raw_id_fields = ('application',)

@admin.register(Repayment)
class RepaymentAdmin(admin.ModelAdmin):
    list_display = ('due_date', 'amount', 'status', 'paid_date', 'payment_amount', 'application')
    list_filter = ('status', 'due_date', 'paid_date')
    search_fields = ('notes', 'application__reference_number')
    raw_id_fields = ('application',)

@admin.register(FundingCalculationHistory)
class FundingCalculationHistoryAdmin(admin.ModelAdmin):
    list_display = ('application', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('application__reference_number',)
    raw_id_fields = ('application', 'created_by')
