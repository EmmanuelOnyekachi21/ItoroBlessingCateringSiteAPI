from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from userauth.utils.email_token import verify_email_token
from account.models import Account


@api_view(['get'])
def verify_email_view(request):
    token = request.query_params.get('token')
    if not token:
        return Response({
            'Error': 'Missing token'
        }, status=status.HTTP_400_BAD_REQUEST)

    email = verify_email_token(token)
    
    if not email:
        return Response({
            'Error': 'Invalid or expired token'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = Account.objects.get(email=email)
        user.is_verified = True
        user.save()
        return Response({
            'Message': 'Email successfully verified',
        })
    except Account.DoesNotExist:
        return Response({
            'Error': 'User not found'
        }, status=status.HTTP_400_BAD_REQUEST)



