"""
Integration tests for performance metrics and reporting.
"""
import pytest
import time
from django.urls import reverse
from rest_framework import status
import json
from datetime import datetime, timedelta
from django.utils import timezone

@pytest.mark.django_db
class TestPerformanceMetrics:
    """Test suite for performance metrics and reporting."""

    def test_report_generation_performance(self, admin_client, application_instance, 
                                          application_instance_approved, application_instance_rejected):
        """Test performance of report generation."""
        # Measure time to generate application status report
        url = reverse('application-status-report')
        start_time = time.time()
        response = admin_client.get(url)
        end_time = time.time()
        
        assert response.status_code == status.HTTP_200_OK
        
        # Report generation should be reasonably fast (under 1 second)
        generation_time = end_time - start_time
        assert generation_time < 1.0, f"Report generation took {generation_time} seconds, which exceeds the 1 second threshold"
        
        # Verify report data
        data = response.json()
        assert 'total_active' in data
        assert 'total_settled' in data
        assert 'total_declined' in data
        assert 'total_withdrawn' in data

    def test_large_dataset_report_performance(self, admin_client, application_instance):
        """Test report performance with a larger dataset."""
        from brokers.models import Broker
        from applications.models import Application
        
        broker = Broker.objects.first()
        
        # Create 10 applications with different stages
        stages = ['inquiry', 'pre_approval', 'valuation', 'formal_approval', 'declined']
        for i in range(10):
            Application.objects.create(
                application_type='residential',
                purpose=f'Test purpose {i}',
                loan_amount=100000.00 + (i * 10000),
                loan_term=360,
                interest_rate=3.5 + (i * 0.1),
                repayment_frequency='monthly',
                broker=broker,
                stage=stages[i % len(stages)]
            )
        
        # Measure time to generate application status report with larger dataset
        url = reverse('application-status-report')
        start_time = time.time()
        response = admin_client.get(url)
        end_time = time.time()
        
        assert response.status_code == status.HTTP_200_OK
        
        # Report generation should still be reasonably fast (under 2 seconds)
        generation_time = end_time - start_time
        assert generation_time < 2.0, f"Report generation with larger dataset took {generation_time} seconds, which exceeds the 2 second threshold"
        
        # Verify report data
        data = response.json()
        assert 'total_active' in data
        assert 'total_settled' in data
        assert 'total_declined' in data
        assert 'total_withdrawn' in data

    def test_application_volume_report_performance(self, admin_client, application_instance):
        """Test performance of application volume report."""
        # Set up date range for the report
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)
        
        # Measure time to generate application volume report
        url = reverse('application-volume-report')
        start_time = time.time()
        response = admin_client.get(url, {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        })
        end_time = time.time()
        
        assert response.status_code == status.HTTP_200_OK
        
        # Report generation should be reasonably fast (under 1 second)
        generation_time = end_time - start_time
        assert generation_time < 1.0, f"Application volume report generation took {generation_time} seconds, which exceeds the 1 second threshold"
        
        # Verify report data
        data = response.json()
        assert 'total_applications' in data
        assert 'total_loan_amount' in data
        assert 'average_loan_amount' in data
        assert 'stage_breakdown' in data
        assert 'time_breakdown' in data

    def test_repayment_compliance_report_performance(self, admin_client, application_instance):
        """Test performance of repayment compliance report."""
        # Create repayments directly without using the fixture that has the created_by field
        from applications.models import Repayment
        from django.utils import timezone
        
        # Create a few repayments for the application
        for i in range(3):
            due_date = timezone.now().date() + timezone.timedelta(days=30 * (i + 1))
            Repayment.objects.create(
                amount=2500.00,
                due_date=due_date,
                application=application_instance,
                # Skip created_by field if it's not in the model
            )
        
        # Measure time to generate repayment compliance report
        url = reverse('repayment-compliance-report')
        start_time = time.time()
        response = admin_client.get(url)
        end_time = time.time()
        
        assert response.status_code == status.HTTP_200_OK
        
        # Report generation should be reasonably fast (under 1 second)
        generation_time = end_time - start_time
        assert generation_time < 1.0, f"Repayment compliance report generation took {generation_time} seconds, which exceeds the 1 second threshold"
        
        # Verify report data
        data = response.json()
        assert 'total_repayments' in data
        assert 'paid_on_time' in data
        assert 'paid_late' in data
        assert 'missed' in data
        assert 'compliance_rate' in data
        assert 'total_amount_due' in data
        assert 'total_amount_paid' in data
        assert 'payment_rate' in data
        assert 'monthly_breakdown' in data

    def test_concurrent_report_access(self, admin_client):
        """Test concurrent access to reports."""
        import threading
        import queue
        
        results = queue.Queue()
        
        def make_request(url):
            start_time = time.time()
            response = admin_client.get(url)
            end_time = time.time()
            results.put((response.status_code, end_time - start_time))
        
        # Create threads for concurrent report access
        threads = []
        report_urls = [
            reverse('application-status-report'),
            reverse('application-volume-report'),
            reverse('repayment-compliance-report')
        ]
        
        for url in report_urls:
            thread = threading.Thread(target=make_request, args=(url,))
            threads.append(thread)
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check results
        while not results.empty():
            status_code, request_time = results.get()
            assert status_code == 200
            assert request_time < 2.0, f"Concurrent report request took {request_time} seconds, which exceeds the 2 second threshold"

    @pytest.mark.skip(reason="WebSocket connection issues need to be fixed first")
    def test_websocket_performance(self, admin_client, admin_user):
        """Test WebSocket performance for notifications."""
        import asyncio
        import time
        from channels.testing import WebsocketCommunicator
        from crm_backend.asgi import application as asgi_application
        from rest_framework_simplejwt.tokens import RefreshToken
        from users.models import Notification
        from asgiref.sync import sync_to_async
        
        async def test_websocket():
            # Get token for admin user
            refresh = RefreshToken.for_user(admin_user)
            token = str(refresh.access_token)
            
            # Connect to WebSocket
            start_time = time.time()
            communicator = WebsocketCommunicator(
                asgi_application,
                f"ws/notifications/?token={token}"  # Remove leading slash
            )
            connected, _ = await communicator.connect()
            connection_time = time.time() - start_time
            
            assert connected
            assert connection_time < 1.0, f"WebSocket connection took {connection_time} seconds, which exceeds the 1 second threshold"
            
            # Create a notification directly in the database
            @sync_to_async
            def create_notification():
                notification = Notification.objects.create(
                    user=admin_user,
                    title='Performance Test',
                    message='Testing WebSocket performance',
                    notification_type='system',
                    is_read=False
                )
                return notification.id
            
            # Measure time to receive notification via WebSocket
            notification_start = time.time()
            notification_id = await create_notification()
            
            # Wait for WebSocket message
            message = await communicator.receive_json_from(timeout=2)
            notification_time = time.time() - notification_start
            
            assert message['type'] == 'notification'
            assert message['notification']['title'] == 'Performance Test'
            assert notification_time < 1.0, f"WebSocket notification delivery took {notification_time} seconds, which exceeds the 1 second threshold"
            
            await communicator.disconnect()
        
        # Run the async test
        loop = asyncio.get_event_loop()
        loop.run_until_complete(test_websocket())
