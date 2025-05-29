"""
This module provides a view for refreshing JWT tokens using the SimpleJWT
package. It defines an endpoint that accepts a POST request with a refresh
token and returns a new access token.

Functions:
    token_refresh_view(request): Handles the token refresh process and
    returns a new access token if the provided refresh token is valid.
"""
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.decorators import permission_classes, api_view


@permission_classes([AllowAny])
@api_view(['POST'])
def token_refresh_view(request):
    """
    Handles JWT token refresh requests.

    This view accepts a POST request containing a refresh token, validates it,
    and returns a new access token if the refresh token is valid. If the token
    is invalid or expired, an appropriate error is raised.

    Args:
        request (Request): The HTTP request object containing the refresh
            token in the data.

    Returns:
        Response: A response object containing the new access token and
            (optionally) a new refresh token.

    Raises:
        InvalidToken: If the provided refresh token is invalid or expired.
    """
    serializer = TokenRefreshSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
    except TokenError as e:
        raise InvalidToken(e.args[0])

    return Response(
        serializer.validated_data,
        status=status.HTTP_200_OK
    )
