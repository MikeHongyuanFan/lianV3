import pytest
from django.urls import reverse
from rest_framework import status
from applications.models import Application, Fee, Repayment
from borrowers.models import Borrower, Guarantor
from brokers.models import Broker
from documents.models import Document, Note
import json
from django.utils import timezone

@pytest.mark.django_db
class TestApplicationRelationships:
    """
    Test suite for Application Relationships
    """
    
    def test_borrower_application_relationship(self, admin_client, application_instance, borrower_instance):
        """Test borrower-application relationship"""
        # Add borrower to application directly
        application_instance.borrowers.add(borrower_instance)
        
        # Verify borrower was added to application
        url = reverse('application-detail', kwargs={'pk': application_instance.id})
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['borrowers']) > 0
        assert response.data['borrowers'][0]['id'] == borrower_instance.id
        
        # Verify application appears in borrower's applications
        url = reverse('borrower-detail', kwargs={'pk': borrower_instance.id})
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'borrower_applications' in response.data
        assert len(response.data['borrower_applications']) > 0
        assert response.data['borrower_applications'][0]['id'] == application_instance.id
    
    def test_broker_application_relationship(self, admin_client, application_instance, broker_instance):
        """Test broker-application relationship"""
        # Update application to assign broker
        url = reverse('application-detail', kwargs={'pk': application_instance.id})
        data = {
            'broker': broker_instance.id
        }
        response = admin_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['broker']['id'] == broker_instance.id
        
        # Verify application appears in broker's applications
        url = reverse('broker-applications', kwargs={'pk': broker_instance.id})
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0
        assert response.data[0]['id'] == application_instance.id
    
    def test_fee_application_relationship(self, admin_client, application_instance):
        """Test fee-application relationship"""
        # Add fee to application
        url = reverse('application-add-fee', kwargs={'pk': application_instance.id})
        data = {
            'fee_type': 'application',
            'amount': '1500.00',
            'due_date': str(timezone.now().date())
        }
        response = admin_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        fee_id = response.data['id']
        
        # Verify fee was added to application
        url = reverse('application-fees', kwargs={'pk': application_instance.id})
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0
        assert response.data[0]['id'] == fee_id
        assert response.data[0]['fee_type'] == 'application'
        assert float(response.data[0]['amount']) == 1500.00
        
        # Verify fee has correct application reference
        url = reverse('fee-detail', kwargs={'pk': fee_id})
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['application'] == application_instance.id
    
    def test_document_application_relationship(self, admin_client, application_instance):
        """Test document-application relationship"""
        # Add document to application
        url = reverse('application-upload-document', kwargs={'pk': application_instance.id})
        
        # Create a simple text file for testing
        from django.core.files.uploadedfile import SimpleUploadedFile
        test_file = SimpleUploadedFile("test_document.txt", b"Test document content", content_type="text/plain")
        
        data = {
            'document_type': 'application_form',
            'description': 'Test document',
            'file': test_file
        }
        response = admin_client.post(url, data, format='multipart')
        assert response.status_code == status.HTTP_200_OK
        document_id = response.data['id']
        
        # Verify document was added to application
        url = reverse('application-documents', kwargs={'pk': application_instance.id})
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0
        assert response.data[0]['id'] == document_id
        assert response.data[0]['document_type'] == 'application_form'
        assert response.data[0]['description'] == 'Test document'
        
        # Verify document has correct application reference
        url = reverse('document-detail', kwargs={'pk': document_id})
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['application'] == application_instance.id
    
    def test_guarantor_application_relationship(self, admin_client, application_instance, guarantor_instance):
        """Test guarantor-application relationship"""
        # Add guarantor to application
        application_instance.guarantors.add(guarantor_instance)
        
        # Verify guarantor was added to application
        url = reverse('application-detail', kwargs={'pk': application_instance.id})
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'guarantors' in response.data
        assert len(response.data['guarantors']) > 0
        assert response.data['guarantors'][0]['id'] == guarantor_instance.id
        
        # Verify application appears in guarantor's applications
        url = reverse('guarantor-detail', kwargs={'pk': guarantor_instance.id})
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'guaranteed_applications' in response.data
        assert len(response.data['guaranteed_applications']) > 0
        assert response.data['guaranteed_applications'][0]['id'] == application_instance.id
    
    def test_note_application_relationship(self, admin_client, application_instance):
        """Test note-application relationship"""
        # Add note to application
        url = reverse('application-add-note', kwargs={'pk': application_instance.id})
        data = {
            'title': 'Test Note',
            'content': 'This is a test note for the application'
        }
        response = admin_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        note_id = response.data['id']
        
        # Verify note was added to application
        url = reverse('application-notes', kwargs={'pk': application_instance.id})
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0
        assert response.data[0]['id'] == note_id
        assert response.data[0]['title'] == 'Test Note'
        assert response.data[0]['content'] == 'This is a test note for the application'
        
        # Verify note has correct application reference
        url = reverse('note-detail', kwargs={'pk': note_id})
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['application'] == application_instance.id
    
    def test_repayment_application_relationship(self, admin_client, application_instance):
        """Test repayment-application relationship"""
        # Add repayment to application
        url = reverse('application-add-repayment', kwargs={'pk': application_instance.id})
        data = {
            'amount': '2500.00',
            'due_date': str(timezone.now().date())
        }
        response = admin_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        repayment_id = response.data['id']
        
        # Verify repayment was added to application
        url = reverse('application-repayments', kwargs={'pk': application_instance.id})
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0
        assert response.data[0]['id'] == repayment_id
        assert float(response.data[0]['amount']) == 2500.00
        
        # Verify repayment has correct application reference
        url = reverse('repayment-detail', kwargs={'pk': repayment_id})
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['application'] == application_instance.id
