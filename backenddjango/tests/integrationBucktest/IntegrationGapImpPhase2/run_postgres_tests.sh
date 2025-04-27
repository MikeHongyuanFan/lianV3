#!/bin/bash

# Set environment variables for the test
# These will make the tests run even without a real PostgreSQL instance
# since we're using the InMemoryChannelLayer
export POSTGRES_TEST_DB=test_db
export POSTGRES_TEST_USER=postgres
export POSTGRES_TEST_PASSWORD=postgres
export POSTGRES_TEST_HOST=localhost
export POSTGRES_TEST_PORT=5433

# Run the PostgreSQL WebSocket tests
echo "Running PostgreSQL WebSocket tests..."
python3 -m pytest test_websocket_postgres.py -v
