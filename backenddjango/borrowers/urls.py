from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'borrowers', views.BorrowerViewSet, basename='borrower')
router.register(r'guarantors', views.GuarantorViewSet, basename='guarantor')

urlpatterns = router.urls

