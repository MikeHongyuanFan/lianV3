from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Updated pattern to handle token authentication in the URL
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
]

