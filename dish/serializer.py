"""
Serializers for the Dish model.

This module defines the serializer for the Dish model to handle
data validation, transformation, and representation for API
requests and responses.
"""

from rest_framework import serializers
from .models import Dish


class DishSerializer(serializers.ModelSerializer):
    """
    Serializer for the Dish model.

    Handles conversion between Dish instances and their JSON
    representations for use in API views.
    """
    class Meta:
        model = Dish
        fields = [
            'id', 'name', 'slug', 'image', 'category', 'is_available',
            'created_at', 'updated_at', 'price', 'description'
        ]
        read_only_fields = ['created_at', 'updated_at', 'slug']
