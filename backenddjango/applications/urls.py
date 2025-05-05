from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'applications', views.ApplicationViewSet, basename='application')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Application creation with cascade
    path('create-with-cascade/', views.ApplicationViewSet.as_view({'post': 'create'}), name='application-list-create'),
    
    # Application validation
    path('validate-schema/', views.ApplicationViewSet.as_view({'post': 'validate_schema'}), name='validate-application-schema'),
    
    # Application signature
    path('<int:pk>/signature/', views.ApplicationViewSet.as_view({'post': 'signature'}), name='application-signature'),
    
    # Application stage update
    path('<int:pk>/stage/', views.ApplicationViewSet.as_view({'put': 'update_stage'}), name='application-stage-update'),
    
    # Application borrowers update
    path('<int:pk>/borrowers/', views.ApplicationViewSet.as_view({'put': 'borrowers'}), name='application-borrowers-update'),
    
    # Application sign
    path('<int:pk>/sign/', views.ApplicationViewSet.as_view({'post': 'sign'}), name='application-sign'),
    
    # Application loan extension
    path('<int:pk>/extend-loan/', views.ApplicationViewSet.as_view({'post': 'extend_loan'}), name='application-extend-loan'),
    
    # Funding calculation
    path('<int:pk>/funding-calculation/', views.ApplicationViewSet.as_view({'post': 'funding_calculation'}), name='application-funding-calculation'),
    
    # Funding calculation history
    path('<int:pk>/funding-calculation-history/', views.ApplicationViewSet.as_view({'get': 'funding_calculation_history'}), name='application-funding-calculation-history'),
]
