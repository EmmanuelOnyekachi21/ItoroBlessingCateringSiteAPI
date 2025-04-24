"""
Views for handling Category-related API endpoints.
Supports listing all active categories and creating new ones.
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category
from .serializers import CategorySerializer


@api_view(['GET', 'POST'])
def category_list_create(request):
    """
    GET: Return a list of active categories.
    POST: Allow staff users to create a new category.
    """
    if request.method == 'GET':
        categories = Category.objects.filter(is_active=True)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response(
                {'message': 'Not Authorized'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
