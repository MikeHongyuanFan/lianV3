from rest_framework import serializers
from .models import Application, Document, Fee, Repayment
from borrowers.models import Borrower, Guarantor
from .validators import validate_company_borrower
from django.db import transaction
from users.serializers import UserSerializer
from brokers.serializers import BrokerDetailSerializer as BrokerSerializer, BDMSerializer, BranchSerializer
from documents.serializers import DocumentSerializer, NoteSerializer, FeeSerializer, RepaymentSerializer, LedgerSerializer

class AddressSerializer(serializers.Serializer):
    street = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)
    postal_code = serializers.CharField(max_length=20)
    country = serializers.CharField(max_length=100)

class EmploymentInfoSerializer(serializers.Serializer):
    employer = serializers.CharField(max_length=255)
    position = serializers.CharField(max_length=100)
    income = serializers.DecimalField(max_digits=12, decimal_places=2)
    years_employed = serializers.DecimalField(max_digits=5, decimal_places=2)

class BorrowerSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    employment_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Borrower
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth',
            'address', 'employment_info', 'tax_id', 'marital_status',
            'residency_status', 'referral_source', 'tags'
        ]
    
    def get_address(self, obj):
        return {
            'street': obj.residential_address or '',
            'city': '',
            'state': '',
            'postal_code': '',
            'country': ''
        }
    
    def get_employment_info(self, obj):
        return {
            'employer': obj.employer_name or '',
            'position': obj.job_title or '',
            'income': obj.annual_income or 0,
            'years_employed': obj.employment_duration or 0
        }
    
    def create(self, validated_data):
        address_data = validated_data.pop('address', None)
        employment_data = validated_data.pop('employment_info', None)
        
        borrower = Borrower.objects.create(**validated_data)
        
        # Create address and employment info if provided
        if address_data:
            borrower.residential_address = address_data.get('street', '')
        
        if employment_data:
            borrower.employer_name = employment_data.get('employer', '')
            borrower.job_title = employment_data.get('position', '')
            borrower.annual_income = employment_data.get('income', 0)
            borrower.employment_duration = employment_data.get('years_employed', 0)
        
        borrower.save()
        
        return borrower

class GuarantorSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    relationship_to_borrower = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    
    class Meta:
        model = Guarantor
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth',
            'address', 'guarantor_type', 'relationship_to_borrower'
        ]
    
    def get_address(self, obj):
        return {
            'street': obj.address or '',
            'city': '',
            'state': '',
            'postal_code': '',
            'country': ''
        }
    
    def create(self, validated_data):
        address_data = validated_data.pop('address', None)
        # Remove relationship_to_borrower as it's not in the model
        if 'relationship_to_borrower' in validated_data:
            validated_data.pop('relationship_to_borrower')
        
        guarantor = Guarantor.objects.create(**validated_data)
        
        if address_data:
            guarantor.address = address_data.get('street', '')
            guarantor.save()
        
        return guarantor

class FinancialInfoSerializer(serializers.Serializer):
    annual_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    net_profit = serializers.DecimalField(max_digits=12, decimal_places=2)
    assets = serializers.DecimalField(max_digits=12, decimal_places=2)
    liabilities = serializers.DecimalField(max_digits=12, decimal_places=2)

class DirectorSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField(allow_blank=True, required=False)
    phone = serializers.CharField(max_length=20, allow_blank=True, required=False)

class CompanyBorrowerSerializer(serializers.ModelSerializer):
    registered_address = AddressSerializer()
    financial_info = FinancialInfoSerializer()
    directors = DirectorSerializer(many=True)
    
    class Meta:
        model = Borrower
        fields = [
            'id', 'company_name', 'company_abn', 'company_acn', 'business_type',
            'years_in_business', 'industry', 'registered_address',
            'directors', 'financial_info'
        ]
    
    def validate(self, data):
        # Use the custom validator for company borrower
        errors = validate_company_borrower(data)
        if errors:
            raise serializers.ValidationError(errors)
        return data
    
    def create(self, validated_data):
        registered_address = validated_data.pop('registered_address')
        financial_info = validated_data.pop('financial_info')
        directors = validated_data.pop('directors')
        
        company = Borrower.objects.create(is_company=True, **validated_data)
        company.registered_address = registered_address
        company.financial_info = financial_info
        company.directors = directors
        company.save()
        
        return company

# Removed PropertySerializer as it's causing issues with the Application model
# The Application model doesn't have a property field that matches this serializer

