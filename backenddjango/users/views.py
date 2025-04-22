from rest_framework import viewsets, status, filters, views
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .models import User, Notification, NotificationPreference
from .serializers import (
    UserSerializer, UserCreateSerializer, NotificationSerializer, 
    NotificationListSerializer, NotificationPreferenceSerializer
)
from .permissions import IsAdmin
from .services import get_or_create_notification_preferences
from django.contrib.auth import authenticate
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, ListAPIView
import logging

# Set up logger
logger = logging.getLogger(__name__)

class LoginView(APIView):
    """
    API endpoint for user login
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        logger.info(f"Login attempt for email: {email}")
        
        # Try to authenticate with email
        user = authenticate(username=email, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,
                'email': user.email,
                'role': user.role,
                'name': f"{user.first_name} {user.last_name}".strip()
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterView(APIView):
    """
    API endpoint for user registration
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            # Log the incoming request data
            logger.info(f"Registration attempt with data: {request.data}")
            
            # Create user with email only, no username needed
            data = request.data.copy()
                
            serializer = UserCreateSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user_id': user.id,
                    'email': user.email,
                    'role': user.role,
                    'name': f"{user.first_name} {user.last_name}".strip()
                }, status=status.HTTP_201_CREATED)
            
            # Log validation errors
            logger.error(f"Registration validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Log any exceptions
            logger.exception(f"Exception during registration: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfileView(RetrieveAPIView):
    """
    API endpoint for retrieving user profile
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user


class UserProfileUpdateView(UpdateAPIView):
    """
    API endpoint for updating user profile
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user


class NotificationListView(ListAPIView):
    """
    API endpoint for listing user notifications
    """
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationListSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_read', 'notification_type']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class NotificationMarkReadView(APIView):
    """
    API endpoint for marking notifications as read
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        notification_id = request.data.get('notification_id')
        
        if notification_id:
            try:
                notification = Notification.objects.get(id=notification_id, user=request.user)
                notification.is_read = True
                notification.save()
                return Response({'status': 'notification marked as read'})
            except Notification.DoesNotExist:
                return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Mark all as read
            Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
            return Response({'status': 'all notifications marked as read'})


class NotificationCountView(APIView):
    """
    API endpoint for getting unread notification count
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return Response({'unread_count': count})


class NotificationPreferenceView(APIView):
    """
    API endpoint for managing notification preferences
    """
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationPreferenceSerializer
    
    def get(self, request):
        """
        Get notification preferences for the current user
        """
        preferences = get_or_create_notification_preferences(request.user)
        serializer = NotificationPreferenceSerializer(preferences)
        return Response(serializer.data)
    
    def put(self, request):
        """
        Update notification preferences for the current user
        """
        preferences = get_or_create_notification_preferences(request.user)
        serializer = NotificationPreferenceSerializer(preferences, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing users
    """
    queryset = User.objects.all().order_by('-date_joined')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Get current user information
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for managing notifications
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_read', 'notification_type']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return NotificationListSerializer
        return NotificationSerializer
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """
        Mark a notification as read
        """
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        
        # Send WebSocket update for unread count
        try:
            from channels.layers import get_channel_layer
            from asgiref.sync import async_to_sync
            
            channel_layer = get_channel_layer()
            unread_count = self.get_queryset().filter(is_read=False).count()
            
            async_to_sync(channel_layer.group_send)(
                f"user_{request.user.id}_notifications",
                {
                    'type': 'notification_count',
                    'count': unread_count
                }
            )
        except Exception as e:
            # Log the error but don't fail the operation
            print(f"Error sending WebSocket notification: {str(e)}")
            
        return Response({'status': 'notification marked as read'})
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """
        Mark all notifications as read
        """
        self.get_queryset().update(is_read=True)
        
        # Send WebSocket update for unread count
        try:
            from channels.layers import get_channel_layer
            from asgiref.sync import async_to_sync
            
            channel_layer = get_channel_layer()
            
            async_to_sync(channel_layer.group_send)(
                f"user_{request.user.id}_notifications",
                {
                    'type': 'notification_count',
                    'count': 0
                }
            )
        except Exception as e:
            # Log the error but don't fail the operation
            print(f"Error sending WebSocket notification: {str(e)}")
            
        return Response({'status': 'all notifications marked as read'})
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """
        Get count of unread notifications
        """
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'unread_count': count})
