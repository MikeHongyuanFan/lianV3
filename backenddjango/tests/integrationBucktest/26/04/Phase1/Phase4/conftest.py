import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from borrowers.models import Borrower
from brokers.models import Broker
from applications.models import Application, Document, Fee, Repayment
from django.utils import timezone
from channels.testing import WebsocketCommunicator
from crm_backend.asgi import application as asgi_application
import json
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

@pytest.fixture
def admin_user(db):
    """Create an admin user for testing"""
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpassword',
        first_name='Admin',
        last_name='User',
        role='admin'
    )

@pytest.fixture
def broker_user(db):
    """Create a broker user for testing"""
    return User.objects.create_user(
        username='broker',
        email='broker@example.com',
        password='brokerpassword',
        first_name='Broker',
        last_name='User',
        role='broker'
    )

@pytest.fixture
def client_user(db):
    """Create a client user for testing"""
    return User.objects.create_user(
        username='client',
        email='client@example.com',
        password='clientpassword',
        first_name='Client',
        last_name='User',
        role='client'
    )

@pytest.fixture
def admin_client(admin_user):
    """Create an authenticated admin client"""
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client

@pytest.fixture
def broker_client(broker_user):
    """Create an authenticated broker client"""
    client = APIClient()
    client.force_authenticate(user=broker_user)
    return client

@pytest.fixture
def client_client(client_user):
    """Create an authenticated client client"""
    client = APIClient()
    client.force_authenticate(user=client_user)
    return client

@pytest.fixture
def broker_instance(db, broker_user):
    """Create a broker instance for testing"""
    return Broker.objects.create(
        user=broker_user,
        name='Test Broker',
        company='Test Broker Company',
        phone='1234567890',
        email='broker@example.com'
    )

@pytest.fixture
def borrower_instance(db, client_user):
    """Create a borrower instance for testing"""
    return Borrower.objects.create(
        user=client_user,
        first_name='John',
        last_name='Doe',
        email='john.doe@example.com',
        phone='1234567890',
        date_of_birth='1980-01-01',
        residential_address='123 Main St'
    )

@pytest.fixture
def application_instance(db, broker_instance):
    """Create an application instance for testing"""
    return Application.objects.create(
        application_type='residential',
        purpose='Home purchase',
        loan_amount=500000.00,
        loan_term=360,
        interest_rate=3.50,
        repayment_frequency='monthly',
        broker=broker_instance,
        stage='inquiry'
    )

@pytest.fixture
def application_instance_approved(db, broker_instance):
    """Create an approved application instance for testing"""
    return Application.objects.create(
        application_type='residential',
        purpose='Home purchase',
        loan_amount=600000.00,
        loan_term=360,
        interest_rate=3.25,
        repayment_frequency='monthly',
        broker=broker_instance,
        stage='approved'
    )

@pytest.fixture
def application_instance_rejected(db, broker_instance):
    """Create a rejected application instance for testing"""
    return Application.objects.create(
        application_type='commercial',
        purpose='Business loan',
        loan_amount=750000.00,
        loan_term=240,
        interest_rate=4.50,
        repayment_frequency='monthly',
        broker=broker_instance,
        stage='rejected'
    )

@pytest.fixture
def fee_instance(db, application_instance):
    """Create a fee instance for testing"""
    return Fee.objects.create(
        fee_type='application',
        description='Application fee',
        amount=1500.00,
        due_date=timezone.now().date(),
        application=application_instance
    )

@pytest.fixture
def repayment_instance(db, application_instance):
    """Create a repayment instance for testing"""
    return Repayment.objects.create(
        amount=2500.00,
        due_date=timezone.now().date(),
        application=application_instance
    )

@pytest.fixture
def repayment_instances(db, application_instance):
    """Create multiple repayment instances for testing"""
    repayments = []
    # Create 12 monthly repayments
    for i in range(12):
        due_date = timezone.now().date() + timezone.timedelta(days=30 * (i + 1))
        repayment = Repayment.objects.create(
            amount=2500.00,
            due_date=due_date,
            application=application_instance
        )
        repayments.append(repayment)
    return repayments

@pytest.fixture
def admin_token(admin_user):
    """Get JWT token for admin user"""
    refresh = RefreshToken.for_user(admin_user)
    return str(refresh.access_token)

@pytest.fixture
def broker_token(broker_user):
    """Get JWT token for broker user"""
    refresh = RefreshToken.for_user(broker_user)
    return str(refresh.access_token)

@pytest.fixture
def client_token(client_user):
    """Get JWT token for client user"""
    refresh = RefreshToken.for_user(client_user)
    return str(refresh.access_token)

@pytest.fixture
async def admin_communicator(admin_token):
    """Create a WebSocket communicator for admin user"""
    communicator = WebsocketCommunicator(
        asgi_application,
        f"ws/notifications/?token={admin_token}"  # Remove leading slash
    )
    connected, _ = await communicator.connect()
    if connected:
        yield communicator
        await communicator.disconnect()
    else:
        pytest.skip("Could not connect to WebSocket")

@pytest.fixture
async def broker_communicator(broker_token):
    """Create a WebSocket communicator for broker user"""
    communicator = WebsocketCommunicator(
        asgi_application,
        f"ws/notifications/?token={broker_token}"  # Remove leading slash
    )
    connected, _ = await communicator.connect()
    if connected:
        yield communicator
        await communicator.disconnect()
    else:
        pytest.skip("Could not connect to WebSocket")

@pytest.fixture
async def client_communicator(client_token):
    """Create a WebSocket communicator for client user"""
    communicator = WebsocketCommunicator(
        asgi_application,
        f"ws/notifications/?token={client_token}"  # Remove leading slash
    )
    connected, _ = await communicator.connect()
    if connected:
        yield communicator
        await communicator.disconnect()
    else:
        pytest.skip("Could not connect to WebSocket")
