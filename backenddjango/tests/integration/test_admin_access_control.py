from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import User


class AdminAccessControlTest(APITestCase):
    """
    Test role-based access control for admin users across all API endpoints
    """
    
    def setUp(self):
        """
        Set up test data and clients
        """
        # Create admin user
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
        self.admin_user.role = 'admin'
        self.admin_user.save()
        
        # Create non-admin users with different roles
        self.broker_user = User.objects.create_user(
            username='broker',
            email='broker@example.com',
            password='brokerpassword'
        )
        self.broker_user.role = 'broker'
        self.broker_user.save()
        
        self.bd_user = User.objects.create_user(
            username='bd',
            email='bd@example.com',
            password='bdpassword'
        )
        self.bd_user.role = 'bd'
        self.bd_user.save()
        
        self.client_user = User.objects.create_user(
            username='client',
            email='client@example.com',
            password='clientpassword'
        )
        self.client_user.role = 'client'
        self.client_user.save()
        
        # Create API clients for each user type
        self.admin_client = APIClient()
        self.admin_client.force_authenticate(user=self.admin_user)
        
        self.broker_client = APIClient()
        self.broker_client.force_authenticate(user=self.broker_user)
        
        self.bd_client = APIClient()
        self.bd_client.force_authenticate(user=self.bd_user)
        
        self.client_client = APIClient()
        self.client_client.force_authenticate(user=self.client_user)
        
        self.unauthenticated_client = APIClient()
        
        # Define API endpoints to test
        self.endpoints = {
            # Users app endpoints
            'user-list': reverse('user-list'),
            'notification-list': reverse('notification-list'),
            
            # Applications app endpoints
            'application-list': reverse('application-list'),
            
            # Borrowers app endpoints
            'borrower-list': reverse('borrower-list'),
            
            # Documents app endpoints
            'document-list': reverse('document-list'),
        }
    
    def test_admin_access_to_all_endpoints(self):
        """
        Test that admin users have access to all endpoints
        """
        for endpoint_name, endpoint_url in self.endpoints.items():
            response = self.admin_client.get(endpoint_url)
            self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED], 
                         f"Admin should have access to {endpoint_name}, got {response.status_code}")
    
    def test_non_admin_restricted_access(self):
        """
        Test that non-admin users have restricted access to admin-only endpoints
        """
        # Define admin-only endpoints
        admin_only_endpoints = [
            'user-list',
            'document-list',
        ]
        
        # Test broker access
        for endpoint_name in admin_only_endpoints:
            endpoint_url = self.endpoints[endpoint_name]
            response = self.broker_client.get(endpoint_url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                           f"Broker should not have access to {endpoint_name}")
        
        # Test BD access
        for endpoint_name in admin_only_endpoints:
            endpoint_url = self.endpoints[endpoint_name]
            response = self.bd_client.get(endpoint_url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                           f"BD should not have access to {endpoint_name}")
        
        # Test client access
        for endpoint_name in admin_only_endpoints:
            endpoint_url = self.endpoints[endpoint_name]
            response = self.client_client.get(endpoint_url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                           f"Client should not have access to {endpoint_name}")
    
    def test_unauthenticated_access_denied(self):
        """
        Test that unauthenticated users cannot access any protected endpoints
        """
        for endpoint_name, endpoint_url in self.endpoints.items():
            response = self.unauthenticated_client.get(endpoint_url)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                           f"Unauthenticated user should not have access to {endpoint_name}")
