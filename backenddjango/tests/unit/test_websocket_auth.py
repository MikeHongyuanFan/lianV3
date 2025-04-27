"""
Custom authentication middleware for WebSocket tests.
"""

from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from channels.testing import WebsocketCommunicator

User = get_user_model()

class TestAuthMiddleware(BaseMiddleware):
    """
    Test-specific middleware that allows passing a user object directly in the scope.
    """
    async def __call__(self, scope, receive, send):
        # Get the user from the scope
        scope['user'] = scope.get('user', AnonymousUser())
        
        # Call the inner application
        return await self.inner(scope, receive, send)

def get_test_application(app):
    """
    Wrap the ASGI application with the test auth middleware.
    """
    return TestAuthMiddleware(app)

class AuthWebsocketCommunicator(WebsocketCommunicator):
    """
    WebSocket communicator that handles authentication for tests.
    """
    def __init__(self, application, path, user, subprotocols=None, headers=None):
        super().__init__(application, path, subprotocols, headers)
        self.scope["user"] = user
