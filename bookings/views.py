"""
This module defines API views for handling catering booking requests.

Functions:
    create_booking(request):
        Handles POST requests to create a new catering booking using
        the BookingSerializer. Validates and saves booking data, and
        returns a response with the created booking details.

    get_booking_choices(request):
        Handles GET requests to retrieve available event types and
        number of guests choices for bookings. Returns a response
        containing these choices for use in booking forms.
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from .serializers import BookingSerializer
from .models import Booking


@api_view(['POST'])
@permission_classes([AllowAny])
def create_booking(request):
    """
    Handles the creation of a new booking request.

    This view receives booking data from the request, validates it using
    the BookingSerializer, and saves the booking if the data is valid.
    Upon successful creation, it returns a JSON response with a success
    message and the serialized booking data.

    Args:
        request (Request): The HTTP request object containing booking data.

    Returns:
        Response: A DRF Response object with a success message, serialized
        booking data, and HTTP 201 status code if creation is successful.

    Raises:
        ValidationError: If the provided data is invalid, a 400 response is
        automatically returned.
    """
    data = request.data.copy()
    if request.user.is_authenticated:
        data['user'] = request.user.public_id
    serializer = BookingSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(
        {
            'message': 'Catering Request Submitted Successfully',
            'data': serializer.data
        },
        status=status.HTTP_201_CREATED
    )

@api_view(['GET'])
def get_booking_choices(request):
    """
    Returns a list of choices for event types.
    
    This view provides a list of available event types for booking
    requests. It returns a JSON response containing the event types
    and their corresponding labels.
    Args:
        request (Request): The HTTP request object.
    Returns:
        Response: A DRF Response object containing the event types and
        their labels.
    """
    return Response({
        'event_types': Booking.EVENT_TYPES,
        'number_of_guests': Booking.NUMBER_OF_GUEST,
    }, status=status.HTTP_200_OK)
