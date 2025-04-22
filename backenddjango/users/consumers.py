import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
import jwt
from django.conf import settings

User = get_user_model()

class NotificationConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time notifications
    """
    async def connect(self):
        """
        Connect to the WebSocket
        """
        # Get token from query string
        token = self.scope['query_string'].decode().split('token=')[1].split('&')[0]
        
        # Authenticate user from token
        try:
            # Decode the token
            decoded_token = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"],
                options={"verify_signature": True}
            )
            
            # Get user from token
            user_id = decoded_token.get('user_id')
            if not user_id:
                await self.close()
                return
                
            # Get user from database
            self.user = await self.get_user(user_id)
            if not self.user:
                await self.close()
                return
                
            # Set the group name to the user's ID
            self.group_name = f"user_{self.user.id}_notifications"
            
            # Join the group
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            
            await self.accept()
            
            # Send initial unread count
            unread_count = await self.get_unread_count()
            await self.send(text_data=json.dumps({
                'type': 'unread_count',
                'count': unread_count
            }))
            
        except (InvalidToken, TokenError, jwt.PyJWTError, IndexError) as e:
            print(f"WebSocket authentication error: {str(e)}")
            await self.close()
            return

    async def disconnect(self, close_code):
        """
        Disconnect from the WebSocket
        """
        # Leave the group
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        """
        Receive message from WebSocket
        """
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'get_unread_count':
            unread_count = await self.get_unread_count()
            await self.send(text_data=json.dumps({
                'type': 'unread_count',
                'count': unread_count
            }))

    async def notification_message(self, event):
        """
        Receive notification from group and send to WebSocket
        """
        # Send the notification to the WebSocket
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': event['notification']
        }))
    
    async def notification_count(self, event):
        """
        Receive notification count update from group and send to WebSocket
        """
        # Send the count to the WebSocket
        await self.send(text_data=json.dumps({
            'type': 'unread_count',
            'count': event['count']
        }))
    
    @database_sync_to_async
    def get_unread_count(self):
        """
        Get the unread notification count for the user
        """
        return self.user.notifications.filter(is_read=False).count()
    @database_sync_to_async
    def get_user(self, user_id):
        """
        Get user from database
        """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

