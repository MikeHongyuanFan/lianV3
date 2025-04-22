from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'branches', views.BranchViewSet, basename='branches')
router.register(r'bdms', views.BDMViewSet, basename='bdms')
router.register(r'', views.BrokerViewSet, basename='broker')

urlpatterns = router.urls
