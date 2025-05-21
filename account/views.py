"""
This module provides API views for managing user account profiles.

It includes endpoints for retrieving and partially updating the
authenticated user's profile data.

HTTP Methods:
    - GET: Returns the serialized data of the current authenticated user.
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from account.serializers import AccountSerializer
from rest_framework.permissions import IsAuthenticated


@api_view(['get', 'patch'])
@permission_classes([IsAuthenticated])
def profile(request):
    """
    Handles retrieval and partial update of the authenticated user's profile.

    - GET: Returns the serialized data of the current user.
    - PATCH: Partially updates the user's profile with provided data if valid.

    Args:
        request (HttpRequest): The HTTP request object containing user and data.

    Returns:
        Response: Serialized user data on success, or validation errors with
        HTTP 400 on failure.
    """
    user = request.user

    if request.method == 'GET':
        serializer = AccountSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = AccountSerializer(
            user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

