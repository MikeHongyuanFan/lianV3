"""
Tests for advanced filtering functionality.
"""
import pytest
from django.utils import timezone
from datetime import timedelta
from applications.filters import ApplicationFilter
from documents.filters import DocumentFilter, FeeFilter, RepaymentFilter
from users.filters import NotificationFilter
from applications.models import Application
from documents.models import Document, Fee, Repayment
from users.models import Notification
from tests.factories import (
    ApplicationFactory, DocumentFactory, FeeFactory, RepaymentFactory,
    NotificationFactory, BorrowerFactory, BrokerFactory, BDMFactory,
    AdminUserFactory
)

pytestmark = pytest.mark.django_db


@pytest.mark.filter
class TestApplicationAdvancedFilters:
    """Tests for advanced application filtering."""
    
    def test_combined_filters(self, admin_user):
        """Test combining multiple filters."""
        # Create test data
        app1 = ApplicationFactory(
            application_type='residential',
            loan_amount=500000,
            stage='inquiry',
            created_at=timezone.now() - timedelta(days=10)
        )
        
        app2 = ApplicationFactory(
            application_type='residential',
            loan_amount=700000,
            stage='assessment',
            created_at=timezone.now() - timedelta(days=5)
        )
        
        app3 = ApplicationFactory(
            application_type='commercial',
            loan_amount=1000000,
            stage='approved',
            created_at=timezone.now() - timedelta(days=2)
        )
        
        # Apply combined filters
        queryset = Application.objects.all()
        filterset = ApplicationFilter(
            data={
                'application_type': 'residential',
                'loan_amount_min': 600000,
                'created_after': (timezone.now() - timedelta(days=7)).date().isoformat()
            },
            queryset=queryset
        )
        
        # Check results
        filtered_apps = filterset.qs
        assert filtered_apps.count() == 1
        assert filtered_apps.first() == app2
    
    def test_date_range_filtering(self):
        """Test filtering by date range."""
        # Create test data with different dates
        today = timezone.now().date()
        
        app1 = ApplicationFactory(created_at=timezone.now() - timedelta(days=30))
        app2 = ApplicationFactory(created_at=timezone.now() - timedelta(days=15))
        app3 = ApplicationFactory(created_at=timezone.now() - timedelta(days=5))
        
        # Filter by date range
        queryset = Application.objects.all()
        filterset = ApplicationFilter(
            data={
                'created_after': (today - timedelta(days=20)).isoformat(),
                'created_before': (today - timedelta(days=10)).isoformat()
            },
            queryset=queryset
        )
        
        # Check results
        filtered_apps = filterset.qs
        assert filtered_apps.count() == 1
        assert filtered_apps.first() == app2
    
    def test_search_with_filters(self):
        """Test combining search with filters."""
        # Create test data
        borrower1 = BorrowerFactory(first_name="John", last_name="Smith")
        borrower2 = BorrowerFactory(first_name="Jane", last_name="Doe")
        
        app1 = ApplicationFactory(
            purpose="Home purchase",
            application_type="residential",
            loan_amount=500000
        )
        app1.borrowers.add(borrower1)
        
        app2 = ApplicationFactory(
            purpose="Investment property",
            application_type="residential",
            loan_amount=700000
        )
        app2.borrowers.add(borrower2)
        
        app3 = ApplicationFactory(
            purpose="Business expansion",
            application_type="commercial",
            loan_amount=1000000
        )
        
        # Apply search with filters
        queryset = Application.objects.all()
        filterset = ApplicationFilter(
            data={
                'search': 'Smith',
                'application_type': 'residential'
            },
            queryset=queryset
        )
        
        # Check results
        filtered_apps = filterset.qs
        assert filtered_apps.count() == 1
        assert filtered_apps.first() == app1


@pytest.mark.filter
class TestDocumentAdvancedFilters:
    """Tests for advanced document filtering."""
    
    def test_combined_document_filters(self):
        """Test combining multiple document filters."""
        # Create test data
        app1 = ApplicationFactory()
        app2 = ApplicationFactory()
        
        doc1 = DocumentFactory(
            application=app1,
            document_type='application_form',
            created_at=timezone.now() - timedelta(days=10),
            title="Application Form"
        )
        
        doc2 = DocumentFactory(
            application=app1,
            document_type='bank_statement',
            created_at=timezone.now() - timedelta(days=5),
            title="Bank Statement"
        )
        
        doc3 = DocumentFactory(
            application=app2,
            document_type='application_form',
            created_at=timezone.now() - timedelta(days=2),
            title="Application Form 2"
        )
        
        # Apply combined filters
        queryset = Document.objects.all()
        filterset = DocumentFilter(
            data={
                'document_type': 'application_form',
                'application': app1.id,
                'search': 'Form'
            },
            queryset=queryset
        )
        
        # Check results
        filtered_docs = filterset.qs
        assert filtered_docs.count() == 1
        assert filtered_docs.first() == doc1


