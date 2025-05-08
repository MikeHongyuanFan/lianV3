import os
import tempfile
from unittest.mock import patch, MagicMock
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ...models import Application
from ...utils.pdf_filler import fill_pdf_form
from borrowers.models import Borrower
from users.models import User


class TestGenerateFilledFormAPI(TestCase):
    """
    Integration tests for the PDF generation API.
    """
    
    def setUp(self):
        """Set up test data."""
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            role='admin'
        )
        
        # Create a test borrower
        self.borrower = Borrower.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='1234567890',
            residential_address='123 Test St, Test City',
            annual_income=100000.00,
            created_by=self.user
        )
        
        # Create a test company borrower
        self.company_borrower = Borrower.objects.create(
            is_company=True,
            company_name='Test Company',
            company_abn='12345678901',
            company_acn='123456789',
            company_address='456 Business St, Test City',
            annual_company_income=500000.00,
            created_by=self.user
        )
        
        # Create a test application
        self.application = Application.objects.create(
            reference_number='APP-TEST123',
            loan_amount=250000.00,
            loan_term=24,
            interest_rate=5.5,
            loan_purpose='purchase',
            exit_strategy='sale',
            additional_comments='Test application',
            created_by=self.user
        )
        
        # Add borrowers to the application
        self.application.borrowers.add(self.borrower)
        
        # Set up the API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Create a temporary directory for test media files
        self.temp_dir = tempfile.TemporaryDirectory()
    
    def tearDown(self):
        """Clean up after tests."""
        self.temp_dir.cleanup()
    
    @patch('applications.views.pdf_generation.fill_pdf_form')
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_generate_filled_pdf_successfully(self, mock_fill_pdf):
        """Test successful PDF generation."""
        # Mock the fill_pdf_form function to return no missing fields
        mock_fill_pdf.return_value = []
        
        # Make the API request
        url = reverse('application-generate-pdf', args=[self.application.id])
        response = self.client.post(url)
        
        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('pdf_path', response.data)
        self.assertEqual(response.data['missing_fields'], [])
        
        # Check that the fill_pdf_form function was called with the correct arguments
        mock_fill_pdf.assert_called_once()
        args, _ = mock_fill_pdf.call_args
        self.assertEqual(args[0], self.application)
        self.assertTrue(args[1].endswith(f"{self.application.id}_filled.pdf"))
    
    @patch('applications.views.pdf_generation.fill_pdf_form')
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_generate_filled_pdf_with_missing_fields(self, mock_fill_pdf):
        """Test PDF generation with missing fields."""
        # Mock the fill_pdf_form function to return some missing fields
        missing_fields = ['company_abn', 'exit_strategy']
        mock_fill_pdf.return_value = missing_fields
        
        # Make the API request
        url = reverse('application-generate-pdf', args=[self.application.id])
        response = self.client.post(url)
        
        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('pdf_path', response.data)
        self.assertEqual(response.data['missing_fields'], missing_fields)
    
    @patch('applications.views.pdf_generation.fill_pdf_form')
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_strict_mode_rejects_incomplete_application(self, mock_fill_pdf):
        """Test strict mode rejection of incomplete applications."""
        # Mock the fill_pdf_form function to return some missing fields
        missing_fields = ['company_abn', 'exit_strategy']
        mock_fill_pdf.return_value = missing_fields
        
        # Make the API request with strict mode enabled
        url = reverse('application-generate-pdf', args=[self.application.id]) + '?strict=true'
        response = self.client.post(url)
        
        # Check the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn('missing_fields', response.data)
        self.assertEqual(response.data['missing_fields'], missing_fields)
    
    def test_nonexistent_application(self):
        """Test request for a non-existent application."""
        # Make the API request with a non-existent application ID
        url = reverse('application-generate-pdf', args=[99999])
        response = self.client.post(url)
        
        # Check the response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    @patch('applications.views.pdf_generation.fill_pdf_form')
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_file_not_found_error(self, mock_fill_pdf):
        """Test handling of FileNotFoundError."""
        # Mock the fill_pdf_form function to raise a FileNotFoundError
        mock_fill_pdf.side_effect = FileNotFoundError("PDF template not found")
        
        # Make the API request
        url = reverse('application-generate-pdf', args=[self.application.id])
        response = self.client.post(url)
        
        # Check the response
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'PDF template not found')
    
    @patch('applications.views.pdf_generation.fill_pdf_form')
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_general_exception(self, mock_fill_pdf):
        """Test handling of general exceptions."""
        # Mock the fill_pdf_form function to raise a general exception
        mock_fill_pdf.side_effect = Exception("Something went wrong")
        
        # Make the API request
        url = reverse('application-generate-pdf', args=[self.application.id])
        response = self.client.post(url)
        
        # Check the response
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', response.data)
        self.assertTrue(response.data['error'].startswith('Error generating PDF:'))
