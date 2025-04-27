import pytest
from django.urls import reverse
from rest_framework import status
from applications.models import Application
from borrowers.models import Borrower
from brokers.models import Broker
import json
from django.utils import timezone
import base64

@pytest.mark.django_db
class TestApplicationsAPI:
    """
    Test suite for Applications API
    """
    
    def test_list_applications_as_admin(self, admin_client):
        """Test listing applications as admin"""
        url = reverse('application-list')
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
    
    def test_list_applications_as_broker(self, broker_client, broker_user):
        """Test listing applications as broker"""
        url = reverse('application-list')
        response = broker_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
    
    def test_list_applications_as_client(self, client_client, client_user):
        """Test listing applications as client"""
        url = reverse('application-list')
        response = client_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
    
    def test_create_application_as_admin(self, admin_client, admin_user, broker_instance):
        """Test creating an application as admin"""
        url = reverse('application-list')
        data = {
            'application_type': 'residential',
            'purpose': 'Home purchase',
            'loan_amount': '500000.00',
            'loan_term': 360,
            'interest_rate': '3.50',
            'repayment_frequency': 'monthly',
            'broker': broker_instance.id
        }
        response = admin_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['application_type'] == 'residential'
        assert response.data['purpose'] == 'Home purchase'
        assert float(response.data['loan_amount']) == 500000.00
    
    def test_create_application_as_broker(self, broker_client, broker_user, broker_instance):
        """Test creating an application as broker"""
        url = reverse('application-list')
        data = {
            'application_type': 'commercial',
            'purpose': 'Business expansion',
            'loan_amount': '750000.00',
            'loan_term': 240,
            'interest_rate': '4.25',
            'repayment_frequency': 'monthly',
            'broker': broker_instance.id
        }
        response = broker_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['application_type'] == 'commercial'
        assert response.data['purpose'] == 'Business expansion'
        assert float(response.data['loan_amount']) == 750000.00
    
    def test_create_application_as_client(self, client_client, client_user):
        """Test creating an application as client (should be forbidden)"""
        url = reverse('application-list')
        data = {
            'application_type': 'residential',
            'purpose': 'Home purchase',
            'loan_amount': '500000.00',
            'loan_term': 360,
            'interest_rate': '3.50',
            'repayment_frequency': 'monthly'
        }
        response = client_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_get_application_detail_as_admin(self, admin_client, application_instance):
        """Test getting application detail as admin"""
        url = reverse('application-detail', kwargs={'pk': application_instance.id})
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == application_instance.id
        assert response.data['reference_number'] == application_instance.reference_number
    
    def test_update_application_as_admin(self, admin_client, application_instance):
        """Test updating an application as admin"""
        url = reverse('application-detail', kwargs={'pk': application_instance.id})
        data = {
            'purpose': 'Updated purpose',
            'loan_amount': '600000.00'
        }
        response = admin_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['purpose'] == 'Updated purpose'
        assert float(response.data['loan_amount']) == 600000.00
    
    def test_delete_application_as_admin(self, admin_client, application_instance):
        """Test deleting an application as admin"""
        url = reverse('application-detail', kwargs={'pk': application_instance.id})
        response = admin_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify it's deleted
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_application_stage(self, admin_client, application_instance):
        """Test updating application stage"""
        url = reverse('application-stage-update', kwargs={'pk': application_instance.id})
        data = {
            'stage': 'pre_approval'
        }
        response = admin_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['stage'] == 'pre_approval'
        
        # Update to next stage
        data = {
            'stage': 'valuation'
        }
        response = admin_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['stage'] == 'valuation'
    
    def test_search_applications(self, admin_client, application_instance):
        """Test searching applications"""
        # Search by reference number
        url = f"{reverse('application-list')}?search={application_instance.reference_number}"
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0
        assert response.data['results'][0]['id'] == application_instance.id
        
        # Search by purpose
        url = f"{reverse('application-list')}?search={application_instance.purpose}"
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0
    
    def test_filter_applications_by_stage(self, admin_client, application_instance):
        """Test filtering applications by stage"""
        url = f"{reverse('application-list')}?stage={application_instance.stage}"
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0
        assert response.data['results'][0]['stage'] == application_instance.stage
    
    def test_filter_applications_by_type(self, admin_client, application_instance):
        """Test filtering applications by type"""
        url = f"{reverse('application-list')}?application_type={application_instance.application_type}"
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0
        assert response.data['results'][0]['application_type'] == application_instance.application_type
    
    def test_application_signature_processing(self, admin_client, application_instance):
        """Test application signature processing"""
        url = reverse('application-sign', kwargs={'pk': application_instance.id})
        
        # Create a simple base64 signature
        signature_data = base64.b64encode(b'test signature data').decode('utf-8')
        
        data = {
            'signature': signature_data,
            'name': 'John Doe',
            'signature_date': str(timezone.now().date())
        }
        
        response = admin_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        
        # Verify signature was processed
        url = reverse('application-detail', kwargs={'pk': application_instance.id})
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['signed_by'] == 'John Doe'
        assert response.data['signature_date'] is not None
    
    def test_update_application_borrowers(self, admin_client, application_instance, borrower_instance):
        """Test updating application borrowers"""
        # First, add the borrower to the application directly
        application_instance.borrowers.add(borrower_instance)
        
        # Verify borrower was added
        url = reverse('application-detail', kwargs={'pk': application_instance.id})
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['borrowers']) > 0
        assert response.data['borrowers'][0]['id'] == borrower_instance.id
    
    def test_validate_application_schema(self, admin_client):
        """Test application schema validation"""
        url = reverse('validate-application-schema')
        
        # Valid data
        valid_data = {
            'application_type': 'residential',
            'purpose': 'Home purchase',
            'loan_amount': '500000.00',
            'loan_term': 360,
            'repayment_frequency': 'monthly'
        }
        response = admin_client.post(url, valid_data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['valid'] is True
        
        # Invalid data (missing required field)
        invalid_data = {
            'application_type': 'residential',
            'purpose': 'Home purchase',
            'loan_amount': '500000.00'
            # Missing loan_term and repayment_frequency
        }
        response = admin_client.post(url, invalid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['valid'] is False
