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
from dish.models import ExtraItem


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
    extras = serializers.DictField(write_only=True, required=False)

    class Meta:
        model = CartItem
        fields = (
            'id',
            # 'cart',
            'dish',
            'cart_code',
            'special_instruction',
            'dish_id',
            'dish_name',
            'quantity',
            'extra_items',
            'delivery_option',
            'unit_price',
            'total_price',
            'extras',
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
    """
    Serializer for CartItem model, providing nested representations 4 related
    Dish, Cart, and ExtraItems models. Used to serialize and deserialize cart
    item data, including associated dish, cart, quantity, and extra items.
    All related fields are read-only and represented using their respective
    serializers.
    """
    extra_items = serializers.DictField(required=False, write_only=True)
    cart_code = serializers.CharField(write_only=True)
    note = serializers.CharField(write_only=True)
    orderoption = serializers.CharField(write_only=True, required=False)


    class Meta:
        model = CartItem
        fields = (
            'id',
            # 'cart',
            'dish',
            'quantity',
            'special_instruction',
            'extra_items',
            "cart_code",
            'note',
            'orderoption'
        )

    def validate(self, attrs):
        # Calculate price
        """
        Payload could come as:
            {
                "dish": 2,
                "quantity": 3,
                "extra_items": {
                    "5": { "quantity": 2 },
                    "9": { "quantity": 1 }
                }
                "cart_code": "AVSYGS!$%@$^%3645"
            }
        """
        dish = attrs['dish']
        quantity = attrs['quantity']
        extra_data = self.initial_data.get('extra_items', {})
        
        unit_price = dish.price
        total = unit_price * quantity
        
        if extra_data and not isinstance(extra_data, dict):
            raise serializers.ValidationError({'extra_items': 'Must be a dictionary'})
        for extra_id, extra_info in extra_data.items():
            try:
                extra = ExtraItem.objects.get(id=extra_id)
                extra_qty = int(extra_info.get('quantity', 1))
                total += extra.price * extra_qty
            except ExtraItem.DoesNotExist:
                continue
        
        attrs['unit_price'] = unit_price
        attrs['total_price'] = total
        
        return attrs
    
    def create(self, validated_data):
        cart_code = self.initial_data.get('cart_code')
        
        # get_or_create() returns a tuple, object and time created
        cart, _ = Cart.objects.get_or_create(
            cart_code=cart_code
        )
        
        orderoption = self.initial_data.get('orderoption')
        valueTypes = [ch[0] for ch in Cart.ORDER_TYPES]
        if orderoption in valueTypes:
            cart.order_type = orderoption
            cart.save()
        
        extra_items = self.initial_data.get(extra_items, {})
        unit_price = validated_data.pop('unit_price')
        total_price = validated_data.pop('total_price')
        
        # Create the cart item with resolved cart
        cart_item = CartItem.objects.create(
            cart=cart,
            dish=validated_data['dish'],
        )
        cart_item_qty = validated_data.pop('quantity')
        if cart_item_qty:
            cart_item.quantity = cart_item_qty
        cart_item_note = validated_data.pop('note')
        if cart_item_note:
            cart_item.special_instruction = cart_item_note
        cart_item.unit_price = unit_price
        cart_item.total_price = total_price
        cart_item.save()
        
        extra_items = validated_data.pop('extra_items')
        for xtra_item_id, data in extra_items.items():
                extra_item = ExtraItem.objects.get(id=xtra_item_id)
                qty = int(data.get('quantity', 1))
                
                CartItemExtra.objects.update_or_create(
                    cart_item=cart_item,
                    extra=extra_item,
                    defaults={'quantity': qty}
                )
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

