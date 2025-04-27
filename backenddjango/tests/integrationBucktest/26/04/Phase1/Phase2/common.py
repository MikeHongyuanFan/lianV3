"""
Common utilities for Phase 2 integration tests.
This module provides helper functions and fixtures for API testing.
"""
import json
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from borrowers.models import Borrower, Guarantor
from brokers.models import Broker, Branch

User = get_user_model()

def get_tokens_for_user(user):
    """
    Get JWT tokens for a user.
    
    Args:
        user: User instance
        
    Returns:
        dict: Dictionary containing access and refresh tokens
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class APITestClient:
    """Helper class for API testing with authentication support."""
    
    def __init__(self):
        self.client = APIClient()
        self.user = None
        self.tokens = None
    
    def create_user(self, username='testuser', email='test@example.com', password='password123', role='client'):
        """
        Create a test user.
        
        Args:
            username: Username for the test user
            email: Email for the test user
            password: Password for the test user
            role: Role for the test user
            
        Returns:
            User: Created user instance
        """
        self.user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        self.user.role = role
        self.user.save()
        return self.user
    
    def create_and_login(self, username='testuser', email='test@example.com', password='password123', role='client'):
        """
        Create a test user and authenticate.
        
        Args:
            username: Username for the test user
            email: Email for the test user
            password: Password for the test user
            role: Role for the test user
            
        Returns:
            tuple: (User instance, tokens dict)
        """
        self.create_user(username, email, password, role)
        self.authenticate()
        return self.user, self.tokens
    
    def authenticate(self):
        """
        Authenticate the client with the current user.
        
        Returns:
            dict: Dictionary containing access and refresh tokens
        """
        if not self.user:
            raise ValueError("No user set. Call create_user first.")
        
        self.tokens = get_tokens_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.tokens['access']}")
        return self.tokens
    
    def clear_credentials(self):
        """Clear authentication credentials."""
        self.client.credentials()
    
    def get(self, url, **kwargs):
        """Wrapper for client.get."""
        return self.client.get(url, **kwargs)
    
    def post(self, url, data=None, format='json', **kwargs):
        """Wrapper for client.post."""
        return self.client.post(url, data, format=format, **kwargs)
    
    def put(self, url, data=None, format='json', **kwargs):
        """Wrapper for client.put."""
        return self.client.put(url, data, format=format, **kwargs)
    
    def patch(self, url, data=None, format='json', **kwargs):
        """Wrapper for client.patch."""
        return self.client.patch(url, data, format=format, **kwargs)
    
    def delete(self, url, **kwargs):
        """Wrapper for client.delete."""
        return self.client.delete(url, **kwargs)

def create_borrower(user=None, **kwargs):
    """
    Create a test borrower.
    
    Args:
        user: User instance to associate with the borrower
        **kwargs: Additional fields for the borrower
        
    Returns:
        Borrower: Created borrower instance
    """
    defaults = {
        'first_name': 'Test',
        'last_name': 'Borrower',
        'email': 'borrower@example.com',
        'phone': '1234567890',
        'residential_address': '123 Test St',
        'date_of_birth': '1990-01-01',
    }
    defaults.update(kwargs)
    
    borrower = Borrower.objects.create(**defaults)
    if user:
        borrower.user = user
        borrower.save()
    
    return borrower

def create_guarantor(borrower, **kwargs):
    """
    Create a test guarantor.
    
    Args:
        borrower: Borrower instance to associate with the guarantor
        **kwargs: Additional fields for the guarantor
        
    Returns:
        Guarantor: Created guarantor instance
    """
    defaults = {
        'guarantor_type': 'individual',
        'first_name': 'Test',
        'last_name': 'Guarantor',
        'email': 'guarantor@example.com',
        'phone': '0987654321',
        'address': '456 Test St',
        'date_of_birth': '1985-01-01',
    }
    defaults.update(kwargs)
    
    guarantor = Guarantor.objects.create(borrower=borrower, **defaults)
    return guarantor

def create_broker(user=None, **kwargs):
    """
    Create a test broker.
    
    Args:
        user: User instance to associate with the broker
        **kwargs: Additional fields for the broker
        
    Returns:
        Broker: Created broker instance
    """
    defaults = {
        'name': 'Test Broker',
        'company': 'Test Brokerage',
        'email': 'broker@example.com',
        'phone': '1234567890',
        'address': '789 Test St',
    }
    defaults.update(kwargs)
    
    broker = Broker.objects.create(**defaults)
    if user:
        broker.user = user
        broker.save()
    
    return broker

def create_branch(**kwargs):
    """
    Create a test branch.
    
    Args:
        **kwargs: Fields for the branch
        
    Returns:
        Branch: Created branch instance
    """
    defaults = {
        'name': 'Test Branch',
        'address': '101 Branch St',
        'phone': '1357924680',
        'email': 'branch@example.com',
    }
    defaults.update(kwargs)
    
    branch = Branch.objects.create(**defaults)
    return branch

def assert_response_status(response, expected_status):
    """
    Assert that the response has the expected status code.
    
    Args:
        response: Response object
        expected_status: Expected status code
        
    Raises:
        AssertionError: If the status code doesn't match
    """
    assert response.status_code == expected_status, \
        f"Expected status {expected_status}, got {response.status_code}. Response: {response.content.decode()}"

def assert_response_contains(response, key, value=None):
    """
    Assert that the response contains the expected key and optionally value.
    
    Args:
        response: Response object
        key: Key to check for
        value: Optional value to check for
        
    Raises:
        AssertionError: If the key or value is not found
    """
    data = json.loads(response.content)
    assert key in data, f"Response does not contain key '{key}'. Response: {data}"
    if value is not None:
        assert data[key] == value, f"Expected '{key}' to be '{value}', got '{data[key]}'"