@pytest.mark.filter
class TestFeeAdvancedFilters:
    """Tests for advanced fee filtering."""
    
    def test_fee_payment_status_filtering(self):
        """Test filtering fees by payment status."""
        # Create test data
        app = ApplicationFactory()
        
        # Paid fees
        fee1 = FeeFactory(
            application=app,
            fee_type='application',
            amount=1000,
            paid_date=timezone.now().date()
        )
        
        fee2 = FeeFactory(
            application=app,
            fee_type='valuation',
            amount=500,
            paid_date=timezone.now().date()
        )
        
        # Unpaid fees
        fee3 = FeeFactory(
            application=app,
            fee_type='legal',
            amount=1500,
            paid_date=None
        )
        
        # Filter by payment status
        queryset = Fee.objects.all()
        filterset = FeeFilter(
            data={'is_paid': 'true'},
            queryset=queryset
        )
        
        # Check results
        filtered_fees = filterset.qs
        assert filtered_fees.count() == 2
        assert fee1 in filtered_fees
        assert fee2 in filtered_fees
        assert fee3 not in filtered_fees
        
        # Filter for unpaid fees
        filterset = FeeFilter(
            data={'is_paid': 'false'},
            queryset=queryset
        )
        
        filtered_fees = filterset.qs
        assert filtered_fees.count() == 1
        assert fee3 in filtered_fees


@pytest.mark.filter
class TestNotificationAdvancedFilters:
    """Tests for advanced notification filtering."""
    
    def test_notification_complex_filtering(self, admin_user):
        """Test complex notification filtering."""
        # Create test data
        user = AdminUserFactory()
        
        # Create notifications with different types and dates
        notification1 = NotificationFactory(
            user=user,
            notification_type='application_status',
            title="Status Change",
            message="Application status changed",
            created_at=timezone.now() - timedelta(days=10),
            is_read=True
        )
        
        notification2 = NotificationFactory(
            user=user,
            notification_type='document_uploaded',
            title="Document Upload",
            message="New document uploaded",
            created_at=timezone.now() - timedelta(days=5),
            is_read=False
        )
        
        notification3 = NotificationFactory(
            user=user,
            notification_type='application_status',
            title="Another Status Change",
            message="Application status changed again",
            created_at=timezone.now() - timedelta(days=2),
            is_read=False
        )
        
        # Apply complex filters
        queryset = Notification.objects.filter(user=user)
        filterset = NotificationFilter(
            data={
                'notification_type': 'application_status',
                'is_read': 'false',
                'date_from': (timezone.now() - timedelta(days=7)).date().isoformat()
            },
            queryset=queryset
        )
        
        # Check results
        filtered_notifications = filterset.qs
        assert filtered_notifications.count() == 1
        assert filtered_notifications.first() == notification3
    
    def test_notification_search_performance(self):
        """Test notification search performance with large dataset."""
        # Create test data
        user = AdminUserFactory()
        
        # Create a large number of notifications
        for i in range(100):
            NotificationFactory(
                user=user,
                notification_type='application_status' if i % 2 == 0 else 'document_uploaded',
                title=f"Notification {i}",
                message=f"This is notification {i}",
                created_at=timezone.now() - timedelta(days=i % 30),
                is_read=i % 3 == 0
            )
        
        # Create a specific notification to search for
        target_notification = NotificationFactory(
            user=user,
            notification_type='application_status',
            title="Important Update",
            message="This is a very important update about your application",
            created_at=timezone.now() - timedelta(days=5),
            is_read=False
        )
        
        # Measure search performance
        import time
        start_time = time.time()
        
        queryset = Notification.objects.filter(user=user)
        filterset = NotificationFilter(
            data={'search': 'important update'},
            queryset=queryset
        )
        
        filtered_notifications = list(filterset.qs)
        end_time = time.time()
        
        # Check results
        assert len(filtered_notifications) == 1
        assert filtered_notifications[0] == target_notification
        
        # Check performance (should be under 100ms for this small dataset)
        assert (end_time - start_time) < 0.1
