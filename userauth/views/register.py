"""
User registration view for the authentication system.

This module provides an API endpoint for user registration. It handles user
data validation, account creation, email verification token generation, and
sending verification emails. Upon successful registration, it returns a
response containing a success message, user data, and JWT tokens for
authentication.

Handle user registration via POST request.

Validates the incoming user data using the RegisterSerializer, creates a new
user account, generates an email verification token, and sends a verification
email to the user. Also issues JWT refresh and access tokens upon successful
registration.

Args:
    request (Request): The HTTP request object containing user registration
        data.

Returns:
    Response: A DRF Response object with a success message, user data, and
        JWT tokens.

Raises:
    ValidationError: If the provided data is invalid.
"""
from rest_framework.response import Response
from rest_framework import status
from userauth.serializers.register import RegisterSerializer
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from userauth.utils.email_sender import send_verification_email
from userauth.utils.email_token import generate_email_token
import logging


logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Handles user registration by validating input data, creating a new user
    account, generating an email verification token, sending a verification
    email, and returning authentication tokens upon successful registration.

    Args:
        request (Request): The HTTP request object containing user
            registration data.

    Returns:
        Response: A response object with a success message, user account
            data, refresh token, and access token.

    Raises:
        ValidationError: If the provided registration data is invalid.
    """
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    account = serializer.save()
    # The .save() method in the serializer handles user creation logic,
    # such as hashing the password and saving the user to the database.

    token = generate_email_token(account.email)
    send_verification_email(account.email, token)
    # The send_verification_email function sends an email to the user
    # with a verification link that includes the generated token.

    logger.info(f'Generated token for {account}: {token}')
    refresh = RefreshToken.for_user(account)
    return Response({
        "message": (
            "Registration successful. Please check your email to verify "
            "your account."
        ),
        "account": serializer.data,
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }, status=status.HTTP_201_CREATED)
