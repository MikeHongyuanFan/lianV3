from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for borrowers
borrower_router = DefaultRouter()
borrower_router.register('', views.BorrowerViewSet, basename='borrower')

# Create a separate router for guarantors
guarantor_router = DefaultRouter()
guarantor_router.register('', views.GuarantorViewSet, basename='guarantor')

urlpatterns = [
    # Include borrower routes at the root
    path('', include(borrower_router.urls)),
    
    # Include guarantor routes under /guarantors/
    path('guarantors/', include(guarantor_router.urls)),
    
    # Additional views
    path('company/', views.CompanyBorrowerListView.as_view(), name='company-borrower-list'),
    path('<int:pk>/financial-summary/', views.BorrowerFinancialSummaryView.as_view(), name='borrower-financial-summary'),
]
