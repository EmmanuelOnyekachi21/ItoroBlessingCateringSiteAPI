"""
This module provides functionality to verify user email addresses via a token.

Functions:
    - verify_email_view(request):
        API endpoint that accept a 'token' as a query parameter, validates it,
        and updates the user's verification status accordingly.

API Behavior:
    - Retrieves the 'token' from the request's query parameters.
    - Validates the token using verify_email_token.
    - If valid, marks the corresponding user's email as verified.

Returns:
    - 400 BAD REQUEST if the token is missing, invalid, expired, or if the
      user is not found.
    - 200 OK if the email is already verified or has been successfully
      verified.
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from userauth.utils.email_token import verify_email_token
from account.models import Account
import logging


logger = logging.getLogger('__name__')


@api_view(['GET'])
def verify_email_view(request):
    """
    Handles email verification requests.

    This view verifies a user's email address using a token provided as a
    query parameter. It performs the following steps:

        1. Retrieves the 'token' from the request's query parameters.
        2. Validates the token and extracts the associated email address.
        3. Checks if a user with the extracted email exists.
        4. If the user exists and is not already verified, marks the user as
           verified.
        5. Returns appropriate HTTP responses for missing or invalid tokens,
           already verified users, or non-existent users.

    Args:
        request (Request): The HTTP request object containing query
            parameters.

    Returns:
        Response: A DRF Response object with a message indicating the result
            of the verification process and the appropriate HTTP status code.
    """

    token = request.query_params.get('token')
    if not token:
        return Response({
            'Error': 'Missing token'
        }, status=status.HTTP_400_BAD_REQUEST)

    email = verify_email_token(token)
    print(email)

    if not email:
        return Response({
            'Error': 'Invalid or expired token'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = Account.objects.get(email=email)
        if user.is_verified:
            return Response({
                'message': 'Email already verified and activated'
            }, status=status.HTTP_200_OK)
        else:
            user.is_verified = True
            user.save()
            logger.info(f'User Account {user} has been verified')
            return Response({
                'message': 'Email successfully verified',
            }, status=status.HTTP_200_OK)
    except Account.DoesNotExist:
        return Response({
            'Error': 'User not found'
        }, status=status.HTTP_400_BAD_REQUEST)
