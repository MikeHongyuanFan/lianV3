"""
Pytest configuration for integration tests.
"""
import pytest
from django.conf import settings

# Configure Django settings for tests
def pytest_configure():
    settings.DEBUG = False
    settings.CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
        },
    }
    
    # Use in-memory database for faster tests
    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
    
    # Disable logging during tests
    settings.LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
    }
