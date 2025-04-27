"""
Configuration for WebSocket integration tests.
This module configures Django settings for WebSocket tests to use PostgreSQL
and in-memory channel layers.
"""
import os
import pytest
from django.conf import settings


def pytest_configure(config):
    """Configure Django settings for WebSocket tests."""
    # Use PostgreSQL for WebSocket tests if available
    if os.environ.get('POSTGRES_TEST_DB'):
        settings.DATABASES["default"] = {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get('POSTGRES_TEST_DB', 'test_db'),
            "USER": os.environ.get('POSTGRES_TEST_USER', 'postgres'),
            "PASSWORD": os.environ.get('POSTGRES_TEST_PASSWORD', 'postgres'),
            "HOST": os.environ.get('POSTGRES_TEST_HOST', 'localhost'),
            "PORT": os.environ.get('POSTGRES_TEST_PORT', '5432'),
        }
    
    # Configure channel layers for testing
    settings.CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
        },
    }
