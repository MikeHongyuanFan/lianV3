"""
WebSocket authentication middleware for JWT tokens.
"""
import logging
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger(__name__)

@database_sync_to_async
def get_user(token):
    """
    Get user from JWT token.
    """
    try:
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        return User.objects.get(id=user_id)
    except (TokenError, User.DoesNotExist, KeyError) as e:
        logger.error(f"Error authenticating WebSocket token: {str(e)}")
        return AnonymousUser()
    except Exception as e:
        logger.error(f"Unexpected error in WebSocket authentication: {str(e)}")
        return AnonymousUser()

class JWTAuthMiddleware:
    """
    Custom JWT authentication middleware for WebSockets.
    """
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        try:
            # Extract token from query string
            query_string = scope.get("query_string", b"").decode()
            params = parse_qs(query_string)
            token = params.get("token", [None])[0]
            
            # Authenticate user if token is provided
            if token:
                user = await get_user(token)
                scope['user'] = user
                logger.debug(f"WebSocket authenticated user: {user.username}")
            else:
                scope['user'] = AnonymousUser()
                logger.debug("WebSocket anonymous user (no token)")
        except Exception as e:
            logger.error(f"Error in WebSocket auth middleware: {str(e)}")
            scope['user'] = AnonymousUser()
        
        # Continue with the inner application
        return await self.inner(scope, receive, send)
