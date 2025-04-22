from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', views.BorrowerViewSet)
router.register(r'guarantors', views.GuarantorViewSet)

urlpatterns = router.urls
