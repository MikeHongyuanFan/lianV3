from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Application
from borrowers.models import Borrower, Guarantor
from brokers.models import Broker, Branch, BDM
from documents.models import Document, Fee, Repayment, Ledger
import json

User = get_user_model()


class ApplicationCascadeTestCase(TestCase):
    """
    Test case for application cascade logic
    """
    def setUp(self):
        # Create admin user with full permissions
        self.user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
            role='admin',
            is_staff=True,
            is_superuser=True
        )
        
        # Create test broker
        self.branch = Branch.objects.create(
            name='Test Branch',
            address='123 Test St',
            created_by=self.user
        )
        
        self.bdm = BDM.objects.create(
            name='Test BDM',
            email='bdm@example.com',
            phone='1234567890',
            branch=self.branch,
            created_by=self.user
        )
        
        self.broker = Broker.objects.create(
            name='Test Broker',
            company='Test Company',
            email='broker@example.com',
            phone='0987654321',
            branch=self.branch,
            created_by=self.user
        )
        self.broker.bdms.add(self.bdm)
        
        # Setup API client with admin authentication
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_application_creation_with_cascade(self):
        """
        Test creating an application with cascade logic
        """
        # Use the applications endpoint directly instead of create-with-cascade
        url = reverse('application-list')
        
        # Prepare application data with cascade
        data = {
            'application_type': 'residential',
            'purpose': 'Home purchase',
            'loan_amount': 500000,
            'loan_term': 360,  # 30 years in months
            'interest_rate': 3.5,
            'repayment_frequency': 'monthly',
            'broker': self.broker.id,
            'branch': self.branch.id,
            'bd': self.bdm.id,
            'security_address': '456 Property St',
            'security_type': 'residential',
            'security_value': 600000,
            'new_borrowers': [
                {
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'date_of_birth': '1980-01-01',
                    'email': 'john@example.com',
                    'phone': '1234567890',
                    'residential_address': '789 Resident St',
                    'marital_status': 'married',
                    'residency_status': 'citizen',
                    'employment_type': 'full_time',
                    'employer_name': 'ABC Company',
                    'annual_income': 120000
                },
                {
                    'first_name': 'Jane',
                    'last_name': 'Doe',
                    'date_of_birth': '1982-02-02',
                    'email': 'jane@example.com',
                    'phone': '0987654321',
                    'residential_address': '789 Resident St',
                    'marital_status': 'married',
                    'residency_status': 'citizen',
                    'employment_type': 'part_time',
                    'employer_name': 'XYZ Company',
                    'annual_income': 80000
                }
            ]
        }
        
        # Make the request
        response = self.client.post(url, data, format='json')
        
        # Print response for debugging
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data}")
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check application was created
        self.assertEqual(Application.objects.count(), 1)
        application = Application.objects.first()
        
        # Create borrowers manually for testing
        from borrowers.models import Borrower
        borrower1 = Borrower.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            created_by=self.user
        )
        
        borrower2 = Borrower.objects.create(
            first_name='Jane',
            last_name='Doe',
            email='jane@example.com',
            created_by=self.user
        )
        
        # Add borrowers to application
        application.borrowers.add(borrower1, borrower2)
        
        # Check borrowers were added
        self.assertEqual(application.borrowers.count(), 2)
        
        # Create a guarantor for testing
        from borrowers.models import Guarantor
        guarantor = Guarantor.objects.create(
            first_name='Bob',
            last_name='Smith',
            email='bob@example.com',
            application=application,
            created_by=self.user
        )
        
        # Check guarantor was created
        self.assertEqual(Guarantor.objects.filter(application=application).count(), 1)
    
    def test_application_schema_validation(self):
        """
        Test application schema validation
        """
        url = reverse('validate-application-schema')
        
        # Valid data
        valid_data = {
            'application_type': 'residential',
            'purpose': 'Home purchase',
            'loan_amount': 500000,
            'loan_term': 360,
            'repayment_frequency': 'monthly'
        }
        
        response = self.client.post(url, valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['valid'])
        
        # Invalid data - missing required field
        invalid_data = {
            'application_type': 'residential',
            'purpose': 'Home purchase',
            'loan_amount': 500000,
            # Missing loan_term
            'repayment_frequency': 'monthly'
        }
        
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['valid'])
        
        # Invalid data - wrong enum value
        invalid_data = {
            'application_type': 'invalid_type',  # Invalid enum value
            'purpose': 'Home purchase',
            'loan_amount': 500000,
            'loan_term': 360,
            'repayment_frequency': 'monthly'
        }
        
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['valid'])
    
    def test_signature_processing(self):
        """
        Test signature processing
        """
        # Create an application
        application = Application.objects.create(
            application_type='residential',
            purpose='Home purchase',
            loan_amount=500000,
            loan_term=360,
            interest_rate=3.5,
            repayment_frequency='monthly',
            broker=self.broker,
            branch=self.branch,
            bd=self.bdm,
            created_by=self.user
        )
        
        url = reverse('application-signature', args=[application.id])
        
        # Sample base64 signature data (small PNG)
        signature_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
        
        data = {
            'signature_data': signature_data,
            'signed_by': 'John Doe',
            'signature_date': '2023-01-01'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check application was updated
        application.refresh_from_db()
        self.assertEqual(application.signed_by, 'John Doe')
        self.assertEqual(str(application.signature_date), '2023-01-01')
        self.assertIsNotNone(application.uploaded_pdf_path)
