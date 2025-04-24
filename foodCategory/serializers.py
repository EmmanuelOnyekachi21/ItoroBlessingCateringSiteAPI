"""
Serializers for the Category model used in the food site API.
"""

from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    Handles serialization and deserialization of Category
    instances, including validation and transformation.
    """

    class Meta:
        model = Category
        fields = '__all__'
        # These fields are automatically handled by the model logic
        read_only_fields = ['slug', 'created_at', 'updated_at']
