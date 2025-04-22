# CRM Loan Management System Tests

This directory contains tests for the CRM Loan Management System.

## Test Structure

- `unit/`: Unit tests for individual components
- `integration/`: Integration tests for component interactions

## Running Tests

To run all tests:

```bash
cd backenddjango
python manage.py test tests
```

To run specific test categories:

```bash
# Run unit tests only
python manage.py test tests.unit

# Run integration tests only
python manage.py test tests.integration

# Run a specific test file
python manage.py test tests.unit.test_user_model
```

## Test Coverage

To generate a test coverage report:

```bash
pip install coverage
coverage run --source='.' manage.py test tests
coverage report
```

For an HTML report:

```bash
coverage html
```

Then open `htmlcov/index.html` in your browser.

## Test Categories

### Unit Tests

- `test_user_model.py`: Tests for the User model
- `test_permissions.py`: Tests for custom permissions
- `test_serializers.py`: Tests for serializers
- `test_models_phase1.py`: Tests for core models from Phase 1

### Integration Tests

- `test_auth_endpoints.py`: Tests for authentication endpoints
- `test_user_api.py`: Tests for the User API
- `test_role_based_access.py`: Tests for role-based access control
- `test_database_relationships.py`: Tests for database relationships

## Adding New Tests

When adding new tests:

1. Follow the naming convention: `test_*.py`
2. Place unit tests in the `unit/` directory
3. Place integration tests in the `integration/` directory
4. Update this README if adding new test categories
