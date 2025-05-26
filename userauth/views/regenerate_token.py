"""
This module provides an API endpoint for regenerating a verification token
for user accounts. It defines a view that accepts an email address,
validates the existence and verification status of the associated account,
generates a new verification token if necessary, and sends the token to
the user's email address. The module also logs token regeneration events
for auditing purposes.
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from userauth.utils.email_token import generate_email_token
from userauth.utils.email_sender import send_verification_email
from account.models import Account
import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
def regenerate_token(request):
    """
    Handles the regeneration of a verification token for a user. This function
    accepts an email address from the request data, validates the email to
    ensure it belongs to a registered user, and checks if the account is
    already verified. If the account is not verified, it generates a new
    verification token, logs the token generation, and sends the token to the
    user's email address.

    Args:
        request (Request): The HTTP request object containing the email in the
            request data.

    Returns:
        Response: A Response object with an appropriate message and HTTP status
            code:
            - 400 BAD REQUEST if the email is not provided or the account is
              already verified.
            - 404 NOT FOUND if the email is not associated with any registered
              account.
            - 200 OK if a new verification token is successfully generated and
              sent.

    Raises:
        Account.DoesNotExist: If no account is found with the provided email.

    Side Effects:
        - Generates a new verification token for the user.
        - Sends a verification email to the user's email address.
        - Logs the token generation for auditing purposes.
    """
    email = request.data.get('email')
    if not email:
        return Response(
            {"message": "Please input email"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Validate email address to ensure that user already registered,
    # and is stored in the database
    try:
        account = Account.objects.get(email=email)
    except Account.DoesNotExist:
        return Response(
            {"message": "Email not found. Please register first"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Check if the account is already verified
    if account.is_verified:
        return Response(
            {"message": "Account already verified"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Generate a new verification token and send the email
    token = generate_email_token(email)
    logger.info("Regenerated token for %s: %s", email, token)
    send_verification_email(email, token)

    return Response(
        {
            "message": (
                "A new verification link has been sent to your email."
                " Please check your inbox or spam folder."
            )
        },
        status=status.HTTP_200_OK
    )
