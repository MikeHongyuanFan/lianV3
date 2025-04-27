from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'notifications', views.NotificationViewSet, basename='notifications')

urlpatterns = [
    # Authentication
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User profile
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('profile/update/', views.UserProfileUpdateView.as_view(), name='user-profile-update'),
    
    # Notifications
    path('notifications-list/', views.NotificationListView.as_view(), name='notification-list'),
    path('notifications-list/mark-read/', views.NotificationMarkReadView.as_view(), name='notification-mark-read'),
    path('notifications-list/count/', views.NotificationCountView.as_view(), name='notification-count'),
    path('notifications-list/search/', views.NotificationListView.as_view(), name='notification-search'),
    
    # Notification preferences
    path('notification-preferences/', views.NotificationPreferenceView.as_view(), name='notification-preferences'),
    
    # Include router URLs
    path('', include(router.urls)),
]
