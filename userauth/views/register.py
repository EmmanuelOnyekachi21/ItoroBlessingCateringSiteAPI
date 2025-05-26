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

@api_view(['post'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    account = serializer.save()
    """
    If validation passes, this line, above, actually creates and saves the new user in the database.

    The .save() method is typically defined in the serializer to handle user\
        creation logic (e.g., hashing the password).
    """
    token = generate_email_token(account.email)
    send_verification_email(account.email, token)
    """
    The send_verification_email function sends an email to the user\
        with a verification link that includes the generated token.
    """
    logger.info(f'Generated token for {account}: {token}')
    refresh = RefreshToken.for_user(account)
    return Response({
        "message": (
            'Registration successful.'
            'Please check your email to verify your account.'
        ),
        "account": serializer.data,
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }, status=status.HTTP_201_CREATED)  

