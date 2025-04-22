from rest_framework import serializers
from .models import Application, Document, Fee, Repayment

class ApplicationListSerializer(serializers.ModelSerializer):
    broker_name = serializers.SerializerMethodField()
    borrower_names = serializers.SerializerMethodField()
    stage_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Application
        fields = [
            'id', 'reference_number', 'loan_amount', 'stage', 'stage_display',
            'created_at', 'broker_name', 'borrower_names'
        ]
    
    def get_broker_name(self, obj):
        return obj.broker.name if obj.broker else ''
    
    def get_borrower_names(self, obj):
        return ', '.join([f"{b.first_name} {b.last_name}" for b in obj.borrowers.all()])
    
    def get_stage_display(self, obj):
        return obj.get_stage_display()

class ApplicationDetailSerializer(serializers.ModelSerializer):
    broker_name = serializers.SerializerMethodField()
    borrower_names = serializers.SerializerMethodField()
    stage_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Application
        fields = '__all__'
    
    def get_broker_name(self, obj):
        return obj.broker.name if obj.broker else ''
    
    def get_borrower_names(self, obj):
        return ', '.join([f"{b.first_name} {b.last_name}" for b in obj.borrowers.all()])
    
    def get_stage_display(self, obj):
        return obj.get_stage_display()

class ApplicationCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Application
        fields = [
            'id', 'reference_number', 'stage', 'application_type', 'purpose',
            'loan_amount', 'loan_term', 'broker', 'branch', 'bd'
        ]

class ApplicationStageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['stage']

class ApplicationBorrowerSerializer(serializers.Serializer):
    borrower_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )
