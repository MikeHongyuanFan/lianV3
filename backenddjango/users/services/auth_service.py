"""
Authentication services.
"""
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from ..serializers import UserSerializer


class AuthService:
    """Service for authentication operations."""
    
    @staticmethod
    def login(email, password):
        """
        Authenticate a user with email and password
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Dictionary with authentication result
        """
        user = authenticate(username=email, password=password)
        
        if user is None:
            return {
                'success': False,
                'error': 'Invalid credentials'
            }
        
        if not user.is_active:
            return {
                'success': False,
                'error': 'User account is disabled'
            }
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        # Serialize user data
        user_data = UserSerializer(user).data
        
        return {
            'success': True,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': user_data
        }
    
    @staticmethod
    def refresh_token(refresh_token):
        """
        Refresh an access token using a refresh token
        
        Args:
            refresh_token: Refresh token string
            
        Returns:
            Dictionary with refresh result
        """
        try:
            refresh = RefreshToken(refresh_token)
            
            return {
                'success': True,
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
        except TokenError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def validate_token(token):
        """
        Validate an access token
        
        Args:
            token: Access token string
            
        Returns:
            Dictionary with validation result
        """
        try:
            # Decode the token
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            
            # Get the user
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            try:
                user = User.objects.get(id=user_id)
                
                # Serialize user data
                user_data = UserSerializer(user).data
                
                return {
                    'success': True,
                    'user': user_data
                }
            except User.DoesNotExist:
                return {
                    'success': False,
                    'error': 'User not found'
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def change_password(user, current_password, new_password):
        """
        Change a user's password
        
        Args:
            user: User object
            current_password: Current password
            new_password: New password
            
        Returns:
            Dictionary with change result
        """
        # Check current password
        if not user.check_password(current_password):
            return {
                'success': False,
                'error': 'Current password is incorrect'
            }
        
        # Set new password
        user.set_password(new_password)
        user.save()
        
        return {
            'success': True
        }
