"""
This module provides logout functionality for authenticated users using JWT.
It defines an API endpoint that allows users to blacklist their refresh token,
effectively logging them out. The endpoint expects a POST request with a valid
refresh token and requires the user to be authenticated.
"""
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logs out a user by blacklisting their refresh token.

    This view expects a POST request with a 'refresh' token in request data
    The refresh token is blacklisted to prevent further use. If the token is
    missing or invalid, an error response is returned.

    Args:
        request (Request): The HTTP request object with the refresh token.

    Returns:
        Response: Indicates success or failure of the logout process.
    """
    try:
        refresh_token = request.data['refresh']
        token = RefreshToken(refresh_token)
        token.blacklist()
    except KeyError:
        return Response(
            {
                "error": "Refresh token is needed"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    except TokenError as e:
        return Response(
            {
                "error": str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response(
        {
            "message": "Successful logging out"
        },
        status=status.HTTP_205_RESET_CONTENT
    )
