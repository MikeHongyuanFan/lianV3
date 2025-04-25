from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Document, Note, Fee, Repayment
from .serializers import (
    DocumentSerializer,
    NoteSerializer,
    FeeSerializer,
    RepaymentSerializer
)
from .filters import DocumentFilter, NoteFilter, FeeFilter, RepaymentFilter
from users.permissions import IsAdmin, IsAdminOrBroker, IsAdminOrBD
from django.http import FileResponse
import os


class DocumentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing documents
    """
    queryset = Document.objects.all().order_by('-created_at')
    serializer_class = DocumentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = DocumentFilter
    search_fields = ['title', 'description', 'file_name']
    parser_classes = [MultiPartParser, FormParser]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdminOrBroker]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # Filter documents based on user role
        if user.role == 'admin':
            return queryset
        elif user.role == 'broker':
            return queryset.filter(application__broker__user=user)
        elif user.role == 'bd':
            return queryset.filter(application__bd=user)
        elif user.role == 'client':
            # Clients can only see documents associated with their borrower profile
            if hasattr(user, 'borrower_profile'):
                return queryset.filter(
                    application__borrowers=user.borrower_profile
                ) | queryset.filter(
                    borrower=user.borrower_profile
                )
        
        return queryset.none()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def update(self, request, *args, **kwargs):
        """
        Update a document
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Check if file is provided
        if 'file' in request.FILES:
            # Create a new version instead of updating the existing document
            file_obj = request.FILES['file']
            
            # Create new version
            new_version = Document.objects.create(
                title=request.data.get('title', instance.title),
                description=request.data.get('description', instance.description),
                document_type=request.data.get('document_type', instance.document_type),
                file=file_obj,
                file_name=file_obj.name,
                file_size=file_obj.size,
                file_type=file_obj.content_type,
                version=instance.version + 1,
                previous_version=instance,
                application=instance.application,
                borrower=instance.borrower,
                created_by=request.user
            )
            
            serializer = self.get_serializer(new_version)
            return Response(serializer.data)
        else:
            # Update metadata only
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            
            return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """
        Download a document
        """
        document = self.get_object()
        file_path = document.file.path
        
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{document.file_name}"'
            return response
        
        return Response(
            {'error': 'File not found'},
            status=status.HTTP_404_NOT_FOUND
        )


class NoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing notes
    """
    queryset = Note.objects.all().order_by('-created_at')
    serializer_class = NoteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = NoteFilter
    search_fields = ['title', 'content']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdminOrBroker]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # Filter notes based on user role
        if user.role == 'admin':
            return queryset
        elif user.role == 'broker':
            return queryset.filter(application__broker__user=user)
        elif user.role == 'bd':
            return queryset.filter(application__bd=user)
        elif user.role == 'client':
            # Clients can only see notes associated with their borrower profile
            if hasattr(user, 'borrower_profile'):
                return queryset.filter(
                    application__borrowers=user.borrower_profile
                ) | queryset.filter(
                    borrower=user.borrower_profile
                )
        
        return queryset.none()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class FeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing fees
    """
    queryset = Fee.objects.all().order_by('-created_at')
    serializer_class = FeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = FeeFilter
    search_fields = ['description']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdminOrBD]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # Filter fees based on user role
        if user.role == 'admin':
            return queryset
        elif user.role == 'broker':
            return queryset.filter(application__broker__user=user)
        elif user.role == 'bd':
            return queryset.filter(application__bd=user)
        elif user.role == 'client':
            # Clients can only see fees associated with their borrower profile
            if hasattr(user, 'borrower_profile'):
                return queryset.filter(application__borrowers=user.borrower_profile)
        
        return queryset.none()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class RepaymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing repayments
    """
    queryset = Repayment.objects.all().order_by('due_date')
    serializer_class = RepaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RepaymentFilter
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdminOrBD]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # Filter repayments based on user role
        if user.role == 'admin':
            return queryset
        elif user.role == 'broker':
            return queryset.filter(application__broker__user=user)
        elif user.role == 'bd':
            return queryset.filter(application__bd=user)
        elif user.role == 'client':
            # Clients can only see repayments associated with their borrower profile
            if hasattr(user, 'borrower_profile'):
                return queryset.filter(application__borrowers=user.borrower_profile)
        
        return queryset.none()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
class DocumentCreateVersionView(APIView):
    """
    View for creating a new version of a document
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, pk):
        """
        Create a new version of a document
        """
        try:
            original_document = Document.objects.get(pk=pk)
        except Document.DoesNotExist:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if file is provided
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        file_obj = request.FILES['file']
        
        # Create new version
        new_version = Document.objects.create(
            title=original_document.title,
            description=request.data.get('description', original_document.description),
            document_type=original_document.document_type,
            file=file_obj,
            file_name=file_obj.name,
            file_size=file_obj.size,
            file_type=file_obj.content_type,
            version=original_document.version + 1,
            previous_version=original_document,
            application=original_document.application,
            borrower=original_document.borrower,
            created_by=request.user
        )
        
        return Response({
            'message': 'New version created successfully',
            'document_id': new_version.id,
            'version': new_version.version,
            'document_url': new_version.file.url if new_version.file else None
        }, status=status.HTTP_201_CREATED)


class FeeMarkPaidView(APIView):
    """
    View for marking a fee as paid
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        """
        Mark a fee as paid
        """
        try:
            fee = Fee.objects.get(pk=pk)
        except Fee.DoesNotExist:
            return Response({'error': 'Fee not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Set paid date
        from django.utils import timezone
        fee.paid_date = request.data.get('paid_date', timezone.now().date())
        fee.save()
        
        return Response({
            'message': 'Fee marked as paid',
            'fee_id': fee.id,
            'paid_date': fee.paid_date
        })


class RepaymentMarkPaidView(APIView):
    """
    View for marking a repayment as paid
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        """
        Mark a repayment as paid
        """
        try:
            repayment = Repayment.objects.get(pk=pk)
        except Repayment.DoesNotExist:
            return Response({'error': 'Repayment not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Set paid date
        from django.utils import timezone
        repayment.paid_date = request.data.get('paid_date', timezone.now().date())
        repayment.save()
        
        return Response({
            'message': 'Repayment marked as paid',
            'repayment_id': repayment.id,
            'paid_date': repayment.paid_date
        })


class ApplicationLedgerView(APIView):
    """
    View for getting ledger entries for an application
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, application_id):
        """
        Get ledger entries for an application
        """
        from applications.models import Application
        
        try:
            application = Application.objects.get(pk=application_id)
        except Application.DoesNotExist:
            return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get ledger entries
        ledger_entries = Ledger.objects.filter(application=application)
        serializer = LedgerSerializer(ledger_entries, many=True)
        
        return Response(serializer.data)
