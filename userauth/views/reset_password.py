"""
This module provides API views for handling password reset functionality
for user accounts. It includes endpoints for requesting a password reset
by email and for verifying a password reset token to set a new password.
Views:
    - request_password_reset_view: Handles password reset requests by generating
      a reset token and sending it to the user's email if the account exists and
      is verified.
    - verify_password_reset_token_view: Verifies the password reset token and
      allows the user to set a new password if the token is valid.

"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from account.models import Account
from django.shortcuts import get_object_or_404
from userauth.utils.password_reset_token import (
    generate_password_reset_token, verify_password_reset_token
)
from userauth.utils.email_sender import (
    send_password_reset_email,
)
import logging


logger = logging.getLogger(__name__)

@api_view(['post'])
def request_password_reset_view(request):
    """
    Handles password reset requests by generating a password reset token
    and sending it to the user's email address.
    This view expects an email address as a query parameter. If the email
    is associated with a verified account, a password reset token is generated
    and sent to the provided email address. If the email does not exist or the
    account is not verified, appropriate error messages are returned.
    Args:
        request (Request): The HTTP request object containing query parameters
    Returns:
        Response: A response object with a success message if the email exists
        and a password reset link is sent, or an error message if the email is
        missing or the account is not verified.
    """
    email = request.data.get('email')
    if not email:
        return Response({
            "error": "Email is required"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        account = Account.objects.get(email=email)
        if not account.is_verified:
            return Response({
                "error": "Account is not verified"
            }, status=status.HTTP_400_BAD_REQUEST)
        # Generate a password reset token
        # and send the email
        # to the user with the new token
        token = generate_password_reset_token(email)
        send_password_reset_email(email, token)
        logger.info(
            f"Password reset email sent to {email}"
        )
    except Account.DoesNotExist:
        logger.error(
            f"Password reset failed for {email}: "
            "Account does not exist"
        )
    return Response({
        "message": (
            "If the email exists, a password reset link has been sent."
        )}, status=status.HTTP_200_OK)


@api_view(['post'])
def verify_password_reset_token_view(request):
    """
    Handles password reset requests by verifying the provided reset token and
    updating the user's password.

    Expects the following fields in the request data:
        - token: The password reset token sent to the user's email.
        - password: The new password to set.
        - confirm_password: Confirmation of the new password.

    Returns:
        - 200 OK with a success message if the password is reset successfully.
        - 400 Bad Request with an error message if any field is missing,
          passwords do not match, the token is invalid/expired, or the account
          does not exist.
    """
    token = request.data.get('token')
    password = request.data.get('password')
    confirm_password = request.data.get('confirm_password')
    
    if not token or not password or not confirm_password:
        return Response({
            "error": "Missing fields"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if password != confirm_password:
        return Response({
            "error": "Passwords do not match"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    email = verify_password_reset_token(token)
    if not email:
        return Response({
            "error": "Invalid or expired token"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = Account.objects.get(email=email)
        user.set_password(password)
        user.save()
        logger.info(
            f"Password reset successful for {email}"
        )
    except Account.DoesNotExist:
        logger.error(
            f"Password reset failed for {email}: "
            "Account does not exist"
        )
        return Response({
            "error": "Account does not exist"
        }, status=status.HTTP_400_BAD_REQUEST)
    return Response({
        "message": "Password reset successful"
    }, status=status.HTTP_200_OK)    
    




