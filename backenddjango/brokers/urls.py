from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create separate routers for each viewset
branch_router = DefaultRouter()
branch_router.register(r'', views.BranchViewSet)

bdm_router = DefaultRouter()
bdm_router.register(r'', views.BDMViewSet)

broker_router = DefaultRouter()
broker_router.register(r'', views.BrokerViewSet)

# Define URL patterns explicitly
urlpatterns = [
    path('branches/', include(branch_router.urls)),
    path('bdms/', include(bdm_router.urls)),
    path('', include(broker_router.urls)),
]
