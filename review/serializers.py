from rest_framework import serializers
from .models import Review
from django.contrib.auth import get_user_model


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField() # uses __str__ of the user model
    dish = serializers.StringRelatedField() # uses __str__ of the dish model
    class Meta:
        model = Review
        fields = [
            'id', 'user', 'dish', 'rating', 'comment',
            'created_at'
        ]
        read_only_fields = [
            'id', 'user', 'created_at'
        ]
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError(
                'Rating must be between 1 and 5'
            )
        return value
