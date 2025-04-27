"""
Pytest configuration for unit tests.
"""
import pytest
import os
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from celery.contrib.testing.worker import start_worker
from celery.contrib.testing.app import TestApp

User = get_user_model()


@pytest.fixture
def api_client():
    """Return an API client for testing."""
    return APIClient()


@pytest.fixture
def admin_user():
    """Create and return an admin user."""
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
    """Create and return a broker user."""
    return User.objects.create_user(
        username='broker',
        email='broker@example.com',
        password='password123',
        role='broker'
    )


@pytest.fixture
def bd_user():
    """Create and return a business development user."""
    return User.objects.create_user(
        username='bd',
        email='bd@example.com',
        password='password123',
        role='bd'
    )


@pytest.fixture
def client_user():
    """Create and return a client user."""
    return User.objects.create_user(
        username='client',
        email='client@example.com',
        password='password123',
        role='client'
    )


@pytest.fixture
def temp_media_root(tmpdir, settings):
    """Create a temporary media root for testing file uploads."""
    settings.MEDIA_ROOT = tmpdir.strpath
    return settings.MEDIA_ROOT


@pytest.fixture(scope='session')
def celery_config():
    """Configure Celery for testing."""
    return {
        'broker_url': 'memory://',
        'result_backend': 'cache+memory://',
        'task_always_eager': True,
        'task_eager_propagates': True,
        'task_store_eager_result': True,
    }


@pytest.fixture(scope='session')
def celery_app():
    """Create a Celery test app."""
    from crm_backend.celery import app
    app.conf.update(
        task_always_eager=True,
        task_eager_propagates=True,
        broker_url='memory://',
        result_backend='cache+memory://',
        task_store_eager_result=True,
    )
    return app


@pytest.fixture(scope='session')
def celery_worker(celery_app):
    """Start a Celery worker for testing."""
    with start_worker(celery_app) as worker:
        yield worker


@pytest.fixture
def mock_websocket_layer():
    """Mock the WebSocket channel layer."""
    from unittest.mock import patch, MagicMock
    
    mock_layer = MagicMock()
    
    with patch('channels.layers.get_channel_layer', return_value=mock_layer):
        yield mock_layer
