from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.decorators import permission_classes, api_view


@permission_classes([AllowAny])
@api_view(['post'])
def token_refresh_view(request):
    """
    Handle JWT token refresh via POST request
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
