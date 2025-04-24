"""
Views for handling dish-related API endpoints.

This module includes a view for retrieving a random selection of available
dishes marked as featured. It uses caching to optimize performance and
includes error logging for debugging purposes.
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Dish
from .serializer import DishSerializer
from django.core.cache import cache
import random, logging

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
            cache.set('available_dish_data', featured, timeout=30)
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
        return Response(dishes)

    except Exception:
        logger.exception("Error retrieving cached dishes")
        queryset = Dish.objects.filter(is_available=True)[:3]
        serializer = DishSerializer(queryset, many=True)
        return Response(serializer.data)
