from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from account.serializers import AccountSerializer
from rest_framework.permissions import IsAuthenticated


@api_view(['get', 'patch'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    
    if request.method == 'GET':
        serializer = AccountSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = AccountSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

