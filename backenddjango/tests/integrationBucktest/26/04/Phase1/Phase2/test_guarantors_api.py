"""
Integration tests for guarantors API endpoints.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from borrowers.models import Guarantor
from .common import APITestClient, create_borrower, create_guarantor, assert_response_status, assert_response_contains

User = get_user_model()

@pytest.mark.django_db
class TestGuarantorsAPI:
    """Test guarantors API endpoints."""
    
    def setup_method(self):
        """Set up test client and data."""
        self.client = APITestClient()
        self.guarantors_url = reverse('guarantor-list')
        
        # Create test users with different roles
        self.admin_data = {
            'username': 'admin',
            'email': 'admin@example.com',
            'password': 'adminpassword',
            'role': 'admin'
        }
        
        self.broker_data = {
            'username': 'broker',
            'email': 'broker@example.com',
            'password': 'brokerpassword',
            'role': 'broker'
        }
        
        self.client_data = {
            'username': 'client',
            'email': 'client@example.com',
            'password': 'clientpassword',
            'role': 'client'
        }
        
        # Test guarantor data
        self.individual_guarantor_data = {
            'guarantor_type': 'individual',
            'first_name': 'Test',
            'last_name': 'Guarantor',
            'email': 'test.guarantor@example.com',
            'phone': '1234567890',
            'address': '123 Test St, Test City',
            'date_of_birth': '1990-01-01',
            'relationship': 'Spouse'
        }
        
        self.company_guarantor_data = {
            'guarantor_type': 'company',
            'company_name': 'Test Company Guarantor',
            'company_abn': '12345678901',
            'company_acn': '123456789',
            'address': '456 Business St, Test City',
            'email': 'company.guarantor@example.com',
            'phone': '0987654321'
        }
    
    def test_list_guarantors_as_admin(self):
        """Test listing guarantors as admin."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create a borrower
        borrower = create_borrower(created_by=admin)
        
        # Create a guarantor
        guarantor = create_guarantor(borrower=borrower, created_by=admin)
        
        # List guarantors
        response = self.client.get(self.guarantors_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        data = response.json()
        assert len(data['results']) >= 1, "Expected at least 1 guarantor in the response"
        assert data['results'][0]['email'] == guarantor.email
    
    def test_list_guarantors_as_broker(self):
        """Test listing guarantors as broker."""
        # Create a broker user and authenticate
        broker, _ = self.client.create_and_login(**self.broker_data)
        
        # Create a borrower associated with the broker
        borrower = create_borrower(created_by=broker)
        
        # Create a guarantor
        guarantor = create_guarantor(borrower=borrower, created_by=broker)
        
        # Create another guarantor not associated with the broker
        admin = User.objects.create_user(
            username='another_admin',
            email='another_admin@example.com',
            password='password',
            role='admin'
        )
        other_borrower = create_borrower(
            first_name='Other',
            last_name='Borrower',
            email='other.borrower@example.com',
            created_by=admin
        )
        other_guarantor = create_guarantor(
            borrower=other_borrower,
            first_name='Other',
            last_name='Guarantor',
            email='other.guarantor@example.com',
            created_by=admin
        )
        
        # List guarantors
        response = self.client.get(self.guarantors_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        data = response.json()
        
        # Broker should only see their own guarantors
        assert len(data['results']) == 1, "Broker should only see their own guarantors"
        assert data['results'][0]['email'] == guarantor.email
    
    def test_list_guarantors_as_client(self):
        """Test listing guarantors as client."""
        # Create a client user and authenticate
        client_user, _ = self.client.create_and_login(**self.client_data)
        
        # Create a borrower associated with the client
        borrower = create_borrower(user=client_user)
        
        # Create a guarantor
        guarantor = create_guarantor(borrower=borrower)
        
        # Create another guarantor not associated with the client
        other_borrower = create_borrower(
            first_name='Other',
            last_name='Borrower',
            email='other.borrower@example.com'
        )
        other_guarantor = create_guarantor(
            borrower=other_borrower,
            first_name='Other',
            last_name='Guarantor',
            email='other.guarantor@example.com'
        )
        
        # List guarantors
        response = self.client.get(self.guarantors_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        data = response.json()
        
        # Client should only see guarantors associated with their borrower profile
        assert len(data['results']) == 1, "Client should only see guarantors associated with their borrower profile"
        assert data['results'][0]['email'] == guarantor.email
    
    def test_create_individual_guarantor_as_admin(self):
        """Test creating an individual guarantor as admin."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create a borrower
        borrower = create_borrower(created_by=admin)
        
        # Create guarantor data with borrower ID
        guarantor_data = self.individual_guarantor_data.copy()
        guarantor_data['borrower'] = borrower.id
        
        # Create a guarantor
        response = self.client.post(self.guarantors_url, data=guarantor_data)
        
        # Assert response
        assert_response_status(response, status.HTTP_201_CREATED)
        assert_response_contains(response, 'first_name', guarantor_data['first_name'])
        assert_response_contains(response, 'last_name', guarantor_data['last_name'])
        assert_response_contains(response, 'email', guarantor_data['email'])
        assert_response_contains(response, 'guarantor_type', 'individual')
        
        # Verify guarantor was created
        guarantor_id = response.json()['id']
        guarantor = Guarantor.objects.get(id=guarantor_id)
        assert guarantor.created_by == admin
        assert guarantor.borrower == borrower
    
    def test_create_company_guarantor_as_admin(self):
        """Test creating a company guarantor as admin."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create a borrower
        borrower = create_borrower(created_by=admin)
        
        # Create guarantor data with borrower ID
        guarantor_data = self.company_guarantor_data.copy()
        guarantor_data['borrower'] = borrower.id
        
        # Create a guarantor
        response = self.client.post(self.guarantors_url, data=guarantor_data)
        
        # Assert response
        assert_response_status(response, status.HTTP_201_CREATED)
        assert_response_contains(response, 'company_name', guarantor_data['company_name'])
        assert_response_contains(response, 'email', guarantor_data['email'])
        assert_response_contains(response, 'guarantor_type', 'company')
        
        # Verify guarantor was created
        guarantor_id = response.json()['id']
        guarantor = Guarantor.objects.get(id=guarantor_id)
        assert guarantor.created_by == admin
        assert guarantor.borrower == borrower
    
    def test_create_guarantor_as_broker(self):
        """Test creating a guarantor as broker."""
        # Create a broker user and authenticate
        broker, _ = self.client.create_and_login(**self.broker_data)
        
        # Create a borrower associated with the broker
        borrower = create_borrower(created_by=broker)
        
        # Create guarantor data with borrower ID
        guarantor_data = self.individual_guarantor_data.copy()
        guarantor_data['borrower'] = borrower.id
        
        # Create a guarantor
        response = self.client.post(self.guarantors_url, data=guarantor_data)
        
        # Assert response
        assert_response_status(response, status.HTTP_201_CREATED)
        assert_response_contains(response, 'first_name', guarantor_data['first_name'])
        assert_response_contains(response, 'last_name', guarantor_data['last_name'])
        assert_response_contains(response, 'email', guarantor_data['email'])
        
        # Verify guarantor was created
        guarantor_id = response.json()['id']
        guarantor = Guarantor.objects.get(id=guarantor_id)
        assert guarantor.created_by == broker
        assert guarantor.borrower == borrower
    
    def test_create_guarantor_as_client(self):
        """Test creating a guarantor as client (should be forbidden)."""
        # Create a client user and authenticate
        client_user, _ = self.client.create_and_login(**self.client_data)
        
        # Create a borrower associated with the client
        borrower = create_borrower(user=client_user)
        
        # Create guarantor data with borrower ID
        guarantor_data = self.individual_guarantor_data.copy()
        guarantor_data['borrower'] = borrower.id
        
        # Try to create a guarantor
        response = self.client.post(self.guarantors_url, data=guarantor_data)
        
        # Assert response
        assert_response_status(response, status.HTTP_403_FORBIDDEN)
    
    def test_get_guarantor_detail_as_admin(self):
        """Test getting guarantor detail as admin."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create a borrower
        borrower = create_borrower(created_by=admin)
        
        # Create a guarantor
        guarantor = create_guarantor(borrower=borrower, created_by=admin)
        
        # Get guarantor detail
        guarantor_detail_url = reverse('guarantor-detail', args=[guarantor.id])
        response = self.client.get(guarantor_detail_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        assert_response_contains(response, 'first_name', guarantor.first_name)
        assert_response_contains(response, 'last_name', guarantor.last_name)
        assert_response_contains(response, 'email', guarantor.email)
    
    def test_update_guarantor_as_admin(self):
        """Test updating a guarantor as admin."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create a borrower
        borrower = create_borrower(created_by=admin)
        
        # Create a guarantor
        guarantor = create_guarantor(borrower=borrower, created_by=admin)
        
        # Update guarantor
        guarantor_detail_url = reverse('guarantor-detail', args=[guarantor.id])
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Guarantor',
            'email': 'updated.guarantor@example.com'
        }
        response = self.client.patch(guarantor_detail_url, data=update_data)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        assert_response_contains(response, 'first_name', update_data['first_name'])
        assert_response_contains(response, 'last_name', update_data['last_name'])
        assert_response_contains(response, 'email', update_data['email'])
    
    def test_delete_guarantor_as_admin(self):
        """Test deleting a guarantor as admin."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create a borrower
        borrower = create_borrower(created_by=admin)
        
        # Create a guarantor
        guarantor = create_guarantor(borrower=borrower, created_by=admin)
        
        # Delete guarantor
        guarantor_detail_url = reverse('guarantor-detail', args=[guarantor.id])
        response = self.client.delete(guarantor_detail_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_204_NO_CONTENT)
        
        # Verify guarantor is deleted
        with pytest.raises(Guarantor.DoesNotExist):
            Guarantor.objects.get(id=guarantor.id)
    
    def test_delete_guarantor_as_broker(self):
        """Test deleting a guarantor as broker."""
        # Create a broker user and authenticate
        broker, _ = self.client.create_and_login(**self.broker_data)
        
        # Create a borrower associated with the broker
        borrower = create_borrower(created_by=broker)
        
        # Create a guarantor
        guarantor = create_guarantor(borrower=borrower, created_by=broker)
        
        # Delete guarantor
        guarantor_detail_url = reverse('guarantor-detail', args=[guarantor.id])
        response = self.client.delete(guarantor_detail_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_204_NO_CONTENT)
        
        # Verify guarantor is deleted
        with pytest.raises(Guarantor.DoesNotExist):
            Guarantor.objects.get(id=guarantor.id)
    
    def test_delete_guarantor_as_client(self):
        """Test deleting a guarantor as client (should be forbidden)."""
        # Create a client user and authenticate
        client_user, _ = self.client.create_and_login(**self.client_data)
        
        # Create a borrower associated with the client
        borrower = create_borrower(user=client_user)
        
        # Create a guarantor
        guarantor = create_guarantor(borrower=borrower)
        
        # Try to delete guarantor
        guarantor_detail_url = reverse('guarantor-detail', args=[guarantor.id])
        response = self.client.delete(guarantor_detail_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_403_FORBIDDEN)
    
    def test_search_guarantors(self):
        """Test searching guarantors."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create a borrower
        borrower = create_borrower(created_by=admin)
        
        # Create guarantors with different names
        guarantor1 = create_guarantor(
            borrower=borrower,
            first_name='John',
            last_name='Smith',
            email='john.smith@example.com',
            created_by=admin
        )
        guarantor2 = create_guarantor(
            borrower=borrower,
            first_name='Jane',
            last_name='Doe',
            email='jane.doe@example.com',
            created_by=admin
        )
        
        # Search for guarantors with 'John'
        response = self.client.get(f"{self.guarantors_url}?search=John")
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        data = response.json()
        
        # Should only include guarantors with 'John' in their name
        assert len(data['results']) == 1, "Expected 1 guarantor matching 'John'"
        assert data['results'][0]['first_name'] == 'John'
        
        # Search for guarantors with 'example.com'
        response = self.client.get(f"{self.guarantors_url}?search=example.com")
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        data = response.json()
        
        # Should include both guarantors
        assert len(data['results']) == 2, "Expected 2 guarantors matching 'example.com'"
    
    def test_filter_guarantors_by_borrower(self):
        """Test filtering guarantors by borrower."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create borrowers
        borrower1 = create_borrower(
            first_name='First',
            last_name='Borrower',
            email='first.borrower@example.com',
            created_by=admin
        )
        borrower2 = create_borrower(
            first_name='Second',
            last_name='Borrower',
            email='second.borrower@example.com',
            created_by=admin
        )
        
        # Create guarantors for each borrower
        guarantor1 = create_guarantor(
            borrower=borrower1,
            first_name='First',
            last_name='Guarantor',
            email='first.guarantor@example.com',
            created_by=admin
        )
        guarantor2 = create_guarantor(
            borrower=borrower2,
            first_name='Second',
            last_name='Guarantor',
            email='second.guarantor@example.com',
            created_by=admin
        )
        
        # Filter guarantors by borrower1
        response = self.client.get(f"{self.guarantors_url}?borrower={borrower1.id}")
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        data = response.json()
        
        # Should only include guarantors for borrower1
        assert len(data['results']) == 1, "Expected 1 guarantor for borrower1"
        assert data['results'][0]['email'] == guarantor1.email
    
    def test_filter_guarantors_by_type(self):
        """Test filtering guarantors by type."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create a borrower
        borrower = create_borrower(created_by=admin)
        
        # Create an individual guarantor
        individual_guarantor = create_guarantor(
            borrower=borrower,
            guarantor_type='individual',
            first_name='Individual',
            last_name='Guarantor',
            email='individual.guarantor@example.com',
            created_by=admin
        )
        
        # Create a company guarantor
        company_guarantor = create_guarantor(
            borrower=borrower,
            guarantor_type='company',
            company_name='Company Guarantor',
            email='company.guarantor@example.com',
            created_by=admin
        )
        
        # Filter guarantors by individual type
        response = self.client.get(f"{self.guarantors_url}?guarantor_type=individual")
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        data = response.json()
        
        # Should only include individual guarantors
        assert len(data['results']) == 1, "Expected 1 individual guarantor"
        assert data['results'][0]['email'] == individual_guarantor.email
        
        # Filter guarantors by company type
        response = self.client.get(f"{self.guarantors_url}?guarantor_type=company")
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        data = response.json()
        
        # Should only include company guarantors
        assert len(data['results']) == 1, "Expected 1 company guarantor"
        assert data['results'][0]['email'] == company_guarantor.email