class ApplicationSignatureSerializer(serializers.Serializer):
    """
    Serializer for application signature
    """
    signature = serializers.CharField(required=True)
    name = serializers.CharField(required=True, max_length=255)
    signature_date = serializers.DateField(required=False)
    notes = serializers.CharField(allow_blank=True, required=False)

class QSInfoSerializer(serializers.Serializer):
    company_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    contact_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    notes = serializers.CharField(allow_blank=True, required=False)

class ApplicationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating applications
    
    This serializer is used by both the regular create endpoint (/api/applications/)
    and the create-with-cascade endpoint (/api/applications/create-with-cascade/).
    The difference is that the create-with-cascade endpoint is specifically intended
    for creating an application along with related entities (borrowers, guarantors,
    company borrowers) in a single request.
    """
    borrowers = BorrowerSerializer(many=True, required=False)
    guarantors = GuarantorSerializer(many=True, required=False)
    company_borrowers = CompanyBorrowerSerializer(many=True, required=False)
    
    class Meta:
        model = Application
        fields = [
            'id', 'reference_number', 'loan_amount', 'loan_term',
            'interest_rate', 'purpose', 'repayment_frequency',
            'application_type', 'product_id', 'estimated_settlement_date',
            'stage', 'broker', 'bd', 'branch', 'borrowers', 'guarantors',
            'company_borrowers', 'security_address', 'security_type', 'security_value',
            'valuer_company_name', 'valuer_contact_name', 'valuer_phone',
            'valuer_email', 'qs_company_name', 'qs_contact_name', 'qs_phone', 'qs_email'
        ]
    
    def create(self, validated_data):
        borrowers_data = validated_data.pop('borrowers', [])
        guarantors_data = validated_data.pop('guarantors', [])
        company_borrowers_data = validated_data.pop('company_borrowers', [])
        
        # Process new_borrowers data if present in the request
        new_borrowers = validated_data.pop('new_borrowers', [])
        
        # Use transaction to ensure all related entities are created or none
        with transaction.atomic():
            # Create the application
            application = Application.objects.create(**validated_data)
            
            # Create borrowers and link to application
            for borrower_data in borrowers_data:
                borrower_serializer = BorrowerSerializer(data=borrower_data)
                borrower_serializer.is_valid(raise_exception=True)
                borrower = borrower_serializer.save()
                application.borrowers.add(borrower)
            
            # Process new_borrowers if present
            for new_borrower_data in new_borrowers:
                # Create a new borrower
                borrower = Borrower.objects.create(
                    first_name=new_borrower_data.get('first_name', ''),
                    last_name=new_borrower_data.get('last_name', ''),
                    date_of_birth=new_borrower_data.get('date_of_birth'),
                    email=new_borrower_data.get('email', ''),
                    phone=new_borrower_data.get('phone', ''),
                    residential_address=new_borrower_data.get('residential_address', ''),
                    marital_status=new_borrower_data.get('marital_status', ''),
                    residency_status=new_borrower_data.get('residency_status', ''),
                    employment_type=new_borrower_data.get('employment_type', ''),
                    employer_name=new_borrower_data.get('employer_name', ''),
                    annual_income=new_borrower_data.get('annual_income', 0),
                    created_by=validated_data.get('created_by')
                )
                # Add the borrower to the application
                application.borrowers.add(borrower)
            
            # Create guarantors and link to application
            for guarantor_data in guarantors_data:
                guarantor_serializer = GuarantorSerializer(data=guarantor_data)
                guarantor_serializer.is_valid(raise_exception=True)
                guarantor = guarantor_serializer.save()
                application.guarantors.add(guarantor)
            
            # Process guarantor_data if present
            guarantor_data_list = validated_data.pop('guarantor_data', [])
            for guarantor_data in guarantor_data_list:
                # Create a new guarantor
                guarantor = Guarantor.objects.create(
                    guarantor_type=guarantor_data.get('guarantor_type', ''),
                    first_name=guarantor_data.get('first_name', ''),
                    last_name=guarantor_data.get('last_name', ''),
                    date_of_birth=guarantor_data.get('date_of_birth'),
                    email=guarantor_data.get('email', ''),
                    phone=guarantor_data.get('phone', ''),
                    address=guarantor_data.get('address', ''),
                    application=application,
                    created_by=validated_data.get('created_by')
                )
                # If borrower_id is provided, link the guarantor to the borrower
                borrower_id = guarantor_data.get('borrower_id')
                if borrower_id:
                    try:
                        borrower = Borrower.objects.get(id=borrower_id)
                        guarantor.borrower = borrower
                        guarantor.save()
                    except Borrower.DoesNotExist:
                        pass
            
            # Create company borrowers and link to application
            for company_data in company_borrowers_data:
                company_serializer = CompanyBorrowerSerializer(data=company_data)
                company_serializer.is_valid(raise_exception=True)
                company = company_serializer.save()
                application.borrowers.add(company)  # Add to borrowers since it's a Borrower model with is_company=True
            
            application.save()
            
            # Create notification for new application
            from users.models import Notification
            if application.bd_id:
                Notification.objects.create(
                    user_id=application.bd_id,  # Notify the BD
                    title=f"New Application: {application.reference_number}",
                    message=f"A new loan application has been submitted with reference {application.reference_number}",
                    notification_type="application_created",
                    related_object_id=application.id
                )
            
            return application

class ApplicationDetailSerializer(serializers.ModelSerializer):
    # Basic application fields are included by default
    
    # Related entities
    borrowers = BorrowerSerializer(many=True, read_only=True)
    guarantors = GuarantorSerializer(many=True, read_only=True)
    
    # Documents and notes
    documents = serializers.SerializerMethodField()
    notes = serializers.SerializerMethodField()
    
    # Financial tracking
    fees = serializers.SerializerMethodField()
    repayments = serializers.SerializerMethodField()
    ledger_entries = serializers.SerializerMethodField()
    
    # Related parties
    broker = BrokerSerializer(read_only=True)
    bd = BDMSerializer(read_only=True)
    branch = BranchSerializer(read_only=True)
    
    # Status information
    stage_display = serializers.CharField(source='get_stage_display', read_only=True)
    created_by_details = UserSerializer(source='created_by', read_only=True)
    
    class Meta:
        model = Application
        fields = [
            # Basic fields
            'id', 'reference_number', 'loan_amount', 'loan_term',
            'interest_rate', 'purpose', 'repayment_frequency',
            'application_type', 'product_id', 'estimated_settlement_date',
            'stage', 'stage_display', 'created_at', 'updated_at',
            
            # Related entities
            'borrowers', 'guarantors', 'broker', 'bd', 'branch',
            
            # Documents and notes
            'documents', 'notes',
            
            # Financial tracking
            'fees', 'repayments', 'ledger_entries',
            
            # Security property details
            'security_address', 'security_type', 'security_value',
            
            # Valuer information
            'valuer_company_name', 'valuer_contact_name', 'valuer_phone',
            'valuer_email', 'valuation_date', 'valuation_amount',
            
            # QS information
            'qs_company_name', 'qs_contact_name', 'qs_phone',
            'qs_email', 'qs_report_date',
            
            # Signature and PDF
            'signed_by', 'signature_date', 'uploaded_pdf_path',
            
            # Metadata
            'created_by_details'
        ]
    
    def get_documents(self, obj):
        documents = Document.objects.filter(application=obj)
        return DocumentSerializer(documents, many=True, context=self.context).data
    
    def get_notes(self, obj):
        from documents.models import Note
        notes = Note.objects.filter(application=obj).order_by('-created_at')
        return NoteSerializer(notes, many=True, context=self.context).data
    
    def get_fees(self, obj):
        fees = Fee.objects.filter(application=obj)
        return FeeSerializer(fees, many=True, context=self.context).data
    
    def get_repayments(self, obj):
        repayments = Repayment.objects.filter(application=obj).order_by('due_date')
        return RepaymentSerializer(repayments, many=True, context=self.context).data
    
    def get_ledger_entries(self, obj):
        from documents.models import Ledger
        ledger_entries = Ledger.objects.filter(application=obj).order_by('-transaction_date')
        return LedgerSerializer(ledger_entries, many=True, context=self.context).data

class ApplicationListSerializer(serializers.ModelSerializer):
    """Serializer for listing applications with minimal information"""
    stage_display = serializers.CharField(source='get_stage_display', read_only=True)
    broker_name = serializers.StringRelatedField(source='broker')
    borrower_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Application
        fields = [
            'id', 'reference_number', 'application_type', 'purpose',
            'loan_amount', 'stage', 'stage_display', 'created_at',
            'broker_name', 'borrower_count', 'estimated_settlement_date'
        ]
    
    def get_borrower_count(self, obj):
        return obj.borrowers.count()

class ApplicationStageUpdateSerializer(serializers.Serializer):
    stage = serializers.ChoiceField(choices=Application.STAGE_CHOICES)
    notes = serializers.CharField(required=False, allow_blank=True)

class ApplicationBorrowerSerializer(serializers.Serializer):
    borrower_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1
    )
