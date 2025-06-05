"""
Serializers for the cart and cart items in the catering site API.

This module defines serializers for the Cart and CartItem models, enabling
conversion between model instances and their JSON representations for API
responses and requests.

Classes:
    CartSerializer: Serializes Cart model instances, including user and
        cart details.
    CartItemSerializer: Serializes CartItem model instances, including
        related dish, cart, quantity, and extras.
"""
from rest_framework import serializers
from rest_framework.response import Response
from .models import Cart, CartItem
from dish.serializer import DishSerializer, ExtraItemsSerializer


class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for the Cart model.
    Serializes the following fields: id, cart_code, user, created_at, and paid.
    The 'user' field is represented as a string and is read-only.
    The 'created_at', 'paid', and 'user' fields are set as read-only to\
        prevent modification via API.
    """

    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Cart
        fields = (
            'id',
            'cart_code',
            'user',
            'created_at',
            'paid',
        )
        read_only_fields = ('created_at', 'paid', 'user')


class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for CartItem model, providing nested representations 4 related
    Dish, Cart, and ExtraItems models. Used to serialize and deserialize cart
    item data, including associated dish, cart, quantity, and extra items.
    All related fields are read-only and represented using their respective
    serializers.
    """
    dish = DishSerializer(read_only=True)
    cart = CartSerializer(read_only=True)
    extras = ExtraItemsSerializer(many=True, read_only=True)

    class Meta:
        model = CartItem
        fields = (
            'id',
            'cart',
            'dish',
            'quantity',
            'extras'
        )


class SimpleCartSerializer(serializers.ModelSerializer):
    """
    Serializer for the Cart model that provides a simplified representation
    including the cart's ID, cart code, and the total number of items.
    Fields:
        id (int): Unique identifier for the cart.
        cart_code (str): Unique code associated with the cart.
        number_of_items (int): Total quantity of all items in the cart,
            calculated by summing the quantity of each item.
    Methods:
        get_number_of_items(obj): Returns the sum of quantities for all
            items in the cart instance.
    """
    number_of_items = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'cart_code', 'number_of_items']
    
    def get_number_of_items(self, obj):
        return sum([item.quantity for item in obj.items.all()])
