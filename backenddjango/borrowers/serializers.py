from rest_framework import serializers
from .models import Borrower, Guarantor
from users.serializers import UserSerializer


class BorrowerListSerializer(serializers.ModelSerializer):
    """Serializer for listing borrowers with minimal information"""
    application_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Borrower
        fields = [
            'id', 'first_name', 'last_name', 'email', 
            'phone', 'created_at', 'application_count',
            'is_company', 'company_name'
        ]
    
    def get_application_count(self, obj):
        return obj.borrower_applications.count()


class BorrowerDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed borrower information"""
    created_by = UserSerializer(read_only=True)
    borrower_applications = serializers.SerializerMethodField()
    
    class Meta:
        model = Borrower
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by']
    
    def get_borrower_applications(self, obj):
        from applications.serializers import ApplicationListSerializer
        applications = obj.borrower_applications.all()
        return ApplicationListSerializer(applications, many=True).data
    
    def create(self, validated_data):
        # Set the created_by field to the current user
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)


class GuarantorSerializer(serializers.ModelSerializer):
    """Serializer for guarantor information"""
    created_by = UserSerializer(read_only=True)
    relationship_to_borrower = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    
    class Meta:
        model = Guarantor
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by']
    
    def create(self, validated_data):
        # Remove relationship_to_borrower if present as it's not in the model
        if 'relationship_to_borrower' in validated_data:
            validated_data.pop('relationship_to_borrower')
            
        # Set the created_by field to the current user
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)
    
    def validate(self, data):
        """
        Validate that the appropriate fields are provided based on guarantor type
        """
        guarantor_type = data.get('guarantor_type')
        
        if guarantor_type == 'individual':
            if not data.get('first_name') or not data.get('last_name'):
                raise serializers.ValidationError("First name and last name are required for individual guarantors")
        elif guarantor_type == 'company':
            if not data.get('company_name'):
                raise serializers.ValidationError("Company name is required for company guarantors")
        
        return data


class GuarantorDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed guarantor information"""
    created_by = UserSerializer(read_only=True)
    relationship_to_borrower = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    guaranteed_applications = serializers.SerializerMethodField()
    
    class Meta:
        model = Guarantor
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by']
    
    def get_guaranteed_applications(self, obj):
        from applications.serializers import ApplicationListSerializer
        applications = obj.guaranteed_applications.all()
        return ApplicationListSerializer(applications, many=True).data
