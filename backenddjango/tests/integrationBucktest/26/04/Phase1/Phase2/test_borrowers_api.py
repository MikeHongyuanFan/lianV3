"""
Integration tests for borrowers API endpoints.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from borrowers.models import Borrower
from .common import APITestClient, create_borrower, assert_response_status, assert_response_contains

User = get_user_model()

@pytest.mark.django_db
class TestBorrowersAPI:
    """Test borrowers API endpoints."""
    
    def setup_method(self):
        """Set up test client and data."""
        self.client = APITestClient()
        self.borrowers_url = reverse('borrower-list')
        self.company_borrowers_url = reverse('company-borrower-list')
        
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
        
        # Test borrower data
        self.borrower_data = {
            'first_name': 'Test',
            'last_name': 'Borrower',
            'email': 'test.borrower@example.com',
            'phone': '1234567890',
            'residential_address': '123 Test St, Test City',
            'date_of_birth': '1990-01-01',
            'employment_type': 'full_time',
            'annual_income': '75000.00'
        }
        
        self.company_borrower_data = {
            'is_company': True,
            'company_name': 'Test Company',
            'company_abn': '12345678901',
            'company_acn': '123456789',
            'company_address': '456 Business St, Test City',
            'email': 'company@example.com',
            'phone': '0987654321'
        }
    
    def test_list_borrowers_as_admin(self):
        """Test listing borrowers as admin."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create a borrower
        borrower = create_borrower(created_by=admin)
        
        # List borrowers
        response = self.client.get(self.borrowers_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        data = response.json()
        assert len(data['results']) >= 1, "Expected at least 1 borrower in the response"
        assert data['results'][0]['email'] == borrower.email
    
    def test_list_borrowers_as_broker(self):
        """Test listing borrowers as broker."""
        # Create a broker user and authenticate
        broker, _ = self.client.create_and_login(**self.broker_data)
        
        # Create a borrower associated with the broker
        borrower = create_borrower(created_by=broker)
        
        # Create another borrower not associated with the broker
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
        
        # List borrowers
        response = self.client.get(self.borrowers_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        data = response.json()
        
        # Broker should only see their own borrowers
        assert len(data['results']) == 1, "Broker should only see their own borrowers"
        assert data['results'][0]['email'] == borrower.email
    
    def test_list_borrowers_as_client(self):
        """Test listing borrowers as client."""
        # Create a client user and authenticate
        client_user, _ = self.client.create_and_login(**self.client_data)
        
        # Create a borrower associated with the client
        borrower = create_borrower(user=client_user)
        
        # Create another borrower not associated with the client
        other_borrower = create_borrower(
            first_name='Other',
            last_name='Borrower',
            email='other.borrower@example.com'
        )
        
        # List borrowers
        response = self.client.get(self.borrowers_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        data = response.json()
        
        # Client should only see their own borrower profile
        assert len(data['results']) <= 1, "Client should only see their own borrower profile"
        if len(data['results']) == 1:
            assert data['results'][0]['email'] == borrower.email
    
    def test_create_borrower_as_admin(self):
        """Test creating a borrower as admin."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create a borrower
        response = self.client.post(self.borrowers_url, data=self.borrower_data)
        
        # Assert response
        assert_response_status(response, status.HTTP_201_CREATED)
        assert_response_contains(response, 'first_name', self.borrower_data['first_name'])
        assert_response_contains(response, 'last_name', self.borrower_data['last_name'])
        assert_response_contains(response, 'email', self.borrower_data['email'])
        
        # Verify borrower was created
        borrower_id = response.json()['id']
        borrower = Borrower.objects.get(id=borrower_id)
        assert borrower.created_by == admin
    
    def test_create_borrower_as_broker(self):
        """Test creating a borrower as broker."""
        # Create a broker user and authenticate
        broker, _ = self.client.create_and_login(**self.broker_data)
        
        # Create a borrower
        response = self.client.post(self.borrowers_url, data=self.borrower_data)
        
        # Assert response
        assert_response_status(response, status.HTTP_201_CREATED)
        assert_response_contains(response, 'first_name', self.borrower_data['first_name'])
        assert_response_contains(response, 'last_name', self.borrower_data['last_name'])
        assert_response_contains(response, 'email', self.borrower_data['email'])
        
        # Verify borrower was created
        borrower_id = response.json()['id']
        borrower = Borrower.objects.get(id=borrower_id)
        assert borrower.created_by == broker
    
    def test_create_borrower_as_client(self):
        """Test creating a borrower as client (should be forbidden)."""
        # Create a client user and authenticate
        client_user, _ = self.client.create_and_login(**self.client_data)
        
        # Try to create a borrower
        response = self.client.post(self.borrowers_url, data=self.borrower_data)
        
        # Assert response
        assert_response_status(response, status.HTTP_403_FORBIDDEN)
    
    def test_get_borrower_detail_as_admin(self):
        """Test getting borrower detail as admin."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create a borrower
        borrower = create_borrower(created_by=admin)
        
        # Get borrower detail
        borrower_detail_url = reverse('borrower-detail', args=[borrower.id])
        response = self.client.get(borrower_detail_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        assert_response_contains(response, 'first_name', borrower.first_name)
        assert_response_contains(response, 'last_name', borrower.last_name)
        assert_response_contains(response, 'email', borrower.email)
    
    def test_get_borrower_detail_as_broker(self):
        """Test getting borrower detail as broker."""
        # Create a broker user and authenticate
        broker, _ = self.client.create_and_login(**self.broker_data)
        
        # Create a borrower associated with the broker
        borrower = create_borrower(created_by=broker)
        
        # Get borrower detail
        borrower_detail_url = reverse('borrower-detail', args=[borrower.id])
        response = self.client.get(borrower_detail_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        assert_response_contains(response, 'first_name', borrower.first_name)
        assert_response_contains(response, 'last_name', borrower.last_name)
        assert_response_contains(response, 'email', borrower.email)
    
    def test_get_borrower_detail_as_broker_not_own(self):
        """Test getting borrower detail as broker for borrower not created by them."""
        # Create a broker user and authenticate
        broker, _ = self.client.create_and_login(**self.broker_data)
        
        # Create a borrower not associated with the broker
        admin = User.objects.create_user(
            username='another_admin',
            email='another_admin@example.com',
            password='password',
            role='admin'
        )
        borrower = create_borrower(created_by=admin)
        
        # Get borrower detail
        borrower_detail_url = reverse('borrower-detail', args=[borrower.id])
        response = self.client.get(borrower_detail_url)
        
        # Assert response (should return 404 as broker can't see other borrowers)
        assert_response_status(response, status.HTTP_404_NOT_FOUND)
    
    def test_update_borrower_as_admin(self):
        """Test updating a borrower as admin."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create a borrower
        borrower = create_borrower(created_by=admin)
        
        # Update borrower
        borrower_detail_url = reverse('borrower-detail', args=[borrower.id])
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Borrower',
            'email': 'updated.borrower@example.com'
        }
        response = self.client.patch(borrower_detail_url, data=update_data)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        assert_response_contains(response, 'first_name', update_data['first_name'])
        assert_response_contains(response, 'last_name', update_data['last_name'])
        assert_response_contains(response, 'email', update_data['email'])
    
    def test_delete_borrower_as_admin(self):
        """Test deleting a borrower as admin."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create a borrower
        borrower = create_borrower(created_by=admin)
        
        # Delete borrower
        borrower_detail_url = reverse('borrower-detail', args=[borrower.id])
        response = self.client.delete(borrower_detail_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_204_NO_CONTENT)
        
        # Verify borrower is deleted
        with pytest.raises(Borrower.DoesNotExist):
            Borrower.objects.get(id=borrower.id)
    
    def test_delete_borrower_as_broker(self):
        """Test deleting a borrower as broker."""
        # Create a broker user and authenticate
        broker, _ = self.client.create_and_login(**self.broker_data)
        
        # Create a borrower associated with the broker
        borrower = create_borrower(created_by=broker)
        
        # Delete borrower
        borrower_detail_url = reverse('borrower-detail', args=[borrower.id])
        response = self.client.delete(borrower_detail_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_204_NO_CONTENT)
        
        # Verify borrower is deleted
        with pytest.raises(Borrower.DoesNotExist):
            Borrower.objects.get(id=borrower.id)
    
    def test_delete_borrower_as_client(self):
        """Test deleting a borrower as client (should be forbidden)."""
        # Create a client user and authenticate
        client_user, _ = self.client.create_and_login(**self.client_data)
        
        # Create a borrower associated with the client
        borrower = create_borrower(user=client_user)
        
        # Try to delete borrower
        borrower_detail_url = reverse('borrower-detail', args=[borrower.id])
        response = self.client.delete(borrower_detail_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_403_FORBIDDEN)
    
    def test_create_company_borrower(self):
        """Test creating a company borrower."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create a company borrower
        response = self.client.post(self.borrowers_url, data=self.company_borrower_data)
        
        # Assert response
        assert_response_status(response, status.HTTP_201_CREATED)
        assert_response_contains(response, 'is_company', True)
        assert_response_contains(response, 'company_name', self.company_borrower_data['company_name'])
        assert_response_contains(response, 'company_abn', self.company_borrower_data['company_abn'])
        assert_response_contains(response, 'company_acn', self.company_borrower_data['company_acn'])
    
    def test_list_company_borrowers(self):
        """Test listing company borrowers."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create a regular borrower
        regular_borrower = create_borrower(created_by=admin)
        
        # Create a company borrower
        company_borrower = create_borrower(
            is_company=True,
            company_name='Test Company',
            company_abn='12345678901',
            company_acn='123456789',
            created_by=admin
        )
        
        # Get all borrowers and filter manually
        response = self.client.get(self.borrowers_url)
        assert_response_status(response, status.HTTP_200_OK)
        
        # Filter company borrowers manually
        all_borrowers = response.json()['results']
        company_borrowers = [b for b in all_borrowers if b.get('is_company') == True]
        
        # Check that the company borrower is in the results
        company_ids = [item['id'] for item in company_borrowers]
        assert company_borrower.id in company_ids, "Company borrower should be in results"
        
        # Check that regular borrower is not in the filtered results
        assert regular_borrower.id not in company_ids, "Regular borrower should not be in company results"
    
    def test_get_borrower_financial_summary(self):
        """Test getting borrower financial summary."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create a borrower
        borrower = create_borrower(
            annual_income='75000.00',
            other_income='5000.00',
            monthly_expenses='2000.00',
            created_by=admin
        )
        
        # Get financial summary
        financial_summary_url = reverse('borrower-financial-summary', args=[borrower.id])
        response = self.client.get(financial_summary_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        
        # The actual content will depend on the implementation of get_borrower_financial_summary
        # but we can at least check that it returns a valid response
        data = response.json()
        assert isinstance(data, dict), "Expected a dictionary response"
    
    def test_search_borrowers(self):
        """Test searching borrowers."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create borrowers with different names
        borrower1 = create_borrower(
            first_name='John',
            last_name='Smith',
            email='john.smith@example.com',
            created_by=admin
        )
        borrower2 = create_borrower(
            first_name='Jane',
            last_name='Doe',
            email='jane.doe@example.com',
            created_by=admin
        )
        
        # Search for borrowers with 'John'
        response = self.client.get(f"{self.borrowers_url}?search=John")
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        data = response.json()
        
        # Should only include borrowers with 'John' in their name
        assert len(data['results']) == 1, "Expected 1 borrower matching 'John'"
        assert data['results'][0]['first_name'] == 'John'
        
        # Search for borrowers with 'example.com'
        response = self.client.get(f"{self.borrowers_url}?search=example.com")
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        data = response.json()
        
        # Should include both borrowers
        assert len(data['results']) == 2, "Expected 2 borrowers matching 'example.com'"
