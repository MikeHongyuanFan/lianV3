from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Application
from .serializers import (
    ApplicationDetailSerializer, ApplicationCreateSerializer,
    ApplicationStageUpdateSerializer, ApplicationBorrowerSerializer
)
from .services import update_application_stage, process_signature_data
from users.permissions import IsAdmin, IsAdminOrBroker, IsAdminOrBD, IsOwnerOrAdmin
from datetime import datetime
from .filters import ApplicationFilter


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing loan applications
    """
    queryset = Application.objects.all().order_by('-created_at')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ApplicationFilter
    search_fields = ['reference_number', 'purpose']
    ordering_fields = ['created_at', 'loan_amount', 'estimated_settlement_date']
    
    def get_queryset(self):
        """
        Filter applications based on user role:
        - Admin: All applications
        - BD: Applications they're assigned to as BD
        - Broker: Applications they're assigned to as broker
        - Client: Applications they're associated with as borrowers
        """
        queryset = Application.objects.all().order_by('-created_at')
        
        # Admin users can see all applications
        if self.request.user.is_superuser or self.request.user.role == 'admin':
            return queryset
            
        # BD users can only see applications they're assigned to
        elif self.request.user.role == 'bd':
            from brokers.models import BDM
            bdm = BDM.objects.filter(user=self.request.user).first()
            if bdm:
                return queryset.filter(bd=bdm)
            return Application.objects.none()
            
        # Broker users can only see applications they're assigned to
        elif self.request.user.role == 'broker':
            from brokers.models import Broker
            broker = Broker.objects.filter(user=self.request.user).first()
            if broker:
                return queryset.filter(broker=broker)
            return Application.objects.none()
            
        # Client users can only see applications they're associated with
        elif self.request.user.role == 'client':
            from borrowers.models import Borrower
            borrower = Borrower.objects.filter(user=self.request.user).first()
            if borrower:
                return queryset.filter(borrowers=borrower)
            return Application.objects.none()
            
        # Default case - return no applications for unknown roles
        return Application.objects.none()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ApplicationCreateSerializer
        elif self.action == 'update_stage':
            return ApplicationStageUpdateSerializer
        elif self.action in ['add_borrowers', 'remove_borrowers']:
            return ApplicationBorrowerSerializer
        elif self.action == 'sign':
            from .serializers import ApplicationSignatureSerializer
            return ApplicationSignatureSerializer
        elif self.action == 'list':
            from .serializers import ApplicationListSerializer
            return ApplicationListSerializer
        return ApplicationDetailSerializer
    
    def get_permissions(self):
        # Admin users have full access to everything
        if self.request.user.is_authenticated and self.request.user.role == 'admin':
            permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdminOrBroker]
        elif self.action in ['update_stage']:
            permission_classes = [IsAuthenticated, IsAdminOrBD]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def update_stage(self, request, pk=None):
        """
        Update application stage
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            application = update_application_stage(
                application_id=pk,
                new_stage=serializer.validated_data['stage'],
                user=request.user
            )
            return Response(ApplicationDetailSerializer(application, context={'request': request}).data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['put'])
    def borrowers(self, request, pk=None):
        """
        Update borrowers for an application
        """
        application = self.get_object()
        
        # Validate borrower IDs
        if 'borrowers' not in request.data or not isinstance(request.data['borrowers'], list):
            return Response(
                {'error': 'borrowers field is required and must be a list of IDs'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        borrower_ids = request.data['borrowers']
        
        # Get borrowers from database
        from borrowers.models import Borrower
        borrowers = Borrower.objects.filter(id__in=borrower_ids)
        
        # Check if all borrowers exist
        if len(borrowers) != len(borrower_ids):
            missing_ids = set(borrower_ids) - set(borrower.id for borrower in borrowers)
            return Response(
                {'error': f'Borrowers with IDs {missing_ids} not found'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Clear existing borrowers and add new ones
        application.borrowers.clear()
        application.borrowers.add(*borrowers)
        
        # Create note
        from documents.models import Note
        Note.objects.create(
            application=application,
            content=f"Updated borrowers: {', '.join([str(b) for b in borrowers])}",
            created_by=request.user
        )
        
        return Response(ApplicationDetailSerializer(application, context={'request': request}).data)
    
    @action(detail=True, methods=['post'])
    def remove_borrowers(self, request, pk=None):
        """
        Remove borrowers from application
        """
        application = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        from borrowers.models import Borrower
        borrower_ids = serializer.validated_data['borrower_ids']
        borrowers = Borrower.objects.filter(id__in=borrower_ids)
        
        application.borrowers.remove(*borrowers)
        
        # Create note
        from documents.models import Note
        Note.objects.create(
            application=application,
            content=f"Removed borrowers: {', '.join([str(b) for b in borrowers])}",
            created_by=request.user
        )
        
        return Response(ApplicationDetailSerializer(application, context={'request': request}).data)
    
    @action(detail=True, methods=['get'])
    def notes(self, request, pk=None):
        """
        Get all notes for an application
        """
        application = self.get_object()
        from documents.models import Note
        notes = Note.objects.filter(application=application).order_by('-created_at')
        from documents.serializers import NoteSerializer
        serializer = NoteSerializer(notes, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_note(self, request, pk=None):
        """
        Add a note to an application
        """
        application = self.get_object()
        from documents.serializers import NoteSerializer
        serializer = NoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        note = serializer.save(
            application=application,
            created_by=request.user
        )
        
        return Response(NoteSerializer(note, context={'request': request}).data)
    
    @action(detail=True, methods=['get'])
    def documents(self, request, pk=None):
        """
        Get all documents for an application
        """
        application = self.get_object()
        from documents.models import Document
        documents = Document.objects.filter(application=application).order_by('-created_at')
        from documents.serializers import DocumentSerializer
        serializer = DocumentSerializer(documents, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def upload_document(self, request, pk=None):
        """
        Upload a document for an application
        """
        application = self.get_object()
        from documents.serializers import DocumentSerializer
        serializer = DocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        document = serializer.save(
            application=application,
            created_by=request.user
        )
        
        # Create note about document upload
        from documents.models import Note
        Note.objects.create(
            application=application,
            content=f"Document uploaded: {document.get_document_type_display()}",
            created_by=request.user
        )
        
        return Response(DocumentSerializer(document, context={'request': request}).data)
    
    @action(detail=True, methods=['get'])
    def fees(self, request, pk=None):
        """
        Get all fees for an application
        """
        application = self.get_object()
        from documents.models import Fee
        fees = Fee.objects.filter(application=application).order_by('-created_at')
        from documents.serializers import FeeSerializer
        serializer = FeeSerializer(fees, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_fee(self, request, pk=None):
        """
        Add a fee to an application
        """
        application = self.get_object()
        
        # Create a copy of the request data and add the application ID
        data = request.data.copy()
        data['application'] = application.id
        
        from documents.serializers import FeeSerializer
        serializer = FeeSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Add created_by to the serializer save
        fee = serializer.save(
            application=application,
            created_by=request.user
        )
        
        # Create note about fee addition
        from documents.models import Note
        Note.objects.create(
            application=application,
            content=f"Fee added: {fee.get_fee_type_display()} - ${fee.amount}",
            created_by=request.user
        )
        
        # Create ledger entry for the fee
        from documents.models import Ledger
        Ledger.objects.create(
            application=application,
            transaction_type='fee_added',
            amount=fee.amount,
            description=f"Fee added: {fee.get_fee_type_display()}",
            transaction_date=fee.created_at,
            created_by=request.user
        )
        
        return Response(FeeSerializer(fee, context={'request': request}).data)
    
    @action(detail=True, methods=['get'])
    def repayments(self, request, pk=None):
        """
        Get all repayments for an application
        """
        application = self.get_object()
        from documents.models import Repayment
        repayments = Repayment.objects.filter(application=application).order_by('due_date')
        from documents.serializers import RepaymentSerializer
        serializer = RepaymentSerializer(repayments, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_repayment(self, request, pk=None):
        """
        Add a repayment to an application
        """
        application = self.get_object()
        
        # Create a copy of the request data and add the application ID
        data = request.data.copy()
        data['application'] = application.id
        
        from documents.serializers import RepaymentSerializer
        serializer = RepaymentSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Add created_by to the serializer save
        repayment = serializer.save(
            application=application,
            created_by=request.user
        )
        
        # Create note about repayment addition
        from documents.models import Note
        Note.objects.create(
            application=application,
            content=f"Repayment scheduled: ${repayment.amount} due on {repayment.due_date}",
            created_by=request.user
        )
        
        # Create ledger entry for the repayment
        from documents.models import Ledger
        Ledger.objects.create(
            application=application,
            transaction_type='repayment_added',
            amount=repayment.amount,
            description=f"Repayment scheduled: ${repayment.amount} due on {repayment.due_date}",
            transaction_date=repayment.created_at,
            created_by=request.user
        )
        
        return Response(RepaymentSerializer(repayment, context={'request': request}).data)
    
    @action(detail=True, methods=['post'])
    def record_payment(self, request, pk=None):
        """
        Record a payment for a repayment
        """
        application = self.get_object()
        repayment_id = request.data.get('repayment_id')
        payment_amount = request.data.get('payment_amount')
        payment_date = request.data.get('payment_date')
        
        try:
            from documents.models import Repayment
            repayment = Repayment.objects.get(id=repayment_id, application=application)
        except Repayment.DoesNotExist:
            return Response({'error': 'Repayment not found'}, status=status.HTTP_404_NOT_FOUND)
        
        repayment.payment_amount = payment_amount
        repayment.paid_date = payment_date
        repayment.status = 'paid'  # Add this field to the model or handle it in the serializer
        repayment.save()
        
        # Create note about payment
        from documents.models import Note
        Note.objects.create(
            application=application,
            content=f"Payment recorded: ${payment_amount} for repayment due on {repayment.due_date}",
            created_by=request.user
        )
        
        # Create ledger entry for the payment
        from documents.models import Ledger
        Ledger.objects.create(
            application=application,
            transaction_type='payment_received',
            amount=payment_amount,
            description=f"Payment received for repayment due on {repayment.due_date}",
            transaction_date=payment_date,
            related_repayment=repayment,
            created_by=request.user
        )
        
        from documents.serializers import RepaymentSerializer
        return Response(RepaymentSerializer(repayment, context={'request': request}).data)
    
    @action(detail=True, methods=['get'])
    def guarantors(self, request, pk=None):
        """
        Get all guarantors for an application
        """
        application = self.get_object()
        from borrowers.serializers import GuarantorSerializer
        guarantors = application.guarantors.all()
        serializer = GuarantorSerializer(guarantors, many=True, context={'request': request})
        return Response(serializer.data)
        
    @action(detail=True, methods=['get'])
    def ledger(self, request, pk=None):
        """
        Get ledger entries for an application
        """
        application = self.get_object()
        from documents.models import Ledger
        ledger_entries = Ledger.objects.filter(application=application).order_by('-transaction_date')
        from documents.serializers import LedgerSerializer
        serializer = LedgerSerializer(ledger_entries, many=True, context={'request': request})
        return Response(serializer.data)
        serializer = LedgerSerializer(ledger_entries, many=True, context={'request': request})
        return Response(serializer.data)
        
    @action(detail=False, methods=['post'])
    def validate_schema(self, request):
        """
        Validate application schema
        """
        # Check for required fields
        required_fields = ['application_type', 'purpose', 'loan_amount', 'loan_term', 'repayment_frequency']
        for field in required_fields:
            if field not in request.data:
                return Response({"valid": False, "error": f"Missing required field: {field}"}, 
                               status=status.HTTP_400_BAD_REQUEST)
        
        # Validate application_type
        valid_types = ['residential', 'commercial', 'personal', 'asset_finance']
        if request.data.get('application_type') not in valid_types:
            return Response({"valid": False, "error": "Invalid application_type"}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Validate repayment_frequency
        valid_frequencies = ['weekly', 'fortnightly', 'monthly']
        if request.data.get('repayment_frequency') not in valid_frequencies:
            return Response({"valid": False, "error": "Invalid repayment_frequency"}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"valid": True})
    
    @action(detail=True, methods=['post'])
    def sign(self, request, pk=None):
        """
        Sign an application
        
        This endpoint processes a signature for an application, updating the signature data,
        signed by name, and signature date. It also creates a note about the signature.
        """
        application = self.get_object()
        from .serializers import ApplicationSignatureSerializer
        
        serializer = ApplicationSignatureSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get signature data
        signature_data = serializer.validated_data['signature']
        signed_by = serializer.validated_data['name']
        signature_date = serializer.validated_data.get('signature_date', datetime.now().date())
        
        # Process signature
        updated_application = process_signature_data(
            application_id=application.id,
            signature_data=signature_data,
            signed_by=signed_by,
            user=request.user
        )
        
        if not updated_application:
            return Response(
                {'error': 'Failed to process signature'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create note about signature
        from documents.models import Note
        Note.objects.create(
            application=application,
            content=f"Application signed by {signed_by} on {signature_date}",
            created_by=request.user
        )
        
        # Return updated application
        return Response(ApplicationDetailSerializer(updated_application, context={'request': request}).data)
