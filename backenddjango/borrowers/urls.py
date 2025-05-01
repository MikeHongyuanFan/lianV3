from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', views.BorrowerViewSet)
router.register(r'guarantors', views.GuarantorViewSet)

# Get the URL patterns from the router
urlpatterns = router.urls

# Add additional URL patterns for views not handled by the router
urlpatterns += [
    # Company borrowers endpoint (Section 3 in documentation)
    path('company/', views.CompanyBorrowerListView.as_view(), name='company-borrower-list'),
    
    # Borrower financial summary endpoint (Section 4 in documentation)
    path('<int:pk>/financial-summary/', views.BorrowerFinancialSummaryView.as_view(), name='borrower-financial-summary'),
]
