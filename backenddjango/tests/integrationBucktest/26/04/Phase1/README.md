# Phase 1: Authentication + Users APIs Integration Tests

This directory contains integration tests for the Authentication and Users APIs of the CRM Loan Management System.

## Test Files

- `common.py`: Shared utilities and helper functions for API testing
- `test_auth_api.py`: Tests for authentication endpoints (login, token refresh, etc.)
- `test_users_api.py`: Tests for user management endpoints (profile, CRUD operations)
- `test_notification_api.py`: Tests for notification endpoints (listing, marking as read, preferences)
- `test_websocket_api.py`: Tests for WebSocket connections and real-time notifications

## Running the Tests

To run all Phase 1 tests:

```bash
cd backenddjango
python -m pytest tests/integrationBucktest/Phase1 -v
```

To run a specific test file:

```bash
python -m pytest tests/integrationBucktest/Phase1/test_auth_api.py -v
```

To run with coverage:

```bash
coverage run -m pytest tests/integrationBucktest/Phase1
coverage report
coverage html
```

## Test Coverage

These tests cover:

1. **Authentication**
   - Login with valid and invalid credentials
   - Token refresh
   - Access to protected endpoints with and without authentication

2. **User Management**
   - User profile retrieval and updates
   - User listing, creation, updates, and deletion
   - Permission checks for different user roles

3. **Notifications**
   - Notification listing and filtering
   - Marking notifications as read
   - Notification preferences
   - Notification search functionality

4. **WebSockets**
   - WebSocket connection and authentication
   - Real-time notification delivery
   - Unread count updates

## Test Strategy

These tests follow the API-level integration testing strategy, focusing on:

- Testing actual API endpoints rather than internal implementations
- Verifying correct HTTP status codes and response data
- Testing both success paths and error cases
- Checking permission controls and authentication requirements
- Ensuring real-time functionality works as expected

This approach provides comprehensive coverage of the system's behavior from an end-user perspective while indirectly testing the underlying components.
