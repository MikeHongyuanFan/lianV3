# Celery Task Testing Infrastructure

This directory contains the test infrastructure for Celery tasks in the CRM Loan Management System.

## Overview

The task testing infrastructure is designed to test:

1. Basic task execution
2. Task scheduling
3. Task retry mechanisms
4. Task error handling
5. Integration with Django models

## Test Structure

- `conftest.py`: Contains pytest fixtures for Celery testing
- `test_celery_base.py`: Base class for Celery task tests
- `test_task_execution.py`: Tests for basic task execution
- `test_task_scheduling.py`: Tests for task scheduling
- `test_task_factories.py`: Factory methods for creating test data

## Running the Tests

To run the task tests, use the following command:

```bash
pytest tests/unit/tasks/ -v
```

To run tests with the `task` marker:

```bash
pytest -m task -v
```

## Test Configuration

The Celery test configuration is defined in `tests/celery_test_config.py`. This configuration:

- Uses an in-memory broker
- Sets `task_always_eager=True` to execute tasks synchronously
- Configures task time limits and retry settings

## Writing Task Tests

When writing tests for Celery tasks:

1. Use the `CeleryTestCase` base class or the `celery_app` fixture
2. Use the `@pytest.mark.task` decorator to mark task tests
3. Mock external dependencies like `send_mail`
4. Use the task factories to create test data

Example:

```python
@pytest.mark.task
@patch('applications.tasks.send_mail')
def test_my_task(mock_send_mail, celery_app):
    # Test setup
    data = TaskTestFactories.create_test_data()
    
    # Execute the task
    my_task()
    
    # Assertions
    assert mock_send_mail.called
    # Additional assertions...
```

## Coverage Goals

The goal for Sprint 3 is to achieve 30-50% test coverage for background tasks. This includes:

- Email notification tasks
- Document generation tasks
- Scheduled report generation tasks
