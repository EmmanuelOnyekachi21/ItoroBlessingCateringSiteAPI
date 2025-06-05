"""
URL configuration for the cart app.

Defines URL patterns for cart-related actions such as:\
    - adding items
    - checking products in the cart.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Add a dish to the cart
    path('add_item/', views.add_dish, name='add-dish'),
    # Check if a product is in the cart
    # path('product_in_cart/', views.product_in_cart, name='product-in-cart'),
    path('get_cart_stat/', views.get_cart_stat, name='get-cart-stat'),
]
