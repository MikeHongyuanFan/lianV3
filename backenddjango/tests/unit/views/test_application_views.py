import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from applications.models import Application
from applications.serializers import ApplicationDetailSerializer
from django.contrib.auth import get_user_model
from brokers.models import Broker, BDM
from borrowers.models import Borrower
import json

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

@pytest.mark.django_db
class TestApplicationViewSet:
    """Tests for the ApplicationViewSet"""
    
    def test_list_applications_admin(self, api_client, admin_user, application):
        """Admin should be able to see all applications"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('application-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['reference_number'] == application.reference_number
    
    def test_list_applications_broker(self, api_client, broker_user, application, broker):
        """Broker should only see their own applications"""
        api_client.force_authenticate(user=broker_user)
        url = reverse('application-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['reference_number'] == application.reference_number
        
        # Create another application with a different broker
        other_broker_user = User.objects.create_user(
            username='other_broker',
            email='other_broker@example.com',
            password='password123',
            role='broker'
        )
        other_broker = Broker.objects.create(
            user=other_broker_user,
            name="Other Broker",
            company="Other Broker Company"
        )
        Application.objects.create(
            reference_number="APP-002",
            application_type="residential",
            purpose="Refinance",
            loan_amount=300000,
            loan_term=15,
            repayment_frequency="monthly",
            broker=other_broker,
            bd=application.bd,
            stage="application_received"
        )
        
        # Broker should still only see their own application
        response = api_client.get(url)
        assert len(response.data['results']) == 1
    
    def test_list_applications_bd(self, api_client, bd_user, application, bdm):
        """BD should only see applications they're assigned to"""
        api_client.force_authenticate(user=bd_user)
        url = reverse('application-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['reference_number'] == application.reference_number
    
    def test_list_applications_client(self, api_client, client_user, application, borrower):
        """Client should only see applications they're associated with"""
        api_client.force_authenticate(user=client_user)
        url = reverse('application-list')
        
        # Initially client should see no applications
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 0
        
        # Add borrower to application
        application.borrowers.add(borrower)
        
        # Now client should see the application
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['reference_number'] == application.reference_number
    
    def test_retrieve_application(self, api_client, admin_user, application):
        """Should be able to retrieve a specific application"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('application-detail', kwargs={'pk': application.id})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['reference_number'] == application.reference_number
        assert float(response.data['loan_amount']) == application.loan_amount
    
    def test_create_application_broker(self, api_client, broker_user, broker, bdm):
        """Broker should be able to create an application"""
        api_client.force_authenticate(user=broker_user)
        url = reverse('application-list')
        
        data = {
            'reference_number': 'APP-003',
            'application_type': 'residential',
            'purpose': 'Purchase',
            'loan_amount': 400000,
            'loan_term': 25,
            'repayment_frequency': 'monthly',
            'broker': broker.id,
            'bd': bdm.id,
            'stage': 'inquiry'
        }
        
        response = api_client.post(url, data, format='json')
        
        # Print response data for debugging
        print(f"Response data: {response.data}")
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Application.objects.count() == 1
        assert Application.objects.get().reference_number == 'APP-003'
    
    def test_create_application_client_forbidden(self, api_client, client_user):
        """Client should not be able to create an application"""
        api_client.force_authenticate(user=client_user)
        url = reverse('application-list')
        
        data = {
            'reference_number': 'APP-004',
            'application_type': 'residential',
            'purpose': 'Purchase',
            'loan_amount': 400000,
            'loan_term': 25,
            'repayment_frequency': 'monthly',
            'stage': 'application_received'
        }
        
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Application.objects.count() == 0
    
    def test_update_application_broker(self, api_client, broker_user, application):
        """Broker should be able to update their application"""
        api_client.force_authenticate(user=broker_user)
        url = reverse('application-detail', kwargs={'pk': application.id})
        
        data = {
            'purpose': 'Refinance',
            'loan_amount': 450000
        }
        
        response = api_client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        
        application.refresh_from_db()
        assert application.purpose == 'Refinance'
        assert application.loan_amount == 450000
    
    def test_update_stage(self, api_client, admin_user, application):
        """Admin should be able to update application stage"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('application-update-stage', kwargs={'pk': application.id})
        
        data = {
            'stage': 'pre_approval'
        }
        
        response = api_client.post(url, data, format='json')
        
        # Print response data for debugging
        print(f"Response data: {response.data}")
        
        assert response.status_code == status.HTTP_200_OK
        
        application.refresh_from_db()
        assert application.stage == 'pre_approval'
    
    def test_add_note(self, api_client, admin_user, application):
        """Should be able to add a note to an application"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('application-add-note', kwargs={'pk': application.id})
        
        data = {
            'content': 'This is a test note'
        }
        
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        
        # Check that the note was created
        notes_url = reverse('application-notes', kwargs={'pk': application.id})
        notes_response = api_client.get(notes_url)
        
        assert notes_response.status_code == status.HTTP_200_OK
        assert len(notes_response.data) == 1
        assert notes_response.data[0]['content'] == 'This is a test note'
    
    def test_filter_applications(self, api_client, admin_user, application):
        """Should be able to filter applications"""
        api_client.force_authenticate(user=admin_user)
        
        # Create another application with different attributes
        Application.objects.create(
            reference_number="APP-005",
            application_type="commercial",
            purpose="Investment",
            loan_amount=1000000,
            loan_term=20,
            repayment_frequency="monthly",
            broker=application.broker,
            bd=application.bd,
            stage="application_received"
        )
        
        # Filter by application type
        url = reverse('application-list') + '?application_type=residential'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['reference_number'] == application.reference_number
        
        # Filter by loan amount greater than
        url = reverse('application-list') + '?loan_amount_min=600000'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['reference_number'] == "APP-005"
    
    def test_search_applications(self, api_client, admin_user, application):
        """Should be able to search applications"""
        api_client.force_authenticate(user=admin_user)
        
        # Create another application with different attributes
        Application.objects.create(
            reference_number="APP-006",
            application_type="residential",
            purpose="Home Renovation",
            loan_amount=200000,
            loan_term=10,
            repayment_frequency="monthly",
            broker=application.broker,
            bd=application.bd,
            stage="application_received"
        )
        
        # Search by purpose
        url = reverse('application-list') + '?search=renovation'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['reference_number'] == "APP-006"
