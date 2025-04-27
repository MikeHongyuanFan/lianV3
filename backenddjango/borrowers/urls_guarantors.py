from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for guarantors
router = DefaultRouter()
router.register('', views.GuarantorViewSet, basename='guarantor')

urlpatterns = router.urls
