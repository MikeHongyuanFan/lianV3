from rest_framework import viewsets, status, filters, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import Borrower, Guarantor
from .serializers import (
    BorrowerListSerializer,
    BorrowerDetailSerializer,
    GuarantorSerializer,
    GuarantorDetailSerializer
)
from .filters import BorrowerFilter, GuarantorFilter
from users.permissions import IsAdmin, IsAdminOrBroker
from .filters import BorrowerFilter, GuarantorFilter
from users.permissions import IsAdmin, IsAdminOrBroker


class BorrowerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing borrowers
    """
    queryset = Borrower.objects.all().order_by('-created_at')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BorrowerFilter
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    ordering_fields = ['created_at', 'last_name', 'first_name']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BorrowerListSerializer
        return BorrowerDetailSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdminOrBroker]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # Filter borrowers based on user role
        if user.role == 'admin':
            return queryset
        elif user.role == 'broker':
            return queryset.filter(created_by=user)
        elif user.role == 'client':
            # Clients can only see their own borrower profile
            if hasattr(user, 'borrower_profile'):
                return queryset.filter(id=user.borrower_profile.id)
        
        return queryset.none()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def applications(self, request, pk=None):
        """
        Get all applications for a borrower
        """
        borrower = self.get_object()
        from applications.serializers import ApplicationListSerializer
        applications = borrower.applications.all().order_by('-created_at')
        serializer = ApplicationListSerializer(applications, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def guarantors(self, request, pk=None):
        """
        Get all guarantors for a borrower
        """
        borrower = self.get_object()
        guarantors = borrower.guarantors.all()
        serializer = GuarantorSerializer(guarantors, many=True)
        return Response(serializer.data)


class GuarantorViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing guarantors
    """
    queryset = Guarantor.objects.all().order_by('-created_at')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = GuarantorFilter
    search_fields = ['first_name', 'last_name', 'email', 'company_name']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            from .serializers import GuarantorDetailSerializer
            return GuarantorDetailSerializer
        return GuarantorSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdminOrBroker]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['get'])
    def guaranteed_applications(self, request, pk=None):
        """
        Get all applications guaranteed by this guarantor
        """
        guarantor = self.get_object()
        from applications.serializers import ApplicationListSerializer
        applications = guarantor.application_guarantors.all()
        serializer = ApplicationListSerializer(applications, many=True)
        return Response(serializer.data)
    
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # Filter guarantors based on user role
        if user.role == 'admin':
            return queryset
        elif user.role == 'broker':
            return queryset.filter(created_by=user)
        elif user.role == 'client':
            # Clients can only see guarantors associated with their borrower profile
            if hasattr(user, 'borrower_profile'):
                return queryset.filter(borrower=user.borrower_profile)
        
        return queryset.none()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
class CompanyBorrowerListView(generics.ListAPIView):
    """
    View for listing company borrowers
    """
    serializer_class = BorrowerListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Borrower.objects.filter(is_company=True)


class BorrowerFinancialSummaryView(APIView):
    """
    View for getting a borrower's financial summary
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        """
        Get a financial summary for a borrower
        """
        from borrowers.services import get_borrower_financial_summary
        summary = get_borrower_financial_summary(pk)
        
        if summary:
            return Response(summary)
        
        return Response({'error': 'Borrower not found'}, status=status.HTTP_404_NOT_FOUND)
