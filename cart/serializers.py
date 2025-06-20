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
from .models import Cart, CartItem, CartItemExtra
from dish.serializer import DishSerializer, ExtraItemsSerializer


class CartItemExtraSerializer(serializers.ModelSerializer):
    """
    Serializer for the CartItemExtra model, providing nested representation
    of ExtraItem associated with a CartItem. Used to serialize and deserialize
    extra items in a cart item.
    """
    extra_name = serializers.SerializerMethodField()
    extra_id = serializers.IntegerField(source='extra.id', read_only=True)
    class Meta:
        model = CartItemExtra
        fields = (
            'id',
            'extra_id',
            'extra_name',
            'quantity',
        )
    
    def get_extra_name(self, obj):
        """
        Returns the name of the extra item associated with the CartItemExtra.
        This method is used to provide a human-readable representation
        of the extra item in the serialized output.
        """
        return obj.extra.name if obj.extra else None


class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for CartItem model, providing nested representations 4 related
    Dish, Cart, and ExtraItems models. Used to serialize and deserialize cart
    item data, including associated dish, cart, quantity, and extra items.
    All related fields are read-only and represented using their respective
    serializers.
    """
    dish_name = serializers.SerializerMethodField()
    dish_id = serializers.IntegerField(source='dish.id', read_only=True)
    # cart_id = serializers.IntegerField(source='cart.id', read_only=True)
    cart_code = serializers.SerializerMethodField()
    extra_items = CartItemExtraSerializer(many=True, read_only=True)
    delivery_option = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = (
            'id',
            # 'cart',
            'cart_code',
            'special_instruction',
            'dish_id',
            'dish_name',
            'quantity',
            'extra_items',
            'delivery_option',
            # 'note'
        )
    
    def get_dish_name(self, obj):
        """
        Returns the name of the dish associated with the CartItem.
        This method is used to provide a human-readable representation
        of the dish in the serialized output.
        """
        return obj.dish.name if obj.dish else None
    
    def get_cart_code(self, obj):
        """
        Returns the cart code associated with the CartItem.
        This method is used to provide a human-readable representation
        of the cart code in the serialized output.
        """
        return obj.cart.cart_code if obj.cart else None
    
    def get_delivery_option(self, obj):
        return obj.cart.order_type if obj.cart else None

class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for the Cart model.
    Serializes the following fields: id, cart_code, user, created_at, and paid.
    The 'user' field is represented as a string and is read-only.
    The 'created_at', 'paid', and 'user' fields are set as read-only to\
        prevent modification via API.
    """

    user = serializers.StringRelatedField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = (
            'id',
            'cart_code',
            'user',
            'created_at',
            'paid',
            'order_type',
            # 'special_instruction',
            'items'
        )
        read_only_fields = ('created_at', 'paid', 'user')

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

