# WebSocket Integration Tests

This directory contains integration tests for WebSocket and real-time features of the CRM Loan Management System.

## Test Structure

The tests are organized into the following files:

1. `websocket_test_config.py` - Configuration for WebSocket tests
2. `conftest.py` - Pytest fixtures and helpers for WebSocket tests
3. `test_websocket_auth.py` - Tests for WebSocket authentication
4. `test_realtime_notifications.py` - Tests for real-time notification delivery
5. `test_websocket_connection.py` - Tests for WebSocket connection management
6. `test_mock_websocket.py` - Mock-based tests for environments without PostgreSQL

## Running the Tests

### With PostgreSQL (Recommended)

To run the tests with PostgreSQL (recommended for WebSocket tests):

```bash
# Set environment variables for PostgreSQL connection
export POSTGRES_TEST_DB=test_db
export POSTGRES_TEST_USER=postgres
export POSTGRES_TEST_PASSWORD=postgres
export POSTGRES_TEST_HOST=localhost
export POSTGRES_TEST_PORT=5432

# Run the tests
python manage.py test tests.integrationBucktest.IntegrationGapImpPhase4
```

### Without PostgreSQL (Using Mocks)

If PostgreSQL is not available, you can run the mock-based tests:

```bash
python manage.py test tests.integrationBucktest.IntegrationGapImpPhase4.test_mock_websocket
```

## Test Coverage

These tests cover:

1. **WebSocket Authentication**
   - Token-based authentication
   - Invalid token handling
   - Missing token handling
   - Token expiration handling

2. **Real-time Notifications**
   - Notification delivery
   - Notification read status updates
   - Notification filtering
   - Multiple client support

3. **WebSocket Connection Management**
   - Connection establishment
   - Connection maintenance
   - Disconnection handling
   - Reconnection logic
   - Message handling

4. **Mock-based Testing**
   - Tests using mocks for environments without PostgreSQL
   - Consumer method testing with mocks

## Dependencies

- Django Channels
- Redis (for channel layers in production)
- PostgreSQL (recommended for tests)
- pytest-asyncio

## Notes

- The tests use an in-memory channel layer for testing
- Some tests require PostgreSQL due to SQLite locking issues with WebSockets
- Mock-based tests are provided as an alternative for environments without PostgreSQL
