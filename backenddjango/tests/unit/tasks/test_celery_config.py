"""
Tests for Celery configuration.
"""
import pytest
from crm_backend.celery import app as celery_app


@pytest.mark.task
def test_celery_app_configuration():
    """Test that the Celery app is properly configured."""
    # Check that the app name is set correctly
    assert celery_app.main == 'crm_backend'
    
    # Check that the namespace is set correctly
    assert celery_app.conf.namespace == 'CELERY'
    
    # Check that the beat schedule is configured
    assert 'check-stale-applications' in celery_app.conf.beat_schedule
    assert 'check-note-reminders' in celery_app.conf.beat_schedule
    assert 'check-repayment-reminders' in celery_app.conf.beat_schedule
    
    # Check that the tasks are correctly configured in the beat schedule
    assert celery_app.conf.beat_schedule['check-stale-applications']['task'] == 'applications.tasks.check_stale_applications'
    assert celery_app.conf.beat_schedule['check-note-reminders']['task'] == 'applications.tasks.check_note_reminders'
    assert celery_app.conf.beat_schedule['check-repayment-reminders']['task'] == 'applications.tasks.check_repayment_reminders'
    
    # Check that the schedules are set
    assert 'schedule' in celery_app.conf.beat_schedule['check-stale-applications']
    assert 'schedule' in celery_app.conf.beat_schedule['check-note-reminders']
    assert 'schedule' in celery_app.conf.beat_schedule['check-repayment-reminders']
