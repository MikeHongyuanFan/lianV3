from rest_framework import serializers
from .models import User, Notification, NotificationPreference


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'phone']
        read_only_fields = ['id']


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating users
    """
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(required=False)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'role', 'phone', 'username']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        
        # Set username to email if not provided
        if 'username' not in validated_data or not validated_data['username']:
            validated_data['username'] = validated_data['email']
            
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        
        # Create default notification preferences for the user
        NotificationPreference.objects.create(user=user)
        
        return user


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification model
    """
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['created_at']


class NotificationListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing notifications
    """
    notification_type_display = serializers.CharField(source='get_notification_type_display', read_only=True)
    related_object_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'notification_type', 'notification_type_display', 
                  'is_read', 'created_at', 'related_object_id', 'related_object_type', 'related_object_info']
    
    def get_related_object_info(self, obj):
        """
        Get basic information about the related object if available
        """
        if not obj.related_object_id or not obj.related_object_type:
            return None
            
        # This could be expanded to include more object types and information
        if obj.related_object_type == 'application':
            try:
                from applications.models import Application
                from applications.serializers import ApplicationListSerializer
                
                application = Application.objects.filter(id=obj.related_object_id).first()
                if application:
                    return {
                        'id': application.id,
                        'reference': application.reference,
                        'status': application.status
                    }
            except ImportError:
                pass
                
        return {
            'id': obj.related_object_id,
            'type': obj.related_object_type
        }


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """
    Serializer for NotificationPreference model
    """
    class Meta:
        model = NotificationPreference
        exclude = ['user', 'created_at', 'updated_at']
        
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
