from rest_framework import serializers
from .models import Interest


class InterestSerializer(serializers.ModelSerializer):
    """Serializer for Interest model"""
    
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Interest
        fields = ['id', 'name', 'category', 'category_display', 'description', 'icon', 'is_active']
        read_only_fields = ['id', 'created_at', 'updated_at']


class InterestListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing interests"""
    
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Interest
        fields = ['id', 'name', 'category', 'category_display', 'icon']
