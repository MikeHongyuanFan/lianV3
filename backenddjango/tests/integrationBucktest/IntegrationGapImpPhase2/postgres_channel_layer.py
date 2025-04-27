"""
PostgreSQL channel layer configuration for testing.
"""
import os

# PostgreSQL channel layer configuration
POSTGRES_CHANNEL_LAYER = {
    "default": {
        "BACKEND": "channels_postgres.core.PostgresChannelLayer",
        "CONFIG": {
            "connection": {
                "host": os.environ.get('POSTGRES_TEST_HOST', 'localhost'),
                "port": int(os.environ.get('POSTGRES_TEST_PORT', '5433')),
                "database": os.environ.get('POSTGRES_TEST_DB', 'test_db'),
                "user": os.environ.get('POSTGRES_TEST_USER', 'postgres'),
                "password": os.environ.get('POSTGRES_TEST_PASSWORD', 'postgres'),
            }
        }
    }
}
