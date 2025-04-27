"""
Integration tests for users API endpoints.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from .common import APITestClient, create_admin_user, assert_response_status, assert_response_contains

User = get_user_model()

@pytest.mark.django_db
class TestUsersAPI:
    """Test users API endpoints."""
    
    def setup_method(self):
        """Set up test client and data."""
        self.client = APITestClient()
        self.users_url = reverse('user-list')
        self.profile_url = reverse('user-profile')
        self.profile_update_url = reverse('user-profile-update')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'role': 'client'
        }
        self.admin_data = {
            'username': 'admin',
            'email': 'admin@example.com',
            'password': 'adminpassword',
            'role': 'admin'
        }
    
    def test_get_user_profile(self):
        """Test getting user profile."""
        # Create a user and authenticate
        user, _ = self.client.create_and_login(**self.user_data)
        
        # Get profile
        response = self.client.get(self.profile_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        assert_response_contains(response, 'email', self.user_data['email'])
        assert_response_contains(response, 'role', self.user_data['role'])
    
    def test_update_user_profile(self):
        """Test updating user profile."""
        # Create a user and authenticate
        user, _ = self.client.create_and_login(**self.user_data)
        
        # Update profile
        update_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'updated@example.com'
        }
        response = self.client.put(self.profile_update_url, data=update_data)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        assert_response_contains(response, 'first_name', update_data['first_name'])
        assert_response_contains(response, 'last_name', update_data['last_name'])
        assert_response_contains(response, 'email', update_data['email'])
    
    def test_list_users_as_admin(self):
        """Test listing users as admin."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create another user
        User.objects.create_user(
            username='anotheruser',
            email='another@example.com',
            password='password123'
        )
        
        # List users
        response = self.client.get(self.users_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        data = response.json()
        assert len(data['results']) >= 2, "Expected at least 2 users in the response"
    
    def test_list_users_as_regular_user(self):
        """Test listing users as regular user (should be allowed)."""
        # Create a regular user and authenticate
        user, _ = self.client.create_and_login(**self.user_data)
        
        # List users
        response = self.client.get(self.users_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        data = response.json()
        assert 'results' in data, "Expected paginated response with 'results' key"
    
    def test_create_user_as_admin(self):
        """Test creating a user as admin."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create a new user
        new_user_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpassword',
            'role': 'client'
        }
        response = self.client.post(self.users_url, data=new_user_data)
        
        # Assert response
        assert_response_status(response, status.HTTP_201_CREATED)
        assert_response_contains(response, 'email', new_user_data['email'])
        assert_response_contains(response, 'role', new_user_data['role'])
    
    def test_create_user_as_regular_user(self):
        """Test creating a user as regular user (should be forbidden)."""
        # Create a regular user and authenticate
        user, _ = self.client.create_and_login(**self.user_data)
        
        # Try to create a new user
        new_user_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpassword',
            'role': 'client'
        }
        response = self.client.post(self.users_url, data=new_user_data)
        
        # Assert response
        assert_response_status(response, status.HTTP_403_FORBIDDEN)
    
    def test_get_user_detail_as_admin(self):
        """Test getting user detail as admin."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create another user
        user = User.objects.create_user(
            username='anotheruser',
            email='another@example.com',
            password='password123'
        )
        
        # Get user detail
        user_detail_url = reverse('user-detail', args=[user.id])
        response = self.client.get(user_detail_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        assert_response_contains(response, 'email', user.email)
    
    def test_get_user_detail_as_regular_user(self):
        """Test getting user detail as regular user (should be allowed)."""
        # Create a regular user and authenticate
        user, _ = self.client.create_and_login(**self.user_data)
        
        # Create another user
        another_user = User.objects.create_user(
            username='anotheruser',
            email='another@example.com',
            password='password123'
        )
        
        # Get user detail
        user_detail_url = reverse('user-detail', args=[another_user.id])
        response = self.client.get(user_detail_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        assert_response_contains(response, 'email', another_user.email)
    
    def test_update_user_as_admin(self):
        """Test updating a user as admin."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create another user
        user = User.objects.create_user(
            username='anotheruser',
            email='another@example.com',
            password='password123'
        )
        
        # Update user
        user_detail_url = reverse('user-detail', args=[user.id])
        update_data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updated@example.com'
        }
        response = self.client.patch(user_detail_url, data=update_data)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        assert_response_contains(response, 'first_name', update_data['first_name'])
        assert_response_contains(response, 'last_name', update_data['last_name'])
        assert_response_contains(response, 'email', update_data['email'])
    
    def test_delete_user_as_admin(self):
        """Test deleting a user as admin."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create another user
        user = User.objects.create_user(
            username='anotheruser',
            email='another@example.com',
            password='password123'
        )
        
        # Delete user
        user_detail_url = reverse('user-detail', args=[user.id])
        response = self.client.delete(user_detail_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_204_NO_CONTENT)
        
        # Verify user is deleted
        with pytest.raises(User.DoesNotExist):
            User.objects.get(id=user.id)
    
    def test_delete_user_as_regular_user(self):
        """Test deleting a user as regular user (should be forbidden)."""
        # Create a regular user and authenticate
        user, _ = self.client.create_and_login(**self.user_data)
        
        # Create another user
        another_user = User.objects.create_user(
            username='anotheruser',
            email='another@example.com',
            password='password123'
        )
        
        # Delete user
        user_detail_url = reverse('user-detail', args=[another_user.id])
        response = self.client.delete(user_detail_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_403_FORBIDDEN)
