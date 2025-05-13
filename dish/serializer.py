"""
Serializers for the Dish model.

This module defines the serializer for the Dish model to handle
data validation, transformation, and representation for API
requests and responses.
"""

from rest_framework import serializers
from .models import Dish, ExtraItem, ExtraCategory
from foodCategory.serializers import CategorySerializer
from django.db.models import Avg
from review.serializers import ReviewSerializer


class DishSerializer(serializers.ModelSerializer):
    """
    Serializer for the Dish model.

    Handles conversion between Dish instances and their JSON
    representations for use in API views.
    """
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Dish
        fields = [
            'id', 'name', 'slug', 'image', 'category', 'is_available',
            'created_at', 'updated_at', 'price', 'description'
        ]
        read_only_fields = ['created_at', 'updated_at', 'slug']


class ExtraItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraItem
        fields = '__all__'


class ExtraCategorySerializer(serializers.ModelSerializer):
    extras = ExtraItemsSerializer(many=True, read_only=True)
    class Meta:
        model = ExtraCategory
        fields = ['id', 'name', 'extras']
        


class DishDetailSerializer(serializers.ModelSerializer):
    allowed_extras = ExtraCategorySerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Dish
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'image',
            'category', 'is_available', 'allowed_extras',
            'average_rating', 'total_reviews', 'reviews'
        ]
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return reviews.aggregate(average=Avg('rating'))
        return None
    
    def get_total_reviews(self, obj):
        total = obj.reviews.count()
        return total
