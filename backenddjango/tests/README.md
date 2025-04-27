# Test Suite Documentation

This document provides an overview of the test infrastructure for the CRM Loan Management System.

## Test Structure

The test suite is organized into the following directories:

- `tests/unit/`: Unit tests for individual components
- `tests/integration/`: Integration tests for API endpoints and component interactions
- `tests/fixtures/`: Common test fixtures used across test types
- `tests/factories/`: Factory Boy factories for creating test objects

## Test Setup

### Prerequisites

Install the test dependencies:

```bash
pip install -r requirements-test.txt
```

### Configuration

The test suite uses pytest and pytest-django for running tests. Configuration is in `pytest.ini` at the project root.

## Running Tests

### Using the Test Runner Script

The `run_tests.sh` script provides a convenient way to run tests with coverage reporting:

```bash
# Run all tests
./tests/run_tests.sh all

# Run only unit tests
./tests/run_tests.sh unit

# Run only integration tests
./tests/run_tests.sh integration

# Run tests with verbose output
./tests/run_tests.sh all --verbose

# Run tests without generating HTML reports
./tests/run_tests.sh all --no-html
```

### Using pytest Directly

You can also run tests directly with pytest:

```bash
# Run all tests
pytest

# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run tests with coverage
pytest --cov=.

# Run tests with specific markers
pytest -m "model"
pytest -m "api"
pytest -m "service"
```

## Test Markers

The following markers are available for categorizing tests:

- `unit`: Unit tests
- `integration`: Integration tests
- `api`: Tests for API endpoints
- `model`: Tests for models
- `serializer`: Tests for serializers
- `service`: Tests for services
- `task`: Tests for background tasks
- `websocket`: Tests for WebSocket consumers

Example usage:

```python
import pytest

@pytest.mark.model
def test_application_model():
    # Test code here
    pass
```

## Test Factories

The test suite uses Factory Boy to create test objects. Factories are available for all major models:

```python
from tests.factories import (
    UserFactory, ApplicationFactory, BorrowerFactory,
    DocumentFactory, BrokerFactory
)

# Create a user
user = UserFactory()

# Create an application with a specific stage
application = ApplicationFactory(stage='assessment')

# Create a company borrower
company = CompanyBorrowerFactory()
```

## Test Fixtures

Common test fixtures are available in `tests/fixtures/common.py` and can be used in any test:

```python
def test_api_endpoint(authenticated_client, sample_application_data):
    # Test code using the fixtures
    response = authenticated_client.post('/api/applications/', sample_application_data)
    assert response.status_code == 201
```

## Coverage Reporting

The test suite generates coverage reports in HTML and XML formats. Coverage configuration is in `.coveragerc`.

To view the coverage report after running tests:

```bash
# Open the HTML coverage report
open coverage_reports/combined/index.html
```

## Continuous Integration

The test suite is integrated with GitHub Actions. The workflow configuration is in `.github/workflows/test.yml`.

The CI pipeline:
1. Sets up a PostgreSQL database and Redis instance
2. Installs dependencies
3. Runs unit and integration tests with coverage
4. Uploads coverage reports to Codecov

## Writing New Tests

### Unit Tests

Unit tests should be placed in `tests/unit/` and focus on testing individual components in isolation:

```python
# tests/unit/test_application_model.py
import pytest
from applications.models import Application

@pytest.mark.model
def test_application_str_representation():
    application = Application(reference_number="APP-001")
    assert str(application) == "APP-001"
```

### Integration Tests

Integration tests should be placed in `tests/integration/` and focus on testing component interactions:

```python
# tests/integration/test_application_api.py
import pytest
from rest_framework import status

@pytest.mark.api
def test_create_application(authenticated_client, sample_application_data):
    response = authenticated_client.post('/api/applications/', sample_application_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['reference_number'] == sample_application_data['reference_number']
```

## Implementation Progress

### Phase 1: Fix Existing Tests & Critical Infrastructure

#### Completed Tasks

1. ✅ Installed pytest and required dependencies
2. ✅ Fixed model test failures
3. ✅ Created proper test fixtures and utilities
4. ✅ Fixed missing model functionality
5. ✅ Set up Factory Boy factories for all models
6. ✅ Configured coverage reporting in CI

#### Current Test Coverage

- Unit test coverage: 57%
- Integration test coverage: 50%
- Combined coverage: 45%

### Next Steps

1. Add tests for WebSocket consumers
2. Add tests for critical authentication services
3. Begin Phase 2: Critical Gaps - Services & Tasks
