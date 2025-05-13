"""
URL configuration for dish-related endpoints.

Includes routes for featured dish functionality.
"""

from django.urls import path, include
from . import views
from review.views import dish_review


urlpatterns = [
    path(
        'featured-dishes/',
        views.random_featured_dish,
        name='random_featured_dish'
    ),
    path('dish/', views.dish_list, name='dish_list'),
    path(
        '<slug:dish_slug>/reviews/',
        dish_review,
        name='dish_review'
    ),
    path(
        '<slug:category_slug>/<slug:slug>/',
        views.dish_detail_view,
        name='dish_detail_view'
    ),
]
