from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import User, Notification
from applications.models import Application, ApplicationStatus
from documents.models import DocumentTemplate
from borrowers.models import Borrower
from brokers.models import Broker


class AdminAPIEndpointsTest(APITestCase):
    """
    Test admin-only API endpoints
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
    
    def test_admin_user_management_endpoints(self):
        """
        Test admin-only user management endpoints
        """
        # Test user creation endpoint
        user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newuserpassword',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        admin_create_response = self.admin_client.post(reverse('user-list'), user_data)
        self.assertEqual(admin_create_response.status_code, status.HTTP_201_CREATED)
        
        non_admin_create_response = self.non_admin_client.post(reverse('user-list'), user_data)
        self.assertEqual(non_admin_create_response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_admin_application_status_management(self):
        """
        Test admin-only application status management endpoints
        """
        # Create a new application
        application_data = {
            'title': 'Test Application',
            'loan_amount': 100000,
            'loan_term': 12,
            'interest_rate': 5.5,
            'status': 'draft'
        }
        
        admin_create_response = self.admin_client.post(reverse('application-list'), application_data)
        self.assertEqual(admin_create_response.status_code, status.HTTP_201_CREATED)
        
        # Get the created application's ID
        application_id = admin_create_response.data['id']
        
        # Update application status to approved (admin-only action)
        status_update = {
            'status': 'approved'
        }
        
        admin_update_response = self.admin_client.patch(
            reverse('application-detail', kwargs={'pk': application_id}),
            status_update
        )
        self.assertEqual(admin_update_response.status_code, status.HTTP_200_OK)
        
        # Non-admin should not be able to update to approved status
        non_admin_update_response = self.non_admin_client.patch(
            reverse('application-detail', kwargs={'pk': application_id}),
            status_update
        )
        self.assertEqual(non_admin_update_response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_admin_document_management(self):
        """
        Test admin-only document management endpoints
        """
        # Create a document
        document_data = {
            'name': 'Test Document',
            'document_type': 'agreement',
            'content': 'This is a test document content'
        }
        
        admin_create_response = self.admin_client.post(reverse('document-list'), document_data)
        self.assertEqual(admin_create_response.status_code, status.HTTP_201_CREATED)
        
        # Get the created document's ID
        document_id = admin_create_response.data['id']
        
        # Admin should be able to delete documents
        admin_delete_response = self.admin_client.delete(
            reverse('document-detail', kwargs={'pk': document_id})
        )
        self.assertEqual(admin_delete_response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Create another document for non-admin test
        another_document_response = self.admin_client.post(reverse('document-list'), document_data)
        another_document_id = another_document_response.data['id']
        
        # Non-admin should not be able to delete documents
        non_admin_delete_response = self.non_admin_client.delete(
            reverse('document-detail', kwargs={'pk': another_document_id})
        )
        self.assertEqual(non_admin_delete_response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_admin_borrower_management(self):
        """
        Test admin-only borrower management actions
        """
        # Create a borrower
        borrower_data = {
            'first_name': 'Test',
            'last_name': 'Borrower',
            'email': 'borrower@example.com',
            'phone': '1234567890',
            'address': '123 Main St'
        }
        
        admin_create_response = self.admin_client.post(reverse('borrower-list'), borrower_data)
        self.assertEqual(admin_create_response.status_code, status.HTTP_201_CREATED)
        
        # Get the created borrower's ID
        borrower_id = admin_create_response.data['id']
        
        # Admin should be able to delete borrowers
        admin_delete_response = self.admin_client.delete(
            reverse('borrower-detail', kwargs={'pk': borrower_id})
        )
        self.assertEqual(admin_delete_response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Create another borrower for non-admin test
        another_borrower_response = self.admin_client.post(reverse('borrower-list'), borrower_data)
        another_borrower_id = another_borrower_response.data['id']
        
        # Non-admin should not be able to delete borrowers
        non_admin_delete_response = self.non_admin_client.delete(
            reverse('borrower-detail', kwargs={'pk': another_borrower_id})
        )
        self.assertEqual(non_admin_delete_response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_admin_notification_management(self):
        """
        Test admin-only notification management actions
        """
        # Create a notification for the admin user
        notification_data = {
            'user': self.admin_user.id,
            'title': 'Test Notification',
            'message': 'This is a test notification',
            'notification_type': 'system'
        }
        
        admin_create_response = self.admin_client.post(reverse('notification-list'), notification_data)
        self.assertEqual(admin_create_response.status_code, status.HTTP_201_CREATED)
        
        # Get the created notification's ID
        notification_id = admin_create_response.data['id']
        
        # Admin should be able to delete any notification
        admin_delete_response = self.admin_client.delete(
            reverse('notification-detail', kwargs={'pk': notification_id})
        )
        self.assertEqual(admin_delete_response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Create a notification for the non-admin user
        notification_data = {
            'user': self.non_admin_user.id,
            'title': 'Test Notification',
            'message': 'This is a test notification',
            'notification_type': 'system'
        }
        
        admin_create_response = self.admin_client.post(reverse('notification-list'), notification_data)
        notification_id = admin_create_response.data['id']
        
        # Non-admin should not be able to delete other users' notifications
        non_admin_delete_response = self.non_admin_client.delete(
            reverse('notification-detail', kwargs={'pk': notification_id})
        )
        self.assertEqual(non_admin_delete_response.status_code, status.HTTP_403_FORBIDDEN)
