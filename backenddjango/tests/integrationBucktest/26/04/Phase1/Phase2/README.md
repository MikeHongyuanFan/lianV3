# Phase 2: Borrowers + Brokers APIs Integration Tests

This directory contains integration tests for the Borrowers and Brokers APIs of the CRM Loan Management System.

## Test Files

- `common.py`: Shared utilities and helper functions for API testing
- `test_borrowers_api.py`: Tests for borrower management endpoints
- `test_guarantors_api.py`: Tests for guarantor management endpoints
- `test_brokers_api.py`: Tests for broker management endpoints
- `test_branches_api.py`: Tests for branch management endpoints

## Running the Tests

To run all Phase 2 tests:

```bash
cd backenddjango
python -m pytest tests/integrationBucktest/Phase2 -v
```

To run a specific test file:

```bash
python -m pytest tests/integrationBucktest/Phase2/test_borrowers_api.py -v
```

To run with coverage:

```bash
coverage run -m pytest tests/integrationBucktest/Phase2
coverage report
coverage html
```

## Test Coverage

These tests cover:

1. **Borrowers Management**
   - Borrower creation, retrieval, update, and deletion
   - Borrower search and filtering
   - Borrower document association
   - Borrower validation

2. **Guarantors Management**
   - Guarantor creation, retrieval, update, and deletion
   - Guarantor association with borrowers
   - Guarantor validation

3. **Brokers Management**
   - Broker creation, retrieval, update, and deletion
   - Broker search and filtering
   - Broker application association
   - Broker permissions and access control

4. **Branches Management**
   - Branch creation, retrieval, update, and deletion
   - Branch association with brokers
   - Branch permissions and access control

## Test Strategy

These tests follow the API-level integration testing strategy, focusing on:

- Testing actual API endpoints rather than internal implementations
- Verifying correct HTTP status codes and response data
- Testing both success paths and error cases
- Checking permission controls and authentication requirements
- Ensuring data validation works as expected
