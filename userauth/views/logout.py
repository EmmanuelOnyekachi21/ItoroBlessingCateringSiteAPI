from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


@api_view(['post'])
@permission_classes([IsAuthenticated])
def logout_view(request):
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
    return Response({"Message": "Successful logging out"}, status=status.HTTP_205_RESET_CONTENT)
