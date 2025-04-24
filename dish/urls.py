"""
URL configuration for dish-related endpoints.

Includes routes for featured dish functionality.
"""

from django.urls import path
from . import views

urlpatterns = [
    path(
        'featured-dishes/',
        views.random_featured_dish,
        name='random_featured_dish'
    ),
]
