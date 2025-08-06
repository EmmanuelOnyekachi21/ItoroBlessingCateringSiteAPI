"""
contact.views
-------------
This module contains view functions for handling contact-related operations
in the Itoro Blessing Catering Site API. It provides endpoints for submitting
contact messages from users.
Functions:
    - submit_contact_message: Handles the submission of contact messages.
"""
from rest_framework.decorators import api_view
from .models import Contact
from .serializer import ContactSerializer
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
def submit_contact_message(request):
    """
    Handles the submission of a contact message via an API endpoint.
    This view function receives a POST request containing contact message data,
    validates the data using the ContactSerializer,
    and saves the message if valid.
    On successful submission, it returns success message with HTTP 200 status
    If validation fails, it returns serializer errors with HTTP 400 status.
    Args:
        request (Request): contains contact message data.
    Returns:
        Response: A DRF Response object with either
                    a success message or validation errors.
    """
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        # No need to save this to a varibale since --
        # i won't be returning such as response
        serializer.save()
        return Response(
            {'message': 'Your message was sent successfully!'},
            status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
