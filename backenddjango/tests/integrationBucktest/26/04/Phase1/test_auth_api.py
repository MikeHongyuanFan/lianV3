"""
Integration tests for authentication API endpoints.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from .common import APITestClient, assert_response_status, assert_response_contains

User = get_user_model()

@pytest.mark.django_db
class TestAuthAPI:
    """Test authentication API endpoints."""
    
    def setup_method(self):
        """Set up test client and data."""
        self.client = APITestClient()
        self.login_url = reverse('login')
        self.refresh_url = reverse('token_refresh')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        }
    
    def test_login_success(self):
        """Test successful login."""
        # Create a user
        user = self.client.create_user(**self.user_data)
        
        # Login
        response = self.client.post(
            self.login_url,
            data={
                'email': self.user_data['email'],
                'password': self.user_data['password']
            }
        )
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        assert_response_contains(response, 'access')
        assert_response_contains(response, 'refresh')
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        # Create a user
        user = self.client.create_user(**self.user_data)
        
        # Login with wrong password
        response = self.client.post(
            self.login_url,
            data={
                'email': self.user_data['email'],
                'password': 'wrongpassword'
            }
        )
        
        # Assert response
        assert_response_status(response, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_nonexistent_user(self):
        """Test login with nonexistent user."""
        # Login with nonexistent user
        response = self.client.post(
            self.login_url,
            data={
                'email': 'nonexistent@example.com',
                'password': 'password123'
            }
        )
        
        # Assert response
        assert_response_status(response, status.HTTP_401_UNAUTHORIZED)
    
    def test_token_refresh_success(self):
        """Test successful token refresh."""
        # Create a user and get tokens
        user = self.client.create_user(**self.user_data)
        tokens = self.client.authenticate()
        
        # Refresh token
        response = self.client.post(
            self.refresh_url,
            data={
                'refresh': tokens['refresh']
            }
        )
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        assert_response_contains(response, 'access')
    
    def test_token_refresh_invalid_token(self):
        """Test token refresh with invalid token."""
        # Refresh with invalid token
        response = self.client.post(
            self.refresh_url,
            data={
                'refresh': 'invalidtoken'
            }
        )
        
        # Assert response
        assert_response_status(response, status.HTTP_401_UNAUTHORIZED)
    
    def test_access_protected_endpoint_with_token(self):
        """Test accessing protected endpoint with valid token."""
        # Create a user and authenticate
        self.client.create_and_login(**self.user_data)
        
        # Access user profile endpoint
        profile_url = reverse('user-profile')
        response = self.client.get(profile_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
    
    def test_access_protected_endpoint_without_token(self):
        """Test accessing protected endpoint without token."""
        # Create a user but don't authenticate
        self.client.create_user(**self.user_data)
        self.client.clear_credentials()
        
        # Access user profile endpoint
        profile_url = reverse('user-profile')
        response = self.client.get(profile_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_401_UNAUTHORIZED)
    
    def test_access_protected_endpoint_with_invalid_token(self):
        """Test accessing protected endpoint with invalid token."""
        # Create a user
        self.client.create_user(**self.user_data)
        
        # Set invalid token
        self.client.client.credentials(HTTP_AUTHORIZATION='Bearer invalidtoken')
        
        # Access user profile endpoint
        profile_url = reverse('user-profile')
        response = self.client.get(profile_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_401_UNAUTHORIZED)
