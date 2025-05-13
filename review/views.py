from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from dish.models import Dish
from review.models import Review
from rest_framework import status
from .serializers import ReviewSerializer
# Create your views here.

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def dish_review(request, dish_slug):
    dish = get_object_or_404(Dish, slug=dish_slug)

    if request.method == 'GET':
        reviews = dish.reviews.all().order_by('-created_at')
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
       
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response(
                {'detail': 'Authentication required to post a review.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, dish=dish)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            
            
