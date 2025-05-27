"""
This module provides the login_view for handling user authentication
requests. It validates user credentials using the LoginSerializer and
returns a response with user data upon successful authentication or
raises an InvalidToken exception if authentication fails.
"""
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from userauth.serializers import LoginSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Handles user login by validating credentials using the LoginSerializer.
    Args:
        request (Request): The HTTP request object containing user login data.
    Returns:
        Response: A Response object containing the validated user data\
            and HTTP 200 status on success.
    Raises:
        InvalidToken: If the provided credentials are invalid\
            or token validation fails.
    """

    serializer = LoginSerializer(data=request.data)

    try:
        serializer.is_valid(raise_exception=True)
    except TokenError as e:
        raise InvalidToken(e.args[0])

    return Response(
        serializer.validated_data,
        status=status.HTTP_200_OK
    )
