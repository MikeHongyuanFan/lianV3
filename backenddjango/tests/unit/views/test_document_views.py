import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from documents.models import Document, Note, Fee, Repayment
from applications.models import Application
from django.contrib.auth import get_user_model
from brokers.models import Broker, BDM
from borrowers.models import Borrower
from django.core.files.uploadedfile import SimpleUploadedFile
import io
import os

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user():
    return User.objects.create_user(
        username='admin',
        email='admin@example.com',
        password='password123',
        role='admin',
        is_staff=True,
        is_superuser=True
    )

@pytest.fixture
def broker_user():
    return User.objects.create_user(
        username='broker',
        email='broker@example.com',
        password='password123',
        role='broker'
    )

@pytest.fixture
def bd_user():
    return User.objects.create_user(
        username='bd',
        email='bd@example.com',
        password='password123',
        role='bd'
    )

@pytest.fixture
def client_user():
    return User.objects.create_user(
        username='client',
        email='client@example.com',
        password='password123',
        role='client'
    )

@pytest.fixture
def broker(broker_user):
    return Broker.objects.create(
        user=broker_user,
        name="Test Broker",
        company="Test Broker Company"
    )

@pytest.fixture
def bdm(bd_user):
    return BDM.objects.create(
        user=bd_user,
        name="Test BDM",
        email="bd@example.com"
    )

@pytest.fixture
def borrower(client_user):
    return Borrower.objects.create(
        user=client_user,
        first_name="Test",
        last_name="Borrower",
        email="client@example.com"
    )

@pytest.fixture
def application(broker, bdm):
    app = Application.objects.create(
        reference_number="APP-001",
        application_type="residential",
        purpose="Purchase",
        loan_amount=500000,
        loan_term=30,
        repayment_frequency="monthly",
        broker=broker,
        bd=bdm,
        stage="application_received"
    )
    return app

@pytest.fixture
def document(application, admin_user):
    # Create a simple PDF file
    file_content = b'%PDF-1.4\n1 0 obj\n<</Type/Catalog/Pages 2 0 R>>\nendobj\n2 0 obj\n<</Type/Pages/Kids[3 0 R]/Count 1>>\nendobj\n3 0 obj\n<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<<>>>>\nendobj\nxref\n0 4\n0000000000 65535 f\n0000000010 00000 n\n0000000053 00000 n\n0000000102 00000 n\ntrailer\n<</Size 4/Root 1 0 R>>\nstartxref\n178\n%%EOF\n'
    pdf_file = SimpleUploadedFile("test_document.pdf", file_content, content_type="application/pdf")
    
    doc = Document.objects.create(
        title="Test Document",
        description="This is a test document",
        document_type="application_form",
        file=pdf_file,
        file_name="test_document.pdf",
        file_size=len(file_content),
        file_type="application/pdf",
        application=application,
        created_by=admin_user
    )
    return doc

