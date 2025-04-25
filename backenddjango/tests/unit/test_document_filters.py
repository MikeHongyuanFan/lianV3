import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from documents.models import Document


@pytest.mark.django_db
class TestDocumentFilters:
    """
    Test suite for Document API filtering
    """
    
    def test_filter_documents_by_type(self, admin_user, document_factory):
        """Test filtering documents by document_type."""
        # Create documents with different types
        document_factory.create(document_type='application_form')
        document_factory.create(document_type='contract')
        document_factory.create(document_type='contract')
        document_factory.create(document_type='valuation_report')
        
        client = APIClient()
        client.force_authenticate(user=admin_user)
        
        url = reverse('document-list')
        response = client.get(f"{url}?document_type=contract")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2
        for doc in response.data['results']:
            assert doc['document_type'] == 'contract'
    
    def test_filter_documents_by_application(self, admin_user, document_factory, application):
        """Test filtering documents by application."""
        # Create another application
        from applications.models import Application
        another_app = Application.objects.create(
            reference_number='APP-TEST-002',
            stage='assessment',
            loan_amount=300000,
            loan_term=240,
            interest_rate=5.0,
            purpose='Investment',
            application_type='commercial',
            created_by=admin_user
        )
        
        # Create documents for different applications
        document_factory.create(application=application)
        document_factory.create(application=application)
        document_factory.create(application=another_app)
        
        client = APIClient()
        client.force_authenticate(user=admin_user)
        
        url = reverse('document-list')
        response = client.get(f"{url}?application={application.id}")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2
        for doc in response.data['results']:
            assert doc['application'] == application.id
    
    def test_search_documents(self, admin_user, document_factory):
        """Test searching documents."""
        document_factory.create(title='Loan Agreement', description='Standard loan agreement')
        document_factory.create(title='Property Valuation', description='Valuation report for property')
        document_factory.create(title='ID Verification', description='Customer identification document')
        
        client = APIClient()
        client.force_authenticate(user=admin_user)
        
        url = reverse('document-list')
        response = client.get(f"{url}?search=valuation")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert 'Valuation' in response.data['results'][0]['title']
    
    def test_filter_documents_by_date_range(self, admin_user, document_factory):
        """Test filtering documents by date range."""
        import datetime
        from django.utils import timezone
        
        # Create documents with different dates
        today = timezone.now()
        yesterday = today - datetime.timedelta(days=1)
        last_week = today - datetime.timedelta(days=7)
        
        document_factory.create(title='Recent Document')
        
        # Create a document with yesterday's date
        doc = document_factory.create(title='Yesterday Document')
        Document.objects.filter(id=doc.id).update(created_at=yesterday)
        
        # Create a document from last week
        doc = document_factory.create(title='Old Document')
        Document.objects.filter(id=doc.id).update(created_at=last_week)
        
        client = APIClient()
        client.force_authenticate(user=admin_user)
        
        url = reverse('document-list')
        yesterday_str = yesterday.strftime('%Y-%m-%d')
        tomorrow_str = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Filter documents created between yesterday and tomorrow (to include today)
        response = client.get(f"{url}?created_after={yesterday_str}&created_before={tomorrow_str}")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2  # Should include Recent and Yesterday documents
        
        # Verify the old document is not included
        titles = [doc['title'] for doc in response.data['results']]
        assert 'Old Document' not in titles
        assert 'Recent Document' in titles
        assert 'Yesterday Document' in titles
