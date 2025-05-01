from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from documents.models import Document, Fee, Repayment
from applications.models import Application
from borrowers.models import Borrower
from brokers.models import Broker

User = get_user_model()


class DocumentAPIPermissionsTest(TestCase):
    """
    Test case for document API permissions
    """
    def setUp(self):
        # Create users with different roles
        self.admin_user = User.objects.create_user(
            email='admin@example.com',
            password='password123',
            role='admin'
        )
        self.broker_user = User.objects.create_user(
            email='broker@example.com',
            password='password123',
            role='broker'
        )
        self.bd_user = User.objects.create_user(
            email='bd@example.com',
            password='password123',
            role='bd'
        )
        self.client_user = User.objects.create_user(
            email='client@example.com',
            password='password123',
            role='client'
        )
        
        # Create broker profile
        self.broker = Broker.objects.create(
            user=self.broker_user,
            company_name="Test Broker Company"
        )
        
        # Create borrower
        self.borrower = Borrower.objects.create(
            user=self.client_user,
            first_name="John",
            last_name="Doe"
        )
        
        # Create application
        self.application = Application.objects.create(
            reference_number="APP-12345678",
            status="draft",
            bd=self.bd_user
        )
        self.application.borrowers.add(self.borrower)
        self.application.broker = self.broker
        self.application.save()
        
        # Create document
        self.document = Document.objects.create(
            title="Test Document",
            document_type="application_form",
            application=self.application,
            created_by=self.admin_user
        )
        
        # Create fee
        self.fee = Fee.objects.create(
            fee_type="application",
            amount=500.00,
            application=self.application,
            created_by=self.admin_user
        )
        
        # Create repayment
        self.repayment = Repayment.objects.create(
            amount=1000.00,
            application=self.application,
            created_by=self.admin_user
        )
        
        # Setup API client
        self.client = APIClient()
    
    def test_document_create_permissions(self):
        """
        Test that admin, broker, and BD users can create documents
        """
        url = reverse('document-list')
        data = {
            'title': 'New Document',
            'document_type': 'other',
            'application': self.application.id
        }
        
        # Test admin user
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Missing file
        
        # Test broker user
        self.client.force_authenticate(user=self.broker_user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Missing file
        
        # Test BD user
        self.client.force_authenticate(user=self.bd_user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Missing file
        
        # Test client user (should be forbidden)
        self.client.force_authenticate(user=self.client_user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_fee_mark_paid_permissions(self):
        """
        Test that only admin and BD users can mark fees as paid
        """
        url = reverse('fee-mark-paid', args=[self.fee.id])
        data = {}
        
        # Test admin user
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Reset fee paid_date
        self.fee.paid_date = None
        self.fee.save()
        
        # Test BD user
        self.client.force_authenticate(user=self.bd_user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Reset fee paid_date
        self.fee.paid_date = None
        self.fee.save()
        
        # Test broker user (should be forbidden)
        self.client.force_authenticate(user=self.broker_user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test client user (should be forbidden)
        self.client.force_authenticate(user=self.client_user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_repayment_mark_paid_permissions(self):
        """
        Test that only admin and BD users can mark repayments as paid
        """
        url = reverse('repayment-mark-paid', args=[self.repayment.id])
        data = {}
        
        # Test admin user
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Reset repayment paid_date
        self.repayment.paid_date = None
        self.repayment.save()
        
        # Test BD user
        self.client.force_authenticate(user=self.bd_user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Reset repayment paid_date
        self.repayment.paid_date = None
        self.repayment.save()
        
        # Test broker user (should be forbidden)
        self.client.force_authenticate(user=self.broker_user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test client user (should be forbidden)
        self.client.force_authenticate(user=self.client_user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)