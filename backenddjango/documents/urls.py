from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', views.DocumentViewSet)
router.register(r'notes', views.NoteViewSet)
router.register(r'fees', views.FeeViewSet)
router.register(r'repayments', views.RepaymentViewSet)

urlpatterns = router.urls
