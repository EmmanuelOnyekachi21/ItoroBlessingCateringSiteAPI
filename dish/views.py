"""
Dish API views.

Provides API endpoints for:
- Listing all available dishes (`dish_list`)
- Retrieving dish details by category and slug (`dish_detail_view`)
- Fetching a random selection of 3 featured dishes with caching
    (`random_featured_dish`).

Uses Django REST Framework decorators (`@api_view`), caching, and
logging.
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import Dish
from .serializer import DishSerializer, DishDetailSerializer
from django.core.cache import cache
import random
import logging
from django.shortcuts import get_object_or_404

# Creates a logger named after the current Python module.
# If your file is called views.py, the logger name becomes yourapp.views
logger = logging.getLogger(__name__)


def cache_available_dish_data():
    """
    Retrieve serialized data of available dishes from cache,
    or query the database and store the result in cache for 30 seconds.

    Returns:
        list: Serialized list of available dishes.
    """
    featured = cache.get('available_dish_data')
    if featured is None:
        queryset = Dish.objects.filter(is_available=True)
        serializer = DishSerializer(queryset, many=True)
        data = serializer.data

        if len(data) > 3:
            featured = random.sample(data, 3)
            cache.set('available_dish_data', featured, timeout=300)
            return featured
        else:
            featured = None
    return featured


@api_view(['GET'])
def random_featured_dish(request):
    """
    Return a random sample of 3 available dishes from cache.

    If fewer than 3 dishes are available, return an error message.
    Falls back to a database query and logs exceptions if cache fails.

    Returns:
        Response: A list of 3 randomly selected dishes or an error message.
    """
    try:
        dishes = cache_available_dish_data()

        if not dishes:
            return Response(
                {"Message": "Not enough dishes to feature."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # featured_dishes = random.sample(dishes, 3)
        logger.info("Cache hit: Retrieved featured dishes from cache.")
        # Log the cache hit
        return Response(dishes)

    except Exception:
        logger.exception("Error retrieving cached dishes")
        queryset = Dish.objects.filter(is_available=True)[:3]
        serializer = DishSerializer(queryset, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def dish_list(request):
    """
    Retrieve a list of available dishes.

    This view filters the Dish objects to include only those marked as
    available, serializes the queryset, and returns the serialized data
    in the response.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: A response object containing serialized data of
        available dishes.
    """
    available_dishes = Dish.objects.filter(is_available=True)
    serializer = DishSerializer(available_dishes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def dish_detail_view(request, category_slug, slug):
    """
    Retrieve and return detailed information about a specific dish.
    Args:
        request (HttpRequest): The HTTP request object.
        category_slug (str): The slug of the dish's category.
        slug (str): The slug of the dish.
    Returns:
        Response: A Response object containing serialized dish data and an
            HTTP 200 OK status if the dish is found and available. Raises a
            404 error if the dish does not exist or is not available.
    """
    dish = get_object_or_404(
        Dish,
        slug=slug,
        category__slug=category_slug,
        is_available=True
    )
    serializer = DishDetailSerializer(dish)
    return Response(
        serializer.data, status=status.HTTP_200_OK
    )
