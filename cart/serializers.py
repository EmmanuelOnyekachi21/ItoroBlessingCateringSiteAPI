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
from dish.models import Dish, ExtraItem


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
            'dish_id',
            'cart_code',
            'dish_name',
            'quantity',
            'unit_price',
            'total_price',
            'extra_items',
            'special_instruction',
            'delivery_option',
            # 'note'
        )
        read_only_fields = ['unit_price', 'total_price']
    
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


class CartItemWriteSerializer(serializers.ModelSerializer):
    dish = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all(), write_only=True)
    extra_items = serializers.DictField(write_only=True, required=False)
    cart_code = serializers.CharField(write_only=True)
    note = serializers.CharField(write_only=True, required=False, allow_blank=True)
    orderoption = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CartItem
        fields = (
            'dish',
            'quantity',
            'cart_code',
            'note',
            'orderoption',
            'extra_items'
        )

    def validate(self, attrs):
        dish = attrs['dish']
        quantity = attrs.get('quantity', 1)
        extras = self.initial_data.get('extra_items', {})

        if extras and not isinstance(extras, dict):
            raise serializers.ValidationError({'extra_items': 'Must be a dictionary'})

        unit_price = dish.price
        total = unit_price * quantity

        # Add extras to total price
        for extra_id, data in extras.items():
            try:
                extra = ExtraItem.objects.get(id=extra_id)
                qty = int(data.get('quantity', 1))
                total += extra.price * qty
            except ExtraItem.DoesNotExist:
                continue

        attrs['unit_price'] = unit_price
        attrs['total_price'] = total
        return attrs

    def create(self, validated_data):
        """
        Creates a CartItem instance and associates it with a Cart. If the cart with
        the provided cart_code does not exist, it is created. Sets the order type
        if provided and valid. Adds extra items to the CartItem if specified.
        All operations are performed atomically to ensure data integrity.
        Args:
            validated_data (dict): Validated data containing dish, quantity,
                unit_price, and total_price for the CartItem.
        Returns:
            CartItem: The created CartItem instance.
        """
        
        from django.db import transaction

        cart_code = self.initial_data.get('cart_code')
        note = self.initial_data.get('note', '')
        orderoption = self.initial_data.get('orderoption')
        extras = self.initial_data.get('extra_items', {})

        with transaction.atomic():
            # Get or create the cart
            cart, _ = Cart.objects.get_or_create(cart_code=cart_code)

            # Set order type if valid
            if orderoption in dict(Cart.ORDER_TYPES):
                cart.order_type = orderoption
                cart.save()

            # Create CartItem
            cart_item = CartItem.objects.create(
                cart=cart,
                dish=validated_data['dish'],
                quantity=validated_data.get('quantity', 1),
                special_instruction=note,
                unit_price=validated_data['unit_price'],
                total_price=validated_data['total_price']
            )

            # Add extras
            for extra_id, data in extras.items():
                try:
                    extra = ExtraItem.objects.get(id=extra_id)
                    qty = int(data.get('quantity', 1))
                    CartItemExtra.objects.update_or_create(
                        cart_item=cart_item,
                        extra=extra,
                        defaults={'quantity': qty}
                    )
                except ExtraItem.DoesNotExist:
                    continue

            return cart_item



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

