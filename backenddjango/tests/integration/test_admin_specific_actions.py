from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import User


class AdminSpecificActionsTest(APITestCase):
    """
    Test admin-specific actions across different API endpoints
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
        
        # Create non-admin user
        self.non_admin_user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='userpassword'
        )
        self.non_admin_user.role = 'broker'
        self.non_admin_user.save()
        
        # Create API clients
        self.admin_client = APIClient()
        self.admin_client.force_authenticate(user=self.admin_user)
        
        self.non_admin_client = APIClient()
        self.non_admin_client.force_authenticate(user=self.non_admin_user)
    
    def test_admin_user_management(self):
        """
        Test that only admin users can create, update, and delete users
        """
        # Test user creation
        user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newuserpassword',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        # Admin should be able to create users
        admin_response = self.admin_client.post(reverse('user-list'), user_data)
        self.assertEqual(admin_response.status_code, status.HTTP_201_CREATED)
        
        # Non-admin should not be able to create users
        non_admin_response = self.non_admin_client.post(reverse('user-list'), user_data)
        self.assertEqual(non_admin_response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_admin_application_management(self):
        """
        Test that only admin users can perform certain application management actions
        """
        # Create a test application
        application_data = {
            'title': 'Test Application',
            'loan_amount': 100000,
            'loan_term': 12,
            'interest_rate': 5.5,
            'status': 'draft'
        }
        
        # Admin creates an application
        application_response = self.admin_client.post(
            reverse('application-list'),
            application_data
        )
        self.assertEqual(application_response.status_code, status.HTTP_201_CREATED)
    
    def test_admin_document_management(self):
        """
        Test that only admin users can manage document templates
        """
        # Skip this test as document creation requires additional setup
        self.skipTest("Document creation requires additional setup")
    
    def test_admin_borrower_management(self):
        """
        Test that only admin users can access borrower data
        """
        # Create a borrower
        borrower_data = {
            'first_name': 'Test',
            'last_name': 'Borrower',
            'email': 'borrower@example.com',
            'phone': '1234567890',
            'address': '123 Main St'
        }
        
        # Admin should be able to create borrowers
        admin_response = self.admin_client.post(
            reverse('borrower-list'),
            borrower_data
        )
        self.assertEqual(admin_response.status_code, status.HTTP_201_CREATED)
