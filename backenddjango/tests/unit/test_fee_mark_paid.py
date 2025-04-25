import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from documents.models import Fee, Ledger
from django.utils import timezone


@pytest.mark.django_db
class TestFeeMarkPaid:
    """
    Test suite for marking fees as paid
    """
    
    def test_mark_fee_as_paid(self, admin_user, fee_factory):
        """Test marking a fee as paid."""
        # Create a fee
        fee = fee_factory.create(paid_date=None)
        
        client = APIClient()
        client.force_authenticate(user=admin_user)
        
        url = reverse('fee-mark-paid', kwargs={'pk': fee.id})
        response = client.post(url, {})
        
        assert response.status_code == status.HTTP_200_OK
        assert 'fee_id' in response.data
        assert 'paid_date' in response.data
        assert 'status' in response.data
        assert response.data['status'] == 'paid'
        
        # Verify fee was updated in database
        fee.refresh_from_db()
        assert fee.paid_date is not None
        
        # Verify ledger entry was created
        ledger_entry = Ledger.objects.filter(
            related_fee=fee,
            transaction_type='fee_paid'
        ).first()
        
        assert ledger_entry is not None
        assert ledger_entry.amount == fee.amount
    
    def test_mark_fee_as_paid_with_custom_date(self, admin_user, fee_factory):
        """Test marking a fee as paid with a custom date."""
        # Create a fee
        fee = fee_factory.create(paid_date=None)
        
        client = APIClient()
        client.force_authenticate(user=admin_user)
        
        custom_date = '2025-03-15'
        url = reverse('fee-mark-paid', kwargs={'pk': fee.id})
        response = client.post(url, {'paid_date': custom_date})
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['paid_date'] == custom_date
        
        # Verify fee was updated in database
        fee.refresh_from_db()
        assert fee.paid_date.isoformat() == custom_date
    
    def test_mark_already_paid_fee(self, admin_user, fee_factory):
        """Test marking an already paid fee."""
        # Create a fee that's already paid
        yesterday = (timezone.now() - timezone.timedelta(days=1)).date()
        fee = fee_factory.create(paid_date=yesterday)
        
        client = APIClient()
        client.force_authenticate(user=admin_user)
        
        url = reverse('fee-mark-paid', kwargs={'pk': fee.id})
        response = client.post(url, {})
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'Fee already marked as paid'
        
        # Verify fee paid date wasn't changed
        fee.refresh_from_db()
        assert fee.paid_date == yesterday
    
    def test_mark_nonexistent_fee(self, admin_user):
        """Test marking a non-existent fee as paid."""
        client = APIClient()
        client.force_authenticate(user=admin_user)
        
        url = reverse('fee-mark-paid', kwargs={'pk': 9999})
        response = client.post(url, {})
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'error' in response.data
    
    def test_unauthorized_user(self, broker_user, fee_factory):
        """Test unauthorized user cannot mark fee as paid."""
        # Create a fee
        fee = fee_factory.create(paid_date=None)
        
        client = APIClient()
        client.force_authenticate(user=broker_user)
        
        url = reverse('fee-mark-paid', kwargs={'pk': fee.id})
        response = client.post(url, {})
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
