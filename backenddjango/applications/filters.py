import django_filters
from django.db.models import Q
from .models import Application


class ApplicationFilter(django_filters.FilterSet):
    """
    Custom filter for applications with advanced filtering options
    """
    min_loan_amount = django_filters.NumberFilter(field_name="loan_amount", lookup_expr='gte')
    max_loan_amount = django_filters.NumberFilter(field_name="loan_amount", lookup_expr='lte')
    min_interest_rate = django_filters.NumberFilter(field_name="interest_rate", lookup_expr='gte')
    max_interest_rate = django_filters.NumberFilter(field_name="interest_rate", lookup_expr='lte')
    created_after = django_filters.DateFilter(field_name="created_at", lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name="created_at", lookup_expr='lte')
    search = django_filters.CharFilter(method='search_filter')
    
    class Meta:
        model = Application
        fields = [
            'stage', 'application_type', 'broker', 'bd', 'branch',
            'min_loan_amount', 'max_loan_amount', 'min_interest_rate', 
            'max_interest_rate', 'created_after', 'created_before',
            'repayment_frequency'
        ]
    
    def search_filter(self, queryset, name, value):
        """
        Search across multiple fields
        """
        return queryset.filter(
            Q(reference_number__icontains=value) |
            Q(purpose__icontains=value) |
            Q(broker__name__icontains=value) |
            Q(borrowers__first_name__icontains=value) |
            Q(borrowers__last_name__icontains=value) |
            Q(borrowers__email__icontains=value)
        ).distinct()
