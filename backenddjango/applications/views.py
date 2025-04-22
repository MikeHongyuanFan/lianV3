from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Application, Document, Fee, Repayment
from .serializers import (
    ApplicationDetailSerializer, ApplicationCreateSerializer,
    ApplicationStageUpdateSerializer, ApplicationBorrowerSerializer
)
from .services import update_application_stage, process_signature_data
from users.permissions import IsAdmin, IsAdminOrBroker, IsAdminOrBD, IsOwnerOrAdmin
from documents.models import Note, Ledger
from documents.serializers import NoteSerializer, DocumentSerializer, FeeSerializer, RepaymentSerializer, LedgerSerializer
from django.utils import timezone
from datetime import datetime


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing loan applications
    """
    queryset = Application.objects.all().order_by('-created_at')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['stage', 'application_type', 'broker', 'bd', 'branch']
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
        return ApplicationDetailSerializer
    
    def get_permissions(self):
        # Admin users have full access to everything
        if self.request.user.is_authenticated and self.request.user.role == 'admin':
            permission_classes = [IsAuthenticated]
        # For create action, allow any authenticated user
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        # For update and delete, require admin or broker
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdminOrBroker]
        # For stage updates, require admin or BD
        elif self.action in ['update_stage']:
            permission_classes = [IsAuthenticated, IsAdminOrBD]
        # For all other actions, just require authentication
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
    
    @action(detail=True, methods=['post'])
    def add_borrowers(self, request, pk=None):
        """
        Add borrowers to application
        """
        application = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        from borrowers.models import Borrower
        borrower_ids = serializer.validated_data['borrower_ids']
        borrowers = Borrower.objects.filter(id__in=borrower_ids)
        
        if len(borrowers) != len(borrower_ids):
            missing_ids = set(borrower_ids) - set(borrower.id for borrower in borrowers)
            return Response(
                {'error': f'Borrowers with IDs {missing_ids} not found'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        application.borrowers.add(*borrowers)
        
        # Create note
        Note.objects.create(
            application=application,
            content=f"Added borrowers: {', '.join([str(b) for b in borrowers])}",
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
        notes = Note.objects.filter(application=application).order_by('-created_at')
        serializer = NoteSerializer(notes, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_note(self, request, pk=None):
        """
        Add a note to an application
        """
        application = self.get_object()
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
        documents = Document.objects.filter(application=application).order_by('-uploaded_at')
        serializer = DocumentSerializer(documents, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def upload_document(self, request, pk=None):
        """
        Upload a document for an application
        """
        application = self.get_object()
        serializer = DocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        document = serializer.save(
            application=application,
            uploaded_by=request.user
        )
        
        # Create note about document upload
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
        fees = Fee.objects.filter(application=application).order_by('-created_at')
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
        
        serializer = FeeSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Add created_by to the serializer save
        fee = serializer.save(
            application=application,
            created_by=request.user
        )
        
        # Create note about fee addition
        Note.objects.create(
            application=application,
            content=f"Fee added: {fee.get_fee_type_display()} - ${fee.amount}",
            created_by=request.user
        )
        
        # Create ledger entry for the fee
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
        repayments = Repayment.objects.filter(application=application).order_by('due_date')
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
        
        serializer = RepaymentSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Add created_by to the serializer save
        repayment = serializer.save(
            application=application,
            created_by=request.user
        )
        
        # Create note about repayment addition
        Note.objects.create(
            application=application,
            content=f"Repayment scheduled: ${repayment.amount} due on {repayment.due_date}",
            created_by=request.user
        )
        
        # Create ledger entry for the repayment
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
            repayment = Repayment.objects.get(id=repayment_id, application=application)
        except Repayment.DoesNotExist:
            return Response({'error': 'Repayment not found'}, status=status.HTTP_404_NOT_FOUND)
        
        repayment.payment_amount = payment_amount
        repayment.paid_date = payment_date
        repayment.status = 'paid'  # Add this field to the model or handle it in the serializer
        repayment.save()
        
        # Create note about payment
        Note.objects.create(
            application=application,
            content=f"Payment recorded: ${payment_amount} for repayment due on {repayment.due_date}",
            created_by=request.user
        )
        
        # Create ledger entry for the payment
        Ledger.objects.create(
            application=application,
            transaction_type='payment_received',
            amount=payment_amount,
            description=f"Payment received for repayment due on {repayment.due_date}",
            transaction_date=timezone.make_aware(datetime.combine(payment_date, datetime.min.time())) if payment_date else timezone.now(),
            related_repayment=repayment,
            created_by=request.user
        )
        
        return Response(RepaymentSerializer(repayment, context={'request': request}).data)
    
    @action(detail=True, methods=['get'])
    def ledger(self, request, pk=None):
        """
        Get ledger entries for an application
        """
        application = self.get_object()
        ledger_entries = Ledger.objects.filter(application=application).order_by('-transaction_date')
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
    def signature(self, request, pk=None):
        """
        Process signature for an application
        """
        try:
            application = self.get_object()
            
            # Get signature data from request
            signature_data = request.data.get('signature_data')
            signed_by = request.data.get('signed_by')
            signature_date = request.data.get('signature_date')
            
            if not signature_data or not signed_by or not signature_date:
                return Response({"error": "Missing required signature data"}, 
                               status=status.HTTP_400_BAD_REQUEST)
            
            # Process signature (in a real app, this would save the signature image)
            application.signed_by = signed_by
            application.signature_date = signature_date
            
            # Simulate PDF generation
            application.uploaded_pdf_path = f"signatures/application_{application.id}_signed.pdf"
            application.save()
            
            # Create note about signature
            Note.objects.create(
                application=application,
                content=f"Application signed by {signed_by} on {signature_date}",
                created_by=request.user
            )
            
            return Response({"status": "signature processed successfully"})
            
        except Application.DoesNotExist:
            return Response({"error": "Application not found"}, status=status.HTTP_404_NOT_FOUND)
from rest_framework.views import APIView

class NewApplicationTemplateView(APIView):
    """
    API endpoint for getting a new application template
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get a new application template
        """
        # Return a template for a new application
        template = {
            "application_type": "personal",
            "loan_amount": 0,
            "term_months": 12,
            "interest_rate": 5.0,
            "purpose": "",
            "stage": "draft",
            "borrowers": [],
            "guarantors": [],
            "documents": [],
            "fees": [],
            "repayments": []
        }
        return Response(template)


