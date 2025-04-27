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
    
    # Application guarantors
    path('<int:pk>/guarantors/', views.ApplicationViewSet.as_view({'get': 'guarantors'}), name='application-guarantors'),
    
    # Application notes
    path('<int:pk>/notes/', views.ApplicationViewSet.as_view({'get': 'notes'}), name='application-notes'),
    path('<int:pk>/add-note/', views.ApplicationViewSet.as_view({'post': 'add_note'}), name='application-add-note'),
    
    # Application documents
    path('<int:pk>/documents/', views.ApplicationViewSet.as_view({'get': 'documents'}), name='application-documents'),
    path('<int:pk>/upload-document/', views.ApplicationViewSet.as_view({'post': 'upload_document'}), name='application-upload-document'),
    
    # Application fees
    path('<int:pk>/fees/', views.ApplicationViewSet.as_view({'get': 'fees'}), name='application-fees'),
    path('<int:pk>/add-fee/', views.ApplicationViewSet.as_view({'post': 'add_fee'}), name='application-add-fee'),
    
    # Application repayments
    path('<int:pk>/repayments/', views.ApplicationViewSet.as_view({'get': 'repayments'}), name='application-repayments'),
    path('<int:pk>/add-repayment/', views.ApplicationViewSet.as_view({'post': 'add_repayment'}), name='application-add-repayment'),
    path('<int:pk>/record-payment/', views.ApplicationViewSet.as_view({'post': 'record_payment'}), name='application-record-payment'),
    
    # Application ledger
    path('<int:pk>/ledger/', views.ApplicationViewSet.as_view({'get': 'ledger'}), name='application-ledger'),
]
