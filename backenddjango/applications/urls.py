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
]
