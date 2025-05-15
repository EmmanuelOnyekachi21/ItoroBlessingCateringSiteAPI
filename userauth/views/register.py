from rest_framework.response import Response
from rest_framework import status
from userauth.serializers.register import RegisterSerializer
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['post'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    account = serializer.save()
    """
    If validation passes, this line actually creates and saves the new user in the database.

    The .save() method is typically defined in the serializer to handle user\
        creation logic (e.g., hashing the password).
    """
    refresh = RefreshToken.for_user(account)
    return Response({
        "account": serializer.data,
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }, status=status.HTTP_201_CREATED)