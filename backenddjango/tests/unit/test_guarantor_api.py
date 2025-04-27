import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from borrowers.models import Guarantor


@pytest.mark.django_db
class TestGuarantorAPI:
    """
    Test suite for Guarantor API endpoints
    """
    
    def test_list_guarantors(self, admin_user, guarantor_factory):
        """Test listing all guarantors."""
        # Create some guarantors
        guarantor_factory.create_batch(3)
        
        client = APIClient()
        client.force_authenticate(user=admin_user)
        
        # Use the correct URL pattern for guarantors list
        url = '/api/guarantors/'
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3
    
    def test_create_individual_guarantor(self, admin_user, individual_borrower):
        """Test creating an individual guarantor."""
        client = APIClient()
        client.force_authenticate(user=admin_user)
        
        url = '/api/guarantors/'
        data = {
            'guarantor_type': 'individual',
            'first_name': 'John',
            'last_name': 'Guarantor',
            'email': 'john.guarantor@example.com',
            'phone': '9876543210',
            'address': '456 Guarantor St',
            'borrower': individual_borrower.id
        }
        
        response = client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['first_name'] == 'John'
        assert response.data['last_name'] == 'Guarantor'
        assert response.data['guarantor_type'] == 'individual'
        
        # Verify guarantor was created in database
        guarantor = Guarantor.objects.get(id=response.data['id'])
        assert guarantor.first_name == 'John'
        assert guarantor.borrower.id == individual_borrower.id
    
    def test_create_company_guarantor(self, admin_user, company_borrower):
        """Test creating a company guarantor."""
        client = APIClient()
        client.force_authenticate(user=admin_user)
        
        url = '/api/guarantors/'
        data = {
            'guarantor_type': 'company',
            'company_name': 'Guarantor Corp',
            'company_abn': '98765432109',
            'company_acn': '987654321',
            'email': 'contact@guarantorcorp.com',
            'phone': '9876543210',
            'address': '789 Corporate Blvd',
            'borrower': company_borrower.id
        }
        
        response = client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['company_name'] == 'Guarantor Corp'
        assert response.data['guarantor_type'] == 'company'
        
        # Verify guarantor was created in database
        guarantor = Guarantor.objects.get(id=response.data['id'])
        assert guarantor.company_name == 'Guarantor Corp'
        assert guarantor.borrower.id == company_borrower.id
    
    def test_get_guarantor_detail(self, admin_user, guarantor_factory):
        """Test getting guarantor details."""
        guarantor = guarantor_factory.create(
            first_name='Jane',
            last_name='Guarantor',
            email='jane.guarantor@example.com'
        )
        
        client = APIClient()
        client.force_authenticate(user=admin_user)
        
        url = f'/api/guarantors/{guarantor.id}/'
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == 'Jane'
        assert response.data['last_name'] == 'Guarantor'
        assert response.data['email'] == 'jane.guarantor@example.com'
    
    def test_update_guarantor(self, admin_user, guarantor_factory):
        """Test updating a guarantor."""
        guarantor = guarantor_factory.create(
            first_name='Original',
            last_name='Name'
        )
        
        client = APIClient()
        client.force_authenticate(user=admin_user)
        
        url = f'/api/guarantors/{guarantor.id}/'
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com'
        }
        
        response = client.patch(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == 'Updated'
        assert response.data['email'] == 'updated@example.com'
        
        # Verify guarantor was updated in database
        guarantor.refresh_from_db()
        assert guarantor.first_name == 'Updated'
        assert guarantor.email == 'updated@example.com'
    
    def test_delete_guarantor(self, admin_user, guarantor_factory):
        """Test deleting a guarantor."""
        guarantor = guarantor_factory.create()
        
        client = APIClient()
        client.force_authenticate(user=admin_user)
        
        url = f'/api/guarantors/{guarantor.id}/'
        response = client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify guarantor was deleted from database
        assert not Guarantor.objects.filter(id=guarantor.id).exists()
    
    def test_filter_guarantors_by_borrower(self, admin_user, guarantor_factory, individual_borrower, company_borrower):
        """Test filtering guarantors by borrower."""
        # Create guarantors for different borrowers
        guarantor_factory.create_batch(2, borrower=individual_borrower)
        guarantor_factory.create(borrower=company_borrower)
        
        client = APIClient()
        client.force_authenticate(user=admin_user)
        
        url = f'/api/guarantors/?borrower={individual_borrower.id}'
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2
        for guarantor in response.data['results']:
            assert guarantor['borrower'] == individual_borrower.id
    
    def test_filter_guarantors_by_type(self, admin_user, guarantor_factory):
        """Test filtering guarantors by type."""
        # Create guarantors of different types
        guarantor_factory.create_batch(2, guarantor_type='individual')
        guarantor_factory.create(guarantor_type='company')
        
        client = APIClient()
        client.force_authenticate(user=admin_user)
        
        url = '/api/guarantors/?guarantor_type=individual'
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2
        for guarantor in response.data['results']:
            assert guarantor['guarantor_type'] == 'individual'
    
    def test_search_guarantors(self, admin_user, guarantor_factory):
        """Test searching guarantors."""
        guarantor_factory.create(first_name='John', last_name='Smith')
        guarantor_factory.create(first_name='Jane', last_name='Doe')
        guarantor_factory.create(company_name='ABC Company', guarantor_type='company')
        
        client = APIClient()
        client.force_authenticate(user=admin_user)
        
        url = '/api/guarantors/?search=john'
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['first_name'] == 'John'
        
        # Search for company name
        url = '/api/guarantors/?search=abc'
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['company_name'] == 'ABC Company'
        
    def test_filter_guarantors_by_application(self, admin_user, guarantor_factory, application):
        """Test filtering guarantors by application."""
        # Create guarantors for different applications
        guarantor_factory.create_batch(2, application=application)
        guarantor_factory.create()  # No application
        
        client = APIClient()
        client.force_authenticate(user=admin_user)
        
        url = f'/api/guarantors/?application={application.id}'
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2
        for guarantor in response.data['results']:
            assert guarantor['application'] == application.id
