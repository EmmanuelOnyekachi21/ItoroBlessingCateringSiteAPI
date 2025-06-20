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
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404


@api_view(['POST'])
# Prevents partial saves (e.g. CartItem saved but an ExtraItem fails)
@transaction.atomic
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
        extra_items = request.data.get('extra_items')
        note = request.data.get('note')
        quantity = int(request.data.get('quantity', 1))
        orderoption = request.data.get('orderoption').lower()
        get_cart, created = Cart.objects.get_or_create(
            cart_code=cart_code
        )
        
        valueType = [ch[0] for ch in Cart.ORDER_TYPES]
        if orderoption in valueType:
            get_cart.order_type = orderoption
            get_cart.save()        
            

        get_dish = Dish.objects.get(id=dish_id)

        # Create CartItem object
        cart_item, _ = CartItem.objects.get_or_create(
            cart=get_cart,
            dish=get_dish
        )
        
        # Update CartItem Quantity
        if cart_item:
            cart_item.quantity = quantity
        if note:
            cart_item.special_instruction = note
        
        cart_item.save()

        # Add new Extras
        if extra_items:
            if not isinstance(extra_items, dict):
                return Response(
                    {'error': 'Extra items must be a dictionary'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            for xtra_item_id, data in extra_items.items():
                extra_item = ExtraItem.objects.get(id=xtra_item_id)
                qty = int(data.get('quantity', 1))
                
                CartItemExtra.objects.update_or_create(
                    cart_item=cart_item,
                    extra=extra_item,
                    defaults={'quantity': qty}
                )
        
        serializers = CartItemSerializer(cart_item)
        return Response({
            "message": "Dish added to cart successfully",
            'data': serializers.data,
        }, status=status.HTTP_201_CREATED)
    except Dish.DoesNotExist:
        return Response(
            {'error': 'Dish not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except ExtraItem.DoesNotExist:
        return Response(
            {'error': 'Extra item not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Cart.DoesNotExist:
        return Response(
            {'error': 'Cart not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'An unexpected error occurred: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )


# @api_view(['POST'])
# def product_in_cart(request):
#     """
#     Checks if a specific dish is present in the user's cart.
#     Args:
#         request (Request): The HTTP request object containing\
#             'cart_code' and 'dish_id' in its data.
#     Returns:
#         Response: A JSON response with a boolean value under\
#             the key 'dish_in_cart' indicating whether the\
#                 specified dish exists in the cart. Returns 200 OK status

#     """
#     cart_code = request.data.get('cart_code')
#     dish_id = request.data.get('dish_id')

#     # Get cart
#     cart = Cart.objects.get(cart_code=cart_code)

#     # Get DIsh
#     dish = Dish.objects.get(id=dish_id)

#     is_exists = CartItem.objects.filter(cart=cart, dish=dish).exists()
#     return Response(
#         {'dish_in_cart': is_exists}, status=status.HTTP_200_OK
#     )


@api_view(['GET'])
def get_cart_stat(request):
    """
    Retrieve the status of a cart using the provided cart code.

    This view expects a 'cart_code' parameter in the request's query
    parameters. If the cart code is present and a cart with that code
    exists, it returns the serialized cart data with a 200 OK status.
    If the cart code is missing, it returns a 400 Bad Request with an
    appropriate message. If the cart does not exist, it returns a 404
    Not Found. Any other exceptions are caught and returned as a 400
    Bad Request.

    Args:
        request (Request): The HTTP request object containing query
            parameters.

    Returns:
        Response: A DRF Response object with the serialized cart data
            or an error message.
    """
    try:
        cart_code = request.query_params.get('cart_code')
        if not cart_code:
            return Response({
                'message': 'Cart code not provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        cart = Cart.objects.get(cart_code=cart_code)
        serializer = SimpleCartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Cart.DoesNotExist:
        return Response(
            {'message': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_cart_item(request):
    """
    Retrieve a specific cart item for a given cart and dish.

    This view expects 'cart_code' and 'dish_id' as query parameters in
    the request. It fetches the cart using the provided cart code
    (ensuring the cart is not paid), and retrieves the dish using the
    provided dish ID. If both exist, it attempts to find the
    corresponding CartItem linking the cart and dish. If found, it
    returns the serialized CartItem data with a 200 OK status. If the
    CartItem does not exist, it returns a 404 Not Found with an
    appropriate message. If either parameter is missing, it returns a
    400 Bad Request.

    Args:
        request (Request): The HTTP request object containing
            'cart_code' and 'dish_id' as query parameters.

    Returns:
        Response: A DRF Response object with the serialized CartItem
            data if found, or an error message if not found or if
            parameters are missing.
    """
    try:
        cart_code = request.query_params.get('cart_code')
        dish_id = request.query_params.get('dish_id')
        
        if not cart_code or not dish_id:
            return Response(
                {'error': 'cart code and dish id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart = get_object_or_404(Cart, cart_code=cart_code, paid=False)
        dish = get_object_or_404(Dish, id=dish_id)
        
        cart_item = CartItem.objects.get(cart=cart, dish=dish)
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except CartItem.DoesNotExist:
        return Response(
            {'message': 'Item not in cart'},status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
def get_cart_item(request):
    """
    Retrieve a specific cart item based on cart code and dish ID.
    This view extracts 'cart_code' and 'dish_id' from the request query
    parameters, fetches the corresponding Cart and Dish objects, and then
    retrieves the CartItem instance that matches both. If found, it returns
    the serialized cart item data with a 200 OK status.
    Returns:
        Response: Serialized CartItem data with HTTP 200 OK if found.
        Response: Error message with HTTP 400 BAD REQUEST if the CartItem
        does not exist.
        Response: Error message with HTTP 404 NOT FOUND for other exceptions.
    Raises:
        CartItem.DoesNotExist: If the cart item is not found.
        Exception: For any other unexpected errors.
    """
    try:
        cart_code = request.query_params.get('cart_code')
        dish_id = request.query_params.get('dish_id')
        
        cart = get_object_or_404(Cart, cart_code=cart_code)
        dish = get_object_or_404(Dish, id=dish_id)
        
        cart_item = CartItem.objects.get(cart=cart, dish=dish)
        
        serilializer = CartItemSerializer(cart_item)
        
        return Response(
            serilializer.data, status=status.HTTP_200_OK
        )
    except CartItem.DoesNotExist:
        return Response({
            'error', 'Cart Item doesn\'t exist'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_404_NOT_FOUND)
    
