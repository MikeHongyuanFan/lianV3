from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', views.BrokerViewSet)
router.register(r'bdms', views.BDMViewSet)
router.register(r'branches', views.BranchViewSet)

urlpatterns = router.urls
