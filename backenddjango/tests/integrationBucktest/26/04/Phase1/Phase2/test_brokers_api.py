"""
Integration tests for brokers API endpoints.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from brokers.models import Broker
from .common import APITestClient, create_broker, create_branch, assert_response_status, assert_response_contains

User = get_user_model()

@pytest.mark.django_db
class TestBrokersAPI:
    """Test brokers API endpoints."""
    
    def setup_method(self):
        """Set up test client and data."""
        self.client = APITestClient()
        self.brokers_url = reverse('broker-list')
        
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
        
        self.bd_data = {
            'username': 'bd',
            'email': 'bd@example.com',
            'password': 'bdpassword',
            'role': 'bd'
        }
        
        # Test broker data
        self.test_broker_data = {
            'name': 'Test Broker',
            'company': 'Test Brokerage',
            'email': 'test.broker@example.com',
            'phone': '1234567890',
            'address': '123 Test St, Test City'
        }
    
    def test_list_brokers_as_admin(self):
        """Test listing brokers as admin."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create a broker
        broker = create_broker(created_by=admin)
        
        # List brokers
        response = self.client.get(self.brokers_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        data = response.json()
        assert len(data['results']) >= 1, "Expected at least 1 broker in the response"
        assert data['results'][0]['email'] == broker.email
    
    def test_list_brokers_as_broker(self):
        """Test listing brokers as broker."""
        # Create a broker user and authenticate
        broker_user, _ = self.client.create_and_login(**self.broker_data)
        
        # Create a broker profile associated with the user
        broker = create_broker(user=broker_user)
        
        # Create another broker not associated with the user
        admin = User.objects.create_user(
            username='another_admin',
            email='another_admin@example.com',
            password='password',
            role='admin'
        )
        other_broker = create_broker(
            name='Other Broker',
            email='other.broker@example.com',
            created_by=admin
        )
        
        # List brokers
        response = self.client.get(self.brokers_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        data = response.json()
        
        # Broker should only see their own profile
        assert len(data['results']) == 1, "Broker should only see their own profile"
        assert data['results'][0]['email'] == broker.email
    
    def test_create_broker_as_admin(self):
        """Test creating a broker as admin."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create a broker
        response = self.client.post(self.brokers_url, data=self.test_broker_data)
        
        # Assert response
        assert_response_status(response, status.HTTP_201_CREATED)
        assert_response_contains(response, 'name', self.test_broker_data['name'])
        assert_response_contains(response, 'company', self.test_broker_data['company'])
        assert_response_contains(response, 'email', self.test_broker_data['email'])
        
        # Verify broker was created
        broker_id = response.json()['id']
        broker = Broker.objects.get(id=broker_id)
        assert broker.created_by == admin
    
    def test_create_broker_as_broker(self):
        """Test creating a broker as broker (should be forbidden)."""
        # Create a broker user and authenticate
        broker_user, _ = self.client.create_and_login(**self.broker_data)
        
        # Try to create a broker
        response = self.client.post(self.brokers_url, data=self.test_broker_data)
        
        # Assert response
        assert_response_status(response, status.HTTP_403_FORBIDDEN)
    
    def test_get_broker_detail_as_admin(self):
        """Test getting broker detail as admin."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create a broker
        broker = create_broker(created_by=admin)
        
        # Get broker detail
        broker_detail_url = reverse('broker-detail', args=[broker.id])
        response = self.client.get(broker_detail_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        assert_response_contains(response, 'name', broker.name)
        assert_response_contains(response, 'email', broker.email)
    
    def test_get_broker_detail_as_broker(self):
        """Test getting broker detail as broker."""
        # Create a broker user and authenticate
        broker_user, _ = self.client.create_and_login(**self.broker_data)
        
        # Create a broker profile associated with the user
        broker = create_broker(user=broker_user)
        
        # Get broker detail
        broker_detail_url = reverse('broker-detail', args=[broker.id])
        response = self.client.get(broker_detail_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        assert_response_contains(response, 'name', broker.name)
        assert_response_contains(response, 'email', broker.email)
    
    def test_get_broker_detail_as_broker_not_own(self):
        """Test getting broker detail as broker for broker not associated with them."""
        # Create a broker user and authenticate
        broker_user, _ = self.client.create_and_login(**self.broker_data)
        
        # Create a broker profile associated with the user
        own_broker = create_broker(user=broker_user)
        
        # Create another broker not associated with the user
        admin = User.objects.create_user(
            username='another_admin',
            email='another_admin@example.com',
            password='password',
            role='admin'
        )
        other_broker = create_broker(
            name='Other Broker',
            email='other.broker@example.com',
            created_by=admin
        )
        
        # Get broker detail
        broker_detail_url = reverse('broker-detail', args=[other_broker.id])
        response = self.client.get(broker_detail_url)
        
        # Assert response (should return 404 as broker can't see other brokers)
        assert_response_status(response, status.HTTP_404_NOT_FOUND)
    
    def test_update_broker_as_admin(self):
        """Test updating a broker as admin."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create a broker
        broker = create_broker(created_by=admin)
        
        # Update broker
        broker_detail_url = reverse('broker-detail', args=[broker.id])
        update_data = {
            'name': 'Updated Broker',
            'company': 'Updated Brokerage',
            'email': 'updated.broker@example.com'
        }
        response = self.client.patch(broker_detail_url, data=update_data)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        assert_response_contains(response, 'name', update_data['name'])
        assert_response_contains(response, 'company', update_data['company'])
        assert_response_contains(response, 'email', update_data['email'])
    
    def test_update_broker_as_broker(self):
        """Test updating a broker as broker (should be forbidden)."""
        # Create a broker user and authenticate
        broker_user, _ = self.client.create_and_login(**self.broker_data)
        
        # Create a broker profile associated with the user
        broker = create_broker(user=broker_user)
        
        # Try to update broker
        broker_detail_url = reverse('broker-detail', args=[broker.id])
        update_data = {
            'name': 'Updated Broker',
            'company': 'Updated Brokerage',
            'email': 'updated.broker@example.com'
        }
        response = self.client.patch(broker_detail_url, data=update_data)
        
        # Assert response
        assert_response_status(response, status.HTTP_403_FORBIDDEN)
    
    def test_delete_broker_as_admin(self):
        """Test deleting a broker as admin."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create a broker
        broker = create_broker(created_by=admin)
        
        # Delete broker
        broker_detail_url = reverse('broker-detail', args=[broker.id])
        response = self.client.delete(broker_detail_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_204_NO_CONTENT)
        
        # Verify broker is deleted
        with pytest.raises(Broker.DoesNotExist):
            Broker.objects.get(id=broker.id)
    
    def test_delete_broker_as_broker(self):
        """Test deleting a broker as broker (should be forbidden)."""
        # Create a broker user and authenticate
        broker_user, _ = self.client.create_and_login(**self.broker_data)
        
        # Create a broker profile associated with the user
        broker = create_broker(user=broker_user)
        
        # Try to delete broker
        broker_detail_url = reverse('broker-detail', args=[broker.id])
        response = self.client.delete(broker_detail_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_403_FORBIDDEN)
    
    def test_search_brokers(self):
        """Test searching brokers."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create brokers with different names
        broker1 = create_broker(
            name='John Smith',
            company='ABC Brokerage',
            email='john.smith@example.com',
            created_by=admin
        )
        broker2 = create_broker(
            name='Jane Doe',
            company='XYZ Brokerage',
            email='jane.doe@example.com',
            created_by=admin
        )
        
        # Search for brokers with 'John'
        response = self.client.get(f"{self.brokers_url}?search=John")
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        data = response.json()
        
        # Should only include brokers with 'John' in their name
        assert len(data['results']) == 1, "Expected 1 broker matching 'John'"
        assert data['results'][0]['name'] == 'John Smith'
        
        # Search for brokers with 'Brokerage'
        response = self.client.get(f"{self.brokers_url}?search=Brokerage")
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        data = response.json()
        
        # Should include both brokers
        assert len(data['results']) == 2, "Expected 2 brokers matching 'Brokerage'"
    
    def test_get_broker_applications(self):
        """Test getting broker applications."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create a broker
        broker = create_broker(created_by=admin)
        
        # Get broker applications
        applications_url = reverse('broker-applications', args=[broker.id])
        response = self.client.get(applications_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        
        # The actual content will depend on whether the broker has any applications
        # but we can at least check that it returns a valid response
        data = response.json()
        assert isinstance(data, list), "Expected a list response"
    
    def test_get_broker_stats(self):
        """Test getting broker statistics."""
        # Create an admin user and authenticate
        admin, _ = self.client.create_and_login(**self.admin_data)
        
        # Create a broker
        broker = create_broker(created_by=admin)
        
        # Get broker statistics
        stats_url = reverse('broker-stats', args=[broker.id])
        response = self.client.get(stats_url)
        
        # Assert response
        assert_response_status(response, status.HTTP_200_OK)
        
        # Check that the response contains the expected fields
        data = response.json()
        assert 'total_applications' in data, "Expected 'total_applications' in response"
        assert 'total_loan_amount' in data, "Expected 'total_loan_amount' in response"
        assert 'applications_by_stage' in data, "Expected 'applications_by_stage' in response"
        assert 'applications_by_type' in data, "Expected 'applications_by_type' in response"
