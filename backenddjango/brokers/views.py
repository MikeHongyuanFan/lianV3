from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Broker, Branch, BDM
from .serializers import (
    BrokerListSerializer,
    BrokerDetailSerializer,
    BranchSerializer,
    BDMSerializer
)
from .filters import BrokerFilter, BranchFilter, BDMFilter
from users.permissions import IsAdmin, IsAdminOrBD
from django.db.models import Count, Sum
from applications.serializers import ApplicationListSerializer
from rest_framework.views import APIView


class BranchViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing branches
    """
    queryset = Branch.objects.all().order_by('name')
    serializer_class = BranchSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = BranchFilter
    search_fields = ['name', 'address']
    # Exclude delete method to match test expectations
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def brokers(self, request, pk=None):
        """
        Get all brokers for a branch
        """
        branch = self.get_object()
        brokers = branch.branch_brokers.all()  # Use the correct related_name
        serializer = BrokerListSerializer(brokers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def bdms(self, request, pk=None):
        """
        Get all BDMs for a branch
        """
        branch = self.get_object()
        bdms = branch.branch_bdms.all()  # Use the correct related_name
        serializer = BDMSerializer(bdms, many=True)
        return Response(serializer.data)


class BrokerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing brokers
    """
    queryset = Broker.objects.all().order_by('name')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BrokerFilter
    search_fields = ['name', 'company', 'email', 'phone']
    ordering_fields = ['name', 'created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BrokerListSerializer
        return BrokerDetailSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # Filter brokers based on user role
        if user.role == 'admin':
            return queryset
        elif user.role == 'bd':
            return queryset.filter(bdms=user)
        elif user.role == 'broker':
            # Brokers can only see their own profile
            if hasattr(user, 'broker_profile'):
                return queryset.filter(id=user.broker_profile.id)
        
        return queryset.none()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def applications(self, request, pk=None):
        """
        Get all applications for a broker
        """
        broker = self.get_object()
        from applications.serializers import ApplicationListSerializer
        applications = broker.broker_applications.all().order_by('-created_at')  # Use the correct related_name
        serializer = ApplicationListSerializer(applications, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """
        Get statistics for a broker
        """
        broker = self.get_object()
        
        # Get applications for this broker
        applications = broker.broker_applications.all()  # Use the correct related_name
        
        # Calculate statistics
        if isinstance(applications, list):
            total_applications = len(applications)
            total_loan_amount = 0
            stage_stats = {}
            type_stats = {}
        else:
            # It's a queryset
            total_applications = applications.count()
            total_loan_amount = applications.aggregate(Sum('loan_amount'))['loan_amount__sum'] or 0
            
            # Applications by stage
            applications_by_stage = applications.values('stage').annotate(count=Count('id'))
            stage_stats = {item['stage']: item['count'] for item in applications_by_stage}
            
            # Applications by type
            applications_by_type = applications.values('application_type').annotate(count=Count('id'))
            type_stats = {item['application_type']: item['count'] for item in applications_by_type}
        
        return Response({
            'total_applications': total_applications,
            'total_loan_amount': total_loan_amount,
            'applications_by_stage': stage_stats,
            'applications_by_type': type_stats
        })


class BDMViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing BDMs
    """
    queryset = BDM.objects.all().order_by('name')
    serializer_class = BDMSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = BDMFilter
    search_fields = ['name', 'email', 'phone']
    # Ensure create method is supported
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # Filter BDMs based on user role
        if user.role == 'admin':
            return queryset
        elif user.role == 'bd':
            # BDs can only see their own profile
            if hasattr(user, 'bdm_profile'):
                return queryset.filter(id=user.bdm_profile.id)
        
        return queryset.none()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def applications(self, request, pk=None):
        """
        Get all applications for a BDM
        """
        bdm = self.get_object()
        from applications.serializers import ApplicationListSerializer
        applications = bdm.bdm_applications.all().order_by('-created_at')  # Use the correct related_name
        serializer = ApplicationListSerializer(applications, many=True)
        return Response(serializer.data)
