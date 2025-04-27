"""
Integration tests for authentication services.
"""
import pytest
from django.contrib.auth import get_user_model
from users.services.auth_service import AuthService
from rest_framework_simplejwt.tokens import RefreshToken
from unittest.mock import patch, MagicMock

User = get_user_model()

@pytest.fixture
def admin_user():
    """Create an admin user for testing."""
    return User.objects.create_user(
        username="admin",
        email="admin@example.com",
        password="password123",
        first_name="Admin",
        last_name="User",
        role="admin"
    )

@pytest.fixture
def inactive_user():
    """Create an inactive user for testing."""
    user = User.objects.create_user(
        username="inactive",
        email="inactive@example.com",
        password="password123",
        first_name="Inactive",
        last_name="User",
        role="user"
    )
    user.is_active = False
    user.save()
    return user

@pytest.mark.django_db
def test_login_success(admin_user):
    """Test successful login."""
    result = AuthService.login(
        email="admin@example.com",
        password="password123"
    )
    
    # Verify login was successful
    assert result["success"] is True
    assert "refresh" in result
    assert "access" in result
    assert "user" in result
    
    # Verify user data
    user_data = result["user"]
    assert user_data["email"] == "admin@example.com"
    assert user_data["first_name"] == "Admin"
    assert user_data["last_name"] == "User"
    assert user_data["role"] == "admin"

@pytest.mark.django_db
def test_login_invalid_credentials():
    """Test login with invalid credentials."""
    # Wrong password
    result = AuthService.login(
        email="admin@example.com",
        password="wrong_password"
    )
    
    assert result["success"] is False
    assert "error" in result
    assert "Invalid credentials" in result["error"]
    
    # Non-existent user
    result = AuthService.login(
        email="nonexistent@example.com",
        password="password123"
    )
    
    assert result["success"] is False
    assert "error" in result
    assert "Invalid credentials" in result["error"]

@pytest.mark.django_db
def test_login_inactive_user(inactive_user):
    """Test login with inactive user."""
    # Mock the authenticate function to return the inactive user
    with patch('users.services.auth_service.authenticate', return_value=inactive_user):
        result = AuthService.login(
            email="inactive@example.com",
            password="password123"
        )
    
    assert result["success"] is False
    assert "error" in result
    assert "disabled" in result["error"].lower()

@pytest.mark.django_db
def test_refresh_token(admin_user):
    """Test refreshing a token."""
    # Generate a refresh token
    refresh = RefreshToken.for_user(admin_user)
    refresh_token = str(refresh)
    
    # Mock the RefreshToken to return a different token when refreshed
    with patch('users.services.auth_service.RefreshToken') as mock_refresh_token:
        # Create a mock refresh token that returns different values
        mock_refresh = MagicMock()
        mock_refresh.access_token = "new_access_token"
        mock_refresh.__str__.return_value = "new_refresh_token"
        
        # Make the mock RefreshToken constructor return our mock
        mock_refresh_token.return_value = mock_refresh
        
        # Refresh the token
        result = AuthService.refresh_token(refresh_token)
    
    # Verify refresh was successful
    assert result["success"] is True
    assert "refresh" in result
    assert "access" in result
    
    # Verify tokens are different
    assert result["refresh"] != refresh_token
    assert result["access"] != str(refresh.access_token)

@pytest.mark.django_db
def test_refresh_token_invalid():
    """Test refreshing an invalid token."""
    result = AuthService.refresh_token("invalid_token")
    
    assert result["success"] is False
    assert "error" in result

@pytest.mark.django_db
def test_validate_token(admin_user):
    """Test validating a token."""
    # Generate a token
    refresh = RefreshToken.for_user(admin_user)
    access_token = str(refresh.access_token)
    
    # Validate the token
    result = AuthService.validate_token(access_token)
    
    # Verify validation was successful
    assert result["success"] is True
    assert "user" in result
    
    # Verify user data
    user_data = result["user"]
    assert user_data["email"] == "admin@example.com"
    assert user_data["first_name"] == "Admin"
    assert user_data["last_name"] == "User"
    assert user_data["role"] == "admin"

@pytest.mark.django_db
def test_validate_token_invalid():
    """Test validating an invalid token."""
    result = AuthService.validate_token("invalid_token")
    
    assert result["success"] is False
    assert "error" in result

@pytest.mark.django_db
def test_change_password(admin_user):
    """Test changing a user's password."""
    result = AuthService.change_password(
        user=admin_user,
        current_password="password123",
        new_password="new_password123"
    )
    
    # Verify password change was successful
    assert result["success"] is True
    
    # Verify user can login with new password
    login_result = AuthService.login(
        email="admin@example.com",
        password="new_password123"
    )
    
    assert login_result["success"] is True

@pytest.mark.django_db
def test_change_password_incorrect_current(admin_user):
    """Test changing a password with incorrect current password."""
    result = AuthService.change_password(
        user=admin_user,
        current_password="wrong_password",
        new_password="new_password123"
    )
    
    assert result["success"] is False
    assert "error" in result
    assert "Current password is incorrect" in result["error"]
    
    # Verify user can still login with old password
    login_result = AuthService.login(
        email="admin@example.com",
        password="password123"
    )
    
    assert login_result["success"] is True