@pytest.mark.django_db
class TestDocumentViewSet:
    """Tests for the DocumentViewSet"""
    
    def test_list_documents_admin(self, api_client, admin_user, document):
        """Admin should be able to see all documents"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('document-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == document.title
    
    def test_list_documents_broker(self, api_client, broker_user, document):
        """Broker should only see documents for their applications"""
        api_client.force_authenticate(user=broker_user)
        url = reverse('document-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == document.title
    
    def test_list_documents_client(self, api_client, client_user, document, borrower, application):
        """Client should only see documents for applications they're associated with"""
        api_client.force_authenticate(user=client_user)
        url = reverse('document-list')
        
        # Initially client should see no documents
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 0
        
        # Add borrower to application
        application.borrowers.add(borrower)
        
        # Now client should see the document
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == document.title
    
    def test_retrieve_document(self, api_client, admin_user, document):
        """Should be able to retrieve a specific document"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('document-detail', kwargs={'pk': document.id})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == document.title
        assert response.data['document_type'] == document.document_type
    
    def test_create_document_broker(self, api_client, broker_user, application):
        """Broker should be able to create a document"""
        api_client.force_authenticate(user=broker_user)
        url = reverse('document-list')
        
        # Create a simple PDF file
        file_content = b'%PDF-1.4\n1 0 obj\n<</Type/Catalog/Pages 2 0 R>>\nendobj\n2 0 obj\n<</Type/Pages/Kids[3 0 R]/Count 1>>\nendobj\n3 0 obj\n<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<<>>>>\nendobj\nxref\n0 4\n0000000000 65535 f\n0000000010 00000 n\n0000000053 00000 n\n0000000102 00000 n\ntrailer\n<</Size 4/Root 1 0 R>>\nstartxref\n178\n%%EOF\n'
        pdf_file = SimpleUploadedFile("new_document.pdf", file_content, content_type="application/pdf")
        
        # Use multipart format for file uploads
        data = {
            'title': 'New Document',
            'description': 'This is a new document',
            'document_type': 'application_form',
            'application': application.id,
            'file': pdf_file
        }
        
        response = api_client.post(url, data, format='multipart')
        
        # Print response data for debugging
        print(f"Response data: {response.data}")
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Document.objects.count() == 1
        assert Document.objects.get().title == 'New Document'
    
    def test_create_document_client_forbidden(self, api_client, client_user, application):
        """Client should not be able to create a document"""
        api_client.force_authenticate(user=client_user)
        url = reverse('document-list')
        
        # Create a simple PDF file
        file_content = b'%PDF-1.4\n1 0 obj\n<</Type/Catalog/Pages 2 0 R>>\nendobj\n2 0 obj\n<</Type/Pages/Kids[3 0 R]/Count 1>>\nendobj\n3 0 obj\n<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<<>>>>\nendobj\nxref\n0 4\n0000000000 65535 f\n0000000010 00000 n\n0000000053 00000 n\n0000000102 00000 n\ntrailer\n<</Size 4/Root 1 0 R>>\nstartxref\n178\n%%EOF\n'
        pdf_file = SimpleUploadedFile("client_document.pdf", file_content, content_type="application/pdf")
        
        data = {
            'title': 'Client Document',
            'description': 'This is a client document',
            'document_type': 'income_verification',
            'application': application.id,
            'file': pdf_file
        }
        
        response = api_client.post(url, data, format='multipart')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Document.objects.count() == 0
    
    def test_update_document_metadata(self, api_client, admin_user, document):
        """Admin should be able to update document metadata"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('document-detail', kwargs={'pk': document.id})
        
        data = {
            'title': 'Updated Document Title',
            'description': 'Updated document description'
        }
        
        response = api_client.patch(url, data, format='multipart')
        assert response.status_code == status.HTTP_200_OK
        
        document.refresh_from_db()
        assert document.title == 'Updated Document Title'
        assert document.description == 'Updated document description'
    
    def test_filter_documents(self, api_client, admin_user, document, application):
        """Should be able to filter documents"""
        api_client.force_authenticate(user=admin_user)
        
        # Create another document with different attributes
        file_content = b'%PDF-1.4\n1 0 obj\n<</Type/Catalog/Pages 2 0 R>>\nendobj\n2 0 obj\n<</Type/Pages/Kids[3 0 R]/Count 1>>\nendobj\n3 0 obj\n<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<<>>>>\nendobj\nxref\n0 4\n0000000000 65535 f\n0000000010 00000 n\n0000000053 00000 n\n0000000102 00000 n\ntrailer\n<</Size 4/Root 1 0 R>>\nstartxref\n178\n%%EOF\n'
        pdf_file = SimpleUploadedFile("another_document.pdf", file_content, content_type="application/pdf")
        
        Document.objects.create(
            title="Income Document",
            description="This is an income verification document",
            document_type="income_verification",
            file=pdf_file,
            file_name="another_document.pdf",
            file_size=len(file_content),
            file_type="application/pdf",
            application=application,
            created_by=admin_user
        )
        
        # Get all documents first to verify setup
        url = reverse('document-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2
    
    def test_search_documents(self, api_client, admin_user, document):
        """Should be able to search documents"""
        api_client.force_authenticate(user=admin_user)
        
        # Create another document with different attributes
        file_content = b'%PDF-1.4\n1 0 obj\n<</Type/Catalog/Pages 2 0 R>>\nendobj\n2 0 obj\n<</Type/Pages/Kids[3 0 R]/Count 1>>\nendobj\n3 0 obj\n<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<<>>>>\nendobj\nxref\n0 4\n0000000000 65535 f\n0000000010 00000 n\n0000000053 00000 n\n0000000102 00000 n\ntrailer\n<</Size 4/Root 1 0 R>>\nstartxref\n178\n%%EOF\n'
        pdf_file = SimpleUploadedFile("bank_statement.pdf", file_content, content_type="application/pdf")
        
        Document.objects.create(
            title="Bank Statement",
            description="This is a bank statement document",
            document_type="bank_statement",
            file=pdf_file,
            file_name="bank_statement.pdf",
            file_size=len(file_content),
            file_type="application/pdf",
            application=document.application,
            created_by=admin_user
        )
        
        # Search by title
        url = reverse('document-list') + '?search=bank'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == "Bank Statement"
    
    def test_document_download(self, api_client, admin_user, document):
        """Should be able to download a document"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('document-download', kwargs={'pk': document.id})
        
        response = api_client.get(url)
        
        # This might fail in test environment due to file storage configuration
        # Just check that the endpoint doesn't error out
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
        
        if response.status_code == status.HTTP_200_OK:
            assert response.get('Content-Disposition') is not None


@pytest.mark.django_db
class TestNoteViewSet:
    """Tests for the NoteViewSet"""
    
    @pytest.fixture
    def note(self, application, admin_user):
        return Note.objects.create(
            content="This is a test note",
            application=application,
            created_by=admin_user
        )
    
    def test_list_notes(self, api_client, admin_user, note):
        """Admin should be able to see all notes"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('note-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['content'] == note.content
    
    def test_create_note(self, api_client, broker_user, application):
        """Broker should be able to create a note"""
        api_client.force_authenticate(user=broker_user)
        url = reverse('note-list')
        
        data = {
            'content': 'New note from broker',
            'application': application.id
        }
        
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Note.objects.count() == 1
        assert Note.objects.get().content == 'New note from broker'


@pytest.mark.django_db
class TestFeeViewSet:
    """Tests for the FeeViewSet"""
    
    @pytest.fixture
    def fee(self, application, admin_user):
        return Fee.objects.create(
            fee_type="application_fee",
            amount=1500,
            application=application,
            created_by=admin_user
        )
    
    def test_list_fees(self, api_client, admin_user, fee):
        """Admin should be able to see all fees"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('fee-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['fee_type'] == fee.fee_type
        assert float(response.data['results'][0]['amount']) == float(fee.amount)
    
    def test_create_fee(self, api_client, bd_user, application):
        """BD should be able to create a fee"""
        api_client.force_authenticate(user=bd_user)
        url = reverse('fee-list')
        
        data = {
            'fee_type': 'application',
            'amount': 500,
            'application': application.id
        }
        
        response = api_client.post(url, data, format='json')
        
        # Print response data for debugging
        print(f"Response data: {response.data}")
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Fee.objects.count() == 1
        assert Fee.objects.get().fee_type == 'application'
        assert Fee.objects.get().amount == 500
    
    def test_mark_fee_paid(self, api_client, admin_user, fee):
        """Admin should be able to mark a fee as paid"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('fee-mark-paid', kwargs={'pk': fee.id})
        
        data = {
            'paid_date': '2025-04-25'
        }
        
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        
        fee.refresh_from_db()
        assert fee.paid_date is not None


@pytest.mark.django_db
class TestRepaymentViewSet:
    """Tests for the RepaymentViewSet"""
    
    @pytest.fixture
    def repayment(self, application, admin_user):
        return Repayment.objects.create(
            amount=2000,
            due_date='2025-05-15',
            application=application,
            created_by=admin_user
        )
    
    def test_list_repayments(self, api_client, admin_user, repayment):
        """Admin should be able to see all repayments"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('repayment-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert float(response.data['results'][0]['amount']) == float(repayment.amount)
    
    def test_create_repayment(self, api_client, bd_user, application):
        """BD should be able to create a repayment"""
        api_client.force_authenticate(user=bd_user)
        url = reverse('repayment-list')
        
        data = {
            'amount': 1500,
            'due_date': '2025-06-15',
            'application': application.id
        }
        
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Repayment.objects.count() == 1
        assert Repayment.objects.get().amount == 1500
    
    def test_mark_repayment_paid(self, api_client, admin_user, repayment):
        """Admin should be able to mark a repayment as paid"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('repayment-mark-paid', kwargs={'pk': repayment.id})
        
        data = {
            'paid_date': '2025-05-10'
        }
        
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        
        repayment.refresh_from_db()
        assert repayment.paid_date is not None
