import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from borrowers.models import Guarantor
from applications.models import Application
from users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user():
    return User.objects.create_user(
        email='admin@example.com',
        password='password123',
        role='admin'
    )


@pytest.fixture
def guarantor(admin_user):
    return Guarantor.objects.create(
        guarantor_type='individual',
        first_name='John',
        last_name='Doe',
        email='john.doe@example.com',
        phone='0412345678',
        address='123 Test St, Sydney NSW 2000',
        created_by=admin_user
    )


@pytest.fixture
def application(admin_user):
    return Application.objects.create(
        loan_amount=500000,
        loan_term=360,
        interest_rate=3.5,
        purpose='Test application',
        created_by=admin_user
    )


@pytest.mark.django_db
def test_guaranteed_applications_endpoint(api_client, admin_user, guarantor, application):
    # Add the guarantor to the application
    application.guarantors.add(guarantor)
    
    # Authenticate as admin
    api_client.force_authenticate(user=admin_user)
    
    # Get the guaranteed applications for the guarantor
    url = reverse('guarantor-guaranteed-applications', kwargs={'pk': guarantor.id})
    response = api_client.get(url)
    
    # Check that the response is successful
    assert response.status_code == status.HTTP_200_OK
    
    # Check that the application is in the response
    assert len(response.data) == 1
    assert response.data[0]['id'] == application.id
    assert response.data[0]['reference_number'] == application.reference_number