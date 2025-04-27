"""
Tests for authentication services.
"""
import pytest
from django.contrib.auth import get_user_model
from users.services.auth_service import AuthService
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

User = get_user_model()

pytestmark = pytest.mark.django_db

@pytest.mark.service
def test_auth_service_login_valid_credentials(admin_user):
    """Test that a user can login with valid credentials."""
    # Set a known password
    admin_user.set_password('password123')
    admin_user.save()
    
    # Login with valid credentials
    result = AuthService.login(admin_user.email, 'password123')
    
    # Check that the login was successful
    assert result['success'] is True
    assert 'access' in result
    assert 'refresh' in result
    assert result['user']['email'] == admin_user.email
    assert result['user']['role'] == admin_user.role


@pytest.mark.service
def test_auth_service_login_invalid_credentials():
    """Test that a user cannot login with invalid credentials."""
    # Login with invalid credentials
    result = AuthService.login('nonexistent@example.com', 'password123')
    
    # Check that the login failed
    assert result['success'] is False
    assert 'error' in result
    assert result['error'] == 'Invalid credentials'


@pytest.mark.service
def test_auth_service_login_inactive_user(admin_user):
    """Test that an inactive user cannot login."""
    # Set a known password and make the user inactive
    admin_user.set_password('password123')
    admin_user.is_active = False
    admin_user.save()
    
    # Login with valid credentials but inactive user
    result = AuthService.login(admin_user.email, 'password123')
    
    # Check that the login failed
    assert result['success'] is False
    assert 'error' in result
    assert result['error'] == 'User account is disabled'


@pytest.mark.service
def test_auth_service_refresh_token_valid():
    """Test that a valid refresh token can be used to get a new access token."""
    # Create a user
    user = User.objects.create_user(
        email='test@example.com',
        password='password123',
        username='testuser'
    )
    
    # Generate a refresh token
    refresh = RefreshToken.for_user(user)
    
    # Refresh the token
    result = AuthService.refresh_token(str(refresh))
    
    # Check that the refresh was successful
    assert result['success'] is True
    assert 'access' in result
    assert 'refresh' in result


@pytest.mark.service
def test_auth_service_refresh_token_invalid():
    """Test that an invalid refresh token cannot be used to get a new access token."""
    # Refresh with an invalid token
    result = AuthService.refresh_token('invalid_token')
    
    # Check that the refresh failed
    assert result['success'] is False
    assert 'error' in result


@pytest.mark.service
def test_auth_service_validate_token_valid(admin_user):
    """Test that a valid token can be validated."""
    # Generate a token
    token = AccessToken.for_user(admin_user)
    
    # Validate the token
    result = AuthService.validate_token(str(token))
    
    # Check that the validation was successful
    assert result['success'] is True
    assert result['user']['email'] == admin_user.email
    assert result['user']['role'] == admin_user.role


@pytest.mark.service
def test_auth_service_validate_token_invalid():
    """Test that an invalid token cannot be validated."""
    # Validate an invalid token
    result = AuthService.validate_token('invalid_token')
    
    # Check that the validation failed
    assert result['success'] is False
    assert 'error' in result


@pytest.mark.service
def test_auth_service_change_password_valid(admin_user):
    """Test that a user can change their password with valid credentials."""
    # Set a known password
    admin_user.set_password('old_password')
    admin_user.save()
    
    # Change the password
    result = AuthService.change_password(admin_user, 'old_password', 'new_password')
    
    # Check that the password change was successful
    assert result['success'] is True
    
    # Check that the user can login with the new password
    login_result = AuthService.login(admin_user.email, 'new_password')
    assert login_result['success'] is True


@pytest.mark.service
def test_auth_service_change_password_invalid_old_password(admin_user):
    """Test that a user cannot change their password with an invalid old password."""
    # Set a known password
    admin_user.set_password('old_password')
    admin_user.save()
    
    # Change the password with an invalid old password
    result = AuthService.change_password(admin_user, 'wrong_password', 'new_password')
    
    # Check that the password change failed
    assert result['success'] is False
    assert 'error' in result
    assert result['error'] == 'Current password is incorrect'
