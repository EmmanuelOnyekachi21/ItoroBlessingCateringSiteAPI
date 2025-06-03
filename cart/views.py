"""
This module provides API views for managing cart operations in the
catering site API.

Views:
    - add_dish: Adds a dish (with optional extra item) to a user's cart,
      creating the cart if it does not exist.
    - product_in_cart: Checks if a specific dish is already present in
      the user's cart.

Dependencies:
    - Uses Django models for Cart, CartItem, Dish, and ExtraItem.
    - Utilizes Django REST Framework for API view handling,
      serialization, and HTTP responses.
"""
from .models import *
from rest_framework.decorators import api_view
from dish.models import Dish, ExtraItem
from .serializers import CartItemSerializer
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
def add_dish(request):
    """
    Adds a dish (and optionally an extra item) to a user's cart.

    This view retrieves or creates a cart using the provided cart code,
    fetches the specified dish and optional extra item, and then creates
    or retrieves a CartItem linking them. If the CartItem is newly
    created, its quantity is set to 1.

    Args:
        request (Request): The HTTP request object containing
            'cart_code', 'dish_id', and optionally 'extra_item_id'
            in its data.

    Returns:
        Response: A DRF Response object containing a success message
            and CartItem data if successful, or an error message if
            an exception occurs.
    """
    try:
        cart_code = request.data.get('cart_code')
        dish_id = request.data.get('dish_id')
        extra_item_id = request.data.get('extra_item_id')
        get_cart, created = Cart.objects.get_or_create(
            cart_code=cart_code
        )
        get_dish = Dish.objects.get(id=dish_id)

        # Get Extra Items
        if extra_item_id:
            get_extras = ExtraItem.objects.get(id=extra_item_id)
        else:
            get_extras = None

        # Create CartItem object
        cart_item, created = CartItem.objects.get_or_create(
            cart=get_cart,
            dish=get_dish,
            extras=get_extras
        )
        if created:
            cart_item.quantity = 1
            cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(
            {
                'message': 'Added to cart successfully',
                'data': serializer.data,
            },
            status=status.HTTP_201_CREATED
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
def product_in_cart(request):
    """
    Checks if a specific dish is present in the user's cart.
    Args:
        request (Request): The HTTP request object containing\
            'cart_code' and 'dish_id' in its data.
    Returns:
        Response: A JSON response with a boolean value under\
            the key 'dish_in_cart' indicating whether the\
                specified dish exists in the cart. Returns HTTP 200 OK status.

    """
    cart_code = request.data.get('cart_code')
    dish_id = request.data.get('dish_id')

    # Get cart
    cart = Cart.objects.get(cart_code=cart_code)

    # Get DIsh
    dish = Dish.objects.get(id=dish_id)

    is_exists = CartItem.objects.filter(cart=cart, dish=dish).exists()
    return Response(
        {'dish_in_cart': is_exists}, status=status.HTTP_200_OK
    )
