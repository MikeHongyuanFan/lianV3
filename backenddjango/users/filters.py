import django_filters
from django.db.models import Q
from .models import Notification


class NotificationFilter(django_filters.FilterSet):
    """
    Custom filter for notifications with advanced filtering options
    """
    date_from = django_filters.DateFilter(field_name="created_at", lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name="created_at", lookup_expr='lte')
    is_read = django_filters.BooleanFilter(field_name="is_read")
    notification_type = django_filters.CharFilter(field_name="notification_type")
    search = django_filters.CharFilter(method='search_filter')
    
    class Meta:
        model = Notification
        fields = [
            'notification_type', 'is_read', 'date_from', 'date_to',
            'related_object_type'
        ]
    
    def search_filter(self, queryset, name, value):
        """
        Search across multiple fields
        """
        return queryset.filter(
            Q(title__icontains=value) |
            Q(message__icontains=value)
        )
