from rest_framework import serializers
from .models import Broker, Branch, BDM
from users.serializers import UserSerializer


class BranchSerializer(serializers.ModelSerializer):
    """Serializer for branch information"""
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Branch
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by']
    
    def create(self, validated_data):
        # Set the created_by field to the current user
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)


class BrokerListSerializer(serializers.ModelSerializer):
    """Serializer for listing brokers with minimal information"""
    branch_name = serializers.SerializerMethodField()
    application_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Broker
        fields = [
            'id', 'name', 'company', 'email', 
            'phone', 'branch_name', 'application_count'
        ]
    
    def get_branch_name(self, obj):
        return obj.branch.name if obj.branch else None
    
    def get_application_count(self, obj):
        return obj.applications.count()


class BrokerDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed broker information"""
    branch = BranchSerializer(read_only=True)
    branch_id = serializers.PrimaryKeyRelatedField(
        queryset=Branch.objects.all(),
        source='branch',
        write_only=True,
        required=False,
        allow_null=True
    )
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Broker
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by']
    
    def create(self, validated_data):
        # Set the created_by field to the current user
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)


class BDMSerializer(serializers.ModelSerializer):
    """Serializer for BDM information"""
    branch = BranchSerializer(read_only=True)
    branch_id = serializers.PrimaryKeyRelatedField(
        queryset=Branch.objects.all(),
        source='branch',
        write_only=True,
        required=False,
        allow_null=True
    )
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = BDM
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by']
    
    def create(self, validated_data):
        # Set the created_by field to the current user
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)
