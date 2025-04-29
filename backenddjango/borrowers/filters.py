import django_filters
from .models import Borrower, Guarantor


class BorrowerFilter(django_filters.FilterSet):
    """
    Filter for borrowers
    """
    created_at_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    is_company = django_filters.BooleanFilter(field_name='is_company')
    
    class Meta:
        model = Borrower
        fields = {
            'first_name': ['exact', 'icontains'],
            'last_name': ['exact', 'icontains'],
            'email': ['exact', 'icontains'],
            'phone': ['exact', 'icontains'],
            'company_name': ['exact', 'icontains'],
            'company_abn': ['exact', 'icontains'],
            'created_by': ['exact'],
        }


class GuarantorFilter(django_filters.FilterSet):
    """
    Filter for guarantors
    """
    created_at_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    guarantor_type = django_filters.ChoiceFilter(choices=Guarantor.GUARANTOR_TYPE_CHOICES)
    relationship_to_borrower = django_filters.ChoiceFilter(choices=Guarantor.RELATIONSHIP_CHOICES)
    
    class Meta:
        model = Guarantor
        fields = {
            'first_name': ['exact', 'icontains'],
            'last_name': ['exact', 'icontains'],
            'email': ['exact', 'icontains'],
            'phone': ['exact', 'icontains'],
            'company_name': ['exact', 'icontains'],
            'company_abn': ['exact', 'icontains'],
            'borrower': ['exact'],
            'application': ['exact'],
            'created_by': ['exact'],
        }
